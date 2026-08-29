"""Shader-style compositing and recording for Neural Flow Lenia fields.

Pure numpy: every frame the viewer shows and every frame written to a GIF or
MP4 comes out of the same `composite()` call, so a recording is exactly what
was on screen rather than a second, differently-tuned rendering.

The look is built the way a fragment shader would build it: per-channel
emissive colour ramps, a filmic tone map, a bloom pass on the luminance, and
optional vector-flow and organism-marker overlays rasterized directly into
the pixel buffer.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import numpy as np

# Emissive colour per channel, in the order channels are stored. Chosen to
# stay distinguishable when two channels overlap and add.
CHANNEL_COLORS = np.array([
    [1.00, 0.28, 0.16],    # ember
    [0.22, 1.00, 0.55],    # bioluminescent green
    [0.30, 0.55, 1.00],    # deep cyan
    [1.00, 0.82, 0.18],    # amber
    [0.85, 0.30, 1.00],    # violet
    [0.20, 0.95, 0.95],    # teal
    [1.00, 0.55, 0.75],    # rose
    [0.65, 0.80, 0.35],    # moss
])


def _blur(x: np.ndarray, sigma: float) -> np.ndarray:
    """Separable Gaussian blur by FFT (periodic, matching the world)."""
    n = x.shape[0]
    idx = np.minimum(np.arange(n), n - np.arange(n))
    g = np.exp(-0.5 * (idx / sigma) ** 2)
    g /= g.sum()
    k = np.outer(g, g)
    return np.real(np.fft.ifft2(np.fft.fft2(x) * np.fft.fft2(k)))


def composite(A: np.ndarray, exposure: float = 1.6, gamma: float = 0.85,
              bloom: float = 0.45, bloom_sigma: float = 2.4,
              floor: float = 0.02) -> np.ndarray:
    """Multi-channel mass -> RGB float image in [0, 1].

    Normalization is per-frame against the field's own peak, so a species
    that carries little mass is still visible; the absolute scale is
    reported numerically in the viewer rather than encoded in brightness.
    """
    A = np.asarray(A, dtype=np.float64)
    peak = float(A.sum(axis=0).max())
    if peak <= 0:
        return np.zeros(A.shape[1:] + (3,))

    rgb = np.zeros(A.shape[1:] + (3,))
    for c in range(A.shape[0]):
        col = CHANNEL_COLORS[c % len(CHANNEL_COLORS)]
        v = np.clip(A[c] / peak, 0.0, None) * exposure
        rgb += v[..., None] * col[None, None, :]

    lum = rgb.mean(axis=2)
    if bloom > 0:
        glow = _blur(lum, bloom_sigma)
        rgb = rgb + bloom * glow[..., None] * np.array([0.9, 0.95, 1.0])

    rgb = rgb / (1.0 + rgb)                       # filmic knee, no clipping
    rgb = np.clip(rgb, 0.0, 1.0) ** gamma
    return np.clip(rgb + floor * (1.0 - rgb), 0.0, 1.0)


def upscale(img: np.ndarray, factor: int) -> np.ndarray:
    return np.repeat(np.repeat(img, factor, axis=0), factor, axis=1)


def _line(buf: np.ndarray, y0: float, x0: float, y1: float, x1: float,
          color: np.ndarray, alpha: float = 0.9) -> None:
    """Rasterize a segment into an RGB buffer, wrapping at the edges."""
    h, w = buf.shape[:2]
    n = max(2, int(max(abs(y1 - y0), abs(x1 - x0)) * 2))
    ys = np.linspace(y0, y1, n).astype(int) % h
    xs = np.linspace(x0, x1, n).astype(int) % w
    buf[ys, xs] = (1 - alpha) * buf[ys, xs] + alpha * color


def draw_flow(img: np.ndarray, dy: np.ndarray, dx: np.ndarray, scale_up: int,
              stride: int = 8, gain: float = 9.0,
              color=(1.0, 1.0, 1.0), alpha: float = 0.55,
              min_speed: float = 1e-3) -> np.ndarray:
    """Vector overlay of the transport field, drawn on the upscaled image.

    Arrows are only drawn where mass is actually moving, so the overlay
    shows the creature's own flow rather than a grid of noise.
    """
    out = img.copy()
    col = np.array(color)
    vy = np.asarray(dy).sum(axis=0) if dy.ndim == 3 else np.asarray(dy)
    vx = np.asarray(dx).sum(axis=0) if dx.ndim == 3 else np.asarray(dx)
    h, w = vy.shape
    for i in range(0, h, stride):
        for j in range(0, w, stride):
            ay, ax = vy[i, j], vx[i, j]
            if np.hypot(ay, ax) < min_speed:
                continue
            y0, x0 = (i + 0.5) * scale_up, (j + 0.5) * scale_up
            y1, x1 = y0 + ay * gain * scale_up, x0 + ax * gain * scale_up
            _line(out, y0, x0, y1, x1, col, alpha)
            # arrowhead
            hy, hx = y1 - y0, x1 - x0
            n = np.hypot(hy, hx) + 1e-9
            hy, hx = hy / n * scale_up * 0.9, hx / n * scale_up * 0.9
            _line(out, y1, x1, y1 - hy + hx * 0.5, x1 - hx - hy * 0.5, col, alpha)
            _line(out, y1, x1, y1 - hy - hx * 0.5, x1 - hx + hy * 0.5, col, alpha)
    return out


def draw_markers(img: np.ndarray, centroids, scale_up: int, radius: int = 7,
                 color=(1.0, 1.0, 1.0), alpha: float = 0.85) -> np.ndarray:
    """Ring markers on tracked organisms."""
    out = img.copy()
    col = np.array(color)
    for (cy, cx) in centroids:
        if not np.isfinite(cy):
            continue
        y0, x0 = (cy + 0.5) * scale_up, (cx + 0.5) * scale_up
        th = np.linspace(0, 2 * np.pi, 64)
        ys = (y0 + radius * scale_up * 0.35 * np.sin(th)).astype(int) % out.shape[0]
        xs = (x0 + radius * scale_up * 0.35 * np.cos(th)).astype(int) % out.shape[1]
        out[ys, xs] = (1 - alpha) * out[ys, xs] + alpha * col
    return out


def to_uint8(img: np.ndarray) -> np.ndarray:
    return (np.clip(img, 0, 1) * 255).astype(np.uint8)


# --------------------------------------------------------------------------
# Recording
# --------------------------------------------------------------------------


def save_gif(frames: list[np.ndarray], path: Path, fps: int = 20) -> Path:
    """Write a GIF with Pillow (always available; no external binary)."""
    from PIL import Image
    imgs = [Image.fromarray(to_uint8(f)) for f in frames]
    imgs[0].save(path, save_all=True, append_images=imgs[1:],
                 duration=int(1000 / fps), loop=0, optimize=True)
    return path


def ffmpeg_available() -> bool:
    return shutil.which("ffmpeg") is not None


def save_mp4(frames: list[np.ndarray], path: Path, fps: int = 24) -> Path | None:
    """Write an MP4 by piping raw frames to ffmpeg.

    Returns None when ffmpeg is absent, so the caller can say so plainly
    instead of shipping a silently missing file.
    """
    if not ffmpeg_available():
        return None
    h, w = frames[0].shape[:2]
    if h % 2 or w % 2:
        frames = [f[:h - h % 2, :w - w % 2] for f in frames]
        h, w = frames[0].shape[:2]
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo",
           "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-",
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", str(path)]
    proc = subprocess.run(
        cmd, input=b"".join(to_uint8(f).tobytes() for f in frames),
        capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {proc.stderr.decode()[:400]}")
    return path

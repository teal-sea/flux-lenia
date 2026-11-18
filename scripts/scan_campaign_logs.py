"""Scan retained machine logs for common credential forms, never print values."""
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = {
    'private_key': r'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----',
    'github': r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b',
    'api_token': r'\b(?:sk-(?:proj-)?[A-Za-z0-9_-]{20,}|xox[baprs]-[A-Za-z0-9-]{15,}|AKIA[A-Z0-9]{16})\b',
    'credential_assignment': r'(?i)\b(?:api[_-]?key|access[_-]?token|auth[_-]?token|password|secret[_-]?key)\b\s*[:=]\s*[\"\']?[A-Za-z0-9_./+\-=]{12,}',
    'bearer': r'(?i)\bBearer\s+[A-Za-z0-9_./+\-=]{16,}',
    'url_password': r'https?://[^\s/:]+:[^\s/@]+@',
    'jwt': r'\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b',
}


def main():
    files = [ROOT / 'outputs/campaign.log', *sorted((ROOT / 'outputs/logs').glob('*.log')),
             *sorted(p for p in (ROOT / 'outputs/gpu_machine_logs').rglob('*') if p.is_file()),
             ROOT / 'campaign_gpu/evidence/gpu_collector.log']
    hits, manifest = [], []
    for p in files:
        raw = p.read_bytes()
        manifest.append({'path': str(p.relative_to(ROOT)), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
        for line, text in enumerate(raw.decode().splitlines(), 1):
            for name, pattern in PATTERNS.items():
                if re.search(pattern, text):
                    hits.append({'path': str(p.relative_to(ROOT)), 'line': line, 'pattern': name})
    receipt = {'files': len(files), 'bytes': sum(x['bytes'] for x in manifest), 'patterns': PATTERNS,
               'hits': hits, 'manifest': manifest,
               'limit': 'Pattern scan, not a proof that arbitrary secrets are absent. Machine IDs, IP addresses, paths and checksums are operational metadata, not credentials.'}
    (ROOT / 'campaign_gpu/evidence/secret-scan.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'files': len(files), 'hits': hits}))
    if hits:
        raise SystemExit(1)


if __name__ == '__main__':
    main()

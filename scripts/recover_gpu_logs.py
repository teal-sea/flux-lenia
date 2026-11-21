"""Recover distinct per-machine logs and JSON hashes from retained fleet tar files.

Usage: python scripts/recover_gpu_logs.py PULLED_ARCHIVE_DIRECTORY
Archives are read, never changed. No network or execution on remote machines.
"""
import csv
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys
import tarfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    source = Path(sys.argv[1])
    fleet = json.loads((ROOT / 'campaign_gpu/gpu_boxes.json').read_text())
    rows, receipts = [], []
    for box, info in sorted(fleet['boxes'].items()):
        archive = source / (box + '.tar')
        digest = hashlib.file_digest(archive.open('rb'), 'sha256').hexdigest()
        assert digest == info['sha256'], box
        logs = 0
        with tarfile.open(archive) as tf:
            for member in tf:
                path = PurePosixPath(member.name)
                assert not path.is_absolute() and '..' not in path.parts
                if not member.isfile():
                    continue
                if member.name.startswith('out/logs/') or member.name == 'out/campaign.log':
                    destination = ROOT / 'outputs/gpu_machine_logs' / box / Path(*path.parts[1:])
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    stream = tf.extractfile(member)
                    assert stream is not None
                    destination.write_bytes(stream.read())
                    logs += 1
                elif member.name.endswith('_food1.json'):
                    stream = tf.extractfile(member)
                    assert stream is not None
                    raw = stream.read()
                    result = 'outputs/' + '/'.join(path.parts[1:])
                    digest_result = hashlib.sha256(raw).hexdigest()
                    rows.append([box, result, digest_result])
                    current = ROOT / result
                    if current.exists() and hashlib.sha256(current.read_bytes()).hexdigest() != digest_result:
                        alternate = ROOT / 'outputs/gpu_machine_logs' / box / 'alternate_results' / Path(*path.parts[1:])
                        alternate.parent.mkdir(parents=True, exist_ok=True)
                        alternate.write_bytes(raw)
        receipts.append({'box': box, 'archive_sha256': digest, 'logs': logs})
    evidence = ROOT / 'campaign_gpu/evidence'
    with (evidence / 'l4-result-hashes.tsv').open('w') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n'); w.writerow(['box','result','sha256']); w.writerows(rows)
    (evidence / 'machine-log-recovery.json').write_text(json.dumps(receipts, indent=2) + '\n')
    print(json.dumps({'archives_verified': len(receipts), 'logs_recovered': sum(x['logs'] for x in receipts), 'json_members': len(rows)}))


if __name__ == '__main__':
    main()

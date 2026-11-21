"""Read-only result audit and evidence tables. Standard library, no simulation.

Run from the repo root: python scripts/gpu_campaign_audit.py
Writes only campaign_gpu/evidence and the missing-run shard.
"""
import csv
import hashlib
import itertools
import json
from pathlib import Path
import re
import shlex
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'campaign_gpu/evidence'
ARMS = ('treat', 'neutral_plus', 'neutral_minus')


def seeds(text):
    result = []
    for part in text.split(','):
        if '-' in part:
            a, b = map(int, part.split('-'))
            result.extend(range(a, b + 1))
        else:
            result.append(int(part))
    return result


def main():
    OUT.mkdir(exist_ok=True)
    planned = defaultdict(list)
    collisions = []
    for shard in sorted((ROOT / 'campaign_gpu/shards').glob('box*.tsv')):
        ids = defaultdict(list)
        for line, row in enumerate(csv.reader(shard.open(), delimiter='\t'), 1):
            ident, outrel, count, args = row
            ids[ident].append(outrel)
            av = shlex.split(args)
            opts = dict(zip(av[::2], av[1::2]))
            for seed, arm in itertools.product(seeds(opts['--seeds']), opts['--arms'].split(',')):
                planned[(outrel, opts['--species'], seed, arm)].append(
                    f'{shard.relative_to(ROOT)}:{line}')
        for ident, dirs in ids.items():
            if len(dirs) > 1:
                collisions.append({'shard': str(shard.relative_to(ROOT)), 'id': ident, 'outputs': dirs})
    archived = defaultdict(list)
    for row in csv.DictReader((OUT / 'l4-result-hashes.tsv').open(), delimiter='\t'):
        archived[(row['result'], row['sha256'])].append(row['box'])
    inventory = []
    mismatches = []
    missing = []
    for experiment, n in [('horizon300k_20261117', 50), ('species_scan_20261117', 20),
                          ('food_sensing_2x2_gpu', 50)]:
        base = ROOT / 'outputs' / experiment
        for cell in sorted(base.iterdir()):
            if not cell.is_dir() or not re.fullmatch(r'SPECIES_\d{3}_[A-Z0-9]+_fs[\d.]+_k[\d.]+_per_channel', cell.name):
                continue
            present = set()
            for path in sorted(cell.glob('*_food1.json')):
                d = json.loads(path.read_text())
                sp, seed, arm = d['species'], d['seed'], d['arm']
                present.add((seed, arm))
                rel = str(cell.relative_to(ROOT / 'outputs'))
                cpu_log = cell / f'run_{sp}_s{seed}_{arm}.log'
                cpu = None
                if cpu_log.exists():
                    for line in cpu_log.read_text().splitlines():
                        try:
                            candidate = json.loads(line)
                            if 'wall_seconds' in candidate:
                                cpu = candidate
                        except json.JSONDecodeError:
                            pass
                if experiment == 'food_sensing_2x2_gpu':
                    hardware, source = 'A100', 'docs/FOOD-SENSING-2x2-GPU-2026-11-16.md:7-19'
                elif cpu and cpu['wall_seconds'] == d['wall_seconds']:
                    hardware, source = 'rented CPU', str(cpu_log.relative_to(ROOT))
                else:
                    assert (rel, sp, seed, arm) in planned, f'No hardware evidence: {path}'
                    hardware = 'L4'
                    digest = hashlib.sha256(path.read_bytes()).hexdigest()
                    matching_boxes = archived[(str(path.relative_to(ROOT)), digest)]
                    assert matching_boxes, f'No exact archived L4 result: {path}'
                    source = ';'.join('outputs/gpu_machine_logs/' + box + '/campaign.log' for box in matching_boxes)
                    if cpu:
                        mismatches.append(str(path.relative_to(ROOT)))
                inventory.append([str(path.relative_to(ROOT)), hardware, source,
                                  hashlib.sha256(path.read_bytes()).hexdigest()])
            for seed, arm in itertools.product(range(1, n + 1), ARMS):
                if (seed, arm) not in present:
                    missing.append([experiment, cell.name, seed, arm])
    with (OUT / 'run-hardware.tsv').open('w') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n'); w.writerow(['result', 'hardware', 'evidence', 'sha256']); w.writerows(inventory)
    grouped = defaultdict(Counter)
    for path, hw, source, sha in inventory:
        grouped[str(Path(path).parent)][hw] += 1
    lines = ['# Hardware by cell', '', '| cell | rented CPU | A100 | L4 | mixed |', '|---|---|---|---|---|']
    for cell, counts in sorted(grouped.items()):
        lines.append(f'| {cell} | {counts["rented CPU"]} | {counts["A100"]} | {counts["L4"]} | {"yes" if len(counts)>1 else "no"} |')
    (OUT / 'hardware-cells.md').write_text('\n'.join(lines) + '\n')
    scan_missing = [m for m in missing if m[0] == 'species_scan_20261117']
    assert len(scan_missing) == 27
    assert {m[1] for m in scan_missing} == {'SPECIES_003_VAGRANT_fs0_k3_per_channel'}
    wanted = sorted({m[2] for m in scan_missing})
    assert {(m[2], m[3]) for m in scan_missing} == set(itertools.product(wanted, ARMS))
    target = 'species_scan_20261117/SPECIES_003_VAGRANT_fs0_k3_per_channel'
    args = ('--species SPECIES_003_VAGRANT --arms ' + ','.join(ARMS) + ' --seeds ' + ','.join(map(str,wanted))
            + ' --steps 30000 --sample-every 100 --frame-every 15000 --transport per_channel --kappa 3 --food-sense 0 --food 1 --batch 64')
    (ROOT / 'campaign_gpu/shards/missing-vagrant-fs0-k3.tsv').write_text(
        f'SPECIES_003_VAGRANT_fs0_k3_per_channel\t{target}\t27\t{args}\n')
    archive_paths = defaultdict(list)
    for (path, digest), boxes in archived.items():
        archive_paths[path].extend(boxes)
    duplicate_cells = Counter(str(Path(path).parent) for path, boxes in archive_paths.items() if len(boxes) > 1)
    receipt = {'totals': dict(Counter(row[1] for row in inventory)), 'runs_labelled': len(inventory),
               'l4_archive_json_members': sum(len(v) for v in archived.values()),
               'l4_archive_unique_paths': len(archive_paths),
               'l4_duplicate_paths_by_cell': dict(duplicate_cells),
               'mixed_cells': sum(len(c)>1 for c in grouped.values()), 'missing': missing,
               'id_collisions': collisions, 'cpu_log_result_mismatches': mismatches,
               'method': 'CPU requires exact wall_seconds equality with retained per-run stdout JSON. Other final-campaign runs require membership in an L4 shard and an exact SHA-256 match with a JSON member of a checksum-verified machine archive. A100 venue is recorded in the 2x2 execution doc. CudaDevice logs corroborate the fleet. Raw result hashes pin the labelled bytes.'}
    (OUT / 'audit.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({k:v for k,v in receipt.items() if k not in ('missing','method')},indent=2))


if __name__ == '__main__':
    main()

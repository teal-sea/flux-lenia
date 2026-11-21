"""Runner integration regression using a fake batch writer, never a simulation."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

RUNNER = Path(os.environ.get('RUN_SHARD', str(Path(__file__).with_name('run_shard.sh')))).resolve()


class RunnerTest(unittest.TestCase):
    def test_batch_identity_resume_and_failure(self):
        for legacy in (False, True):
            with self.subTest(legacy_marker=legacy):
                self.exercise(legacy)

    def exercise(self, legacy):
        with tempfile.TemporaryDirectory(dir=os.environ['TMPDIR']) as tmp:
            root = Path(tmp)
            (root / 'code/scripts').mkdir(parents=True)
            (root / 'venv/bin').mkdir(parents=True)
            (root / 'venv/bin/python').symlink_to('/usr/bin/python3')
            (root / 'code/scripts/gpu_batch.py').write_text(
                "import sys\nfrom pathlib import Path\n"
                "a=sys.argv; out=Path(a[a.index('--outdir')+1]); out.mkdir(parents=True,exist_ok=True)\n"
                "with (out.parent/'calls').open('a') as f: f.write(str(out)+'\\n')\n"
                "if '--fail' in a: sys.exit(2)\n"
                "seed=a[a.index('--seed')+1]\n"
                "(out/('s'+seed+'_food1.json')).write_text('{}')\n")
            shard = root / 'shard.tsv'
            shard.write_text('same\thorizon/cell\t1\t--seed 1\n'
                             'same\tscan/cell\t1\t--seed 1\n'
                             'same\tscan/cell\t2\t--seed 2\n')
            (root / 'out').mkdir()
            (root / 'out/campaign.log').write_text('old DONE same runs=1\n' if legacy else '')
            env = dict(os.environ, FL=str(root))
            def run():
                return subprocess.run(['bash', str(RUNNER), str(shard)], env=env,
                                      capture_output=True, text=True)
            first = run()
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            self.assertTrue((root / 'out/horizon/cell/s1_food1.json').exists())
            self.assertTrue((root / 'out/scan/cell/s1_food1.json').exists())
            self.assertTrue((root / 'out/scan/cell/s2_food1.json').exists())
            self.assertEqual(len(list((root / 'out/logs').glob('*.log'))), 3)
            second = run()
            self.assertEqual(second.returncode, 0)
            self.assertEqual(second.stdout.count('(DONE)'), 3)
            self.assertEqual(len((root / 'out/scan/calls').read_text().splitlines()), 2)
            shard.write_text('same\tfailure/cell\t1\t--seed 1 --fail\n')
            failure = run()
            self.assertEqual(failure.returncode, 1)
            self.assertIn('FINISHED_WITH_FAILURES', failure.stdout)
            self.assertFalse(any(line.endswith('Z ALL_DONE') for line in failure.stdout.splitlines()))
            self.assertNotIn(' DONE batch=', failure.stdout)
            self.assertIn('FAIL batch=', run().stdout)


if __name__ == '__main__':
    unittest.main()

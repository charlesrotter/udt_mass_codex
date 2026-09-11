"""Unchanged-program banking replay; no scientific implementation or source edits."""
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CAPTURE = ROOT / 'udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py'
PLAN = json.loads((HERE / 'ADDITIONAL_REPLAY_PLAN.json').read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
env = dict(os.environ)
threads = {k: '1' for k in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS']}
env.update(threads)
env['PYTHONDONTWRITEBYTECODE'] = '1'
results = []
for row in PLAN:
    script, saved = ROOT / row['script'], ROOT / row['saved_stdout']
    assert sha(script) == row['script_sha256']
    assert sha(saved) == row['saved_stdout_sha256']
    stem = HERE / 'replays' / row['label']
    command = [sys.executable, '-B', str(CAPTURE), str(stem), str(ROOT),
               sys.executable, '-B', str(script)] + row['args']
    result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, timeout=65)
    with Path(str(stem) + '.launcher.stdout').open('xb') as f:
        f.write(result.stdout)
    with Path(str(stem) + '.launcher.stderr').open('xb') as f:
        f.write(result.stderr)
    receipt = json.loads(Path(str(stem) + '.json').read_text())
    output = Path(str(stem) + '.stdout')
    item = dict(row, launcher_argv=command, launcher_returncode=result.returncode,
                capture_sha256=sha(CAPTURE), thread_environment=threads,
                dont_write_bytecode=True, python=sys.version,
                platform=platform.platform(), receipt=receipt,
                stdout_sha256=sha(output),
                stdout_byte_identical=output.read_bytes() == saved.read_bytes(),
                script_unchanged=sha(script) == row['script_sha256'],
                saved_output_unchanged=sha(saved) == row['saved_stdout_sha256'])
    with Path(str(stem) + '.comparison.json').open('x') as f:
        json.dump(item, f, indent=2)
        f.write('\n')
    results.append(item)
    print(row['label'], 'exit', receipt['returncode'], 'bytes_equal', item['stdout_byte_identical'], flush=True)
with (HERE / 'ADDITIONAL_REPLAY_RESULTS.json').open('x') as f:
    json.dump(results, f, indent=2)
    f.write('\n')
assert all(r['receipt']['returncode'] == 0 and r['script_unchanged'] and r['saved_output_unchanged'] for r in results)

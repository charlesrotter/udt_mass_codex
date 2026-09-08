"""Post-seal same-code regression and precise declared mutation replay."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

repo = Path.cwd()
review = Path(__file__).resolve().parent
step = review.parent
runner = repo / 'udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py'
assert hashlib.sha256((step/'check_cf1.py').read_bytes()).hexdigest() == '3272d699a432c86f4137505a99e44af18588e942fcf310d375acde35ee7367c9'
assert hashlib.sha256((step/'CANDIDATE_INITIAL.md').read_bytes()).hexdigest() == '35263178061ec4ad2e65add33b43e8f66c008a6447a76bf2fb1263f8f42b92ea'
expected = {
    'baseline': [],
    'integer_only': ['closure_3/2','closure_2/3','closure_7/5','closure_5/7',
                     'rational_sampling_false_pass_retained'],
    'all_rational_regular': ['regular_3/2','regular_2/3','regular_7/5','regular_5/7'],
    'wrong_period': ['interior_period_3/2','interior_period_2/3',
                     'interior_period_7/5','interior_period_5/7'],
    'swap_axes': ['axis_holonomy_orders_3/2','axis_holonomy_orders_2/3',
                  'axis_holonomy_orders_7/5','axis_holonomy_orders_5/7'],
}
rows = []
for mode, failed in expected.items():
    prefix = review / ('author_replay_' + mode)
    command = [sys.executable, '-B', str(runner), str(prefix), str(repo),
               sys.executable, '-B', str(step/'check_cf1.py'), mode]
    process = subprocess.run(command, capture_output=True, text=True)
    receipt = json.loads(prefix.with_suffix('.json').read_text())
    result = json.loads(prefix.with_suffix('.stdout').read_text())
    expected_exit = 0 if mode == 'baseline' else 1
    assert process.returncode == receipt['returncode'] == expected_exit
    assert receipt['timeout'] is False
    assert prefix.with_suffix('.stderr').read_bytes() == b''
    assert result['failed'] == failed, result
    saved = (step / ('check_' + mode + '.stdout')).read_bytes()
    replay = prefix.with_suffix('.stdout').read_bytes()
    assert saved == replay
    rows.append({'mode': mode, 'actual_returncode': receipt['returncode'],
                 'failed_guards': result['failed'], 'passed': result['passed'],
                 'saved_stdout_byte_identical': saved == replay,
                 'wrapper_stdout': process.stdout, 'wrapper_stderr': process.stderr})
print(json.dumps({'kind': 'same-code regression, not implementation independence',
                  'rows': rows, 'all_expected_outcomes': True,
                  'thread_environment': {k: os.environ.get(k) for k in
                   ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']}}, indent=2))

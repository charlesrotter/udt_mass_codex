"""Tiny CPU-only checkpoint adversarial regressions; no scientific certification."""
from pathlib import Path
import hashlib
import importlib.util
import json
import platform
import resource
import sys
import time

resource.setrlimit(resource.RLIMIT_AS, (2 * 1024**3, 2 * 1024**3))
HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parent.parent
ROOT = PACKAGE.parent
started = time.monotonic()
spec = importlib.util.spec_from_file_location('smk_scope_checkpoint', PACKAGE / 'checkpoint_io.py')
cp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cp)
import numpy as np

fixtures = HERE / 'cpu_fixtures'
fixtures.mkdir(exist_ok=False)
state = np.arange(160, dtype=np.float64).reshape(1, 5, 32) / 160
signature = {'spec': 'scope-spec', 'rhs': 'scope-rhs'}
results = {}

def rejected(name, expected, call):
    try:
        call()
    except cp.CheckpointError as exc:
        results[name] = {'passed': str(exc) == expected, 'actual': str(exc), 'expected': expected}
    else:
        results[name] = {'passed': False, 'actual': 'accepted', 'expected': expected}

run = fixtures / 'roundtrip'
run.mkdir()
folder = cp.save(run, signature, state, 10, 1.1, 1024**2)
loaded, step, t, selected = cp.load_latest(run, signature, state.shape, .01, 4.)
results['committed_roundtrip'] = {'passed': np.array_equal(loaded, state) and step == 10 and t == 1.1 and selected == folder}
uncommitted = run / 'checkpoints' / 'ckpt_000000099_later_incomplete'
uncommitted.mkdir()
(uncommitted / 'state.npz').write_bytes(b'incomplete diagnostic payload')
results['later_uncommitted_ignored'] = {'passed': cp.load_latest(run, signature, state.shape, .01, 4.)[3] == folder}
rejected('changed_signature', 'SPEC_OR_CODE_MISMATCH', lambda: cp.load_latest(run, {'spec': 'changed'}, state.shape, .01, 4.))
payload_path = folder / 'state.npz'
payload_before = payload_path.read_bytes()
(HERE / 'fixture_payload_before_corruption.npz').write_bytes(payload_before)
payload_path.write_bytes(payload_before + b'corruption')
rejected('committed_corruption', 'PAYLOAD_HASH_MISMATCH', lambda: cp.load_latest(run, signature, state.shape, .01, 4.))
bad = state.copy()
bad[0, 0, 0] = float('nan')
rejected('nonfinite_state', 'NONFINITE_OR_WRONG_DTYPE', lambda: cp.save(run, signature, bad, 11, 1.11, 1024**2))
rejected('tiny_output_limit', 'OUTPUT_BUDGET', lambda: cp.save(run, signature, state, 11, 1.11, 1))
source = ROOT / 'udt_gpu_time_live_discovery_2026-09-30/evolve.py'
launch = json.loads((PACKAGE / 'LAUNCH.json').read_text())
results['NGD1_source_matches_launch'] = {'passed': hashlib.sha256(source.read_bytes()).hexdigest() == launch['source_sha256']}
result = {
    'status': 'PASS' if all(v['passed'] for v in results.values()) else 'FAIL',
    'python': sys.version,
    'numpy': np.__version__,
    'platform': platform.platform(),
    'elapsed_seconds': time.monotonic() - started,
    'gpu_used': False,
    'checks': results,
    'source_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in (PACKAGE/'WORK_ORDER.md', PACKAGE/'checkpoint_io.py', PACKAGE/'smoke_runner.py', source)},
    'limits': 'CPU regression of checkpoint library; not independent dynamics or general 3D certification',
}
(HERE / 'CPU_CHECK_RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
raise SystemExit(0 if result['status'] == 'PASS' else 1)

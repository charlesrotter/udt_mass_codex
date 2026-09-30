"""CPU-only adversarial controls against the initial preserved SMK1 source."""
from pathlib import Path
import contextlib, fcntl, hashlib, importlib.util, io, json, resource, sys, time
from unittest.mock import patch
import numpy as np

HERE = Path(__file__).resolve().parent
SNAP = HERE / 'initial_source'
ROOT = HERE.parents[2]
sys.path.insert(0, str(SNAP))
import checkpoint_io as ck
ms = importlib.util.spec_from_file_location('reviewed_runner', SNAP / 'smoke_runner.py')
runner = importlib.util.module_from_spec(ms)
ms.loader.exec_module(runner)
runner.SOURCE = ROOT / 'udt_gpu_time_live_discovery_2026-09-30/evolve.py'
OUT = HERE / 'initial_fixtures'
OUT.mkdir(exist_ok=False)
started = time.monotonic()
results = []
base = np.zeros((1, 5, 32), dtype=np.float64)
signature = {'test': 'synthetic filesystem fixture'}

def record(name, observed, **kw):
    value = {'name': name, 'observed': observed, **kw}
    results.append(value)
    print(json.dumps(value), flush=True)

def rejected(name, thunk, wanted):
    try:
        thunk()
    except Exception as e:
        assert str(e) == wanted, (name, type(e).__name__, str(e), wanted)
        record(name, 'REJECTED_AS_EXPECTED', reason=str(e))
    else:
        raise AssertionError(f'{name}: unexpected acceptance')

def fixture(name):
    run = OUT / name
    run.mkdir()
    first = ck.save(run, signature, base, 0, 1., 1024 * 1024)
    return run, first

run, first = fixture('identity_and_partial')
loaded = ck.load_latest(run, signature, base.shape, .1, 4)
assert np.array_equal(loaded[0], base)
record('identity', 'PASS')
later = run / 'checkpoints' / 'ckpt_000000001_partial'
later.mkdir()
(later / 'state.npz').write_bytes(b'incomplete payload')
assert ck.load_latest(run, signature, base.shape, .1, 4)[3] == first
record('uncommitted_later_payload', 'PRIOR_COMMITTED_RECOVERED')

run, first = fixture('marker_create_before_write')
later = run / 'checkpoints' / 'ckpt_000000001_interrupted'
later.mkdir()
for name in ('state.npz', 'metadata.json'):
    (later / name).write_bytes((first / name).read_bytes())
# This is the concrete state after open('xb') but before f.write(...).
(later / 'COMMITTED').open('xb').close()
rejected('interrupted_marker_blocks_recovery',
         lambda: ck.load_latest(run, signature, base.shape, .1, 4),
         'METADATA_HASH_MISMATCH')
record('interrupted_marker_verdict', 'DEFECT_REPRODUCED',
       reason='An uncommitted marker prevents recovery of earlier valid checkpoint')

for target, expected in [('state.npz', 'PAYLOAD_HASH_MISMATCH'),
                         ('metadata.json', 'METADATA_HASH_MISMATCH')]:
    run, first = fixture('corrupt_' + target.replace('.', '_'))
    with (first / target).open('ab') as f:
        f.write(b'corruption')
    rejected('corrupt_' + target,
             lambda: ck.load_latest(run, signature, base.shape, .1, 4), expected)

run, first = fixture('signature_mismatch')
rejected('changed_signature', lambda: ck.load_latest(run, {}, base.shape, .1, 4),
         'SPEC_OR_CODE_MISMATCH')
bad = base.copy(); bad[0, 0, 0] = np.nan
rejected('nonfinite_save', lambda: ck.save(run, signature, bad, 1, 1.1, 1024 ** 2),
         'NONFINITE_OR_WRONG_DTYPE')
rejected('tiny_output', lambda: ck.save(run, signature, base, 1, 1.1, 1),
         'OUTPUT_BUDGET')

spec = {'dt': 1., 'end': 4., 'n': 32, 'checkpoint_steps': 1,
        'cases': [{'id': 'synthetic_empty_modes'}], 'k': 1., 'wall_seconds': 5,
        'gpu_bytes': 1024 ** 2, 'output_bytes': 1024 ** 2}
specfile = OUT / 'spec.json'; specfile.write_bytes(ck.json_bytes(spec))
lockfile = OUT / 'owned.lock'
run = OUT / 'rejected_endpoint'; run.mkdir()
bad = base.copy(); bad[0, 4] = np.sin(np.arange(32) * 2 * np.pi / 32)
residual = np.max(np.abs(np.fft.ifft(1j * np.fft.fftfreq(32, 1/32)
                                   * np.fft.fft(bad[0, 4])).real))
assert residual > 0.99
sig = runner.signature(spec)
ck.save(run, sig, bad, 3, 4., 1024 ** 2)
def invoke_runner(argv):
    with patch.object(sys, 'argv', ['smoke_runner.py'] + argv):
        return runner.main()

rejected('existing_run',
         lambda: invoke_runner([str(specfile), str(run), '--lock', str(lockfile)]),
         'REFUSE_EXISTING_RUN')
with lockfile.open('a+') as lock:
    fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    rejected('concurrent_cooperative_lock',
             lambda: invoke_runner([str(specfile), str(run), '--resume',
                                    '--lock', str(lockfile)]), 'GPU_WORKER_LOCKED')

import torch
orig_as_tensor = torch.as_tensor
orig_fftfreq = torch.fft.fftfreq
def cpu_as_tensor(*args, **kw):
    kw['device'] = 'cpu'; return orig_as_tensor(*args, **kw)
def cpu_fftfreq(*args, **kw):
    kw['device'] = 'cpu'; return orig_fftfreq(*args, **kw)
captured = io.StringIO()
with patch.object(torch.cuda, 'is_available', return_value=True), \
     patch.object(torch.cuda, 'reset_peak_memory_stats'), \
     patch.object(torch.cuda, 'get_device_name', return_value='CPU_MOCK_NO_CUDA'), \
     patch.object(torch, 'as_tensor', side_effect=cpu_as_tensor), \
     patch.object(torch.fft, 'fftfreq', side_effect=cpu_fftfreq), \
     contextlib.redirect_stdout(captured):
    rc = invoke_runner([str(specfile), str(run), '--resume', '--lock', str(lockfile)])
output = captured.getvalue()
(OUT / 'endpoint_mock_stdout.txt').write_text(output)
assert rc == 0 and 'SMOKE_CONTROL_COMPLETE' in output
record('constraint_rejected_endpoint_resume', 'DEFECT_REPRODUCED',
       independent_constraint_max=float(residual), returncode=rc,
       runner_stdout=output.strip(), mock='CUDA calls mapped to CPU; no GPU used')

result = {'status': 'INITIAL_CANDIDATE_REFUTED', 'checks': results,
          'elapsed_seconds': time.monotonic() - started,
          'max_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
          'versions': {'python': sys.version, 'numpy': np.__version__,
                       'torch': torch.__version__},
          'source_hashes': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                            for p in SNAP.iterdir() if p.is_file()}}
assert result['elapsed_seconds'] < 180 and result['max_rss_kib'] < 2 * 1024 ** 2
(HERE / 'INITIAL_DIAGNOSTIC_RESULT.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k != 'checks'}), flush=True)

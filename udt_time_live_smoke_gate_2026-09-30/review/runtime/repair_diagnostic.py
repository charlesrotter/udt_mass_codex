"""CPU-only fault injection against hash-frozen repaired SMK1 source."""
from pathlib import Path
import contextlib, hashlib, importlib.util, io, json, resource, sys, time
from unittest.mock import patch
import numpy as np

HERE = Path(__file__).resolve().parent
SNAP = HERE / 'repaired_source'
ROOT = HERE.parents[2]
sys.path.insert(0, str(SNAP))
import checkpoint_io as ck
ms = importlib.util.spec_from_file_location('reviewed_runner', SNAP / 'smoke_runner.py')
runner = importlib.util.module_from_spec(ms); ms.loader.exec_module(runner)
runner.SOURCE = ROOT / 'udt_gpu_time_live_discovery_2026-09-30/evolve.py'
OUT = HERE / 'repair_fixtures'; OUT.mkdir(exist_ok=False)
started = time.monotonic(); results = []
base = np.zeros((1, 5, 32), dtype=np.float64)
signature = {'test': 'synthetic filesystem fixture'}

class InjectedInterruption(Exception):
    pass

def record(name, **kw):
    value = {'name': name, 'status': 'PASS', **kw}
    results.append(value); print(json.dumps(value), flush=True)

def rejected(thunk, wanted):
    try:
        thunk()
    except ck.CheckpointError as e:
        assert str(e) == wanted, (str(e), wanted)
        return
    raise AssertionError(f'Expected rejection {wanted}')

def fixture(name):
    run = OUT / name; run.mkdir()
    first = ck.save(run, signature, base, 0, 1., 1024 ** 2)
    return run, first

original_exclusive = ck.exclusive
original_link = ck.os.link
for when in ('during_pending_create', 'before_publication', 'after_publication'):
    run, first = fixture(when)
    def interrupted_exclusive(path, data):
        if Path(path).name == 'COMMITTED.pending':
            Path(path).open('xb').close()
            raise InjectedInterruption(when)
        return original_exclusive(path, data)
    def interrupted_link(src, dst):
        folder = Path(src).parent
        assert Path(src).read_text().strip() == ck.digest((folder / 'metadata.json').read_bytes())
        if when == 'after_publication':
            original_link(src, dst)
        raise InjectedInterruption(when)
    target = 'exclusive' if when == 'during_pending_create' else 'os.link'
    with contextlib.ExitStack() as stack:
        if target == 'exclusive':
            stack.enter_context(patch.object(ck, 'exclusive', side_effect=interrupted_exclusive))
        else:
            stack.enter_context(patch.object(ck.os, 'link', side_effect=interrupted_link))
        try:
            ck.save(run, signature, base + 1., 1, 1.1, 1024 ** 2)
        except InjectedInterruption:
            pass
        else:
            raise AssertionError('Injection did not occur')
    state, step, _, selected = ck.load_latest(run, signature, base.shape, .1, 4)
    expected = 1 if when == 'after_publication' else 0
    assert step == expected and np.array_equal(state, base + expected)
    if expected == 0:
        assert selected == first
    record(when, selected_step=step)

run, first = fixture('diagnostic_exclusion')
bad = base.copy(); bad[0, 0, 0] = np.nan
diagnostic = ck.save(run, signature, bad, 1, 1.1, 1024 ** 2, diagnostic='TEST_FAILURE')
assert (diagnostic / 'DIAGNOSTIC').is_file() and not (diagnostic / 'COMMITTED').exists()
assert json.loads((diagnostic / 'metadata.json').read_text())['eligible_for_resume'] is False
assert ck.load_latest(run, signature, base.shape, .1, 4)[3] == first
record('diagnostic_exclusion', nonfinite_diagnostic_preserved=True)

run, first = fixture('payload_corrupt')
with (first / 'state.npz').open('ab') as f:
    f.write(b'corruption')
rejected(lambda: ck.load_latest(run, signature, base.shape, .1, 4), 'PAYLOAD_HASH_MISMATCH')
record('committed_corruption_still_rejected')

folder = OUT / 'publish_no_overwrite'; folder.mkdir()
(folder / 'COMMITTED').write_bytes(b'original')
try:
    ck.publish_marker(folder, 'COMMITTED', b'new marker')
except FileExistsError:
    pass
else:
    raise AssertionError('Overwrote committed marker')
assert (folder / 'COMMITTED').read_bytes() == b'original'
record('marker_no_overwrite')

spec = {'dt': 1., 'end': 4., 'n': 32, 'checkpoint_steps': 1,
        'cases': [{'id': 'synthetic_empty_modes'}], 'k': 1., 'wall_seconds': 5,
        'gpu_bytes': 1024 ** 2, 'output_bytes': 1024 ** 2}
specfile = OUT / 'spec.json'; specfile.write_bytes(ck.json_bytes(spec))
lockfile = OUT / 'owned.lock'
import torch
original_as_tensor = torch.as_tensor; original_fftfreq = torch.fft.fftfreq
def cpu_as_tensor(*args, **kw):
    kw['device'] = 'cpu'; return original_as_tensor(*args, **kw)
def cpu_fftfreq(*args, **kw):
    kw['device'] = 'cpu'; return original_fftfreq(*args, **kw)

for case in ('large_constraint', 'nonfinite_derived_constraint', 'valid_endpoint'):
    run = OUT / case; run.mkdir()
    state = base.copy()
    if case == 'large_constraint':
        state[0, 4] = np.sin(np.arange(32) * 2 * np.pi / 32)
    if case == 'nonfinite_derived_constraint':
        state[0, 0] = 1000.
    assert np.isfinite(state).all()
    sig = runner.signature(spec)
    checkpoint = ck.save(run, sig, state, 3, 4., 1024 ** 2)
    captured = io.StringIO()
    with patch.object(torch.cuda, 'is_available', return_value=True), \
         patch.object(torch.cuda, 'reset_peak_memory_stats'), \
         patch.object(torch.cuda, 'max_memory_allocated', return_value=0), \
         patch.object(torch.cuda, 'get_device_name', return_value='CPU_MOCK_NO_CUDA'), \
         patch.object(torch, 'as_tensor', side_effect=cpu_as_tensor), \
         patch.object(torch.fft, 'fftfreq', side_effect=cpu_fftfreq), \
         patch.object(sys, 'argv', ['smoke_runner.py', str(specfile), str(run),
                                   '--resume', '--lock', str(lockfile)]), \
         contextlib.redirect_stdout(captured):
        if case == 'valid_endpoint':
            assert runner.main() == 0
        else:
            rejected(runner.main, 'CONSTRAINT_LIMIT')
    output = captured.getvalue()
    (run / 'mock_stdout.txt').write_text(output)
    if case == 'valid_endpoint':
        assert 'SMOKE_CONTROL_COMPLETE' in output
    else:
        assert 'SMOKE_CONTROL_COMPLETE' not in output
        diagnoses = list((run / 'diagnostics').glob('ckpt_*'))
        assert len(diagnoses) == 1 and (diagnoses[0] / 'DIAGNOSTIC').is_file()
        assert len(list((run / 'checkpoints').glob('ckpt_*'))) == 1
    record(case, expected='COMPLETE' if case == 'valid_endpoint' else 'CONSTRAINT_LIMIT',
           mock='CUDA calls mapped to CPU; no GPU used')

result = {'status': 'REPAIRED_RUNTIME_CHECKS_PASS', 'checks': results,
          'elapsed_seconds': time.monotonic() - started,
          'max_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
          'versions': {'python': sys.version, 'numpy': np.__version__, 'torch': torch.__version__},
          'source_hashes': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                            for p in SNAP.iterdir() if p.is_file()}}
assert result['elapsed_seconds'] < 180 and result['max_rss_kib'] < 2 * 1024 ** 2
(HERE / 'REPAIR_DIAGNOSTIC_RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k:v for k,v in result.items() if k != 'checks'}), flush=True)

"""Independent direct reading of parent-produced repaired runtime evidence.

CPU, <=180 seconds/2 GiB. This follow-up is designed after seeing the parent
result and verifies saved-byte restart identity and quoted engineering records;
it does not rerun CUDA or re-prove original-metric science.
"""
from pathlib import Path
import hashlib, json, resource, time
import numpy as np

HERE = Path(__file__).resolve().parent
PKG = HERE.parents[1]
EXEC = PKG / 'execution_repaired'
started = time.monotonic()
digest = lambda raw: hashlib.sha256(raw).hexdigest()
result = json.loads((EXEC / 'SMOKE_RESULT.json').read_text())
for check in result['checks']:
    assert check['returncode'] == check['expected']
    for ext in ('stdout', 'stderr'):
        assert digest((EXEC / 'checks' / (check['label'] + '.' + ext)).read_bytes()) == check[ext + '_sha256']
assert len(result['checks']) == 18
final = {}
max_constraint = 0.
shape = None
for name in ('uninterrupted', 'resumed', 'sigterm', 'sigkill'):
    run = EXEC / 'runs' / name
    spec = json.loads((run / 'spec.json').read_text())
    folders = sorted(p for p in (run / 'checkpoints').glob('ckpt_*')
                     if (p / 'COMMITTED').is_file())
    for folder in folders:
        meta_raw = (folder / 'metadata.json').read_bytes()
        assert (folder / 'COMMITTED').read_text().strip() == digest(meta_raw)
        meta = json.loads(meta_raw)
        assert meta['eligible_for_resume'] is True
        payload = (folder / 'state.npz').read_bytes()
        assert digest(payload) == meta['payload_sha256']
        with np.load(folder / 'state.npz', allow_pickle=False) as z:
            state = z['state']
        assert state.dtype == np.float64 and np.isfinite(state).all()
        assert state.shape == (3, 5, 32)
        wave = np.fft.fftfreq(32, 1/32) * spec['k']
        def dx(a):
            return np.fft.ifft(1j * wave * np.fft.fft(a, axis=-1), axis=-1).real
        p, v, q, w, lam = (state[:, j] for j in range(5))
        residual = float(np.max(np.abs(dx(lam) - 2 * meta['t'] *
                            (v * dx(p) + np.exp(2*p) * w * dx(q)))))
        max_constraint = max(max_constraint, residual)
        assert residual < 2e-6
    assert meta['t'] == 4. and meta['step'] == 600
    final[name] = {'state_sha256': digest(state.tobytes(order='C')),
                   'checkpoint': str(folder.relative_to(PKG)),
                   'shape': list(state.shape), 'dtype': str(state.dtype)}
assert len({x['state_sha256'] for x in final.values()}) == 1
events = [json.loads(line) for line in (EXEC / 'checks/uninterrupted.stdout').read_text().splitlines()]
peak = max(x.get('gpu_allocated_peak', 0) for x in events)
last = events[-1]
assert last['status'] == 'SMOKE_CONTROL_COMPLETE'
assert last['torch'] == '2.5.1+cu121' and last['dtype'] == 'torch.float64'
assert peak == 42496
out = {'status': 'SAVED_RUNTIME_EVIDENCE_PASS', 'result_sha256': digest((EXEC / 'SMOKE_RESULT.json').read_bytes()),
       'log_hash_pairs_verified': len(result['checks']), 'final_states': final,
       'bitwise_state_identity': True, 'independent_numpy_max_constraint': max_constraint,
       'peak_torch_allocated_bytes_from_log': peak, 'final_runtime_event': last,
       'elapsed_seconds': time.monotonic()-started,
       'max_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
       'scope': 'Direct saved-byte/log integrity and NumPy momentum residual check; no GPU rerun, no broader solver certification'}
assert out['elapsed_seconds'] < 180 and out['max_rss_kib'] < 2 * 1024**2
(HERE / 'SAVED_RUNTIME_EVIDENCE_RESULT.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(out, indent=2))

"""Direct trigonometric saved-clock reader, independent of SMK1 runtime imports."""
from pathlib import Path
import argparse
import hashlib
import io
import json
import platform
import resource
import sys
import time

resource.setrlimit(resource.RLIMIT_AS, (2*1024**3, 2*1024**3))
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('run')
ap.add_argument('output')
args = ap.parse_args()
started = time.monotonic()
run = Path(args.run)
out = Path(args.output)
assert not out.exists(), 'preserve prior readout check'
folders = sorted(p.parent for p in (run/'checkpoints').glob('ckpt_*/COMMITTED'))
assert len(folders) >= 2
inputs = {}

def saved(folder):
    raw = (folder/'metadata.json').read_bytes()
    assert (folder/'COMMITTED').read_text().strip() == hashlib.sha256(raw).hexdigest()
    meta = json.loads(raw)
    payload = (folder/'state.npz').read_bytes()
    assert hashlib.sha256(payload).hexdigest() == meta['payload_sha256']
    with np.load(io.BytesIO(payload), allow_pickle=False) as data:
        state = data['state']
    assert state.dtype == np.float64 and list(state.shape) == meta['shape']
    assert np.isfinite(state).all()
    for p in (folder/'metadata.json', folder/'state.npz', folder/'COMMITTED'):
        inputs[str(p)] = hashlib.sha256(p.read_bytes()).hexdigest()
    return state, meta

initial, mi = saved(folders[0])
final, mf = saved(folders[-1])
assert mi['step'] == 0 and mi['t'] == 1 and mf['t'] == 4
assert mi['signature'] == mf['signature']
spec = json.loads((run/'spec.json').read_text())
n, k = spec['n'], spec['k']
assert n == 32 and len(spec['cases']) == final.shape[0]
x = np.arange(n)*2*np.pi/(n*k)
modes = np.concatenate((np.arange(n//2), np.arange(-n//2, 0)))
delta = k*((x+3.)[:,None] - x[None,:])
weights = np.cos(modes[:,None,None]*delta[None,:,:]).sum(axis=0)/n
lambda_observer = final[:,4] @ weights.T
logz = (lambda_observer-initial[:,4])/4 - np.log(4.)/4
z = np.exp(logz)
cases = []
for idx, case in enumerate(spec['cases']):
    cases.append({'id': case['id'], 'logZ': logz[idx].tolist(), 'Z': z[idx].tolist(),
                  'sampled_logZ_min': float(logz[idx].min()), 'sampled_logZ_max': float(logz[idx].max()),
                  'sampled_Z_min': float(z[idx].min()), 'sampled_Z_max': float(z[idx].max())})
result = {'status': 'COMPUTED_FOR_COMPARISON', 'marking': {'te': 1, 'to': 4, 'd': 3,
          'branch': 'positive longitudinal null branch', 'clocks': 'supplied fixed coordinate',
          'sample_count_per_case': n}, 'cases': cases, 'inputs_sha256': inputs,
          'python': sys.version, 'numpy': np.__version__, 'platform': platform.platform(),
          'elapsed_seconds': time.monotonic()-started, 'gpu_used': False,
          'limit': 'saved-array readout correspondence; not independent evolution or continuum extrema'}
out.write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('cases','inputs_sha256')}, indent=2))
print(json.dumps([{k:v for k,v in c.items() if k not in ('logZ','Z')} for c in cases], indent=2))

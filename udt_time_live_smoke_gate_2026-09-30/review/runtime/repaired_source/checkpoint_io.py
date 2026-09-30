"""Immutable committed checkpoint records; engineering, not scientific evidence."""
from pathlib import Path
import hashlib, io, json, math, os, uuid
import numpy as np

class CheckpointError(RuntimeError): pass

def digest(data): return hashlib.sha256(data).hexdigest()

def json_bytes(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False)+'\n').encode()

def exclusive(path, data):
    with Path(path).open('xb') as f:
        f.write(data); f.flush(); os.fsync(f.fileno())

def syncdir(path):
    fd=os.open(path,os.O_RDONLY|os.O_DIRECTORY)
    try: os.fsync(fd)
    finally: os.close(fd)

def publish_marker(folder, name, data):
    # SIGKILL before publication leaves an ignored temporary marker. The hard
    # link publishes complete bytes atomically and refuses any existing name.
    temporary=folder/(name+'.pending')
    exclusive(temporary,data)
    syncdir(folder)
    os.link(temporary,folder/name)
    syncdir(folder)

def save(run, signature, state, step, t, output_limit, *, diagnostic=None):
    run=Path(run)
    if state.dtype!=np.float64 or (diagnostic is None and not np.isfinite(state).all()):
        raise CheckpointError('NONFINITE_OR_WRONG_DTYPE')
    buffer=io.BytesIO(); np.savez_compressed(buffer,state=state)
    payload=buffer.getvalue()
    meta=json_bytes({'signature':signature,'step':step,'t':t,'shape':list(state.shape),
                     'dtype':'float64','payload_sha256':digest(payload),
                     'eligible_for_resume':diagnostic is None,'diagnostic':diagnostic})
    used=sum(p.stat().st_size for p in run.rglob('*') if p.is_file())
    if used+len(payload)+len(meta)+130>output_limit:
        raise CheckpointError('OUTPUT_BUDGET')
    root=run/('checkpoints' if diagnostic is None else 'diagnostics');root.mkdir(exist_ok=True)
    syncdir(run)
    folder=root/f'ckpt_{step:09d}_{uuid.uuid4().hex[:12]}'
    folder.mkdir(exist_ok=False)
    exclusive(folder/'state.npz',payload)
    exclusive(folder/'metadata.json',meta)
    # An incomplete folder never supersedes the last committed record.
    publish_marker(folder,'COMMITTED' if diagnostic is None else 'DIAGNOSTIC',
                   (digest(meta)+'\n').encode())
    syncdir(folder);syncdir(root)
    return folder

def load_latest(run, signature, shape, dt, end):
    committed=sorted(p for p in (Path(run)/'checkpoints').glob('ckpt_*')
                     if p.is_dir() and (p/'COMMITTED').is_file())
    if not committed:raise CheckpointError('NO_COMMITTED_CHECKPOINT')
    folder=committed[-1]
    raw=(folder/'metadata.json').read_bytes()
    if (folder/'COMMITTED').read_text().strip()!=digest(raw):
        raise CheckpointError('METADATA_HASH_MISMATCH')
    meta=json.loads(raw)
    if meta.get('eligible_for_resume') is not True:raise CheckpointError('INELIGIBLE_CHECKPOINT')
    if meta['signature']!=signature:raise CheckpointError('SPEC_OR_CODE_MISMATCH')
    payload=(folder/'state.npz').read_bytes()
    if digest(payload)!=meta['payload_sha256']:raise CheckpointError('PAYLOAD_HASH_MISMATCH')
    with np.load(io.BytesIO(payload),allow_pickle=False) as data:
        if set(data.files)!={'state'}:raise CheckpointError('STATE_SCHEMA')
        state=data['state']
    step=meta['step'];t=meta['t']
    if type(step)!=int or not 0<=step<=math.ceil((end-1)/dt):raise CheckpointError('STEP_RANGE')
    if not math.isfinite(t) or abs(t-min(1+step*dt,end))>1e-12:raise CheckpointError('TIME_MISMATCH')
    if f'ckpt_{step:09d}_' not in folder.name:raise CheckpointError('STEP_NAME_MISMATCH')
    if tuple(state.shape)!=tuple(shape) or meta['shape']!=list(shape):raise CheckpointError('STATE_SHAPE')
    if state.dtype!=np.float64 or meta['dtype']!='float64' or not np.isfinite(state).all():
        raise CheckpointError('NONFINITE_OR_WRONG_DTYPE')
    return state,step,t,folder

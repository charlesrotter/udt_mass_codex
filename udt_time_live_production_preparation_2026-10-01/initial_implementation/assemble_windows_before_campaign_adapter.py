"""Build bounded uniform windows from authenticated immutable checkpoints."""
import argparse,hashlib,io,json
from pathlib import Path
import numpy as np
B=Path(__file__).resolve().parent;ROOT=B.parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def assemble(name):
    receipt=json.loads((B/'invocations'/f'{name}.json').read_text())
    if receipt['returncode']!=0:raise ValueError('INCOMPLETE_CASE')
    run=B/'runs'/name;spec=json.loads((run/'spec.json').read_text());bytick={}
    source_spec=B/'specs'/f'{name}.json'
    if sha(source_spec)!=receipt['spec_sha256'] or json.loads(source_spec.read_text())!=spec:raise ValueError('SPEC_INPUT_CHANGED')
    for folder in (run/'checkpoints').glob('ckpt_*'):
        if not (folder/'COMMITTED').exists():continue
        meta=folder/'metadata.json';payload=folder/'state.npz'
        if (folder/'COMMITTED').read_text().strip()!=sha(meta):raise ValueError('METADATA_HASH')
        m=json.loads(meta.read_text());tick=m['step']
        if not m['eligible_for_resume'] or m['diagnostic'] is not None:raise ValueError('INELIGIBLE')
        if abs(m['t']-(1+tick*spec['dt_min']))>1e-12:raise ValueError('TIME_TICK')
        if m['signature']['spec']!=sha(run/'spec.json'):raise ValueError('SPEC_SIGNATURE')
        if m['signature']['code'][str((B/'production_worker.py').relative_to(ROOT))]!=receipt['worker_sha256']:raise ValueError('WORKER_SIGNATURE')
        if tick in bytick and bytick[tick][1]['payload_sha256']!=m['payload_sha256']:raise ValueError('DUPLICATE_TICK_DISAGREEMENT')
        bytick[tick]=(folder,m)
    out=B/'histories';out.mkdir(exist_ok=True);rows=[]
    for index,w in enumerate(spec['windows']):
        ticks=[w['center']+(i-w['count']//2)*w['stride'] for i in range(w['count'])]
        states=[];sources={}
        for tick in ticks:
            folder,m=bytick[tick];payload=folder/'state.npz'
            if sha(payload)!=m['payload_sha256']:raise ValueError('PAYLOAD_HASH')
            with np.load(payload,allow_pickle=False) as d:state=d['state']
            if state.shape!=(2,spec['n'],spec['n'],spec['n'],4,4) or state.dtype!=np.float64 or not np.isfinite(state).all():raise ValueError('STATE_SCHEMA')
            states.append(state)
            for q in [payload,folder/'metadata.json',folder/'COMMITTED']:sources[str(q.relative_to(ROOT))]=sha(q)
        states=np.stack(states);path=out/f'{name}_window{index}.npz';buf=io.BytesIO()
        np.savez_compressed(buf,g=states[:,0],v=states[:,1],times=1+np.array(ticks)*spec['dt_min'],period=np.array(spec['period']))
        with path.open('xb') as f:f.write(buf.getvalue())
        record=dict(history_sha256=sha(path),source_sha256=sources,spec_sha256=receipt['spec_sha256'],worker_sha256=receipt['worker_sha256'],assembler_sha256=sha(__file__),ticks=ticks,shape=list(states.shape),scope='Uniform diagnostic window; authenticated byte correspondence, not equation certification')
        with path.with_suffix('.sources.json').open('x') as f:json.dump(record,f,indent=2,sort_keys=True);f.write('\n')
        rows.append(dict(path=str(path.relative_to(ROOT)),bytes=path.stat().st_size,times=[1+ticks[0]*spec['dt_min'],1+ticks[-1]*spec['dt_min']]))
    return rows

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('cases',nargs='+');args=ap.parse_args();print(json.dumps({name:assemble(name) for name in args.cases},indent=2))

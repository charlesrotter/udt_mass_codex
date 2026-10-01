"""Independent direct checkpoint-array comparison of assembled smoke windows."""
import hashlib,json,resource
from pathlib import Path
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
import numpy as np
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1];ROOT=BASE.parent
def sha(q):return hashlib.sha256(Path(q).read_bytes()).hexdigest()
records=[]
for kind,names in [('pause',['case_a','case_b']),('signal',['case_c'])]:
    manifest=BASE/'supervisor_smoke'/(kind+'.json');m=json.loads(manifest.read_text());roots=[Path(q) for q in m['storage_roots']]
    total=sum(q.stat().st_size for root in roots for q in root.rglob('*') if q.is_file());assert total<=m['output_bytes']
    for name in names:
        folder=BASE/'supervisor_smoke'/('analysis_'+kind)/name;record=json.loads((folder/'ASSEMBLY.json').read_text())
        for p,h in record['input_sha256'].items():assert sha(p)==h
        for p,h in record['output_sha256'].items():assert sha(p)==h
        history=folder/'histories'/(name+'_window0.npz');source=json.loads(history.with_suffix('.sources.json').read_text())
        assert source['history_sha256']==sha(history)
        for p,h in source['source_sha256'].items():assert sha(ROOT/p)==h
        bytick={}
        for marker in (BASE/'runs/supervisor_smoke'/name).glob('checkpoints/*/COMMITTED'):
            meta=json.loads((marker.parent/'metadata.json').read_text());bytick[meta['step']]=marker.parent/'state.npz'
        with np.load(history,allow_pickle=False) as data:
            assert data['g'].shape==data['v'].shape==(9,8,8,8,4,4)
            assert np.array_equal(data['times'],1+np.array(source['ticks'])/3200)
            for i,tick in enumerate(source['ticks']):
                with np.load(bytick[tick],allow_pickle=False) as checkpoint:
                    assert np.array_equal(data['g'][i],checkpoint['state'][0]) and np.array_equal(data['v'][i],checkpoint['state'][1])
        records.append(dict(case=name,history_sha256=sha(history),matched_saved_times=9,total_budgeted_smoke_bytes=total))
result=dict(status='SMOKE_EXTRACTION_DIRECT_ARRAY_PASS',records=records,scope='Authenticated history and all nine g/v slices compared directly with checkpoints. This is correspondence, not independent Ricci qualification.')
with (HERE/'SMOKE_ASSEMBLY_REVIEW.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(result,indent=2))

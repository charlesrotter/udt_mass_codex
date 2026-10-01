"""CPU independent inspection of completed new-state runtime artifacts."""
import hashlib
import json
from pathlib import Path
import numpy as np
BASE=Path(__file__).resolve().parents[2]

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

records=[]
with np.load(BASE/'histories/n8_repaired.npz',allow_pickle=False) as data:
    expected={k:data[k][-1] for k in ('g','v')}
for name in ('resumed','sigterm'):
    path=BASE/'histories'/f'{name}.npz'
    with np.load(path,allow_pickle=False) as data:
        equal=all(np.array_equal(expected[k],data[k][-1]) for k in expected)
        assert equal
    records.append(dict(history=name,final_g_v_bitwise_equal=equal,sha256=sha(path)))
for name,code in [('wall_stop',75),('invalid_constraint',2)]:
    receipt=json.loads((BASE/'checks'/f'{name}.json').read_text())
    assert receipt['returncode']==code and not receipt['timeout']
    run=BASE/'runs'/name
    committed=list((run/'checkpoints').glob('*/COMMITTED'))
    diagnostics=list((run/'diagnostics').glob('*/DIAGNOSTIC'))
    if name=='wall_stop':assert committed and not diagnostics
    else:assert not committed and diagnostics
    for marker in committed+diagnostics:
        raw=(marker.parent/'metadata.json').read_bytes();meta=json.loads(raw)
        assert marker.read_text().strip()==hashlib.sha256(raw).hexdigest()
        assert meta['payload_sha256']==sha(marker.parent/'state.npz')
        assert meta['eligible_for_resume']==(name=='wall_stop')
    records.append(dict(run=name,returncode=code,committed=len(committed),diagnostic=len(diagnostics),receipt_sha256=sha(BASE/'checks'/f'{name}.json')))
inputs=[BASE/n for n in ('WORK_ORDER.md','SMOKE_PLAN.md','REPAIR_FREEZE.json','BATCH_FREEZE.json',
                         'initial_data.py','evolution.py','constraints.py','run_smoke.py','batch_smoke.py',
                         'clock_readout.py','CLOCK_READOUT.json','SHORT_RUN_RESULT.json')]
print(json.dumps(dict(status='RUNTIME_ARTIFACT_REVIEW_PASS',records=records,
    checked_sources={str(p.relative_to(BASE)):sha(p) for p in inputs},
    scope='Direct saved-array final-state comparisons and immutable stop/diagnostic metadata. Does not certify every failure path or perform a new GPU test.'),indent=2))

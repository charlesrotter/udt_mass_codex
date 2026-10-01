"""CPU source-level counterexample against preserved pre-repair validation.

np.load is replaced only to supply an in-memory malformed state within review
ownership. No fake file is put into the producer's initial directory.
"""
import hashlib, importlib.util, json
from pathlib import Path
from unittest.mock import patch
import numpy as np

HERE=Path(__file__).resolve().parent
SOURCE=HERE/'initial_implementation/production_worker.py'
# The source is evaluated with its original path so its reviewed module imports
# keep their original meaning, but exact bytes come from the preserved copy.
ORIGINAL=HERE.parents[1]/'production_worker.py'
module=type(np)('reviewed_worker');module.__file__=str(ORIGINAL)
exec(compile(SOURCE.read_text(),str(ORIGINAL),'exec'),module.__dict__)
n=8;g=np.broadcast_to(np.diag([-1.,1.,1.,1.]),(n,n,n,4,4)).copy();v=np.zeros_like(g)
g[...,0,1]=1e-3
class Data(dict):
    def __enter__(self):return self
    def __exit__(self,*args):return False
data=Data(g=g,v=v,period=np.array(2*np.pi))
spec=dict(n=n,initial='udt_time_live_production_preparation_2026-10-01/initial/mock.npz',
    period=2*np.pi,dt_min=.001,end_tick=100,max_step_ticks=4,cfl=.1,
    check_ticks=4,checkpoint_ticks=20,windows=[dict(center=50,stride=2,count=5)],
    wall_seconds=10,gpu_bytes=1024**3,output_bytes=1024**2,constraint_limit=2e-5)
with patch.object(module.np,'load',return_value=data):
    saves,checks,path=module.validate(spec)
assert np.max(np.abs(g-g.swapaxes(-1,-2)))>0
print(json.dumps(dict(status='PRE_REPAIR_ASYMMETRIC_INITIAL_ACCEPTED',
    exact_source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    asymmetry=float(np.max(np.abs(g-g.swapaxes(-1,-2)))),
    scope='Only pre-Torch validation counterexample, not a claim of successful malformed evolution.'),indent=2))

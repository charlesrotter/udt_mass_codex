"""Pre-survey development checks against explicit metrics, not own RHS targets."""
import json,time
from pathlib import Path
import numpy as np
import torch
from initial_data import exact_control,construct
from evolution import Engine

B=Path(__file__).resolve().parent
torch.set_num_threads(1);torch.use_deterministic_algorithms(True)
records=[];start=time.monotonic();engine=Engine(8,2*np.pi,'cuda')
for kind in ('flat','kasner','gauge_wave'):
    raw,vel,expected=exact_control(kind,8,.037)
    g=torch.tensor(raw,device='cuda');v=torch.tensor(vel,device='cuda')
    _,acc=engine.rhs(g,v);harm=engine.geometry(g,v)[-1]
    error=float(np.max(np.abs(acc.cpu().numpy()-expected)))
    constraint=float(harm.abs().max())
    assert error<2e-11,(kind,error)
    assert constraint<2e-12,(kind,constraint)
    errors=[]
    for dt in (.01,.005):
        raw,vel,_=exact_control(kind,8,0)
        g=torch.tensor(raw,device='cuda');v=torch.tensor(vel,device='cuda')
        for _ in range(round(.1/dt)):g,v=engine.step(g,v,dt)
        target,target_v,_=exact_control(kind,8,.1)
        error=max(float(np.max(np.abs(g.cpu().numpy()-target))),float(np.max(np.abs(v.cpu().numpy()-target_v))))
        assert error<2e-7,(kind,dt,error)
        errors.append(error)
    records.append({'kind':kind,'rhs_error':float(np.max(np.abs(acc.cpu().numpy()-expected))),
                    'harmonic':constraint,'end_state_errors':errors})
report={'status':'DEVELOPMENT_CONTROLS_PASS','checks':records,'seconds':time.monotonic()-start,
        'torch':torch.__version__,'device':torch.cuda.get_device_name(0),
        'gpu_allocated_peak':torch.cuda.max_memory_allocated(),'scope':'exact supplied controls only; broader histories not yet checked'}
with (B/'DEVELOPMENT_CONTROLS.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')
print(json.dumps(report,indent=2))

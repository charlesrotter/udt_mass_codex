"""Exact-vacuum and deliberately nonvacuum controls for outcome-informed stencil diagnosis."""
import hashlib
import json
from pathlib import Path
import numpy as np
from diagnose_window_truncation import center_ricci, verify_weights

verify_weights()
times=2.49+np.arange(-4,5)*.0025
shape=(9,4,4,4,4,4)
rows=[]
for label,p in [('kasner',(-1/3,2/3,2/3)),('nonvacuum_kasner',(.2,.3,.5))]:
    history=np.zeros(shape)
    for i,rate in enumerate((1.,*p)):
        history[...,i,i]=((-1 if i==0 else 1)*np.exp(2*rate*(times-1)))[:,None,None,None]
    expected=np.zeros((4,4));expected[0,0]=sum(p)-sum(x*x for x in p)
    for order in [4,6,8]:
        result=center_ricci(history,times,2*np.pi,order)
        error=float(abs(result-expected).max())
        assert error<2e-8
        maximum=float(abs(result).max())
        if label=='nonvacuum_kasner':assert maximum>.6
        rows.append(dict(label=label,order=order,ricci_max=maximum,analytic_error=error))
for h in [.2,5.]:
    history=np.zeros(shape);history[...,0,0]=-1
    for i in range(1,4):history[...,i,i]=np.exp(2*h*(times-2.49))[:,None,None,None]
    expected=np.diag([-3*h*h,3*h*h,3*h*h,3*h*h])
    for order in [4,6,8]:
        result=center_ricci(history,times,2*np.pi,order)
        error=float(abs(result-expected).max())
        maximum=float(abs(result).max())
        assert maximum>.1
        if order>=6:assert error<1e-7
        rows.append(dict(label='nonvacuum_exponential_flrw',h=h,order=order,ricci_max=maximum,analytic_error=error))
here=Path(__file__).resolve().parent
print(json.dumps(dict(status='PASS',rows=rows,
    exact_rational_stencil_moments_verified=True,
    source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    diagnostic_sha256=hashlib.sha256((here/'diagnose_window_truncation.py').read_bytes()).hexdigest(),
    scope='Controls of higher-order diagnostic on exact analytic metrics; no changed PDE, tolerance or saved field.'),indent=2,sort_keys=True))

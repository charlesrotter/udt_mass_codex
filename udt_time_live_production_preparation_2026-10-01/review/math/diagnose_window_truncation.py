"""Finite diagnostic after failed spatial gate; no tolerance or field change."""
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[3]
OLD=ROOT/'udt_three_spatial_smoke_2026-10-01/review/equations_recovery'
sys.path.insert(0,str(OLD))
from history_ricci import metric_jets, original_ricci, spatial_derivative

COEFFICIENTS={
 4:([-1,8,0,-8,1],-12,[-1,16,-30,16,-1],12),
 6:([-1,9,-45,0,45,-9,1],60,[2,-27,270,-490,270,-27,2],180),
 8:([3,-32,168,-672,0,672,-168,32,-3],840,[-9,128,-1008,8064,-14350,8064,-1008,128,-9],5040)
}

def verify_weights():
    for order,(first,den1,second,den2) in COEFFICIENTS.items():
        offsets=range(-order//2,order//2+1)
        for power in range(order+1):
            a=sum(Fraction(c,den1)*j**power for c,j in zip(first,offsets))
            b=sum(Fraction(c,den2)*j**power for c,j in zip(second,offsets))
            assert a==(1 if power==1 else 0),(order,power,a)
            assert b==(2 if power==2 else 0),(order,power,b)


def center_ricci(history,times,period,order):
    index=len(times)//2;g,d,dd=metric_jets(history,times,index,period)
    dt=float(times[1]-times[0]);first,den1,second,den2=COEFFICIENTS[order]
    # Exact zero-sum stencils, evaluated after subtracting central metric.
    residuals=history[index-order//2:index+order//2+1]-g
    d[...,0,:,:]=np.einsum('t,t...->...',np.asarray(first)/den1,residuals)/dt
    dd[...,0,0,:,:]=np.einsum('t,t...->...',np.asarray(second)/den2,residuals)/(dt*dt)
    for i in range(3):
        dd[...,0,i+1,:,:]=dd[...,i+1,0,:,:]=spatial_derivative(d[...,0,:,:],i,period)
    return original_ricci(g,d,dd)[0]


def main():
    verify_weights();rows=[]
    for filename in sys.argv[2:]:
        with np.load(filename,allow_pickle=False) as data:
            history,times,period=data['g'],data['times'],float(data['period'])
            record=dict(path=filename,sha256=hashlib.sha256(Path(filename).read_bytes()).hexdigest(),
                        center_time=float(times[4]),orders={})
            for order in COEFFICIENTS:
                r=center_ricci(history,times,period,order)
                record['orders'][str(order)]=dict(ricci_max=float(abs(r).max()),ricci_rms=float(np.sqrt(np.mean(r*r))))
            rows.append(record)
    result=dict(status='DIAGNOSTIC_ONLY',rows=rows,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        inherited_checker_sha256=hashlib.sha256((OLD/'history_ricci.py').read_bytes()).hexdigest(),
        exposure='Written after first24 five-point windows showed no frozen spatial residual improvement; not a pre-frozen certification test.',
        scope='Same saved metrics, centered4/6/8th-order time differentiation at one matched center; unchanged Fourier and original Ricci. Does not replace failed frozen gate or diagnose unsaved times.')
    with Path(sys.argv[1]).open('x') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()

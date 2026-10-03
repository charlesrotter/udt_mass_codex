"""Independent direct-coordinate PSW1 check; no CBR1 parent imports.

FREE analytic scale factor and boost controls. CPU float64 DOP853 with finite
query list and finite integration intervals, no GPU or elapsed timeout.
"""
import hashlib,json,platform
from pathlib import Path
import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import mpmath as mp

OUT=Path(__file__).resolve().parent

def metric(t,k):
    a=1+k*t*t
    return a,2*k*t/a

def inner(t,x,y,k):
    a,_=metric(t,k)
    return -x[0]*y[0]+a*a*np.dot(x[1:],y[1:])

def accel(t,v,w,k):
    a,H=metric(t,k)
    return np.r_[-a*a*H*np.dot(v[1:],w[1:]),-H*(v[0]*w[1:]+w[0]*v[1:])]

def ode(s,y,k,transport=False):
    x,v=y[:4],y[4:8]
    z=np.r_[v,accel(x[0],v,v,k)]
    return np.r_[z,accel(x[0],v,y[8:12],k)] if transport else z

def ivp(y,end,k,transport=False):
    s=solve_ivp(lambda q,z:ode(q,z,k,transport),(0,end),y,method='DOP853',
                rtol=2.4e-14,atol=3e-16,dense_output=True,max_step=abs(end)/8)
    assert s.success
    return s

def eta(t,k):
    return t if k==0 else np.arctan(np.sqrt(k)*t)/np.sqrt(k)

def frame(t,beta,k):
    a,_=metric(t,k)
    b=np.asarray(beta,dtype=float);b2=b@b;g=1/np.sqrt(1-b2)
    U=np.r_[g,g*b/a]
    spatial=np.eye(3)+(g-1)*np.outer(b,b)/b2 if b2 else np.eye(3)
    triad=[np.r_[g*b[i],spatial[:,i]/a] for i in range(3)]
    return U,triad

def clock(t0,U,n,L,k,emission_difference=False):
    o=np.r_[t0,0.,0.,0.]
    prep=ivp(np.r_[o,n,U],L,k,True).y[:,-1]
    receiver=ivp(prep[:4].tolist()+prep[8:12].tolist(),8*L,k)
    def arrival(emitter):
        def incidence(tau):
            b=receiver.sol(tau)[:4]
            return eta(b[0],k)-eta(emitter[0],k)-np.linalg.norm(b[1:]-emitter[1:])
        tau=brentq(incidence,0.,8*L,xtol=5e-16,rtol=9e-16)
        b=receiver.sol(tau)
        return tau,b,incidence(tau)
    tau,b,res=arrival(o)
    N=b[1:4]/np.linalg.norm(b[1:4]);ae,_=metric(t0,k);ar,_=metric(b[0],k)
    p=(ar/ae)*(U[0]-ae*N@U[1:])/(b[4]-ar*N@b[5:8])
    result=dict(p=float(p),logp=float(np.log(p)),tau=float(tau),
                null_residual=float(res),
                prep_spacelike_norm_error=float(inner(prep[0],prep[4:8],prep[4:8],k)-1),
                prep_timelike_norm_error=float(inner(prep[0],prep[8:12],prep[8:12],k)+1),
                prep_orthogonality=float(inner(prep[0],prep[4:8],prep[8:12],k)),
                receiver_norm_error=float(inner(b[0],b[4:8],b[4:8],k)+1))
    if emission_difference:
        estimates=[]
        for ds in [1e-4,5e-5]:
            plus=ivp(np.r_[o,U],ds,k).y[:4,-1]
            minus=ivp(np.r_[o,U],-ds,k).y[:4,-1]
            estimates.append(float((arrival(plus)[0]-arrival(minus)[0])/(2*ds)))
        result['arrival_derivatives']=estimates
        result['derivative_frequency_error']=abs(estimates[-1]-p)
    return result

def main():
    rows=[]
    # Arbitrary non-axis-aligned velocity; its boosted coordinate triad is supplied.
    beta=np.array([.2,-.3,.25]);t0=.3;k=.2
    U,triad=frame(t0,beta,k)
    a,H=metric(t0,k);A=2*k/a;gamma=U[0]
    ric=-(2*gamma*gamma+1)*A+2*H*H*(gamma*gamma-1)
    for L in [.04,.02,.01,.005,.0025]:
        readings=[clock(t0,U,n,L,k,L==.02) for n in triad]
        c=-2*sum(z['logp'] for z in readings)/(L*L)
        rows.append(dict(L=L,c=c,oracle_RicUU=ric,error=abs(c-ric),readings=readings))
    assert rows[-1]['error']<.25*rows[0]['error']
    assert all(abs(r['null_residual'])<2e-14 for z in rows for r in z['readings'])
    assert all(abs(r[key])<2e-12 for z in rows for r in z['readings'] for key in
        ['prep_spacelike_norm_error','prep_timelike_norm_error','prep_orthogonality','receiver_norm_error'])
    assert max(r['derivative_frequency_error'] for r in rows[1]['readings'])<1e-9
    flatU,flatn=frame(t0,beta,0)
    flat=[clock(t0,flatU,n,.13,0,True) for n in flatn]
    assert max(abs(x['p']-1) for x in flat)<2e-13
    # Separately evaluated 70-digit exact comoving control at H(0)=0.
    mp.mp.dps=70
    high=[]
    U,triad=frame(0,[0,0,0],k)
    for L in [.2,.1,.05]:
        r=clock(0,U,triad[0],L,k,True)
        ll=mp.mpf(str(L));kk=mp.mpf(str(k));tb=mp.tan(mp.sqrt(kk)*ll)/mp.sqrt(kk)
        p=1+kk*tb*tb
        high.append(dict(L=L,direct=r,exact_p=str(p),absolute_error=abs(r['p']-float(p))))
    assert max(x['absolute_error'] for x in high)<2e-13
    result=dict(status='PASS finite independent controls; no parent implementation exposed',
       versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,mpmath=mp.__version__),
       settings=dict(dtype='float64 plus70-digit exact-control evaluation',method='DOP853',rtol=2.4e-14,atol=3e-16,
                     max_step='absolute integration interval/8',cpu_only=True,finite_clock_queries=21,
                     omissions='No main controls, no parent code or outputs, no interval/error-bound certificate'),
       moving_frame=rows,flat=flat,exact_comoving=high)
    p=OUT/'SOURCE_FIRST_CHECK.json'
    with p.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(dict(status=result['status'],moving_errors=[z['error'] for z in rows],
                         frequency_difference=max(r['derivative_frequency_error'] for r in rows[1]['readings']),
                         flat_max=max(abs(x['p']-1) for x in flat),
                         exact_max=max(x['absolute_error'] for x in high))))

if __name__=='__main__':main()

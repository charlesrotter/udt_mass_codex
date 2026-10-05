"""Frozen OJM1 fidelity controls; imports no parent/source computation code."""
import os
for _name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[_name] = '1'
import resource
resource.setrlimit(resource.RLIMIT_AS, (2*1024**3, 2*1024**3))
import json, sys, platform
from pathlib import Path
import numpy as np
import scipy
from scipy.integrate import quad, solve_ivp
import mpmath as mp

BASE = Path(__file__).parent
records = []
def fixed_case(a, b, R, label):
    m,H = 1.,.01
    f=lambda r: 1-2*m/r-H*H*r*r
    s=lambda r: np.sqrt(1-f(r)*b*b/r**2)
    sa=s(a)
    P=quad(lambda r: b/(r*r*s(r)), a, R, epsabs=1e-12, epsrel=1e-12)[0]
    I=quad(lambda r: 1/(r*r*s(r)**3), a, R, epsabs=1e-12, epsrel=1e-12)[0]
    exact=np.array([a*sa*R*s(R)*I, a*R*np.sin(P)/b if b else R-a])
    def rhs(r,y):
        ss=1-f(r)*b*b/r**2
        acc=b*b*(r-3*m)/r**4
        q=3*m*b*b/r**5
        return [y[1],(q*y[0]-acc*y[1])/ss,y[3],(-q*y[2]-acc*y[3])/ss]
    sol=solve_ivp(rhs,(a,R),[0,1/sa,0,1/sa],method='DOP853',rtol=2e-11,atol=2e-12)
    ode=sol.y[[0,2],-1]
    err=np.abs(ode-exact)/(1+np.abs(exact))
    rec=dict(label=label,a=a,b=b,R=R,P=P,P_over_pi=P/np.pi,
             B_variation=exact.tolist(),B_ode=ode.tolist(),relative_errors=err.tolist(),
             ode_success=bool(sol.success),pass_comparison=bool(sol.success and max(err)<2e-8))
    records.append(rec)
    return rec

for b in [0.,1.,4.]:
    for R in [10.,100.,1000.]:
        fixed_case(8.,b,R,f'fixed_b{b:g}_R{R:g}')
for fraction in [.99,.9999,.999999]:
    a=3.001
    b=fraction*a/np.sqrt(1-2/a-.01**2*a*a)
    fixed_case(a,b,1000.,f'near_tangent_{fraction}')

mp.mp.dps=50
m,a,H,E=map(mp.mpf,['1','8','.01','1.2'])
h=1-3*m/a
Omega=mp.sqrt(m/a**3-H**2)
def incidence_case(R):
    x=1/R
    # Reciprocal-radius integration is smooth across the coordinate horizon.
    def s(w,b): return mp.sqrt(1+H**2*b*b-b*b*w*w+2*m*b*b*w**3)
    def P(b): return mp.quad(lambda w:b/s(w,b),[x,1/a])
    def U(b): return mp.quad(lambda w:b*b/(s(w,b)*(1+s(w,b))),[x,1/a])
    def tail(w):
        V=mp.sqrt(H**2+(E*E-1)*w*w+2*m*w**3)
        return 1/(V*(E*w+V))
    d=mp.quad(tail,[0,x])
    b=mp.findroot(lambda b:P(b)-Omega*U(b)-Omega*d,Omega*a/(H*H*R))
    residual=abs(P(b)-Omega*U(b)-Omega*d)
    sa=s(1/a,b); so=s(x,b)
    I=mp.quad(lambda w:1/s(w,b)**3,[x,1/a])
    B1=a*sa*R*so*I
    B2=a*R*mp.sin(P(b))/b
    v=mp.sqrt(E*E-1+2*m/R+H*H*R*R)
    A=1/(E+v)+v*b*b/(R*R*(1+so))
    DA=A*mp.sqrt(abs(B1*B2))
    L=mp.quad(lambda w:1/(w*w*s(w,b)),[x,1/a])
    Do=A*L
    Z=(1-Omega*b)/(mp.sqrt(h)*A)
    expected=(a+E/H)/mp.sqrt(h)
    product=Z*(1/H-DA)
    vals=dict(R=R,b=b,t_e=-d-U(b),incidence_residual=residual,s_source=sa,
              B_parallel=B1,B_perp=B2,D_A=DA,D_o=Do,Z=Z,pole_product=product,
              pole_residue=expected,pole_relative_error=abs(product/expected-1),
              affine_area_gap=Do-DA)
    rec={k:mp.nstr(v,48) for k,v in vals.items()}
    rec.update(label='actual_R'+str(int(R)),pass_incidence=bool(residual<mp.mpf('1e-35') and sa>0))
    records.append(rec)

for R in ['1000','10000','100000','1000000']:
    incidence_case(mp.mpf(R))

result=dict(case_count=len(records),resources=dict(cpu_only=True,address_space_cap_bytes=2*1024**3,
    blas_threads=1,timeout=None),versions=dict(python=sys.version,platform=platform.platform(),
    numpy=np.__version__,scipy=scipy.__version__,mpmath=mp.__version__),records=records)
result['all_frozen_checks_pass']=all(r.get('pass_comparison',r.get('pass_incidence',False)) for r in records)
(BASE/'INDEPENDENT_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
sys.exit(0 if result['all_frozen_checks_pass'] else 1)

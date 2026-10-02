"""Independent ERC1 source-first checks; no ERC1 parent imports."""
import hashlib, json, platform
from pathlib import Path
import sympy as s
import numpy as np
import scipy
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq

OUT = Path(__file__).resolve().parent
checks = []
def zero(name, expr):
    value = s.simplify(s.trigsimp(expr))
    checks.append({'name': name, 'zero': value == 0, 'residual': str(value)})
    if value != 0:
        raise AssertionError((name, value))

# Direct differential geometry in dual numbers (constant + epsilon coefficient).
def add(*xs): return tuple(s.simplify(sum(x[k] for x in xs)) for k in [0, 1])
def mul(x,y): return (s.simplify(x[0]*y[0]),s.simplify(x[0]*y[1]+x[1]*y[0]))
def scale(x,c): return tuple(s.simplify(c*q) for q in x)
def diff(x,c): return tuple(s.diff(q,c) for q in x)
Z=(s.S.Zero,s.S.Zero)
def geometry(coords,diag):
    n=len(coords)
    inv=[(1/g[0],-g[1]/g[0]**2) for g in diag]
    def g(i,j): return diag[i] if i==j else Z
    gamma={}
    for k in range(n):
        for i in range(n):
            for j in range(n):
                gamma[k,i,j]=scale(mul(inv[k],add(diff(g(k,j),coords[i]),
                    diff(g(k,i),coords[j]),scale(diff(g(i,j),coords[k]),-1))),s.Rational(1,2))
    ric={}
    for i in range(n):
        for j in range(n):
            terms=[]
            for k in range(n):
                terms += [diff(gamma[k,i,j],coords[k]),scale(diff(gamma[k,i,k],coords[j]),-1)]
                for l in range(n):
                    terms += [mul(gamma[k,i,j],gamma[l,k,l]),scale(mul(gamma[l,i,k],gamma[k,j,l]),-1)]
            ric[i,j]=add(*terms)
    scalar=add(*[mul(inv[i],ric[i,i]) for i in range(n)])
    return inv,gamma,ric,scalar

t,r,th,ph=s.symbols('t r theta phi', real=True)
p,q=s.Function('p')(r),s.Function('q')(r)
diag=[(-s.S.One,-2*p),(s.S.One,-2*q),(r*r,-2*q*r*r),
      (r*r*s.sin(th)**2,-2*q*r*r*s.sin(th)**2)]
inv,gamma,ric,scalar=geometry([t,r,th,ph],diag)
lap=lambda z:s.diff(z,r,2)+2*s.diff(z,r)/r
zero('static scalar from metric',scalar[1]-2*lap(2*q-p))
zero('static Ric00 from metric',ric[0,0][1]-lap(p))
alpha=s.symbols('alpha',nonzero=True,real=True)
R1=scalar[1]
hess={}
coords=[t,r,th,ph]
for i in range(4):
    for j in range(4):
        hess[i,j]=s.diff(R1,coords[i],coords[j])-sum(gamma[k,i,j][0]*s.diff(R1,coords[k]) for k in range(4))
box=sum(inv[i][0]*hess[i,i] for i in range(4))
E={}
for i in range(4):
    for j in range(4):
        base=diag[i][0] if i==j else 0
        E[i,j]=s.simplify(ric[i,j][1]-base*R1/2+2*alpha*(base*box-hess[i,j]))
phi=-1/(10*r)-s.exp(-r)/(6*r)
psi=-1/(10*r)+s.exp(-r)/(6*r)
sub={p:phi,q:psi,alpha:s.Rational(1,6)}
for ij,e in E.items():zero('static E'+str(ij),e.subs(sub).doit())
zero('static scalar profile',R1.subs(sub).doit()-s.exp(-r)/r)
bad=s.simplify(E[0,0].subs({p:phi,q:phi,alpha:s.Rational(1,6)}).doit())
assert bad != 0
checks.append({'name':'omitting independent Psi is detected','nonzero_residual':str(bad)})

# A separate full-metric calculation, using zero first coefficients.
a=s.Function('a')(t)
iv,ga,ri,sc=geometry([t,s.Symbol('x'),s.Symbol('y'),s.Symbol('z')],
                     [(-s.S.One,0),(a*a,0),(a*a,0),(a*a,0)])
zero('FLRW Ric00',ri[0,0][0]+3*s.diff(a,t,2)/a)
zero('FLRW spatial Ric',ri[1,1][0]-(a*s.diff(a,t,2)+2*s.diff(a,t)**2))
zero('FLRW metric scalar',sc[0]-6*(s.diff(a,t,2)/a+s.diff(a,t)**2/a**2))
H,R,P,L=s.symbols('H R P Lambda',real=True)
Hd=R/6-2*H*H
Pd=-3*H*P-(R-4*L)/(6*alpha)
F=1+2*alpha*R
C=3*F*H*H-alpha*R*R/2+6*alpha*H*P-L
D=F*(Hd+3*H*H)-(R+alpha*R*R)/2-2*alpha*(Pd+2*H*P)+L
zero('FLRW trace relation',3*D-C)
zero('FLRW constraint propagation',s.diff(C,H)*Hd+s.diff(C,R)*P+s.diff(C,P)*Pd+4*H*C)
ini={H:s.Rational(1,10),R:s.Rational(1,10),P:-s.Rational(31,600),alpha:1,L:0}
zero('initial constraint',C.subs(ini))
badC=C.subs(dict(ini,**{})).subs({}) # Copy preserves the exact original constraint.
perturbed=C.subs({**ini,P:ini[P]+s.Rational(1,1000)})
assert perturbed != 0
checks.append({'name':'perturbed initial constraint detected','nonzero_residual':str(perturbed)})

# One independent numerical witness. These choices are FREE, not physical scale.
def rhs(time,z):
    av,hv,rv,pv,eta=z
    return [av*hv,rv/6-2*hv*hv,pv,-3*hv*pv-rv/6,1/av]
records=[]
saved={}
for tol in [1e-8,1e-10,1e-12]:
    sol=solve_ivp(rhs,(0.,2.),[1.,.1,.1,-31/600,0.],method='Radau',
                  rtol=tol,atol=tol/100,dense_output=True)
    assert sol.success
    ts=np.linspace(0,2,101);ys=sol.sol(ts)
    assert np.isfinite(ys).all() and ys[0].min()>0 and (1+2*ys[2]).min()>0
    av,hv,rv,pv,eta=ys
    hd=rv/6-2*hv*hv;pd=-3*hv*pv-rv/6
    e00=-3*(1+2*rv)*(hd+hv*hv)+(rv+rv*rv)/2+6*hv*pv
    eii=(1+2*rv)*(hd+3*hv*hv)-(rv+rv*rv)/2-2*(pd+2*hv*pv)
    constraint=3*(1+2*rv)*hv*hv-rv*rv/2+6*hv*pv
    residual=float(max(np.max(np.abs(e00)),np.max(np.abs(eii)),np.max(np.abs(constraint))))
    assert residual<=1e-7
    def qeta(z):return quad(lambda u:1/sol.sol(u)[0],0,z,epsabs=1e-12,epsrel=1e-12)[0]
    clock=[]
    for emitted in [.1,.12]:
        row={'emission':emitted}
        for name,distance in [('arrival',.2),('echo',.4)]:
            event=brentq(lambda u:qeta(u)-qeta(emitted)-distance,emitted,2,xtol=1e-13)
            byeta=brentq(lambda u:sol.sol(u)[4]-sol.sol(emitted)[4]-distance,emitted,2,xtol=1e-13)
            row[name]=event;row[name+'_eta_difference']=abs(event-byeta)
            assert abs(event-byeta)<=1e-8
        clock.append(row)
    record={'rtol':tol,'success':bool(sol.success),'nfev':sol.nfev,
       'endpoint':ys[:,-1].tolist(),'minimum_a':float(av.min()),'minimum_F':float((1+2*rv).min()),
       'maximum_original_tensor_and_constraint_residual':residual,'clock_events':clock,
       'oneway_finite_period_ratio':(clock[1]['arrival']-clock[0]['arrival'])/.02,
       'echo_finite_period_ratio':(clock[1]['echo']-clock[0]['echo'])/.02}
    records.append(record);saved[str(tol)]={'times':ts.tolist(),'states':ys.tolist()}
enddiff=float(np.max(np.abs(np.asarray(records[-1]['endpoint'])-records[-2]['endpoint'])))
clockdiff=max(abs(records[-1][k]-records[-2][k]) for k in ['oneway_finite_period_ratio','echo_finite_period_ratio'])
assert max(enddiff,clockdiff)<=1e-7
result={'scope':'one supplied finite FLRW witness and exact restricted symbolic checks',
 'versions':{'python':platform.python_version(),'sympy':s.__version__,'numpy':np.__version__,'scipy':scipy.__version__},
 'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'source_first_sha256':hashlib.sha256((OUT/'SOURCE_FIRST.md').read_bytes()).hexdigest(),
 'symbolic_checks':checks,'cases':records,'tight_endpoint_difference':enddiff,
 'tight_finite_period_difference':clockdiff,'pass':True}
(OUT/'source_first_result.json').write_text(json.dumps(result,indent=2)+'\n')
(OUT/'source_first_states.json').write_text(json.dumps(saved,indent=2)+'\n')
print(json.dumps(result,indent=2))

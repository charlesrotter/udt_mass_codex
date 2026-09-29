"""Independent bounded exact anchors for LCIA1 source review, not whole-proof certification.

Question: do the inspected local-clock assumptions erase the restricted negative
results? Supplied symbolic Lorentz metrics and timing maps; no physical choice.
CPU one thread, 60 s / 512 MiB via existing capture utility, no GPU or data.
All polynomial examples are free mathematical controls. In particular the FCV
polynomial is NOT a compact smooth bump and certifies no all-jet claim.
"""
import json
import platform
import sympy as s

out = {}

def geometry(g, coords):
    n=len(coords); inv=g.inv()
    C=[[[s.simplify(sum(inv[a,d]*(s.diff(g[d,c],coords[b])+s.diff(g[d,b],coords[c])-s.diff(g[b,c],coords[d]))/2 for d in range(n))) for c in range(n)] for b in range(n)] for a in range(n)]
    Ric=s.Matrix(n,n,lambda a,b:s.simplify(sum(s.diff(C[c][a][b],coords[c])-s.diff(C[c][a][c],coords[b])+sum(C[c][c][d]*C[d][a][b]-C[c][b][d]*C[d][a][c] for d in range(n)) for c in range(n))))
    R=s.simplify(sum(inv[a,b]*Ric[a,b] for a in range(n) for b in range(n)))
    return inv,C,Ric,R

t,x,y,z=s.symbols('t x y z',real=True)
F=s.Function('F')(t,x)
_,_,_,R=geometry(s.diag(-1/F,F),(t,x))
assert s.simplify(R-(s.diff(F,t,2)-s.diff(1/F,x,2)))==0
out['CRD_scalar_curvature']=str(R)
out['CRD_principal']='F_tt + F**(-2) F_xx; definite for F>0, restricted forcing only'

_,_,Ric,R=geometry(s.diag(-1,t,t,t),(t,x,y,z))
assert R==0 and Ric[0,0]==3/(4*t**2) and Ric[1,1]==1/(4*t)
out['GRS_R2_degeneracy']={'R':str(R),'Ric_tt':str(Ric[0,0]),'Ric_xx':str(Ric[1,1])}

N=1+x*x+y**3
g=s.diag(-N*N,1,1,1)
inv,_,Ric,R=geometry(g,(t,x,y,z))
coords=(t,x,y,z)
j=[s.simplify(sum(Ric[a,b]*inv[a,c]*s.diff(R,coords[c]) for a in range(4) for c in range(4))) for b in range(4)]
curl=s.simplify((s.diff(j[2],x)-s.diff(j[1],y)).subs({x:1,y:1}))
assert curl==s.Rational(16,3)
out['CRV_fixed_metric_curl']=str(curl)

em=s.symbols('em',real=True)
b=x**3*(1-x)**3
# Different polynomial from the source. Differentiate the original null ODE:
# d(delta t)/dx = 2(em+x)b(x), with delta t(0)=0.
arrival_delta=s.integrate(2*(em+x)*b,(x,0,1))
Q=s.diff(arrival_delta,em)
assert Q==s.Rational(1,70) and b.subs(x,0)==b.subs(x,1)==0
out['FCV_original_null_ODE_control']={'arrival_delta':str(arrival_delta),'Q':str(Q),'compact_bump_claim_checked_numerically':False}

q=s.symbols('q',positive=True)
gamma=1+q*q/2
sp=s.Matrix([q*q/2,q,0])
assert s.simplify(gamma**2-sp.dot(sp))==1
assert s.simplify(gamma-sp[0])==1
out['FSL_direction_control']='gamma^2-|spatial|^2=1 and Z=1 for all q>0; norm tends to one'

p,q=s.symbols('p q',positive=True)
P=p*q
radar=s.simplify(((P-1)/2)/((P+1)/2))
assert radar==(p*q-1)/(p*q+1)
beta,dK,dS=s.symbols('beta dK dS',real=True)
a,b=s.symbols('a b',real=True)
sol=s.solve([a+beta*b-dK,b+beta*a+dS],(a,b))
assert s.simplify(sol[a]-(dK+beta*dS)/(1-beta**2))==0
assert s.simplify(sol[b]-(-dS-beta*dK)/(1-beta**2))==0
out['ICN_radar_and_longitudinal_gradient']={'radar':str(radar),'partial_T_phi':str(sol[a]),'c_partial_R_phi':str(sol[b])}

ell,tau=s.symbols('ell tau',positive=True)
f=s.Function('f')
assert s.simplify(s.diff(ell*f(tau/ell),tau).subs(tau,ell*t)-s.diff(f(t),t))==0
out['MGC_clock_homothety']='f_ell(ell t) derivative equals f_prime(t); matched clocks required'

print(json.dumps({'status':'PASS','scope':'seven exact source argument anchors; not ten-package recertification','python':platform.python_version(),'sympy':s.__version__,'checks':out},indent=2))

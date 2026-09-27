"""Exact checks for an UNADOPTED metric-response hypothesis, not native physics.

Uses the previously checked connection-to-curvature method, now applied to the
full quadratic response before symmetry equations are solved. Independent review
uses a separate implementation. No physical boundary, source or fit is supplied.
"""
import json
import platform
import time
from pathlib import Path
import sympy as s

start=time.monotonic()
t,r,theta,az=s.symbols('t r theta az',real=True)
x=(t,r,theta,az)
f=s.Function('f')(r)
alpha=s.symbols('alpha',real=True)
g=s.diag(-f,1/f,r**2,r**2*s.sin(theta)**2)
inv=g.inv()
def clean(v): return s.factor(s.trigsimp(s.simplify(v)))
gamma=[[[clean(sum(inv[a,d]*(s.diff(g[d,c],x[b])+s.diff(g[d,b],x[c])-s.diff(g[b,c],x[d]))/2 for d in range(4))) for c in range(4)] for b in range(4)] for a in range(4)]
ric=s.Matrix(4,4,lambda a,b:clean(sum(s.diff(gamma[c][a][b],x[c])-s.diff(gamma[c][a][c],x[b])+sum(gamma[c][c][d]*gamma[d][a][b]-gamma[c][b][d]*gamma[d][a][c] for d in range(4)) for c in range(4))))
rm=(inv*ric).applyfunc(clean)
R=clean(s.trace(rm))
F=1+2*alpha*R
L=R+alpha*R**2
hess=s.Matrix(4,4,lambda a,b:clean(s.diff(F,x[a],x[b])-sum(gamma[c][a][b]*s.diff(F,x[c]) for c in range(4))))
hm=(inv*hess).applyfunc(clean)
boxF=clean(s.trace(hm))
E=(F*rm-s.eye(4)*L/2+s.eye(4)*boxF-hm).applyfunc(clean)
checks=[]
def equal(name,expr,expected=0):
 residual=clean(expr-expected)
 assert residual==0,(name,residual)
 checks.append(name)
def nonzero(name,expr,values):
 value=clean(expr.subs(values))
 assert value!=0,(name,value)
 checks.append(name)

equal('full_scalar_curvature',R,-s.diff(f,r,2)-4*s.diff(f,r)/r-2*(f-1)/r**2)
equal('full_time_radial_ricci',rm[1,1]-rm[0,0])
equal('hessian_time',hm[0,0],alpha*s.diff(f,r)*s.diff(R,r))
equal('hessian_radial',hm[1,1],2*alpha*f*s.diff(R,r,2)+alpha*s.diff(f,r)*s.diff(R,r))
equal('hessian_angular',hm[2,2],2*alpha*f*s.diff(R,r)/r)
equal('boxF',boxF,2*alpha*(f*s.diff(R,r,2)+(s.diff(f,r)+2*f/r)*s.diff(R,r)))
equal('response_time_radial_difference',E[1,1]-E[0,0],-2*alpha*f*s.diff(R,r,2))
equal('response_trace',s.trace(E),-R+3*boxF)
equal('response_radial_divergence',s.diff(E[1,1],r)+s.diff(f,r)/(2*f)*(E[1,1]-E[0,0])+2/r*(E[1,1]-E[2,2]))
for a in range(4):
 for b in range(4):
  if a!=b:equal(f'offdiagonal_{a}_{b}',E[a,b])
G=rm-s.eye(4)*R/2
for i in range(4):equal(f'alpha_zero_{i}',E[i,i].subs(alpha,0),G[i,i])
u,v,p,q,C=s.symbols('u v p q C',real=True)
family=1+p/r+q/r**2-v*r**2/12-u*r**3/20
equal('integrated_scalar_family',R.subs(f,family).doit(),u*r+v)
tr=clean((s.trace(E)-4*C).subs(f,family).doit()*r**2)
expected=-s.Rational(3,2)*alpha*u**2*r**4+(-u-2*alpha*u*v)*r**3+(-v-4*C)*r**2+12*alpha*u*r+6*alpha*u*p
equal('trace_polynomial',tr,expected)
equal('decisive_linear_coefficient',s.Poly(tr,r).coeff_monomial(r),12*alpha*u)
fconst=family.subs(u,0)
Econst=E.subs(f,fconst).doit().applyfunc(clean)
for i,sign in enumerate((-1,-1,1,1)):
 equal(f'constantR_full_response_{i}',Econst[i,i]+v/4,sign*(1+2*alpha*v)*q/r**4)
for i in range(4):equal(f'generic_einstein_survivor_{i}',(Econst[i,i]+v/4).subs(q,0))
critical=-1/(2*alpha)
for i in range(4):equal(f'exceptional_survivor_{i}',Econst[i,i].subs(v,critical),1/(8*alpha))
nonzero('exceptional_is_nonEinstein', (rm[1,1]-R/4).subs(f,fconst).doit().subs(v,critical),{alpha:1,p:0,q:1,r:1})
nonzero('generic_q_fails', (Econst[1,1]+v/4),{alpha:1,p:0,q:1,v:0,r:1})
fcrit=fconst.subs(v,critical)
assert fcrit.subs({alpha:1,p:0,q:1,r:1})>0
checks.append('exceptional_witness_regular_positive')
equal('exceptional_q_tangent_scalar',s.diff(R.subs(f,fcrit).doit(),q))
for i in range(4):equal(f'exceptional_q_tangent_response_{i}',s.diff(Econst[i,i].subs(v,critical),q))
equal('critical_h_coefficient',-(critical+alpha*critical**2)/2-1/(8*alpha))
equal('critical_deltaRic_coefficient',1+2*alpha*critical)
equal('critical_deltaL_coefficient',1+2*alpha*critical)

# Catch removal of a full-metric angular contribution: in a 2D calculation the
# Einstein tensor vanishes identically and would falsely admit a quartic profile.
quartic=1+r**4
full_control=G.subs(f,quartic).doit().applyfunc(clean)
nonzero('full_angular_nonvacuous_control',full_control[2,2]-full_control[0,0],{r:1})

result={'status':'PASS','count':len(checks),'checks':checks,
 'versions':{'python':platform.python_version(),'sympy':s.__version__},
 'elapsed_seconds':time.monotonic()-start,
 'scalar':str(R),'trace_polynomial':str(tr),
 'constant_R_residual':[str(clean(Econst[i,i]+v/4)) for i in range(4)],
 'limits':'Exact smooth static spherical reciprocal f>0 on connected r>0 interval. Chosen metric response under DDR; not UDT admission, empirical support or a global/causality/stability theorem.'}
Path(__file__).with_name('EXTENSION_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

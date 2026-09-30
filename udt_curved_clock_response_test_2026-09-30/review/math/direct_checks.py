"""Independent curved-null and integrating-factor anchors after candidate exposure."""
import json
import platform
import sympy as S

checks=[]
def eq(name,expr):
    residual=S.simplify(expr)
    assert residual==0,(name,residual)
    checks.append({'name':name,'type':'exact_identity','residual':str(residual)})
def bad(name,expr):
    residual=S.simplify(expr)
    assert residual!=0,(name,residual)
    checks.append({'name':name,'type':'wrong_formula_rejected','residual':str(residual)})

# Independent supplied curved comparison a(t)=t>0, not the CES1 preparation.
# Comoving proper clocks at x=0,L have tau=t^2/2. On any compact positive
# emission interval, choose a shell away from both clocks and t=0.
s,L,r,eps,f=S.symbols('s L r epsilon f',positive=True)
t,x,y,z=S.symbols('t x y z',real=True)
te=S.sqrt(2*s)
A=(te+L)**2/2
Z=S.diff(A,s)
D=S.log(Z)
alpha=s
# Actual reciprocal null equation follows from ds^2=0 in the perturbed metric.
null_slope=S.exp(2*eps*f)
eq('original_null_condition',-S.exp(-2*eps*f)*null_slope**2+S.exp(2*eps*f))
eq('linearized_null_rhs',S.diff(null_slope,eps).subs(eps,0)-2*f)
# beta is only a polynomial normalized integral anchor for a genuine smooth bump.
beta=30*r**2*(1-r)**2
eq('unit_integral_anchor',S.integrate(beta,(r,0,1))-1)
f_on_ray=alpha*beta/(2*te)
exit_delay=S.integrate(2*f_on_ray,(r,0,1))
eq('actual_exit_delay',exit_delay-alpha/te)
arrival_e=(te+L+eps*exit_delay)**2/2
V=S.diff(arrival_e,eps).subs(eps,0)
eq('curved_proper_arrival',V-Z*alpha)
Q=S.diff(S.log(S.diff(arrival_e,s)),eps).subs(eps,0)
eq('curved_nonconstant_clock_response',Q-S.diff(alpha,s)-S.diff(D,s)*alpha)
eq('explicit_positive_response',Q-(1-L/(2*(te+L))))
bad('reject_frozen_clock_drift',Q-S.diff(alpha,s))
bad('reject_coordinate_as_proper_arrival',V-exit_delay)

# Compute curvature and proper-clock geodesicity directly from g=t^2 eta.
coords=(t,x,y,z)
g=S.diag(-t*t,t*t,t*t,t*t)
ginv=g.inv()
Gamma={}
for a in range(4):
 for b in range(4):
  for c in range(4):
   Gamma[a,b,c]=S.simplify(sum(ginv[a,d]*(S.diff(g[d,c],coords[b])+S.diff(g[d,b],coords[c])-S.diff(g[b,c],coords[d])) for d in range(4))/2)
u=S.Matrix([1/t,0,0,0])
for a in range(4):
 acceleration=sum(u[b]*S.diff(u[a],coords[b]) for b in range(4))+sum(Gamma[a,b,c]*u[b]*u[c] for b in range(4) for c in range(4))
 eq('comoving_clock_geodesic_component_'+str(a),acceleration)
eq('proper_clock_normalization',(u.T*g*u)[0]+1)
a,b,c,d=1,2,1,2
R=S.diff(Gamma[a,b,d],coords[c])-S.diff(Gamma[a,b,c],coords[d])+sum(Gamma[a,j,c]*Gamma[j,b,d]-Gamma[a,j,d]*Gamma[j,b,c] for j in range(4))
Rlower=S.simplify(g[1,1]*R)
eq('nonzero_computed_curvature',Rlower-1)

# Integrating-factor mean-sign witness on a nonconstant exact readout.
M=1+s
J=1+s
alpha0=1-S.exp(-s)
eq('nonconstant_mean_integrating_factor',M*S.diff(alpha0,s)+J*alpha0-M)
bad('reject_missing_J_witness',M*S.diff(alpha0,s)-M)

print(json.dumps({'status':'PASS','python':platform.python_version(),'sympy':S.__version__,'scope':'independent exact curved comparison and mean-sign algebra; no CES1 curved solution or tube existence certified','domain':'s,L>0; t>0 compact neighborhoods; smooth compact shell underlying normalized polynomial integral control','checks':checks,'counts':{k:sum(c['type']==k for c in checks) for k in sorted({c['type'] for c in checks})}},indent=2))

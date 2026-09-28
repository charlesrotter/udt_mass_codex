#!/usr/bin/env python3
"""Bounded symbolic/finite-pulse checks; no fit or physical-law selection."""
from pathlib import Path
import hashlib
import json
import math
import platform
import sympy as s

HERE = Path(__file__).resolve().parent
x, t = s.symbols('x t', real=True)
b, a, kap, f0 = s.symbols('b a kappa f0', positive=True)
f = s.Function('f')(x)
phi = -s.log(f)/2
checks = {}
def zero(name, expression):
    checks[name] = s.simplify(expression) == 0
    if not checks[name]:
        raise AssertionError((name, s.simplify(expression)))

# Original differential equation, not just the integrated answer.
residual = 1/f-kap*s.diff(phi, x)
zero('original_Popt_residual', residual-(1+kap*s.diff(f,x)/2)/f)
affine = f0-2*x/kap
zero('affine_original_equation', residual.subs(f,affine).doit())
zero('positive_counterprofile_nonconstant', s.diff(s.exp(2*a*x)/a,x)-2*s.exp(2*a*x))
counter_residual = residual.subs(f,s.exp(-2*a*x)).doit()
zero('counterprofile_residual',counter_residual-(s.exp(2*a*x)-kap*a))

# Exact positive travel integral and proper-clock coefficient.
F = f0-b*x
O = -s.log(F/f0)/b
D = -s.log(F/f0)/2
zero('travel_integral_derivative',s.diff(O,x)-1/F)
zero('proper_clock_normalization',s.sqrt(f0)*O-2*s.sqrt(f0)*D/b)
y=s.symbols('y',real=True)
Ftilde=s.simplify(F.subs(x,s.sqrt(f0)*y)/f0)
zero('reference_normalized_profile',Ftilde-(1-b*y/s.sqrt(f0)))
zero('reference_normalized_optical_coefficient',-2/s.diff(Ftilde,y)-2*s.sqrt(f0)/b)
f_endpoint=s.symbols('f_endpoint',positive=True)
zero('two_direction_clock_product',s.sqrt(f0/f_endpoint)*s.sqrt(f_endpoint/f0)-1)
zero('local_length_to_optical_conversion',1/F-(1/s.sqrt(F))/s.sqrt(F))

# Pull back Minkowski metric; this tests flatness without using curvature formulas.
Fl=1-b*x
rho=2*s.sqrt(Fl)/b
TT=rho*s.sinh(b*t/2);XX=rho*s.cosh(b*t/2)
coords=(t,x)
J=s.Matrix([[s.diff(TT,c) for c in coords],[s.diff(XX,c) for c in coords]])
pull=J.T*s.diag(-1,1)*J
for i in range(2):
    for j in range(2):
        zero(f'flat_pullback_{i}{j}',pull[i,j]-s.diag(-Fl,1/Fl)[i,j])

# Independently construct the 2D connection and curvature on generic f.
g=s.diag(-f,1/f);ginv=g.inv();dim=2
Gamma=[[[s.simplify(sum(ginv[i,l]*(s.diff(g[l,k],coords[j])+s.diff(g[l,j],coords[k])-s.diff(g[j,k],coords[l])) for l in range(dim))/2) for k in range(dim)] for j in range(dim)] for i in range(dim)]
Ric=s.zeros(dim)
for i in range(dim):
    for j in range(dim):
        Ric[i,j]=s.simplify(sum(s.diff(Gamma[k][i][j],coords[k])-s.diff(Gamma[k][i][k],coords[j])+sum(Gamma[k][i][j]*Gamma[l][k][l]-Gamma[l][i][k]*Gamma[k][j][l] for l in range(dim)) for k in range(dim)))
R=s.simplify(s.trace(ginv*Ric))
zero('longitudinal_curvature',R+s.diff(f,x,2))
zero('affine_longitudinal_flatness',R.subs(f,Fl).doit())
U=s.Matrix([1/s.sqrt(f),0]);acc=s.Matrix([s.simplify(sum(U[j]*s.diff(U[i],coords[j]) for j in range(dim))+sum(Gamma[i][j][k]*U[j]*U[k] for j in range(dim) for k in range(dim))) for i in range(dim)])
zero('static_acceleration_norm',(acc.T*g*acc)[0]-s.diff(f,x)**2/(4*f))

# Reconstruct isotropy from a finite spanning set; the analytic argument covers all n.
H,K=s.symbols('H K');ax,ay,az=s.symbols('ax ay az')
s11,s22,s12,s13,s23=s.symbols('s11 s22 s12 s13 s23')
avec=s.Matrix([ax,ay,az]);S=s.Matrix([[s11,s12,s13],[s12,s22,s23],[s13,s23,-s11-s22]])
directions=[s.eye(3)[:,i]*sign for i in range(3) for sign in (-1,1)]
directions += [(s.eye(3)[:,i]+s.eye(3)[:,j])/s.sqrt(2) for i,j in [(0,1),(0,2),(1,2)]]
equations=[H+(avec.dot(n))+(n.T*S*n)[0]-K for n in directions]
solution=s.solve(equations,[ax,ay,az,s11,s22,s12,s13,s23,K],dict=True)
checks['all_direction_isotropy_coefficients']=solution==[{ax:0,ay:0,az:0,s11:0,s22:0,s12:0,s13:0,s23:0,K:H}]
assert checks['all_direction_isotropy_coefficients']

# Positive scale-factor control: null integral determines actual arrival map.
te,L,h=s.symbols('te L h',positive=True)
tr=-s.log(s.exp(-h*te)-h*L)/h
zero('homogeneous_arrival_slope',s.diff(tr,te)-s.exp(h*(tr-te)))
zero('homogeneous_null_incidence',(s.exp(-h*te)-s.exp(-h*tr))/h-L)

# Deliberate wrong assertions must fail nontrivially, not just fail a checksum.
mutants={
 'reciprocity_alone_implies_constant_Popt':s.simplify(s.diff(s.exp(2*a*x)/a,x))==0,
 'same_positive_shift_both_static_directions':s.simplify((f0/F)-1)==0,
 'same_coefficient_after_proper_clock_normalization':s.simplify(2*s.sqrt(f0)/b-2/b)==0,
 'shear_can_be_isotropic':s.simplify((s.Matrix([1,0,0]).T*s.diag(2,-1,-1)*s.Matrix([1,0,0]))[0]-(s.Matrix([0,1,0]).T*s.diag(2,-1,-1)*s.Matrix([0,1,0]))[0])==0,
}
assert not any(mutants.values())

# Finite-pulse probes use emission proper times and the actual arrival map.
numerics=[]
for fp in (lambda q:1-.2*q, lambda q:math.exp(-.4*q)):
    xa,xb=.2,.8;Na,Nb=math.sqrt(fp(xa)),math.sqrt(fp(xb))
    # Delay cancels for stationary observers; retain an arbitrary positive
    # constant to check the derivative of the complete arrival map itself.
    delay=1.25;eps=1e-5;ta=.4
    def arrival(tau_emit): return Nb*(tau_emit/Na+delay)
    slope=(arrival(ta+eps)-arrival(ta-eps))/(2*eps)
    numerics.append({'readout':'stationary_A_to_B','expected':Nb/Na,'measured':slope,'error':abs(slope-Nb/Na)})
hh=.2;ll=.3;ta=.1;eps=1e-5
def dynamic_arrival(tt):return -math.log(math.exp(-hh*tt)-hh*ll)/hh
slope=(dynamic_arrival(ta+eps)-dynamic_arrival(ta-eps))/(2*eps)
expected=math.exp(hh*(dynamic_arrival(ta)-ta))
numerics.append({'readout':'supplied_homogeneous_control','expected':expected,'measured':slope,'error':abs(slope-expected)})
assert max(row['error'] for row in numerics)<1e-8

result={'scope':'conditional single-context symbolic checks and floating-point pulse controls; no independent review or native admission implied','python':platform.python_version(),'sympy':s.__version__,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'exact_checks':checks,'rejected_mutants':{k:not v for k,v in mutants.items()},'finite_pulse_controls':numerics,'max_pulse_error':max(row['error'] for row in numerics),'passed':all(checks.values()) and not any(mutants.values())}
(HERE/'CHECK_RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))

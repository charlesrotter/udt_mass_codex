"""Exact scoped coefficient/linear-response checks; no native law adoption.

All free coefficients are mathematical controls from WORK_ORDER.md. The symbol
calculation is an exact first variation, not a finite-amplitude approximation.
"""
import json
import platform
import time
from pathlib import Path
import sympy as s

start = time.monotonic()
checks = {}
def eq(name, actual, expected=0):
    residual = s.factor(s.expand(actual-expected))
    if residual != 0:
        raise AssertionError((name, residual))
    checks[name] = {"residual": str(residual)}
def nz(name, value):
    value = s.factor(value)
    if value == 0:
        raise AssertionError((name, value))
    checks[name] = {"nonzero_control": str(value)}

eta = s.diag(-1, 1, 1, 1)
q = s.Matrix(s.symbols('q0:4', real=True))
q_up = eta*q
q2 = (q.T*eta*q)[0]
a, b, alpha, rho = s.symbols('a b alpha rho', real=True)
def sym_matrix(prefix, n):
    values = iter(s.symbols(f'{prefix}0:{n*(n+1)//2}', real=True))
    m = s.zeros(n)
    for i in range(n):
        for j in range(i, n):
            m[i,j] = m[j,i] = next(values)
    return m
def pair(u,v):
    return s.trace(eta*u*eta*v)
def curvature(h):
    tr = s.trace(eta*h)
    ric = s.Matrix(4,4,lambda i,j: (-q[i]*(q_up.T*h[:,j])[0]
          -q[j]*(q_up.T*h[:,i])[0]+q2*h[i,j]+q[i]*q[j]*tr)/2)
    scalar = s.expand(s.trace(eta*ric))
    return ric, scalar
def linear_response(h):
    ric, scalar = curvature(h)
    return a*ric+b*eta*scalar

h, k = sym_matrix('h',4), sym_matrix('k',4)
ric_h, r_h = curvature(h)
eq('scalar_symbol',r_h,-(q_up.T*h*q_up)[0]+q2*s.trace(eta*h))
for j in range(4):
    eq(f'linear_bianchi_{j}',(q_up.T*ric_h)[j],q[j]*r_h/2)
skew = pair(k,linear_response(h))-pair(h,linear_response(k))
_, r_k = curvature(k)
expected = (a/2+b)*(s.trace(eta*k)*r_h-s.trace(eta*h)*r_k)
eq('full_arbitrary_symbol_helmholtz_skew',skew,expected)
hv, kv = s.diag(1,1,0,0), eta
qv = dict(zip(q,(0,1,0,0)))
witness = s.expand(pair(kv,linear_response(hv))-pair(hv,linear_response(kv))).subs(qv)
eq('one_symbol_necessity_witness',witness,-2*(a+2*b))
eq('einstein_symbol_self_adjoint',skew.subs(b,-a/2))
nz('tracefree_ricci_not_unrestricted_variational',witness.subs({a:1,b:-s.Rational(1,4)}))

# Existing full primary curvature formula supplies an off-shell nonconstant-R
# control; it is not a response-law solution or a new metric-family derivation.
r = s.symbols('r', positive=True)
f = 1+r**3
R = -s.diff(f,r,2)-4*s.diff(f,r)/r-2*(f-1)/r**2
eq('nonconstant_scalar_control',R,-20*r)
nz('on_shell_off_shell_divergence_discriminator',s.diff(R,r)/4)

# Auxiliary rewrite: alpha is nonzero; never divide by psi.
psi, Rvar, lam = s.symbols('psi Rvar lam', real=True)
aux = psi*Rvar-(psi-1)**2/(4*alpha)+2*lam
eq('auxiliary_scalar_equation',s.diff(aux,psi),Rvar-(psi-1)/(2*alpha))
eq('auxiliary_elimination_density',aux.subs(psi,1+2*alpha*Rvar),Rvar+alpha*Rvar**2+2*lam)
eq('trace_sector_variation_sign',-s.diff(2*lam*s.symbols('volume'),s.symbols('volume'))/2,-lam)

P = -eta*q2+q*q.T
def quadratic_response(h):
    ric, scalar = curvature(h)
    return ric-eta*scalar/2+2*alpha*P*scalar
eq('quadratic_linearized_trace',s.trace(eta*quadratic_response(h)),-(1+6*alpha*q2)*r_h)
lift = -2*alpha*rho*eta
_, lift_R = curvature(lift)
eq('scalar_lift_curvature',lift_R,-6*alpha*q2*rho)
lift_E = quadratic_response(lift)
for i in range(4):
    for j in range(i,4):
        eq(f'scalar_lift_full_residual_factor_{i}{j}',lift_E[i,j],-2*alpha*P[i,j]*(1+6*alpha*q2)*rho)
shell = {q[0]**2:q[1]**2+q[2]**2+q[3]**2+1/(6*alpha)}
eq('scalar_shell_reproduces_rho',s.expand(lift_R).subs(shell),rho)
for i in range(4):
    for j in range(i,4):
        eq(f'scalar_shell_full_equation_{i}{j}',s.factor(lift_E[i,j]).subs(shell))
nz('nonzero_scalar_gauge_invariant_control',s.expand(lift_R).subs(shell).subs(rho,1))
tt = s.diag(0,1,-1,0)
wave = {q[0]:1,q[1]:0,q[2]:0,q[3]:1}
for i in range(4):
    for j in range(i,4):
        eq(f'TT_null_full_equation_{i}{j}',quadratic_response(tt)[i,j].subs(wave))

# Pointwise orthonormal spatial frame checks the invariant Legendre map;
# this does not independently compute the canonical Poisson bracket.
A, root_h = s.symbols('A root_h', nonzero=True, real=True)
K = sym_matrix('K',3)
trK = s.trace(K)
pi = root_h/A*(K-trK*s.eye(3))
velocity_residual = A/root_h*(pi-s.trace(pi)*s.eye(3)/2)-K
for i in range(3):
    for j in range(i,3):
        eq(f'legendre_velocity_inverse_{i}{j}',velocity_residual[i,j])
kinetic = A/root_h*(s.trace(pi*pi)-s.trace(pi)**2/2)
eq('legendre_kinetic_contraction',kinetic,root_h/A*(s.trace(K*K)-trK**2))
eq('legendre_transform',2*s.trace(pi*K)-kinetic,root_h/A*(s.trace(K*K)-trK**2))

result={"status":"PASS","count":len(checks),"checks":checks,
        "python":platform.python_version(),"sympy":s.__version__,
        "elapsed_seconds":time.monotonic()-start,
        "helmholtz_witness":str(s.factor(witness)),
        "scalar_lift_factor":"-2 alpha P_ab (1+6 alpha q^2) rho",
        "limits":"Conditional class/response mathematics and exact first variations only; no native admission, nonlinear existence, complete mode count, stability, or full hyperbolicity proof."}
Path(__file__).with_name('PARENT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

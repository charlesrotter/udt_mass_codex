"""Exact author checks; spatial connection plus ADM first variation, not a PDE solve."""
import hashlib
import json
import platform
from pathlib import Path
import sympy as S

x, y, z, e = S.symbols('x y z e', real=True)
coords = (x, y, z)
u = S.Function('u')(x)
h = S.diag(1, S.exp(2*u), S.exp(-2*u))
hi = h.inv()
s = -S.Rational(2, 3)
K = S.diag(-s/2 + S.diff(u, x)**2/(2*s), s, s)
kcov = h*K
tau = S.trace(K)
checks = {}

def simp(a):
    return a.applyfunc(S.simplify) if isinstance(a, S.MatrixBase) else S.simplify(a)

def zero(name, a):
    a = simp(a)
    ok = a == S.zeros(*a.shape) if isinstance(a, S.MatrixBase) else a == 0
    checks[name] = bool(ok)
    if not ok:
        raise AssertionError((name, a))

G = [[[simp(sum(hi[i,l]*(S.diff(h[l,k], coords[j]) + S.diff(h[l,j], coords[k])
                      - S.diff(h[j,k], coords[l])) for l in range(3))/2)
       for k in range(3)] for j in range(3)] for i in range(3)]
Ric = S.Matrix(3, 3, lambda i,j: simp(sum(
    S.diff(G[k][i][j], coords[k])-S.diff(G[k][i][k], coords[j])
    + sum(G[k][k][l]*G[l][i][j]-G[k][j][l]*G[l][i][k] for l in range(3))
    for k in range(3))))
Rm = simp(hi*Ric)
R = S.trace(Rm)
zero('full_Hamiltonian', R+tau**2-S.trace(K*K))
momentum = S.Matrix([sum(S.diff(K[j,i], coords[j]) + sum(
    G[j][j][l]*K[l,i]-G[l][j][i]*K[j,l] for l in range(3)) for j in range(3))
    - S.diff(tau, coords[i]) for i in range(3)])
zero('all_three_momentum_components', momentum)
zero('scalar_curvature', R+2*S.diff(u,x)**2)

def curl(cov):
    # epsilon_ikl = [ikl], since det(h)=1; raise the two derivative/tensor indices.
    D = [[[simp(S.diff(cov[l,j], coords[k])-sum(G[m][k][l]*cov[m,j]
        + G[m][k][j]*cov[l,m] for m in range(3))) for j in range(3)]
        for l in range(3)] for k in range(3)]
    raw = S.Matrix(3,3,lambda i,j: sum(S.LeviCivita(i,k,l)*hi[k,k]*hi[l,l]*D[k][l][j]
        for k in range(3) for l in range(3)))
    return simp((raw+raw.T)/2)

Em = simp(Rm+tau*K-K*K)
Bcov = -curl(kcov)  # B_ij = epsilon_i^kl C_klj0 / 2, negative-K convention.
zero('E_trace', S.trace(Em))
zero('B_trace', S.trace(hi*Bcov))
Ec = simp(h*Em)
curlB = simp(hi*curl(Bcov))
curlE = simp(hi*curl(Ec))

# Independent spatial-Ricci first variation from coordinate Christoffels.
dh = -2*kcov
dhi = -hi*dh*hi
dG = [[[simp(sum(dhi[i,l]*(S.diff(h[l,k], coords[j])+S.diff(h[l,j], coords[k])
    -S.diff(h[j,k], coords[l])) + hi[i,l]*(S.diff(dh[l,k], coords[j])
    +S.diff(dh[l,j], coords[k])-S.diff(dh[j,k], coords[l])) for l in range(3))/2)
    for k in range(3)] for j in range(3)] for i in range(3)]
dRic = S.Matrix(3,3,lambda i,j: simp(sum(
    S.diff(dG[k][i][j], coords[k])-S.diff(dG[k][i][k], coords[j])
    +sum(dG[k][k][l]*G[l][i][j]+G[k][k][l]*dG[l][i][j]
        -dG[k][j][l]*G[l][i][k]-G[k][j][l]*dG[l][i][k] for l in range(3))
    for k in range(3))))
dRm = simp(dhi*Ric+hi*dRic)
dK = simp(Rm+tau*K)
dtau = S.trace(dK)
dE = simp(dRm+dtau*K+tau*dK-dK*K-K*dK)
zero('trace_ADM_E_derivative', S.trace(dE))
KEtf = simp(K*Em-S.eye(3)*S.trace(K*Em)/3)
local = simp(2*tau*Em-3*KEtf)
zero('full_E_Bianchi_against_ADM', dE-local-curlB)

def at_origin(a):
    return simp(a.subs(u,e*S.cos(x)).doit().subs(x,0))

E0, B0, K0, dE0 = map(at_origin, (Em, hi*Bcov, K, dE))
zero('origin_B', B0)
zero('origin_curlE_and_hence_projected_Bdot', at_origin(curlE))
zero('origin_E_expected', E0-S.diag(-S.Rational(4,9),S.Rational(2,9)+e,S.Rational(2,9)-e))
zero('origin_Edot_direct', dE0-S.diag(S.Rational(8,9),-S.Rational(4,9)+e,-S.Rational(4,9)-e))
zero('origin_curlB_nontrivial_formula', at_origin(curlB)-S.diag(0,e,-e))

def diagnostic(Q):
    return simp(1-6*S.trace(Q**3)**2/S.trace(Q**2)**3)

def rate(Q,F):
    i2, i3 = S.trace(Q**2), S.trace(Q**3)
    return simp(36*i3*(i3*S.trace(Q*F)-i2*S.trace(Q**2*F))/i2**4)

d = S.symbols('d', real=True)
A = diagnostic(E0).subs(e,2*d/9)
Adot = rate(E0,dE0).subs(e,2*d/9)
targetA = d**2*(d**2-9)**2/(d**2+3)**3
targetRate = 162*d**2*(d**2-1)*(d**2-9)/(d**2+3)**4
zero('shape_formula', A-targetA)
zero('rate_formula', Adot-targetRate)
zero('curl_contribution', rate(E0,at_origin(curlB)).subs(e,2*d/9)-d*S.diff(targetA,d))
zero('local_contribution', rate(E0,at_origin(local)).subs(e,2*d/9)-2*d*S.diff(targetA,d))
zero('amplitude_null', rate(E0,E0))
Omega = S.Matrix([[0,1,2],[-1,0,3],[-2,-3,0]])
zero('frame_commutator_null', rate(E0,Omega*E0-E0*Omega))
probe = S.Rational(1,9)
assert S.trace(E0**2).subs(e,probe) != 0
assert rate(E0,dE0).subs(e,probe) > 0
checks['rational_probe_nonzero_positive'] = True
mutant = simp((dE0-at_origin(local)).subs(e,probe))
assert mutant != S.zeros(3)
checks['dropping_curl_detected'] = True
wrong_inverse = at_origin(hi*dRic+dtau*K+tau*dK-dK*K-K*dK)
assert simp((wrong_inverse-dE0).subs(e,probe)) != S.zeros(3)
checks['omitting_inverse_metric_derivative_detected'] = True

# All Kasner exponents in the usual rational chart, not only an isotropic control.
w,T = S.symbols('w T', positive=True)
ps = (-w/(1+w+w*w),(1+w)/(1+w+w*w),w*(1+w)/(1+w+w*w))
EK = S.diag(*[p*(1-p)/T**2 for p in ps])
KK = S.diag(*[-p/T for p in ps])
zero('Kasner_KE_STF', KK*EK-S.eye(3)*S.trace(KK*EK)/3)
zero('Kasner_shape_rate', rate(EK,S.diff(EK,T)))

print(json.dumps({
    'python':platform.python_version(),'sympy':S.__version__,
    'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'check_kind':'exact symbolic spatial geometry plus ADM first variation; not existence proof',
    'checks':checks,'all_passed':all(checks.values()),
    'E_origin':str(E0),'B_origin':str(B0),'E_dot_origin':str(dE0),
    'A_delta':str(S.factor(A)),'nA_delta':str(S.factor(Adot)),
    'rational_epsilon_1_9_rate':str(rate(E0,dE0).subs(e,probe)),
    'curl_omission_residual':str(mutant),
    'omitted':'no PDE integration, genericity, long-time or physical identification'
},indent=2))

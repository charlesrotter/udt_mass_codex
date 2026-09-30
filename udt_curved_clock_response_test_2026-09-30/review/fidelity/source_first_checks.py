"""Independent exact anchors; no producer scientific code or numerical geometry."""
import json
import platform
import sympy as sp

checks = []
rejections = []

def identity(name, expression):
    value = sp.simplify(expression)
    assert value == 0, (name, value)
    checks.append(name)

def wrong(name, difference):
    value = sp.simplify(difference)
    assert value != 0, (name, value)
    rejections.append({"name": name, "nonzero_difference": str(value)})

eps, f, E, alpha, Z, psi = sp.symbols('eps f E alpha Z psi', real=True, nonzero=True)
G = sp.diag(-1, 1)
H = sp.diag(2, 2)
l = sp.Matrix([E, E])
identity('null tangent', (l.T * G * l)[0])
identity('reciprocal trace', sp.trace(G.inv() * H))
identity('null reciprocal contraction', (l.T * H * l)[0] - 4*E**2)
family = sp.diag(-sp.exp(-2*eps*f), sp.exp(2*eps*f))
identity('finite plane determinant', family.det()+1)
for i in range(2):
    identity('finite reciprocal tangent '+str(i), sp.diff(family[i,i],eps).subs(eps,0)-f*H[i,i])
rho = sp.symbols('rho', real=True)
identity('normalized integrand', sp.Rational(1,2)*(psi*rho/(2*E**2))*(l.T*H*l)[0]-psi*rho)
identity('affine action scaling', sp.Rational(1,2)*alpha**2*(2*psi)/alpha-alpha*psi)
identity('affine frequency cancellation', alpha*psi/(alpha/Z)-Z*psi)
s = sp.symbols('s', real=True)
D = sp.Function('D')(s)
P = sp.Function('P')(s)
A = sp.Function('a')(s)
W = sp.Function('w')(s)
M = sp.Function('M')(s)
N = sp.Function('N')(s)
full = sp.diff(sp.exp(D)*P,s)/sp.exp(D)
identity('moving arrival slope', full-sp.diff(P,s)-sp.diff(D,s)*P)
affine_full = sp.diff(A*P/(A/sp.exp(D)),s)/sp.exp(D)
identity('variable affine normalization', affine_full-full)
identity('second contrast moment', sp.diff(D**2,s)/2-D*sp.diff(D,s))
identity('integration by parts coefficient', -sp.diff(W*M,s)+W*N+sp.diff(W,s)*M+W*sp.diff(M,s)-W*N)
eta = sp.symbols('eta', positive=True)
v = (sp.exp(2*eta)-1)/(sp.exp(2*eta)+1)
clock_rate = 2*sp.exp(eta)/(sp.exp(2*eta)+1)
identity('flat physical rapidity clock ratio', clock_rate/(1-v)-sp.exp(eta))
K, d, ds, p = sp.symbols('K d ds p', real=True)
identity('same sign witness integrand', d*(K*p+ds*p)-d*p*(K+ds))
wrong('missing D_s drift', (full-sp.diff(P,s)).subs({D:s, P:1}).doit())
omega = A/sp.exp(D)
bad_denominator = sp.diff(A*P,s)/omega/sp.exp(D)
wrong('missing receiver frequency derivative', (affine_full-bad_denominator).subs({A:sp.exp(2*s), D:s, P:1}).doit())
wrong('half reciprocal tangent', (l.T*(H/2)*l)[0]-4*E**2)
wrong('missing label weight derivative', (-sp.diff(W*M,s)+W*sp.diff(M,s)).subs({W:s**2+1, M:2}).doit())
result = {"status":"PASS", "identities":checks, "wrong_formulas_rejected":rejections,
          "python":platform.python_version(), "sympy":sp.__version__,
          "scope":"Exact algebra only; geometric tube/support and continuity are analytic hypotheses/arguments.",
          "shapes":{"reciprocal_plane":[2,2],"null_tangent":[2,1]}}
print(json.dumps(result, indent=2, sort_keys=True))

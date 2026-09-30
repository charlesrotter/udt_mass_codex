"""Author exact diagnostic; supplied metric family, no physical adoption."""
import json
import platform
import sympy as s

t, x, y, z = coordinates = s.symbols('t x y z', real=True)
kappa = s.symbols('kappa', real=True)
A = s.Function('A')(t)  # FREE: smooth and positive on the diagnostic domain.
g = s.diag(-1, A**2, A**2, A**2*s.exp(2*kappa*x))
gi = g.inv()
n = 4
Gamma = [[[s.simplify(sum(gi[a,d]*(s.diff(g[d,c], coordinates[b])
                 + s.diff(g[d,b], coordinates[c])
                 - s.diff(g[b,c], coordinates[d])) for d in range(n))/2)
           for c in range(n)] for b in range(n)] for a in range(n)]

def zero(value):
    assert s.simplify(value) == 0, str(value)

beta = [A, 0, 0, 0]
for a in range(n):
    for b in range(n):
        lie = sum(beta[c]*s.diff(g[a,b], coordinates[c])
                  + g[c,b]*s.diff(beta[c], coordinates[a])
                  + g[a,c]*s.diff(beta[c], coordinates[b]) for c in range(n))
        zero(lie - 2*s.diff(A,t)*g[a,b])
for a in range(n):
    zero(Gamma[a][0][0])  # U = partial_t is unit and geodesic.
theta = sum(Gamma[a][a][0] for a in range(n))
zero(theta - 3*s.diff(A,t)/A)
for a in range(1,n):
    for b in range(1,n):
        zero(Gamma[0][a][b] - theta*g[a,b]/3)

ray = [1/A, 1/A**2, 0, 0]
zero(sum(g[a,b]*ray[a]*ray[b] for a in range(n) for b in range(n)))
for a in range(n):
    zero(sum(ray[b]*s.diff(ray[a],coordinates[b]) for b in range(n))
         + sum(Gamma[a][b][c]*ray[b]*ray[c] for b in range(n) for c in range(n)))
zero(A*ray[0]-1)  # omega=ray[0], so omega/Theta=1 with Theta=1/A.

Ric = s.zeros(n)
for a in range(n):
    for b in range(n):
        Ric[a,b] = s.simplify(sum(
            s.diff(Gamma[c][a][b],coordinates[c])
            - s.diff(Gamma[c][a][c],coordinates[b])
            + sum(Gamma[c][c][d]*Gamma[d][a][b]
                  - Gamma[c][b][d]*Gamma[d][a][c] for d in range(n))
            for c in range(n)))
R = s.simplify(sum(gi[a,b]*Ric[a,b] for a in range(n) for b in range(n)))
expected = 6*s.diff(A,t,2)/A + 6*s.diff(A,t)**2/A**2 - 2*kappa**2/A**2
zero(R-expected)
zero(R-R.subs(kappa,0)+2*kappa**2/A**2)
null_Ric = s.simplify(sum(Ric[a,b]*ray[a]*ray[b]
                         for a in range(n) for b in range(n)))
zero(null_Ric-null_Ric.subs(kappa,0)+kappa**2/A**4)
print(json.dumps({
    'status':'PASS', 'evidence_type':'author exact symbolic diagnostic',
    'python':platform.python_version(), 'sympy':s.__version__,
    'metric_shape':[4,4], 'coordinate_order':['t','x','y','z'],
    'checks':['CKV beta=A*partial_t', 'U geodesic', 'expansion=3A_prime/A',
              'zero shear', 'affine radial null ray', 'A*omega conserved',
              'scalar curvature difference', 'null Ricci difference'],
    'scalar_curvature':str(R), 'null_Ricci':str(null_Ric),
    'not_checked':['native admission','observational fit','global completion',
                   'Einstein equation','physical radiation identification',
                   'independent review']},indent=2))

"""Original source-first diagnostic; standard geometry, no producer imports."""
import json
import platform
import sympy as s

t, x, y, z = s.symbols('t x y z', real=True)
coords = (t, x, y, z)
g = s.diag(-1, t**6, t**6, t**6)
gi = g.inv()
d = 4
checks = []

def check(name, actual, expected):
    if isinstance(actual, s.MatrixBase):
        diff = (actual - expected).applyfunc(s.simplify)
        assert diff == s.zeros(*diff.shape), (name, diff)
    else:
        assert s.simplify(actual - expected) == 0, (name, actual, expected)
    checks.append(name)

conn = [[[s.simplify(sum(gi[k,l] * (
    s.diff(g[l,j], coords[i]) + s.diff(g[l,i], coords[j])
    - s.diff(g[i,j], coords[l])) / 2 for l in range(d)))
    for j in range(d)] for i in range(d)] for k in range(d)]
ric = s.Matrix(d, d, lambda i,j: s.simplify(sum(
    s.diff(conn[k][i][j], coords[k]) - s.diff(conn[k][i][k], coords[j])
    + sum(conn[k][k][l]*conn[l][i][j] - conn[k][j][l]*conn[l][i][k]
          for l in range(d)) for k in range(d))))

def trace(tensor):
    return s.simplify(sum(gi[i,j]*tensor[i,j] for i in range(d) for j in range(d)))

def tf(tensor):
    return (tensor - trace(tensor)*g/4).applyfunc(s.simplify)

def divergence(tensor):
    return s.Matrix([s.simplify(sum(gi[a,c]*(
        s.diff(tensor[a,b], coords[c])
        - sum(conn[k][c][a]*tensor[k,b] + conn[k][c][b]*tensor[a,k]
              for k in range(d))) for a in range(d) for c in range(d)))
        for b in range(d)])

R = trace(ric)
G = ric - R*g/2
S = tf(ric)
dR = s.Matrix([s.diff(R, q) for q in coords])
zero = s.zeros(4,1)
a, b, C, Lam = s.symbols('a b C Lambda', real=True)
E = a*ric+b*R*g+C*g
check('Ricci from original metric', ric, s.diag(-18/t**2,24*t**4,24*t**4,24*t**4))
check('Scalar curvature', R, 90/t**2)
check('Off-shell div Ric equals half dR', divergence(ric), dR/2)
check('Off-shell div G vanishes', divergence(G), zero)
check('Ricci and Einstein trace-free parts agree', tf(G), S)
check('Pure trace is DDR invisible', tf(G+C*g), S)
check('Shape divergence is quarter dR', divergence(S), dR/4)
check('Correct scalar completion conserves', divergence(S-R*g/4+C*g), zero)
check('General class divergence', divergence(E), (a/2+b)*dR)
check('Conservation preserves shape equation', tf(a*G+C*g), a*S)
assert divergence(ric)[0] != 0
assert divergence(S)[0] != 0
assert divergence(S+R*g/4)[0] != 0
checks.append('Nonzero controls reject automatic Ric/shape conservation and wrong trace sign')

eta = s.diag(-1,1,1,1)
on_shell_E = a*(Lam*eta-4*Lam*eta/2)+C*eta
check('DDR solution representative can remain nonzero', on_shell_E, (C-a*Lam)*eta)
check('Full equation fixes extra scalar combination', on_shell_E.subs(C,a*Lam), s.zeros(4))
assert on_shell_E.subs({a:2,C:1,Lam:3}) != s.zeros(4)
checks.append('Nonzero DDR versus full-equation control')

# Change the metric variation convention for the SAME nonzero pairing.
g0 = g.subs(t,2)
inv0 = g0.inv()
E0 = ric.subs(t,2)
h = s.Matrix([[2,1,0,0],[1,3,0,0],[0,0,5,0],[0,0,0,7]])
hinv = -inv0*h*inv0
volume = s.sqrt(-g0.det())
raised = inv0*E0*inv0
pair_inverse = volume*sum(E0[i,j]*hinv[i,j] for i in range(d) for j in range(d))
pair_covariant = sum((-volume*raised[i,j])*h[i,j] for i in range(d) for j in range(d))
check('Same-action covariant density requires minus sign', pair_inverse, pair_covariant)
assert pair_inverse != 0 and pair_inverse != -pair_covariant
checks.append('Wrong-sign density control is nonzero')

print(json.dumps({
    'scope':'exact supplied-metric and representative/equation controls; not native physics',
    'python':platform.python_version(), 'sympy':s.__version__,
    'metric':'diag(-1,t^6,t^6,t^6), t>0', 'shape':[4,4],
    'arithmetic':'exact symbolic/rational; no tolerance', 'checks':checks,
    'count':len(checks), 'Ricci':str(ric), 'R':str(R),
    'div_Ric':str(divergence(ric)), 'div_TF_Ric':str(divergence(S)),
    'div_general_response':str(divergence(E)),
    'on_DDR_Einstein_class_full_response':str(on_shell_E),
    'same_action_pairing':str(pair_inverse)
},indent=2))

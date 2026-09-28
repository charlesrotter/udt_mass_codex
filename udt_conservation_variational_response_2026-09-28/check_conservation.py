"""Exact supplied-metric checks, not a proof of general classification/physics."""
import hashlib
import json
from pathlib import Path
import platform
import sys
import sympy as s

t, x, y, z = coords = s.symbols('t x y z', real=True)
N = 1 + x**2 + y**3  # FREE mathematical witness; N>0 near x=y=1.
g = s.diag(-N**2, 1, 1, 1)
gi = g.inv()
n = 4
simp = s.factor
Gamma = [[[simp(sum(gi[a, d] * (s.diff(g[d, c], coords[b])
    + s.diff(g[d, b], coords[c]) - s.diff(g[b, c], coords[d]))
    for d in range(n)) / 2) for c in range(n)] for b in range(n)] for a in range(n)]
Ric = s.Matrix(n, n, lambda a, b: simp(sum(
    s.diff(Gamma[c][a][b], coords[c]) - s.diff(Gamma[c][a][c], coords[b])
    + sum(Gamma[c][c][d] * Gamma[d][a][b]
          - Gamma[c][b][d] * Gamma[d][a][c] for d in range(n))
    for c in range(n))))
R = simp(s.trace(gi * Ric))
G = Ric - R * g / 2
S0 = Ric - R * g / 4
S1 = R * S0

def div(E):
    return s.Matrix([simp(sum(gi[a, c] * (
        s.diff(E[a, b], coords[c]) - sum(Gamma[d][c][a] * E[d, b]
        + Gamma[d][c][b] * E[a, d] for d in range(n)))
        for a in range(n) for c in range(n))) for b in range(n)])

checks = []
def equal(name, left, right):
    defect = simp(left-right)
    checks.append({'name': name, 'passed': defect == 0, 'residual': str(defect)})

def nonzero(name, value):
    exact = simp(value)
    checks.append({'name': name, 'passed': exact != 0, 'value': str(exact)})

expected = s.diag(N*(s.diff(N,x,2)+s.diff(N,y,2)), -s.diff(N,x,2)/N,
                  -s.diff(N,y,2)/N, 0)
for a in range(n):
    for b in range(n):
        equal(f'Ricci from full metric {a}{b}', Ric[a,b], expected[a,b])
equal('scalar from full metric', R, -2*(2+6*y)/N)
equal('trace S0', s.trace(gi*S0), 0)
equal('trace S1', s.trace(gi*S1), 0)
dR = s.Matrix([s.diff(R, v) for v in coords])
j0, j1 = div(S0), div(S1)
divRic, divG = div(Ric), div(G)
for b in range(n):
    equal(f'contracted Bianchi {b}', divRic[b], dR[b]/2)
    equal(f'Einstein divergence {b}', divG[b], 0)
    equal(f'trace-free Ricci divergence {b}', j0[b], dR[b]/4)
    equal(f'nonlinear trace-free divergence {b}', j1[b], (Ric*gi*dR)[b])
    equal(f'conservative trace primitive {b}', j0[b]+s.diff(-R/4,coords[b]), 0)
equal('j nonlinear x', j1[1], -16*x*(3*y+1)/N**3)
equal('j nonlinear y', j1[2], 72*y*(x*x-2*y**3-y*y+1)/N**3)
curl1 = simp(s.diff(j1[2],x)-s.diff(j1[1],y))
curl0 = simp(s.diff(j0[2],x)-s.diff(j0[1],y))
point = {x: 1, y: 1}
equal('Ricci trace completion curl zero', curl0, 0)
equal('nonlinear curl at regular point', curl1.subs(point), s.Rational(16,3))
nonzero('reject all natural responses have trace completion', curl1.subs(point))
nonzero('reject Ricci identically conserved', divRic[1].subs(point))
nonzero('reject wrong plus sign in scalar primitive',
        (j0[1]+s.diff(R/4,x)).subs(point))
equal('regular lapse at witness', N.subs(point), 3)
equal('Lorentz determinant at witness', g.det().subs(point), -9)
# Passing trace-free DDR does not imply conservation of its chosen representative.
trivial = R*g
equal('pure trace DDR is vacuous', s.trace(gi*trivial)/4, R)
divtrivial = div(trivial)
for b in range(n):
    equal(f'pure trace divergence {b}', divtrivial[b], dR[b])
nonzero('reject DDR alone implies conservation', divtrivial[1].subs(point))

result = {'kind': 'exact symbolic/rational witness checks', 'python': platform.python_version(),
    'sympy': s.__version__, 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'metric': str(g), 'ricci': str(Ric), 'scalar': str(R),
    'j_nonlinear': str(j1), 'curl_nonlinear': str(curl1),
    'point': {'x':1,'y':1}, 'curl_value': str(curl1.subs(point)),
    'checks': checks, 'passed': all(c['passed'] for c in checks),
    'limitations': ['one supplied static witness, not full metric coverage',
        'no proof of general inverse-variational or classification theorem',
        'no adopted physical response or empirical GR-filter claim']}
with Path(sys.argv[1]).open('x') as f:
    json.dump(result,f,indent=2); f.write('\n')
print(json.dumps({'passed':result['passed'],'checks':len(checks),
                  'curl_value':result['curl_value']}))
assert result['passed'], [c for c in checks if not c['passed']]

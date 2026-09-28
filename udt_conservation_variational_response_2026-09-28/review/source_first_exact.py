"""Independent CRV1 source-first check; no producer code imported.

One smooth Lorentz4 chart t,y>0; UNADOPTED mathematical witness.
Metric/sign/chart/profile: free-and-explored comparison choices.
Exact arithmetic, one process, no fitting/grid/GPU; capture supplies 60s/512MiB.
"""
import hashlib
import json
import pathlib
import platform
import sys

import sympy as s

t, x, y, z = s.symbols('t x y z', real=True)
q = (t, x, y, z)
n = 4
g = s.diag(-1, t**4, 1, y**4)
gi = g.inv()
clean = lambda value: s.factor(s.cancel(value))
Gamma = [[[clean(sum(gi[a, d] * (
    s.diff(g[d, c], q[b]) + s.diff(g[d, b], q[c])
    - s.diff(g[b, c], q[d])) / 2 for d in range(n)))
    for c in range(n)] for b in range(n)] for a in range(n)]
Ric = s.Matrix(n, n, lambda a, b: clean(sum(
    s.diff(Gamma[c][a][b], q[c]) - s.diff(Gamma[c][a][c], q[b])
    + sum(Gamma[c][a][b]*Gamma[d][c][d]
          - Gamma[d][a][c]*Gamma[c][b][d] for d in range(n))
    for c in range(n))))

def trace(T):
    return clean(sum(gi[a, b]*T[a, b] for a in range(n) for b in range(n)))

def div(T):
    # Compute g^{ac} nabla_c T_ab directly, not from Bianchi or product formula.
    return s.Matrix([clean(sum(gi[a, c]*(s.diff(T[a, b], q[c]) - sum(
        Gamma[d][c][a]*T[d, b] + Gamma[d][c][b]*T[a, d]
        for d in range(n))) for a in range(n) for c in range(n)))
        for b in range(n)])

def grad(f):
    return s.Matrix([s.diff(f, coord) for coord in q])

checks = {}
def zero(name, expression):
    values = list(expression) if isinstance(expression, s.MatrixBase) else [expression]
    checks[name] = all(clean(v) == 0 for v in values)
    assert checks[name], (name, values)

def nonzero(name, expression):
    checks[name] = clean(expression) != 0
    assert checks[name], (name, expression)

R = trace(Ric)
Q = clean(trace(Ric*gi*Ric))
A = clean(4/t**2)
B = clean(-4/y**2)
T = Ric - R*g/4
S = Q*T
j = div(S)
curl_ty = clean(s.diff(j[2], t) - s.diff(j[0], y))
point = {t: s.Integer(1), y: s.Integer(2)}

zero('Ricci_from_metric_vs_product_formula', Ric-s.diag(-2/t**2, 2*t**2, -2/y**2, -2*y**2))
zero('scalar_curvature', R-A-B)
zero('Ricci_squared', Q-(A**2+B**2)/2)
zero('tracefree_Ricci', trace(T))
zero('tracefree_trial_S', trace(S))
zero('contracted_Bianchi', div(Ric)-grad(R)/2)
zero('Einstein_divergence', div(Ric-R*g/2))
zero('shape_divergence', div(T)-grad(R)/4)
zero('pure_trace_DDR', R*g-trace(R*g)*g/4)
zero('pure_trace_divergence', div(R*g)-grad(R))
nonzero('pure_trace_divergence_t_nonzero', div(R*g)[0].subs(point))
nonzero('Ricci_offshell_divergence_t_nonzero', div(Ric)[0].subs(point))
expected_j = s.Matrix([
    (3*A**2-2*A*B+B**2)*s.diff(A,t)/8,
    0,
    (A**2-2*A*B+3*B**2)*s.diff(B,y)/8,
    0,
])
zero('independent_product_formula_for_j', j-expected_j)
zero('curl_product_formula', curl_ty-(A-B)*s.diff(A,t)*s.diff(B,y)/2)
zero('curl_exact_value', curl_ty.subs(point)+20)
nonzero('trace_completion_obstruction', curl_ty.subs(point))
f = -R/4
zero('linear_shape_completion', div(T+f*g))
zero('wrong_sign_trace_completion_rejected', div(T-f*g)-grad(R)/2)
nonzero('wrong_sign_trace_completion_really_nonzero', div(T-f*g)[0].subs(point))
# Controls must distinguish absent factors and reversed orientation.
nonzero('drop_Q_gradient_control_rejected', (j-Q*div(T))[0].subs(point))
nonzero('reverse_curl_control_rejected', (-curl_ty-(-20)).subs(point))

result = {
    'scope': 'Exact single UNADOPTED metric witness; not native UDT or GR-filter admission',
    'versions': {'python': sys.version, 'sympy': s.__version__, 'platform': platform.platform()},
    'coordinates': [str(v) for v in q], 'domain': 't>0,y>0',
    'metric': str(g), 'Ricci': str(Ric), 'R': str(R), 'Q': str(Q),
    'S_definition': 'Q*(Ric-R*g/4)', 'j_components': [str(v) for v in j],
    'dj_ty': str(curl_ty), 'point': {'t': 1, 'y': 2},
    'dj_ty_at_point': str(curl_ty.subs(point)),
    'j_at_point': [str(v.subs(point)) for v in j],
    'checks': checks, 'passed': sum(checks.values()),
    'implementation': 'Original source-first Christoffel/Ricci/covariant-divergence loops; shared SymPy library, no producer imports',
    'script_sha256': hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
}
target = pathlib.Path(__file__).with_name('source_first_exact_result.json')
with target.open('x') as stream:
    json.dump(result, stream, indent=2)
    stream.write('\n')
print(json.dumps(result, indent=2))

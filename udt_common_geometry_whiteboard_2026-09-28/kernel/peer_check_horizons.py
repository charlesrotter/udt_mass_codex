#!/usr/bin/env python3
"""Independent static-metric HR1/HR2 checks; exact and deliberately narrow."""
import os
for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[name] = '2'
import resource
resource.setrlimit(resource.RLIMIT_AS, (2 * 1024**3, 2 * 1024**3))
import datetime, hashlib, json, pathlib, platform, time
import sympy as s
start = time.monotonic()
out = pathlib.Path(__file__).with_name('PEER_CHECK_RESULT.json')
if out.exists():
    raise RuntimeError('Refusing to overwrite saved peer check result')
checks = []
def zero(name, expr):
    residual = s.simplify(expr)
    checks.append({'name': name, 'residual': str(residual), 'pass': residual == 0})
def nonzero(name, expr):
    residual = s.simplify(expr)
    checks.append({'name': name, 'negative_control': str(residual),
                   'pass': bool(residual != 0)})
def metric_objects(g, coords):
    gi = g.inv()
    n = len(coords)
    connection = [[[s.simplify(sum(gi[a,d] * (
        s.diff(g[d,c], coords[b]) + s.diff(g[d,b], coords[c])
        - s.diff(g[b,c], coords[d])) / 2 for d in range(n)))
        for c in range(n)] for b in range(n)] for a in range(n)]
    ricci = s.Matrix(n, n, lambda b,d: s.simplify(sum(
        s.diff(connection[a][d][b], coords[a])
        - s.diff(connection[a][a][b], coords[d])
        + sum(connection[a][a][e]*connection[e][d][b]
              - connection[a][d][e]*connection[e][a][b]
              for e in range(n)) for a in range(n))))
    return connection, s.simplify(sum(gi[b,d]*ricci[b,d]
                                     for b in range(n) for d in range(n)))
t, l = s.symbols('t l', real=True)
E, k = s.symbols('E k', positive=True)
N = s.Function('N')(l)
g = s.diag(-N**2, 1)
coords = (t, l)
Gamma, curvature = metric_objects(g, coords)
zero('original_Ricci_scalar', curvature + 2*s.diff(N,l,2)/N)
for sign in (-1, 1):
    tangent = s.Matrix([E/N**2, sign*E/N])
    zero(f'null_sign_{sign}', (tangent.T*g*tangent)[0])
    for a in range(2):
        acc = sum(tangent[b]*s.diff(tangent[a],coords[b]) for b in range(2))
        acc += sum(Gamma[a][b][c]*tangent[b]*tangent[c]
                   for b in range(2) for c in range(2))
        zero(f'original_affine_equation_sign_{sign}_component_{a}', acc)
    zero(f'calibrated_tape_rate_sign_{sign}', N*tangent[1]-sign*E)
U = s.Matrix([1/N, 0])
zero('static_unit_norm', (U.T*g*U)[0]+1)
zero('frequency_from_original_metric', -(U.T*g*s.Matrix([E/N**2,E/N]))[0]-E/N)
zero('static_proper_acceleration', Gamma[1][0][0]/N**2-s.diff(N,l)/N)
zero('HR2_depth_curvature', s.diff(-s.log(N),l)**2-s.diff(-s.log(N),l,2)-s.diff(N,l,2)/N)
calibrated = s.diag(1,1/N).T*g*s.diag(1,1/N)
zero('G176_calibrated_determinant', calibrated.det()+1)
zero('G176_calibrated_radial_entry', calibrated[1,1]-1/N**2)
Ns = s.symbols('N_source', positive=True)
R = 1/Ns
ordered_depth = -s.log(R)
redshift_depth = -s.log(Ns)
zero('redshift_and_ordered_depth_have_opposite_sign', ordered_depth+redshift_depth)
zero('anchor_received_factor_N_half', R.subs(Ns,s.Rational(1,2))-2)
zero('anchor_ordered_depth_N_half', ordered_depth.subs(Ns,s.Rational(1,2))+s.log(2))
nonzero('wrong_depth_sign_N_half', (ordered_depth-redshift_depth).subs(Ns,s.Rational(1,2)))
nonzero('wrong_optical_equals_affine_density_N_half', (1/Ns-Ns).subs(Ns,s.Rational(1,2)))
p = s.symbols('p', positive=True)
base = 1+k*l/p
primitive = p*(base**(1-p)-1)/(k*(1-p))
zero('p_not_one_affine_primitive', s.diff(primitive,l)-base**(-p))
zero('p_one_affine_primitive', s.diff(s.log(1+k*l)/k,l)-1/(1+k*l))
zero('common_initial_depth_slope', s.diff(p*s.log(base),l).subs(l,0)-k)
for pv, expected in [(s.Rational(1,2), s.oo), (s.Integer(1),s.oo), (s.Integer(2),2/k)]:
    expression = s.log(1+k*l)/k if pv==1 else primitive.subs(p,pv)
    limit = s.limit(expression,l,s.oo)
    checks.append({'name': f'explicit_tail_p_{pv}', 'limit': str(limit),
                   'pass': limit == expected})
zero('exponential_tape_primitive', s.diff((1-s.exp(-k*l))/k,l)-s.exp(-k*l))
zero('exponential_affine_endpoint', s.limit((1-s.exp(-k*l))/(E*k),l,s.oo)-1/(E*k))
v, tape = s.symbols('v tape', real=True)
lapse = 1-k*tape
jacobian = s.Matrix([[1,-1/lapse**2],[0,1/lapse]])
ef = s.simplify(jacobian.T*s.diag(-lapse**2,1)*jacobian)
zero('EF_metric_vv', ef[0,0]+lapse**2)
zero('EF_metric_vs', ef[0,1]-1)
zero('EF_metric_ss', ef[1,1])
zero('EF_nondegenerate_at_horizon', ef.det().subs(tape,1/k)+1)
ef_gamma, ef_curvature = metric_objects(ef,(v,tape))
zero('EF_finite_curvature', ef_curvature+2*k**2)
crossing = s.Matrix([0,-E])
zero('EF_crossing_null', (crossing.T*ef*crossing)[0])
zero('EF_crossing_Killing_energy', -(ef*crossing)[0]-E)
for a in range(2):
    zero(f'EF_affine_crossing_equation_{a}', ef_gamma[a][1][1]*E**2)
result = {
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'scope': 'Independent peer checks of supplied HR1/HR2 static radial class only',
    'python': platform.python_version(), 'sympy': s.__version__,
    'script_sha256': hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
    'runtime_seconds': time.monotonic()-start,
    'peak_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    'checks': checks, 'all_pass': all(c['pass'] for c in checks)}
payload = json.dumps(result, indent=2)+'\n'
out.write_text(payload)
print(payload, end='')
raise SystemExit(0 if result['all_pass'] else 1)

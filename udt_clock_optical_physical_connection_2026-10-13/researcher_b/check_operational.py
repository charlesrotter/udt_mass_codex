"""Finite exact controls frozen in PROBE_FREEZE; not a general proof or fit."""
import hashlib
import json
import platform
from pathlib import Path
import sympy as s

records = []

def check(name, residual, **details):
    value = s.simplify(residual)
    passed = value == 0
    records.append(dict(name=name, passed=bool(passed), residual=str(value), **details))
    if not passed:
        raise AssertionError((name, str(value)))

def ricci_direct(g, x):
    """Coordinate Christoffel/Ricci calculation from supplied original metrics."""
    n = len(x)
    inv = g.inv()
    G = [[[s.simplify(sum(inv[a, d] * (s.diff(g[d, c], x[b]) +
            s.diff(g[d, b], x[c]) - s.diff(g[b, c], x[d])) / 2
            for d in range(n))) for c in range(n)] for b in range(n)] for a in range(n)]
    R = s.zeros(n)
    for b in range(n):
        for d in range(n):
            R[b, d] = s.simplify(sum(s.diff(G[a][d][b], x[a]) -
                s.diff(G[a][a][b], x[d]) + sum(G[a][a][m] * G[m][d][b] -
                    G[a][d][m] * G[m][a][b] for m in range(n)) for a in range(n)))
    return R, s.simplify(s.trace(inv * R))

def coeff(expr, var, degree):
    return s.expand(s.series(expr, var, 0, degree + 1).removeO()).coeff(var, degree)

t, r, th, ph = s.symbols('t r th ph', real=True)
K, ell, accel = s.symbols('K ell accel', positive=True)
x = [t, r, th, ph]
F = 1 - K * r**2
metrics = [
    ('de_sitter', s.diag(-F, 1/F, r**2, r**2*s.sin(th)**2),
     s.tanh(s.sqrt(K)*ell)**2/(K*ell**2), 12*K),
    ('ultrastatic_spatial_curvature', s.diag(-1, 1/F, r**2, r**2*s.sin(th)**2),
     s.sin(s.sqrt(K)*ell)**2/(K*ell**2), 6*K),
]
for name, metric, normalized_area, expected in metrics:
    Ric, Scal = ricci_direct(metric, x)
    check(name+'_original_metric_scalar', Scal-expected, scalar=str(Scal))
    check(name+'_exact_radar_area', coeff(normalized_area, ell, 2)+Scal/18,
          normalized_area=str(normalized_area))
    if name.startswith('ultrastatic'):
        check(name+'_clock_tide_zero', Ric[0, 0], interpretation='Clock ratios equal one by time translation.')

# Exact accelerated-Minkowski control; the source clock is not geodesic.
accelerated_area = (s.sinh(accel*ell)/(accel*ell))**2
check('accelerated_minkowski_area', coeff(accelerated_area, ell, 2)-accel**2/3)

# Generic symmetric Ricci tensor, and a trace-compatible electric tensor.
rr = s.symbols('R00 R01 R02 R03 R11 R12 R13 R22 R23 R33')
Ric = s.Matrix([[rr[0],rr[1],rr[2],rr[3]], [rr[1],rr[4],rr[5],rr[6]],
                [rr[2],rr[5],rr[7],rr[8]], [rr[3],rr[6],rr[8],rr[9]]])
eta = s.diag(-1,1,1,1)
Scal = s.trace(eta*Ric)
u = s.Matrix([1,0,0,0])
rho_mean = s.Integer(0)
for i in [1,2,3]:
    for sign in [-1,1]:
        n = s.zeros(4,1); n[i] = sign
        rho_mean += ((u+n).T * Ric * (u+n))[0]/6
check('six_direction_null_mean', rho_mean-(Scal+4*rr[0])/3)
area_mean = 2*rr[0]/9-rho_mean/6
check('scalar_radar_mean_cancellation', area_mean+Scal/18)

# Cubic distance ambiguity and concrete radar correction.
e, rho, b, z = s.symbols('e rho b z', real=True)
lambda_of_s = z-b*z**3
area_in_s = s.expand(lambda_of_s**2*(1-rho*lambda_of_s**2/6)/z**2)
check('cubic_reparameterization', coeff(area_in_s,z,2)+rho/6+2*b)
check('radar_coefficient', coeff(area_in_s.subs(b,-e/3),z,2)-(4*e-rho)/6)

# Fermi radial geodesic and return jets, checked as formal cubic expansions.
lam = s.symbols('lam', real=True)
t_lam = lam-e*lam**3/3
r_lam = lam-e*lam**3/6
check('Fermi_time_geodesic_linear_residual', coeff(s.diff(t_lam,lam,2)+2*e*r_lam,lam,1))
check('Fermi_radial_geodesic_linear_residual', coeff(s.diff(r_lam,lam,2)+e*r_lam,lam,1))
radar_lam = r_lam-e*r_lam**3/6
check('radar_affine_cubic_relation', coeff(radar_lam,lam,3)+e/3)

# Exact same-plane boost: U'=(5/4)U+(3/4)n, n'=(3/4)U+(5/4)n.
c, h = s.Rational(5,4),s.Rational(3,4)
check('rational_boost_lorentz', c*c-h*h-1)
check('rational_boost_bivector', c*c-h*h-1)
check('rational_boost_null_rescaling', c+h-2)
# GRC1 alpha,beta,gamma=(6,2,1), tangential ray; all unboosted sky areas negative.
n1 = s.symbols('n1', real=True)
e0 = -2-4*n1**2
rho0 = -5+5*n1**2
check('grc1_unboosted_sky', (4*e0-rho0)/6+(3+21*n1**2)/6)
check('grc1_boosted_area_failure', s.Rational(4*(-2)-4*(-5),6)-s.Integer(2))

inputs = ['INITIAL_PROPOSAL.md','PROBE_FREEZE.md','OPERATIONAL_CANDIDATE.md','check_operational.py']
root = Path(__file__).resolve().parent
output = dict(status='PASS', evidence_kind='finite exact symbolic controls, same researcher',
              python=platform.python_version(),sympy=s.__version__,checks=records,
              inputs_sha256={p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in inputs},
              omissions=['No finite-size error constant','No full theorem mechanization',
                         'No physical attribution test data','No independent context or implementation claim'])
print(json.dumps(output,indent=2))

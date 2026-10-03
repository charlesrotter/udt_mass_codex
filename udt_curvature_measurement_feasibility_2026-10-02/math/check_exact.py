"""CMF1 separately authored exact algebra and counterexample checks.

No parent/sibling modules or calculations imported. PSW1 coefficients are an
accepted conditional input, not claimed rederived here. Geometric test values
and boosts are FREE controls, not physical choices. CPU finite symbolic work.
"""
from pathlib import Path
from itertools import product
from fractions import Fraction
import hashlib
import json
import platform
import sys
import sympy as s

BASE = Path(__file__).resolve().parent
checks = []


def check(name, expression, expected=0):
    remainder = s.simplify(expression - expected)
    if remainder != 0:
        raise AssertionError((name, str(remainder)))
    checks.append(name)


# Linear map generated from arbitrary symmetric tensors, not preinserted trace.
indices = [(i, j) for i in range(4) for j in range(i, 4)]
coeffs = s.symbols('c0:10')
C = s.zeros(4)
for (i, j), coeff in zip(indices, coeffs):
    C[i, j] = C[j, i] = coeff
v = s.Rational(3, 5)
gamma = s.Rational(5, 4)
frames = [s.eye(4)[:, 0]]
for i in range(1, 4):
    for sign in [1, -1]:
        frames.append(gamma * (s.eye(4)[:, 0] + sign * v * s.eye(4)[:, i]))
eta = s.diag(-1, 1, 1, 1)
for i, u in enumerate(frames):
    check(f'unit_timelike_{i}', (u.T * eta * u)[0], -1)
observations = [(u.T * C * u)[0] for u in frames]
design = s.Matrix([[s.diff(q, c) for c in coeffs] for q in observations])
target = sum(eta[i, i] * C[i, i] for i in range(4))
trace_row = s.Matrix([s.diff(target, c) for c in coeffs])
weight_solution = list(s.linsolve((design.T, trace_row)))[0]
check('design_rank', design.rank(), 7)
check('unseen_dimensions', len(design.nullspace()), 3)
for j, w in enumerate(weight_solution):
    check(f'weight_{j}', w, -s.Rational(28, 3) if j == 0 else s.Rational(8, 9))
check('arbitrary_tensor_trace', sum(w*q for w, q in zip(weight_solution, observations)), target)
for j, null in enumerate(design.nullspace()):
    check(f'unseen_preserves_trace_{j}', (trace_row.T * null)[0])
check('worst_case_noise_weight', sum(abs(w) for w in weight_solution), s.Rational(44, 3))

# Original algebraic curvature of product time x constant-curvature space.
K = s.symbols('K')
spatial_dot = lambda u, w: sum(u[i]*w[i] for i in range(1, 4))


def A(x, y, z, w):
    return K*(spatial_dot(y, z)*spatial_dot(x, w)-spatial_dot(x, z)*spatial_dot(y, w))


basis = [s.eye(4)[:, i] for i in range(4)]
ric = s.Matrix(4, 4, lambda a, b: sum(eta[i, i]*A(basis[i], basis[a], basis[b], basis[i]) for i in range(4)))
for i in range(3):
    for j in range(3):
        check(f'one_frame_invisible_{i}_{j}', A(basis[i+1], basis[0], basis[0], basis[j+1]))
check('spatial_product_scalar', s.trace(eta*ric), 6*K)
check('boost_reveals_transverse_tide', A(basis[2], frames[1], frames[1], basis[2]), s.Rational(9, 16)*K)
check('clock_trace_of_product', sum(weight_solution[i]*(u.T*ric*u)[0] for i,u in enumerate(frames)), 6*K)

# Nine-point Lorentzian stencil from monomial values, including quartic bias.
x = s.symbols('x0:4')
h = s.symbols('h', nonzero=True)
signs = [-1, 1, 1, 1]
zero = dict.fromkeys(x, 0)


def stencil(expression):
    center = expression.subs(zero)
    result = 0
    for i, sign in enumerate(signs):
        plus = zero | {x[i]: h}
        minus = zero | {x[i]: -h}
        result += sign*(expression.subs(plus)-2*center+expression.subs(minus))/h**2
    return s.expand(result)


for degrees in product(range(5), repeat=4):
    if sum(degrees) > 4:
        continue
    monomial = s.prod(xi**degree for xi, degree in zip(x, degrees))
    exact = sum(sign*s.diff(monomial, xi, 2) for sign,xi in zip(signs,x)).subs(zero)
    fourth = h**2*sum(sign*s.diff(monomial, xi, 4) for sign,xi in zip(signs,x)).subs(zero)/12
    check('stencil_monomial_'+''.join(map(str,degrees)), stencil(monomial), exact+fourth)
stencil_weights = [-2*sum(signs)] + [sign for sign in signs for _ in range(2)]
check('stencil_center_weight', stencil_weights[0], -4)
check('stencil_noise_norm', sum(abs(w) for w in stencil_weights), 12)


def metric_curvature(metric, time):
    """Original connection and Ricci for metrics depending only on coordinate0."""
    inv = metric.inv()
    derivative = lambda e, i: s.diff(e, time) if i == 0 else s.S(0)
    G = [[[s.simplify(sum(inv[a,d]*(derivative(metric[d,c],b)+derivative(metric[d,b],c)-derivative(metric[b,c],d))/2 for d in range(4))) for c in range(4)] for b in range(4)] for a in range(4)]
    Ric = s.Matrix(4, 4, lambda a,b: s.simplify(sum(derivative(G[c][a][b],c)-derivative(G[c][a][c],b)+sum(G[c][c][d]*G[d][a][b]-G[c][b][d]*G[d][a][c] for d in range(4)) for c in range(4))))
    scalar = s.simplify(sum(inv[a,b]*Ric[a,b] for a in range(4) for b in range(4)))
    return G, Ric, scalar


# Trace equation false-pass witness, independently differentiated metric.
t, k = s.symbols('t k', real=True)
metric = s.diag(-1, 1+2*k*t, 1+2*k*t, 1+2*k*t)
connection, ric, scalar = metric_curvature(metric, t)
check('trace_witness_scalar', scalar)
check('trace_witness_00_original', ric[0,0] - scalar*metric[0,0]/2, 3*k**2/(1+2*k*t)**2)
assert (ric[0,0] - scalar*metric[0,0]/2).subs({t:0,k:1}) == 3
checks.append('trace_pass_does_not_imply_tensor_pass')

# Independent conformal-coordinate geometry: L is conformal time in this
# prescribed homogeneous clock experiment, a(L)=p(L), d/dt=(1/p)d/dL.
L = s.symbols('L', real=True)
p = s.Function('p')(L)
conformal = s.diag(-p**2, p**2, p**2, p**2)
G, Ric, R = metric_curvature(conformal, L)
check('original_metric_clock_scalar', R, 6*s.diff(p,L,2)/p**3)
b3,b4,b5,alpha,beta,Lambda = s.symbols('b3 b4 b5 alpha beta Lambda', nonzero=True)
pj = s.exp(b3*L**3+b4*L**4+b5*L**5)
Rj = R.subs(p,pj).doit()
dot = lambda expression: s.diff(expression,L)/pj
Hj = s.diff(pj,L)/pj**2
Fj = 1+2*alpha*Rj+3*beta*Rj**2
fj = Rj+alpha*Rj**2+beta*Rj**3
trace = -3*(dot(dot(Fj))+3*Hj*dot(Fj))+Fj*Rj-2*fj
d0 = s.simplify(trace.subs(L,0))
d1 = s.simplify(s.diff(trace,L).subs(L,0))
check('original_scalar_trace_initial_residual', d0, -864*alpha*b4-23328*beta*b3**2)
check('original_scalar_trace_first_residual', d1, -4320*alpha*b5-279936*beta*b3*b4-36*b3)
solb4 = s.solve(d0,b4)[0]
solb5 = s.solve(d1.subs(b4,solb4),b5)[0]
check('derived_quartic_relation', solb4, -27*beta*b3**2/alpha)
check('derived_quintic_relation', solb5, -b3/(120*alpha)+s.Rational(12,5)*solb4**2/b3)

# A nonzero trace residual is a real rejection check: perturb the predicted b4.
assert s.simplify(d0.subs(b4,solb4+1)) == -864*alpha
checks.append('wrong_quartic_candidate_rejected')

# Exact parameter identification under the conditional quadratic necessary test.
# Use Fraction arithmetic independently of the tensor algebra library.
alpha0 = Fraction(7, 3)
lam0 = Fraction(-2, 5)
xs = [Fraction(-4,7), Fraction(11,13), Fraction(3,2)]
ys = [(r-4*lam0)/(6*alpha0) for r in xs]
alpha_fit = (xs[1]-xs[0])/(6*(ys[1]-ys[0]))
lam_fit = (xs[0]-6*alpha_fit*ys[0])/4
assert (alpha_fit,lam_fit)==(alpha0,lam0)
assert 6*alpha_fit*ys[2]-xs[2]+4*lam_fit == 0
assert 6*alpha_fit*(ys[2]+Fraction(1,100))-xs[2]+4*lam_fit != 0
checks += ['fraction_two_point_parameter_recovery','fraction_heldout_survivor','fraction_heldout_bad_record_rejected']

z = s.symbols('z')
f = z+alpha*z**2+beta*z**3
F = s.diff(f,z)
background = s.expand(F*z-2*f+4*Lambda)
check('background_root_polynomial', background, beta*z**3-z+4*Lambda)
mass = s.factor((F-z*s.diff(F,z))/(3*s.diff(F,z)))
check('cubic_flat_pole', mass.subs(z,0), 1/(6*alpha))
check('cubic_pole_slope', s.diff(mass,z).subs(z,0), -beta/(2*alpha**2))
check('root_derivative_is_pole_numerator_negative', s.diff(background,z), z*s.diff(F,z)-F)

result = {
    'status':'PASS_EXACT_FINITE_CHECKS_NOT_EMPIRICAL_CONFIRMATION',
    'checks':checks,
    'check_count':len(checks),
    'design':{'rank':7,'nullity':3,'weights':[str(w) for w in weight_solution], 'noise_l1':'44/3'},
    'stencil':{'dimension':4,'records':9,'central_weight':-4,'noise_l1':12},
    'trace_counterexample':{'metric':'diag(-1,1+2kt,1+2kt,1+2kt)','scalar_R':'0','E00_at_t0_k1':'3'},
    'clock_residuals':{'constant':str(d0),'linear':str(d1)},
    'versions':{'python':sys.version,'sympy':s.__version__,'platform':platform.platform()},
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'limits':['PSW1 limiting clock theorem inherited, not independently reproved','No full tensor recovery, apparatus simulation or empirical data','Scalar trace is necessary only; clock jet relations are necessary coefficients only']
}
with (BASE/'EXACT_RESULT.json').open('x') as stream:
    json.dump(result,stream,indent=2)
    stream.write('\n')
print(json.dumps(result,indent=2))

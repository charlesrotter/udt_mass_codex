"""Independent exact witness checks; no author/source-package implementation import.

This is not a census or proof of the general differentiability estimate.
All coefficients are fixed mathematical values in declared component units.
The derivative witness uses the campaign's conditional ambient tensor slots;
it makes no claim that every such slot collection is a realizable metric jet.
"""
from fractions import Fraction as Q
import hashlib
import itertools
import json
import platform
from pathlib import Path

N = 4
SIGN = (-1, 1, 1, 1)
ETA = tuple(tuple(Q(SIGN[i] if i == j else 0) for j in range(N)) for i in range(N))
ZERO = tuple(tuple(Q(0) for _ in range(N)) for _ in range(N))
checks = []
catches = []


def gate(label, condition):
    if not condition:
        raise AssertionError(label)
    checks.append(label)


def add(*matrices):
    return tuple(tuple(sum(a[i][j] for a in matrices) for j in range(N)) for i in range(N))


def scale(c, a):
    return tuple(tuple(c * a[i][j] for j in range(N)) for i in range(N))


def trace(a):
    return sum(SIGN[i] * a[i][i] for i in range(N))


def tf(a):
    return add(a, scale(-trace(a) / N, ETA))


def square(a):
    return tuple(tuple(sum(a[i][k] * SIGN[k] * a[k][j] for k in range(N)) for j in range(N)) for i in range(N))


def maxnorm(a):
    return max(abs(x) for row in a for x in row)


def realize_ricci(a):
    scalar = trace(a)
    return {
        (i, j, k, l): (
            ETA[i][k] * a[j][l] - ETA[i][l] * a[j][k]
            - ETA[j][k] * a[i][l] + ETA[j][l] * a[i][k]
        ) / (N - 2) - scalar * (
            ETA[i][k] * ETA[j][l] - ETA[i][l] * ETA[j][k]
        ) / ((N - 1) * (N - 2))
        for i, j, k, l in itertools.product(range(N), repeat=4)
    }


def ricci(curvature):
    return tuple(tuple(sum(SIGN[i] * curvature[i, j, i, l] for i in range(N)) for l in range(N)) for j in range(N))


def pullback2(a, boost):
    return tuple(tuple(sum(boost[p][i] * boost[q][j] * a[p][q] for p in range(N) for q in range(N)) for j in range(N)) for i in range(N))


def check_curvature(curvature, name):
    gate(name + ':first_pair', all(v == -curvature[j, i, k, l] for (i, j, k, l), v in curvature.items()))
    gate(name + ':last_pair', all(v == -curvature[i, j, l, k] for (i, j, k, l), v in curvature.items()))
    gate(name + ':pair_exchange', all(v == curvature[k, l, i, j] for (i, j, k, l), v in curvature.items()))
    gate(name + ':bianchi', all(curvature[i, j, k, l] + curvature[i, k, l, j] + curvature[i, l, j, k] == 0 for i, j, k, l in curvature))


def caught(label, actual, wrong):
    try:
        assert actual == wrong, label
    except AssertionError:
        catches.append(label)
    else:
        raise AssertionError('false pass: ' + label)


# Explicit mixed-Ricci involution: nonzero S, zero TF(Ric^2).
involution = tuple(tuple(Q(SIGN[i] * (1 if i < 2 else -1) if i == j else 0) for j in range(N)) for i in range(N))
curvature = realize_ricci(involution)
check_curvature(curvature, 'involution_realizer')
gate('involution_realizes_ricci', ricci(curvature) == involution)
gate('involution_scalar_zero', trace(involution) == 0)
gate('involution_tracefree_nonzero', tf(involution) != ZERO)
gate('involution_square_metric', square(involution) == ETA)
gate('quadratic_DDR_without_Ricci_DDR', tf(square(involution)) == ZERO)
caught('reject_DDR_implies_S_zero_without_nonzero_a', tf(involution), ZERO)

# A generic Ricci witness with both nonzero trace and quadratic TF part.
generic = tuple(tuple(Q(((2, 1, 0, 0), (1, 3, 1, 0), (0, 1, -2, 1), (0, 0, 1, 5))[i][j]) for j in range(N)) for i in range(N))
generic_curvature = realize_ricci(generic)
check_curvature(generic_curvature, 'generic_realizer')
gate('generic_realizes_ricci', ricci(generic_curvature) == generic)
S = tf(generic)
Q2 = tf(square(generic))
gate('nonvacuous_quadratic', Q2 != ZERO)
gate('nonvacuous_trace', trace(generic) != 0)
H = tf(add(generic, involution))
gate('nonvacuous_hessian', H != ZERO)

# A rank-six formal derivative slot with scalar-curvature Hessian H.
# D_abcdmn = (eta_ac eta_bd - eta_ad eta_bc) H_mn / 12.
# Double curvature contraction gives exactly H, independently of tf algebra.
recovered_hessian = tuple(tuple(sum(
    SIGN[i] * SIGN[j] * (ETA[i][i] * ETA[j][j] - ETA[i][j] * ETA[j][i]) * H[m][n] / 12
    for i in range(N) for j in range(N)
) for n in range(N)) for m in range(N))
gate('formal_derivative_scalar_hessian', recovered_hessian == H)

# Nonzero coefficient and deliberately nonhomogeneous fixed polynomial germ.
a, b, d, q, c = Q(3, 2), Q(-2, 5), Q(7, 3), Q(-5, 4), Q(13, 7)
rates = []
for k in (2, 4, 8, 16):
    eps, delta = Q(1, k * k), Q(1, k)
    Aeps = scale(eps, generic)
    Deps = scale(eps * delta * delta, recovered_hessian)
    full = add(scale(c, ETA), scale(a, Aeps), scale(b * trace(Aeps), ETA), scale(d, Deps), scale(q, square(Aeps)))
    predicted = add(scale(a * eps, S), scale(d * eps * delta * delta, H), scale(q * eps * eps, Q2))
    gate('exact_TF_expansion:' + str(k), tf(full) == predicted)
    error = add(tf(full), scale(-a * eps, S))
    bound = abs(d) * eps * delta * delta * maxnorm(H) + abs(q) * eps * eps * maxnorm(Q2)
    gate('exact_remainder_bound:' + str(k), maxnorm(error) <= bound)
    rates.append({'k': k, 'epsilon': str(eps), 'delta': str(delta), 'error_over_epsilon': str(maxnorm(error) / eps), 'bound_over_epsilon': str(bound / eps)})
    caught('detect_dropped_even_derivative:' + str(k), tf(full), add(scale(a * eps, S), scale(q * eps * eps, Q2)))
    caught('detect_dropped_quadratic:' + str(k), tf(full), add(scale(a * eps, S), scale(d * eps * delta * delta, H)))
    caught('detect_missing_trace_projection:' + str(k), tf(full), full)

# A fixed even-derivative response can cancel a nonzero aS when no slow hierarchy is imposed.
cancel_H = scale(-a / d, S)
gate('unsuppressed_even_derivative_cancellation', add(scale(a, S), scale(d, cancel_H)) == ZERO)
gate('cancellation_not_Einstein', S != ZERO)

# Rational boost: checks covariance but does not assert arbitrary-boost norm uniformity.
boost = ((Q(5, 3), Q(4, 3), Q(0), Q(0)), (Q(4, 3), Q(5, 3), Q(0), Q(0)), (Q(0), Q(0), Q(1), Q(0)), (Q(0), Q(0), Q(0), Q(1)))
gate('boost_metric', pullback2(ETA, boost) == ETA)
boosted = pullback2(generic, boost)
gate('boost_trace', trace(boosted) == trace(generic))
gate('boost_TF', tf(boosted) == pullback2(S, boost))
gate('boost_square', square(boosted) == pullback2(square(generic), boost))
gate('boost_quadratic_TF', tf(square(boosted)) == pullback2(Q2, boost))
gate('all_expected_catches', len(catches) == 13)

print(json.dumps({
    'status': 'PASS_EXACT_WITNESSES_ONLY',
    'python': platform.python_version(),
    'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'implementation': 'standard-library Fraction; independent code; no author imports',
    'scope': 'conditional algebraic curvature and ambient derivative slots; not actual metric development or a general proof',
    'checks': checks,
    'check_count': len(checks),
    'hostile_catches': catches,
    'hostile_catch_count': len(catches),
    'rates': rates,
    'counterexample': {'mixed_Ricci_diagonal': [1, 1, -1, -1], 'scalar': '0', 'S_nonzero': True, 'TF_Ricci_squared_zero': True},
    'omissions': ['G301 full basis census reused, not rerun', 'No actual metric-jet realization theorem', 'No physical class-membership theorem', 'No uniform rate for all differentiable maps', 'No UDT coefficient or scale adoption']
}, indent=2))

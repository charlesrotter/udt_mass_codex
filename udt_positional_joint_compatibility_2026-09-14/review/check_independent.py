"""Small exact source-formula checks; no physical-admission assertion."""
from fractions import Fraction as F
import datetime
import hashlib
import json
from pathlib import Path
import platform
import sys


def clean(p):
    return {n: F(a) for n, a in p.items() if a}


def add(*ps):
    out = {}
    for p in ps:
        for n, a in p.items():
            out[n] = out.get(n, F(0)) + a
    return clean(out)


def scale(p, a):
    return clean({n: a * b for n, b in p.items()})


def shift(p, n):
    return {k + n: a for k, a in p.items()}


def diff(p):
    return clean({n - 1: n * a for n, a in p.items()})


def evaluate(p, x):
    return sum((a * x ** n for n, a in p.items()), F(0))


def amplitudes(p):
    first = diff(p)
    transverse = add({0: F(1)}, scale(p, -1), scale(shift(first, 1), F(1, 2)))
    longitudinal = scale(add(shift(diff(first), 2), scale(shift(first, 1), -1)), F(1, 2))
    return transverse, longitudinal


def equal(a, b):
    assert a == b, (a, b)


profiles = [
    {0: F(1)},
    {0: F(1), 2: F(2, 3)},
    {0: F(1), 2: F(3, 7), 4: F(5, 11), 6: F(1, 13)},
    {0: F(2), -2: F(1, 9), -1: F(1, 3), 1: F(2, 5), 3: F(4, 7)},
]
radii = [F(1, 2), F(1), F(3, 2)]
samples = []
for profile in profiles:
    transverse, longitudinal = amplitudes(profile)
    equal(longitudinal, shift(diff(transverse), 1))
    equal(diff(shift(profile, -2)), scale(shift(add(transverse, {0: F(-1)}), -3), 2))
    for homogeneous in (F(-3, 7), F(0), F(11, 5)):
        equal(amplitudes(add(profile, {2: homogeneous})), (transverse, longitudinal))
    for r in radii:
        f = evaluate(profile, r)
        fp = evaluate(diff(profile), r)
        fpp = evaluate(diff(diff(profile)), r)
        assert f > 0
        p = -r * fp / (2 * f)
        zeta = -r * r * fpp / (2 * f) + r * r * fp * fp / (2 * f * f)
        equal(f * (2 * p * p + p - zeta), evaluate(longitudinal, r))
        equal(1 - f * (1 + p), evaluate(transverse, r))
        samples.append({"r": str(r), "f": str(f), "A_perp": str(evaluate(transverse, r)),
                        "A_parallel": str(evaluate(longitudinal, r))})

# At x=1+y, exp(epsilon*y*y)=1+epsilon*y*y+O(y^4).
# Coefficients through y^3 are exact Taylor coefficients for every real epsilon.
diagnostics = []
for epsilon in (F(-7, 3), F(0), F(5, 2)):
    local = {0: F(2), 1: F(2), 2: 1 + 2 * epsilon, 3: 2 * epsilon}
    jets = [evaluate(local, F(0)), evaluate(diff(local), F(0)), evaluate(diff(diff(local)), F(0))]
    equal(jets, [F(2), F(2), 2 + 4 * epsilon])
    f, fp, fpp = jets
    equal(1 - f + fp / 2, F(0))
    equal((fpp - fp) / 2, 2 * epsilon)
    equal([1 / f, -fp / (f * f)], [F(1, 2), F(-1, 2)])
    diagnostics.append({"epsilon": str(epsilon), "jets": list(map(str, jets)),
                        "A_perp": "0", "A_parallel": str(2 * epsilon)})

directions = []
N, fp = F(3, 2), F(3, 5)
gradient = -fp / (2 * N)
for t in (F(-2), F(-1, 2), F(0), F(1, 3), F(1), F(3)):
    cosine, sine = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)
    equal(cosine * cosine + sine * sine, F(1))
    depth, screen = gradient * cosine, gradient * sine
    equal(depth * depth + screen * screen, gradient * gradient)
    directions.append({"cos": str(cosine), "sin": str(sine), "sum": str(gradient * gradient)})

catches = {}
profile = profiles[2]
transverse, longitudinal = amplitudes(profile)
mutations = {
    "longitudinal_first_derivative_sign": (
        scale(add(shift(diff(diff(profile)), 2), shift(diff(profile), 1)), F(1, 2)),
        shift(diff(transverse), 1)),
    "transverse_constant_dropped": (
        add(shift(diff(profile), 1), scale(profile, -2)),
        scale(add(transverse, {0: F(-2)}), 2)),
}
for name, (bad, expected) in mutations.items():
    try:
        equal(bad, expected)
    except AssertionError:
        catches[name] = "REJECTED_BY_EQUALITY_CHECK"
    else:
        raise AssertionError("mutation passed: " + name)

print(json.dumps({
    "status": "PASS_BOUNDED_EXACT_FORMULA_CHECKS",
    "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "python": sys.version,
    "platform": platform.platform(),
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "implementation": "standard-library Fraction Laurent polynomials and exact Taylor jets; no parent scientific import",
    "profile_count": len(profiles), "positive_regular_samples": samples,
    "diagnostic_cases": diagnostics, "projection_cases": directions, "mutation_catches": catches,
    "maximum_claim": "supplement to source-first calculus argument; no all-UDT countermodel, physical admission, or source theorem replay",
}, indent=2))

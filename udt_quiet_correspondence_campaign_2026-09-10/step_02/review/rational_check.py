"""Independent QC2 algebra support; no SymPy, author import, or result read.

Laurent coefficient algebra uses Fraction throughout. Analytic interval and
limit reasoning is in SOURCE_FIRST_REPORT.md; these checks do not replace it.
"""

from fractions import Fraction as F
import json
import platform


counts = {"coefficient_identities": 0, "exact_probes": 0, "negative_controls": 0}


def clean(p):
    return {n: F(a) for n, a in p.items() if a}


def add(p, q):
    return clean({n: p.get(n, F(0)) + q.get(n, F(0)) for n in p.keys() | q.keys()})


def scale(p, a):
    return clean({n: F(a) * c for n, c in p.items()})


def mul(p, q):
    out = {}
    for n, a in p.items():
        for m, b in q.items():
            out[n+m] = out.get(n+m, F(0)) + a*b
    return clean(out)


def deriv(p):
    return clean({n-1: n*a for n, a in p.items() if n})


def val(p, x):
    x = F(x)
    return sum((a*x**n for n, a in p.items()), F(0))


def linear_residual(p):
    return add(scale(mul({2: F(1)}, deriv(deriv(p))), F(1, 2)), scale(p, -1))


def angular(p):
    return add(linear_residual(p), {0: F(1)})


def check(actual, expected, label, kind="coefficient_identities"):
    assert actual == expected, (label, actual, expected)
    counts[kind] += 1


def demand(condition, label):
    assert condition, label
    counts["exact_probes"] += 1


def must_fail(callback, label):
    try:
        callback()
    except AssertionError:
        counts["negative_controls"] += 1
    else:
        raise AssertionError("negative control failed to reject: " + label)


h = {2: F(1, 3), -1: F(2, 3), 0: F(-1)}
one = {0: F(1)}
h1, h2 = deriv(h), deriv(deriv(h))
factorized_h = scale(mul(mul({1: F(1), 0: F(-1)}, {1: F(1), 0: F(-1)}),
                           {0: F(1), -1: F(2)}), F(1, 3))
check(h, factorized_h, "whole-positive-axis h factorization")
check(linear_residual(h), one, "constant forcing identity")
check(val(h, 1), F(0), "zero value anchor")
check(val(h1, 1), F(0), "zero derivative anchor")

radial = scale(h2, F(1, 2))
tangential = scale(mul(h1, {-1: F(1)}), F(1, 2))
sphere = mul(h, {-2: F(1)})
check(radial, {0: F(1, 3), -3: F(2, 3)}, "radial coefficient")
check(tangential, {0: F(1, 3), -3: F(-1, 3)}, "tangential coefficient")
check(sphere, {0: F(1, 3), -2: F(-1), -3: F(2, 3)}, "sphere coefficient")
check(deriv(radial), {-4: F(-2)}, "radial decreasing on positive axis")
check(deriv(tangential), {-4: F(1)}, "tangential increasing on positive axis")
check(deriv(sphere), mul({1: F(2), 0: F(-2)}, {-4: F(1)}),
      "sphere increasing for x>=1")
check(val(radial, 1), F(1), "radial maximum")
check(val(tangential, 1), F(0), "tangential minimum")
check(val(sphere, 1), F(0), "sphere minimum")

# Endpoint L=1/t: substitute each independent coefficient before taking t->0.
endpoint_increment = clean({2-n: a for n, a in h.items()})
endpoint_q = add(one, endpoint_increment)
check(endpoint_q, {0: F(4, 3), 2: F(-1), 3: F(2, 3)},
      "expanding endpoint polynomial in inverse extent")
demand(all(n >= 0 for n in endpoint_q), "endpoint polynomial has finite t->0 limit")
check(endpoint_q.get(0), F(4, 3), "expanding endpoint squared clock limit")

# Split shrinking-margin family affinely in delta, so endpoint cancellation
# is a coefficient identity, not extrapolation from finitely many deltas.
p_base = {0: F(1), 2: F(-1, 4)}
p_var = {2: F(1, 4)}
q_var = add(p_var, h)
check(angular(p_base), {}, "limiting reference balanced")
check(linear_residual(p_var), {}, "varying reference homogeneous")
check(val(p_base, 2), F(0), "zero base endpoint")
check(val(p_var, 2), F(1), "reference endpoint delta coefficient")
check(val(q_var, 2), F(5, 3), "perturbed endpoint delta coefficient")
check(val(q_var, 1), val(p_var, 1), "affine anchor value matching")
check(val(deriv(q_var), 1), val(deriv(p_var), 1), "affine anchor derivative matching")
check(add(p_base, p_var), one, "delta=1 reference endpoint of family")

domain_rows = []
for extent in [F(2), F(3), F(4), F(8), F(16), F(64)]:
    epsilon = extent**-2
    p, q = one, add(one, scale(h, epsilon))
    check(angular(q), {0: epsilon}, "expanding residual")
    check(val(q, 1), val(p, 1), "expanding value matching")
    check(val(deriv(q), 1), val(deriv(p), 1), "expanding derivative matching")
    for k in range(17):
        x = 1 + (extent-1)*F(k, 16)
        demand(val(q, x) >= 1, "positive common margin")
        demand(0 <= epsilon*val(radial, x) <= epsilon, "radial bound")
        demand(0 <= epsilon*val(tangential, x) <= epsilon/F(3), "tangential bound")
        demand(0 <= epsilon*val(sphere, x) <= epsilon/F(3), "sphere bound")
    ratio_squared = val(q, extent)/val(q, 1)
    check(ratio_squared, val(endpoint_q, 1/extent), "endpoint substitution", "exact_probes")
    domain_rows.append({"extent": str(extent), "epsilon": str(epsilon),
                        "relative_clock_squared": str(ratio_squared)})

margin_rows = []
for delta in [F(1), F(1, 2), F(1, 4), F(1, 16), F(1, 64), F(1, 1024)]:
    p = add(p_base, scale(p_var, delta))
    q = add(p, scale(h, delta))
    check(angular(p), {}, "shrinking reference balanced")
    check(angular(q), {0: delta}, "shrinking residual")
    check(val(q, 1), val(p, 1), "shrinking value matching")
    check(val(deriv(q), 1), val(deriv(p), 1), "shrinking derivative matching")
    for k in range(17):
        x = 1 + F(k, 16)
        demand(val(q, x) >= val(p, x) >= delta, "positive delta margin")
        demand(0 <= delta*val(radial, x) <= delta, "shrinking radial bound")
        demand(0 <= delta*val(tangential, x) <= delta/F(3), "shrinking tangential bound")
        demand(0 <= delta*val(sphere, x) <= delta/F(3), "shrinking sphere bound")
    relative_clock_squared = (val(q, 2)/val(q, 1))/(val(p, 2)/val(p, 1))
    check(relative_clock_squared, F(5, 3), "shrinking clock quotient", "exact_probes")
    margin_rows.append({"delta": str(delta), "relative_clock_squared": str(relative_clock_squared)})

# Each intentionally defective assertion must raise. Counts for ordinary
# identities/probes increase only after successful genuine checks.
must_fail(lambda: check(linear_residual(add(one, scale(h, F(1, 4)))),
                        {0: F(1, 4)}, "missing sphere constant"), "sphere omission")
bad_h = {2: F(1, 3), -1: F(1, 3), 0: F(-1)}
must_fail(lambda: check(val(bad_h, 1), F(0), "corrupted anchor"), "anchor coefficient")
bad_q = add(add(p_base, scale(p_var, F(1, 4))), scale(h, F(-1, 2)))
must_fail(lambda: demand(val(bad_q, 2) > 0, "negative endpoint rejected"), "lost positivity")
must_fail(lambda: check(F(5, 3), F(1), "relative clocks falsely exact"), "clock omission")
must_fail(lambda: check(scale(h2, F(1, 4)), radial, "wrong curvature normalization"),
          "curvature factor")

print(json.dumps({"python": platform.python_version(), "arithmetic": "stdlib Fraction",
                  "counts": counts, "expanding": domain_rows, "shrinking": margin_rows,
                  "status": "PASS; finite algebra support, analytic proof separately recorded"},
                 sort_keys=True, indent=2))

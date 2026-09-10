"""GL1 exact support, not a full-space classification or an adopted response.

Tests a contracted m=2 polynomial subcase using Ricci and Hessian-of-scalar
slots. All displayed coefficients are FREE diagnostic numbers, not UDT laws.
The generic Taylor/parity argument is analytical; finite checks cannot prove it.
"""

from fractions import Fraction as Q
import json
import platform
import random

sgn = [-1, 1, 1, 1]
eta = [[Q(sgn[i] if i == j else 0) for j in range(4)] for i in range(4)]
zero = [[Q(0) for _ in range(4)] for _ in range(4)]
counts = {"curvature_identities": 0, "weighted_identities": 0,
          "exact_bound_probes": 0, "covariance_checks": 0, "negative_controls": 0}


def add(a, b):
    return [[a[i][j]+b[i][j] for j in range(4)] for i in range(4)]


def scale(a, k):
    return [[k*v for v in row] for row in a]


def trace(a):
    return sum(sgn[i]*a[i][i] for i in range(4))


def tf(a):
    return add(a, scale(eta, -trace(a)/4))


def square(a):
    return [[sum(a[i][k]*sgn[k]*a[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def norm1(a):
    return sum(abs(v) for row in a for v in row)


def equal(a, b, kind):
    assert a == b, (kind, a, b)
    counts[kind] += 1


def demand(condition, label):
    assert condition, label
    counts["exact_bound_probes"] += 1


def reject(callback):
    try:
        callback()
    except AssertionError:
        counts["negative_controls"] += 1
    else:
        raise AssertionError("corrupted claim was not rejected")


def curvature_from_ricci(ric):
    # Kulkarni decomposition, all lower indices; contraction in slots0,2.
    schouten = scale(add(ric, scale(eta, -trace(ric)/6)), Q(1, 2))
    return [[[[eta[a][c]*schouten[b][d]-eta[a][d]*schouten[b][c]
               -eta[b][c]*schouten[a][d]+eta[b][d]*schouten[a][c]
               for d in range(4)] for c in range(4)] for b in range(4)] for a in range(4)]


def ricci(k):
    return [[sum(sgn[a]*k[a][b][a][d] for a in range(4)) for d in range(4)] for b in range(4)]


def model(r, h, a=Q(2), b=Q(-3), c=Q(5), d=Q(-2)):
    # Fixed trace-only constant is deliberately retained before projection.
    full = add(scale(eta, Q(7)), add(scale(r, a), add(scale(h, b),
           add(scale(square(r), c), scale(r, d*trace(r))))))
    return tf(full)


def transform(a, lam):
    return [[sum(lam[k][i]*a[k][l]*lam[l][j] for k in range(4) for l in range(4))
             for j in range(4)] for i in range(4)]


rng = random.Random(1092026)
samples = []
for _ in range(12):
    r = [[Q(rng.randint(-4, 4), rng.randint(1, 5)) for _ in range(4)] for _ in range(4)]
    h = [[Q(rng.randint(-3, 3), rng.randint(1, 4)) for _ in range(4)] for _ in range(4)]
    r = [[(r[i][j]+r[j][i])/2 for j in range(4)] for i in range(4)]
    h = [[(h[i][j]+h[j][i])/2 for j in range(4)] for i in range(4)]
    samples.append((r, h))

boost = [[Q(5, 3), Q(4, 3), Q(0), Q(0)],
         [Q(4, 3), Q(5, 3), Q(0), Q(0)],
         [Q(0), Q(0), Q(1), Q(0)], [Q(0), Q(0), Q(0), Q(1)]]
equal(transform(eta, boost), eta, "covariance_checks")
equal(model(zero, zero), zero, "weighted_identities")

epsilons = [Q(1, 2), Q(1, 3), Q(1, 10), Q(1, 100)]
for r, h in samples:
    k = curvature_from_ricci(r)
    equal(ricci(k), r, "curvature_identities")
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    equal(k[a][b][c][d], -k[b][a][c][d], "curvature_identities")
                    equal(k[a][b][c][d]+k[a][c][d][b]+k[a][d][b][c], Q(0), "curvature_identities")
    equal(trace(tf(r)), Q(0), "curvature_identities")
    equal(model(transform(r, boost), transform(h, boost)),
          transform(model(r, h), boost), "covariance_checks")
    coeff4 = add(scale(tf(h), Q(-3)), add(scale(tf(square(r)), Q(5)),
                 scale(tf(r), Q(-2)*trace(r))))
    bound4 = 6*norm1(h)+14*norm1(r)**2
    for e in epsilons:
        actual = model(scale(r, e**2), scale(h, e**4))
        leading = scale(tf(r), 2*e**2)
        remainder = add(actual, scale(leading, -1))
        equal(remainder, scale(coeff4, e**4), "weighted_identities")
        demand(norm1(remainder) <= bound4*e**4, "explicit contracted norm1 bound")
        equal(scale(remainder, e**-2), scale(coeff4, e**2), "weighted_identities")

# Known degenerate stratum, reused control, not a new result or actual metric.
r0 = [[Q(-1 if i == 0 else (1 if i == 1 else -1)) if i == j else Q(0)
       for j in range(4)] for i in range(4)]
equal(tf(square(r0)), zero, "weighted_identities")
demand(norm1(tf(r0)) > 0, "a=0 quadratic balance does not force S=0")

# Named corruptions only. These are not full-operator mutation coverage.
reject(lambda: equal(tf(square(r0)), tf(r0), "weighted_identities"))
e = Q(1, 10)
r, h = samples[0]
good = add(model(scale(r, e**2), scale(h, e**4)), scale(tf(r), -2*e**2))
reject(lambda: equal(good, zero, "weighted_identities"))
bad_hierarchy = add(model(zero, scale(r0, e**2)), scale(model(zero, r0), -e**4))
reject(lambda: equal(bad_hierarchy, zero, "weighted_identities"))

# Odd input under -I changes sign, while the even rank-two output must not.
# A proposed nonzero linear extraction is explicitly shown to fail that test.
odd_input = Q(3, 7)
reject(lambda: equal(scale(tf(r0), -odd_input), scale(tf(r0), odd_input), "covariance_checks"))

print(json.dumps({"status": "PASS; finite support, not generic proof",
                  "python": platform.python_version(), "arithmetic": "Fraction exact",
                  "counts": counts, "matrix_pairs": len(samples),
                  "epsilon_values": [str(e) for e in epsilons],
                  "scope": "contracted m=2 diagnostics; no physical coefficient adopted",
                  "omissions": "full G301 basis census, arbitrary actual jet realization, PDE, empirical data"},
                 indent=2, sort_keys=True))

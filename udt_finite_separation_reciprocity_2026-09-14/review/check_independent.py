"""FSR1 exact matrix checks; no parent scientific imports or physical admission."""
from fractions import Fraction as Q
from pathlib import Path
import datetime
import hashlib
import json
import platform
import sys


def eye(n):
    return [[Q(int(i == j)) for j in range(n)] for i in range(n)]


def tr(a):
    return list(map(list, zip(*a)))


def mm(a, b):
    return [[sum((x * y for x, y in zip(row, col)), Q(0))
             for col in zip(*b)] for row in a]


def inverse(a):
    n = len(a)
    aug = [row[:] + ident for row, ident in zip(a, eye(n))]
    for j in range(n):
        pivot = next(i for i in range(j, n) if aug[i][j])
        aug[j], aug[pivot] = aug[pivot], aug[j]
        scale = aug[j][j]
        aug[j] = [x / scale for x in aug[j]]
        for i in range(n):
            if i != j:
                scale = aug[i][j]
                aug[i] = [x - scale * y for x, y in zip(aug[i], aug[j])]
    assert [row[:n] for row in aug] == eye(n)
    return [row[n:] for row in aug]


def project(a):
    assert a[0][0] > 0
    return [a[i][0] / a[0][0] for i in range(1, 4)]


def mv(a, v):
    return [sum((x * y for x, y in zip(row, v)), Q(0)) for row in a]


def axis_boost(axis, c, s):
    assert c > 0 and c*c-s*s == 1
    a = eye(4)
    a[0][0] = a[axis][axis] = c
    a[0][axis] = a[axis][0] = s
    return a


def rotation(i, j, c, s):
    assert c*c+s*s == 1
    a = eye(4)
    a[i][i] = a[j][j] = c
    a[i][j], a[j][i] = -s, s
    return a


def norm2(v):
    return sum((x*x for x in v), Q(0))


eta = eye(4)
eta[0][0] = Q(-1)
bx = axis_boost(1, Q(5, 4), Q(3, 4))
by = axis_boost(2, Q(13, 12), Q(5, 12))
bz = axis_boost(3, Q(17, 15), Q(-8, 15))
rxy = rotation(1, 2, Q(0), Q(1))
ryz = rotation(2, 3, Q(5, 13), Q(12, 13))
rxz = rotation(1, 3, Q(3, 5), Q(-4, 5))

# Construct arrows as elementary products, then RECOVER their canonical carry.
# Parent instead constructs a canonical boost from a half-boost vector and supplies R.
words = [
    ("identity", []), ("zero_vector_rotated", [rxy, ryz]),
    ("radial", [bx]), ("radial_with_rotated_axes", [bx, rxy]),
    ("noncollinear_xy", [by, bx]),
    ("all_axes_boosted", [bz, by, bx]),
    ("all_axes_and_rotations", [ryz, bx, rxz, bz, by]),
    ("reversed_product", [inverse(by), inverse(bz), inverse(rxz), inverse(bx), inverse(ryz)]),
]
records, arrows = [], []
for label, factors in words:
    a = eye(4)
    for factor in factors:
        a = mm(a, factor)
    ai = inverse(a)  # generic elimination, not the Lorentz transpose shortcut
    assert mm(tr(a), mm(eta, a)) == eta
    assert mm(ai, a) == eye(4) == mm(a, ai)
    assert ai == mm(eta, mm(tr(a), eta))
    gamma, c = a[0][0], [a[i][0] for i in range(1, 4)]
    v, vi = project(a), project(ai)
    assert gamma > 0 and gamma*gamma-norm2(c) == 1
    assert norm2(v) < 1 and ai[0][0] == gamma

    # Reconstruct the symmetric canonical boost from the clock column.
    # gamma+1 remains positive at v=0; there is no division by |v|.
    b = eye(4)
    b[0][0] = gamma
    for i in range(3):
        b[0][i+1] = b[i+1][0] = c[i]
        for j in range(3):
            b[i+1][j+1] += c[i]*c[j]/(gamma+1)
    rr = mm(inverse(b), a)
    assert rr[0] == [Q(1), Q(0), Q(0), Q(0)]
    assert [row[0] for row in rr] == [Q(1), Q(0), Q(0), Q(0)]
    r = [row[1:] for row in rr[1:]]
    assert mm(tr(r), r) == eye(3)
    assert mm(b, rr) == a
    assert vi == [-x for x in mv(inverse(r), v)]
    # Independently read reverse vector from the original matrix's first ROW.
    assert vi == [-a[0][i]/gamma for i in range(1, 4)]
    assert norm2(vi) == norm2(v)
    omission = [x+y for x, y in zip(vi, v)]
    records.append({"label": label, "forward": v, "reverse": vi,
                    "gamma": gamma, "omit_carry_defect": omission})
    arrows.append(a)

assert records[0]["forward"] == records[1]["forward"] == [Q(0)]*3
assert records[2]["reverse"] == [Q(-3, 5), Q(0), Q(0)]
assert records[3]["forward"] == [Q(3, 5), Q(0), Q(0)]
assert records[3]["reverse"] == [Q(0), Q(3, 5), Q(0)]
assert all(x != 0 for x in records[6]["forward"])
assert any(records[3]["omit_carry_defect"])
assert any(records[6]["omit_carry_defect"])

# All 64 selected ordered products: the general proof remains matrix algebra.
wrong_order_detected = 0
for a in arrows:
    for b in arrows:
        correct = inverse(mm(b, a))
        assert correct == mm(inverse(a), inverse(b))
        if correct != mm(inverse(b), inverse(a)):
            wrong_order_detected += 1
assert wrong_order_detected > 0

# Exact rational finite squeezes: K preservation and eta non-preservation.
# DDR tangent is also reconstructed algebraically from exp(+/-2d)' at d=0.
k = [[Q(0), Q(1)], [Q(1), Q(0)]]
eta2 = [[Q(-1), Q(0)], [Q(0), Q(1)]]
squeeze_records = []
for scale in [Q(1), Q(2), Q(2, 3), Q(7, 4)]:
    d = [[1/scale, Q(0)], [Q(0), scale]]
    assert mm(tr(d), mm(k, d)) == k
    actual = mm(tr(d), mm(eta2, d))
    assert actual == [[-1/(scale*scale), Q(0)], [Q(0), scale*scale]]
    assert (actual == eta2) == (scale == 1)
    squeeze_records.append({"scale": scale, "transformed_eta": actual})
generator = [[Q(-1), Q(0)], [Q(0), Q(1)]]
left, right = mm(tr(generator), eta2), mm(eta2, generator)
tangent = [[left[i][j]+right[i][j] for j in range(2)] for i in range(2)]
assert tangent == [[Q(2), Q(0)], [Q(0), Q(2)]]

result = {
    "status": "PASS_INDEPENDENT_EXACT_FINITE_ALGEBRA_ONLY",
    "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "python": sys.version, "platform": platform.platform(),
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "method": "standard-library Fraction matrices; generic Gaussian inversion; elementary-arrow products and recovered canonical carry",
    "parent_code_exposure": "read before implementation; no parent scientific imports or SymPy use",
    "arrow_cases": records, "ordered_products_checked": 64,
    "wrong_inverse_order_rejected_cases": wrong_order_detected,
    "squeeze_cases": squeeze_records, "DDR_tangent": tangent,
    "hostile_controls": {"drop_carry": "REJECTED", "wrong_inverse_order": "REJECTED",
                         "pretend_squeeze_preserves_eta": "REJECTED"},
    "scope": "exact selected algebraic diagnostics, supplementing the analytic general argument; no geometry, physical admission or response-law selection",
}
print(json.dumps(result, default=str, indent=2))

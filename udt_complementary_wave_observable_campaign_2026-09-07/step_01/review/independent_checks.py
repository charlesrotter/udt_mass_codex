"""Finite exact-rational CO1 anchors; no candidate imports or detector/event data."""
from fractions import Fraction as Q
import json
import platform


def transpose(a):
    return list(map(list, zip(*a)))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def multiply(a, b):
    return [[dot(row, col) for col in transpose(b)] for row in a]


def rank(a):
    m = [[Q(v) for v in row] for row in a]
    r = 0
    for c in range(len(m[0])):
        p = next((i for i in range(r, len(m)) if m[i][c]), None)
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        div = m[r][c]
        m[r] = [v / div for v in m[r]]
        for i in range(len(m)):
            if i != r:
                fac = m[i][c]
                m[i] = [x - fac * y for x, y in zip(m[i], m[r])]
        r += 1
        if r == len(m):
            break
    return r


def cross(a, b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2],
            a[0]*b[1]-a[1]*b[0]]


def inverse2(a):
    det = a[0][0]*a[1][1]-a[0][1]*a[1][0]
    assert det
    return [[a[1][1]/det, -a[0][1]/det],
            [-a[1][0]/det, a[0][0]/det]]


eplus = [[Q(1), Q(0), Q(0)], [Q(0), Q(-1), Q(0)], [Q(0)]*3]
ecross = [[Q(0), Q(1), Q(0)], [Q(1), Q(0), Q(0)], [Q(0)]*3]
second = [[Q(0)]*4 for _ in range(4)]
for i in range(3):
    for j in range(3):
        second[i+1][j+1] = 6*eplus[i][j]-4*ecross[i][j]
k = [Q(1), Q(0), Q(0), Q(-1)]  # units c_E=1 only in this algebraic check


def d2(a, b, c, d):
    return second[a][b]*k[c]*k[d]


def riemann(a, b, c, d):
    return (d2(a, d, b, c)+d2(b, c, a, d)
            -d2(a, c, b, d)-d2(b, d, a, c))/2


eta = [-1, 1, 1, 1]
ricci = [[sum(eta[a]*riemann(a,b,a,d) for a in range(4))
          for d in range(4)] for b in range(4)]
assert all(v == 0 for row in ricci for v in row)
electric = [[riemann(0,i+1,0,j+1) for j in range(3)] for i in range(3)]
assert electric == [[Q(-3), Q(2), Q(0)], [Q(2), Q(3), Q(0)], [Q(0)]*3]
assert sum(electric[i][i] for i in range(3)) == 0
assert all(electric[2][j] == 0 for j in range(3))


def detector_row(a, b):
    assert dot(a, a) == dot(b, b) == 1 and dot(a, b) == 0
    d = [[(a[i]*a[j]-b[i]*b[j])/2 for j in range(3)] for i in range(3)]
    row = [sum(d[i][j]*e[i][j] for i in range(3) for j in range(3))
           for e in [eplus, ecross]]
    tide = sum(d[i][j]*electric[i][j] for i in range(3) for j in range(3))
    assert tide == -dot(row, [Q(6), Q(-4)])/2
    return row


F = [detector_row([Q(1),Q(0),Q(0)], [Q(0),Q(1),Q(0)]),
     detector_row([Q(3,5),Q(4,5),Q(0)], [Q(-4,5),Q(3,5),Q(0)]),
     detector_row([Q(5,13),Q(12,13),Q(0)], [Q(-12,13),Q(5,13),Q(0)])]
assert rank(F) == 2
null = cross(*transpose(F))
assert any(null) and all(dot(null, c) == 0 for c in transpose(F))
for hp in [Q(-7,3),Q(0),Q(11,2)]:
    for hc in [Q(-5,7),Q(0),Q(2,9)]:
        signal = [dot(row, [hp,hc]) for row in F]
        assert dot(null, signal) == 0
        recovered = [dot(row, signal[:2]) for row in inverse2(F[:2])]
        assert recovered == [hp,hc]
        assert dot(F[2], recovered) == signal[2]

# Rank1 training predicts a colinear holdout but not its missing polarization.
rank1 = [[Q(1),Q(0)], [Q(2),Q(0)]]
colinear = [Q(3),Q(0)]
missing = [Q(0),Q(1)]
assert rank(rank1) == rank(rank1+[colinear]) == 1
assert rank(rank1+[missing]) == 2
assert dot(colinear, [Q(0),Q(1)]) == 0
assert dot(missing, [Q(0),Q(1)]) == 1

# A physically realizable near-aligned, exactly rank2 pair has a large inverse.
q = Q(1, 1000000)
a = [(1-q*q)/(1+q*q), 2*q/(1+q*q), Q(0)]
b = [-a[1], a[0], Q(0)]
near = [F[0], detector_row(a,b)]
assert rank(near) == 2
inverse = inverse2(near)
noise = [Q(0),Q(1,1000)]
spurious_h = [dot(row,noise) for row in inverse]
assert abs(spurious_h[1]) > 249

# Nonzero alternatives lying in the tensor signal plane evade every tensor null.
invisible = [dot(row,[Q(7),Q(-3)]) for row in F]
assert any(invisible) and dot(null,invisible) == 0
visible = [Q(0),Q(0),Q(1)]
assert dot(null,visible) != 0
# Arbitrary channel functions saturate the data space and destroy restrictions.
with_nuisance = [F[i]+[Q(int(i==j)) for j in range(3)] for i in range(3)]
assert rank(with_nuisance) == 3

checks = {
    "direct_linearized_riemann_ricci_zero": True,
    "electric_tide_sign_and_factor": True,
    "physical_unit_arm_detector_projection": True,
    "three_channel_rank_two_null_dimension_one": True,
    "nine_exact_waveform_recovery_cases": True,
    "rank_one_predictable_and_unpredictable_holdout_separator": True,
    "near_aligned_full_rank_noise_amplification": True,
    "nonzero_alternative_invisible_to_null_separator": True,
    "channel_specific_nuisance_saturation": True,
}
print(json.dumps({
    "python": platform.python_version(),
    "evidence_kind": "finite exact-rational independent anchors, not observational data",
    "candidate_imports": False,
    "checks": checks,
    "electric_tide": [[str(x) for x in row] for row in electric],
    "detector_rows": [[str(x) for x in row] for row in F],
    "null_vector": [str(x) for x in null],
    "near_aligned_spurious_cross_from_0.001_channel_error": float(spurious_h[1]),
    "near_aligned_inverse_cross_coefficient": str(inverse[1][1]),
}, indent=2, sort_keys=True))

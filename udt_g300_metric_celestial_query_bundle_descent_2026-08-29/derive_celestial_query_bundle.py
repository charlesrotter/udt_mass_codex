#!/usr/bin/env python3
"""Exact stdlib checks for the preregistered G300 celestial control fiber."""

from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
ZERO = F(0)
ONE = F(1)
ETA = (-ONE, ONE, ONE, ONE)
LANDING = (
    "NO_PROPER_LAWFUL_RANK_TWO_QUERY_FAMILY_IS_DERIVED__THE_QUERY_DOMAIN_REMAINS_"
    "WHOLLY_OPERATIONAL"
)


def q(value):
    return value if isinstance(value, F) else F(value)


def dot(x, y):
    return sum(ETA[i] * x[i] * y[i] for i in range(4))


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4)) for i in range(4))


def mv(a, x):
    return tuple(sum(a[i][j] * x[j] for j in range(4)) for i in range(4))


def tr(a):
    return tuple(tuple(a[j][i] for j in range(4)) for i in range(4))


def identity():
    return tuple(tuple(ONE if i == j else ZERO for j in range(4)) for i in range(4))


def lorentz_inverse(a):
    at = tr(a)
    return tuple(tuple(ETA[i] * at[i][j] * ETA[j] for j in range(4)) for i in range(4))


def spatial_rotation(quat):
    a, b, c, d = map(q, quat)
    n = a * a + b * b + c * c + d * d
    r = (
        ((a*a+b*b-c*c-d*d)/n, 2*(b*c-a*d)/n, 2*(b*d+a*c)/n),
        (2*(b*c+a*d)/n, (a*a-b*b+c*c-d*d)/n, 2*(c*d-a*b)/n),
        (2*(b*d-a*c)/n, 2*(c*d+a*b)/n, (a*a-b*b-c*c+d*d)/n),
    )
    return (
        (ONE, ZERO, ZERO, ZERO),
        (ZERO, *r[0]),
        (ZERO, *r[1]),
        (ZERO, *r[2]),
    )


def boost(stereo):
    p = tuple(map(q, stereo))
    norm2 = sum(x*x for x in p)
    if norm2 >= ONE:
        raise ValueError("hyperbolic stereographic point must lie inside the unit ball")
    den = ONE - norm2
    gamma = (ONE + norm2) / den
    s = tuple(2*x/den for x in p)
    rows = [[ZERO for _ in range(4)] for _ in range(4)]
    rows[0][0] = gamma
    for i in range(3):
        rows[0][i+1] = s[i]
        rows[i+1][0] = s[i]
        for j in range(3):
            rows[i+1][j+1] = (ONE if i == j else ZERO) + s[i]*s[j]/(gamma+ONE)
    return tuple(tuple(row) for row in rows)


def sky(stereo):
    a, b = map(q, stereo)
    den = ONE + a*a + b*b
    return (ZERO, 2*a/den, 2*b/den, (ONE-a*a-b*b)/den)


def relation(boost_point, quaternion):
    return mm(boost(boost_point), spatial_rotation(quaternion))


def is_lorentz(a):
    for i in range(4):
        for j in range(4):
            value = sum(ETA[k]*a[k][i]*a[k][j] for k in range(4))
            if value != (ETA[i] if i == j else ZERO):
                return False
    return True


def aberration(a, n):
    k = (ONE, n[1], n[2], n[3])
    y = mv(a, k)
    omega = y[0]
    if omega <= ZERO:
        raise AssertionError("future-null direction lost positive frequency")
    ny = (ZERO, y[1]/omega, y[2]/omega, y[3]/omega)
    return ny, ONE/omega, omega


def source_checks():
    expected = {
        "founding.md": "physical normalized pair position is the metric's complete projective relation state",
        "udt_g176_completed_pair_dual_reciprocity_consolidation_2026-08-19/ADOPTION_RECORD.md":
            "Dual Reciprocity applies to the completed physical observer-pair pullback",
        "udt_g179_complete_coframe_pair_pullback_extension_2026-08-19/EXACT_DERIVATION.md":
            "The metric and germ are supplied.",
        "udt_g220_covariant_null_clock_arrow_timelive_lift_2026-08-22/EXACT_DERIVATION.md":
            "This is a covariant dynamic formula on the declared null query.",
        "udt_g244_metric_native_observer_sky_response_query_2026-08-24/EXACT_DERIVATION.md":
            "The history, observation sheet, endpoint incidence, and branch are supplied.",
        "udt_g274_projective_pair_position_network_descent_2026-08-26/EXACT_DERIVATION.md":
            "Full completed arrows live in the Lorentz frame groupoid",
        "udt_g298_causal_diamond_to_pair_germ_transfer_2026-08-29/EXACT_DERIVATION.md":
            "complete path-labelled relation state",
        "udt_g299_complete_relation_kernel_domain_ownership_2026-08-29/EXACT_DERIVATION.md":
            "active premises do not yet define that lawful query family or subfunctor.",
        "udt_g299_complete_relation_kernel_domain_ownership_2026-08-29/AUDIT_REPORT.md":
            "G299 is externally closed at its bounded working-premise grade.",
    }
    manifest = {}
    for line in (PACKAGE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        digest, path = line.split("\t")
        manifest[path] = digest
    assert set(manifest) == set(expected)
    for path, phrase in expected.items():
        data = (ROOT / path).read_bytes()
        assert hashlib.sha256(data).hexdigest() == manifest[path]
        assert phrase in data.decode("utf-8")
    return len(manifest), len(expected)


def main():
    hashes, phrases = source_checks()
    assertions = 0
    cases = 0

    boost_points = (
        (F(0), F(0), F(0)),
        (F(1,5), F(0), F(0)),
        (F(1,6), F(1,7), F(0)),
        (F(-1,8), F(1,9), F(1,10)),
        (F(2,11), F(-1,12), F(1,13)),
    )
    quaternions = ((1,0,0,0), (1,1,0,0), (2,1,1,0), (3,-1,2,1))
    directions = tuple(
        sky((F(a, 7), F(b, 8)))
        for a, b in (
            (-3,-2), (-3,1), (-2,3), (-1,-3), (-1,0), (-1,2),
            (0,-2), (0,-1), (0,0), (0,1), (0,3), (1,-3),
            (1,-1), (1,2), (2,-2), (2,0), (2,3), (3,-1),
            (3,1), (4,-2), (4,3),
        )
    )
    relations = tuple(relation(p, rot) for p in boost_points for rot in quaternions)

    for p in relations:
        assert is_lorentz(p); assertions += 1
        pinv = lorentz_inverse(p)
        assert mm(pinv, p) == identity(); assertions += 1
        for n in directions:
            cases += 1
            assert n[0] == ZERO and dot(n,n) == ONE; assertions += 2
            ny, r, omega = aberration(p, n)
            assert omega > ZERO and r > ZERO; assertions += 2
            assert ny[0] == ZERO and dot(ny,ny) == ONE; assertions += 2
            back, rinv, oinv = aberration(pinv, ny)
            assert back == n; assertions += 1
            assert rinv == ONE/r and oinv == ONE/omega; assertions += 2
            clock = (r, ZERO, ZERO, ZERO)
            assert dot(clock,clock) == -r*r; assertions += 1
            assert dot(clock,ny) == ZERO and dot(ny,ny) == ONE; assertions += 2
            lam = F(7,5)
            yscaled = mv(p, tuple(lam*x for x in (ONE,n[1],n[2],n[3])))
            assert lam/yscaled[0] == r; assertions += 1
            assert tuple(yscaled[i]/yscaled[0] for i in range(1,4)) == ny[1:]; assertions += 1

    for p1 in relations:
        for p2 in relations:
            p21 = mm(p2,p1)
            assert is_lorentz(p21); assertions += 1
            for n in directions:
                cases += 1
                n1, r1, _ = aberration(p1,n)
                n2, r2, _ = aberration(p2,n1)
                nd, rd, _ = aberration(p21,n)
                assert n2 == nd; assertions += 1
                assert rd == r1*r2; assertions += 1

    rotations = tuple(spatial_rotation(rot) for rot in quaternions)
    for p in relations:
        for rx in rotations:
            for ry in rotations:
                transformed = mm(mm(ry,p), lorentz_inverse(rx))
                assert is_lorentz(transformed); assertions += 1
                for n in directions[:5]:
                    cases += 1
                    n_original, r_original, _ = aberration(p,n)
                    n_changed, r_changed, _ = aberration(transformed,mv(rx,n))
                    assert n_changed == mv(ry,n_original); assertions += 1
                    assert r_changed == r_original; assertions += 1

    # Every clock-containing plane representative alpha*U+beta*n reduces to its sky direction.
    u0 = (ONE,ZERO,ZERO,ZERO)
    for n in directions:
        for alpha, beta in ((F(-3,2),F(2,3)), (F(0),F(5,4)), (F(7,5),F(-3,7))):
            cases += 1
            v = tuple(alpha*u0[i] + beta*n[i] for i in range(4))
            spatial = tuple(v[i] + dot(v,u0)*u0[i] for i in range(4))
            assert spatial == tuple(beta*n[i] for i in range(4)); assertions += 1
            assert dot(spatial,u0) == ZERO and dot(spatial,spatial) == beta*beta; assertions += 2

    # G298 active-screen planes both occur in the full clock-containing plane bundle.
    for rr in (F(1,3), F(2,3), F(1), F(3,2), F(5,2)):
        for w in (F(-3,2), F(-1,2), F(1,4), F(4,3)):
            cases += 1
            gamma = (ONE+rr*rr+rr*rr*w*w)/(2*rr)
            a = (-ONE+rr*rr+rr*rr*w*w)/(2*rr)
            uy = (gamma,a,w,ZERO)
            e1 = (ZERO,ONE,ZERO,ZERO)
            ny = (rr-gamma,rr-a,-w,ZERO)
            st = tuple(e1[i] + a*uy[i] for i in range(4))
            assert dot(uy,uy) == -ONE; assertions += 1
            assert dot(uy,ny) == ZERO and dot(ny,ny) == ONE; assertions += 2
            assert dot(uy,st) == ZERO and dot(st,st) == ONE+a*a; assertions += 2
            # e1 = st-a*uy: orthogonalization preserves the transported-source plane.
            assert e1 == tuple(st[i]-a*uy[i] for i in range(4)); assertions += 1
            assert -rr*rr*w != ZERO; assertions += 1

    # The identity relation admits no gauge-natural unit direction fixed by spatial isotropy.
    rx_pi = ((ONE,ZERO,ZERO),(ZERO,-ONE,ZERO),(ZERO,ZERO,-ONE))
    ry_pi = ((-ONE,ZERO,ZERO),(ZERO,ONE,ZERO),(ZERO,ZERO,-ONE))
    fixed_rx = lambda v: (v[0],-v[1],-v[2]) == v
    fixed_ry = lambda v: (-v[0],v[1],-v[2]) == v
    for n in directions:
        cases += 1
        spatial = n[1:]
        assert not (fixed_rx(spatial) and fixed_ry(spatial)); assertions += 1
    assertions += 2
    assert rx_pi != ry_pi
    assert all(dot(n,n) == ONE for n in directions)

    result = {
        "status": "PASS",
        "landing": LANDING,
        "source_hashes": hashes,
        "source_phrase_checks": phrases,
        "relations": len(relations),
        "directions": len(directions),
        "cases": cases,
        "assertions": assertions,
        "query_fiber_oriented": "S^2",
        "query_fiber_unoriented": "RP^2",
        "celestial_family_type": "ALGEBRAICALLY_AVAILABLE_SUPPLIED_DIRECTION_CONTROL_FIBER",
        "lawful_query_family_ownership": "NOT_DERIVED",
        "composition_owner": "full path-labelled metric isometry",
        "individual_query": "SUPPLIED",
        "route_population": "OPEN",
        "engine": "stdlib Fraction exact arithmetic",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

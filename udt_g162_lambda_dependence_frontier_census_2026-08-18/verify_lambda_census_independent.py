#!/usr/bin/env python3
"""Independent stdlib Fraction/dual-number replay for G162."""

from __future__ import annotations

import csv
import hashlib
import json
import random
import subprocess
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
SOURCE_SNAPSHOT = "ee261b38"
OUTCOME_CLASS = (
    "SECOND_REPAIR_SCALAR_KERNEL_DESCENDS_TO_QUOTIENT__CANONICAL_ENDPOINT_CARRY_EXACT__"
    "JOINED_ROUTE_FRAME_CHANNEL_RETAINS_LAMBDA__HISTORY_GAP_UNCHANGED"
)
LANDING = (
    "BOUNDED_SCALAR_RECIPROCAL_KERNEL_IS_RESIDUAL_LORENTZ_INVARIANT__"
    "UNIQUE_POSITIVE_ENDPOINT_ROOTS_GIVE_EXACT_FLAT_CALIBRATION_CARRY__"
    "GENERAL_COMPATIBLE_CARRY_FACTORS_AS_RB_INVERSE_LAMBDA_RA__JOINED_C_"
    "AND_GAMMA_RETAIN_SUPPLIED_ROUTE_FRAME_RAPIDITY__NORMAL_HOLONOMY_"
    "JACOBI_AND_EXTRINSIC_CHANNELS_REMAIN_SEPARATELY_TYPED__RAPIDITY_"
    "SELECTION_RETIRED_AS_SCALAR_KERNEL_GATE_ONLY__PHYSICAL_HISTORY_QUERY_"
    "PATH_CARRY_XMAX_AND_COMPLETION_OPEN"
)


class Dual:
    def __init__(self, value=0, derivative=0):
        self.value, self.derivative = F(value), F(derivative)

    def __add__(self, other):
        other = other if isinstance(other, Dual) else Dual(other)
        return Dual(self.value + other.value, self.derivative + other.derivative)

    __radd__ = __add__

    def __neg__(self):
        return Dual(-self.value, -self.derivative)

    def __sub__(self, other):
        return self + (-other if isinstance(other, Dual) else -Dual(other))

    def __rsub__(self, other):
        return Dual(other) - self

    def __mul__(self, other):
        other = other if isinstance(other, Dual) else Dual(other)
        return Dual(self.value * other.value,
                    self.derivative * other.value + self.value * other.derivative)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = other if isinstance(other, Dual) else Dual(other)
        return Dual(self.value / other.value,
                    (self.derivative * other.value - self.value * other.derivative)
                    / other.value**2)

    def __rtruediv__(self, other):
        return Dual(other) / self

    def __eq__(self, other):
        other = other if isinstance(other, Dual) else Dual(other)
        return self.value == other.value and self.derivative == other.derivative


def tr(a):
    return [list(row) for row in zip(*a)]


def mm(a, b):
    zero = Dual() if isinstance(a[0][0], Dual) or isinstance(b[0][0], Dual) else F(0)
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), zero)
             for j in range(len(b[0]))] for i in range(len(a))]


def madd(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def msub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def mscale(c, a):
    return [[c * entry for entry in row] for row in a]


def inv2(a):
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    return [[a[1][1] / det, -a[0][1] / det], [-a[1][0] / det, a[0][0] / det]]


def root(t, ell, beta):
    return [[t, t * beta], [F(0) if not isinstance(t, Dual) else Dual(), ell]]


def boost(z):
    assert F(-1) < z < F(1)
    den = 1 - z * z
    c, s = (1 + z * z) / den, 2 * z / den
    return [[c, s], [s, c]]


def det2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def sqrt_fraction(value):
    from math import isqrt
    assert value >= 0
    n, d = isqrt(value.numerator), isqrt(value.denominator)
    assert n * n == value.numerator and d * d == value.denominator
    return F(n, d)


def root_from_metric(h):
    t = sqrt_fraction(-h[0][0])
    beta = h[0][1] / h[0][0]
    ell = sqrt_fraction(h[1][1] - h[0][1] * h[0][1] / h[0][0])
    return root(t, ell, beta)


def values(a):
    return [[item.value for item in row] for row in a]


def derivatives(a):
    return [[item.derivative for item in row] for row in a]


def verify_manifest():
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(rows) == 13
    for row in rows:
        payload = subprocess.run(
            ["git", "show", f"{SOURCE_SNAPSHOT}:{row['path']}"], cwd=ROOT,
            check=True, stdout=subprocess.PIPE,
        ).stdout
        assert len(payload) == int(row["bytes"])
        assert hashlib.sha256(payload).hexdigest() == row["sha256"]
    return len(rows)


def main():
    source_count = verify_manifest()
    rng = random.Random(162)
    eta = [[F(-1), F(0)], [F(0), F(1)]]
    trials = 900

    for _ in range(trials):
        ta, la, tb, lb = [F(rng.randint(1, 9)) for _ in range(4)]
        ba, bb = F(rng.randint(-8, 8), 5), F(rng.randint(-8, 8), 5)
        z = F(rng.randint(-7, 7), 10)
        ra, rb, lam = root(ta, la, ba), root(tb, lb, bb), boost(z)
        ha, hb = mm(mm(tr(ra), eta), ra), mm(mm(tr(rb), eta), rb)
        m = mm(mm(inv2(rb), lam), ra)
        carried = mm(mm(tr(m), hb), m)
        assert carried == ha
        assert mm(mm(tr(lam), eta), lam) == eta
        assert det2(lam) == 1
        assert mm(mm(rb, m), inv2(ra)) == lam

        # Reverse direction, recomputing the endpoint root only from the compatible metric.
        reverse_root = root_from_metric(carried)
        reverse_lam = mm(mm(rb, m), inv2(reverse_root))
        assert mm(mm(tr(reverse_lam), eta), reverse_lam) == eta
        assert mm(mm(inv2(rb), reverse_lam), reverse_root) == m

        kval = [[F(rng.randint(-6, 6), 5), F(rng.randint(-6, 6), 5)],
                [F(rng.randint(-6, 6), 5), F(rng.randint(-6, 6), 5)]]
        kdag = mm(mm(inv2(ha), tr(kval)), ha)
        sh, ah = mscale(F(1, 2), madd(kval, kdag)), mscale(F(1, 2), msub(kval, kdag))
        assert msub(madd(mm(tr(kval), ha), mm(ha, kval)), mscale(F(2), mm(ha, sh))) == [[F(0), F(0)], [F(0), F(0)]]
        assert madd(mm(tr(ah), ha), mm(ha, ah)) == [[F(0), F(0)], [F(0), F(0)]]

        mcal = mm(inv2(rb), ra)
        assert mm(mm(tr(mcal), hb), mcal) == ha
        assert mm(mm(rb, mcal), inv2(ra)) == [[F(1), F(0)], [F(0), F(1)]]
        assert det2(m) == det2(ra) / det2(rb) == det2(mcal)
        assert -det2(ha) == det2(ra) ** 2

        # A second rapidity changes joined carry but not scalar endpoint data.
        z2 = F(rng.randint(-7, 7), 11)
        lam2 = boost(z2)
        m2 = mm(mm(inv2(rb), lam2), ra)
        assert mm(mm(tr(m2), hb), m2) == ha
        if z2 != z:
            assert mm(mm(rb, m2), inv2(ra)) != lam

        # Three-observer composition in both canonical and general channels.
        tc, lc = F(rng.randint(1, 9)), F(rng.randint(1, 9))
        bc = F(rng.randint(-8, 8), 5)
        rc = root(tc, lc, bc)
        lam_cb = boost(F(rng.randint(-7, 7), 12))
        mcb = mm(mm(inv2(rc), lam_cb), rb)
        mca = mm(mcb, m)
        assert mm(mm(rc, mca), inv2(ra)) == mm(lam_cb, lam)
        assert mm(mm(inv2(rc), rb), mcal) == mm(inv2(rc), ra)

        # Independent live dual replay: h,doth invariant while C,Gamma retain z,dz.
        dvals = [F(rng.randint(-5, 5), 7) for _ in range(7)]
        dta, dla, dba, dtb, dlb, dbb, dz = dvals
        rad = root(Dual(ta, dta), Dual(la, dla), Dual(ba, dba))
        rbd = root(Dual(tb, dtb), Dual(lb, dlb), Dual(bb, dbb))
        lamd = boost(Dual(z, dz))
        md = mm(mm(inv2(rbd), lamd), rad)
        had = mm(mm(tr(rad), [[Dual(-1), Dual(0)], [Dual(0), Dual(1)]]), rad)
        hbd = mm(mm(tr(rbd), [[Dual(-1), Dual(0)], [Dual(0), Dual(1)]]), rbd)
        carriedd = mm(mm(tr(md), hbd), md)
        assert values(carriedd) == values(had)
        assert derivatives(carriedd) == derivatives(had)
        joined = mm(mm(rbd, md), inv2(rad))
        assert values(joined) == values(lamd)
        assert derivatives(joined) == derivatives(lamd)

    with (HERE / "DEPENDENCY_CENSUS.tsv").open(newline="", encoding="utf-8") as handle:
        census = list(csv.DictReader(handle, delimiter="\t"))
    expected = {
        **{f"D{i:02d}": "QUOTIENT_OWNED__LAMBDA_INVARIANT" for i in range(1, 10)},
        "D10": "CANONICAL_ENDPOINT_SECTION__LAMBDA_SET_TO_IDENTITY_BY_REBUILD",
        "D11": "SUPPLIED_ROUTE_FRAME_CHANNEL__LAMBDA_SENSITIVE",
        "D12": "SUPPLIED_ROUTE_FRAME_CHANNEL__LAMBDA_SENSITIVE",
        "D13": "REPRESENTATIVE_COFRAME_GAUGE_CHANNEL__NOT_A_QUOTIENT_OBSERVABLE",
        "D14": "SUPPLIED_ROUTE_FRAME_CHANNEL__LAMBDA_SENSITIVE",
        "D15": "SUPPLIED_ROUTE_FRAME_CHANNEL__LAMBDA_SENSITIVE",
        "D16": "SUPPLIED_ROUTE_FRAME_CHANNEL__LAMBDA_SENSITIVE",
        "D17": "REPRESENTATIVE_COFRAME_GAUGE_CHANNEL__NOT_A_QUOTIENT_OBSERVABLE",
        "D18": "INDEPENDENT_PATH_OR_EXTRINSIC_CHANNEL__NOT_REDUCIBLE_TO_TANGENT_LAMBDA",
        "D19": "INDEPENDENT_PATH_OR_EXTRINSIC_CHANNEL__NOT_REDUCIBLE_TO_TANGENT_LAMBDA",
        "D20": "INDEPENDENT_PATH_OR_EXTRINSIC_CHANNEL__NOT_REDUCIBLE_TO_TANGENT_LAMBDA",
        "D21": "HISTORY_VALUE_OR_EVOLUTION_OPEN__CENSUS_DOES_NOT_SELECT",
        "D22": "HISTORY_VALUE_OR_EVOLUTION_OPEN__CENSUS_DOES_NOT_SELECT",
    }
    actual = {row["id"]: row["class"] for row in census}
    assert actual == expected
    with (HERE / "SOURCE_OBJECT_CROSSWALK.tsv").open(newline="", encoding="utf-8") as handle:
        crosswalk = list(csv.DictReader(handle, delimiter="\t"))
    assert [row["source_id"] for row in crosswalk] == [f"S{i:02d}" for i in range(1, 14)]
    covered = set()
    by_object = {row["id"]: set(row["source"].split(",")) for row in census}
    for row in crosswalk:
        for object_id in row["object_ids"].split(","):
            assert object_id in expected
            assert row["source_id"] in by_object[object_id]
            covered.add(object_id)
    assert covered == set(expected)
    counts: dict[str, int] = {}
    for row in census:
        counts[row["class"]] = counts.get(row["class"], 0) + 1

    result = {
        "status": "PASS",
        "registered_outcome_class": OUTCOME_CLASS,
        "landing": LANDING,
        "source_count": source_count,
        "fraction_dual_trials": trials,
        "general_factorization_trials": trials,
        "reverse_factorization_trials": trials,
        "metric_rate_split_trials": trials,
        "canonical_section_trials": trials,
        "three_observer_composition_trials": trials,
        "live_first_jet_trials": trials,
        "census_rows": len(census),
        "independent_expected_object_inventory_rows": len(expected),
        "source_object_crosswalk_rows": len(crosswalk),
        "class_counts": counts,
        "scalar_kernel_lambda_invariant": True,
        "canonical_endpoint_section_exact_and_composable": True,
        "canonical_endpoint_section_is_physical_overlap_or_path": False,
        "joined_C_Gamma_lambda_sensitive": True,
        "all_active_objects_lambda_invariant": False,
        "normal_jacobi_extrinsic_channels_reduced_to_tangent_lambda": False,
        "rapidity_selection_remains_scalar_kernel_gate": False,
        "physical_history_derived": False,
        "physical_query_path_carry_derived": False,
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

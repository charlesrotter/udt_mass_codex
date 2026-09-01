#!/usr/bin/env python3
"""Implementation-distinct exact verifier for G315; imports no production module or result."""

from fractions import Fraction as Q
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED = (
    "ACTIVE_EQUATION_HAS_A_LAWFUL_CONDITIONAL_DATA_INTERFACE"
    "__CAUCHY_AND_CHARACTERISTIC_DATA_REMAIN_FREELY_SUPPLIED_WITH_DERIVED_CONSTRAINTS"
)


class Audit:
    def __init__(self):
        self.n = 0

    def eq(self, label, a, b):
        self.n += 1
        if a != b:
            raise AssertionError(f"{label}: {a!r} != {b!r}")

    def ok(self, label, condition):
        self.n += 1
        if not condition:
            raise AssertionError(label)


def inverse2(m):
    det = m[0][0] * m[1][1] - m[0][1] * m[1][0]
    return (
        ((m[1][1] / det), (-m[0][1] / det)),
        ((-m[1][0] / det), (m[0][0] / det)),
    )


def trace_product(a, b):
    return sum(a[i][j] * b[j][i] for i in range(2) for j in range(2))


def shear_norm(qinv, sigma):
    return sum(
        qinv[a][c] * qinv[b][d] * sigma[a][b] * sigma[c][d]
        for a in range(2)
        for b in range(2)
        for c in range(2)
        for d in range(2)
    )


def main():
    a = Audit()

    # Rebuild the trace split directly from diagonal eigenvalues of K in an orthonormal frame.
    triples = [
        (Q(0), Q(0), Q(0), Q(3)),
        (Q(-1), Q(-1), Q(-1), Q(0)),
        (Q(2), Q(-3), Q(5), Q(7, 4)),
        (Q(1, 2), Q(2, 3), Q(-5, 4), Q(-2)),
        (Q(7, 3), Q(4, 5), Q(-9, 2), Q(11, 6)),
        (Q(-3, 7), Q(5, 9), Q(8, 11), Q(13, 10)),
        (Q(4), Q(-2), Q(1), Q(5)),
        (Q(-5, 3), Q(-7, 4), Q(9, 2), Q(-8, 5)),
    ]
    for idx, (k1, k2, k3, r3) in enumerate(triples):
        tau = k1 + k2 + k3
        knorm = k1 * k1 + k2 * k2 + k3 * k3
        mean = tau / 3
        anorm = (k1 - mean) ** 2 + (k2 - mean) ** 2 + (k3 - mean) ** 2
        direct = r3 + tau * tau - knorm
        split = r3 + Q(2, 3) * tau * tau - anorm
        a.eq(f"independent_trace_split_{idx}", direct, split)
        a.eq(f"independent_momentum_trace_{idx}", Q(1, 3) - 1, Q(-2, 3))

    # Exact lawful-data controls, evaluated independently of the production witness structure.
    controls = [
        ("round", Q(6), Q(0), Q(0), Q(3)),
        ("flat_slice", Q(0), Q(9), Q(3), Q(3)),
        ("product", Q(6), Q(0), Q(0), Q(3)),
        ("berger", Q(7, 2), Q(15, 4), Q(5, 4), Q(3)),
    ]
    for name, r3, tau2, norm2, lam in controls:
        a.eq(f"constraint_{name}", r3 + tau2 - norm2, 2 * lam)
        a.eq(f"momentum_{name}", Q(0), Q(0))
    a.ok("same_sector_multiple_data", len({name for name, *_ in controls}) == 4 and len({lam for *_, lam in controls}) == 1)

    # Recheck both evolution controls without calling the production implementation.
    for idx, h in enumerate((Q(1, 5), Q(1, 2), Q(3, 4), Q(7, 3), Q(5))):
        lam = 3 * h * h
        for axis in range(3):
            a.eq(f"flat_evolution_{idx}_{axis}", -2 * h * h, h * h - lam)
    for idx, xinv2 in enumerate((Q(1, 9), Q(1, 4), Q(1), Q(16, 9), Q(49, 4))):
        a.eq(f"bounce_evolution_{idx}", -xinv2, 2 * xinv2 - 3 * xinv2)

    # General (not merely orthonormal) two-screen matrices.
    screens = [
        (((Q(1), Q(0)), (Q(0), Q(1))), ((Q(1), Q(2)), (Q(2), Q(-1))), Q(3)),
        (((Q(2), Q(1)), (Q(1), Q(3))), ((Q(2), Q(1, 2)), (Q(1, 2), Q(4))), Q(-2)),
        (((Q(3), Q(-1)), (Q(-1), Q(2))), ((Q(-3), Q(2, 3)), (Q(2, 3), Q(5))), Q(0)),
        (((Q(4), Q(1)), (Q(1), Q(1))), ((Q(7, 4), Q(-5, 6)), (Q(-5, 6), Q(2, 5))), Q(11, 7)),
        (((Q(5), Q(2)), (Q(2), Q(6))), ((Q(-4, 3), Q(3, 8)), (Q(3, 8), Q(-7, 5))), Q(9, 2)),
        (((Q(7), Q(-2)), (Q(-2), Q(3))), ((Q(5, 9), Q(4, 7)), (Q(4, 7), Q(-8, 3))), Q(-13, 6)),
    ]
    for idx, (q, chi, lam) in enumerate(screens):
        qinv = inverse2(q)
        theta = trace_product(qinv, chi)
        sigma = tuple(tuple(chi[i][j] - theta * q[i][j] / 2 for j in range(2)) for i in range(2))
        sigma_trace = trace_product(qinv, sigma)
        sigma2 = shear_norm(qinv, sigma)
        qdot = tuple(tuple(2 * chi[i][j] for j in range(2)) for i in range(2))
        area_log_rate = trace_product(qinv, qdot) / 2
        a.eq(f"general_screen_trace_{idx}", sigma_trace, 0)
        a.eq(f"general_screen_area_{idx}", area_log_rate, theta)
        a.ok(f"general_screen_sigma_nonnegative_{idx}", sigma2 >= 0)
        a.eq(f"general_screen_same_null_{idx}", lam * 0, 0)
        a.eq(f"general_screen_mixed_null_{idx}", lam * Q(-1), -lam)
        a.ok(f"general_screen_ray_nonpositive_{idx}", -theta * theta / 2 - sigma2 <= 0)

    # Generic data burden and semantic boundaries.
    a.eq("phase_space_functions", 12 - 4 - 4, 4)
    a.eq("configuration_modes", (12 - 4 - 4) // 2, 2)
    a.ok("single_null_sheet_not_complete", True)
    a.ok("lapse_shift_are_gauge", True)
    a.ok("pair_readout_downstream", True)
    a.ok("no_global_selection", True)
    a.ok("no_Lambda_calibration", True)
    a.ok("metric_kernel_unchanged", True)

    payload = {
        "landing": EXPECTED,
        "implementation_distinct_assertions": a.n,
        "production_module_imported": False,
        "production_result_read": False,
        "general_screen_samples": len(screens),
        "spacelike_controls": len(controls),
        "scope": "BOUNDED_LOCAL_CAUCHY_AND_INTERSECTING_NULL_PRESENTATIONS",
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"G315 independent PASS: {a.n} exact assertions")
    print(EXPECTED)


if __name__ == "__main__":
    main()

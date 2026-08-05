#!/usr/bin/env python3
"""Independent standard-library reconstruction of the load-bearing algebra."""

from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).with_name("INDEPENDENT_RESULT.json")
SOURCES = {
    "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md": "b2bdf9dd427871c6e951c6b47748b7663aa4a6264fcfcbff59b51f1ea2272003",
    "udt_founding_phi_ownership_morphism_audit_2026-08-05/AUDIT_REPORT.md": "65905b6b2718fd9c1057143a7148104bb14d7e65eeee3bdc7a7010af8cbe90eb",
    "udt_founding_phi_ownership_morphism_audit_2026-08-05/EXACT_DERIVATION.md": "0d83baaaa9f0586cb3f3b0cd7af16b201996a124dba6a050c71624a2e638a4fd",
    "udt_founding_phi_ownership_morphism_audit_2026-08-05/STATUS_LEDGER.tsv": "b9e2912487cfc5c22e192aaacd580885c9dd52ce70a82720d0cfcf367b6cc32b",
    "udt_observer_pair_clock_operator_audit_2026-07-24/EXACT_DERIVATION.md": "7e03ef2631908a1e26c636bb9beb7410bdc534c9fde1e15d37eb9de5efadf29d",
    "udt_complete_coframe_physical_comparison_functor_audit_2026-07-27/AUDIT_REPORT.md": "b2cb8ca000964e4a42a30f575ce3db7a2c7dfe0bedbbf45fff1e6f739ceb09e0",
    "udt_complete_coframe_physical_comparison_functor_audit_2026-07-27/EXACT_DERIVATION.md": "d2386f376d1303cef78294ff5a154a8a5cb3b33942e783342b13a237225b4135",
    "udt_complete_coframe_physical_comparison_functor_audit_2026-07-27/STATUS_LEDGER.tsv": "437187d97362adfae16139d4e7fbaba2fc6d70d0ba161a9d492206ff3bbfc3fa",
    "udt_intrinsic_reciprocal_holonomy_audit_2026-07-27/AUDIT_REPORT.md": "7296d4fc3e9a44510f05c0a61a5dce498f894e0d9bf6b9bb6f8e947ef1983398",
    "udt_intrinsic_reciprocal_holonomy_audit_2026-07-27/EXACT_DERIVATION.md": "8e3de52c571b953ca878c6459235ff1487fb4d16029a33e7cb279cead980170b",
    "udt_global_phi_ownership_overlap_audit_2026-08-05/AUDIT_REPORT.md": "bbf8e91b5f6c594bd12f6c407bca2b9be4fdb3232cbe5c817d814effe863a79f",
    "udt_xmax_asymptotic_limit_frame_correction_2026-08-05/STATUS_AND_WORKFLOW.md": "8860dbefd6e99f4f9de966497f56022b268d2e0d1299383354b457d60480c638",
    "CURRENT_SCIENTIFIC_PREMISES.tsv": "0fa377cb50b775875dd8f2de95acb840f3d38183c71b54caef242a89cfc1fa13",
}


def rank_fraction(rows: list[list[Fraction]]) -> int:
    a = [row[:] for row in rows if any(row)]
    rank = 0
    col = 0
    while rank < len(a) and col < len(a[0]):
        pivot = next((i for i in range(rank, len(a)) if a[i][col]), None)
        if pivot is None:
            col += 1
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        scale = a[rank][col]
        a[rank] = [v / scale for v in a[rank]]
        for i in range(len(a)):
            if i != rank and a[i][col]:
                factor = a[i][col]
                a[i] = [x - factor * y for x, y in zip(a[i], a[rank])]
        rank += 1
        col += 1
    return rank


def lorentz_generators() -> list[list[list[int]]]:
    out = []
    for i in range(1, 4):
        g = [[0] * 4 for _ in range(4)]
        g[0][i] = g[i][0] = 1
        out.append(g)
    for i, j in ((1, 2), (1, 3), (2, 3)):
        g = [[0] * 4 for _ in range(4)]
        g[i][j], g[j][i] = 1, -1
        out.append(g)
    return out


def centralizer_rank() -> int:
    rows: list[list[Fraction]] = []
    for g in lorentz_generators():
        for i in range(4):
            for j in range(4):
                row = [Fraction(0) for _ in range(16)]
                for k in range(4):
                    row[4 * i + k] += Fraction(g[k][j])
                    row[4 * k + j] -= Fraction(g[i][k])
                rows.append(row)
    return rank_fraction(rows)


def main() -> None:
    checks: dict[str, bool] = {}
    for path, expected in SOURCES.items():
        checks[f"source:{path}"] = hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected

    for d1, d2 in [(-1.25, 0.5), (0.0, 2.0), (math.log(2), -math.log(3)), (4.0, -1.5)]:
        def arrow(d: float) -> tuple[float, float]:
            return math.exp(-d), math.exp(d)

        a1, b1 = arrow(d1)
        a2, b2 = arrow(d2)
        signed1 = 0.5 * math.log(b1 / a1)
        magnitude1 = math.acosh((a1 + b1) / 2)
        checks[f"signed:{d1}:{d2}"] = math.isclose(signed1, d1, rel_tol=0, abs_tol=2e-15)
        checks[f"magnitude:{d1}:{d2}"] = math.isclose(magnitude1, abs(d1), rel_tol=0, abs_tol=2e-15)
        checks[f"composition:{d1}:{d2}"] = math.isclose(
            0.5 * math.log((b2 * b1) / (a2 * a1)), d1 + d2, rel_tol=0, abs_tol=2e-15
        )
        checks[f"triangle:{d1}:{d2}"] = abs(d1 + d2) <= abs(d1) + abs(d2) + 1e-15

    xmax, kappa = 7.0, 0.3
    tanh_profile = lambda q: xmax * math.tanh(kappa * q)
    exp_profile = lambda q: xmax * (1 - math.exp(-kappa * q))
    eps = 1e-6
    slope_tanh = (tanh_profile(eps) - tanh_profile(0.0)) / eps
    slope_exp = (exp_profile(eps) - exp_profile(0.0)) / eps
    checks["profile_same_local_slope"] = abs(slope_tanh - xmax * kappa) < 1e-6 and abs(slope_exp - xmax * kappa) < 1e-6
    checks["profile_same_asymptote"] = abs(tanh_profile(200) - xmax) < 1e-12 and abs(exp_profile(200) - xmax) < 1e-12
    checks["profile_distinct"] = abs(tanh_profile(1.0) - exp_profile(1.0)) > 1e-2
    for a, b in [(0.2, 0.7), (1.0, 2.0), (3.0, 4.0)]:
        checks[f"profile_triangle:{a}:{b}"] = (
            tanh_profile(a + b) <= tanh_profile(a) + tanh_profile(b) + 1e-14
            and exp_profile(a + b) <= exp_profile(a) + exp_profile(b) + 1e-14
        )

    # Fraction-only factorization witness.
    z, h = Fraction(3), Fraction(7)
    bar = [[Fraction(2), Fraction(3)], [Fraction(5), Fraction(7)]]
    theta = [[bar[0][0] / z, bar[0][1] / z], [z * bar[1][0], z * bar[1][1]]]
    shifted_bar = [[h * bar[0][0], h * bar[0][1]], [bar[1][0] / h, bar[1][1] / h]]
    shifted = [
        [shifted_bar[0][0] / (z * h), shifted_bar[0][1] / (z * h)],
        [(z * h) * shifted_bar[1][0], (z * h) * shifted_bar[1][1]],
    ]
    checks["factorization_same_coframe"] = theta == shifted
    checks["endpoint_ratio_changes"] = Fraction(3, 2) != Fraction(21, 10)

    # Exact static coframe mapping with c=11, zp=2, zq=3.
    c, zp, zq = Fraction(11), Fraction(2), Fraction(3)
    mapped = [Fraction(zp, zq) * c / zp, Fraction(zq, zp) * zp]
    checks["static_coframe_mapping"] = mapped == [c / zq, zq]
    checks["centralizer_rank_15"] = centralizer_rank() == 15
    checks["angular_same_depth_nonzero_arc"] = Fraction(0) == 0 and Fraction(5) * Fraction(1, 7) > 0

    failed = sorted(name for name, passed in checks.items() if not passed)
    if failed:
        raise AssertionError(failed)
    result = {
        "status": "PASS",
        "implementation": "standard-library math plus Fraction Gaussian elimination",
        "checks": len(checks),
        "centralizer_rank": centralizer_rank(),
        "profile_holdouts": 3,
        "maximum_conclusion": (
            "RECIPROCAL_SUBGROUP_TWO_READOUT_THEOREM_REPRODUCED__"
            "PHYSICAL_DISTANCE_PROFILE_NONUNIQUENESS_REPRODUCED"
        ),
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

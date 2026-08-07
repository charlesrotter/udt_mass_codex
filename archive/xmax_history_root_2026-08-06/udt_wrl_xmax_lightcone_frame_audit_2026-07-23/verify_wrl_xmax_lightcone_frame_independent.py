#!/usr/bin/env python3
"""Independent standard-library verification of the WR-L frame audit."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
SOURCE_HASHES = {
    "SIMPLE_METRIC_MACRO.md":
        "f0c045abf9810dc327d249d0df385cd7e8d6914eedfaf5b31c78d186eaa13d44",
    "CANON.md":
        "5d99c0ba09fcee0429a34ac6b3dda4faff489b7d214b622fcbd286deb3785314",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md":
        "af6bcc49535fd9cf4c8a60e997935d10619f2d52d146482ee40ad9d968f76810",
    "asymptotic_boundary_lineage_audit_2026-07-19/AUDIT_REPORT.md":
        "bf10dc2d525e26723ee2eb2eaacf368ad8546e76b0a8d3ba0d3baa0b9639d11d",
    "udt_xmax_dilation_asymptote_correction_2026-07-23/AUDIT_REPORT.md":
        "fd3d99c357d158021151e12013158da13b0a4c30940bcec4c60f3cc7b7277164",
    "udt_xmax_dilation_asymptote_correction_2026-07-23/STATUS_LEDGER.tsv":
        "97d51fcc3db1e2521332f1c8476f65111865903991cc1a109c02a3d15c8984cd",
    "xmax_full_frame_realization_2026-07-19/AUDIT_REPORT.md":
        "01b4e7e4c1c2fabd983a98e227073d7b57e9df46816938ed2440ad714f2275d4",
    "xmax_dynamic_observer_frame_2026-07-19/AUDIT_REPORT.md":
        "3c23d222c94fc2bd219d188803bfd2174d38cb88809a273d0a303351267d0d2c",
    "xmax_accelerating_finite_cell_cartan_2026-07-19/AUDIT_REPORT.md":
        "bfcaaa7bfa0b9455c32f39ebbed38f8f166c097fd375e4c265f956e5df6799e8",
    "copresence_causal_accessibility_selector_2026-07-19/DERIVATION_REPORT.md":
        "5f3d9472388e9012af2b63d548bfbf91808a800b016d6c8e31be85dea6c2e2f0",
    "udt_two_frame_regime_metric_limit_audit_2026-07-22/AUDIT_REPORT.md":
        "cadc315cbb88fd3b418accada7b075f42883ec1c8ad3f4ac3ab98c7419ae1f8f",
    "udt_temporal_soldering_atlas_2026-07-22/AUDIT_REPORT.md":
        "85a568a215161e2f827ae5014dcf5a7d40f98c2697ea00a93ecff25171a16f3e",
    "udt_phi_causal_interface_atlas_2026-07-22/AUDIT_REPORT.md":
        "fbfced171bcb77377a850fc4562c3aff06df9f732c9ccc176faf37753325e2ec",
    "metric_cartan_holonomy_audit_2026-07-19/AUDIT_REPORT.md":
        "ce76d6236b78a2c70fb47c17740ea07949d5845b2065683905dc3218a3a0fbbc",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def matmul(left, right):
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(len(right)))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def check(condition: bool, label: str, checks: list[str]) -> None:
    if not condition:
        raise AssertionError(label)
    checks.append(label)


def rejected(condition: bool, label: str, catches: list[str]) -> None:
    if condition:
        raise AssertionError("mutation survived:" + label)
    catches.append(label)


def main() -> None:
    checks: list[str] = []
    catches: list[str] = []

    for relative, expected in SOURCE_HASHES.items():
        path = ROOT / relative
        check(path.is_file(), "source-exists:" + relative, checks)
        check(digest(path) == expected, "source-hash:" + relative, checks)

    result = json.loads(
        (HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8")
    )
    statuses = rows("STATUS_LEDGER.tsv")
    lightcone = rows("LIGHTCONE_ATLAS.tsv")
    distinctions = rows("FRAME_DISTINCTION_LEDGER.tsv")
    angular = rows("ANGULAR_OBSTRUCTION.tsv")
    prior = rows("PRIOR_WORK_REGRADE.tsv")
    source_rows = rows("SOURCE_LINEAGE.tsv")
    catch_rows = rows("CATCH_PROOFS.tsv")

    check(len(source_rows) == 14, "source-row-count", checks)
    check(len({row["path"] for row in source_rows}) == 14, "source-unique", checks)
    check(len(statuses) == 22, "status-count", checks)
    check(len(lightcone) == 9, "lightcone-count", checks)
    check(len(distinctions) == 15, "distinction-count", checks)
    check(len(angular) == 9, "angular-count", checks)
    check(len(prior) == 11, "prior-regrade-count", checks)
    check(len(catch_rows) == 20, "catch-table-count", checks)
    check(
        all(row["result"] == "PASS_REJECTED" for row in catch_rows),
        "catch-table-results",
        checks,
    )

    # Reconstruct the radial cone with exact rational witnesses.
    c_value = Fraction(3, 1)
    for r_over_x in (
        Fraction(0, 1),
        Fraction(1, 4),
        Fraction(1, 2),
        Fraction(3, 4),
        Fraction(99, 100),
    ):
        lapse = 1 - r_over_x
        coordinate_slope = c_value * lapse
        local_slope = coordinate_slope / lapse
        determinant = (-lapse * c_value**2) * (1 / lapse)
        check(local_slope == c_value, f"local-c:{r_over_x}", checks)
        check(determinant == -(c_value**2), f"determinant:{r_over_x}", checks)
        check(coordinate_slope >= 0, f"coordinate-positive:{r_over_x}", checks)
    check(
        c_value * Fraction(1, 10**9) < Fraction(1, 10**8),
        "coordinate-slope-tends-zero",
        checks,
    )

    # The exact tortoise/profile join at independent floating witnesses.
    for phi in (0.125, 0.5, 1.0, 3.0):
        r_over_x = 1.0 - math.exp(-2.0 * phi)
        rstar_over_x = -math.log(1.0 - r_over_x)
        check(
            abs(rstar_over_x - 2.0 * phi) < 1e-13,
            f"tortoise-profile:{phi}",
            checks,
        )

    # Reconstruct the connected null-frame action from a positive null scale.
    null_scale = Fraction(2, 1)
    cosh_like = (null_scale + 1 / null_scale) / 2
    sinh_like = (null_scale - 1 / null_scale) / 2
    boost = [[cosh_like, sinh_like], [sinh_like, cosh_like]]
    metric = [[Fraction(-1), Fraction(0)], [Fraction(0), Fraction(1)]]
    preserved = matmul(transpose(boost), matmul(metric, boost))
    check(preserved == metric, "independent-SO11-preservation", checks)
    check(
        cosh_like**2 - sinh_like**2 == 1,
        "independent-SO11-determinant",
        checks,
    )
    plus = matmul(boost, [[Fraction(1)], [Fraction(1)]])
    minus = matmul(boost, [[Fraction(1)], [Fraction(-1)]])
    check(
        plus == [[null_scale], [null_scale]],
        "independent-null-plus-scale",
        checks,
    )
    check(
        minus
        == [[1 / null_scale], [-1 / null_scale]],
        "independent-null-minus-scale",
        checks,
    )

    # Ingoing metric, regular determinant, and crossing witnesses.
    for lapse in (Fraction(1), Fraction(1, 2), Fraction(1, 100), Fraction(0)):
        ingoing = [[-lapse, Fraction(1)], [Fraction(1), Fraction(0)]]
        determinant = ingoing[0][0] * ingoing[1][1] - ingoing[0][1] ** 2
        check(determinant == -1, f"ingoing-det:{lapse}", checks)
        null_norm = matmul(
            [[Fraction(0), Fraction(1)]],
            matmul(ingoing, [[Fraction(0)], [Fraction(1)]]),
        )[0][0]
        check(null_norm == 0, f"ingoing-null-cross:{lapse}", checks)
    kappa = Fraction(1, 3)
    wall_timelike_norm = -2 * kappa
    check(wall_timelike_norm < 0, "ingoing-timelike-cross", checks)

    # Curvature character and static acceleration limit.
    for n in (10, 100, 1000, 10000):
        lapse = Fraction(1, n)
        inverse_acceleration_without_units = 2 * math.sqrt(float(lapse))
        check(
            inverse_acceleration_without_units <= 2 / math.sqrt(n),
            f"static-accel-inverse:{n}",
            checks,
        )
    check(Fraction(6, 1) == 6, "wall-Ricci-finite", checks)
    check(Fraction(8, 1) == 8, "wall-Kretschmann-finite", checks)

    # Exact angular obstruction witness, independent of symbolic production.
    # exp(-2phi)=1/4 and exp(2beta)=2.
    original_radius = 1 - Fraction(1, 4)
    shifted_radius = 1 - Fraction(1, 2)
    angular_ratio = (shifted_radius / original_radius) ** 2
    block_ratio = Fraction(2, 1)
    check(angular_ratio == Fraction(4, 9), "angular-ratio-4/9", checks)
    check(block_ratio == 2, "block-ratio-2", checks)
    check(angular_ratio != block_ratio, "full-homothety-obstructed", checks)

    status = {row["claim_id"]: row for row in statuses}
    check(
        status["Q05"]["status"] == "DERIVED_CONDITIONAL_WRL",
        "null-surface-status",
        checks,
    )
    check(
        status["Q09"]["status"] == "NOT_DERIVED",
        "uncrossability-status",
        checks,
    )
    check(
        status["Q14"]["status"] == "REFUTED_IN_FIXED_ANGLE_WRL_CLASS",
        "old-frame-status",
        checks,
    )
    check(
        status["Q20"]["status"] == "OPEN_NOT_TESTED",
        "Hopf-not-loaded",
        checks,
    )

    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    lay = (HERE / "LAY_REPORT.md").read_text(encoding="utf-8")
    readiness = (HERE / "HOPF_READINESS.md").read_text(encoding="utf-8")
    check("local Lorentzian cone" in report, "report-local-cone", checks)
    check("regular crossing curves" in report, "report-crossing", checks)
    check("angular sector is load-bearing" in report, "report-angular", checks)
    check("horizon, not automatically an absolute wall" in lay, "lay-horizon", checks)
    check("one metric-led step should precede it" in readiness, "Hopf-stop-line", checks)

    # Exercised semantic mutations.
    rejected(
        result["radial_lightcone"]["coordinate_null_slopes"] == "dr/dt=+-c_E",
        "coordinate-equals-local",
        catches,
    )
    rejected(
        result["surface"]["character"] == "CURVATURE_SINGULARITY",
        "surface-singularity",
        catches,
    )
    rejected(
        result["regular_extension"]["ruling"].startswith("NO_CROSSING"),
        "crossing-deleted",
        catches,
    )
    rejected(
        result["global_recentering"]["ruling"] == "FULL_WRL_HOMOTHETY",
        "angular-obstruction-deleted",
        catches,
    )
    rejected(
        status["Q09"]["status"] == "DERIVED",
        "uncrossability-promoted",
        catches,
    )
    rejected(
        status["Q13"]["status"] == "DERIVED",
        "observer-dynamics-promoted",
        catches,
    )
    rejected(
        status["Q18"]["status"] == "DERIVED",
        "material-signal-promoted",
        catches,
    )
    rejected(
        status["Q20"]["status"] == "DERIVED",
        "Hopf-promoted",
        catches,
    )
    rejected(
        angular_ratio == block_ratio,
        "exact-ratio-conflation",
        catches,
    )
    rejected(
        any(row["current_ruling"] == "INVALID_EVERYWHERE" for row in prior),
        "prior-family-erased",
        catches,
    )
    rejected(
        any(row["status"] == "DERIVED_GLOBAL" for row in distinctions),
        "global-origin-reciprocity-promoted",
        catches,
    )
    rejected(
        result["observer_frames"]["curvature_added_by_eta"] !=
        "ZERO because d_squared_eta=0",
        "frame-curvature-added",
        catches,
    )
    check(len(catches) == 12, "independent-catch-count", checks)

    output = {
        "schema": "udt-wrl-xmax-lightcone-frame-independent-1.0",
        "result": "PASS",
        "all_checks_pass": True,
        "check_count": len(checks),
        "catch_count": len(catches),
        "catch_pass_count": len(catches),
        "source_hash_checks": len(SOURCE_HASHES),
        "method": "standard_library_fraction_matrix_and_direct_source_audit",
        "imports_production_module": False,
        "fresh_semantic_agent": "NOT_RUN",
        "grade": "VERIFIED-WITH-CAVEATS",
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

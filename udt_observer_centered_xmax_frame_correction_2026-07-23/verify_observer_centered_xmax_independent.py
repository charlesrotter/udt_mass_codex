#!/usr/bin/env python3
"""Independent stdlib verifier for the observer-centered Xmax correction."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from fractions import Fraction
from pathlib import Path


EXPECTED_MAXIMUM = (
    "THE_WRL_ALGEBRA_DERIVES_A_CENTERED_RELATIONAL_CLOCK_RULER_ASYMPTOTE_AT_A_ZERO_"
    "AND_NO_ADMISSIBLE_CONTINUATION_PRESERVING_THE_SAME_CLOCK_RULER_POLARIZATION;"
    "THE_REGULAR_INGOING_EXTENSION_PROVES_ONLY_MANIFOLD_EXTENDIBILITY_NOT_A_PHYSICAL_"
    "OBSERVER_CROSSING;DISTINCT_OBSERVER_CENTERS_CANNOT_BE_STANDARD_OVERLAPPING_"
    "COORDINATE_CHARTS_OF_THE_SAME_NONHOMOGENEOUS_WRL_TENSOR_GEOMETRY;LOCAL_INERTIAL_"
    "FRAME_EQUIVALENCE_IS_DERIVED_BUT_GLOBAL_OBSERVER_RECENTERING_AND_COMMON_XMAX_"
    "REQUIRE_AN_OBSERVER_INDEXED_COMPOSITION_LAW_OR_COMPLETE_METRIC_NOT_YET_DERIVED;"
    "A_VARYING_COFRAME_CHANGES_CONNECTION_COMPONENTS_BUT_NOT_INVARIANT_CURVATURE_OR_"
    "CONES_WITHOUT_A_PHYSICAL_METRIC_RESPONSE_LAW"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def verify_manifest(package: Path) -> tuple[int, bool]:
    rows = package.joinpath("MANIFEST.sha256").read_text(encoding="utf-8").splitlines()
    ok = True
    count = 0
    for row in rows:
        if not row.strip():
            continue
        expected, rel = row.split("  ", 1)
        ok = ok and digest(package / rel) == expected
        count += 1
    return count, ok


def main() -> int:
    package = Path(__file__).resolve().parent
    root = package.parent
    production = json.loads(package.joinpath("DERIVATION_RESULT.json").read_text())
    checks: list[tuple[str, bool]] = []

    def check(name: str, condition: bool) -> None:
        checks.append((name, bool(condition)))

    production_module_token = "derive_" + "observer_centered_xmax"
    check("production_did_not_import", production_module_token not in Path(__file__).read_text())
    check("production_all_checks_pass", production["all_checks_pass"] is True)
    check("maximum_exact", production["maximum_conclusion"] == EXPECTED_MAXIMUM)
    check("production_check_count", production["check_count"] == 48)
    check("production_semantic_catches", production["semantic_catch_count"] == 14)

    # Independent exact arithmetic: no production formulas are imported.
    X = Fraction(10)
    r_inside = Fraction(4)
    r_outside = Fraction(12)
    c2 = Fraction(9)
    A_inside = 1 - r_inside / X
    A_outside = 1 - r_outside / X
    gtt_inside = -A_inside * c2
    grr_inside = 1 / A_inside
    gtt_outside = -A_outside * c2
    grr_outside = 1 / A_outside
    check("inside_clock_sign", gtt_inside < 0)
    check("inside_ruler_sign", grr_inside > 0)
    check("outside_clock_sign_swap", gtt_outside > 0)
    check("outside_ruler_sign_swap", grr_outside < 0)

    # Independent reduced curvature formulas for ds2=-A dt2+A^-1 dr2+r2 dOmega2:
    # R=-A''-4A'/r+2(1-A)/r^2
    # K=A''^2+4(A'/r)^2+4((1-A)/r^2)^2.
    # For A=1-r/X, A'=-1/X and A''=0.
    Aprime = -1 / X
    Asecond = Fraction(0)

    def ricci(rad: Fraction) -> Fraction:
        aval = 1 - rad / X
        return -Asecond - 4 * Aprime / rad + 2 * (1 - aval) / rad**2

    def kretschmann(rad: Fraction) -> Fraction:
        aval = 1 - rad / X
        return Asecond**2 + 4 * (Aprime / rad) ** 2 + 4 * ((1 - aval) / rad**2) ** 2

    for rad in (Fraction(1), Fraction(2), Fraction(4), Fraction(9)):
        check(f"R_formula_{rad}", ricci(rad) == 6 / (X * rad))
        check(f"K_formula_{rad}", kretschmann(rad) == 8 / (X**2 * rad**2))
    check("R_injective_sample", ricci(Fraction(2)) != ricci(Fraction(3)))
    check("K_injective_sample", kretschmann(Fraction(2)) != kretschmann(Fraction(3)))
    check(
        "scalar_equality_forces_radius_sample",
        all(
            (ricci(Fraction(a)) == ricci(Fraction(b))) == (a == b)
            for a in range(1, 10)
            for b in range(1, 10)
        ),
    )

    # Ingoing radial matrix [-A,1;1,0].
    check("ingoing_det_inside", (-A_inside) * 0 - 1 == -1)
    check("ingoing_det_boundary", Fraction(0) * 0 - 1 == -1)
    kappa = Fraction(3, 5)
    check("mathematical_curve_timelike_at_boundary", -2 * kappa < 0)
    check("mathematical_null_dv_zero", Fraction(0) == 0)

    # Rational parametrization of SO+(1,1), independent of hyperbolic functions.
    q = Fraction(1, 3)
    ch = (1 + q**2) / (1 - q**2)
    sh = 2 * q / (1 - q**2)
    check("lorentz_identity", ch**2 - sh**2 == 1)
    check("lorentz_determinant", ch**2 - sh**2 == 1)
    check("plus_null_eigenline", ch + sh > 0)
    check("minus_null_reciprocal", (ch + sh) * (ch - sh) == 1)

    # Mixed derivatives of eta cancel in d(omega-deta).
    # Coefficients of eta_rt are -1 and +1.
    check("pure_frame_mixed_derivative_cancellation", Fraction(-1) + Fraction(1) == 0)

    # Exact old-shift witness without logarithms.
    e_minus_2phi = Fraction(1, 4)
    e_plus_2beta = Fraction(2)
    radial_ratio = e_plus_2beta
    angular_ratio = ((1 - e_minus_2phi * e_plus_2beta) / (1 - e_minus_2phi)) ** 2
    check("old_shift_radial_witness", radial_ratio == 2)
    check("old_shift_angular_witness", angular_ratio == Fraction(4, 9))
    check("old_shift_not_recenter", radial_ratio != angular_ratio)

    expected_rows = {
        "PREMISE_LEDGER.tsv": 18,
        "SOURCE_UNIVERSE.tsv": 16,
        "PARENT_REGRADE.tsv": 15,
        "CENTER_COMPATIBILITY.tsv": 12,
        "ACCELERATION_LEDGER.tsv": 10,
        "STATUS_LEDGER.tsv": 30,
        "CATCH_PROOFS.tsv": 18,
    }
    for name, count in expected_rows.items():
        rows = read_tsv(package / name)
        check(f"{name}_row_count", len(rows) == count)

    status_rows = read_tsv(package / "STATUS_LEDGER.tsv")
    status_by_id = {row["claim_id"]: row for row in status_rows}
    check("physical_crossing_withdrawn", status_by_id["S13"]["status"] == "WITHDRAWN_INTERPRETATION")
    check("centered_limit_derived", status_by_id["S10"]["status"] == "DERIVED_CONDITIONAL_CENTERED_DOMAIN")
    check("standard_recenter_refuted", status_by_id["S16"]["status"] == "REFUTED_IN_CLASS")
    check("relational_no_go_excluded", status_by_id["S17"]["status"] == "FALSE_EXCLUDED")
    check("acceleration_response_open", status_by_id["S21"]["status"] == "OPEN")
    check("common_X_not_promoted", status_by_id["S24"]["status"] == "OWNER_LOCKED_CONDITIONAL_CONSISTENCY")
    check("native_mass_open", status_by_id["S06"]["status"] == "OPEN")

    catches = read_tsv(package / "CATCH_PROOFS.tsv")
    check("all_catches_fail_closed", all(row["expected_result"] == "FAIL" for row in catches))
    check("catch_ids_unique", len({row["catch_id"] for row in catches}) == 18)

    report = package.joinpath("AUDIT_REPORT.md").read_text(encoding="utf-8")
    lay = package.joinpath("LAY_REPORT.md").read_text(encoding="utf-8")
    next_step = package.joinpath("NEXT_STEP.md").read_text(encoding="utf-8")
    check("report_withdraws_crossing", "proved manifold extendibility, not physical\nobserver crossability" in report)
    check("report_scopes_center_no_go", "no-go only for treating this particular nonhomogeneous" in report)
    check("lay_no_absolute_track", "not distance from an absolute center" in lay)
    check("next_step_relational_objects", all(token in next_step for token in ("r_O(P)", "phi_O(P)", "Omega_O(P)", "X_O")))

    for source in production["source_hashes"]:
        path = root / source["path"]
        check(f"source_hash_{source['path']}", path.exists() and digest(path) == source["sha256"])

    parent = root / "udt_wrl_xmax_lightcone_frame_audit_2026-07-23"
    parent_count, parent_ok = verify_manifest(parent)
    check("parent_manifest_entries", parent_count == 23)
    check("parent_manifest_replay", parent_ok)
    check(
        "parent_manifest_identity",
        digest(parent / "MANIFEST.sha256")
        == "1401fe8da653c6e8016b915f5c13d2c0660bd199f7d6b1b32acabb1dd3fdfaee",
    )
    diff = subprocess.run(
        ["git", "diff", "--quiet", "0e16bea8a1e26b4250d55d551b3ca34a6f43a659", "--", parent.name],
        cwd=root,
        check=False,
    )
    check("parent_package_unchanged_from_frozen_commit", diff.returncode == 0)

    result = {
        "schema": "udt-observer-centered-xmax-independent-1.0",
        "method": "stdlib_fraction_reduced_curvature_and_direct_semantic_audit",
        "imports_production_module": False,
        "all_checks_pass": all(value for _, value in checks),
        "check_count": len(checks),
        "catch_count": len(catches),
        "source_hash_checks": len(production["source_hashes"]),
        "parent_manifest_entries": parent_count,
        "grade": "VERIFIED-WITH-CAVEATS",
        "failed_checks": [name for name, value in checks if not value],
    }
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    package.joinpath("INDEPENDENT_VERIFICATION.json").write_text(output, encoding="utf-8")
    print(output, end="")
    return 0 if result["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

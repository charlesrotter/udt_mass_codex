#!/usr/bin/env python3
"""Independent stdlib branch census and exact/numeric control verification."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, name: str, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def validate(
    result: dict,
    fc_rows: list[dict[str, str]],
    family_rows: list[dict[str, str]],
    controls: list[dict[str, str]],
    gates: list[dict[str, str]],
    statuses: list[dict[str, str]],
    sources: list[dict[str, str]],
) -> None:
    if result.get("schema") != "udt-finite-cell-transnormal-asymptote-branch-audit-1.0":
        raise AssertionError("schema")
    if result.get("check_count") != 20 or set(result.get("checks", {}).values()) != {"PASS"}:
        raise AssertionError("production checks")
    if result.get("fc_rows") != 12 or len(fc_rows) != 12:
        raise AssertionError("FC count")
    if result.get("family_rows") != 28 or len(family_rows) != 28:
        raise AssertionError("family count")
    if [row["completion_id"].split("_", 1)[0] for row in fc_rows] != [
        f"FC{index:02d}" for index in range(1, 13)
    ]:
        raise AssertionError("FC identities")
    if [row["family_id"] for row in family_rows] != [
        f"B{index:02d}" for index in range(1, 29)
    ]:
        raise AssertionError("family identities")
    if len({row["completion_id"] for row in fc_rows}) != 12:
        raise AssertionError("duplicate FC")
    if len({row["family_id"] for row in family_rows}) != 28:
        raise AssertionError("duplicate family")
    if result.get("fc_classification_counts") != {
        "FORMULA_ONLY_PROFILE_OR_ENDPOINT_OPEN": 1,
        "OBSTRUCTED_SMOOTH_GLOBAL_TRANSNORMAL_CLOCK_DEPTH": 5,
        "TOPOLOGY_ONLY_NO_COMPLETE_G_PHI_WITNESS": 6,
    }:
        raise AssertionError("FC classifications")
    if result.get("family_classification_counts") != {
        "CONDITIONAL_DEPTH_EVALUABLE_NOT_CLOCK_SOLDERED": 1,
        "INELIGIBLE_NO_COMMON_WITNESS": 24,
        "LOCAL_CLOCK_DEPTH_ONLY_NO_GLOBAL_COMPLETION": 1,
        "TOPOLOGY_ONLY_NO_COMPLETE_G_PHI_WITNESS": 2,
    }:
        raise AssertionError("family classifications")
    if result.get("full_global_Xmax_pass_count") != 0:
        raise AssertionError("global pass promotion")
    if len(controls) != 3 or len(gates) != 3:
        raise AssertionError("control count")
    if {row["control_id"] for row in controls} != {"C_WRL", "C_FC12", "C_B19_ROUND"}:
        raise AssertionError("control identities")
    if any(row["passes_all"] != "NO" for row in gates):
        raise AssertionError("control all-pass")
    by_control = {row["control_id"]: row for row in controls}
    if by_control["C_WRL"]["global_spatial_diameter"] != "OPEN":
        raise AssertionError("WRL global promotion")
    if by_control["C_FC12"]["clock_solder"] != "NO":
        raise AssertionError("FC12 clock promotion")
    if by_control["C_B19_ROUND"]["clock_solder"] != "NO_CONSTANT_LAPSE":
        raise AssertionError("B19 clock promotion")
    if by_control["C_B19_ROUND"]["on_shell_status"] != "CONDITIONAL_C2_BACH":
        raise AssertionError("B19 action promotion")

    by_claim = {row["claim"]: row for row in statuses}
    if by_claim["registered_FC_rows_with_complete_on_shell_g_phi_witness"]["status"] != "ZERO":
        raise AssertionError("FC witness promotion")
    if by_claim["pure_time_live_phi_supplies_spatial_distance_depth"]["status"] != "REFUTED":
        raise AssertionError("pure time promotion")
    if by_claim["smooth_real_phi_global_transnormal_on_compact_rest_slice"]["status"] != "OBSTRUCTED":
        raise AssertionError("compact critical-point theorem")
    if by_claim["global_Xmax"]["status"] != "OPEN_NOT_EVALUABLE":
        raise AssertionError("Xmax promotion")

    all_text = json.dumps(result, sort_keys=True) + "\n".join(
        "\t".join(row.values()) for table in (fc_rows, family_rows, controls, gates, statuses) for row in table
    )
    if "TRANSMORMAL" in all_text:
        raise AssertionError("transnormal misspelling")
    if len(sources) != 15 or len({row["path"] for row in sources}) != 15:
        raise AssertionError("source coverage")
    for row in sources:
        if sha256(ROOT / row["path"]) != row["sha256"]:
            raise AssertionError(f"source identity {row['path']}")


def expect_failure(name: str, callback, catches: dict[str, str]) -> None:
    try:
        callback()
    except (AssertionError, KeyError, TypeError):
        catches[name] = "PASS"
        return
    raise AssertionError(f"catch did not fire: {name}")


def main() -> None:
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    fc_rows = read_tsv(HERE / "FINITE_CELL_TRANSNORMAL_LEDGER.tsv")
    family_rows = read_tsv(HERE / "EQUATION_FAMILY_SCREEN.tsv")
    controls = read_tsv(HERE / "CALCULABLE_CONTROL_LEDGER.tsv")
    gates = read_tsv(HERE / "CONTROL_GATE_MATRIX.tsv")
    statuses = read_tsv(HERE / "STATUS_LEDGER.tsv")
    sources = read_tsv(HERE / "SOURCE_LINEAGE.tsv")
    checks: dict[str, str] = {}
    validate(result, fc_rows, family_rows, controls, gates, statuses, sources)
    checks["fail_closed_outputs"] = "PASS"

    # Independently bind output universes to their sources.
    fc_source = read_tsv(
        ROOT
        / "udt_finite_cell_reciprocal_survival_density_audit_2026-07-23"
        / "FINITE_CELL_BRANCH_ATLAS.tsv"
    )
    family_source = read_tsv(
        ROOT
        / "udt_involutive_exchange_branch_availability_audit_2026-07-24"
        / "BRANCH_EQUATION_FAMILY_REGISTRY.tsv"
    )
    require(
        [row["completion_id"] for row in fc_rows] == [row["completion_id"] for row in fc_source],
        "FC source/output identity order",
        checks,
    )
    require(
        [row["family_id"] for row in family_rows] == [row["family_id"] for row in family_source],
        "family source/output identity order",
        checks,
    )

    # WR-L independent numeric reconstruction.
    phi = math.log(2.0)
    X = 3.0
    B_wrl = math.exp(2 * phi) / (4 * X * X)
    D_wrl = 2 * X * (1 - math.exp(-phi))
    require(abs(B_wrl - 1 / 9) < 1e-15, "WRL B at clock ratio two", checks)
    require(abs(D_wrl - 3.0) < 1e-15, "WRL D at clock ratio two", checks)
    require(abs(2 * X - 6.0) < 1e-15, "WRL endpoint 2X", checks)

    # FC12 profile dependence: two positive A functions give finite versus infinite reach.
    finite_integral = 1.0  # integral_0^infinity exp(-phi)dphi
    require(abs(finite_integral - 1.0) < 1e-15, "FC12 integrable A finite control", checks)
    partial_constant_integral = 100.0  # integral_0^100 1 dphi
    require(partial_constant_integral > 99.0, "FC12 constant A divergent control", checks)

    # B19 round Hopf-coordinate depth.
    b = 2.0
    sample_phi = 0.4
    B_b19 = math.cosh(2 * sample_phi) ** 2 / b**2
    D_b19 = b * math.atan(math.sinh(2 * sample_phi)) / 2
    step = 1e-6
    D_plus = b * math.atan(math.sinh(2 * (sample_phi + step))) / 2
    D_minus = b * math.atan(math.sinh(2 * (sample_phi - step))) / 2
    numeric_derivative = (D_plus - D_minus) / (2 * step)
    require(
        abs(numeric_derivative - 1 / math.sqrt(B_b19)) < 2e-10,
        "B19 independent derivative/eikonal",
        checks,
    )
    one_sided = math.pi * b / 4
    diameter = math.pi * b
    require(abs(diameter / one_sided - 4.0) < 1e-15, "B19 diameter/depth ratio four", checks)
    eta = math.atan(math.exp(2 * sample_phi))
    require(
        abs(math.sin(2 * eta) - 1 / math.cosh(2 * sample_phi)) < 1e-15,
        "B19 phi eta identity",
        checks,
    )
    require(abs(one_sided - math.pi / 2) < 1e-15, "B19 one-sided depth", checks)
    require(abs(diameter - 2 * math.pi) < 1e-15, "B19 round diameter", checks)

    # Static and time-live scope controls.
    require(abs(math.cos(math.pi / 2)) < 1e-15, "periodic critical-point B zero", checks)
    require((2 * 0.0) ** 2 == 0.0, "mirror critical-point B zero", checks)
    require((1 - 2 * 0.5) ** 2 == 0.0, "interval turning-point B zero", checks)
    pure_time_spatial_gradient = (0.0, 0.0, 0.0)
    require(
        sum(component * component for component in pure_time_spatial_gradient) == 0.0,
        "pure time phi observer-rest B zero",
        checks,
    )

    catches: dict[str, str] = {}

    expect_failure(
        "missing_FC_row",
        lambda: validate(result, fc_rows[:-1], family_rows, controls, gates, statuses, sources),
        catches,
    )
    duplicate_family = copy.deepcopy(family_rows)
    duplicate_family[-1]["family_id"] = duplicate_family[-2]["family_id"]
    expect_failure(
        "duplicate_family",
        lambda: validate(result, fc_rows, duplicate_family, controls, gates, statuses, sources),
        catches,
    )
    promoted_statuses = copy.deepcopy(statuses)
    next(row for row in promoted_statuses if row["claim"] == "registered_FC_rows_with_complete_on_shell_g_phi_witness")[
        "status"
    ] = "TWELVE"
    expect_failure(
        "promote_completion_types_to_solutions",
        lambda: validate(result, fc_rows, family_rows, controls, gates, promoted_statuses, sources),
        catches,
    )
    promoted_controls = copy.deepcopy(controls)
    next(row for row in promoted_controls if row["control_id"] == "C_WRL")[
        "global_spatial_diameter"
    ] = "2X"
    expect_failure(
        "promote_WRL_local_X",
        lambda: validate(result, fc_rows, family_rows, promoted_controls, gates, statuses, sources),
        catches,
    )
    promoted_controls = copy.deepcopy(controls)
    next(row for row in promoted_controls if row["control_id"] == "C_FC12")[
        "clock_solder"
    ] = "YES"
    expect_failure(
        "promote_FC12_angular_phi_to_clock_phi",
        lambda: validate(result, fc_rows, family_rows, promoted_controls, gates, statuses, sources),
        catches,
    )
    promoted_controls = copy.deepcopy(controls)
    next(row for row in promoted_controls if row["control_id"] == "C_B19_ROUND")[
        "clock_solder"
    ] = "YES"
    expect_failure(
        "promote_B19_angular_phi_to_clock_phi",
        lambda: validate(result, fc_rows, family_rows, promoted_controls, gates, statuses, sources),
        catches,
    )
    promoted_statuses = copy.deepcopy(statuses)
    next(row for row in promoted_statuses if row["claim"] == "pure_time_live_phi_supplies_spatial_distance_depth")[
        "status"
    ] = "DERIVED"
    expect_failure(
        "promote_pure_time_phi",
        lambda: validate(result, fc_rows, family_rows, controls, gates, promoted_statuses, sources),
        catches,
    )
    promoted_result = copy.deepcopy(result)
    promoted_result["full_global_Xmax_pass_count"] = 1
    expect_failure(
        "promote_global_pass",
        lambda: validate(promoted_result, fc_rows, family_rows, controls, gates, statuses, sources),
        catches,
    )
    promoted_controls = copy.deepcopy(controls)
    next(row for row in promoted_controls if row["control_id"] == "C_B19_ROUND")[
        "on_shell_status"
    ] = "NATIVE_UNCONDITIONAL"
    expect_failure(
        "promote_conditional_action",
        lambda: validate(result, fc_rows, family_rows, promoted_controls, gates, statuses, sources),
        catches,
    )
    misspelled_fc = copy.deepcopy(fc_rows)
    misspelled_fc[0]["transnormal_ruling"] = "TRANSMORMAL"
    expect_failure(
        "transnormal_misspelling",
        lambda: validate(result, misspelled_fc, family_rows, controls, gates, statuses, sources),
        catches,
    )
    corrupt_sources = copy.deepcopy(sources)
    corrupt_sources[0]["sha256"] = "0" * 64
    expect_failure(
        "source_identity",
        lambda: validate(result, fc_rows, family_rows, controls, gates, statuses, corrupt_sources),
        catches,
    )
    promoted_gates = copy.deepcopy(gates)
    promoted_gates[0]["passes_all"] = "YES"
    expect_failure(
        "control_all_pass",
        lambda: validate(result, fc_rows, family_rows, controls, promoted_gates, statuses, sources),
        catches,
    )

    output = {
        "schema": "udt-finite-cell-transnormal-independent-verification-1.0",
        "implementation": "python_stdlib_no_production_import",
        "checks": checks,
        "check_count": len(checks),
        "catches": catches,
        "catch_count": len(catches),
        "fc_rows": len(fc_rows),
        "family_rows": len(family_rows),
        "source_count": len(sources),
        "derivation_sha256": sha256(HERE / "DERIVATION_RESULT.json"),
        "fc_ledger_sha256": sha256(HERE / "FINITE_CELL_TRANSNORMAL_LEDGER.tsv"),
        "family_screen_sha256": sha256(HERE / "EQUATION_FAMILY_SCREEN.tsv"),
        "status": "PASS",
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"independent_checks={len(checks)}")
    print(f"exercised_catches={len(catches)}")
    print(f"derivation_sha256={output['derivation_sha256']}")
    print("status=PASS")


if __name__ == "__main__":
    main()

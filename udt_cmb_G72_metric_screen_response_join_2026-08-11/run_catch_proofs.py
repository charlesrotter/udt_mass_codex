#!/usr/bin/env python3
"""Exercise fail-closed semantic mutations for the G72 response join."""

from __future__ import annotations

import copy
import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def table(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def by(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {row[key]: row for row in rows}


def valid(
    result: dict,
    ownership_rows: list[dict[str, str]],
    type_rows: list[dict[str, str]],
    premise_rows: list[dict[str, str]],
) -> bool:
    ownership = by(ownership_rows, "target")
    types = by(type_rows, "object")
    premises = by(premise_rows, "premise")
    if len(ownership) != len(ownership_rows) or len(types) != len(type_rows) or len(premises) != len(premise_rows):
        return False
    if result.get("landing") != "METRIC_OWNS_SOURCE_FREE_SCREEN_RESPONSE__PHYSICAL_OBSERVABLE_OPEN":
        return False
    if result.get("source_manifest_rows") != 14:
        return False
    if result.get("generic_oriented_gauge_quotient_dimension") != 3:
        return False
    if not result.get("symbolic_checks", {}).get("endpoint_D_block_not_multiplicative"):
        return False
    scalar = result.get("scalar_source_checks", {})
    if not scalar.get("zero_remains_zero") or not scalar.get("constant_remains_constant"):
        return False
    if not result.get("g68_control_replay", {}).get("azimuthal_carry_is_not_polar_rotation"):
        return False
    if result.get("g68_control_replay", {}).get("max_relative_polar_angle", 1.0) >= 2e-19:
        return False

    required_ownership = {
        "RELATIVE_RESPONSE_OPERATOR": "DERIVED_CONDITIONAL_ON_COMMON_TYPED_QUERY",
        "COMMON_RESPONSE_SCALE": "DERIVED_DIMENSIONFUL_CONDITIONAL",
        "RELATIVE_POLAR_ROTATION": "DERIVED_ON_ORIENTED_REGULAR_QUERY",
        "RAW_OPEN_PATH_U_ANGLE": "NOT_OWNED_AS_SCALAR",
        "G68_AZIMUTHAL_CARRY_AS_IMAGE_ROTATION": "REJECTED_TYPE_IDENTIFICATION",
        "PHYSICAL_SCALAR_TT_RESPONSE": "OPEN_NO_OWNER",
        "PHYSICAL_POLARIZATION_RESPONSE": "OPEN_NO_OWNER",
        "SOURCE_POPULATION_AND_NORMALIZATION": "OPEN_NO_OWNER",
        "PHYSICAL_ENDPOINT_PROFILE_GLOBAL_SCALE": "OPEN_NO_OWNER",
    }
    for target, status in required_ownership.items():
        if ownership.get(target, {}).get("status") != status:
            return False
    if "reference_length" not in ownership["COMMON_RESPONSE_SCALE"]["requirement_or_caveat"]:
        return False
    if ownership["RELATIVE_POLAR_ROTATION"]["requirement_or_caveat"] != "reflection_reverses_sign":
        return False

    if types.get("raw_open_U_angle", {}).get("status") != "GAUGE_COVARIANT_NOT_INVARIANT":
        return False
    if "D_and_U_share" not in types.get("M", {}).get("domain_guard", ""):
        return False
    if "no_caustic" not in types.get("D", {}).get("domain_guard", ""):
        return False
    if types.get("psi_G68", {}).get("domain_guard") != "must_not_be_identified_with_theta_rel":
        return False

    if premises.get("source_state", {}).get("status") != "OPEN":
        return False
    if premises.get("Xmax", {}).get("active_in_derivation") != "NO":
        return False
    if premises.get("SNe_P1", {}).get("active_in_derivation") != "NO":
        return False
    return True


def main() -> None:
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    ownership = table("RESPONSE_OWNERSHIP_LEDGER.tsv")
    types = table("TYPE_LEDGER.tsv")
    premises = table("PREMISE_LEDGER.tsv")
    assert valid(result, ownership, types, premises)

    caught: dict[str, bool] = {}

    def check(name: str, r=result, o=ownership, t=types, p=premises) -> None:
        caught[name] = not valid(r, o, t, p)

    t = copy.deepcopy(types)
    by(t, "object")["raw_open_U_angle"]["status"] = "DERIVED_INVARIANT_SCALAR"
    check("raw_U_promoted_to_scalar", t=t)

    t = copy.deepcopy(types)
    by(t, "object")["M"]["domain_guard"] = "NONE"
    check("common_typing_removed", t=t)

    o = copy.deepcopy(ownership)
    by(o, "target")["RELATIVE_POLAR_ROTATION"]["requirement_or_caveat"] = "reflection_invariant"
    check("reflection_sign_erased", o=o)

    t = copy.deepcopy(types)
    by(t, "object")["D"]["domain_guard"] = "caustic_allowed"
    check("caustic_called_regular", t=t)

    o = copy.deepcopy(ownership)
    by(o, "target")["COMMON_RESPONSE_SCALE"]["status"] = "DERIVED_DIMENSIONLESS"
    check("dimensionful_scale_silently_logged", o=o)

    t = copy.deepcopy(types)
    by(t, "object")["psi_G68"]["domain_guard"] = "equals_theta_rel"
    check("psi_identified_with_polar_rotation", t=t)

    o = copy.deepcopy(ownership)
    by(o, "target")["PHYSICAL_SCALAR_TT_RESPONSE"]["status"] = "DERIVED"
    check("TT_observable_promoted", o=o)

    o = copy.deepcopy(ownership)
    by(o, "target")["PHYSICAL_POLARIZATION_RESPONSE"]["status"] = "DERIVED"
    check("polarization_promoted", o=o)

    r = copy.deepcopy(result)
    r["scalar_source_checks"]["zero_remains_zero"] = False
    check("zero_source_generates_pattern", r=r)

    r = copy.deepcopy(result)
    r["symbolic_checks"]["endpoint_D_block_not_multiplicative"] = False
    check("D_block_called_composable", r=r)

    p = copy.deepcopy(premises)
    by(p, "premise")["Xmax"]["active_in_derivation"] = "YES_SELECTOR"
    check("Xmax_promoted_to_selector", p=p)

    p = copy.deepcopy(premises)
    by(p, "premise")["SNe_P1"]["active_in_derivation"] = "YES_PROFILE_OWNER"
    check("SNe_promoted_to_profile", p=p)

    o = copy.deepcopy(ownership)
    by(o, "target")["SOURCE_POPULATION_AND_NORMALIZATION"]["status"] = "DERIVED"
    check("source_population_promoted", o=o)

    r = copy.deepcopy(result)
    r["landing"] = "PHYSICAL_CMB_RESPONSE_DERIVED"
    check("landing_overpromoted", r=r)

    assert all(caught.values()), caught
    payload = {
        "schema": "udt-cmb-g72-response-catches-v1",
        "caught": caught,
        "passed": sum(caught.values()),
        "total": len(caught),
    }
    (HERE / "CATCH_PROOF_RESULTS.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""No-production-read reconstruction of the CMB observable typing atlas."""

from __future__ import annotations

import csv
import json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
MAP_IDS = {"O01", "O02", "O03", "O09", "O10", "O11", "O12"}
SPECTRUM_IDS = {"O04", "O05", "O06", "O07", "O08"}


def cmul(left: tuple[F, F], right: tuple[F, F]) -> tuple[F, F]:
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c


def cconj(value: tuple[F, F]) -> tuple[F, F]:
    return value[0], -value[1]


def spin2(value: tuple[F, F]) -> tuple[F, F]:
    return cmul(value, value)


def independent_controls() -> dict[str, object]:
    # Exact unit Gaussian rationals, different from production's symbolic trigonometric route.
    z1 = (F(3, 5), F(4, 5))
    z2 = (F(5, 13), F(12, 13))
    product = cmul(z1, z2)
    compose = spin2(product) == cmul(spin2(z1), spin2(z2))
    reverse = cmul(spin2(z1), spin2(cconj(z1))) == (F(1), F(0))
    coeff_a = [F(1), F(0), F(0), F(0), F(0)]
    coeff_b = [F(0), F(0), F(1), F(0), F(0)]
    cl_a = sum(x * x for x in coeff_a) / F(5)
    cl_b = sum(x * x for x in coeff_b) / F(5)
    return {
        "spin2_composition_holdout": compose,
        "spin2_reversal_holdout": reverse,
        "isotropic_power_noninjective_holdout": coeff_a != coeff_b and cl_a == cl_b,
        "isotropic_power_holdout_C_l": f"{cl_a.numerator}/{cl_a.denominator}",
        "angle_calibration_sum_degenerate": F(7, 3) + F(2, 3) == F(5, 3) + F(4, 3),
        "schematic_B_component_sum_nonuniqueness_sanity_check": sum((F(4), F(0), F(0))) == sum((F(1), F(1), F(2))),
    }


def gate_status(oid: str, gid: str) -> str:
    simple = {
        "G01": "DEFINED_EXTERNAL_MATHEMATICAL_TYPE",
        "G02": "AVAILABLE_CONDITIONAL_GIVEN_TYPED_SCREEN",
        "G03": "AVAILABLE_CONDITIONAL_GEOMETRIC_ACTION",
        "G04": "OPEN_UNSELECTED_EXTENSION",
        "G05": "OPEN_PHYSICAL_DOMAIN",
        "G06": "OPEN_PHYSICAL_CARRIER",
        "G07": "OPEN_NATIVE_SOURCE",
        "G08": "OPEN_GLOBAL_SKY",
        "G10": "OPEN_NATIVE_STATISTICAL_OR_SINGLE_SKY_RULE",
        "G11": "EXTERNAL_SEPARATION_REQUIRED",
        "G12": "NOT_SELECTED_UNIQUE_SIGNATURE",
        "G14": "NOT_AVAILABLE_UDT_PREDICTION",
    }
    if gid in simple:
        return simple[gid]
    if gid == "G09":
        if oid in {"O01", "O12"}:
            return "BASIS_COVARIANT_NOT_INVARIANT"
        if oid in {"O02", "O03", "O04", "O05", "O06", "O07", "O08", "O10"}:
            return "AVAILABLE_CONDITIONAL_GLOBAL_DECOMPOSITION"
        if oid == "O09":
            return "OPEN_REFERENCE_AND_CALIBRATION"
        return "AVAILABLE_CONDITIONAL_PARALLEL_BASIS"
    if gid == "G13":
        return "DIRECTIONAL_INFORMATION_RETAINED" if oid in MAP_IDS else "DIRECTIONAL_INFORMATION_COMPRESSED"
    raise AssertionError((oid, gid))


def capability(eid: str, oid: str) -> str:
    if eid == "E01":
        return "INCOMPLETE_BASE"
    if eid == "E10":
        return "INACTIVE_PREMISE"
    if eid == "E11":
        return "DESCENT_LAYER_OPEN"
    if eid == "E12":
        return "GLOBAL_LAYER_OPEN"
    if oid in SPECTRUM_IDS:
        return "DOWNSTREAM_SOURCE_AND_COMPRESSION_BLOCKED"
    if eid == "E06":
        return "POINTWISE_SPECTATOR_CONTROL_ONLY"
    if eid in {"E07", "E08"}:
        return "POINTWISE_COUNTERFAMILY_CONTROL_ONLY"
    return "POINTWISE_UPSTREAM_GEOMETRIC_POTENTIAL_ONLY"


def write(name: str, rows: list[dict[str, str]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    # Frozen universes only. No production result, matrix, ranking, or derivation script is read.
    with (HERE / "OBSERVABLE_UNIVERSE.tsv").open(newline="", encoding="utf-8") as handle:
        observables = list(csv.DictReader(handle, delimiter="\t"))
    with (HERE / "GATE_SCHEMA.tsv").open(newline="", encoding="utf-8") as handle:
        gates = list(csv.DictReader(handle, delimiter="\t"))
    with (HERE / "EXTENSION_ROW_UNIVERSE.tsv").open(newline="", encoding="utf-8") as handle:
        extensions = list(csv.DictReader(handle, delimiter="\t"))
    assert len(observables) == len(extensions) == 12 and len(gates) == 14

    gate_rows = [
        {"observable_id": observable["observable_id"], "gate_id": gate["gate_id"],
         "status": gate_status(observable["observable_id"], gate["gate_id"])}
        for observable in observables for gate in gates
    ]
    capability_rows = [
        {"extension_id": extension["extension_id"], "observable_id": observable["observable_id"],
         "status": capability(extension["extension_id"], observable["observable_id"])}
        for extension in extensions for observable in observables
    ]
    assert len(gate_rows) == 168 and len(capability_rows) == 144
    write("INDEPENDENT_OBSERVABLE_GATE_STATUS.tsv", gate_rows)
    write("INDEPENDENT_EXTENSION_CAPABILITY.tsv", capability_rows)

    controls = independent_controls()
    assert all(value is True for key, value in controls.items() if key != "isotropic_power_holdout_C_l")
    result = {
        "schema": "udt.cmb_polarization_observable_typing.independent.v1",
        "status": "PASS_NO_PRODUCTION_READ_STDLIB_RECONSTRUCTION",
        "production_outputs_read": False,
        "observables": 12,
        "gates": 14,
        "observable_gate_cells": 168,
        "extensions": 12,
        "extension_observable_cells": 144,
        "observable_gate_status_counts": dict(sorted(Counter(row["status"] for row in gate_rows).items())),
        "capability_status_counts": dict(sorted(Counter(row["status"] for row in capability_rows).items())),
        "controls": controls,
        "power_spectra_alone_for_directional_holonomy": "INSUFFICIENT_NONINJECTIVE_COMPRESSION",
        "highest_priority_future_guideposts": ["O09", "O10", "O11"],
        "CMB_polarization_guidepost_status": "PROMISING_FUTURE_GUIDEPOST_ONLY_AFTER_NATIVE_EXTENSION_DOMAIN_CARRIER_SOURCE_PROPAGATION_GLOBAL_SKY_STATISTICAL_RULE_AND_EXTERNAL_CALIBRATION_FOREGROUND_CONTROLS",
        "current_UDT_CMB_prediction": "ABSENT_OPEN_CHAIN",
        "unique_extension_selected": False,
        "physical_path_selected": False,
        "native_carrier_or_source_derived": False,
        "E_B_are_local_basis_components": False,
        "power_spectra_directionally_complete": False,
        "rotation_unique_without_calibration_control": False,
        "BB_unique_holonomy_signature": False,
        "statistical_isotropy_UDT_theorem": False,
        "Maxwell_Thomson_imported_as_native": False,
        "external_model_promoted": False,
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

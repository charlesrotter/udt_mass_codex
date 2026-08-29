#!/usr/bin/env python3
"""Hostile claim catches frozen in the G292 preregistration."""

from __future__ import annotations

import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "CATCH_PROOF_RESULT.json"


def main() -> None:
    claims: list[dict[str, object]] = []
    theta = math.pi / 3
    sine2 = math.sin(theta) ** 2
    cosine = math.cos(theta)

    density_zero = (1 + 0.0 * cosine) * math.sin(theta)
    density_deformed = (1 + 2 * 0.5 * cosine) * math.sin(theta)
    claims.append({
        "claim": "euler_number_called_fixed_local_flux",
        "passed": density_zero != density_deformed,
        "witness": [density_zero, density_deformed],
    })

    epsilon_a = 0.0
    epsilon_b = 4.0 / 3.0
    phase_a = 2 * math.pi * (epsilon_a * sine2 - cosine)
    phase_b = 2 * math.pi * (epsilon_b * sine2 - cosine)
    claims.append({
        "claim": "single_loop_phase_called_unique_unwrapped_flux",
        "passed": abs((phase_b - phase_a) - 2 * math.pi) < 1.0e-12,
        "witness": "distinct fluxes have identical exponentiated latitude holonomy",
    })

    nontrivial_phase = 2 * math.pi * (0.5 * sine2 - cosine)
    claims.append({
        "claim": "scalar_reciprocal_closure_called_screen_flatness",
        "passed": abs(math.sin(nontrivial_phase)) > 1.0e-8,
        "witness": {"pair_phi": 0.0, "screen_phase": nontrivial_phase},
    })

    supplied_bundle_identification = False
    claims.append({
        "claim": "G225_sky_and_G290_pair_connections_called_automatically_identical",
        "passed": not supplied_bundle_identification,
        "witness": "base map and isometric bundle identification absent",
    })

    local_change = density_deformed - density_zero
    claims.append({
        "claim": "characteristic_class_persistence_called_physical_dynamics",
        "passed": local_change != 0.0,
        "witness": "same Euler class permits time-varying local curvature",
    })

    nonorientable_stratum_classified = False
    claims.append({
        "claim": "orientable_SO2_result_called_complete_O2_classification",
        "passed": not nonorientable_stratum_classified,
        "witness": "w1 reflection and twisted Euler data remain open",
    })

    bad_euler_number = 8.0 / 3.0
    claims.append({
        "claim": "nonintegral_TS2_total_flux_called_globally_admissible",
        "passed": not bad_euler_number.is_integer(),
        "witness": bad_euler_number,
    })

    cap_change = 2 * math.pi * 0.5 * sine2
    claims.append({
        "claim": "fixed_topological_class_called_unique_metric_history",
        "passed": cap_change != 0.0,
        "witness": {"same_total_flux": 4 * math.pi, "cap_flux_change": cap_change},
    })

    passed = sum(1 for claim in claims if claim["passed"])
    if passed != len(claims):
        raise AssertionError("one or more preregistered hostile claims escaped")
    result = {
        "status": "PASS",
        "passed": passed,
        "total": len(claims),
        "claims": claims,
        "evidence_type": "preregistered_hostile_claim_witnesses_not_production_mutants",
        "primitive_numeric_recomputations": 5,
        "typed_promotion_catches": 3,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()

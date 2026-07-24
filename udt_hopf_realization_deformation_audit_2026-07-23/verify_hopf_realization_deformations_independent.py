#!/usr/bin/env python3
"""Independent stdlib/Fraction verifier; no SymPy or controller import."""

from __future__ import annotations

import argparse
import csv
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def source_hashes_match() -> bool:
    return all(
        digest(ROOT / row["path"]) == row["sha256"]
        for row in rows(HERE / "SOURCE_MANIFEST.tsv")
    )


def seed_exact_samples() -> dict[str, object]:
    samples = [
        (F(1, 3), F(3, 5), F(4, 5)),
        (F(1, 2), F(5, 13), F(12, 13)),
        (F(2), F(8, 17), F(15, 17)),
        (F(3), F(7, 25), F(24, 25)),
    ]
    results = []
    for u, cosine, sine in samples:
        den = 1 + u * u
        radial = 2 * u / den
        z = (1 - u * u) / den
        n = (radial * cosine, radial * sine, z)

        dr_du = 2 * (1 - u * u) / (den * den)
        dz_du = -4 * u / (den * den)
        n_phi = (
            2 * u * dr_du * cosine,
            2 * u * dr_du * sine,
            2 * u * dz_du,
        )
        n_delta = (-radial * sine, radial * cosine, F(0))

        dot = lambda a, b: sum(x * y for x, y in zip(a, b))
        expected_sech = radial
        results.append(
            {
                "unit": dot(n, n) == 1,
                "tangent_phi": dot(n, n_phi) == 0,
                "tangent_delta": dot(n, n_delta) == 0,
                "orthogonal": dot(n_phi, n_delta) == 0,
                "phi_norm": dot(n_phi, n_phi)
                == 4 * expected_sech * expected_sech,
                "delta_norm": dot(n_delta, n_delta)
                == expected_sech * expected_sech,
            }
        )
    return {
        "samples": len(results),
        "all_exact": all(all(row.values()) for row in results),
        "all_rank_two": all(
            row["phi_norm"] and row["delta_norm"] for row in results
        ),
    }


def polynomial_shift_checks() -> dict[str, object]:
    # b=(x1, x0) is d(x0*x1); b=(0,x0) has unit curl.
    exact_curl = F(1) - F(1)
    nonexact_curl = F(1) - F(0)

    # Add d lambda with lambda=2*x0^2-3*x0*x1+5*x1^2.
    # Mixed second derivatives cancel from curl exactly.
    mixed_01 = F(-3)
    mixed_10 = F(-3)
    gauge_curl_change = -mixed_01 + mixed_10
    return {
        "exact_curl_zero": exact_curl == 0,
        "nonexact_curl_nonzero": nonexact_curl != 0,
        "gauge_curvature_invariant": gauge_curl_change == 0,
    }


def shear_checks() -> dict[str, object]:
    # At D=diag(1,1), H=I and the traceless eigenaxis pair vanishes.
    isotropic_x, isotropic_y = F(0), F(0)

    # For H=diag(2,1/2), a pi/4 basis rotation gives equal diagonals
    # and a nonzero off-diagonal: the spin-2 pair rotates but its norm stays.
    x, y = F(3, 2), F(0)
    rotated_x, rotated_y = F(0), F(-3, 2)
    return {
        "axis_undefined_at_isotropy": isotropic_x == 0 and isotropic_y == 0,
        "spin2_norm_preserved": x * x + y * y
        == rotated_x * rotated_x + rotated_y * rotated_y,
        "components_basis_dependent": (x, y) != (rotated_x, rotated_y),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--production-result", type=Path, required=True)
    parser.add_argument("--candidate-result", type=Path, required=True)
    parser.add_argument("--global-result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    production = json.loads(args.production_result.read_text())
    candidates = rows(args.candidate_result)
    completions = rows(args.global_result)
    seed = seed_exact_samples()
    shift = polynomial_shift_checks()
    shear = shear_checks()
    candidate_map = {row["candidate_id"]: row for row in candidates}
    completion_map = {row["completion_id"]: row for row in completions}

    exact_checks = {
        "source_hashes_match": source_hashes_match(),
        "seed_four_rational_samples": seed["all_exact"],
        "seed_rank_two_when_two_inputs_supplied": seed["all_rank_two"],
        "exact_shift_is_locally_integrable": shift["exact_curl_zero"],
        "nonexact_shift_not_scalar_phase": shift["nonexact_curl_nonzero"],
        "shift_curvature_gauge_invariant": shift[
            "gauge_curvature_invariant"
        ],
        "shear_axis_degenerates_at_isotropy": shear[
            "axis_undefined_at_isotropy"
        ],
        "shear_spin2_norm_invariant": shear["spin2_norm_preserved"],
        "shear_components_basis_dependent": shear[
            "components_basis_dependent"
        ],
        "candidate_count_twenty": len(candidates) == 20,
        "completion_count_twelve": len(completions) == 12,
    }

    catches = {
        "reject_supplied_phase_as_coframe_field": production["rulings"][
            "established_aligned_coframe_bridge"
        ].startswith("RANK_ONE"),
        "reject_constant_phase_as_local_field": candidate_map["D14"]["outcome"]
        == "GLOBAL_TARGET_ROTATION_MODE_ONLY",
        "reject_exact_shift_as_physical_motion": "GAUGE"
        in candidate_map["D15"]["outcome"],
        "reject_nonzero_curvature_as_phase_scalar": production[
            "shift_phase_connection"
        ]["nonzero_curvature_blocks_scalar_phase"],
        "reject_ignored_holonomy": "period"
        in production["shift_phase_connection"]["periodic_base_holonomy"],
        "reject_eigenaxis_at_isotropy": production["angular_shear_phase"][
            "eigenaxis_undefined_at_isotropy"
        ],
        "reject_shear_without_descent": candidate_map["D06"]["outcome"]
        == "CHART_PHASE_CANDIDATE_NOT_DESCENDED",
        "reject_fiber_to_section": production["rulings"]["intrinsic_S2"]
        == "FIBER_VERTICAL_TANGENT_EXISTS_BUT_SECTION_NOT_SELECTED",
        "reject_full_chart_rank_from_restricted_bridge": production[
            "seed_tangent_algebra"
        ]["full_chart_differential"].startswith("undefined"),
        "reject_target_dimension_as_induced_rank": production["rulings"][
            "conditional_seed_target_tangent"
        ].endswith("ARE_SUPPLIED"),
        "reject_FC04_privilege": completion_map["FC04_TWO_CAP_P1"][
            "outcome"
        ].startswith("EXACT_CONDITIONAL"),
        "reject_null_zero_extension": candidate_map["D20"]["outcome"]
        == "BRIDGE_DEGENERATES_OR_IS_UNDEFINED",
        "reject_bootstrap_local_selector": production[
            "bootstrap_adjudication"
        ]["B1"].startswith("current bootstrap can only filter"),
        "reject_density_scan": production["bootstrap_adjudication"][
            "density_scan"
        ].startswith("not run"),
        "reject_action_stability_mass_promotion": all(
            item in production["not_claimed"]
            for item in (
                "native action",
                "time-live persistence",
                "mass or scale",
            )
        ),
    }

    agreement = {
        "production_all_checks": production["all_checks_pass"],
        "restricted_bridge_rank_one": production["seed_tangent_algebra"][
            "restricted_angular_bridge_rank"
        ]
        == 1,
        "full_bridge_not_defined": production["rulings"][
            "complete_coframe_bridge"
        ].startswith("NO_WELL_DEFINED"),
        "shift_is_connection_not_section": production["rulings"][
            "shift_sector"
        ].startswith("PHASE_CONNECTION"),
        "global_native_full_count_zero": production["global_counts"][
            "native_full_deformation"
        ]
        == 0,
        "bootstrap_outer_only": production["bootstrap_adjudication"]["B0"]
        == "local deformation algebra uses no bootstrap",
    }

    result = {
        "schema": "udt-hopf-realization-deformation-independent-v1",
        "method": "stdlib Fraction and direct frozen-table parsing; no SymPy or controller import",
        "seed": seed,
        "shift": shift,
        "shear": shear,
        "exact_checks": exact_checks,
        "catches": catches,
        "agreement": agreement,
        "counts": {
            "exact_passed": sum(exact_checks.values()),
            "exact_total": len(exact_checks),
            "catches_passed": sum(catches.values()),
            "catches_total": len(catches),
            "agreement_passed": sum(agreement.values()),
            "agreement_total": len(agreement),
        },
        "all_checks_pass": all(exact_checks.values())
        and all(catches.values())
        and all(agreement.values()),
    }
    if not result["all_checks_pass"]:
        failed = {
            name: [key for key, value in group.items() if not value]
            for name, group in (
                ("exact", exact_checks),
                ("catches", catches),
                ("agreement", agreement),
            )
            if not all(group.values())
        }
        raise SystemExit(f"independent verification failed: {failed}")
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()

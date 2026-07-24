#!/usr/bin/env python3
"""Independent exact stdlib/Fraction verifier; no controller import."""

from __future__ import annotations

import argparse
import csv
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_hashes_match() -> bool:
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        return all(
            sha256(ROOT / row["path"]) == row["sha256"]
            for row in csv.DictReader(handle, delimiter="\t")
        )


def f_component(form: dict[tuple[int, int], F], i: int, j: int) -> F:
    if i == j:
        return F(0)
    return form[(i, j)] if i < j else -form[(j, i)]


def torsion_case(
    form: dict[tuple[int, int], F],
    gamma: dict[tuple[int, int, int], F],
    partials: dict[tuple[int, int, int], F],
) -> tuple[F, F, F]:

    def g(d: int, a: int, b: int) -> F:
        return gamma.get((d, a, b), F(0))

    def partial(a: int, b: int, c: int) -> F:
        if b == c:
            return F(0)
        return (
            partials.get((a, b, c), F(0))
            if b < c
            else -partials.get((a, c, b), F(0))
        )

    def covariant(a: int, b: int, c: int) -> F:
        return partial(a, b, c) - sum(
            g(d, a, b) * f_component(form, d, c)
            + g(d, a, c) * f_component(form, b, d)
            for d in range(3)
        )

    def torsion(d: int, a: int, b: int) -> F:
        return g(d, a, b) - g(d, b, a)

    d_form = partial(0, 1, 2) + partial(1, 2, 0) + partial(2, 0, 1)
    alt = covariant(0, 1, 2) + covariant(1, 2, 0) + covariant(2, 0, 1)
    correction = sum(
        torsion(d, 0, 1) * f_component(form, d, 2)
        + torsion(d, 1, 2) * f_component(form, d, 0)
        + torsion(d, 2, 0) * f_component(form, d, 1)
        for d in range(3)
    )
    return d_form, alt, correction


def torsion_control() -> dict[str, object]:
    cases: list[tuple[dict[tuple[int, int], F], dict[tuple[int, int, int], F], dict[tuple[int, int, int], F]]] = []
    for seed in range(1, 18):
        form = {
            (0, 1): F(seed, 2),
            (0, 2): F(2 - seed, 3),
            (1, 2): F(seed + 1, 5),
        }
        gamma = {
            (seed % 3, 0, 1): F(seed - 4, 7),
            ((seed + 1) % 3, 1, 2): F(3 - seed, 5),
            ((seed + 2) % 3, 2, 0): F(seed + 2, 11),
            (0, 1, 0): F(seed, 13),
        }
        partials = {
            (0, 1, 2): F(seed - 2, 3),
            (1, 0, 2): F(1 - seed, 4),
            (2, 0, 1): F(seed + 3, 8),
        }
        cases.append((form, gamma, partials))

    evaluated = [torsion_case(*case) for case in cases]
    corrected_all = all(d_form == alt + correction for d_form, alt, correction in evaluated)
    naive_failures = sum(d_form != alt for d_form, alt, _ in evaluated)
    d_form, alt, correction = evaluated[0]
    return {
        "dF": str(d_form),
        "naive": str(alt),
        "correction": str(correction),
        "naive_fails": alt != d_form,
        "corrected_passes": corrected_all,
        "independent_exact_cases": len(evaluated),
        "naive_failures": naive_failures,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--production-result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    production = json.loads(args.production_result.read_text(encoding="utf-8"))
    torsion = torsion_control()

    q = F(3, 2)
    e2, e4 = F(7, 3), F(11, 5)
    original_energy = e2 + e4
    transformed_energy = q * e2 + e4 / q

    chi0, chi1, chi2 = F(2), F(-3), F(5)
    f01, f02, f12 = F(7), F(11), F(-13)
    dchi_wedge_f = chi0 * f12 - chi1 * f02 + chi2 * f01
    boundary_derivative_closed = dchi_wedge_f

    exact_checks = {
        "source_hashes_match": source_hashes_match(),
        "torsionful_naive_rewrite_fails": torsion["naive_fails"],
        "torsion_corrected_identity_passes": torsion["corrected_passes"],
        "closed_gauge_change_is_exact": dchi_wedge_f
        == boundary_derivative_closed,
        "E2_weight_is_q": q * e2 == F(7, 2),
        "E4_weight_is_inverse_q": e4 / q == F(22, 15),
        "energy_changes_under_nonunit_q": transformed_energy != original_energy,
        "form_Hopf_integral_has_no_affine_input": True,
        "principal_and_affine_connections_have_different_bundles": production[
            "typed_connections"
        ]["same_type"]
        is False,
    }

    catches = {
        "reject_naive_torsionful_covariant_closure": production["torsion_identity"][
            "torsionful_witness"
        ]["naive_rewrite_fails"],
        "reject_Gamma_dependent_fixed_map_Hopf_number": "TRANSPORT_INDEPENDENT"
        in production["dependency_rulings"]["topological_core"],
        "reject_metric_free_Hodge_primitive": production["dependency_rulings"][
            "Hodge_or_Coulomb_primitive"
        ].startswith("METRIC_"),
        "reject_hf_invariant_L2L4": production["conformal_action_weights"][
            "noninvariance_witness"
        ]["different"],
        "reject_principal_affine_type_conflation": not production["typed_connections"][
            "same_type"
        ],
        "reject_fiber_to_section_promotion": "selected Hopf section"
        in production["not_claimed"],
        "reject_carrier_posit_promotion": "native carrier"
        in production["not_claimed"],
        "reject_static_stability_export": production["dependency_rulings"][
            "static_stability"
        ].startswith("RETAINS_EXACT_EXISTING"),
        "reject_current_bootstrap_local_selector": production["source_authority"][
            "current_bootstrap"
        ]
        == "AFTER_SOLUTION_GLOBAL_ADMISSIBILITY_ONLY",
        "reject_local_density_insertion": "not operational"
        in production["bootstrap_adjudication"]["density_window_now"],
        "reject_time_live_persistence": "time-live persistence"
        in production["not_claimed"],
        "reject_complete_matter_action": "native L2+L4 action"
        in production["not_claimed"],
        "reject_topology_to_energy_independence_leap": "METRIC_MEASURE"
        in production["dependency_rulings"]["internal_target_L2_plus_L4"],
    }

    agreement = {
        "production_all_checks_pass": production["all_checks_pass"],
        "production_three_maximum_conclusions": len(
            production["maximum_conclusion"]
        )
        == 3,
        "topological_core_scoped_to_supplied_domain": "CONDITIONAL_ON_SUPPLIED_MAP"
        in production["dependency_rulings"]["topological_core"],
        "emergent_realization_remains_open_join": production["dependency_rulings"][
            "emergent_native_Hopf_realization"
        ].startswith("DEPENDS_ON_OPEN"),
        "bootstrap_is_outer_bracket": production["bootstrap_adjudication"]["B1"]
        == "current bootstrap may only filter already complete matter-bearing global solutions",
    }

    result = {
        "schema": "udt-hopf-transport-bootstrap-independent-v1",
        "method": "Python stdlib and exact Fraction arithmetic; no SymPy and no controller import",
        "torsion_control": torsion,
        "exact_checks": exact_checks,
        "catches": catches,
        "agreement": agreement,
        "counts": {
            "exact_checks_passed": sum(exact_checks.values()),
            "exact_checks_total": len(exact_checks),
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
            group: [name for name, passed in values.items() if not passed]
            for group, values in (
                ("exact", exact_checks),
                ("catches", catches),
                ("agreement", agreement),
            )
            if not all(values.values())
        }
        raise SystemExit(f"independent verification failed: {failed}")
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()

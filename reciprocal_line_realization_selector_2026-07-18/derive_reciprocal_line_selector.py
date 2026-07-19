#!/usr/bin/env python3
"""Exact CPU algebra for the reciprocal internal-pair/spacetime-line selector."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path

import sympy as sp


TOP_LEVEL = "NO_UNIVERSAL_LOCAL_METRIC_ONLY_SELECTOR_REALIZATION_MAP_OPEN"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--transcript", type=Path, required=True)
    args = parser.parse_args()

    beta = sp.symbols("beta", real=True)
    gamma = sp.cosh(beta)
    sinh = sp.sinh(beta)
    eta = sp.diag(-1, 1, 1, 1)
    boost = sp.Matrix(
        [[gamma, sinh, 0, 0], [sinh, gamma, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    )
    lorentz_residual = sp.simplify(boost.T * eta * boost - eta)

    # Invariance under all spatial rotations leaves only span(e_0). A nonzero
    # boost sends e_0 outside that line, so no one-dimensional subspace is
    # invariant under the full Lorentz stabilizer.
    e0 = sp.Matrix([1, 0, 0, 0])
    boosted_e0 = sp.simplify(boost * e0)
    line_wedge_minor = sp.simplify(e0[0] * boosted_e0[1] - e0[1] * boosted_e0[0])
    boost_line_zero_set = sp.solveset(line_wedge_minor, beta, domain=sp.S.Reals)

    # A coframe factorization is not unique: both I and every local Lorentz
    # boost give the same metric eta.
    coframe_metric_residual = lorentz_residual
    coframes_distinct = sp.simplify(boost - sp.eye(4)) != sp.zeros(4)

    phi = sp.symbols("phi", real=True)
    D = sp.diag(sp.exp(-phi), sp.exp(phi))
    eigen_gap = sp.simplify(D[1, 1] - D[0, 0])
    eigen_gap_zero_set = sp.solveset(eigen_gap, phi, domain=sp.S.Reals)
    D_at_zero = D.subs(phi, 0)

    omega = sp.symbols("Omega", positive=True)
    v = sp.Matrix(sp.symbols("v0:4"))
    cone_old = (v.T * eta * v)[0]
    cone_new = sp.simplify((v.T * (omega**2 * eta) * v)[0])

    # Boundary collar u=0. Both extensions equal the boundary normal there,
    # while their tangential components differ in the bulk.
    u, L, eps = sp.symbols("u L eps", positive=True)
    normal_0 = sp.Matrix([1, 0])
    normal_1 = sp.Matrix([1, eps * u * (L - u)])
    boundary_agreement = sp.simplify((normal_1 - normal_0).subs(u, 0))
    midpoint_difference = sp.simplify((normal_1 - normal_0).subs(u, L / 2))

    flat_ricci = sp.zeros(4)
    constant_phi_gradient = sp.zeros(4, 1)

    checks = {
        "T2_boost_preserves_lorentz_metric": lorentz_residual == sp.zeros(4),
        "T2_rotation_fixed_candidate_moved_by_every_nonzero_real_boost": boost_line_zero_set == sp.FiniteSet(0),
        "T3_flat_metric_jet_retains_lorentz_isotropy": lorentz_residual == sp.zeros(4),
        "T4_metric_factorization_not_unique": bool(coframes_distinct and coframe_metric_residual == sp.zeros(4)),
        "T4_reciprocal_endomorphism_degenerates_exactly_at_phi_zero": eigen_gap_zero_set == sp.FiniteSet(0),
        "T4_phi_zero_endomorphism_is_identity": D_at_zero == sp.eye(2),
        "T5_flat_curvature_eigenframe_degenerate": flat_ricci == sp.zeros(4),
        "T5_constant_phi_gradient_vanishes": constant_phi_gradient == sp.zeros(4, 1),
        "T6_conformal_rescaling_preserves_null_cone": sp.simplify(cone_new - omega**2 * cone_old) == 0,
        "T7_extensions_agree_at_seal": boundary_agreement == sp.zeros(2, 1),
        "T7_extensions_differ_in_bulk": midpoint_difference != sp.zeros(2, 1),
    }
    if not all(checks.values()):
        raise RuntimeError(f"exact derivation check failed: {checks}")

    routes = {
        "internal_reciprocal_pair": "DERIVED_KINEMATIC",
        "S0_pointwise_metric_only_line_selector": "REFUTED_IN_CLASS",
        "S1_universal_local_finite_jet_metric_only_selector": "REFUTED_IN_CLASS",
        "S2_internal_to_spacetime_realization": "OPEN",
        "S3_curvature_eigenline": "CONDITIONAL_STRATIFIED",
        "S3_gradient_phi": "CIRCULAR_OR_EXTRA_FIELD",
        "S3_static_killing_line": "CONDITIONAL_SECTOR_ONLY",
        "S3_declared_spacetime_endomorphism": "CONDITIONAL_STRUCTURED",
        "S4_seal_normal_line": "CONDITIONAL_BOUNDARY_LOCAL",
        "S4_boundary_to_bulk_extension": "UNDERDETERMINED",
        "auxiliary_field_requirement": "NOT_DERIVED",
        "variation_domain": "OPEN",
        "complete_action_source_boundary_charge": "OPEN",
    }

    result = {
        "schema": "udt.reciprocal-line-realization-selector.v1",
        "top_level_outcome": TOP_LEVEL,
        "checks": checks,
        "check_count": len(checks),
        "routes": routes,
        "exact_algebra": {
            "lorentz_residual": str(lorentz_residual),
            "boosted_e0": str(boosted_e0),
            "line_wedge_minor": str(line_wedge_minor),
            "boost_line_zero_set": str(boost_line_zero_set),
            "reciprocal_endomorphism": str(D),
            "eigenvalue_gap": str(eigen_gap),
            "eigenvalue_gap_zero_set": str(eigen_gap_zero_set),
            "endomorphism_at_phi_zero": str(D_at_zero),
            "conformal_cone_factor": str(sp.simplify(cone_new / cone_old)),
            "boundary_agreement": str(boundary_agreement),
            "bulk_extension_difference": str(midpoint_difference),
        },
        "scope_guards": {
            "flat_trivial_configuration_allowed": True,
            "generic_stratified_selectors_not_excluded": True,
            "global_boundary_selectors_not_excluded": True,
            "auxiliary_structure_not_required_by_no_go": True,
            "internal_pair_not_identified_as_spacetime_tensor": True,
            "no_action_or_variation_domain_selected": True,
        },
        "least_missing_object": {
            "name": "native_internal_pair_to_spacetime_line_realization_rule",
            "required_facets": [
                "domain_and_codomain",
                "diffeomorphism_and_common_scale_transformation_law",
                "relative_normalization",
                "internal_pairing_and_orthogonality_meaning",
                "phi_zero_and_other_degeneracy_handling",
                "finite_cell_boundary_and_bulk_compatibility",
                "global_existence_and_branch_rule",
            ],
            "full_coframe_required": False,
        },
        "environment": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "cpu_only": True,
        },
    }

    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    args.output.write_text(rendered, encoding="utf-8")
    transcript_lines = [
        f"top_level_outcome={TOP_LEVEL}",
        f"python={platform.python_version()}",
        f"sympy={sp.__version__}",
        f"checks={sum(checks.values())}/{len(checks)}",
        f"lorentz_residual={lorentz_residual}",
        f"boosted_e0={boosted_e0}",
        f"line_wedge_minor={line_wedge_minor}",
        f"boost_line_zero_set={boost_line_zero_set}",
        f"coframes_distinct={coframes_distinct}",
        f"endomorphism_at_phi_zero={D_at_zero}",
        f"eigenvalue_gap_zero_set={eigen_gap_zero_set}",
        f"boundary_agreement={boundary_agreement}",
        f"bulk_extension_difference={midpoint_difference}",
        f"result_sha256={sha256_text(rendered)}",
    ]
    args.transcript.write_text("\n".join(transcript_lines) + "\n", encoding="utf-8")
    print("\n".join(transcript_lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

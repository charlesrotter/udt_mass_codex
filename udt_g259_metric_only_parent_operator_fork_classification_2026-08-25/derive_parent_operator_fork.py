#!/usr/bin/env python3
"""Derive the bounded G259 metric-only parent-operator fork."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
LANDING = (
    "CONDITIONAL_LOVELOCK_CLASS_SELECTS_EINSTEIN_ZERO_SET"
    "__CLASS_ASSUMPTIONS_NOT_UDT_DERIVED"
    "__EXTREME_METRIC_DEPARTURE_REQUIRES_EXPLICIT_NEW_STRUCTURE"
    "__SOURCE_HISTORY_REMAINS_OPEN"
)


def main() -> None:
    r, t = sp.symbols("r t", positive=True)
    C, b, ell, lam = sp.symbols("C b ell lam", nonzero=True)
    f = sp.Function("f")(r)

    # Exact primary spherical GR-comparison residual replay.
    e0 = sp.expand(r * sp.diff(f, r) + f - 1)
    e1 = sp.expand(r * sp.diff(f, r) + r**2 * sp.diff(f, r, 2) / 2)
    dependence = sp.simplify(r * sp.diff(e0, r) - 2 * e1)
    assert dependence == 0

    f_gr = 1 + C / r
    assert sp.simplify(e0.subs(f, f_gr).doit()) == 0
    assert sp.simplify(e1.subs(f, f_gr).doit()) == 0

    # The arbitrary primary profile is equivalent algebraically to an arbitrary mass aspect
    # until a source or a vacuum condition is supplied.
    mu = sp.Function("mu")(r)
    f_mu = 1 - 2 * mu / r
    e0_mu = sp.simplify(e0.subs(f, f_mu).doit())
    e1_mu = sp.simplify(e1.subs(f, f_mu).doit())
    assert e0_mu == -2 * sp.diff(mu, r)
    assert e1_mu == -r * sp.diff(mu, r, 2)

    # A fourth-order, natural, divergence-free counteroperator from delta int R^2 sqrt(-g).
    # Evaluate it on g=-dt^2+a(t)^2 d x^2 with a=exp(b t^2).
    hubble = 2 * b * t
    hubble_dot = sp.diff(hubble, t)
    scalar_r = sp.expand(6 * (hubble_dot + 2 * hubble**2))
    ricci_00 = sp.expand(-3 * (hubble_dot + hubble**2))
    ricci_space = sp.expand(hubble_dot + 3 * hubble**2)  # coefficient of g_ij
    scalar_dot = sp.diff(scalar_r, t)
    scalar_ddot = sp.diff(scalar_r, t, 2)
    box_scalar = sp.expand(-scalar_ddot - 3 * hubble * scalar_dot)
    h_r2_00 = sp.expand(
        2 * scalar_r * ricci_00
        + scalar_r**2 / 2
        + 2 * (-box_scalar - scalar_ddot)
    )
    h_r2_space = sp.expand(
        2 * scalar_r * ricci_space
        - scalar_r**2 / 2
        + 2 * (box_scalar + hubble * scalar_dot)
    )
    divergence = sp.simplify(
        sp.diff(h_r2_00, t) + 3 * hubble * (h_r2_00 + h_r2_space)
    )
    assert divergence == 0
    assert sp.simplify(h_r2_00.subs(t, 0) + 72 * b**2) == 0
    assert sp.simplify(h_r2_space.subs(t, 0) + 216 * b**2) == 0

    einstein_00 = sp.expand(3 * hubble**2)
    einstein_space = sp.expand(-(2 * hubble_dot + 3 * hubble**2))
    extension_00 = sp.expand(einstein_00 + lam * ell**2 * h_r2_00)
    extension_space = sp.expand(einstein_space + lam * ell**2 * h_r2_space)
    assert sp.simplify(extension_00.subs(t, 0) + 72 * lam * ell**2 * b**2) == 0
    assert sp.simplify(extension_space.subs(t, 0) + 4 * b + 216 * lam * ell**2 * b**2) == 0

    # c_E^x G_obs^y cannot have pure length units without a mass/source attachment.
    x, y = sp.symbols("x y")
    unit_solution = sp.solve(
        (sp.Eq(x + 3 * y, 1), sp.Eq(-x - 2 * y, 0), sp.Eq(-y, 0)),
        (x, y),
        dict=True,
    )
    assert unit_solution == []

    # Twelve value knots leave derivative freedom. A node polynomial preserves every value and
    # changes the first derivative at every simple node.
    node_polynomial = sp.prod(r - sp.Integer(i) for i in range(1, 13))
    node_checks = 0
    for i in range(1, 13):
        assert node_polynomial.subs(r, i) == 0
        assert sp.diff(node_polynomial, r).subs(r, i) != 0
        node_checks += 2

    atlas = [
        {
            "class": "currently_owned_F1_F4_W1_W3",
            "status": "NO_PARENT_OPERATOR",
            "gr_quiet": "required_conditionally",
            "new_structure": "none",
            "scale": "none",
            "selection": "underdetermined",
        },
        {
            "class": "local_metric_only_second_order_divergence_free",
            "status": "CONDITIONAL_CLASS",
            "gr_quiet": "exact",
            "new_structure": "locality_second_order_rank2_divergence_free",
            "scale": "none_after_flat_quiet",
            "selection": "Einstein_vacuum_zero_set_for_nonzero_operator",
        },
        {
            "class": "local_metric_only_higher_derivative",
            "status": "UNOWNED_CLASS",
            "gr_quiet": "can_retain_Ricci_flat_branch",
            "new_structure": "higher_metric_derivatives_and_coefficient_law",
            "scale": "length_squared_for_Einstein_plus_R2",
            "selection": "nonunique",
        },
        {
            "class": "global_or_nonlocal_relation",
            "status": "UNOWNED_CLASS",
            "gr_quiet": "must_be_proved",
            "new_structure": "population_measure_and_global_operator",
            "scale": "possibly_global_or_integration",
            "selection": "open",
        },
        {
            "class": "extra_reciprocal_state",
            "status": "UNOWNED_CLASS",
            "gr_quiet": "must_be_proved",
            "new_structure": "covariant_pair_or_split_field",
            "scale": "not_automatically_fixed",
            "selection": "open",
        },
        {
            "class": "Einstein_metric_operator_plus_source_history",
            "status": "CONDITIONAL_FORK",
            "gr_quiet": "exact",
            "new_structure": "source_constitutive_and_population_law",
            "scale": "G_obs_requires_mass_or_density_attachment",
            "selection": "metric_operator_fixed_source_history_open",
        },
    ]
    with (ROOT / "CANDIDATE_CLASS_ATLAS.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=atlas[0].keys(), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(atlas)

    result = {
        "status": "PASS",
        "landing": LANDING,
        "mode": "METRIC_LED_OBSERVING_OPERATOR_CLASSIFICATION",
        "lovelock_method": {
            "dimension": 4,
            "basis": ["metric", "Einstein"],
            "basis_dimension": 2,
            "flat_quiet_removes_metric_term": True,
            "vacuum_zero_set_after_flat_quiet": "Einstein",
            "source_normalization_still_requires_attachment": True,
            "assumptions_owned_by_F1_F4_W1_W3": False,
            "theorem_scope_file": "LOVELOCK_NAVARRO_SCOPE.md",
            "zero_operator_excluded": True,
            "nonzero_coefficient_required": True,
        },
        "spherical_replay": {
            "E0": str(e0),
            "E1": str(e1),
            "dependence": str(dependence),
            "vacuum_family": "f=1+C/r",
            "mass_aspect_E0": str(e0_mu),
            "mass_aspect_E1": str(e1_mu),
        },
        "higher_order_counterfamily": {
            "operator": "Einstein_ab + lambda ell^2 H_R2_ab",
            "lambda_values_registered": [1, 2],
            "retains_every_Ricci_flat_metric": True,
            "H_R2_00_at_t0": str(h_r2_00.subs(t, 0)),
            "H_R2_space_at_t0": str(h_r2_space.subs(t, 0)),
            "identity_divergence_residual": str(divergence),
            "requires_new_length_squared_coefficient": True,
        },
        "dimension_audit": {
            "cE_and_Gobs_form_length": False,
            "mass_or_density_attachment_needed_for_length": True,
        },
        "G258_value_gate": {
            "node_count": 12,
            "value_preserving_derivative_changing_assertions": node_checks,
            "values_select_operator": False,
            "continuous_derivatives_or_source_required": True,
        },
        "metric_only_reciprocal_scalar": {
            "spherical_branch": "phi=-1/2 log(norm(grad areal_radius)^2)",
            "general_4d_without_pair_or_split": False,
        },
        "fit_coefficients": 0,
        "observational_values_used": 0,
        "gpu_used": False,
        "protected_inputs_used": 0,
        "open": [
            "ownership of locality second order rank2 and identity divergence freedom",
            "metric-dynamics GR fork versus modified parent operator",
            "source and matter law",
            "native transfer",
            "continuous time-live nonspherical history",
            "global relation population and completion",
            "X_max",
        ],
    }
    (ROOT / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(LANDING)
    print(f"candidate_classes={len(atlas)} node_assertions={node_checks}")
    print(f"H_R2_t0=({h_r2_00.subs(t, 0)},{h_r2_space.subs(t, 0)})")


if __name__ == "__main__":
    main()

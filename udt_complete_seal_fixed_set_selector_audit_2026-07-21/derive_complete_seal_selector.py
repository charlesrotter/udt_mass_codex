#!/usr/bin/env python3
"""Exact complete-seal lift, fixed-set, orientation, and jet-parity algebra."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def require(name: str, condition, checks: dict[str, str]) -> None:
    if not bool(condition):
        raise AssertionError(name)
    checks[name] = "PASS"


def require_zero(name: str, expression, checks: dict[str, str]) -> None:
    value = sp.simplify(expression)
    if isinstance(value, sp.MatrixBase):
        good = value == sp.zeros(*value.shape)
    else:
        good = value == 0
    require(name, good, checks)


def block_diagonal(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    output = sp.zeros(left.rows + right.rows)
    output[: left.rows, : left.cols] = left
    output[left.rows :, left.cols :] = right
    return output


def full_metric(base: sp.Matrix, cross: sp.Matrix, angular: sp.Matrix) -> sp.Matrix:
    return base.row_join(cross).col_join(cross.T.row_join(angular))


def symmetric_basis(dimension: int):
    basis = []
    for i in range(dimension):
        for j in range(i, dimension):
            matrix = sp.zeros(dimension)
            matrix[i, j] = 1
            matrix[j, i] = 1
            if i == j:
                matrix[i, j] = 1
            basis.append(matrix)
    return basis


def parity_dimensions(seal: sp.Matrix):
    even = 0
    odd = 0
    for basis in symmetric_basis(seal.rows):
        transformed = sp.simplify(seal.T * basis * seal)
        if transformed == basis:
            even += 1
        elif transformed == -basis:
            odd += 1
        else:
            raise AssertionError("basis is not seal-eigen in diagonal frame")
    return even, odd


def main() -> None:
    checks: dict[str, str] = {}
    identity2 = sp.eye(2)
    exchange = sp.Matrix([[0, 1], [1, 0]])
    axis = sp.diag(1, -1)
    base_seal = sp.diag(1, -1)
    eta = sp.diag(-1, 1, 1, 1)
    rotation45 = sp.sqrt(2) * sp.Matrix([[1, -1], [1, 1]]) / 2

    angular_lifts = {
        "PLUS_IDENTITY": identity2,
        "MINUS_IDENTITY": -identity2,
        "AXIS_REFLECTION": axis,
        "HOPF_EXCHANGE_LOCAL": exchange,
    }
    expected = {
        "PLUS_IDENTITY": {"fixed": 3, "anti": 1, "det": -1, "spatial_fixed": 2, "spatial_anti": 1},
        "MINUS_IDENTITY": {"fixed": 1, "anti": 3, "det": -1, "spatial_fixed": 0, "spatial_anti": 3},
        "AXIS_REFLECTION": {"fixed": 2, "anti": 2, "det": 1, "spatial_fixed": 1, "spatial_anti": 2},
        "HOPF_EXCHANGE_LOCAL": {"fixed": 2, "anti": 2, "det": 1, "spatial_fixed": 1, "spatial_anti": 2},
    }
    lift_results = {}
    for name, angular in angular_lifts.items():
        seal = block_diagonal(base_seal, angular)
        spatial = sp.diag(-1, 1, 1)
        spatial[1:, 1:] = angular
        fixed = 4 - (seal - sp.eye(4)).rank()
        anti = 4 - (seal + sp.eye(4)).rank()
        spatial_fixed = 3 - (spatial - sp.eye(3)).rank()
        spatial_anti = 3 - (spatial + sp.eye(3)).rank()
        require_zero(f"{name}_involution", seal**2 - sp.eye(4), checks)
        require_zero(f"{name}_canonical_isometry", seal.T * eta * seal - eta, checks)
        require(f"{name}_fixed_count", fixed == expected[name]["fixed"], checks)
        require(f"{name}_anti_count", anti == expected[name]["anti"], checks)
        require(f"{name}_dimension_partition", fixed + anti == 4, checks)
        require(f"{name}_determinant", sp.det(seal) == expected[name]["det"], checks)
        require(f"{name}_determinant_from_anti", sp.det(seal) == (-1) ** anti, checks)
        require(f"{name}_time_orientation", seal[0, 0] == 1, checks)
        require(f"{name}_radial_normal_reversed", seal[1, 1] == -1, checks)
        require(f"{name}_spatial_fixed_count", spatial_fixed == expected[name]["spatial_fixed"], checks)
        require(f"{name}_spatial_anti_count", spatial_anti == expected[name]["spatial_anti"], checks)
        lift_results[name] = {
            **expected[name],
            "fixed_set_codimension_if_pointwise_isometry": anti,
            "time_orientation_preserved": True,
            "radial_normal_reversed": True,
            "admits_seal_local_second_pair": name in ("AXIS_REFLECTION", "HOPF_EXCHANGE_LOCAL"),
        }

    # The two reflection lifts are the same local O(2) conjugacy class.
    require_zero("axis_and_Hopf_exchange_are_orthogonally_conjugate", rotation45.T * exchange * rotation45 - axis, checks)
    require("reflection_lifts_not_identical_in_registered_basis", axis != exchange, checks)

    # Exact conditional selectors.
    require(
        "pointwise_codimension_one_selects_plus_identity",
        [name for name, row in lift_results.items() if row["anti"] == 1] == ["PLUS_IDENTITY"],
        checks,
    )
    require(
        "orientation_preserving_leaves_two_reflection_lifts",
        {name for name, row in lift_results.items() if row["det"] == 1}
        == {"AXIS_REFLECTION", "HOPF_EXCHANGE_LOCAL"},
        checks,
    )
    require(
        "orientation_reversing_leaves_two_identity_lifts",
        {name for name, row in lift_results.items() if row["det"] == -1}
        == {"PLUS_IDENTITY", "MINUS_IDENTITY"},
        checks,
    )
    require(
        "time_orientation_does_not_select",
        all(row["time_orientation_preserved"] for row in lift_results.values()),
        checks,
    )
    require(
        "single_reversed_spatial_normal_selects_plus_identity",
        [name for name, row in lift_results.items() if row["spatial_anti"] == 1] == ["PLUS_IDENTITY"],
        checks,
    )

    # Ordinary pointwise mirror parity: an even tangential metric has zero
    # first normal jet. Current UDT instead permits a nonzero odd phi slope.
    n, h0, h1, a = sp.symbols("n h0 h1 a", real=True)
    tangential_component = h0 + h1 * n
    require(
        "ordinary_pointwise_mirror_forces_tangential_first_jet_zero",
        sp.solve(
            sp.Poly(tangential_component - tangential_component.subs(n, -n), n).coeffs(),
            h1,
            dict=True,
        )
        == [{h1: 0}],
        checks,
    )
    reciprocal_clock = -sp.exp(-2 * a * n)
    require_zero("reciprocal_clock_value_at_seal", reciprocal_clock.subs(n, 0) + 1, checks)
    require_zero("reciprocal_clock_normal_derivative", sp.diff(reciprocal_clock, n).subs(n, 0) - 2 * a, checks)
    require("free_nonzero_phi_slope_not_ordinary_even_tangential_metric", (2 * a).subs(a, 1) != 0, checks)

    # Complete first-jet parity for a supplied full involutive isometry. In a
    # seal eigenframe, even symmetric jets live within equal-parity blocks and
    # odd jets live between fixed and anti-fixed blocks.
    jet_results = {}
    for name, row in lift_results.items():
        diagonal_seal = sp.diag(*([1] * row["fixed"] + [-1] * row["anti"]))
        even, odd = parity_dimensions(diagonal_seal)
        expected_even = row["fixed"] * (row["fixed"] + 1) // 2 + row["anti"] * (row["anti"] + 1) // 2
        expected_odd = row["fixed"] * row["anti"]
        require(f"{name}_even_metric_jet_dimension", even == expected_even, checks)
        require(f"{name}_odd_metric_jet_dimension", odd == expected_odd, checks)
        require(f"{name}_symmetric_jet_complete", even + odd == 10, checks)
        jet_results[name] = {"even_symmetric_dimension": even, "odd_symmetric_dimension": odd}

    # Nonzero-cross complete Lorentz witnesses preserve every lift's isometry,
    # orientation, and eigenspace multiplicity at both registered mu values.
    epsilon = sp.Rational(1, 10)
    witness_cross = {
        "PLUS_IDENTITY": sp.Matrix([[epsilon, epsilon], [epsilon, epsilon]]),
        "MINUS_IDENTITY": sp.Matrix([[epsilon, epsilon], [-epsilon, -epsilon]]),
        "AXIS_REFLECTION": sp.Matrix([[epsilon, epsilon], [epsilon, -epsilon]]),
        "HOPF_EXCHANGE_LOCAL": sp.Matrix([[epsilon, epsilon], [epsilon, epsilon]]),
    }
    nonzero_cross_results = {}
    for name, angular in angular_lifts.items():
        full_seal = block_diagonal(exchange, angular)
        for k in (2, 3):
            base = sp.Matrix([[1, -k], [-k, 1]])
            metric = full_metric(base, witness_cross[name], identity2)
            schur = sp.simplify(identity2 - witness_cross[name].T * base.inv() * witness_cross[name])
            require_zero(f"{name}_MU{k*k}_full_isometry", full_seal.T * metric * full_seal - metric, checks)
            require(f"{name}_MU{k*k}_Lorentz_base", sp.det(base) < 0, checks)
            require(f"{name}_MU{k*k}_positive_screen_first_minor", schur[0, 0] > 0, checks)
            require(f"{name}_MU{k*k}_positive_screen_determinant", sp.det(schur) > 0, checks)
            require(f"{name}_MU{k*k}_orientation_unchanged", sp.det(full_seal) == expected[name]["det"], checks)
            require(
                f"{name}_MU{k*k}_fixed_multiplicity_unchanged",
                4 - (full_seal - sp.eye(4)).rank() == expected[name]["fixed"],
                checks,
            )
            nonzero_cross_results[f"{name}_MU{k*k}"] = {
                "determinant": str(sp.factor(sp.det(metric))),
                "fixed": expected[name]["fixed"],
                "anti": expected[name]["anti"],
                "orientation": expected[name]["det"],
                "status": "EXACT_NONZERO_CROSS_LORENTZ_WITNESS",
            }

    # An orientable metric does not require every isometry to preserve
    # orientation; the canonical spatial mirror itself is an exact isometry of
    # oriented Minkowski space with determinant -1.
    canonical_mirror = sp.diag(1, -1, 1, 1)
    require_zero("orientation_reversing_isometry_exists_on_orientable_metric", canonical_mirror.T * eta * canonical_mirror - eta, checks)
    require("orientation_reversing_isometry_determinant", sp.det(canonical_mirror) == -1, checks)

    output = {
        "schema": "udt-complete-seal-fixed-set-selector-derivation-1.0",
        "maximum_conclusion": "UDT_COMPLETE_SEAL_FIXED_SET_SELECTOR_STATUS_CHARACTERIZED",
        "check_count": len(checks),
        "checks": dict(sorted(checks.items())),
        "outcomes": [
            "COMPLETE_LIFT_REMAINS_OPEN_BECAUSE_SEAL_POINTWISE_ACTION_IS_UNDERDETERMINED",
            "PLUS_IDENTITY_SELECTED_ONLY_IF_POINTWISE_CODIMENSION_ONE_METRIC_MIRROR_IS_ADDED",
            "CURRENT_ODD_PHI_FOLD_DOES_NOT_SUPPLY_ORDINARY_POINTWISE_METRIC_MIRROR",
            "ORIENTATION_PRESERVATION_IS_NOT_DERIVED_AND_WOULD_LEAVE_TWO_REFLECTION_LIFTS",
            "TIME_ORIENTATION_PRESERVES_ALL_FOUR_LIFTS",
            "AXIS_AND_HOPF_REFLECTIONS_ARE_LOCALLY_CONJUGATE",
            "NONZERO_CROSS_COUPLING_DOES_NOT_CHANGE_FIXED_SET_CLASSIFICATION",
            "REFLECTION_SEAL_TWO_PAIR_ROUTE_REMAINS_CONDITIONAL_ON_EXTRA_ANGULAR_IDENTIFICATION",
        ],
        "lift_results": lift_results,
        "metric_jet_parity": jet_results,
        "nonzero_cross_witnesses": nonzero_cross_results,
        "conditional_rulings": {
            "pointwise_codimension_one_fixed_hypersurface": "PLUS_IDENTITY_ONLY",
            "orientation_preserving_involution": "AXIS_REFLECTION_OR_HOPF_EXCHANGE_LOCAL",
            "orientation_reversing_involution": "PLUS_IDENTITY_OR_MINUS_IDENTITY",
            "time_orientation_preserving": "ALL_FOUR",
            "current_static_phi_odd_fold": "NO_COMPLETE_LIFT_SELECTION",
        },
        "authority": {
            "canonized": "phi is odd at the seal; phi=0 there; normal derivative is free",
            "not_supplied": "pointwise full-metric fixation, complete angular/time-on action, induced metric parity, normal jet, orientation law, or angular quotient",
            "ordinary_mirror_warning": "a pointwise metric mirror would force even tangential first jets and is not derivable from the current scalar fold wording",
        },
        "two_pair_consequence": {
            "reflection_lifts": "admit the parent seal-local complementary pair",
            "identity_lifts": "forbid a nonzero anticommuting angular pair",
            "selection": "OPEN; the desired second pair cannot be used to select its own lift",
        },
        "smallest_missing_join": {
            "question": "Is the phi-odd finite-cell fold accompanied by a separately derived non-pointwise angular identification, and if so which one?",
            "status": "OPEN",
        },
        "scope": {
            "complete": "four registered constant angular lifts, their fixed-set/orientation classes, symmetric first-jet parity, and eight nonzero-cross witnesses",
            "not_covered": [
                "field-dependent angular seal actions",
                "global quotient periods caps and topology",
                "bulk transport holonomy or dynamics",
                "boundary action polarization and charge",
                "carrier source mass scale and canonization",
            ],
        },
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

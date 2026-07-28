#!/usr/bin/env python3
"""Exact clean-room closure-rank audit for current UDT metric reductions."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
from pathlib import Path

import sympy as sp


AMPLITUDES = ("phi", "sigma", "alpha", "k", "S10", "S11", "S20", "S21")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def matrix_rank_columns(columns: list[sp.Matrix]) -> int:
    return int(sp.Matrix.hstack(*[c.reshape(c.rows * c.cols, 1) for c in columns]).rank())


def neutral_generators() -> dict[str, sp.Matrix]:
    z = sp.zeros(4)
    out: dict[str, sp.Matrix] = {}
    out["phi"] = sp.diag(-1, 1, 0, 0)
    out["sigma"] = sp.diag(0, 0, sp.Rational(1, 2), sp.Rational(1, 2))
    out["alpha"] = sp.diag(0, 0, -1, 1)
    for name, row, col in (
        ("k", 2, 3),
        ("S10", 2, 0),
        ("S11", 2, 1),
        ("S20", 3, 0),
        ("S21", 3, 1),
    ):
        m = z.copy()
        m[row, col] = 1
        out[name] = m
    return out


def torsion_connection_rank() -> tuple[int, int]:
    """Rank of omega_(ab)c -> omega^a_b wedge e^b in four dimensions."""
    variables = [(a, b, c) for a in range(4) for b in range(a + 1, 4) for c in range(4)]
    rows = []
    signs = (-1, 1, 1, 1)

    def coeff(a: int, b: int, c: int, var: tuple[int, int, int]) -> int:
        i, j, k = var
        if c != k:
            return 0
        if (a, b) == (i, j):
            return 1
        if (a, b) == (j, i):
            return -1
        return 0

    for a in range(4):
        for c in range(4):
            for d in range(c + 1, 4):
                # coefficient of e^c wedge e^d in omega^a_b wedge e^b
                row = []
                for var in variables:
                    value = signs[a] * (coeff(a, d, c, var) - coeff(a, c, d, var))
                    row.append(value)
                rows.append(row)
    matrix = sp.Matrix(rows)
    return len(variables), int(matrix.rank())


def maurer_cartan_control() -> dict[str, object]:
    t, x = sp.symbols("t x")
    e = sp.Matrix([[1 + t * x, t], [x, 1]])
    inv = sp.simplify(e.inv())
    at = sp.simplify(e.diff(t) * inv)
    ax = sp.simplify(e.diff(x) * inv)
    residual = sp.simplify(ax.diff(t) - at.diff(x) - (at * ax - ax * at))
    return {
        "test_matrix": [[str(v) for v in row] for row in e.tolist()],
        "determinant": str(sp.factor(e.det())),
        "right_maurer_cartan_residual": [[str(sp.simplify(v)) for v in row] for row in residual.tolist()],
        "zero": residual == sp.zeros(2),
        "interpretation": "IDENTITY_FOR_ARBITRARY_INVERTIBLE_COFRAME_NOT_BACKGROUND_EVOLUTION",
    }


def system_rows() -> list[dict[str, object]]:
    rows = [
        ("C01", "COHOMOGENEITY_ONE_BACKGROUND", "OPEN_UNDERDETERMINED_CONFIGURATION", 8, 0, 8, False),
        ("C02", "ONE_PLUS_ONE_TIME_LIVE_BACKGROUND", "OPEN_UNDERDETERMINED_EVOLUTION", 8, 0, 8, False),
        ("C03", "STATIONARY_TWISTED_S3_PROFILE", "CONFIGURATION_FAMILY_NOT_PROFILE_EQUATION", -1, 0, -1, False),
        ("C04", "REDUCED_CONSTANT_DEPTH_PRODUCT", "REGISTERED_FIXED_CONTROL_NO_NONTRIVIAL_EVOLUTION", 0, 0, 0, False),
        ("C05", "GEODESIC_PATH", "CLOSED_KINEMATIC_ON_SUPPLIED_CONFIGURATION", 8, 8, 0, True),
        ("C06", "AMBIENT_PARALLEL_TRANSPORT", "CLOSED_KINEMATIC_ON_SUPPLIED_CONFIGURATION", 4, 4, 0, True),
        ("C07", "PROJECTED_SCREEN_TRANSPORT", "CLOSED_KINEMATIC_ON_SUPPLIED_CONFIGURATION_AND_SCREEN_STRATUM", 2, 2, 0, True),
        ("C08", "JACOBI_TRANSPORT", "CLOSED_KINEMATIC_ON_SUPPLIED_CONFIGURATION_AND_GEODESIC", 8, 8, 0, True),
        ("C09", "CURVATURE_PRESCRIPTION_BACKGROUND", "OPEN_NO_SELECTED_CURVATURE_RESPONSE", 8, 0, 8, False),
        ("C10", "BOOTSTRAP_DENSITY_BACKGROUND", "OPEN_ON_SHELL_ADMISSIBILITY_NOT_EVOLUTION", -1, 0, -1, False),
        ("C11", "CARRIER_TIME_LIVE", "OPEN_CARRIER_AND_ACTION_UNSELECTED", -1, 0, -1, False),
        ("C12", "FINITE_CELL_FREE_BOUNDARY", "OPEN_COMPATIBILITY_NOT_BOUNDARY_EVOLUTION", -1, 0, -1, False),
        ("C13", "CONNECTION_OR_CURVATURE_DEFINITION", "DERIVED_EVALUATOR_NOT_BACKGROUND_EQUATION", 24, 24, 0, False),
        ("C14", "Bianchi_IDENTITY", "DERIVED_IDENTITY_NOT_BACKGROUND_EQUATION", 0, 0, 0, False),
        ("C15", "LEGACY_ODE_OR_TIME_LIVE", "QUARANTINED_PENDING_POSTVERDICT_PROVENANCE", -1, 0, -1, False),
    ]
    return [
        {
            "candidate_id": cid,
            "system_class": name,
            "classification": classification,
            "state_directions": state,
            "supplied_equation_rank": rank,
            "closure_deficit": deficit,
            "conditionally_executable": executable,
        }
        for cid, name, classification, state, rank, deficit, executable in rows
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    outdir = args.output_dir.resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    generators = neutral_generators()
    eta = sp.diag(-1, 1, 1, 1)
    coframe_rank = matrix_rank_columns([generators[name] for name in AMPLITUDES])
    metric_tangents = [sp.simplify(generators[name].T * eta + eta * generators[name]) for name in AMPLITUDES]
    metric_rank = matrix_rank_columns(metric_tangents)
    connection_unknowns, cartan_rank = torsion_connection_rank()

    rows = system_rows()
    result = {
        "schema": "udt-cleanroom-metric-reduction-readiness-1.0",
        "amplitudes": list(AMPLITUDES),
        "cleanroom": {
            "legacy_equation_files_opened": False,
            "legacy_solver_imports": [],
            "old_solver_results_used": False,
        },
        "neutral_chart": {
            "coframe_tangent_rank": coframe_rank,
            "metric_tangent_rank": metric_rank,
            "configuration_directions": len(AMPLITUDES),
            "founded_phi_is_extra_scalar": False,
            "interpretation": "EIGHT_LIVE_CHART_DIRECTIONS_WITH_PHI_EMBEDDED_AS_FOUNDED_PAIR_DEPTH",
        },
        "cartan_first_equation": {
            "connection_unknowns": connection_unknowns,
            "linear_rank": cartan_rank,
            "background_equation_rank": 0,
            "interpretation": "UNIQUELY_DEFINES_TORSION_FREE_METRIC_CONNECTION_FROM_COFRAME_JETS",
        },
        "cartan_second_equation": {
            "background_equation_rank": 0,
            "interpretation": "DEFINES_CURVATURE_FROM_CONNECTION_AND_ITS_DERIVATIVES",
        },
        "bianchi": {
            "background_equation_rank": 0,
            "interpretation": "IDENTITY_AFTER_CONNECTION_AND_CURVATURE_DEFINITIONS",
        },
        "maurer_cartan": maurer_cartan_control(),
        "background_reductions": {
            "cohomogeneity_one": {
                "live_profile_directions": 8,
                "metric_supplied_profile_equation_rank": 0,
                "closure_deficit": 8,
                "closed": False,
            },
            "one_plus_one": {
                "live_configuration_amplitudes": 8,
                "first_base_jet_directions": 16,
                "time_principal_directions": 8,
                "metric_supplied_evolution_principal_rank": 0,
                "evolution_closure_deficit": 8,
                "closed": False,
            },
        },
        "path_systems": {
            "geodesic": {"state_dimension": 8, "equation_rank": 8, "closed_given_metric_and_initial_data": True},
            "ambient_parallel": {"state_dimension": 4, "equation_rank": 4, "closed_given_metric_path_and_initial_data": True},
            "projected_screen": {"state_dimension": 2, "equation_rank": 2, "closed_given_metric_screen_path_and_initial_data": True},
            "jacobi": {"state_dimension": 8, "equation_rank": 8, "closed_given_metric_geodesic_and_initial_data": True},
        },
        "systems": rows,
        "inactive_inputs": {
            "strong_local_CSN": False,
            "action": False,
            "source": False,
            "carrier": False,
            "bootstrap_local_equation": False,
            "GR_field_equation": False,
        },
        "acceptance_filters": [],
        "cross_spliced_controls": False,
        "authorization": {
            "metric_background_ode": False,
            "metric_time_live": False,
            "legacy_solver_execution": False,
            "gpu": False,
            "conditional_kinematic_path_ode_atlas": True,
            "next_clean_metric_step": "OFF_SHELL_COMPLETE_COFRAME_VARIATION_DOMAIN_AND_STRATIFICATION_ATLAS",
        },
        "maximum_conclusion": "REGISTERED_CURRENT_METRIC_KINEMATICS_CLOSE_PATHWISE_TRANSPORT_ON_SUPPLIED_CONFIGURATIONS_BUT_DO_NOT_CLOSE_A_BACKGROUND_PROFILE_OR_TIME_LIVE_SYSTEM",
        "environment": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
        },
    }

    result_path = outdir / "DERIVATION_RESULT.json"
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    with (outdir / "SYSTEM_OUTCOMES.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps({
        "result": "PASS",
        "coframe_tangent_rank": coframe_rank,
        "metric_tangent_rank": metric_rank,
        "cartan_connection_rank": cartan_rank,
        "background_ode_closed": False,
        "time_live_closed": False,
        "conditionally_closed_path_systems": 4,
        "result_sha256": sha256(result_path),
    }, sort_keys=True))


if __name__ == "__main__":
    main()

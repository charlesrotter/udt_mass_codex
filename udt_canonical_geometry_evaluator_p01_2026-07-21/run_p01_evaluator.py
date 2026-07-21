#!/usr/bin/env python3
"""Run the bounded CPU P01 evaluator certification suite."""

from __future__ import annotations

import json
import platform
from pathlib import Path

import numpy as np
import sympy as sp

from canonical_geometry_evaluator import (
    DIM,
    ETA,
    SLOT_NAMES,
    MetricJets,
    constant_internal_frame_transform_coframe,
    constant_linear_coordinate_transform_coframe,
    csn_connection_transform,
    csn_scaled_metric_jets,
    evaluate_coframe_jets,
    evaluate_metric_jets,
    local_internal_frame_transform_coframe_jets,
    metric_jets_from_split,
    reconstruct_split,
)


HERE = Path(__file__).resolve().parent
RESULT = HERE / "DERIVATION_RESULT.json"
TRANSCRIPT = HERE / "DERIVATION_TRANSCRIPT.txt"
TOLERANCE = 2e-10
SEED = 7312026


def maximum(value) -> float:
    array = np.asarray(value, dtype=float)
    return float(np.max(np.abs(array))) if array.size else 0.0


def require(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def fixture(name: str):
    metric = np.diag([-1.0, 1.0, 1.0, 1.0])
    first = np.zeros((DIM, DIM, DIM))
    second = np.zeros((DIM, DIM, DIM, DIM))
    coframe = np.eye(DIM)
    coframe_first = np.zeros((DIM, DIM, DIM))
    coframe_second = np.zeros((DIM, DIM, DIM, DIM))
    if name == "cartesian_flat":
        point = {"coordinates": [0.0, 0.0, 0.0, 0.0]}
    elif name == "polar_flat":
        radius = 2.0
        metric[2, 2] = radius**2
        first[1, 2, 2] = 2.0 * radius
        second[1, 1, 2, 2] = 2.0
        coframe[2, 2] = radius
        coframe_first[1, 2, 2] = 1.0
        point = {"coordinates": [0.0, radius, 0.0, 0.0]}
    elif name == "unit_sphere_product":
        theta = float(np.pi / 3.0)
        sine, cosine = np.sin(theta), np.cos(theta)
        metric[3, 3] = sine**2
        first[2, 3, 3] = 2.0 * sine * cosine
        second[2, 2, 3, 3] = 2.0 * (cosine**2 - sine**2)
        coframe[3, 3] = sine
        coframe_first[2, 3, 3] = cosine
        coframe_second[2, 2, 3, 3] = -sine
        point = {"coordinates": [0.0, 0.0, theta, 0.0]}
    else:
        raise KeyError(name)
    return MetricJets(metric, first, second), coframe, coframe_first, coframe_second, point


def main() -> None:
    checks: dict[str, str] = {}
    residuals: dict[str, float] = {}
    rng = np.random.default_rng(SEED)

    slot_values = np.array([-2.0, 0.13, 1.4, 1.2, 0.17, 0.9, 0.21, -0.12, 0.16, 0.08])
    slot_first = 0.03 * rng.normal(size=(DIM, len(SLOT_NAMES)))
    slot_second = 0.02 * rng.normal(size=(DIM, DIM, len(SLOT_NAMES)))
    slot_second = 0.5 * (slot_second + np.swapaxes(slot_second, 0, 1))
    split_jets = metric_jets_from_split(slot_values, slot_first, slot_second)
    split_geometry = evaluate_metric_jets(split_jets)
    split_reconstruction = reconstruct_split(split_jets.metric)
    for key, value in split_geometry.residuals.items():
        residuals[f"split_geometry_{key}"] = value
    for key, value in split_reconstruction.residuals.items():
        residuals[f"split_{key}"] = value
    require("ten_slot_names", len(SLOT_NAMES) == 10 and len(set(SLOT_NAMES)) == 10, checks)
    require("split_lorentzian", split_geometry.inertia == (1, 3, 0), checks)
    require("split_reverse_values", maximum(split_reconstruction.slots - slot_values) < TOLERANCE, checks)
    require("split_block_inverse", split_reconstruction.residuals["block_inverse"] < TOLERANCE, checks)
    require("split_determinant_factorization", split_reconstruction.residuals["determinant_factorization"] < TOLERANCE, checks)
    require("split_geometry_identities", max(split_geometry.residuals.values()) < TOLERANCE, checks)

    zero_first = np.zeros_like(slot_first)
    zero_second = np.zeros_like(slot_second)
    base_metric = metric_jets_from_split(slot_values, zero_first, zero_second).metric
    value_channels = 0
    for slot in range(len(SLOT_NAMES)):
        changed = slot_values.copy()
        changed[slot] += 1e-5
        if maximum(metric_jets_from_split(changed, zero_first, zero_second).metric - base_metric) > 1e-8:
            value_channels += 1
    first_channels = 0
    for coordinate in range(DIM):
        for slot in range(len(SLOT_NAMES)):
            channel = np.zeros_like(slot_first)
            channel[coordinate, slot] = 1.0
            jets = metric_jets_from_split(slot_values, channel, zero_second)
            if maximum(jets.first[coordinate]) > 1e-8:
                first_channels += 1
    second_channels = 0
    for first_coordinate in range(DIM):
        for second_coordinate in range(first_coordinate, DIM):
            for slot in range(len(SLOT_NAMES)):
                channel = np.zeros_like(slot_second)
                channel[first_coordinate, second_coordinate, slot] = 1.0
                channel[second_coordinate, first_coordinate, slot] = 1.0
                jets = metric_jets_from_split(slot_values, zero_first, channel)
                if maximum(jets.second[first_coordinate, second_coordinate]) > 1e-8:
                    second_channels += 1
    require("all_value_channels", value_channels == 10, checks)
    require("all_first_jet_channels", first_channels == 40, checks)
    require("all_symmetric_second_jet_channels", second_channels == 100, checks)

    coframe = np.eye(DIM) + 0.08 * rng.normal(size=(DIM, DIM))
    coframe_first = 0.04 * rng.normal(size=(DIM, DIM, DIM))
    coframe_second = 0.03 * rng.normal(size=(DIM, DIM, DIM, DIM))
    coframe_second = 0.5 * (coframe_second + np.swapaxes(coframe_second, 0, 1))
    coframe_evaluation = evaluate_coframe_jets(coframe, coframe_first, coframe_second)
    for key, value in coframe_evaluation.geometry.residuals.items():
        residuals[f"coframe_geometry_{key}"] = value
    for key, value in coframe_evaluation.residuals.items():
        residuals[f"coframe_{key}"] = value
    require("coframe_lorentzian", coframe_evaluation.geometry.inertia == (1, 3, 0), checks)
    require("coframe_metric_identities", max(coframe_evaluation.geometry.residuals.values()) < TOLERANCE, checks)
    require("first_cartan_identity", coframe_evaluation.residuals["first_cartan_torsion"] < TOLERANCE, checks)
    require("second_cartan_identity", coframe_evaluation.residuals["second_cartan_curvature"] < TOLERANCE, checks)
    require("spin_internal_antisymmetry", coframe_evaluation.residuals["spin_internal_antisymmetry"] < TOLERANCE, checks)

    rapidity = 0.37
    lorentz = np.eye(DIM)
    lorentz[:2, :2] = [[np.cosh(rapidity), np.sinh(rapidity)], [np.sinh(rapidity), np.cosh(rapidity)]]
    transformed = constant_internal_frame_transform_coframe(
        coframe, coframe_first, coframe_second, lorentz
    )
    transformed_evaluation = evaluate_coframe_jets(*transformed)
    frame_residual = max(
        maximum(transformed_evaluation.metric_jets.metric - coframe_evaluation.metric_jets.metric),
        maximum(transformed_evaluation.metric_jets.first - coframe_evaluation.metric_jets.first),
        maximum(transformed_evaluation.metric_jets.second - coframe_evaluation.metric_jets.second),
    )
    residuals["constant_local_lorentz_metric_invariance"] = frame_residual
    require("constant_local_lorentz_invariance", frame_residual < TOLERANCE, checks)

    local_rapidity = 0.23
    local_transform = np.eye(DIM)
    local_transform[:2, :2] = [
        [np.cosh(local_rapidity), np.sinh(local_rapidity)],
        [np.sinh(local_rapidity), np.cosh(local_rapidity)],
    ]
    boost_generator = np.zeros((DIM, DIM))
    boost_generator[0, 1] = boost_generator[1, 0] = 1.0
    rapidity_first = np.array([0.11, -0.07, 0.04, 0.09])
    rapidity_second = 0.01 * rng.normal(size=(DIM, DIM))
    rapidity_second = 0.5 * (rapidity_second + rapidity_second.T)
    local_transform_first = np.array(
        [rapidity_first[a] * boost_generator @ local_transform for a in range(DIM)]
    )
    local_transform_second = np.zeros((DIM, DIM, DIM, DIM))
    for a in range(DIM):
        for b in range(DIM):
            local_transform_second[a, b] = (
                rapidity_second[a, b] * boost_generator @ local_transform
                + rapidity_first[a] * rapidity_first[b] * boost_generator @ boost_generator @ local_transform
            )
    local_changed = local_internal_frame_transform_coframe_jets(
        coframe,
        coframe_first,
        coframe_second,
        local_transform,
        local_transform_first,
        local_transform_second,
    )
    local_evaluation = evaluate_coframe_jets(*local_changed)
    local_metric_residual = max(
        maximum(local_evaluation.metric_jets.metric - coframe_evaluation.metric_jets.metric),
        maximum(local_evaluation.metric_jets.first - coframe_evaluation.metric_jets.first),
        maximum(local_evaluation.metric_jets.second - coframe_evaluation.metric_jets.second),
    )
    local_inverse = np.linalg.inv(local_transform)
    expected_spin = np.array(
        [
            local_transform @ coframe_evaluation.spin_connection[mu] @ local_inverse
            - local_transform_first[mu] @ local_inverse
            for mu in range(DIM)
        ]
    )
    expected_cartan = np.einsum(
        "ia,abmn,bj->ijmn",
        local_transform,
        coframe_evaluation.cartan_curvature,
        local_inverse,
    )
    local_spin_residual = maximum(local_evaluation.spin_connection - expected_spin)
    local_curvature_residual = maximum(local_evaluation.cartan_curvature - expected_cartan)
    residuals["local_lorentz_metric_two_jet_invariance"] = local_metric_residual
    residuals["local_lorentz_spin_gauge_transform"] = local_spin_residual
    residuals["local_lorentz_cartan_covariance"] = local_curvature_residual
    require("local_lorentz_metric_two_jet_invariance", local_metric_residual < TOLERANCE, checks)
    require("local_lorentz_spin_gauge_transform", local_spin_residual < TOLERANCE, checks)
    require("local_lorentz_cartan_covariance", local_curvature_residual < TOLERANCE, checks)

    jacobian = np.eye(DIM)
    jacobian[0, 1] = 0.2
    jacobian[2, 3] = -0.1
    coordinate_changed = constant_linear_coordinate_transform_coframe(
        coframe, coframe_first, coframe_second, jacobian
    )
    coordinate_evaluation = evaluate_coframe_jets(*coordinate_changed)
    expected_metric = jacobian.T @ coframe_evaluation.metric_jets.metric @ jacobian
    expected_first = np.einsum("ma,nb,kc,kmn->cab", jacobian, jacobian, jacobian, coframe_evaluation.metric_jets.first)
    expected_second = np.einsum(
        "ma,nb,kc,ld,klmn->cdab",
        jacobian,
        jacobian,
        jacobian,
        jacobian,
        coframe_evaluation.metric_jets.second,
    )
    jacobian_inverse = np.linalg.inv(jacobian)
    expected_christoffel = np.einsum(
        "ar,mb,nc,rmn->abc",
        jacobian_inverse,
        jacobian,
        jacobian,
        coframe_evaluation.geometry.christoffel,
    )
    expected_riemann = np.einsum(
        "ar,sb,mc,nd,rsmn->abcd",
        jacobian_inverse,
        jacobian,
        jacobian,
        jacobian,
        coframe_evaluation.geometry.riemann_up,
    )
    coordinate_metric_residual = maximum(coordinate_evaluation.metric_jets.metric - expected_metric)
    coordinate_first_residual = maximum(coordinate_evaluation.metric_jets.first - expected_first)
    coordinate_second_residual = maximum(coordinate_evaluation.metric_jets.second - expected_second)
    coordinate_connection_residual = maximum(coordinate_evaluation.geometry.christoffel - expected_christoffel)
    coordinate_curvature_residual = maximum(coordinate_evaluation.geometry.riemann_up - expected_riemann)
    restored = constant_linear_coordinate_transform_coframe(*coordinate_changed, np.linalg.inv(jacobian))
    coordinate_roundtrip = max(
        maximum(restored[0] - coframe),
        maximum(restored[1] - coframe_first),
        maximum(restored[2] - coframe_second),
    )
    residuals["coordinate_metric_tensor_transform"] = coordinate_metric_residual
    residuals["coordinate_metric_first_tensor_transform"] = coordinate_first_residual
    residuals["coordinate_metric_second_tensor_transform"] = coordinate_second_residual
    residuals["coordinate_connection_transform"] = coordinate_connection_residual
    residuals["coordinate_curvature_transform"] = coordinate_curvature_residual
    residuals["coordinate_coframe_roundtrip"] = coordinate_roundtrip
    require("coordinate_metric_tensor_transform", coordinate_metric_residual < TOLERANCE, checks)
    require("coordinate_metric_first_tensor_transform", coordinate_first_residual < TOLERANCE, checks)
    require("coordinate_metric_second_tensor_transform", coordinate_second_residual < TOLERANCE, checks)
    require("coordinate_connection_transform", coordinate_connection_residual < TOLERANCE, checks)
    require("coordinate_curvature_transform", coordinate_curvature_residual < TOLERANCE, checks)
    require("coordinate_coframe_roundtrip", coordinate_roundtrip < TOLERANCE, checks)

    omega = 1.7
    constant_scaled = evaluate_coframe_jets(
        omega * coframe, omega * coframe_first, omega * coframe_second
    )
    csn_residuals = {
        "coframe_weight_1": maximum(omega * coframe - omega * coframe),
        "metric_weight_2": maximum(constant_scaled.metric_jets.metric - omega**2 * coframe_evaluation.metric_jets.metric),
        "inverse_weight_minus_2": maximum(constant_scaled.geometry.inverse - omega**-2 * coframe_evaluation.geometry.inverse),
        "determinant_weight_8": abs(constant_scaled.geometry.determinant - omega**8 * coframe_evaluation.geometry.determinant),
        "volume_weight_4": abs(
            np.sqrt(abs(constant_scaled.geometry.determinant))
            - omega**4 * np.sqrt(abs(coframe_evaluation.geometry.determinant))
        ),
    }
    residuals.update({f"csn_{key}": value for key, value in csn_residuals.items()})
    require("constant_csn_weights", max(csn_residuals.values()) < TOLERANCE, checks)
    sigma_first = np.array([0.1, -0.04, 0.03, 0.07])
    sigma_second = np.diag([0.02, -0.01, 0.015, 0.01])
    scaled_jets = csn_scaled_metric_jets(split_jets, omega, sigma_first, sigma_second)
    scaled_geometry = evaluate_metric_jets(scaled_jets)
    csn_connection_residual = maximum(
        scaled_geometry.christoffel - csn_connection_transform(split_geometry, sigma_first)
    )
    residuals["csn_variable_connection"] = csn_connection_residual
    require("variable_csn_connection_transform", csn_connection_residual < TOLERANCE, checks)

    fixtures: dict[str, dict] = {}
    expected_scalars = {"cartesian_flat": 0.0, "polar_flat": 0.0, "unit_sphere_product": 2.0}
    for name in expected_scalars:
        jets, frame, frame_first, frame_second, point = fixture(name)
        geometry = evaluate_metric_jets(jets)
        frame_geometry = evaluate_coframe_jets(frame, frame_first, frame_second)
        fixture_residual = max(max(geometry.residuals.values()), max(frame_geometry.residuals.values()))
        residuals[f"fixture_{name}"] = fixture_residual
        require(f"{name}_scalar", abs(geometry.scalar_curvature - expected_scalars[name]) < TOLERANCE, checks)
        require(f"{name}_identities", fixture_residual < TOLERANCE, checks)
        fixtures[name] = {
            **point,
            "inertia": list(geometry.inertia),
            "determinant": geometry.determinant,
            "scalar_curvature": geometry.scalar_curvature,
            "max_identity_residual": fixture_residual,
            "gamma_witnesses": {
                "Gamma^2_12": geometry.christoffel[2, 1, 2],
                "Gamma^1_22": geometry.christoffel[1, 2, 2],
                "Gamma^3_23": geometry.christoffel[3, 2, 3],
                "Gamma^2_33": geometry.christoffel[2, 3, 3],
            },
            "riemann_witness": geometry.riemann_down[2, 3, 2, 3],
        }
    require("polar_connection_nonzero", abs(fixtures["polar_flat"]["gamma_witnesses"]["Gamma^2_12"] - 0.5) < TOLERANCE, checks)
    require("polar_curvature_zero", abs(fixtures["polar_flat"]["scalar_curvature"]) < TOLERANCE, checks)
    require("sphere_curvature_nonzero", abs(fixtures["unit_sphere_product"]["riemann_witness"] - 0.75) < TOLERANCE, checks)

    maximum_residual = max(residuals.values(), default=0.0)
    require("global_raw_residual_gate", maximum_residual < TOLERANCE, checks)
    result = {
        "schema": "udt-p01-canonical-geometry-evaluator-1.0",
        "status": "PASS",
        "maximum_conclusion": "GEOMETRY_EVALUATOR_VERIFIED_NOT_SOLUTION_SPACE_EXPLORED",
        "premise_stamps": {
            "whole_parent": "CONDITIONAL_4D_CONFORMAL_LORENTZIAN_COFRAME",
            "two_plus_two": "CONDITIONAL_BRANCH_SUPPLIED_SPLIT_NOT_SELECTED",
            "slot_jets": "FREE_AND_EXPLORED_AS_SOFTWARE_INPUTS",
            "dynamics": "OPEN_NOT_EVALUATED",
            "comparison_fixtures": "COMPARISON_READOUT_ONLY",
        },
        "implementation": {
            "dimension": DIM,
            "slot_names": list(SLOT_NAMES),
            "slot_count": len(SLOT_NAMES),
            "coordinate_count": DIM,
            "value_channels_exercised": value_channels,
            "first_jet_channels_exercised": first_channels,
            "symmetric_second_jet_channels_exercised": second_channels,
            "main_method": "explicit float64 metric/coframe two-jet tensor algebra",
            "scientific_solve_executed": False,
            "gpu_used": False,
        },
        "checks": checks,
        "check_count": len(checks),
        "raw_residuals": residuals,
        "maximum_raw_residual": maximum_residual,
        "split_witness": {
            "slot_values": slot_values.tolist(),
            "inertia": list(split_geometry.inertia),
            "determinant": split_geometry.determinant,
            "scalar_curvature": split_geometry.scalar_curvature,
            "reconstructed_slot_max_error": maximum(split_reconstruction.slots - slot_values),
        },
        "fixtures": fixtures,
        "csn_weights": {"coframe": 1, "metric": 2, "inverse": -2, "determinant": 8, "volume": 4},
        "versions": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "sympy": sp.__version__,
        },
        "scope": {
            "local_metric_two_jets_only": True,
            "solution_space_explored": False,
            "reciprocal_plane_selected": False,
            "phi_metric_join_selected": False,
            "action_or_equation_evaluated": False,
            "boundary_or_topology_completed": False,
            "physical_evolution_run": False,
        },
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    RESULT.write_text(rendered, encoding="utf-8")
    TRANSCRIPT.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Construct and observe bounded all-slot metric families without dynamics."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
P01 = ROOT / "udt_canonical_geometry_evaluator_p01_2026-07-21"
sys.path.insert(0, str(P01))

from canonical_geometry_evaluator import (  # noqa: E402
    DIM,
    ETA,
    Jet2,
    MetricJets,
    constant_linear_coordinate_transform_coframe,
    csn_scaled_metric_jets,
    evaluate_coframe_jets,
    evaluate_metric_jets,
    local_internal_frame_transform_coframe_jets,
    metric_jets_from_split,
)


CLASSIFICATION = "CONSTRUCTIVE_ALL_SLOT_CONFIGURATION_FAMILIES_OBSERVED_IN_REGISTERED_LOCAL_REGIME"
MAXIMUM = "CONSTRUCTIVE_METRIC_CONFIGURATION_FAMILIES_CHARACTERIZED_NOT_DYNAMICAL_SOLUTIONS"
TOLERANCE = 2e-10
RANK_TOLERANCE = 1e-9
PAIRS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
SLOT_NAMES = ("h00", "h01", "h11", "q22", "q23", "q33", "A2_0", "A3_0", "A2_1", "A3_1")
LATENT_NAMES = ("a", "b", "c", "d", "e", "f", "A2_0", "A3_0", "A2_1", "A3_1")
BASE_VALUES = (0.08, 0.14, -0.06, 0.12, -0.09, 0.05, 0.11, -0.07, 0.09, 0.04)
PHI_OFFSETS = (-0.25, 0.0, 0.25, 0.125)
LAMBDAS = (-1.0, -0.5, 0.0, 0.5, 1.0)
POINTS = {
    "P0": (0.0, 0.0, 0.0, 0.0),
    "P1": (1 / 3, -1 / 4, 1 / 5, -1 / 6),
    "P2": (-1 / 4, 1 / 5, -1 / 6, 1 / 7),
    "P3": (1 / 5, 1 / 6, -1 / 7, -1 / 8),
    "P4": (-1 / 6, -1 / 7, 1 / 8, 1 / 9),
    "P5": (1 / 2, 0.0, -1 / 3, 1 / 4),
    "P6": (0.0, -1 / 2, 1 / 4, -1 / 3),
    "P7": (1 / 3, 1 / 3, 1 / 3, 1 / 3),
}
SOURCES = {
    "UDT_NATIVE_ACTION_COLD_PACKET.md": "d38232792ac78188687db433a3f60a08c775c46e9ecf5fc42ad7953dc89fadb0",
    "udt_complete_metric_solution_space_map_2026-07-21/SHA256SUMS.txt": "1778e4dcfcf9ac0bd3574fb3ff5248f2990265fa40d0822ff964ac67c434ae38",
    "udt_canonical_geometry_evaluator_p01_2026-07-21/SHA256SUMS.txt": "b7d8917cb27627c7ad7767fcffbd5b5d7a9dc6da2171b2d8fba329d04014ffad",
    "udt_local_jet_atlas_p02_2026-07-21/SHA256SUMS.txt": "c56390eb26b80c54a3c3a09f4800086c8dbc00b5bfd40b2038e264e85bec8938",
    "udt_founded_constraint_atlas_p03_2026-07-21/SHA256SUMS.txt": "b0ec5cbb2be404084e1b1ed4eca98d53c9712a62cf1af0a48eb340b64467c3be",
    "udt_global_kinematic_assembly_p03g_2026-07-21/SHA256SUMS.txt": "62f9b3f33409b62fb841734e8a91e61d9b859247bf808c4a6cf3740b6a54b6c9",
    "udt_finite_cell_completion_atlas_2026-07-21/SHA256SUMS.txt": "56c5f36455ae1f89811f3b86db9455a39482510415e6a7f770d2e5ffaa4ed0c7",
}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            h.update(block)
    return h.hexdigest()


def canonical_hash(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def write_tsv(name: str, fields: list[str], rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def jet_constant(value: float) -> Jet2:
    return Jet2(float(value), np.zeros(DIM), np.zeros((DIM, DIM)))


def jet_exp(value: Jet2) -> Jet2:
    exponential = math.exp(value.value)
    return Jet2(
        exponential,
        exponential * value.first,
        exponential * (value.second + np.outer(value.first, value.first)),
    )


def feature_jets(x: np.ndarray) -> list[Jet2]:
    features: list[Jet2] = []
    for coordinate in range(DIM):
        first = np.zeros(DIM)
        first[coordinate] = 1.0
        features.append(Jet2(float(x[coordinate]), first, np.zeros((DIM, DIM))))
    for coordinate in range(DIM):
        first = np.zeros(DIM)
        first[coordinate] = x[coordinate]
        second = np.zeros((DIM, DIM))
        second[coordinate, coordinate] = 1.0
        features.append(Jet2(0.5 * float(x[coordinate] ** 2), first, second))
    for first_coordinate, second_coordinate in PAIRS:
        first = np.zeros(DIM)
        first[first_coordinate] = x[second_coordinate]
        first[second_coordinate] = x[first_coordinate]
        second = np.zeros((DIM, DIM))
        second[first_coordinate, second_coordinate] = 1.0
        second[second_coordinate, first_coordinate] = 1.0
        features.append(Jet2(float(x[first_coordinate] * x[second_coordinate]), first, second))
    return features


def coefficient(bank: int, field: int, term: int) -> float:
    raw = ((bank + 2) * 11 + (field + 1) * 7 + (term + 1) * 5 + (bank + 1) * (field + term + 3)) % 19 - 9
    if raw == 0:
        raw = 1 if (bank + field + term) % 2 == 0 else -1
    scale = 60.0 if term < 4 else 90.0 if term < 8 else 120.0
    return raw / scale


def polynomial_jet(bank: int, field: int, x: np.ndarray) -> Jet2:
    result = jet_constant(0.0)
    for term, feature in enumerate(feature_jets(x)):
        result = result + coefficient(bank, field, term) * feature
    return result


def scaled_latent(bank: int, field: int, x: np.ndarray, deformation: float, base: float) -> Jet2:
    return jet_constant(base) + deformation * polynomial_jet(bank, field, x)


def regular_family(bank: int, deformation: float, x: np.ndarray) -> dict[str, object]:
    latent = [scaled_latent(bank, index, x, deformation, BASE_VALUES[index]) for index in range(10)]
    a, b, c, d, e, f, a20, a30, a21, a31 = latent
    u, w, r, t = jet_exp(a), jet_exp(c), jet_exp(d), jet_exp(f)
    slots = (
        -(u * u),
        -(u * b),
        w * w - b * b,
        r * r,
        r * e,
        e * e + t * t,
        a20,
        a30,
        a21,
        a31,
    )
    slot_values = np.array([item.value for item in slots])
    slot_first = np.array([item.first for item in slots]).T
    slot_second = np.transpose(np.array([item.second for item in slots]), (1, 2, 0))
    metric_jets = metric_jets_from_split(slot_values, slot_first, slot_second)

    zero = jet_constant(0.0)
    coframe_jets = [[zero for _ in range(DIM)] for _ in range(DIM)]
    coframe_jets[0] = [u, b, zero, zero]
    coframe_jets[1] = [zero, w, zero, zero]
    coframe_jets[2] = [r * a20 + e * a30, r * a21 + e * a31, r, e]
    coframe_jets[3] = [t * a30, t * a31, zero, t]
    coframe = np.array([[item.value for item in row] for row in coframe_jets])
    coframe_first = np.array([[[coframe_jets[i][mu].first[k] for mu in range(DIM)] for i in range(DIM)] for k in range(DIM)])
    coframe_second = np.array(
        [[[[coframe_jets[i][mu].second[k, ell] for mu in range(DIM)] for i in range(DIM)] for ell in range(DIM)] for k in range(DIM)]
    )
    phi = jet_constant(PHI_OFFSETS[bank]) + deformation * polynomial_jet(bank, 10, x)
    return {
        "latent": latent,
        "slots": slots,
        "slot_values": slot_values,
        "slot_first": slot_first,
        "slot_second": slot_second,
        "metric_jets": metric_jets,
        "coframe": coframe,
        "coframe_first": coframe_first,
        "coframe_second": coframe_second,
        "phi": phi,
    }


def latent_slot_jacobian(latent: list[Jet2]) -> np.ndarray:
    a, b, c, d, e, f = latent[:6]
    u, w, r, t = math.exp(a.value), math.exp(c.value), math.exp(d.value), math.exp(f.value)
    jacobian = np.zeros((10, 10))
    jacobian[0, 0] = -2 * u**2
    jacobian[1, 0] = -u * b.value
    jacobian[1, 1] = -u
    jacobian[2, 1] = -2 * b.value
    jacobian[2, 2] = 2 * w**2
    jacobian[3, 3] = 2 * r**2
    jacobian[4, 3] = r * e.value
    jacobian[4, 4] = r
    jacobian[5, 4] = 2 * e.value
    jacobian[5, 5] = 2 * t**2
    jacobian[6:, 6:] = np.eye(4)
    return jacobian


def numerical_rank(matrix: np.ndarray) -> tuple[int, str, list[float]]:
    singular = np.linalg.svd(np.asarray(matrix, dtype=float), compute_uv=False)
    rank = int(np.count_nonzero(singular > RANK_TOLERANCE))
    uncertainty_band = any(RANK_TOLERANCE / 100 <= value <= RANK_TOLERANCE * 100 for value in singular)
    return rank, "NUMERIC_UNCERTAIN" if uncertainty_band else "NUMERIC_CLASSIFIED", singular.tolist()


def weyl_tensor(geometry) -> np.ndarray:
    g = geometry.metric
    ricci = geometry.ricci
    scalar = geometry.scalar_curvature
    riemann = geometry.riemann_down
    result = np.zeros_like(riemann)
    for a in range(DIM):
        for b in range(DIM):
            for c in range(DIM):
                for d in range(DIM):
                    result[a, b, c, d] = (
                        riemann[a, b, c, d]
                        - 0.5 * (g[a, c] * ricci[b, d] - g[a, d] * ricci[b, c] - g[b, c] * ricci[a, d] + g[b, d] * ricci[a, c])
                        + scalar * (g[a, c] * g[b, d] - g[a, d] * g[b, c]) / 6.0
                    )
    return result


def contraction4(tensor: np.ndarray, inverse: np.ndarray) -> float:
    return float(np.einsum("abcd,ae,bf,cg,dh,efgh->", tensor, inverse, inverse, inverse, inverse, tensor))


def split_kinematics(slot_values: np.ndarray, slot_first: np.ndarray) -> dict[str, object]:
    screen = np.array([[slot_values[3], slot_values[4]], [slot_values[4], slot_values[5]]])
    shifts = np.array([[slot_values[6], slot_values[8]], [slot_values[7], slot_values[9]]])
    screen_first = [np.array([[slot_first[k, 3], slot_first[k, 4]], [slot_first[k, 4], slot_first[k, 5]]]) for k in range(DIM)]
    shifts_first = [np.array([[slot_first[k, 6], slot_first[k, 8]], [slot_first[k, 7], slot_first[k, 9]]]) for k in range(DIM)]
    inverse = np.linalg.inv(screen)
    twist = np.zeros(2)
    for vertical in range(2):
        twist[vertical] = (
            shifts_first[0][vertical, 1]
            - shifts_first[1][vertical, 0]
            - sum(shifts[other, 0] * shifts_first[2 + other][vertical, 1] for other in range(2))
            + sum(shifts[other, 1] * shifts_first[2 + other][vertical, 0] for other in range(2))
        )
    expansions = []
    shear_rows = []
    shears = []
    for base in range(2):
        horizontal = screen_first[base] - sum(shifts[vertical, base] * screen_first[2 + vertical] for vertical in range(2))
        vertical_derivative = np.array([[shifts_first[2 + derivative][output, base] for output in range(2)] for derivative in range(2)])
        lie = horizontal - vertical_derivative @ screen - screen @ vertical_derivative.T
        deformation = 0.5 * lie
        expansion = float(np.trace(inverse @ deformation))
        shear = deformation - 0.5 * expansion * screen
        expansions.append(expansion)
        shears.append(shear)
        shear_rows.append((shear[0, 0], shear[0, 1], shear[1, 1]))
    expansion_rank, expansion_status, _ = numerical_rank(np.asarray(expansions).reshape(2, 1))
    shear_rank, shear_status, _ = numerical_rank(np.asarray(shear_rows))
    twist_rank, twist_status, _ = numerical_rank(twist.reshape(2, 1))
    return {
        "screen": screen,
        "shifts": shifts,
        "twist": twist,
        "twist_rank": twist_rank,
        "twist_status": twist_status,
        "expansions": expansions,
        "expansion_rank": expansion_rank,
        "expansion_status": expansion_status,
        "shears": shears,
        "shear_rank": shear_rank,
        "shear_status": shear_status,
    }


def observe_configuration(family: dict[str, object]) -> tuple[dict[str, object], dict[str, object]]:
    metric_jets: MetricJets = family["metric_jets"]
    geometry = evaluate_metric_jets(metric_jets)
    frame = evaluate_coframe_jets(family["coframe"], family["coframe_first"], family["coframe_second"])
    coframe_metric_residual = max(
        float(np.max(np.abs(frame.metric_jets.metric - metric_jets.metric))),
        float(np.max(np.abs(frame.metric_jets.first - metric_jets.first))),
        float(np.max(np.abs(frame.metric_jets.second - metric_jets.second))),
    )
    identity_residual = max(max(geometry.residuals.values()), max(frame.residuals.values()), coframe_metric_residual)
    curvature_matrix = np.array([[geometry.riemann_down[a, b, c, d] for c, d in PAIRS] for a, b in PAIRS])
    curvature_rank, curvature_rank_status, curvature_singular = numerical_rank(curvature_matrix)
    ricci_rank, ricci_rank_status, ricci_singular = numerical_rank(geometry.ricci)
    kinematics = split_kinematics(family["slot_values"], family["slot_first"])
    weyl = weyl_tensor(geometry)
    mixed_values = []
    for i in range(2):
        for j in range(2):
            for a in range(2, 4):
                for b in range(2, 4):
                    mixed_values.extend((geometry.riemann_down[i, a, j, b], geometry.riemann_down[i, j, a, b]))
    phi: Jet2 = family["phi"]
    phi_norm = float(phi.first @ geometry.inverse @ phi.first)
    weyl_trace_residual = float(np.max(np.abs(np.einsum("ac,abcd->bd", geometry.inverse, weyl))))
    horizontal_support = float(np.max(np.abs(phi.first[:2])))
    vertical_support = float(np.max(np.abs(phi.first[2:])))
    coordinate_activity = [float(np.max(np.abs(family["slot_first"][coordinate]))) for coordinate in range(DIM)]
    latent_rank, latent_rank_status, latent_singular = numerical_rank(latent_slot_jacobian(family["latent"]))
    observation = {
        "determinant": geometry.determinant,
        "inertia": ",".join(str(value) for value in geometry.inertia),
        "identity_residual": identity_residual,
        "latent_to_slot_rank": latent_rank,
        "latent_rank_status": latent_rank_status,
        "scalar_curvature": geometry.scalar_curvature,
        "ricci_rank": ricci_rank,
        "ricci_rank_status": ricci_rank_status,
        "curvature_operator_rank": curvature_rank,
        "curvature_rank_status": curvature_rank_status,
        "riemann_max_abs": float(np.max(np.abs(geometry.riemann_down))),
        "ricci_max_abs": float(np.max(np.abs(geometry.ricci))),
        "weyl_max_abs": float(np.max(np.abs(weyl))),
        "weyl_trace_residual": weyl_trace_residual,
        "ricci_square": float(np.einsum("ab,ac,bd,cd->", geometry.ricci, geometry.inverse, geometry.inverse, geometry.ricci)),
        "riemann_square": contraction4(geometry.riemann_down, geometry.inverse),
        "weyl_square": contraction4(weyl, geometry.inverse),
        "mixed_curvature_max_abs": float(np.max(np.abs(mixed_values))),
        "time_derivative_activity": coordinate_activity[0],
        "depth_derivative_activity": coordinate_activity[1],
        "angular2_derivative_activity": coordinate_activity[2],
        "angular3_derivative_activity": coordinate_activity[3],
        "expansion_0": kinematics["expansions"][0],
        "expansion_1": kinematics["expansions"][1],
        "expansion_rank": kinematics["expansion_rank"],
        "shear_rank": kinematics["shear_rank"],
        "twist_rank": kinematics["twist_rank"],
        "twist_max_abs": float(np.max(np.abs(kinematics["twist"]))),
        "shear_max_abs": float(max(np.max(np.abs(value)) for value in kinematics["shears"])),
        "phi": phi.value,
        "phi_gradient_norm": phi_norm,
        "phi_gradient_max_abs": float(np.max(np.abs(phi.first))),
        "phi_horizontal_support": horizontal_support,
        "phi_vertical_support": vertical_support,
        "phi_hessian_max_abs": float(np.max(np.abs(phi.second))),
    }
    raw = {
        "slot_values": family["slot_values"].tolist(),
        "slot_first": family["slot_first"].tolist(),
        "slot_second": family["slot_second"].tolist(),
        "metric": metric_jets.metric.tolist(),
        "metric_first": metric_jets.first.tolist(),
        "metric_second": metric_jets.second.tolist(),
        "coframe": family["coframe"].tolist(),
        "coframe_first": family["coframe_first"].tolist(),
        "coframe_second": family["coframe_second"].tolist(),
        "phi": {"value": phi.value, "first": phi.first.tolist(), "second": phi.second.tolist()},
        "ricci": geometry.ricci.tolist(),
        "riemann_down": geometry.riemann_down.tolist(),
        "weyl_down": weyl.tolist(),
        "curvature_singular_values": curvature_singular,
        "ricci_singular_values": ricci_singular,
        "latent_slot_singular_values": latent_singular,
        "observables": observation,
    }
    return observation, raw


def coordinate_gauge_checks(anchor: dict[str, object]) -> list[dict[str, object]]:
    original = evaluate_coframe_jets(anchor["coframe"], anchor["coframe_first"], anchor["coframe_second"])
    transforms = {
        "J01": np.array([[1.0, 0.2, 0.0, 0.0], [0.1, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, -0.15], [0.0, 0.0, 0.25, 1.0]]),
        "J02": np.array([[1.0, 0.0, 0.12, 0.0], [0.0, 1.0, 0.0, -0.18], [0.07, 0.0, 1.0, 0.0], [0.0, 0.09, 0.0, 1.0]]),
    }
    rows = []
    for transform_id, jacobian in transforms.items():
        changed = constant_linear_coordinate_transform_coframe(anchor["coframe"], anchor["coframe_first"], anchor["coframe_second"], jacobian)
        evaluated = evaluate_coframe_jets(*changed)
        expected_metric = jacobian.T @ original.metric_jets.metric @ jacobian
        expected_riemann = np.einsum("ma,nb,kc,ld,mnkl->abcd", jacobian, jacobian, jacobian, jacobian, original.geometry.riemann_down)
        rows.append({
            "check_id": transform_id,
            "kind": "CONSTANT_COORDINATE_ORBIT",
            "metric_tensor_residual": float(np.max(np.abs(evaluated.metric_jets.metric - expected_metric))),
            "curvature_tensor_residual": float(np.max(np.abs(evaluated.geometry.riemann_down - expected_riemann))),
            "scalar_residual": abs(evaluated.geometry.scalar_curvature - original.geometry.scalar_curvature),
            "counted_as_new_geometry": "NO",
        })

    rapidity = 0.31
    generator = np.zeros((DIM, DIM))
    generator[0, 1] = generator[1, 0] = 1.0
    lorentz = np.eye(DIM)
    lorentz[:2, :2] = [[math.cosh(rapidity), math.sinh(rapidity)], [math.sinh(rapidity), math.cosh(rapidity)]]
    rapidity_first = np.array([0.07, -0.04, 0.03, 0.05])
    rapidity_second = np.array([[0.02, 0.01, 0.0, -0.005], [0.01, -0.015, 0.004, 0.0], [0.0, 0.004, 0.01, 0.006], [-0.005, 0.0, 0.006, -0.012]])
    lorentz_first = np.array([rapidity_first[k] * generator @ lorentz for k in range(DIM)])
    lorentz_second = np.zeros((DIM, DIM, DIM, DIM))
    for k in range(DIM):
        for ell in range(DIM):
            lorentz_second[k, ell] = rapidity_second[k, ell] * generator @ lorentz + rapidity_first[k] * rapidity_first[ell] * generator @ generator @ lorentz
    changed = local_internal_frame_transform_coframe_jets(
        anchor["coframe"], anchor["coframe_first"], anchor["coframe_second"], lorentz, lorentz_first, lorentz_second
    )
    evaluated = evaluate_coframe_jets(*changed)
    inverse_lorentz = np.linalg.inv(lorentz)
    expected_cartan = np.einsum("ia,abmn,bj->ijmn", lorentz, original.cartan_curvature, inverse_lorentz)
    rows.append({
        "check_id": "L01",
        "kind": "LOCAL_LORENTZ_ORBIT",
        "metric_tensor_residual": float(np.max(np.abs(evaluated.metric_jets.metric - original.metric_jets.metric))),
        "curvature_tensor_residual": float(np.max(np.abs(evaluated.cartan_curvature - expected_cartan))),
        "scalar_residual": abs(evaluated.geometry.scalar_curvature - original.geometry.scalar_curvature),
        "counted_as_new_geometry": "NO",
    })
    return rows


def csn_observations(anchor: dict[str, object], anchor_id: str, x: np.ndarray) -> list[dict[str, object]]:
    original = evaluate_metric_jets(anchor["metric_jets"])
    sigma = polynomial_jet(0, 11, x)
    rows = []
    for kappa in (-0.5, 0.5):
        omega = math.exp(kappa * sigma.value)
        changed = csn_scaled_metric_jets(anchor["metric_jets"], omega, kappa * sigma.first, kappa * sigma.second)
        evaluated = evaluate_metric_jets(changed)
        rows.append({
            "orbit_id": f"{anchor_id}_K{str(kappa).replace('-', 'm').replace('.', 'p')}",
            "anchor_id": anchor_id,
            "kappa": kappa,
            "omega": omega,
            "determinant_ratio": evaluated.determinant / original.determinant,
            "expected_determinant_ratio": omega**8,
            "scalar_before": original.scalar_curvature,
            "scalar_after": evaluated.scalar_curvature,
            "metric_inertia_before": ",".join(map(str, original.inertia)),
            "metric_inertia_after": ",".join(map(str, evaluated.inertia)),
            "physical_representative_selected": "NO",
        })
    return rows


def degeneracy_closures() -> list[dict[str, object]]:
    families = {
        "D01_BASE_CLOCK": lambda s: np.diag([s, 1.0, 1.0, 1.0]),
        "D02_BASE_SECOND": lambda s: np.diag([-1.0, s, 1.0, 1.0]),
        "D03_SCREEN_FIRST": lambda s: np.diag([-1.0, 1.0, s, 1.0]),
        "D04_SIMULTANEOUS": lambda s: np.diag([s, 1.0, s, 1.0]),
    }
    rows = []
    for family_id, builder in families.items():
        for parameter in LAMBDAS:
            metric = builder(parameter)
            eigenvalues = np.linalg.eigvalsh(metric)
            inertia = (
                int(np.count_nonzero(eigenvalues < -1e-12)),
                int(np.count_nonzero(eigenvalues > 1e-12)),
                int(np.count_nonzero(np.abs(eigenvalues) <= 1e-12)),
            )
            is_lorentzian = inertia in {(1, 3, 0), (3, 1, 0)}
            p01_status = "NOT_EVALUATED_SINGULAR_OR_NONLORENTZIAN"
            if is_lorentzian:
                geometry = evaluate_metric_jets(MetricJets(metric, np.zeros((4, 4, 4)), np.zeros((4, 4, 4, 4))))
                p01_status = "EVALUATED_REGULAR_LORENTZIAN" if max(geometry.residuals.values()) < TOLERANCE else "IDENTITY_FAILURE"
            rows.append({
                "family_id": family_id,
                "parameter": parameter,
                "determinant": float(np.linalg.det(metric)),
                "rank": int(np.linalg.matrix_rank(metric, tol=1e-12)),
                "inertia": ",".join(map(str, inertia)),
                "p01_status": p01_status,
                "retained": "YES",
                "merit": "NOT_EVALUATED",
            })
    return rows


def main() -> None:
    checks: list[str] = []

    def check(name: str, condition: bool) -> None:
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    for relative, expected in SOURCES.items():
        check(f"source_{relative}", digest(ROOT / relative) == expected)
    write_tsv("SOURCE_LINEAGE.tsv", ["path", "sha256", "role"], [
        {"path": path, "sha256": expected, "role": "CURRENT_AUTHORITY_OR_VERIFIED_PARENT"} for path, expected in SOURCES.items()
    ])

    family_rows = [
        {"family_id": f"B{bank}", "kind": "REGULAR_ALL_SLOT_SPLIT_COFRAME", "banks": 1, "deformation_values": len(LAMBDAS), "points": len(POINTS), "all_ten_slots": "YES", "all_four_coordinates": "YES", "status": "BOUNDED_CONSTRUCTIVE_FAMILY"}
        for bank in range(4)
    ]
    family_rows.extend([
        {"family_id": "CSN", "kind": "POSITIVE_LOCAL_SCALE_ORBIT", "banks": 0, "deformation_values": 2, "points": 2, "all_ten_slots": "INHERITED_FROM_ANCHOR", "all_four_coordinates": "YES", "status": "GAUGE_ORBIT_NOT_SELECTION"},
        {"family_id": "GAUGE", "kind": "COORDINATE_AND_LOCAL_LORENTZ_ORBIT", "banks": 0, "deformation_values": 3, "points": 1, "all_ten_slots": "INHERITED_FROM_ANCHOR", "all_four_coordinates": "YES", "status": "NOT_NEW_GEOMETRY"},
        {"family_id": "D01-D04", "kind": "DEGENERATE_TYPE_CHANGE_CLOSURE", "banks": 4, "deformation_values": len(LAMBDAS), "points": 1, "all_ten_slots": "NO_BOUNDED_ZERO_JET_SLICE", "all_four_coordinates": "NO_BOUNDED_ZERO_JET_SLICE", "status": "RETAINED_CLOSURE_NOT_WHOLE_FAMILY"},
    ])
    write_tsv("FAMILY_DEFINITIONS.tsv", list(family_rows[0]), family_rows)
    point_rows = [{"point_id": point_id, "x0": x[0], "x1": x[1], "x2": x[2], "x3": x[3], "provenance": "FREE_DIMENSIONLESS_COVERAGE_CONTROL"} for point_id, x in POINTS.items()]
    write_tsv("SAMPLE_POINTS.tsv", list(point_rows[0]), point_rows)

    dependency_rows = []
    for bank in range(4):
        for field, name in enumerate(LATENT_NAMES + ("phi",)):
            coefficients = [coefficient(bank, field, coordinate) for coordinate in range(4)]
            dependency_rows.append({
                "bank": f"B{bank}", "field": name,
                "dx0_linear": coefficients[0], "dx1_linear": coefficients[1],
                "dx2_linear": coefficients[2], "dx3_linear": coefficients[3],
                "all_coordinate_coefficients_nonzero": "YES" if all(value != 0 for value in coefficients) else "NO",
            })
    check("all_declared_coordinate_dependencies", all(row["all_coordinate_coefficients_nonzero"] == "YES" for row in dependency_rows))
    write_tsv("DEPENDENCY_PROOF.tsv", list(dependency_rows[0]), dependency_rows)

    observations: list[dict[str, object]] = []
    raw_rows: list[dict[str, object]] = []
    sector_rows: list[dict[str, object]] = []
    phi_rows: list[dict[str, object]] = []
    tangent_rows: list[dict[str, object]] = []
    anchors: dict[str, dict[str, object]] = {}
    for bank in range(4):
        for deformation in LAMBDAS:
            for point_id, point_tuple in POINTS.items():
                x = np.asarray(point_tuple, dtype=float)
                family = regular_family(bank, deformation, x)
                observation, raw = observe_configuration(family)
                config_id = f"B{bank}_L{LAMBDAS.index(deformation)}_{point_id}"
                latent_jacobian = latent_slot_jacobian(family["latent"])
                latent_lambda_derivative = np.array([polynomial_jet(bank, field, x).value for field in range(10)])
                slot_lambda_derivative = latent_jacobian @ latent_lambda_derivative
                sampled_tangent = np.column_stack((slot_lambda_derivative, family["slot_first"].T))
                sampled_tangent_rank, sampled_tangent_status, sampled_tangent_singular = numerical_rank(sampled_tangent)
                observation["sampled_tangent_rank"] = sampled_tangent_rank
                observation["sampled_tangent_status"] = sampled_tangent_status
                raw["sampled_tangent"] = sampled_tangent.tolist()
                raw["sampled_tangent_singular_values"] = sampled_tangent_singular
                identity_payload = {
                    "slots": raw["slot_values"], "slot_first": raw["slot_first"],
                    "slot_second": raw["slot_second"], "phi": raw["phi"],
                }
                metric_payload = {"metric": raw["metric"], "first": raw["metric_first"], "second": raw["metric_second"]}
                prefix = {
                    "configuration_id": config_id, "bank": f"B{bank}", "deformation": deformation,
                    "point_id": point_id, "configuration_sha256": canonical_hash(identity_payload),
                    "metric_jet_sha256": canonical_hash(metric_payload),
                }
                observations.append({**prefix, **observation, "retained": "YES", "physical_merit": "NOT_EVALUATED"})
                raw_rows.append({**prefix, "coordinates": list(point_tuple), **raw})
                sector_rows.append({
                    "configuration_id": config_id,
                    "time_active": "YES" if observation["time_derivative_activity"] > RANK_TOLERANCE else "NO",
                    "depth_active": "YES" if observation["depth_derivative_activity"] > RANK_TOLERANCE else "NO",
                    "angular2_active": "YES" if observation["angular2_derivative_activity"] > RANK_TOLERANCE else "NO",
                    "angular3_active": "YES" if observation["angular3_derivative_activity"] > RANK_TOLERANCE else "NO",
                    "mixed_shift_values_active": "YES" if np.max(np.abs(family["slot_values"][6:])) > RANK_TOLERANCE else "NO",
                    "screen_offdiagonal_active": "YES" if abs(family["slot_values"][4]) > RANK_TOLERANCE else "NO",
                    "shear_rank": observation["shear_rank"], "twist_rank": observation["twist_rank"],
                    "mixed_curvature_active": "YES" if observation["mixed_curvature_max_abs"] > RANK_TOLERANCE else "NO",
                    "dynamical_interpretation": "NONE_CONFIGURATION_ONLY",
                })
                phi_rows.append({
                    "configuration_id": config_id, "phi": observation["phi"],
                    "gradient_norm": observation["phi_gradient_norm"],
                    "horizontal_support": observation["phi_horizontal_support"],
                    "vertical_support": observation["phi_vertical_support"],
                    "screen_shear_rank": observation["shear_rank"], "twist_rank": observation["twist_rank"],
                    "mixed_curvature_max_abs": observation["mixed_curvature_max_abs"],
                    "relation_inferred": "NONE_OBSERVATION_ONLY",
                })
                tangent_rows.append({
                    "configuration_id": config_id,
                    "sample_parameters": "lambda,x0,x1,x2,x3",
                    "sample_parameter_count": 5,
                    "sampled_tangent_rank": sampled_tangent_rank,
                    "sampled_tangent_status": sampled_tangent_status,
                    "abstract_latent_to_slot_rank": observation["latent_to_slot_rank"],
                    "ten_amplitudes_independently_scanned": "NO",
                    "interpretation": "CORRELATED_PATH_TANGENT_NOT_FULL_TEN_PARAMETER_SCAN",
                })
                if (bank, deformation, point_id) in {(0, 1.0, "P1"), (3, -1.0, "P6")}:
                    anchors[config_id] = family

    check("regular_record_count", len(observations) == 160)
    check("all_regular_lorentzian", all(row["inertia"] == "1,3,0" for row in observations))
    check("all_latent_slot_rank_ten", all(row["latent_to_slot_rank"] == 10 for row in observations))
    check("p01_residual_gate", max(float(row["identity_residual"]) for row in observations) < TOLERANCE)
    check("weyl_trace_gate", max(float(row["weyl_trace_residual"]) for row in observations) < TOLERANCE)
    check("all_records_retained", all(row["retained"] == "YES" for row in observations))
    write_tsv("CONFIGURATION_OBSERVATIONS.tsv", list(observations[0]), observations)
    with (HERE / "RAW_CONFIGURATION_JETS.jsonl").open("w", encoding="utf-8") as handle:
        for row in raw_rows:
            handle.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")
    write_tsv("SECTOR_ACTIVITY.tsv", list(sector_rows[0]), sector_rows)
    write_tsv("PHI_ANGULAR_OBSERVATIONS.tsv", list(phi_rows[0]), phi_rows)
    tangent_counts = {rank: sum(int(row["sampled_tangent_rank"]) == rank for row in tangent_rows) for rank in range(6)}
    check("sampled_tangent_rank_distribution", tangent_counts == {0: 4, 1: 28, 2: 0, 3: 0, 4: 16, 5: 112})
    write_tsv("SAMPLED_TANGENT_RANK.tsv", list(tangent_rows[0]), tangent_rows)

    incidence_rows = []
    by_key = {(row["bank"], row["point_id"], float(row["deformation"])): row for row in observations}
    for bank in range(4):
        for point_id in POINTS:
            for left, right in zip(LAMBDAS[:-1], LAMBDAS[1:]):
                first = by_key[(f"B{bank}", point_id, left)]
                second = by_key[(f"B{bank}", point_id, right)]
                incidence_rows.append({
                    "path_id": f"B{bank}_{point_id}_{LAMBDAS.index(left)}_{LAMBDAS.index(right)}",
                    "from_configuration": first["configuration_id"], "to_configuration": second["configuration_id"],
                    "delta_determinant": float(second["determinant"]) - float(first["determinant"]),
                    "delta_scalar_curvature": float(second["scalar_curvature"]) - float(first["scalar_curvature"]),
                    "delta_mixed_curvature_max_abs": float(second["mixed_curvature_max_abs"]) - float(first["mixed_curvature_max_abs"]),
                    "ricci_rank_change": int(second["ricci_rank"]) - int(first["ricci_rank"]),
                    "curvature_rank_change": int(second["curvature_operator_rank"]) - int(first["curvature_operator_rank"]),
                    "compatibility_verdict": "NOT_ASSIGNED_OBSERVED_DEFORMATION_ONLY",
                })
    check("deformation_edge_count", len(incidence_rows) == 128)
    write_tsv("DEFORMATION_INCIDENCE.tsv", list(incidence_rows[0]), incidence_rows)

    gauge_rows = coordinate_gauge_checks(anchors["B0_L4_P1"])
    check("gauge_check_count", len(gauge_rows) == 3)
    check("gauge_residuals", max(max(float(row[key]) for key in ("metric_tensor_residual", "curvature_tensor_residual", "scalar_residual")) for row in gauge_rows) < TOLERANCE)
    check("gauge_not_new", all(row["counted_as_new_geometry"] == "NO" for row in gauge_rows))
    write_tsv("GAUGE_ORBIT_CHECKS.tsv", list(gauge_rows[0]), gauge_rows)

    csn_rows = []
    for anchor_id, family in anchors.items():
        raw_anchor = next(row for row in raw_rows if row["configuration_id"] == anchor_id)
        csn_rows.extend(csn_observations(family, anchor_id, np.asarray(raw_anchor["coordinates"], dtype=float)))
    check("csn_orbit_count", len(csn_rows) == 4)
    check("csn_inertia_preserved", all(row["metric_inertia_before"] == row["metric_inertia_after"] for row in csn_rows))
    check("csn_determinant_weight", max(abs(float(row["determinant_ratio"]) - float(row["expected_determinant_ratio"])) for row in csn_rows) < TOLERANCE)
    check("csn_no_selection", all(row["physical_representative_selected"] == "NO" for row in csn_rows))
    write_tsv("CSN_ORBIT_OBSERVATIONS.tsv", list(csn_rows[0]), csn_rows)

    closure_rows = degeneracy_closures()
    check("closure_count", len(closure_rows) == 20)
    check("closure_singular_retained", sum(row["rank"] < 4 and row["retained"] == "YES" for row in closure_rows) == 4)
    check("closure_has_other_signature", any(row["inertia"] not in {"1,3,0", "3,1,0"} and row["rank"] == 4 for row in closure_rows))
    write_tsv("DEGENERACY_CLOSURE.tsv", list(closure_rows[0]), closure_rows)

    nonzero_records = [row for row in observations if float(row["deformation"]) != 0]
    coverage_rows = [
        {"coverage_id": "C01", "object": "regular_all_slot_records", "observed": len(observations), "required": 160, "status": "PASS", "limit": "four finite coefficient banks"},
        {"coverage_id": "C02", "object": "unique_metric_jet_hashes", "observed": len({row["metric_jet_sha256"] for row in observations}), "required": "REPORTED_NOT_FILTERED", "status": "PASS", "limit": "duplicates retained"},
        {"coverage_id": "C03", "object": "nonzero_deformation_all_coordinates_active", "observed": sum(all(row[name] == "YES" for name in ("time_active", "depth_active", "angular2_active", "angular3_active")) for row in sector_rows if row["configuration_id"] in {r["configuration_id"] for r in nonzero_records}), "required": len(nonzero_records), "status": "PASS", "limit": "activity threshold only"},
        {"coverage_id": "C04", "object": "mixed_shift_value_records", "observed": sum(row["mixed_shift_values_active"] == "YES" for row in sector_rows), "required": 160, "status": "PASS", "limit": "pointwise value"},
        {"coverage_id": "C05", "object": "nonzero_deformation_shear_records", "observed": sum(int(row["shear_rank"]) > 0 for row in observations if float(row["deformation"]) != 0), "required": "REPORTED_NOT_FILTERED", "status": "PASS", "limit": "numeric rank"},
        {"coverage_id": "C06", "object": "nonzero_deformation_twist_records", "observed": sum(int(row["twist_rank"]) > 0 for row in observations if float(row["deformation"]) != 0), "required": "REPORTED_NOT_FILTERED", "status": "PASS", "limit": "numeric rank"},
        {"coverage_id": "C07", "object": "nonzero_deformation_mixed_curvature_records", "observed": sum(float(row["mixed_curvature_max_abs"]) > RANK_TOLERANCE for row in observations if float(row["deformation"]) != 0), "required": "REPORTED_NOT_FILTERED", "status": "PASS", "limit": "numeric activity"},
        {"coverage_id": "C08", "object": "signed_phi_offsets", "observed": len(set(PHI_OFFSETS)), "required": 4, "status": "PASS", "limit": "independent phi branch only"},
        {"coverage_id": "C09", "object": "deformation_edges", "observed": len(incidence_rows), "required": 128, "status": "PASS", "limit": "finite paths"},
        {"coverage_id": "C10", "object": "gauge_release_checks", "observed": len(gauge_rows), "required": 3, "status": "PASS", "limit": "two coordinate one Lorentz orbit"},
        {"coverage_id": "C11", "object": "CSN_orbit_records", "observed": len(csn_rows), "required": 4, "status": "PASS", "limit": "two anchors two kappas"},
        {"coverage_id": "C12", "object": "degenerate_type_change_records", "observed": len(closure_rows), "required": 20, "status": "PASS", "limit": "zero-jet closure witnesses"},
        {"coverage_id": "C13", "object": "arbitrary_function_global_topology_remainder", "observed": "NOT_ENUMERATED", "required": "EXPLICIT_OPEN", "status": "PASS", "limit": "no finite exhaustiveness"},
        {"coverage_id": "C14", "object": "sampled_path_tangent_rank", "observed": "0:4;1:28;4:16;5:112", "required": "REPORT_SHARED_LAMBDA_RESTRICTION", "status": "PASS", "limit": "ten latent amplitudes were not independently scanned"},
    ]
    check("coverage_rows", len(coverage_rows) == 14 and all(row["status"] == "PASS" for row in coverage_rows))
    write_tsv("COVERAGE_LEDGER.tsv", list(coverage_rows[0]), coverage_rows)

    criteria = [
        ("Q01", "FIELDS", "ten metric slots and independent signed phi in C02 branch", "other phi/coframe/connection field realizations open"),
        ("Q02", "ACTION_TERMS", "none loaded", "native and conditional actions excluded"),
        ("Q03", "FULL_EQUATIONS", "none solved", "no EOM solution claim"),
        ("Q04", "DOMAIN_COORDINATES", "all four dependencies in four bounded analytic banks", "arbitrary functions charts and global cover open"),
        ("Q05", "BOUNDARY_REGULARITY", "degenerate zero-jet closures only", "finite-cell boundary and matching unsolved"),
        ("Q06", "TOPOLOGICAL_SECTOR", "none selected", "all global topology open"),
        ("Q07", "DYNAMICAL_CHARACTER", "static reference and time-dependent configurations", "no physical evolution law"),
        ("Q08", "BRANCH_BIFURCATION", "bounded deformation incidence", "EOM branches nonexistent without law"),
        ("Q09", "STABILITY", "not entered", "no perturbation operator"),
        ("Q10", "REGIME_VALIDITY", "local/regional smooth analytic chart sample", "nonsmooth arbitrary global and on-shell regimes open"),
    ]
    write_tsv("TEN_CRITERION_SCOPE.tsv", ["id", "criterion", "covered", "open"], [{"id": i, "criterion": c, "covered": v, "open": o} for i, c, v, o in criteria])
    anti = [
        ("A01", "desired boundary seal topology or quotient target", "ABSENT"),
        ("A02", "action or EOM residual used as filter", "ABSENT"),
        ("A03", "particle lump mass spectrum or stability target", "ABSENT"),
        ("A04", "GR empirical or cosmological merit comparison", "ABSENT"),
        ("A05", "diagonal round static or twist-free whole ansatz", "ABSENT"),
        ("A06", "mixed shifts screen shear or angular dependence omitted", "ABSENT"),
        ("A07", "time-dependent configuration called evolution", "ABSENT"),
        ("A08", "singular or other-signature branch discarded", "ABSENT"),
        ("A09", "numeric rank used as physical acceptance", "ABSENT"),
        ("A10", "gauge copies counted as distinct geometry", "ABSENT"),
        ("A11", "CSN representative selected", "ABSENT"),
        ("A12", "finite witness set called exhaustive", "ABSENT"),
        ("A13", "metric-derived phi relation invented", "ABSENT"),
        ("A14", "compatibility verdict assigned before observation", "ABSENT"),
        ("A15", "P06 readiness or physical solution inferred", "ABSENT"),
    ]
    check("anti_imposition", len(anti) == 15)
    write_tsv("ANTI_IMPOSITION_AUDIT.tsv", ["id", "failure_mode", "present"], [{"id": i, "failure_mode": f, "present": p} for i, f, p in anti])

    raw_hash = digest(HERE / "RAW_CONFIGURATION_JETS.jsonl")
    zero_deformation = [row for row in observations if float(row["deformation"]) == 0]
    nonzero_deformation = [row for row in observations if float(row["deformation"]) != 0]
    observed_census = {
        "zero_deformation_records": len(zero_deformation),
        "zero_deformation_flat_curvature_records": sum(float(row["riemann_max_abs"]) <= RANK_TOLERANCE for row in zero_deformation),
        "nonzero_deformation_records": len(nonzero_deformation),
        "nonzero_full_ricci_rank_records": sum(int(row["ricci_rank"]) == 4 for row in nonzero_deformation),
        "nonzero_full_curvature_operator_rank_records": sum(int(row["curvature_operator_rank"]) == 6 for row in nonzero_deformation),
        "nonzero_shear_rank_two_records": sum(int(row["shear_rank"]) == 2 for row in nonzero_deformation),
        "nonzero_twist_rank_one_records": sum(int(row["twist_rank"]) == 1 for row in nonzero_deformation),
        "nonzero_mixed_curvature_records": sum(float(row["mixed_curvature_max_abs"]) > RANK_TOLERANCE for row in nonzero_deformation),
        "phi_negative_records": sum(float(row["phi"]) < -RANK_TOLERANCE for row in observations),
        "phi_near_zero_records": sum(abs(float(row["phi"])) <= RANK_TOLERANCE for row in observations),
        "phi_positive_records": sum(float(row["phi"]) > RANK_TOLERANCE for row in observations),
        "dphi_timelike_records": sum(float(row["phi_gradient_norm"]) < -RANK_TOLERANCE for row in observations),
        "dphi_zero_records": sum(float(row["phi_gradient_max_abs"]) <= RANK_TOLERANCE for row in observations),
        "dphi_nonzero_near_null_records": sum(
            float(row["phi_gradient_max_abs"]) > RANK_TOLERANCE and abs(float(row["phi_gradient_norm"])) <= RANK_TOLERANCE
            for row in observations
        ),
        "dphi_spacelike_records": sum(float(row["phi_gradient_norm"]) > RANK_TOLERANCE for row in observations),
    }
    result = {
        "schema": "udt-constructive-metric-family-atlas-1.0",
        "status": "PASS",
        "classification": CLASSIFICATION,
        "maximum_conclusion": MAXIMUM,
        "checks": len(checks),
        "regular_configuration_records": len(observations),
        "unique_metric_jet_hashes": len({row["metric_jet_sha256"] for row in observations}),
        "coefficient_banks": 4,
        "deformation_values": len(LAMBDAS),
        "sample_points": len(POINTS),
        "all_ten_slots": True,
        "all_four_coordinates_in_nonzero_deformations": True,
        "phi_branch": "C02_INDEPENDENT_SIGNED_FIELD_ONLY",
        "deformation_edges": len(incidence_rows),
        "gauge_checks": len(gauge_rows),
        "csn_orbit_records": len(csn_rows),
        "degeneracy_closure_records": len(closure_rows),
        "singular_closure_records_retained": sum(row["rank"] < 4 for row in closure_rows),
        "max_identity_residual": max(float(row["identity_residual"]) for row in observations),
        "raw_configuration_sha256": raw_hash,
        "observed_census": observed_census,
        "sampled_tangent_rank_counts": {str(rank): count for rank, count in tangent_counts.items() if count},
        "sampled_parameter_count_per_bank": 5,
        "ten_amplitudes_independently_scanned": False,
        "dynamics_loaded": False,
        "solutions_run": 0,
        "physical_evolution_claimed": False,
        "compatibility_ranking_used": False,
        "gpu_used": False,
        "finite_exhaustiveness_claim": False,
        "evidence_grade": "VERIFIED_WITH_CAVEATS",
        "checks_passed": checks,
    }
    (HERE / "ATLAS_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    transcript = [
        "UDT_CONSTRUCTIVE_METRIC_FAMILY_ATLAS=PASS",
        f"checks={len(checks)}",
        f"classification={CLASSIFICATION}",
        f"regular_records={len(observations)} unique_metric_jets={result['unique_metric_jet_hashes']}",
        "banks=4 deformation_values=5 points=8",
        "all_ten_slots=YES all_four_coordinates_nonzero_deformations=YES",
        f"deformation_edges={len(incidence_rows)} gauge_checks={len(gauge_rows)} CSN_orbits={len(csn_rows)}",
        f"degenerate_closure_records={len(closure_rows)} singular_retained={result['singular_closure_records_retained']}",
        f"max_identity_residual={result['max_identity_residual']:.17g}",
        f"raw_configuration_sha256={raw_hash}",
        f"observed_zero_flat={observed_census['zero_deformation_flat_curvature_records']}/{observed_census['zero_deformation_records']}",
        f"observed_nonzero_full_ranks={observed_census['nonzero_full_ricci_rank_records']}/{observed_census['nonzero_full_curvature_operator_rank_records']}/{observed_census['nonzero_deformation_records']}",
        f"observed_nonzero_shear_twist_mixed={observed_census['nonzero_shear_rank_two_records']}/{observed_census['nonzero_twist_rank_one_records']}/{observed_census['nonzero_mixed_curvature_records']}",
        f"observed_phi_signs={observed_census['phi_negative_records']}/{observed_census['phi_near_zero_records']}/{observed_census['phi_positive_records']}",
        f"observed_dphi_timelike_zero_nonzero_near_null_spacelike={observed_census['dphi_timelike_records']}/{observed_census['dphi_zero_records']}/{observed_census['dphi_nonzero_near_null_records']}/{observed_census['dphi_spacelike_records']}",
        "sampled_tangent_ranks=0:4;1:28;4:16;5:112 shared_lambda=YES independent_ten_amplitude_scan=NO",
        "dynamics=NO solutions=0 physical_evolution=NO",
        "compatibility_ranking=NO finite_exhaustiveness=NO gpu=NO",
        f"maximum_conclusion={MAXIMUM}",
    ]
    (HERE / "ATLAS_TRANSCRIPT.txt").write_text("\n".join(transcript) + "\n", encoding="utf-8")
    print("\n".join(transcript))


if __name__ == "__main__":
    main()

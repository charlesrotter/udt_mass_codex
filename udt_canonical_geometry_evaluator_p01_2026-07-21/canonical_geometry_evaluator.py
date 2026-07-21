#!/usr/bin/env python3
"""Law-neutral local 4D metric/coframe geometry evaluator for P01.

The 2+2 interface is conditional on a supplied base/screen split.  Nothing in
this module selects that split, an action, a source, or a physical solution.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


DIM = 4
ETA = np.diag([-1.0, 1.0, 1.0, 1.0])
SLOT_NAMES = (
    "h00",
    "h01",
    "h11",
    "q22",
    "q23",
    "q33",
    "A2_0",
    "A3_0",
    "A2_1",
    "A3_1",
)


class GeometryInputError(ValueError):
    pass


@dataclass(frozen=True)
class MetricJets:
    metric: np.ndarray
    first: np.ndarray
    second: np.ndarray


@dataclass(frozen=True)
class GeometryEvaluation:
    metric: np.ndarray
    inverse: np.ndarray
    determinant: float
    inertia: tuple[int, int, int]
    christoffel: np.ndarray
    christoffel_first: np.ndarray
    riemann_up: np.ndarray
    riemann_down: np.ndarray
    ricci: np.ndarray
    scalar_curvature: float
    residuals: dict[str, float]


@dataclass(frozen=True)
class CoframeEvaluation:
    metric_jets: MetricJets
    geometry: GeometryEvaluation
    inverse_frame: np.ndarray
    spin_connection: np.ndarray
    spin_connection_first: np.ndarray
    torsion: np.ndarray
    cartan_curvature: np.ndarray
    coordinate_curvature_in_frame: np.ndarray
    residuals: dict[str, float]


@dataclass(frozen=True)
class SplitReconstruction:
    slots: np.ndarray
    base: np.ndarray
    screen: np.ndarray
    shifts: np.ndarray
    block_inverse: np.ndarray
    determinant_factor: float
    residuals: dict[str, float]


@dataclass(frozen=True)
class Jet2:
    value: float
    first: np.ndarray
    second: np.ndarray

    @classmethod
    def constant(cls, value: float) -> "Jet2":
        return cls(float(value), np.zeros(DIM), np.zeros((DIM, DIM)))

    def __add__(self, other: float | "Jet2") -> "Jet2":
        rhs = other if isinstance(other, Jet2) else Jet2.constant(float(other))
        return Jet2(self.value + rhs.value, self.first + rhs.first, self.second + rhs.second)

    __radd__ = __add__

    def __neg__(self) -> "Jet2":
        return Jet2(-self.value, -self.first, -self.second)

    def __sub__(self, other: float | "Jet2") -> "Jet2":
        return self + (-other if isinstance(other, Jet2) else -float(other))

    def __rsub__(self, other: float | "Jet2") -> "Jet2":
        return (-self) + other

    def __mul__(self, other: float | "Jet2") -> "Jet2":
        rhs = other if isinstance(other, Jet2) else Jet2.constant(float(other))
        return Jet2(
            self.value * rhs.value,
            self.first * rhs.value + self.value * rhs.first,
            self.second * rhs.value
            + self.value * rhs.second
            + np.outer(self.first, rhs.first)
            + np.outer(rhs.first, self.first),
        )

    __rmul__ = __mul__


def _as_float_array(value, shape: tuple[int, ...], name: str) -> np.ndarray:
    array = np.asarray(value, dtype=float)
    if array.shape != shape:
        raise GeometryInputError(f"{name} shape {array.shape}, expected {shape}")
    if not np.all(np.isfinite(array)):
        raise GeometryInputError(f"{name} contains non-finite values")
    return array


def _maximum(array: np.ndarray) -> float:
    return float(np.max(np.abs(array))) if array.size else 0.0


def validate_metric_jets(jets: MetricJets, tolerance: float = 2e-10) -> MetricJets:
    metric = _as_float_array(jets.metric, (DIM, DIM), "metric")
    first = _as_float_array(jets.first, (DIM, DIM, DIM), "metric first jet")
    second = _as_float_array(jets.second, (DIM, DIM, DIM, DIM), "metric second jet")
    if _maximum(metric - metric.T) > tolerance:
        raise GeometryInputError("metric is not symmetric")
    if _maximum(first - np.swapaxes(first, 1, 2)) > tolerance:
        raise GeometryInputError("metric first jet is not symmetric in metric indices")
    if _maximum(second - np.swapaxes(second, 0, 1)) > tolerance:
        raise GeometryInputError("metric second jet is not symmetric in derivative indices")
    if _maximum(second - np.swapaxes(second, 2, 3)) > tolerance:
        raise GeometryInputError("metric second jet is not symmetric in metric indices")
    return MetricJets(metric.copy(), first.copy(), second.copy())


def evaluate_metric_jets(jets: MetricJets, tolerance: float = 2e-10) -> GeometryEvaluation:
    jets = validate_metric_jets(jets, tolerance)
    g, dg, ddg = jets.metric, jets.first, jets.second
    try:
        inverse = np.linalg.inv(g)
    except np.linalg.LinAlgError as exc:
        raise GeometryInputError("metric is singular") from exc
    determinant = float(np.linalg.det(g))
    eigenvalues = np.linalg.eigvalsh(g)
    negative = int(np.count_nonzero(eigenvalues < -tolerance))
    positive = int(np.count_nonzero(eigenvalues > tolerance))
    zero = DIM - negative - positive
    inertia = (negative, positive, zero)
    if zero or sorted((negative, positive)) != [1, 3]:
        raise GeometryInputError(f"metric is not Lorentzian: inertia={inertia}")

    inverse_first = np.zeros((DIM, DIM, DIM))
    for k in range(DIM):
        inverse_first[k] = -inverse @ dg[k] @ inverse

    christoffel = np.zeros((DIM, DIM, DIM))
    christoffel_first = np.zeros((DIM, DIM, DIM, DIM))
    for rho in range(DIM):
        for mu in range(DIM):
            for nu in range(DIM):
                h = np.array([dg[mu, sigma, nu] + dg[nu, sigma, mu] - dg[sigma, mu, nu] for sigma in range(DIM)])
                christoffel[rho, mu, nu] = 0.5 * inverse[rho] @ h
                for k in range(DIM):
                    dh = np.array(
                        [
                            ddg[k, mu, sigma, nu]
                            + ddg[k, nu, sigma, mu]
                            - ddg[k, sigma, mu, nu]
                            for sigma in range(DIM)
                        ]
                    )
                    christoffel_first[k, rho, mu, nu] = 0.5 * (
                        inverse_first[k, rho] @ h + inverse[rho] @ dh
                    )

    riemann_up = np.zeros((DIM, DIM, DIM, DIM))
    for rho in range(DIM):
        for sigma in range(DIM):
            for mu in range(DIM):
                for nu in range(DIM):
                    riemann_up[rho, sigma, mu, nu] = (
                        christoffel_first[mu, rho, nu, sigma]
                        - christoffel_first[nu, rho, mu, sigma]
                        + sum(
                            christoffel[rho, mu, lam] * christoffel[lam, nu, sigma]
                            - christoffel[rho, nu, lam] * christoffel[lam, mu, sigma]
                            for lam in range(DIM)
                        )
                    )
    riemann_down = np.einsum("ar,rsuv->asuv", g, riemann_up)
    ricci = np.einsum("rsrn->sn", riemann_up)
    scalar = float(np.einsum("sn,sn", inverse, ricci))

    metric_compatibility = np.zeros((DIM, DIM, DIM))
    for alpha in range(DIM):
        for mu in range(DIM):
            for nu in range(DIM):
                metric_compatibility[alpha, mu, nu] = dg[alpha, mu, nu] - sum(
                    christoffel[rho, alpha, mu] * g[rho, nu]
                    + christoffel[rho, alpha, nu] * g[mu, rho]
                    for rho in range(DIM)
                )
    first_bianchi = np.zeros_like(riemann_down)
    for a in range(DIM):
        for b in range(DIM):
            for c in range(DIM):
                for d in range(DIM):
                    first_bianchi[a, b, c, d] = (
                        riemann_down[a, b, c, d]
                        + riemann_down[a, c, d, b]
                        + riemann_down[a, d, b, c]
                    )

    residuals = {
        "inverse": _maximum(g @ inverse - np.eye(DIM)),
        "christoffel_lower_symmetry": _maximum(christoffel - np.swapaxes(christoffel, 1, 2)),
        "metric_compatibility": _maximum(metric_compatibility),
        "riemann_last_pair_antisymmetry": _maximum(riemann_down + np.swapaxes(riemann_down, 2, 3)),
        "riemann_first_pair_antisymmetry": _maximum(riemann_down + np.swapaxes(riemann_down, 0, 1)),
        "riemann_pair_exchange": _maximum(riemann_down - np.transpose(riemann_down, (2, 3, 0, 1))),
        "first_bianchi": _maximum(first_bianchi),
        "ricci_symmetry": _maximum(ricci - ricci.T),
    }
    return GeometryEvaluation(
        g,
        inverse,
        determinant,
        inertia,
        christoffel,
        christoffel_first,
        riemann_up,
        riemann_down,
        ricci,
        scalar,
        residuals,
    )


def metric_jets_from_coframe(
    coframe,
    coframe_first,
    coframe_second,
    eta=ETA,
    tolerance: float = 2e-10,
) -> MetricJets:
    e = _as_float_array(coframe, (DIM, DIM), "coframe")
    de = _as_float_array(coframe_first, (DIM, DIM, DIM), "coframe first jet")
    dde = _as_float_array(coframe_second, (DIM, DIM, DIM, DIM), "coframe second jet")
    eta_array = _as_float_array(eta, (DIM, DIM), "internal metric")
    if _maximum(eta_array - eta_array.T) > tolerance:
        raise GeometryInputError("internal metric is not symmetric")
    if _maximum(dde - np.swapaxes(dde, 0, 1)) > tolerance:
        raise GeometryInputError("coframe second jet is not symmetric in derivative indices")
    g = e.T @ eta_array @ e
    dg = np.zeros((DIM, DIM, DIM))
    ddg = np.zeros((DIM, DIM, DIM, DIM))
    for a in range(DIM):
        dg[a] = de[a].T @ eta_array @ e + e.T @ eta_array @ de[a]
        for b in range(DIM):
            ddg[a, b] = (
                dde[a, b].T @ eta_array @ e
                + de[a].T @ eta_array @ de[b]
                + de[b].T @ eta_array @ de[a]
                + e.T @ eta_array @ dde[a, b]
            )
    return validate_metric_jets(MetricJets(g, dg, ddg), tolerance)


def evaluate_coframe_jets(
    coframe,
    coframe_first,
    coframe_second,
    eta=ETA,
    tolerance: float = 2e-10,
) -> CoframeEvaluation:
    e = _as_float_array(coframe, (DIM, DIM), "coframe")
    de = _as_float_array(coframe_first, (DIM, DIM, DIM), "coframe first jet")
    dde = _as_float_array(coframe_second, (DIM, DIM, DIM, DIM), "coframe second jet")
    eta_array = _as_float_array(eta, (DIM, DIM), "internal metric")
    metric_jets = metric_jets_from_coframe(e, de, dde, eta_array, tolerance)
    geometry = evaluate_metric_jets(metric_jets, tolerance)
    try:
        inverse_frame = np.linalg.inv(e)
    except np.linalg.LinAlgError as exc:
        raise GeometryInputError("coframe is singular") from exc

    inverse_frame_first = np.zeros((DIM, DIM, DIM))
    for k in range(DIM):
        inverse_frame_first[k] = -inverse_frame @ de[k] @ inverse_frame

    gamma = geometry.christoffel
    dgamma = geometry.christoffel_first
    spin = np.zeros((DIM, DIM, DIM))
    spin_first = np.zeros((DIM, DIM, DIM, DIM))
    bterm = np.zeros((DIM, DIM, DIM))
    for mu in range(DIM):
        for internal in range(DIM):
            for nu in range(DIM):
                bterm[mu, internal, nu] = sum(
                    gamma[rho, mu, nu] * e[internal, rho] for rho in range(DIM)
                ) - de[mu, internal, nu]
            spin[mu, internal] = bterm[mu, internal] @ inverse_frame
            for k in range(DIM):
                db = np.zeros(DIM)
                for nu in range(DIM):
                    db[nu] = (
                        sum(
                            dgamma[k, rho, mu, nu] * e[internal, rho]
                            + gamma[rho, mu, nu] * de[k, internal, rho]
                            for rho in range(DIM)
                        )
                        - dde[k, mu, internal, nu]
                    )
                spin_first[k, mu, internal] = (
                    db @ inverse_frame + bterm[mu, internal] @ inverse_frame_first[k]
                )

    torsion = np.zeros((DIM, DIM, DIM))
    for internal in range(DIM):
        for mu in range(DIM):
            for nu in range(DIM):
                torsion[internal, mu, nu] = (
                    de[mu, internal, nu]
                    - de[nu, internal, mu]
                    + sum(
                        spin[mu, internal, other] * e[other, nu]
                        - spin[nu, internal, other] * e[other, mu]
                        for other in range(DIM)
                    )
                )

    cartan_curvature = np.zeros((DIM, DIM, DIM, DIM))
    frame_curvature = np.zeros((DIM, DIM, DIM, DIM))
    for internal in range(DIM):
        for other in range(DIM):
            for mu in range(DIM):
                for nu in range(DIM):
                    cartan_curvature[internal, other, mu, nu] = (
                        spin_first[mu, nu, internal, other]
                        - spin_first[nu, mu, internal, other]
                        + sum(
                            spin[mu, internal, middle] * spin[nu, middle, other]
                            - spin[nu, internal, middle] * spin[mu, middle, other]
                            for middle in range(DIM)
                        )
                    )
                    frame_curvature[internal, other, mu, nu] = sum(
                        e[internal, rho]
                        * geometry.riemann_up[rho, sigma, mu, nu]
                        * inverse_frame[sigma, other]
                        for rho in range(DIM)
                        for sigma in range(DIM)
                    )

    spin_lower = np.einsum("ik,mkj->mij", eta_array, spin)
    residuals = {
        "coframe_metric_reconstruction": _maximum(metric_jets.metric - e.T @ eta_array @ e),
        "spin_internal_antisymmetry": _maximum(spin_lower + np.swapaxes(spin_lower, 1, 2)),
        "first_cartan_torsion": _maximum(torsion),
        "second_cartan_curvature": _maximum(cartan_curvature - frame_curvature),
    }
    return CoframeEvaluation(
        metric_jets,
        geometry,
        inverse_frame,
        spin,
        spin_first,
        torsion,
        cartan_curvature,
        frame_curvature,
        residuals,
    )


def metric_jets_from_split(slot_values, slot_first, slot_second, tolerance: float = 2e-10) -> MetricJets:
    values = _as_float_array(slot_values, (len(SLOT_NAMES),), "slot values")
    first = _as_float_array(slot_first, (DIM, len(SLOT_NAMES)), "slot first jets")
    second = _as_float_array(slot_second, (DIM, DIM, len(SLOT_NAMES)), "slot second jets")
    if _maximum(second - np.swapaxes(second, 0, 1)) > tolerance:
        raise GeometryInputError("slot second jets are not symmetric in derivative indices")
    jets = [Jet2(values[index], first[:, index], second[:, :, index]) for index in range(len(SLOT_NAMES))]
    h = [[jets[0], jets[1]], [jets[1], jets[2]]]
    q = [[jets[3], jets[4]], [jets[4], jets[5]]]
    shifts = [[jets[6], jets[8]], [jets[7], jets[9]]]  # A[screen][base]
    metric = [[Jet2.constant(0.0) for _ in range(DIM)] for _ in range(DIM)]
    for i in range(2):
        for j in range(2):
            metric[i][j] = h[i][j] + sum(
                (q[a][b] * shifts[a][i] * shifts[b][j] for a in range(2) for b in range(2)),
                Jet2.constant(0.0),
            )
        for b in range(2):
            metric[i][2 + b] = sum(
                (q[a][b] * shifts[a][i] for a in range(2)), Jet2.constant(0.0)
            )
            metric[2 + b][i] = metric[i][2 + b]
    for a in range(2):
        for b in range(2):
            metric[2 + a][2 + b] = q[a][b]
    g = np.array([[metric[mu][nu].value for nu in range(DIM)] for mu in range(DIM)])
    dg = np.array(
        [[[metric[mu][nu].first[k] for nu in range(DIM)] for mu in range(DIM)] for k in range(DIM)]
    )
    ddg = np.array(
        [
            [
                [[metric[mu][nu].second[k, ell] for nu in range(DIM)] for mu in range(DIM)]
                for ell in range(DIM)
            ]
            for k in range(DIM)
        ]
    )
    return validate_metric_jets(MetricJets(g, dg, ddg), tolerance)


def reconstruct_split(metric, tolerance: float = 2e-10) -> SplitReconstruction:
    g = _as_float_array(metric, (DIM, DIM), "metric")
    if _maximum(g - g.T) > tolerance:
        raise GeometryInputError("metric is not symmetric")
    screen = g[2:, 2:].copy()
    try:
        screen_inverse = np.linalg.inv(screen)
    except np.linalg.LinAlgError as exc:
        raise GeometryInputError("screen block is singular") from exc
    screen_eigenvalues = np.linalg.eigvalsh(screen)
    if np.any(screen_eigenvalues <= tolerance):
        raise GeometryInputError("conditional screen block is not positive definite")
    shifts = np.zeros((2, 2))
    for i in range(2):
        shifts[:, i] = screen_inverse @ g[i, 2:]
    base = np.zeros((2, 2))
    for i in range(2):
        for j in range(2):
            base[i, j] = g[i, j] - shifts[:, i] @ screen @ shifts[:, j]
    slots = np.array(
        [
            base[0, 0], base[0, 1], base[1, 1],
            screen[0, 0], screen[0, 1], screen[1, 1],
            shifts[0, 0], shifts[1, 0], shifts[0, 1], shifts[1, 1],
        ]
    )
    base_inverse = np.linalg.inv(base)
    base_eigenvalues = np.linalg.eigvalsh(base)
    if not (base_eigenvalues[0] < -tolerance and base_eigenvalues[1] > tolerance):
        raise GeometryInputError("conditional base block is not Lorentzian")
    block_inverse = np.zeros((DIM, DIM))
    block_inverse[:2, :2] = base_inverse
    block_inverse[:2, 2:] = -base_inverse @ shifts.T
    block_inverse[2:, :2] = -shifts @ base_inverse
    block_inverse[2:, 2:] = screen_inverse + shifts @ base_inverse @ shifts.T
    determinant_factor = float(np.linalg.det(base) * np.linalg.det(screen))
    rebuilt = metric_jets_from_split(slots, np.zeros((DIM, 10)), np.zeros((DIM, DIM, 10))).metric
    residuals = {
        "forward_reverse": _maximum(rebuilt - g),
        "block_inverse": _maximum(block_inverse - np.linalg.inv(g)),
        "determinant_factorization": abs(determinant_factor - float(np.linalg.det(g))),
    }
    return SplitReconstruction(slots, base, screen, shifts, block_inverse, determinant_factor, residuals)


def csn_scaled_metric_jets(jets: MetricJets, omega: float, sigma_first, sigma_second) -> MetricJets:
    jets = validate_metric_jets(jets)
    if not np.isfinite(omega) or omega <= 0:
        raise GeometryInputError("CSN factor must be finite and positive")
    sigma = _as_float_array(sigma_first, (DIM,), "d ln Omega")
    dsigma = _as_float_array(sigma_second, (DIM, DIM), "dd ln Omega")
    if _maximum(dsigma - dsigma.T) > 2e-10:
        raise GeometryInputError("dd ln Omega is not symmetric")
    scale = omega**2
    g = scale * jets.metric
    dg = np.zeros_like(jets.first)
    ddg = np.zeros_like(jets.second)
    for a in range(DIM):
        dg[a] = scale * (jets.first[a] + 2.0 * sigma[a] * jets.metric)
        for b in range(DIM):
            ddg[a, b] = scale * (
                jets.second[a, b]
                + 2.0 * sigma[b] * jets.first[a]
                + 2.0 * sigma[a] * jets.first[b]
                + (2.0 * dsigma[a, b] + 4.0 * sigma[a] * sigma[b]) * jets.metric
            )
    return validate_metric_jets(MetricJets(g, dg, ddg))


def csn_connection_transform(geometry: GeometryEvaluation, sigma_first) -> np.ndarray:
    sigma = _as_float_array(sigma_first, (DIM,), "d ln Omega")
    sigma_up = geometry.inverse @ sigma
    transformed = geometry.christoffel.copy()
    for rho in range(DIM):
        for mu in range(DIM):
            for nu in range(DIM):
                transformed[rho, mu, nu] += (
                    (1.0 if rho == mu else 0.0) * sigma[nu]
                    + (1.0 if rho == nu else 0.0) * sigma[mu]
                    - geometry.metric[mu, nu] * sigma_up[rho]
                )
    return transformed


def constant_linear_coordinate_transform_coframe(
    coframe,
    coframe_first,
    coframe_second,
    jacobian,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    e = _as_float_array(coframe, (DIM, DIM), "coframe")
    de = _as_float_array(coframe_first, (DIM, DIM, DIM), "coframe first jet")
    dde = _as_float_array(coframe_second, (DIM, DIM, DIM, DIM), "coframe second jet")
    jac = _as_float_array(jacobian, (DIM, DIM), "coordinate Jacobian")
    if abs(float(np.linalg.det(jac))) < 1e-12:
        raise GeometryInputError("coordinate Jacobian is singular")
    transformed = e @ jac
    transformed_first = np.einsum("kb,kim,ma->bia", jac, de, jac)
    transformed_second = np.einsum("kb,lc,klim,ma->bcia", jac, jac, dde, jac)
    return transformed, transformed_first, transformed_second


def constant_internal_frame_transform_coframe(
    coframe,
    coframe_first,
    coframe_second,
    lorentz,
    eta=ETA,
    tolerance: float = 2e-10,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    transform = _as_float_array(lorentz, (DIM, DIM), "internal frame transform")
    return local_internal_frame_transform_coframe_jets(
        coframe,
        coframe_first,
        coframe_second,
        transform,
        np.zeros((DIM, DIM, DIM)),
        np.zeros((DIM, DIM, DIM, DIM)),
        eta,
        tolerance,
    )


def local_internal_frame_transform_coframe_jets(
    coframe,
    coframe_first,
    coframe_second,
    lorentz,
    lorentz_first,
    lorentz_second,
    eta=ETA,
    tolerance: float = 2e-10,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Apply a local Lorentz two-jet to a coframe two-jet at one point."""
    e = _as_float_array(coframe, (DIM, DIM), "coframe")
    de = _as_float_array(coframe_first, (DIM, DIM, DIM), "coframe first jet")
    dde = _as_float_array(coframe_second, (DIM, DIM, DIM, DIM), "coframe second jet")
    transform = _as_float_array(lorentz, (DIM, DIM), "internal frame transform")
    dtransform = _as_float_array(lorentz_first, (DIM, DIM, DIM), "internal frame transform first jet")
    ddtransform = _as_float_array(
        lorentz_second, (DIM, DIM, DIM, DIM), "internal frame transform second jet"
    )
    eta_array = _as_float_array(eta, (DIM, DIM), "internal metric")
    if _maximum(dde - np.swapaxes(dde, 0, 1)) > tolerance:
        raise GeometryInputError("coframe second jet is not symmetric in derivative indices")
    if _maximum(ddtransform - np.swapaxes(ddtransform, 0, 1)) > tolerance:
        raise GeometryInputError("internal frame transform second jet is not symmetric")
    if _maximum(transform.T @ eta_array @ transform - eta_array) > tolerance:
        raise GeometryInputError("internal transform is not Lorentz")
    for a in range(DIM):
        first_constraint = dtransform[a].T @ eta_array @ transform + transform.T @ eta_array @ dtransform[a]
        if _maximum(first_constraint) > tolerance:
            raise GeometryInputError("internal transform first jet leaves the Lorentz group")
        for b in range(DIM):
            second_constraint = (
                ddtransform[a, b].T @ eta_array @ transform
                + dtransform[a].T @ eta_array @ dtransform[b]
                + dtransform[b].T @ eta_array @ dtransform[a]
                + transform.T @ eta_array @ ddtransform[a, b]
            )
            if _maximum(second_constraint) > tolerance:
                raise GeometryInputError("internal transform second jet leaves the Lorentz group")
    transformed = transform @ e
    transformed_first = np.zeros_like(de)
    transformed_second = np.zeros_like(dde)
    for a in range(DIM):
        transformed_first[a] = dtransform[a] @ e + transform @ de[a]
        for b in range(DIM):
            transformed_second[a, b] = (
                ddtransform[a, b] @ e
                + dtransform[a] @ de[b]
                + dtransform[b] @ de[a]
                + transform @ dde[a, b]
            )
    return transformed, transformed_first, transformed_second


def residual_maximum(residuals: Iterable[dict[str, float]]) -> float:
    values = [abs(value) for group in residuals for value in group.values()]
    return max(values, default=0.0)

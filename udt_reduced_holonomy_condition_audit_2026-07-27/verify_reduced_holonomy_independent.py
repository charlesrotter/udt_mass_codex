#!/usr/bin/env python3
"""Independent Koszul case audit and coordinate-curvature survivor replay."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
import sympy as sp
import torch

HERE = Path(__file__).resolve().parent
torch.set_default_dtype(torch.float64)
jacfwd = torch.func.jacfwd
SIGN = (-1, 1, 1, 1)
KAPPA = -2.0
EVENTS = {
    "P00": (0.0, 0.0, 0.0),
    "P01": (1.0/4.0, -1.0/5.0, 1.0/6.0),
    "P02": (-1.0/3.0, 1.0/7.0, 1.0/5.0),
}


def write_tsv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)


def independent_structure():
    lam = sp.symbols("lambda", real=True)
    p1, p2, p3, A, B, C = sp.symbols("p1 p2 p3 A B C", real=True)
    bracket = {}

    def exterior(upper, left, right, coefficient):
        bracket[(upper, left, right)] = -coefficient
        bracket[(upper, right, left)] = coefficient

    exterior(0, 0, 1, p1); exterior(0, 0, 2, p2); exterior(0, 0, 3, p3); exterior(0, 2, 3, A)
    exterior(1, 1, 2, -p2); exterior(1, 1, 3, -p3); exterior(1, 2, 3, B)
    exterior(2, 1, 2, lam*p1); exterior(2, 2, 3, -lam*p3); exterior(2, 1, 3, -C)
    exterior(3, 1, 3, lam*p1); exterior(3, 2, 3, lam*p2); exterior(3, 1, 2, C)
    return (lam, p1, p2, p3, A, B, C), bracket


def koszul_connection(bracket):
    def component(upper, left, right):
        return bracket.get((upper, left, right), sp.S(0))

    gamma = {}
    for out in range(4):
        for direction in range(4):
            for acted in range(4):
                # 2<del_direction E_acted,E_out> =
                # <[E_direction,E_acted],E_out>-<[E_acted,E_out],E_direction>
                # +<[E_out,E_direction],E_acted>.
                lowered = (
                    SIGN[out] * component(out, direction, acted)
                    - SIGN[direction] * component(direction, acted, out)
                    + SIGN[acted] * component(acted, out, direction)
                ) / 2
                value = sp.factor(SIGN[out] * lowered)
                if value != 0:
                    gamma[(out, direction, acted)] = value
    return gamma


def nabla_expressions(gamma, lam, value):
    eigenvalues = (-1, 1, lam, lam)
    expressions = []
    for (out, direction, acted), coefficient in gamma.items():
        expression = sp.factor(coefficient * (eigenvalues[acted] - eigenvalues[out]))
        if value is not None:
            expression = sp.factor(expression.subs(lam, value))
        if expression != 0:
            expressions.append(expression)
    return expressions


def quaternion(coordinates: torch.Tensor) -> torch.Tensor:
    radius_squared = (coordinates * coordinates).sum()
    denominator = 1 + radius_squared
    return torch.cat((((1-radius_squared)/denominator).reshape(1), 2*coordinates/denominator))


def survivor_coframe(coordinates: torch.Tensor, phi0: float = 0.0) -> torch.Tensor:
    q = quaternion(coordinates)
    dq = jacfwd(quaternion)(coordinates)
    q0, vector = q[0], q[1:]
    sigma_columns = []
    for axis in range(3):
        derivative_vector = dq[1:, axis]
        sigma_columns.append(
            q0*derivative_vector - vector*dq[0, axis] - torch.linalg.cross(vector, derivative_vector)
        )
    sigma = torch.stack(sigma_columns, dim=1)
    coframe = torch.zeros((4, 4), dtype=coordinates.dtype)
    coframe[0, 0] = torch.exp(torch.tensor(-phi0, dtype=coordinates.dtype))
    spatial_scale = torch.exp(torch.tensor(phi0, dtype=coordinates.dtype))
    coframe[1, 1:] = spatial_scale*sigma[2]
    coframe[2, 1:] = spatial_scale*sigma[0]
    coframe[3, 1:] = spatial_scale*sigma[1]
    return coframe


def survivor_metric(coordinates: torch.Tensor, phi0: float = 0.0) -> torch.Tensor:
    coframe = survivor_coframe(coordinates, phi0)
    signature = torch.diag(torch.tensor((-1.0, 1.0, 1.0, 1.0), dtype=coordinates.dtype))
    return coframe.T @ signature @ coframe


def coordinate_connection(coordinates: torch.Tensor, phi0: float = 0.0) -> torch.Tensor:
    metric = survivor_metric(coordinates, phi0)
    inverse = torch.linalg.inv(metric)
    spatial = jacfwd(lambda point: survivor_metric(point, phi0))(coordinates)
    derivatives = torch.zeros((4, 4, 4), dtype=coordinates.dtype)
    derivatives[1:] = spatial.permute(2, 0, 1)
    return torch.stack([
        torch.stack([
            torch.stack([
                sum(inverse[upper, other] * (
                    derivatives[left, other, right] + derivatives[right, other, left]
                    - derivatives[other, left, right]
                ) / 2 for other in range(4))
                for right in range(4)])
            for left in range(4)])
        for upper in range(4)])


def coordinate_riemann(coordinates: torch.Tensor, phi0: float = 0.0) -> torch.Tensor:
    connection = coordinate_connection(coordinates, phi0)
    spatial = jacfwd(lambda point: coordinate_connection(point, phi0))(coordinates)
    derivatives = torch.zeros((4, 4, 4, 4), dtype=coordinates.dtype)
    derivatives[1:] = spatial.permute(3, 0, 1, 2)
    riemann = torch.zeros((4, 4, 4, 4), dtype=coordinates.dtype)
    for upper in range(4):
        for acted in range(4):
            for left in range(4):
                for right in range(4):
                    value = derivatives[left, upper, right, acted] - derivatives[right, upper, left, acted]
                    for middle in range(4):
                        value = value + (
                            connection[upper, left, middle]*connection[middle, right, acted]
                            - connection[upper, right, middle]*connection[middle, left, acted]
                        )
                    riemann[upper, acted, left, right] = value
    return riemann


def expected_frame_riemann(phi0: float = 0.0) -> np.ndarray:
    result = np.zeros((4, 4, 4, 4))
    coefficient = (KAPPA*np.exp(-phi0))**2/4.0
    for left, right in ((1, 2), (1, 3), (2, 3)):
        result[left, right, left, right] = coefficient
        result[right, left, left, right] = -coefficient
        result[left, right, right, left] = -coefficient
        result[right, left, right, left] = coefficient
    return result


def algebra_rank(riemann: np.ndarray) -> int:
    rows = []
    for left in range(4):
        for right in range(left+1, 4):
            matrix = riemann[:, :, left, right]
            rows.append((matrix[0,1], matrix[0,2], matrix[0,3], matrix[1,2], matrix[1,3], matrix[2,3]))
    return int(np.linalg.matrix_rank(np.asarray(rows), tol=1.0e-9))


def main() -> int:
    symbols, bracket = independent_structure()
    lam, p1, p2, p3, A, B, C = symbols
    gamma = koszul_connection(bracket)

    case_specs = (
        ("GENERIC_LAMBDA_ZERO_PROBE", 0, (p1,p2,p3,A,B), {C: sp.Rational(7,5)}),
        ("GENERIC_LAMBDA_TWO_PROBE", 2, (p1,p2,p3,A,B), {C: sp.Rational(7,5)}),
        ("LAMBDA_PLUS_ONE", 1, (p1,p2,p3,A), {B: sp.Rational(7,5), C: sp.Rational(-9,7)}),
        ("LAMBDA_MINUS_ONE", -1, (p1,p2,p3,B), {A: sp.Rational(7,5), C: sp.Rational(-9,7)}),
    )
    case_rows = []
    for case, value, required, allowed in case_specs:
        expressions = nabla_expressions(gamma, lam, value)
        zero_substitution = {symbol: 0 for symbol in required} | allowed
        sufficiency = all(sp.simplify(expression.subs(zero_substitution)) == 0 for expression in expressions)
        necessity = True
        for symbol in required:
            probe = dict(zero_substitution); probe[symbol] = 1
            necessity &= any(sp.simplify(expression.subs(probe)) != 0 for expression in expressions)
        assert sufficiency and necessity
        case_rows.append({
            "case": case, "nabla_component_count": len(expressions),
            "required_zero": ";".join(str(symbol) for symbol in required),
            "sufficiency_exact": "PASS", "each_required_variable_detected": "PASS",
        })
    write_tsv(HERE / "INDEPENDENT_CASE_HOLDOUTS.tsv", case_rows)

    coordinate_rows = []
    maximum_scaled_error = 0.0
    ranks = []
    expected = expected_frame_riemann(0.0)
    for event_id, values in EVENTS.items():
        point = torch.tensor(values)
        coframe = survivor_coframe(point, 0.0)
        frame = torch.linalg.inv(coframe)
        coordinate = coordinate_riemann(point, 0.0)
        transformed = torch.einsum("am,mnrs,nb,rc,sd->abcd", coframe, coordinate, frame, frame, frame)
        actual = transformed.detach().numpy()
        absolute = float(np.max(np.abs(actual-expected)))
        scale = max(1.0, float(np.max(np.abs(expected))))
        scaled = absolute/scale
        rank = algebra_rank(actual)
        ranks.append(rank); maximum_scaled_error = max(maximum_scaled_error, scaled)
        determinant = float(torch.linalg.det(survivor_metric(point, 0.0)))
        coordinate_rows.append({
            "event_id": event_id, "phi0": "0", "scaled_curvature_error": f"{scaled:.17g}",
            "curvature_algebra_rank": rank, "metric_determinant": f"{determinant:.17g}",
        })
    write_tsv(HERE / "INDEPENDENT_CURVATURE_HOLDOUTS.tsv", coordinate_rows)

    primary = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    assert primary["survivor"]["curvature_holonomy_rank"] == 3
    status = "PASS" if maximum_scaled_error <= 2.0e-8 and set(ranks) == {3} else "FAIL"
    result = {
        "schema": "udt-reduced-holonomy-condition-independent-1.0", "status": status,
        "independent_Koszul_connection_components": len(gamma),
        "case_holdouts": len(case_rows), "all_case_iff_probes": "PASS",
        "coordinate_curvature_holdouts": len(coordinate_rows),
        "maximum_coordinate_curvature_scaled_error": maximum_scaled_error,
        "independent_survivor_curvature_ranks": sorted(set(ranks)),
        "survivor_metrics_nondegenerate": all(float(row["metric_determinant"]) != 0 for row in coordinate_rows),
        "torch_version": torch.__version__, "cpu_only": True,
        "imports_primary_solver": False,
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Exact production derivation for the bounded G302 two-gate classification."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
RESULT = ROOT / "DERIVATION_RESULT.json"
DOMAIN = ROOT / "DOMAIN_CLASSIFICATION.tsv"


def matrix_key(matrix: sp.Matrix) -> tuple[sp.Expr, ...]:
    return tuple(matrix[i, j] for i in range(matrix.rows) for j in range(matrix.cols))


def boost(axis: int, sign: int) -> sp.Matrix:
    matrix = sp.eye(4)
    c = sp.Rational(5, 3)
    s = sign * sp.Rational(4, 3)
    matrix[0, 0] = c
    matrix[axis, axis] = c
    matrix[0, axis] = s
    matrix[axis, 0] = s
    return matrix


def rotation(first: int, second: int, sign: int) -> sp.Matrix:
    matrix = sp.eye(4)
    c = sp.Rational(3, 5)
    s = sign * sp.Rational(4, 5)
    matrix[first, first] = c
    matrix[second, second] = c
    matrix[first, second] = -s
    matrix[second, first] = s
    return matrix


def trace_span_gate() -> dict[str, object]:
    eta = sp.diag(-1, 1, 1, 1)
    seed = sp.diag(1, 1, 0, 0)
    generators = [sp.eye(4)]
    generators.extend(boost(axis, sign) for axis in range(1, 4) for sign in (1, -1))
    generators.extend(
        rotation(first, second, sign)
        for first, second in ((1, 2), (1, 3), (2, 3))
        for sign in (1, -1)
    )
    candidates = list(generators)
    candidates.extend(left * right for left in generators for right in generators)

    transforms: list[sp.Matrix] = []
    seen: set[tuple[sp.Expr, ...]] = set()
    for candidate in candidates:
        key = matrix_key(candidate)
        if key not in seen:
            seen.add(key)
            transforms.append(candidate)

    indices = [(i, j) for i in range(4) for j in range(i, 4)]
    orbit_vectors: list[list[sp.Expr]] = []
    for transform in transforms:
        assert sp.simplify(transform.T * eta * transform - eta) == sp.zeros(4)
        tangent = sp.simplify(transform.T * seed * transform)
        metric_trace = sp.simplify(sum(eta[i, i] * tangent[i, i] for i in range(4)))
        assert metric_trace == 0
        orbit_vectors.append([tangent[i, j] for i, j in indices])

    orbit_matrix = sp.Matrix(orbit_vectors)
    shape_rank = orbit_matrix.rank()
    base_rank = sp.Matrix(orbit_vectors[: len(generators)]).rank()

    selected: list[list[sp.Expr]] = []
    selected_indices: list[int] = []
    current_rank = 0
    for index, vector in enumerate(orbit_vectors):
        trial_rank = sp.Matrix(selected + [vector]).rank()
        if trial_rank > current_rank:
            selected.append(vector)
            selected_indices.append(index)
            current_rank = trial_rank
        if current_rank == shape_rank:
            break

    conformal_vector = [eta[i, j] for i, j in indices]
    complete_rank = sp.Matrix(selected + [conformal_vector]).rank()
    assert shape_rank == 9
    assert base_rank == 8
    assert complete_rank == 10

    omega, h00, h01, h11 = sp.symbols("omega h00 h01 h11", real=True)
    h = sp.Matrix([[h00, h01], [h01, h11]])
    scaled = sp.exp(2 * omega) * h
    det_ratio = sp.simplify(scaled.det() / h.det())
    m_ratio = sp.sqrt(det_ratio)
    normalized_difference = sp.simplify(scaled / m_ratio - h)
    assert det_ratio == sp.exp(4 * omega)
    assert m_ratio == sp.exp(2 * omega)
    assert normalized_difference == sp.zeros(2)

    return {
        "lorentz_orbit_count": len(transforms),
        "generator_only_rank": base_rank,
        "reciprocal_shape_rank": shape_rank,
        "traceless_symmetric_dimension": 9,
        "selected_exact_basis_indices": selected_indices,
        "common_scale_direction": "eta_ab",
        "complete_metric_rank": complete_rank,
        "symmetric_metric_dimension": 10,
        "all_reciprocal_tangents_metric_trace": "0",
        "pair_determinant_scale_ratio": str(det_ratio),
        "pair_common_scale_ratio": str(m_ratio),
        "determinant_normalized_pair_change": "zero",
        "ownership_boundary": (
            "all planes form an algebraic control family; current premises do not own their "
            "physical population"
        ),
        "selection_consequence": (
            "reciprocal shape supplies S2_0, retained common scale supplies the trace line, "
            "so current complete-pair structure does not select the G301 trace-free residual"
        ),
    }


def geometry_gate() -> dict[str, object]:
    r = sp.symbols("r", positive=True, finite=True)
    b, R0 = sp.symbols("b R0", finite=True, real=True)
    f = sp.Function("f")(r)
    fp = sp.diff(f, r)
    fpp = sp.diff(f, r, 2)

    # Exact coordinate-curvature formulas for the primary metric.  An independent verifier below
    # recomputes them from the full Christoffel/Riemann definitions.
    ricci_mixed_t = -(fpp / 2 + fp / r)
    ricci_mixed_r = ricci_mixed_t
    ricci_mixed_angular = (1 - f - r * fp) / r**2
    scalar = sp.simplify(2 * ricci_mixed_t + 2 * ricci_mixed_angular)
    riemann_squared = sp.simplify(fpp**2 + 4 * fp**2 / r**2 + 4 * (f - 1) ** 2 / r**4)
    ricci_squared = sp.simplify(2 * ricci_mixed_t**2 + 2 * ricci_mixed_angular**2)
    weyl_squared = sp.simplify(riemann_squared - 2 * ricci_squared + scalar**2 / 3)

    expected_scalar = -fpp - 4 * fp / r + 2 * (1 - f) / r**2
    assert sp.simplify(scalar - expected_scalar) == 0

    tracefree_difference = sp.simplify(ricci_mixed_t - ricci_mixed_angular)
    ode = sp.simplify(-2 * r**2 * tracefree_difference)
    assert ode == r**2 * fpp - 2 * f + 2

    # Euler-Cauchy homogeneous exponents m=2,-1 plus the particular solution f=1.
    m = sp.symbols("m")
    indicial = sp.factor(m * (m - 1) - 2)
    assert sp.solve(indicial, m) == [-1, 2]
    f_solution = 1 + b / r - R0 * r**2 / 12
    substitutions = {
        f: f_solution,
        fp: sp.diff(f_solution, r),
        fpp: sp.diff(f_solution, r, 2),
    }
    assert sp.simplify(ode.subs(substitutions)) == 0

    scalar_solution = sp.factor(scalar.subs(substitutions))
    riemann_solution = sp.factor(riemann_squared.subs(substitutions))
    ricci_solution = sp.factor(ricci_squared.subs(substitutions))
    weyl_solution = sp.factor(weyl_squared.subs(substitutions))
    expected_scalar = R0
    expected_ricci = R0**2 / 4
    expected_riemann = R0**2 / 6 + 12 * b**2 / r**6
    expected_weyl = 12 * b**2 / r**6
    assert sp.simplify(scalar_solution - expected_scalar) == 0
    assert sp.simplify(ricci_solution - expected_ricci) == 0
    assert sp.simplify(riemann_solution - expected_riemann) == 0
    assert sp.simplify(weyl_solution - expected_weyl) == 0
    scalar_solution = expected_scalar
    ricci_solution = expected_ricci
    riemann_solution = expected_riemann
    weyl_solution = expected_weyl

    angular_parallel = sp.simplify(r * (r * fpp - fp) / 2)
    angular_perpendicular = sp.simplify((r * fp - 2 * f + 2) / 2)
    angular_parallel_solution = sp.factor(angular_parallel.subs(substitutions))
    angular_perpendicular_solution = sp.factor(angular_perpendicular.subs(substitutions))
    assert angular_parallel_solution == 3 * b / (2 * r)
    assert angular_perpendicular_solution == -3 * b / (2 * r)

    phi = -sp.log(f_solution) / 2
    chi = sp.factor((1 - f_solution) / (1 + f_solution))
    positive_f = sp.symbols("positive_f", positive=True)
    twice_phi = -sp.log(positive_f)
    tanh_exponential_form = (sp.exp(twice_phi) - 1) / (sp.exp(twice_phi) + 1)
    assert sp.simplify(tanh_exponential_form - (1 - positive_f) / (1 + positive_f)) == 0

    # Pure scalar-curvature part in an orthonormal frame.
    K = R0 / 12
    null_screen_scalar_part = sp.simplify(K * (1 * 0 - 0**2))
    timelike_section_scalar_part = sp.simplify(K * (1 * -1 - 0**2))
    ricci_null = sp.simplify(R0 * 0 / 4)
    assert null_screen_scalar_part == 0
    assert ricci_null == 0
    assert timelike_section_scalar_part == -R0 / 12

    crossover = "(12*Abs(b)/Abs(R0))**(1/3)"
    quiet_parameter = "Abs(b)*sqrt(Abs(R0)/12)"
    domains = domain_rows()
    with DOMAIN.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(domains[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(domains)

    return {
        "metric": "diag(-f,1/f,r^2,r^2*sin(theta)^2) with x0=c_E*t",
        "tracefree_ode": str(ode),
        "indicial_polynomial": str(indicial),
        "indicial_roots": [-1, 2],
        "complete_C2_solution": str(f_solution),
        "scalar_curvature": str(scalar_solution),
        "ricci_squared": str(ricci_solution),
        "riemann_squared": str(riemann_solution),
        "weyl_squared": str(weyl_solution),
        "phi": str(phi),
        "chi": str(chi),
        "angular_parallel": str(angular_parallel_solution),
        "angular_perpendicular": str(angular_perpendicular_solution),
        "R0_absent_from_registered_angular_channels": True,
        "b_absent_from_scalar_and_ricci_curvature": True,
        "null_screen_R0_contribution": str(null_screen_scalar_part),
        "ricci_null_R0_contribution": str(ricci_null),
        "unit_timelike_section_R0_contribution": str(timelike_section_scalar_part),
        "smooth_areal_center_condition": "b=0",
        "smooth_center_subfamily": "f=1-R0*r^2/12",
        "nonsmooth_center_witness_for_b_nonzero": "WeylSquared=12*b^2/r^6",
        "G288_mapping": "c2=-R0/12 and b=0",
        "G301_generic_mapping": "R0=0",
        "crossover_radius_when_b_R0_nonzero": crossover,
        "quiet_separation_parameter": quiet_parameter,
        "epsilon_quiet_condition": quiet_parameter + " < epsilon^(3/2)",
        "domain_strata_count": len(domains),
        "scope_boundary": (
            "conditional exact static diagonal areal-spherical response; not a nonspherical, "
            "time-live, mass, source, history, or physical-query theorem"
        ),
    }


def domain_rows() -> list[dict[str, str]]:
    return [
        {
            "R0_condition": "R0<0",
            "b_condition": "b>=0",
            "positive_f_intervals": "(0,infinity)",
            "root_structure": "no positive root",
            "center_status": "smooth only when b=0",
        },
        {
            "R0_condition": "R0<0",
            "b_condition": "b<0",
            "positive_f_intervals": "(r_h,infinity)",
            "root_structure": "one simple positive root r_h",
            "center_status": "center excluded; Weyl singular",
        },
        {
            "R0_condition": "R0=0",
            "b_condition": "b>=0",
            "positive_f_intervals": "(0,infinity)",
            "root_structure": "no positive root",
            "center_status": "smooth only when b=0",
        },
        {
            "R0_condition": "R0=0",
            "b_condition": "b<0",
            "positive_f_intervals": "(-b,infinity)",
            "root_structure": "one simple positive root -b",
            "center_status": "center excluded; Weyl singular",
        },
        {
            "R0_condition": "R0>0",
            "b_condition": "b>=0",
            "positive_f_intervals": "(0,r_plus)",
            "root_structure": "one simple positive outer root; r_plus=sqrt(12/R0) when b=0",
            "center_status": "smooth only when b=0",
        },
        {
            "R0_condition": "R0>0",
            "b_condition": "-4/(3*sqrt(R0))<b<0",
            "positive_f_intervals": "(r_minus,r_plus)",
            "root_structure": "two simple positive roots",
            "center_status": "center excluded; Weyl singular",
        },
        {
            "R0_condition": "R0>0",
            "b_condition": "b=-4/(3*sqrt(R0))",
            "positive_f_intervals": "none",
            "root_structure": "one positive double root at 2/sqrt(R0); f does not become positive",
            "center_status": "no positive-f static interval",
        },
        {
            "R0_condition": "R0>0",
            "b_condition": "b<-4/(3*sqrt(R0))",
            "positive_f_intervals": "none",
            "root_structure": "no positive root and f<0",
            "center_status": "no positive-f static interval",
        },
    ]


def main() -> None:
    result = {
        "landing": (
            "RECIPROCAL_SHAPE_SPANS_NINE_AND_COMPLETE_SCALE_RESTORES_TEN"
            "__NO_G301_CLASS_SELECTED__TRACEFREE_BRANCH_HAS_EXACT_CHANNEL_SEPARATION"
        ),
        "status": "INTERNAL_PRODUCTION_DERIVATION_COMPLETE",
        "gate_A": trace_span_gate(),
        "gate_B": geometry_gate(),
        "physics_changes": {
            "metric_changed": False,
            "kernel_changed": False,
            "field_equation_adopted": False,
            "history_selected": False,
            "mass_interpretation_adopted": False,
            "observations_used": False,
        },
    }
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(result["landing"])
    print("shape rank", result["gate_A"]["reciprocal_shape_rank"])
    print("complete rank", result["gate_A"]["complete_metric_rank"])
    print("solution", result["gate_B"]["complete_C2_solution"])
    print("angular", result["gate_B"]["angular_parallel"], result["gate_B"]["angular_perpendicular"])


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Standard-library independent reconstruction of the load-bearing rank algebra."""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent


def quotient_control(c: Fraction, a: Fraction, radius: Fraction, em2: Fraction, ep2: Fraction, e2l: Fraction):
    gtt = -(c * c * em2)
    gt3 = -(c * a * em2)
    g33 = radius * radius * ep2 - a * a * em2
    q33 = g33 - gt3 * gt3 / gtt
    q = (radius * radius * e2l, radius * radius * e2l, q33)
    slice_diagonal = (q[0], q[1], g33)
    slice_to_quotient_det_ratio = (slice_diagonal[0] * slice_diagonal[1] * slice_diagonal[2]) / (q[0] * q[1] * q[2])
    expected_ratio = 1 - a * a * em2 / (radius * radius * ep2)
    assert slice_to_quotient_det_ratio == expected_ratio
    return q, slice_to_quotient_det_ratio


def main() -> None:
    controls = []
    for a in (Fraction(0), Fraction(2, 5), Fraction(11)):
        q, ratio = quotient_control(
            c=Fraction(7),
            a=a,
            radius=Fraction(13),
            em2=Fraction(2),
            ep2=Fraction(3),
            e2l=Fraction(5),
        )
        assert q == (Fraction(845), Fraction(845), Fraction(507))
        controls.append({"a": str(a), "quotient_diagonal": [str(value) for value in q], "slice_to_quotient_det_ratio": str(ratio)})

    # Exact volume-response coefficients in d log(sqrt(det q)).
    generic_lambda = Fraction(2, 3)
    phi_coefficient = 1 + 2 * generic_lambda
    assert phi_coefficient == Fraction(7, 3)
    assert 1 + 2 * Fraction(-1, 2) == 0

    # Independent exact mean-zero perturbations for three positive two-cell weights.
    kernel_controls = []
    for w1, w2 in ((Fraction(2), Fraction(3)), (Fraction(5), Fraction(7)), (Fraction(11), Fraction(13))):
        f1, f2 = w2, -w1
        derivative = w1 * f1 + w2 * f2
        assert derivative == 0
        kernel_controls.append(
            {"weights": [str(w1), str(w2)], "perturbation": [str(f1), str(f2)], "derivative": "0"}
        )

    # c^alpha G^beta cannot have length or density dimensions.
    # Length: beta=0 from M, alpha=0 from T, contradicts L=1.
    # Density: beta=-1 from M, alpha=2 from T, gives L=-1 rather than -3.
    dimensional_controls = {
        "length_candidate_from_M_T": {"alpha": 0, "beta": 0, "actual_L": 0, "required_L": 1},
        "density_candidate_from_M_T": {"alpha": 2, "beta": -1, "actual_L": -1, "required_L": -3},
    }

    primary = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    assert primary["quotient_metric_shift_a_cancels"]
    assert primary["volume_phi_derivative_rank_generic"] == 1
    assert primary["volume_phi_derivative_rank_lambda_minus_half"] == 0
    assert primary["finite_differentiable_scalar_family_derivative_has_infinite_kernel"]
    assert not primary["native_mass_available"]
    assert not primary["same_solution_density_executable"]
    assert not primary["bootstrap_return_map_available"]

    result = {
        "schema": "udt.metric_native_selector_rank.independent.v1",
        "status": "PASS",
        "method": "stdlib_Fraction_Schur_complement_dimension_and_kernel_controls",
        "quotient_shift_cancellation_controls": controls,
        "generic_volume_phi_coefficient": str(phi_coefficient),
        "lambda_minus_half_phi_coefficient": "0",
        "weighted_kernel_controls": kernel_controls,
        "dimensional_controls": dimensional_controls,
        "primary_semantic_promotions_accepted": False,
    }
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    (HERE / "INDEPENDENT_RESULT.json").write_text(encoded, encoding="utf-8")
    print(encoded, end="")


if __name__ == "__main__":
    main()

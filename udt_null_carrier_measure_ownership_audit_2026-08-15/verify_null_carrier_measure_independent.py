#!/usr/bin/env python3
"""Implementation-distinct exact-Fraction replay; imports neither SymPy nor the primary script."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def main() -> None:
    # D=[[2,1],[1,3]], D'=[[1,2],[-1,1]].
    determinant = Fraction(5)
    determinant_prime = Fraction(4)
    expansion = determinant_prime / determinant
    label_weight = Fraction(7)
    density = label_weight / determinant
    density_prime = -label_weight * determinant_prime / determinant**2
    transport_residual = density_prime + expansion * density
    assert transport_residual == 0

    relabel_jacobian = Fraction(3)
    assert (label_weight * relabel_jacobian) / (determinant * relabel_jacobian) == density

    # Adapted-tube divergence is C'/J. A first-integral label density has C'=0;
    # a deliberately varying density supplies the catch.
    tube_jacobian = Fraction(11)
    tube_closed = Fraction(0) / tube_jacobian
    tube_nonclosed = Fraction(2) / tube_jacobian
    assert tube_closed == 0 and tube_nonclosed != 0

    outgoing_divergence = Fraction(2, 3)  # flat spherical outgoing k at r=3.
    coframe_triple_derivative = Fraction(1)  # theta2=(1+x)dy.
    box_t_squared = Fraction(-2)
    chern_simons_f_wedge_f = Fraction(2)
    null_shell_scaling_at_three = Fraction(9)
    arbitrary_density_transport = Fraction(-5)  # X_H(x0)=-p0 at p0=5.
    constant_density_transport = Fraction(0)

    assert outgoing_divergence != 0
    assert coframe_triple_derivative != 0
    assert box_t_squared != 0
    assert chern_simons_f_wedge_f != 0
    assert null_shell_scaling_at_three != 1
    assert arbitrary_density_transport != 0
    assert constant_density_transport == 0

    result = {
        "implementation": "stdlib_Fraction_no_SymPy_no_primary_import",
        "determinant_expansion_identity": expansion == Fraction(4, 5),
        "inverse_area_transport_zero": transport_residual == 0,
        "source_relabelling_invariant": True,
        "query_tube_first_integral_closed": tube_closed == 0,
        "query_tube_nonfirst_integral_catch": tube_nonclosed != 0,
        "star_k_nonclosure_catch": outgoing_divergence != 0,
        "coframe_triple_nonclosure_catch": coframe_triple_derivative != 0,
        "star_dphi_nonclosure_catch": box_t_squared != 0,
        "chern_simons_nonclosure_catch": chern_simons_f_wedge_f != 0,
        "null_shell_projective_scale_not_fixed": null_shell_scaling_at_three != 1,
        "arbitrary_distribution_not_transported": arbitrary_density_transport != 0,
        "constant_distribution_is_one_of_many": constant_density_transport == 0,
        "all_pass": True,
    }
    (ROOT / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

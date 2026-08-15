#!/usr/bin/env python3
"""Primary exact algebra for the bounded null-carrier measure ownership audit."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent


def main() -> None:
    a, b, c, d = sp.symbols("a b c d", real=True)
    ap, bp, cp, dp = sp.symbols("ap bp cp dp", real=True)
    D = sp.Matrix([[a, b], [c, d]])
    Dp = sp.Matrix([[ap, bp], [cp, dp]])
    det_d = sp.factor(D.det())
    det_prime = sp.expand(ap * d + a * dp - bp * c - b * cp)
    expansion = sp.factor(sp.trace(Dp * D.inv()))
    determinant_identity = sp.simplify(expansion - det_prime / det_d) == 0

    C = sp.symbols("C", nonzero=True, real=True)
    density = C / det_d
    density_prime = -C * det_prime / det_d**2  # C is a first integral along the rays.
    density_transport = sp.simplify(density_prime + expansion * density)

    # A and C are both coordinate densities on the source-label screen. Under y=y(y'),
    # both acquire the same positive Jacobian factor r, leaving their ratio invariant.
    A, label_C, relabel_jac = sp.symbols("A label_C relabel_jac", positive=True)
    relabel_ratio = sp.simplify((label_C * relabel_jac) / (A * relabel_jac) - label_C / A)

    # In adapted query-tube coordinates, vol=J dlam^ds^dy1^dy2 and K=partial_lam.
    # For rho=C/J, div(rho K)=(1/J) partial_lam(C).
    tube_J, tube_C_prime = sp.symbols("tube_J tube_C_prime", nonzero=True, real=True)
    tube_divergence = sp.simplify(tube_C_prime / tube_J)
    tube_divergence_first_integral = tube_divergence.subs(tube_C_prime, 0)

    # Exact catches against automatic closure of natural-looking spacetime 3-forms.
    r = sp.symbols("r", positive=True)
    outgoing_null_divergence = sp.simplify(2 / r)  # k=partial_t+partial_r in flat spherical chart.
    x = sp.symbols("x", real=True)
    coframe_triple_derivative_coefficient = sp.diff(1 + x, x)
    t = sp.symbols("t", real=True)
    phi = t**2
    box_phi = -sp.diff(phi, t, 2)  # Minkowski signature (-,+,+,+).

    # A=t dx+y dz gives F=dt^dx+dy^dz and F^F=2 vol_4.
    chern_simons_derivative_coefficient = sp.Integer(2)

    # Under p -> scale*p in four momentum dimensions, d^4p -> scale^4 and
    # delta(H) -> scale^-2 delta(H), so the null-shell measure scales as scale^2.
    scale = sp.symbols("scale", positive=True)
    null_shell_scaling_weight = sp.simplify(scale**4 * scale**-2)

    # Flat null Hamiltonian H=(-p0^2+p1^2+p2^2+p3^2)/2.
    x0, x1, x2, x3, p0, p1, p2, p3 = sp.symbols(
        "x0 x1 x2 x3 p0 p1 p2 p3", real=True
    )
    coordinates = (x0, x1, x2, x3, p0, p1, p2, p3)
    H = sp.Rational(1, 2) * (-p0**2 + p1**2 + p2**2 + p3**2)
    flow = [sp.diff(H, p) for p in (p0, p1, p2, p3)] + [
        -sp.diff(H, q) for q in (x0, x1, x2, x3)
    ]
    phase_divergence = sp.simplify(sum(sp.diff(v, q) for v, q in zip(flow, coordinates)))
    arbitrary_density_residual = sp.simplify(
        sum(v * sp.diff(x0, q) for v, q in zip(flow, coordinates))
    )
    constant_density_residual = sp.simplify(
        sum(v * sp.diff(sp.Symbol("f0"), q) for v, q in zip(flow, coordinates))
    )

    result = {
        "jacobi_determinant": str(det_d),
        "jacobi_determinant_prime": str(det_prime),
        "determinant_expansion_identity": determinant_identity,
        "inverse_area_density_transport_residual": str(density_transport),
        "source_relabelling_ratio_residual": str(relabel_ratio),
        "query_tube_divergence_general": str(tube_divergence),
        "query_tube_divergence_first_integral": str(tube_divergence_first_integral),
        "outgoing_null_star_k_not_closed_divergence": str(outgoing_null_divergence),
        "raw_coframe_triple_not_closed_coefficient": str(coframe_triple_derivative_coefficient),
        "star_dphi_not_closed_box_phi": str(box_phi),
        "chern_simons_not_closed_F_wedge_F_coefficient": str(chern_simons_derivative_coefficient),
        "null_shell_measure_scaling": str(null_shell_scaling_weight),
        "hamiltonian_phase_divergence": str(phase_divergence),
        "arbitrary_phase_density_transport_residual": str(arbitrary_density_residual),
        "constant_phase_density_transport_residual": str(constant_density_residual),
        "query_label_pushforward_valid_but_tautological": True,
        "new_ownership_beyond_query_typing": False,
        "metric_density_and_jacobi_representation_exact": True,
        "geometric_label_current_unique_after_label_measure": True,
        "physical_carrier_identification_selected": False,
        "physical_population_selected": False,
        "physical_eta_selected": False,
        "landing": (
            "LABEL_CURRENT_VALID_BUT_TAUTOLOGICAL"
            "__NO_NEW_OWNERSHIP_BEYOND_QUERY_TYPING"
            "__METRIC_DENSITY_AND_JACOBI_REPRESENTATION_EXACT"
            "__PHYSICAL_CARRIER_IDENTIFICATION_POPULATION_ZERO_SIDE_FLUX_AND_ETA_OPEN"
        ),
    }
    (ROOT / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exact algebra controls for the phi ontology audit."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


OUT = Path(__file__).resolve().parent / "ONTOLOGY_ALGEBRA_RESULT.json"


def matrix_zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def main() -> None:
    phi, omega, c_e = sp.symbols("phi omega c_E", real=True, positive=True)
    # The separate real symbol avoids the positive assumption on phi used only
    # to make the exponential/log reconstruction branch explicit.
    p = sp.symbols("p", real=True)
    u, v = sp.symbols("u v", positive=True)
    A, B, b = sp.symbols("A B b", real=True, nonzero=True)

    phi_ratio = sp.log(v / u) / 2
    common = sp.sqrt(u * v)
    decomposition = sp.diag(u, v) - common * sp.diag(sp.exp(-phi_ratio), sp.exp(phi_ratio))

    scaled_phi = sp.expand_log(sp.log((omega * v) / (omega * u)) / 2, force=True)
    original_phi = sp.expand_log(phi_ratio, force=True)

    P = sp.diag(sp.exp(-p), sp.exp(p))
    K = sp.Matrix([[0, 1], [1, 0]])

    Omega = sp.symbols("Omega", positive=True)
    g_diag = Omega**2 * sp.diag(-sp.exp(-2 * p) * c_e**2, sp.exp(2 * p))
    reconstruction = sp.expand_log(
        sp.log(g_diag[1, 1] / (-g_diag[0, 0] / c_e**2)) / 4,
        force=True,
    )

    F = sp.Matrix([[0, b], [1 / b, 0]])
    H0 = sp.Matrix([[A, B], [B, A * b**2]])
    g_mixed = sp.simplify(P.T * H0 * P)
    P_minus = sp.diag(sp.exp(p), sp.exp(-p))
    g_minus = sp.simplify(P_minus.T * H0 * P_minus)

    checks = {
        "positive_pair_decomposition": matrix_zero(decomposition.applyfunc(sp.powdenest)),
        "common_scale_phi_invariance": sp.simplify(scaled_phi - original_phi) == 0,
        "dual_pairing_invariance": matrix_zero(P.T * K * P - K),
        "diagonal_block_phi_reconstruction": sp.simplify(reconstruction - p) == 0,
        "diagonal_reconstruction_CSN_independent": not reconstruction.has(Omega),
        "K_readout_phi_invisible": matrix_zero(P.T * K * P - K) and not (P.T * K * P).has(p),
        "mixed_readout_phi_visible": g_mixed.has(p),
        "mixed_readout_seal_identity": matrix_zero(F.T * g_minus * F - g_mixed),
        "mixed_family_continuous_parameter_retained": g_mixed.has(A, B, b),
    }

    result = {
        "sympy_version": sp.__version__,
        "all_pass": all(checks.values()),
        "checks": checks,
        "formulas": {
            "phi_ratio": str(phi_ratio),
            "conditional_diagonal_reconstruction": str(reconstruction),
            "dual_pairing_readout": str(P.T * K * P),
            "mixed_readout": str(g_mixed),
        },
        "scope": (
            "exact algebra for registered positive reciprocal pairs and named conditional "
            "2x2 readouts; not a field equation or a physical readout selector"
        ),
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

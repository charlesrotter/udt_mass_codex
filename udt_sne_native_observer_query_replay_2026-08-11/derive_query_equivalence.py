#!/usr/bin/env python3
"""Exact symbolic check of historical SNe formulas under terminal pair retyping."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def require(checks: dict[str, str], name: str, expression: sp.Expr | bool) -> None:
    if not bool(expression):
        raise AssertionError(name)
    checks[name] = "PASS"


def run() -> dict[str, object]:
    phi = sp.symbols("phi", real=True)
    z = sp.symbols("z", positive=True)
    rw, x, n, alpha = sp.symbols("R_w X n alpha", positive=True)
    opz = 1 + z
    substitution = {z: sp.exp(phi) - 1}
    checks: dict[str, str] = {}

    r_phi = {
        "P1": rw * (1 - sp.exp(-2 * phi / n)),
        "P2": 2 * x * phi,
        "P3": x * (sp.exp(2 * phi / alpha) - 1),
    }
    r_z = {
        "P1": rw * (1 - opz ** (-2 / n)),
        "P2": 2 * x * sp.log(opz),
        "P3": x * (opz ** (2 / alpha) - 1),
    }
    for profile in ("P1", "P2", "P3"):
        require(
            checks,
            f"{profile}_r_pair_retype",
            sp.simplify(r_z[profile].subs(substitution) - r_phi[profile]) == 0,
        )
        d_l_phi = sp.exp(2 * phi) * r_phi[profile]
        d_l_z = opz**2 * r_z[profile]
        require(
            checks,
            f"{profile}_dL_pair_retype",
            sp.simplify(d_l_z.subs(substitution) - d_l_phi) == 0,
        )

    require(
        checks,
        "conditional_ceff_redshift_identity",
        sp.simplify(sp.exp(-2 * phi) - (opz ** -2).subs(substitution)) == 0,
    )
    require(
        checks,
        "P1_n1_z_zplus2",
        sp.simplify((opz**2 * r_z["P1"]).subs(n, 1) - rw * z * (z + 2)) == 0,
    )
    require(
        checks,
        "dimensionless_shape_contains_no_cE",
        all("c_E" not in str(value) for value in r_z.values()),
    )

    result = {
        "schema": "udt-sne-query-equivalence-1.0",
        "status": "PASS",
        "sympy": sp.__version__,
        "check_count": len(checks),
        "checks": checks,
        "interpretation": {
            "formula_change_from_retyping": False,
            "phi_pair_identification": "CONDITIONAL_ON_REGISTERED_SNE_QUERY",
            "dA_equals_r": "CONDITIONAL_REGISTERED_READOUT",
            "dL_relation": "CONDITIONAL_REGISTERED_READOUT",
            "c_eff_pair": "CONDITIONAL_PAIR_CONE_READOUT_NOT_SIGNAL_SPEED",
        },
    }
    (HERE / "QUERY_EQUIVALENCE.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"PASS exact_checks={len(checks)}")
    return result


if __name__ == "__main__":
    run()

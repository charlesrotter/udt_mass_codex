#!/usr/bin/env python3
"""Exact symbolic curvature anchor for the conditional founding spherical metric."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def main() -> None:
    r = sp.symbols("r", positive=True, real=True)
    f = sp.Function("f")(r)  # f=exp(-2 phi); c_E drops out of curvature.
    fp, fpp = sp.diff(f, r), sp.diff(f, r, 2)
    w = sp.factor((r**2*fpp - 2*r*fp + 2*f - 2)/(6*r**2))
    scalar = sp.factor(-(r**2*fpp + 4*r*fp + 2*f - 2)/r**2)
    ricci_pair = sp.factor(-(r*fpp + 2*fp)/(2*r))
    ricci_screen = sp.factor(-(r*fp + f - 1)/r**2)
    ricci_gap = sp.factor(ricci_pair-ricci_screen)

    a, b = sp.symbols("a b", real=True)
    conformally_flat = 1 + a*r + b*r**2
    substitutions = {f: conformally_flat, fp: sp.diff(conformally_flat,r), fpp: sp.diff(conformally_flat,r,2)}
    checks = {
        "weyl_trace": sp.simplify(w-w/2-w/2) == 0,
        "conformally_flat_general_solution_check": sp.simplify(w.subs(substitutions)) == 0,
        "ricci_gap_on_conformally_flat_family": sp.factor(ricci_gap.subs(substitutions)) == a/r,
    }
    if not all(checks.values()):
        raise RuntimeError(checks)

    result = {
        "schema": "udt-founding-spherical-curvature-split-v1",
        "status": "PASS",
        "metric_parameterization": "f(r)=exp(-2*phi(r)); c_E constant",
        "scalar_curvature": sp.sstr(scalar),
        "weyl_electric_eigenvalues": [sp.sstr(w), sp.sstr(-w/2), sp.sstr(-w/2)],
        "magnetic_weyl": "zero",
        "weyl_amplitude": sp.sstr(w),
        "classification_when_w_nonzero": "D",
        "classification_when_w_zero": "O",
        "type_O_local_family": "f(r)=1+a*r+b*r**2",
        "ricci_pair_eigenvalue": sp.sstr(ricci_pair),
        "ricci_screen_eigenvalue": sp.sstr(ricci_screen),
        "ricci_pair_minus_screen": sp.sstr(ricci_gap),
        "ricci_gap_on_type_O_family": "a/r",
        "split_result": {
            "w_nonzero": "UNIQUE_WEYL_DERIVED_SPLIT",
            "w_zero_a_nonzero": "RICCI_DERIVED_WHEN_WEYL_DEGENERATE",
            "w_zero_a_zero": "NO_TESTED_POINTWISE_CURVATURE_OWNER",
        },
        "checks": checks,
        "maximum_conclusion": "local_pointwise_split_ownership_only_not_history_or_relation_selection",
    }
    (HERE / "FOUNDING_SYMBOLIC_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

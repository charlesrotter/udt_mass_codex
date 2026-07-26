#!/usr/bin/env python3
"""Independent exact-rational checks; no SymPy or production import."""

from __future__ import annotations

from fractions import Fraction as F
import json


def transpose(a):
    return [list(row) for row in zip(*a)]


def mul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))] for i in range(len(a))]


def sub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def scale(c, a):
    return [[F(c) * value for value in row] for row in a]


def det2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def diag4(a, b, c, d):
    return [[F(a), F(0), F(0), F(0)], [F(0), F(b), F(0), F(0)], [F(0), F(0), F(c), F(0)], [F(0), F(0), F(0), F(d)]]


def check(name, condition, checks):
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def main():
    checks = {}
    X = [[F(-1), F(0)], [F(0), F(1)]]
    Fswap = [[F(0), F(1)], [F(1), F(0)]]
    eta = [[F(-1), F(0)], [F(0), F(1)]]
    check("independent_aligned_self_adjoint", mul(transpose(X), eta) == mul(eta, X), checks)
    check("independent_aligned_swap_anti_isometry", mul(mul(transpose(Fswap), eta), Fswap) == scale(-1, eta), checks)
    check("independent_reciprocal_swap_involutive", mul(Fswap, Fswap) == [[F(1), F(0)], [F(0), F(1)]], checks)

    # Exhaustive bounded integer census backs the symbolic complete family.
    self_adjoint_lorentz = []
    isometric_lorentz = []
    simultaneous = []
    for A in range(-3, 4):
        for B in range(-3, 4):
            for C in range(-3, 4):
                H = [[F(A), F(B)], [F(B), F(C)]]
                if det2(H) >= 0:
                    continue
                self_adjoint = mul(transpose(X), H) == mul(H, X)
                isometric = mul(mul(transpose(Fswap), H), Fswap) == H
                if self_adjoint:
                    self_adjoint_lorentz.append((A, B, C))
                if isometric:
                    isometric_lorentz.append((A, B, C))
                if self_adjoint and isometric:
                    simultaneous.append((A, B, C))
    check("independent_self_adjoint_census_has_B_zero", bool(self_adjoint_lorentz) and all(B == 0 for _, B, _ in self_adjoint_lorentz), checks)
    check("independent_isometric_census_has_C_equal_A", bool(isometric_lorentz) and all(C == A for A, _, C in isometric_lorentz), checks)
    check("independent_simultaneous_Lorentzian_empty", simultaneous == [], checks)
    check("independent_mixed_isometry_requires_nonzero_B", all(B != 0 for _, B, _ in isometric_lorentz), checks)
    check("independent_mixed_eigenline_norms_same", all(A == C for A, _, C in isometric_lorentz), checks)
    # Applying an involutive conformal map twice gives H=omega^2 H; these
    # positive rational controls independently reject nonunit factors.
    for factor in (F(1, 2), F(2), F(3)):
        check(f"independent_positive_nonunit_conformal_rejected_{factor}", factor * factor != 1, checks)

    Hmix = [[F(1), F(-2)], [F(-2), F(1)]]
    Hnull = [[F(0), F(1)], [F(1), F(0)]]
    check("independent_mixed_witness_Lorentzian", det2(Hmix) == -3, checks)
    check("independent_mixed_witness_isometric", mul(mul(transpose(Fswap), Hmix), Fswap) == Hmix, checks)
    check("independent_mixed_witness_not_self_adjoint", mul(transpose(X), Hmix) != mul(Hmix, X), checks)
    check("independent_null_witness_Lorentzian", det2(Hnull) == -1, checks)
    check("independent_null_channels_both_null", Hnull[0][0] == Hnull[1][1] == 0, checks)

    # Complete aligned and mixed lambda=0 controls.
    Xzero = diag4(-1, 1, 0, 0)
    eta4 = diag4(-1, 1, 1, 1)
    F4 = diag4(1, 1, 1, 1)
    F4[0][0] = F4[1][1] = F(0)
    F4[0][1] = F4[1][0] = F(1)
    check("independent_complete_swap_odd", mul(mul(F4, Xzero), F4) == scale(-1, Xzero), checks)
    check("independent_complete_swap_not_aligned_isometry", mul(mul(transpose(F4), eta4), F4) != eta4, checks)
    Hmix4 = diag4(1, 1, 1, 1)
    Hmix4[0][0], Hmix4[0][1], Hmix4[1][0], Hmix4[1][1] = F(1), F(-2), F(-2), F(1)
    check("independent_complete_mixed_swap_isometry", mul(mul(transpose(F4), Hmix4), F4) == Hmix4, checks)
    check("independent_complete_mixed_not_self_adjoint", mul(transpose(Xzero), Hmix4) != mul(Hmix4, Xzero), checks)

    # Direct block-pattern samples for complete self-adjoint strata.
    generic = [
        [F(-2), 0, 0, 0],
        [0, F(3), 0, 0],
        [0, 0, F(2), F(1)],
        [0, 0, F(1), F(2)],
    ]
    plus = [
        [F(-2), 0, 0, 0],
        [0, F(3), F(1), F(1)],
        [0, F(1), F(2), F(1)],
        [0, F(1), F(1), F(2)],
    ]
    minus = [
        [F(-2), 0, F(1), F(1)],
        [0, F(3), 0, 0],
        [F(1), 0, F(2), F(1)],
        [F(1), 0, F(1), F(2)],
    ]
    check("independent_generic_block_self_adjoint", mul(transpose(diag4(-1, 1, 2, 2)), generic) == mul(generic, diag4(-1, 1, 2, 2)), checks)
    check("independent_plus_block_self_adjoint", mul(transpose(diag4(-1, 1, 1, 1)), plus) == mul(plus, diag4(-1, 1, 1, 1)), checks)
    check("independent_minus_block_self_adjoint", mul(transpose(diag4(-1, 1, -1, -1)), minus) == mul(minus, diag4(-1, 1, -1, -1)), checks)

    output = {
        "schema": "udt-calibrated-reciprocal-readout-independent-1.0",
        "result": "PASS",
        "implementation": "python_stdlib_fraction_no_sympy_no_production_import",
        "check_count": len(checks),
        "checks": checks,
        "bounded_integer_census": {
            "range": [-3, 3],
            "self_adjoint_Lorentzian": len(self_adjoint_lorentz),
            "inverting_isometric_Lorentzian": len(isometric_lorentz),
            "simultaneous": len(simultaneous),
        },
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

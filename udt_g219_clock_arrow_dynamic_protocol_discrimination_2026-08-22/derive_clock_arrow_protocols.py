#!/usr/bin/env python3
"""Exact symbolic production derivation for the bounded G219 control."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def check_manifest() -> int:
    rows = HERE.joinpath("SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:]
    for row in rows:
        expected, relative = row.split("\t")
        actual = hashlib.sha256(ROOT.joinpath(relative).read_bytes()).hexdigest()
        assert actual == expected, relative
    return len(rows)


def zero(expr: sp.Expr) -> bool:
    return sp.simplify(sp.expand_trig(expr).rewrite(sp.exp)) == 0


def protocol_record(lhs: str, rhs: sp.Expr, source_clock: sp.Symbol) -> dict[str, str]:
    """Generate both readable and machine-canonical formulas from checked algebra."""
    rhs = sp.simplify(rhs)
    slope = sp.simplify(sp.diff(rhs, source_clock))
    depth = sp.simplify(sp.expand_log(-sp.log(slope), force=True))
    return {
        "map": f"{lhs}={sp.sstr(rhs)}",
        "slope": sp.sstr(slope),
        "depth": sp.sstr(depth),
        "map_canonical": sp.srepr(rhs),
        "slope_canonical": sp.srepr(slope),
        "depth_canonical": sp.srepr(depth),
    }


def derive() -> dict[str, object]:
    eta, a, b, length = sp.symbols("eta a b L", real=True)
    a_radar, a_minus_symbol = sp.symbols("a_radar a_minus", real=True)
    r, c = sp.symbols("r c", positive=True, real=True)
    r1, r2, s1, s2 = sp.symbols("r1 r2 s1 s2", positive=True, real=True)
    C, S, E = sp.cosh(eta), sp.sinh(eta), sp.exp(eta)
    checks: dict[str, bool] = {}

    b_null = E * (a + length)
    checks["outgoing_null_incidence"] = zero((C * b_null - a) - (length + S * b_null))
    null_slope = sp.diff(b_null, a)

    b_afermi = a / C
    checks["A_Fermi_orthogonality"] = zero(C * b_afermi - a)
    a_f = sp.symbols("a_f", real=True)
    b_bfermi = C * a_f + S * length
    bfermi_orthogonality = -C * (a_f - C * b_bfermi) + S * (-length - S * b_bfermi)
    checks["B_Fermi_orthogonality"] = zero(bfermi_orthogonality)

    a_minus = sp.exp(-eta) * b - length
    a_plus = E * b + length
    radar_time = sp.simplify((a_minus + a_plus) / 2)
    radar_range = sp.simplify((a_plus - a_minus) / 2)
    checks["radar_time_equals_A_Fermi_time"] = zero(radar_time - C * b)
    checks["radar_range_is_B_position"] = zero(radar_range - (length + S * b))

    a_inverse = sp.exp(-eta) * b - length
    a_return = E * b + length
    checks["inverse_recovers_emission"] = zero(a_inverse.subs(b, b_null) - a)
    checks["future_return_is_null"] = zero((a_return - C * b) - (length + S * b))
    echo = sp.simplify(a_return.subs(b, b_null))
    checks["echo_slope"] = zero(sp.diff(echo, a) - sp.exp(2 * eta))
    checks["inverse_not_return_symbolically"] = not zero(a_inverse - a_return)

    delta = -sp.log(r)
    clock_T, ruler_L = r, 1 / r
    q = sp.simplify(clock_T / ruler_L)
    chi = sp.simplify((ruler_L - clock_T) / (ruler_L + clock_T))
    checks["founded_determinant_one"] = sp.simplify(clock_T * ruler_L - 1) == 0
    checks["q_factor"] = sp.simplify(q - r**2) == 0
    checks["chi_factor"] = sp.simplify(chi - (1 - r**2) / (1 + r**2)) == 0
    checks["reversal_depth"] = sp.simplify(-sp.log(1 / r) + delta) == 0

    composite = r2 * (r1 * a + s1) + s2
    checks["matched_chain_rule"] = sp.diff(composite, a) == r1 * r2
    checks["depth_composition"] = sp.expand_log(-sp.log(r1 * r2), force=True) == -sp.log(r1) - sp.log(r2)
    mutation = r * a + c * a**2
    checks["mutation_incidence"] = mutation.subs(a, 0) == 0
    checks["mutation_first_jet"] = sp.diff(mutation, a).subs(a, 0) == r
    checks["mutation_second_jet"] = sp.diff(mutation, a, 2).subs(a, 0) == 2 * c

    assert all(checks.values()), {key: value for key, value in checks.items() if not value}
    protocols = {
        "null_A_emit_to_B_receive": protocol_record("b", b_null, a),
        "A_Fermi": protocol_record("b", b_afermi, a),
        "B_Fermi_as_A_to_B_relation": protocol_record("b", b_bfermi.subs(a_f, a), a),
        "A_radar_simultaneity": protocol_record("b", a_radar / C, a_radar),
        "null_mathematical_inverse": protocol_record("a", a_inverse, b),
        "future_return_B_to_A": protocol_record("a_plus", a_return, b),
        "A_echo": protocol_record(
            "a_plus", length + sp.exp(2 * eta) * (a_minus_symbol + length), a_minus_symbol
        ),
    }
    return {"manifest_files": check_manifest(), "checks": checks, "protocols": protocols}


if __name__ == "__main__":
    print(json.dumps(derive(), indent=2, sort_keys=True))

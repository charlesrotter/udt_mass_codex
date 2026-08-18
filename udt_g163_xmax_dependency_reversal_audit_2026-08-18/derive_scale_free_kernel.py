#!/usr/bin/env python3
"""Exact production algebra for the preregistered G163 dependency reversal."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUTCOME = "SCALE_FREE_KERNEL_CLOSES__XMAX_IS_DIMENSIONAL_NULL_DIRECTION__DEPENDENCY_REVERSAL_REQUIRED"


def source_gate() -> int:
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(rows) == 26
    for row in rows:
        payload = (ROOT / row["path"]).read_bytes()
        assert len(payload) == int(row["bytes"])
        assert hashlib.sha256(payload).hexdigest() == row["sha256"]
    return len(rows)


def z(expr):
    assert sp.simplify(expr) == 0, sp.simplify(expr)


def main() -> None:
    source_count = source_gate()
    checks: list[str] = []

    T, L, q1, q2, scale = sp.symbols("T L q1 q2 scale", positive=True)
    phi, X, ell0 = sp.symbols("phi X ell0", real=True, positive=True)

    q = T / L
    chi = (L - T) / (L + T)
    z(chi - (1 - q) / (1 + q))
    checks.append("projective_pair_identity")

    q_from_chi = (1 - chi) / (1 + chi)
    z(q_from_chi - q)
    checks.append("projective_inverse")

    c1 = (1 - q1) / (1 + q1)
    c2 = (1 - q2) / (1 + q2)
    c12 = (1 - q1 * q2) / (1 + q1 * q2)
    z(c12 - (c1 + c2) / (1 + c1 * c2))
    checks.append("mobius_composition_from_ratio_multiplication")

    z(((1 - (1 / q)) / (1 + (1 / q))) + chi)
    checks.append("reversal")

    chi_phi = sp.tanh(phi)
    z(sp.diff(chi_phi, phi) - (1 - chi_phi**2))
    checks.append("scale_free_first_differential")

    # Positivity of T,L gives |L-T| < L+T; verify the exact positive gap.
    z((L + T) ** 2 - (L - T) ** 2 - 4 * L * T)
    checks.append("bounded_open_interval_gap")

    # Common rescaling changes metric scale but not reciprocal shape.
    T2, L2 = scale * T, scale * L
    z((L2 - T2) / (L2 + T2) - chi)
    z(T2 / L2 - q)
    z((T2 * L2) ** 2 - scale**4 * (T * L) ** 2)
    checks.append("common_rescaling_preserves_kernel_changes_volume")

    # Native residuals contain no X: the exact identifiability Jacobian has rank zero.
    native = sp.Matrix([
        q - T / L,
        chi - (1 - q) / (1 + q),
        c12 - (c1 + c2) / (1 + c1 * c2),
        sp.diff(chi_phi, phi) - (1 - chi_phi**2),
    ])
    jac_x = native.jacobian([X])
    assert jac_x == sp.zeros(native.rows, 1)
    assert jac_x.rank() == 0
    checks.append("native_xmax_identifiability_rank_zero")

    # The same local slope and reciprocal depth admit every positive finite asymptote.
    delta = sp.symbols("delta", real=True)
    Xp, ellp = sp.symbols("Xp ellp", positive=True)
    x_finite = Xp * sp.tanh(ellp * delta / Xp)
    z(sp.diff(x_finite, delta).subs(delta, 0) - ellp)
    assert sp.limit(x_finite, delta, sp.oo) == Xp
    assert sp.limit(x_finite, delta, -sp.oo) == -Xp
    checks.append("arbitrary_finite_asymptote_same_local_slope")

    # An unbounded dimensional marking has the same local slope unless boundedness is separately owned.
    x_unbounded = ellp * delta
    z(sp.diff(x_unbounded, delta) - ellp)
    assert sp.limit(x_unbounded, delta, sp.oo) == sp.oo
    checks.append("unbounded_marking_countermodel")

    # A dimensionful Mobius display composes only after its scale is supplied.
    a, b = sp.symbols("a b")
    x1, x2 = Xp * a, Xp * b
    z((x1 + x2) / (1 + x1 * x2 / Xp**2) - Xp * (a + b) / (1 + a * b))
    checks.append("dimensionful_mobius_scale_is_inserted_parameter")

    # c_E and G_obs alone cannot produce a length monomial.
    alpha, beta = sp.symbols("alpha beta")
    solution = sp.linsolve([
        -beta,
        -alpha - 2 * beta,
        alpha + 3 * beta - 1,
    ], (alpha, beta))
    assert solution is sp.EmptySet
    checks.append("ce_g_dimensional_length_no_go")

    with (HERE / "DEPENDENCY_LEDGER_PREREG.tsv").open(newline="", encoding="utf-8") as handle:
        ledger = list(csv.DictReader(handle, delimiter="\t"))
    assert [row["id"] for row in ledger] == [f"G{i}" for i in range(135, 155)]
    assert len({row["expected_class"] for row in ledger}) >= 8
    checks.append("complete_g135_g154_dependency_inventory")

    result = {
        "status": "PASS",
        "registered_outcome_class": OUTCOME,
        "source_count": source_count,
        "exact_checks": len(checks),
        "exact_check_names": checks,
        "native_xmax_jacobian_rank": 0,
        "dimensionless_bound_derived": True,
        "dimensionful_xmax_derived": False,
        "dependency_rows": len(ledger),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

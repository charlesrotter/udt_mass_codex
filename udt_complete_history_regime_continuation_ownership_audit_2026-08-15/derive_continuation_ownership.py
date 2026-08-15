#!/usr/bin/env python3
"""Exact bounded ownership test for complete UDT regime continuations."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
T = sp.symbols("t", positive=True)
ETA2 = sp.diag(-1, 1)
ETA4 = sp.diag(-1, 1, 1, 1)


def zero_matrix(matrix: sp.Matrix) -> bool:
    return all(sp.factor(sp.cancel(value)) == 0 for value in matrix)


def source_hashes_ok() -> bool:
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        rows = csv.DictReader(handle, delimiter="\t")
        for row in rows:
            data = (ROOT / row["path"]).read_bytes()
            if row["path"] == "CURRENT_SCIENTIFIC_PREMISES.tsv":
                lines = data.splitlines(keepends=True)
                if not lines or not lines[-1].startswith(b"G98\t"):
                    return False
                data = b"".join(lines[:-1])
            digest = hashlib.sha256(data).hexdigest()
            if digest != row["sha256"]:
                return False
    return True


def complete_coframe() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix]:
    sigma = 1 + T / 31
    beta = T / 37
    B = sp.Matrix([[sigma / T, sigma * beta / T], [0, sigma * T]])
    Q = sp.Matrix([[1 + T / 7, T / 11], [0, 1 + T / 13]])
    S = sp.Matrix([[T / 17, T**2 / 19], [T**3 / 23, T**4 / 29]])
    E = B.row_join(sp.zeros(2)).col_join((Q * S).row_join(Q))
    return B, Q, S, E


def target(kind: str) -> tuple[sp.Matrix, sp.Expr, sp.Expr]:
    clock = 1 / T
    if kind == "flat":
        ruler = T
    elif kind == "monotone":
        ruler = T**2
    elif kind == "loud_quiet_loud":
        w = (T - sp.Rational(1, 2)) * (sp.Rational(3, 2) - T)
        ruler = T / w**2
    else:
        raise ValueError(kind)

    # Both base and screen components are present while the two columns remain orthogonal.
    r = sp.Rational(1, 10)
    s = sp.Rational(1, 20) if kind != "loud_quiet_loud" else sp.Rational(1, 4) + 3 * (T - 1) ** 2
    u0 = clock * (1 + r**2) / (1 - r**2)
    a0 = clock * 2 * r / (1 - r**2)
    u1 = ruler * (1 - s**2) / (1 + s**2)
    a1 = ruler * 2 * s / (1 + s**2)
    return sp.diag(u0, u1).col_join(sp.diag(a0, a1)), clock, ruler


def family(kind: str) -> dict[str, object]:
    B, Q, S, E = complete_coframe()
    V, clock, ruler = target(kind)
    J = sp.simplify(E.inv() * V)
    Y, Z = J[:2, :], J[2:, :]
    h = sp.simplify(J.T * E.T * ETA4 * E * J)
    expected = sp.diag(-clock**2, ruler**2)

    derivatives = {name: matrix.diff(T) for name, matrix in (("B", B), ("Q", Q), ("S", S), ("Y", Y), ("Z", Z))}
    all_live = all(any(sp.simplify(x.subs(T, 1)) != 0 for x in matrix) for matrix in derivatives.values())
    all_s_live = all(sp.simplify(x.subs(T, 1)) != 0 for x in derivatives["S"])

    U = sp.simplify(B * Y)
    R = sp.simplify(S * Y + Z)
    A = sp.simplify(Q * R)
    Bd, Qd, Sd, Yd, Zd = (derivatives[name] for name in ("B", "Q", "S", "Y", "Z"))
    Ud_B = Bd * Y
    Ud_Y = B * Yd
    Ad_Q = Qd * R
    Ad_S = Q * Sd * Y
    Ad_Y = Q * S * Yd
    Ad_Z = Q * Zd
    contributions = {
        "B": sp.simplify(Ud_B.T * ETA2 * U + U.T * ETA2 * Ud_B),
        "Q": sp.simplify(Ad_Q.T * A + A.T * Ad_Q),
        "S": sp.simplify(Ad_S.T * A + A.T * Ad_S),
        "Y": sp.simplify(Ud_Y.T * ETA2 * U + U.T * ETA2 * Ud_Y + Ad_Y.T * A + A.T * Ad_Y),
        "Z": sp.simplify(Ad_Z.T * A + A.T * Ad_Z),
    }
    every_contribution_live = all(
        any(sp.simplify(x.subs(T, 1)) != 0 for x in matrix) for matrix in contributions.values()
    )
    contribution_partition = zero_matrix(h.diff(T) - sum(contributions.values(), sp.zeros(2)))

    phi_pair = sp.factor(sp.Rational(1, 4) * sp.log((-h.det()) / h[0, 0] ** 2))
    phi_base = sp.log(T)
    modulation = sp.expand_log(phi_pair - phi_base, force=True)
    exp4m = sp.factor(((-h.det()) / h[0, 0] ** 2) / T**4)

    if kind == "flat":
        shape_checks = {"flat": sp.factor(exp4m - 1) == 0}
    elif kind == "monotone":
        shape_checks = {
            "monotone_exact": sp.factor(exp4m - T**2) == 0,
            "monotone_positive_at_control": bool(sp.diff(exp4m, T).subs(T, 1) > 0),
        }
    else:
        w = (T - sp.Rational(1, 2)) * (sp.Rational(3, 2) - T)
        shape_checks = {
            "lql_exact": sp.factor(exp4m - w**-4) == 0,
            "lql_stationary": sp.factor(sp.diff(exp4m, T).subs(T, 1)) == 0,
            "lql_strict_minimum": bool(sp.diff(exp4m, T, 2).subs(T, 1) > 0),
            "lql_left_divergence": sp.limit(exp4m, T, sp.Rational(1, 2), dir="+") == sp.oo,
            "lql_right_divergence": sp.limit(exp4m, T, sp.Rational(3, 2), dir="-") == sp.oo,
        }

    checks = {
        "factorization": zero_matrix(E * J - V),
        "target_metric": zero_matrix(h - expected),
        "rank_two": J.subs(T, 1).rank() == 2,
        "regular": bool(h[0, 0].subs(T, 1) < 0 and h.det().subs(T, 1) < 0),
        "all_B_Q_S_Y_Z_live": all_live,
        "all_four_S_entries_live": all_s_live,
        "all_five_h_contributions_live": every_contribution_live,
        "exact_hdot_contribution_partition": contribution_partition,
        **shape_checks,
    }
    return {
        "kind": kind,
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "exp_4_terminal_modulation": str(exp4m),
        "terminal_modulation": str(modulation),
    }


def owner_summary() -> dict[str, object]:
    with (HERE / "CANDIDATE_OWNER_ATLAS.tsv").open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    active_owners = [row["candidate_id"] for row in rows if row["active_native_nonidentity_history_rule"] == "yes"]
    return {
        "candidate_count": len(rows),
        "active_native_history_owner_count": len(active_owners),
        "active_native_history_owners": active_owners,
    }


def main() -> None:
    families = [family(kind) for kind in ("flat", "monotone", "loud_quiet_loud")]
    owners = owner_summary()
    checks = {
        "source_hashes": source_hashes_ok(),
        "three_separating_families": len(families) == 3,
        "all_family_checks": all(item["all_checks_pass"] for item in families),
        "no_active_native_history_owner": owners["active_native_history_owner_count"] == 0,
    }
    result = {
        "schema": "udt.complete_history_regime_continuation_ownership.v1",
        "landing": "PERMITTED_NOT_OWNED",
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "families": families,
        "owner_summary": owners,
        "maximum_conclusion": "No active equation in the frozen source universe owns a unique or separating complete-history regime continuation on the tested regular stratum.",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Independent Fraction replay; imports neither SymPy nor the production derivation."""

from __future__ import annotations

import csv
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def eye(n: int) -> list[list[F]]:
    return [[F(i == j) for j in range(n)] for i in range(n)]


def transpose(a: list[list[F]]) -> list[list[F]]:
    return [list(row) for row in zip(*a)]


def multiply(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))] for i in range(len(a))]


def inverse(a: list[list[F]]) -> list[list[F]]:
    n = len(a)
    work = [row[:] + ident for row, ident in zip(a, eye(n))]
    for col in range(n):
        pivot = next(row for row in range(col, n) if work[row][col])
        work[col], work[pivot] = work[pivot], work[col]
        scale = work[col][col]
        work[col] = [value / scale for value in work[col]]
        for row in range(n):
            if row == col:
                continue
            factor = work[row][col]
            work[row] = [x - factor * y for x, y in zip(work[row], work[col])]
    return [row[n:] for row in work]


def block_coframe(t: F) -> tuple[list[list[F]], list[list[F]], list[list[F]], list[list[F]]]:
    sigma = 1 + t / 31
    beta = t / 37
    b = [[sigma / t, sigma * beta / t], [F(0), sigma * t]]
    q = [[1 + t / 7, t / 11], [F(0), 1 + t / 13]]
    s = [[t / 17, t**2 / 19], [t**3 / 23, t**4 / 29]]
    qs = multiply(q, s)
    e = [b[0] + [F(0), F(0)], b[1] + [F(0), F(0)], qs[0] + q[0], qs[1] + q[1]]
    return b, q, s, e


def target(t: F, kind: str) -> list[list[F]]:
    clock = 1 / t
    if kind == "flat":
        ruler, s = t, F(1, 20)
    elif kind == "monotone":
        ruler, s = t**2, F(1, 20)
    elif kind == "loud_quiet_loud":
        w = (t - F(1, 2)) * (F(3, 2) - t)
        ruler, s = t / w**2, F(1, 4) + 3 * (t - 1) ** 2
    else:
        raise ValueError(kind)
    r = F(1, 10)
    u0 = clock * (1 + r**2) / (1 - r**2)
    a0 = clock * 2 * r / (1 - r**2)
    u1 = ruler * (1 - s**2) / (1 + s**2)
    a1 = ruler * 2 * s / (1 + s**2)
    return [[u0, F(0)], [F(0), u1], [a0, F(0)], [F(0), a1]]


def pair_metric(v: list[list[F]]) -> list[list[F]]:
    eta_v = [[-x for x in v[0]], v[1][:], v[2][:], v[3][:]]
    return multiply(transpose(v), eta_v)


def exp4m(h: list[list[F]], t: F) -> F:
    det = h[0][0] * h[1][1] - h[0][1] * h[1][0]
    return ((-det) / h[0][0] ** 2) / t**4


def source_hashes_ok() -> bool:
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            data = (ROOT / row["path"]).read_bytes()
            if row["path"] == "CURRENT_SCIENTIFIC_PREMISES.tsv":
                lines = data.splitlines(keepends=True)
                if not lines or not lines[-1].startswith(b"G98\t"):
                    return False
                data = b"".join(lines[:-1])
            if hashlib.sha256(data).hexdigest() != row["sha256"]:
                return False
    return True


def main() -> None:
    times = [F(3, 4), F(1), F(5, 4)]
    kinds = ["flat", "monotone", "loud_quiet_loud"]
    checks: dict[str, bool] = {"source_hashes": source_hashes_ok()}
    snapshots: dict[str, object] = {}
    for kind in kinds:
        values = []
        states = []
        for t in times:
            b, q, s, e = block_coframe(t)
            v = target(t, kind)
            j = multiply(inverse(e), v)
            h = pair_metric(multiply(e, j))
            checks[f"{kind}_factorization_{t}"] = multiply(e, j) == v
            checks[f"{kind}_regular_{t}"] = h[0][0] < 0 and h[0][0] * h[1][1] - h[0][1] * h[1][0] < 0
            values.append(exp4m(h, t))
            states.append((b, q, s, j[:2], j[2:]))
        checks[f"{kind}_B_Q_S_Y_Z_change"] = all(states[0][i] != states[2][i] for i in range(5))
        checks[f"{kind}_all_S_entries_change"] = all(states[0][2][i][j] != states[2][2][i][j] for i in range(2) for j in range(2))
        snapshots[kind] = [str(value) for value in values]

    checks["flat_shape"] = snapshots["flat"] == ["1", "1", "1"]
    checks["monotone_shape"] = snapshots["monotone"] == [str(t**2) for t in times]
    lql = [F(1, ((t - F(1, 2)) * (F(3, 2) - t)) ** 4) for t in times]
    checks["lql_shape"] = snapshots["loud_quiet_loud"] == [str(value) for value in lql]
    checks["lql_quiet_middle"] = lql[0] > lql[1] and lql[2] > lql[1] and lql[0] == lql[2]

    with (HERE / "CANDIDATE_OWNER_ATLAS.tsv").open(newline="") as handle:
        owners = list(csv.DictReader(handle, delimiter="\t"))
    checks["fifteen_candidates"] = len(owners) == 15
    checks["no_active_native_owner"] = all(row["active_native_nonidentity_history_rule"] == "no" for row in owners)
    checks["conditional_actions_not_active"] = all(
        row["active_native_nonidentity_history_rule"] == "no" for row in owners if row["candidate_id"] in {"O11", "O12"}
    )
    checks["observation_not_native_owner"] = next(row for row in owners if row["candidate_id"] == "O14")["active_native_nonidentity_history_rule"] == "no"

    primary = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    checks["primary_landing"] = primary["landing"] == "PERMITTED_NOT_OWNED"
    checks["primary_pass"] = primary["all_checks_pass"] is True

    result = {
        "schema": "udt.complete_history_regime_continuation_independent.v1",
        "method": "stdlib Fraction matrix replay; no SymPy and no production import",
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "exact_exp_4M_samples": snapshots,
        "caveat": "Exact rational samples independently support the symbolic family theorem; they are not a second symbolic proof of all-domain derivatives or limits.",
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

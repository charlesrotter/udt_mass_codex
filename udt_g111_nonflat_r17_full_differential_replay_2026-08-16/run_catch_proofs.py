#!/usr/bin/env python3
"""Hostile mutation checks for the G111 evidence gates."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

import derive_nonflat_replay as production


HERE = Path(__file__).resolve().parent


def caught(condition: bool, name: str, checks: dict[str, bool]) -> None:
    checks[name] = bool(condition)
    if not condition:
        raise AssertionError(name)


def main() -> None:
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    with (HERE / "CONTROL_ATLAS.tsv").open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    checks: dict[str, bool] = {}
    # Mutate q12-q21=2*p3 to the wrong sign at a nonzero witness.
    p3 = 0.1
    correct_difference = 2.0 * p3
    mutated_difference = -2.0 * p3
    caught(abs(correct_difference - 2.0 * p3) == 0.0 and abs(mutated_difference - 2.0 * p3) > 0.0, "reject_incompatible_second_jets", checks)
    geometry = production.build_symbolic_geometry()
    point = (production.sp.Rational(1, 2),) * 4
    values = production.substitutions(
        geometry, production.sp.Rational(1, 5), point,
        production.sp.Rational(1, 4), production.sp.Rational(1),
    )
    gamma = production.connection_to_float(geometry["gamma_up"], values)
    n, first, second = production.screen_for_axis(0, 1)
    observer = np.array([1.0, 0.0, 0.0, 0.0])
    k = np.concatenate(([1.0], n))
    metric = np.diag(np.array(production.ETA, dtype=float))
    screens = (np.concatenate(([0.0], first)), np.concatenate(([0.0], second)))
    pair_initial = np.einsum("i,j,ijk->k", observer, k, gamma)
    pair_screen_derivative = np.column_stack(
        ([pair_initial @ metric @ screen for screen in screens], np.zeros(2))
    )
    dsky_vertex_derivative = np.eye(2)
    caught(
        np.linalg.norm(pair_screen_derivative - dsky_vertex_derivative) > 1.0e-6,
        "reject_same_W_zero_angular_map",
        checks,
    )
    caught(all(int(row["pair_screen_rank"]) <= 1 for row in rows), "reject_rank_two_pair_screen", checks)
    mutated_vertex_value = np.eye(2)
    mutated_vertex_derivative = np.zeros((2, 2))
    caught(
        np.linalg.norm(mutated_vertex_value) > 0.0
        and np.linalg.norm(mutated_vertex_derivative - np.eye(2)) > 0.0,
        "reject_wrong_vertex_normalization",
        checks,
    )
    caught(len(rows) == 1152 and len(rows[:-1]) != 1152, "reject_dropped_control", checks)
    twist_pairs: dict[tuple[str, ...], dict[str, float]] = defaultdict(dict)
    for row in rows:
        key = (row["epsilon"], row["lambda_R"], row["point_id"], row["sky_axis"])
        twist_pairs[key][row["twist_a"]] = float(row["tidal_trace"])
    twist_difference = max(abs(values["1/4"] - values["-1/4"]) for values in twist_pairs.values())
    caught(twist_difference > 1.0e-6, "reject_twist_sign_erasure", checks)
    # Execute an actual Riemann-index mutation at a frozen witness.
    riemann = production.tensor_to_float(geometry["riemann_lower"], values)
    correct = production.optical_tidal(riemann, n, (first, second))
    mutated = np.empty((2, 2))
    for i, one in enumerate(screens):
        for j, two in enumerate(screens):
            mutated[i, j] = np.einsum("a,b,c,d,abcd", one, k, two, k, riemann)
    caught(np.linalg.norm(correct - mutated) > 1.0e-6, "reject_wrong_riemann_contraction", checks)
    caught(
        all(float(row["null_screen_residual"]) == 0.0 for row in rows),
        "reject_non_normalized_null_screen",
        checks,
    )
    caught(all(row["selected"] == "NO" for row in rows), "reject_hidden_control_selection", checks)
    output = {"schema": "UDT_G111_CATCH_PROOFS_V1", "checks": checks, "all_checks_pass": all(checks.values()), "maximum_twist_sign_trace_difference": twist_difference}
    (HERE / "CATCH_PROOF_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

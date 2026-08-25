#!/usr/bin/env python3
"""Hostile in-memory mutation catches for the G254 closure contract."""

from __future__ import annotations

import argparse
import copy
import csv
import json
from pathlib import Path

from derive_closure_census import counterfamily_record, validate_contract, validate_witness


PACKAGE = Path(__file__).resolve().parent


def read_contract() -> list[dict[str, str]]:
    with (PACKAGE / "CLOSURE_CONTRACT.tsv").open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def must_fail(label, callback):
    try:
        callback()
    except (AssertionError, KeyError):
        return {"mutation": label, "caught": True}
    raise AssertionError(f"mutation escaped: {label}")


def mutate_yes(rows, candidate):
    changed = copy.deepcopy(rows)
    for row in changed:
        if row["candidate"] == candidate:
            row["counts_as_history_equation"] = "yes"
            return changed
    raise KeyError(candidate)


def run() -> dict[str, object]:
    rows = read_contract()
    catches = []
    catches.append(must_fail(
        "pullback_promoted_to_dynamics",
        lambda: validate_contract(mutate_yes(rows, "metric_pullback_h_equals_JTgJ")),
    ))
    catches.append(must_fail(
        "bianchi_promoted_to_dynamics",
        lambda: validate_contract(mutate_yes(rows, "Bianchi_and_Ricci_commutator")),
    ))
    catches.append(must_fail(
        "observational_fit_promoted_to_dynamics",
        lambda: validate_contract(mutate_yes(rows, "observational_loss_or_fit")),
    ))
    catches.append(must_fail(
        "einstein_or_action_import_promoted_to_dynamics",
        lambda: validate_contract(mutate_yes(rows, "Einstein_or_chosen_action_equation")),
    ))
    catches.append(must_fail(
        "solver_launched_without_owned_residual",
        lambda: validate_contract(rows, stage2_started=True),
    ))
    witness = counterfamily_record()
    mutated_witness = dict(witness)
    mutated_witness["b7_curvature"] = mutated_witness["b0_curvature"]
    catches.append(must_fail(
        "arbitrary_history_invariant_separator_deleted",
        lambda: validate_witness(mutated_witness),
    ))
    assert all(item["caught"] for item in catches)
    return {
        "status": "PASS",
        "catch_count": len(catches),
        "catches": catches,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    result = run()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if arguments.output:
        arguments.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

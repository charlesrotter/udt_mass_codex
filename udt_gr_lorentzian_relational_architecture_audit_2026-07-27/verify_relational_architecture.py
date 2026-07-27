#!/usr/bin/env python3
"""Fail-closed structural and anti-import verifier for the GR/UDT architecture audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DEPENDENCIES = [
    "METRIC_LOCAL",
    "METRIC_PLUS_ORIENTATION",
    "OBSERVER_EVENT",
    "OBSERVER_PAIR",
    "PATH_OR_CONGRUENCE",
    "CONNECTION_TRANSPORT",
    "GAUGE_EQUIVALENCE",
    "GLOBAL_HYPOTHESIS",
    "DYNAMICS_AND_DATA",
    "OPERATIONAL_POSTULATE",
]


def read_tsv(name: str) -> list[dict[str, str]]:
    with (ROOT / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def keyed(rows: list[dict[str, str]], key: str, expected: int) -> dict[str, dict[str, str]]:
    values = [row[key] for row in rows]
    if len(rows) != expected or len(set(values)) != expected:
        raise AssertionError(f"{key}: expected {expected} unique rows, got {len(rows)}/{len(set(values))}")
    return {row[key]: row for row in rows}


def source_set(cell: str) -> set[str]:
    return {part for part in cell.split(";") if part}


def verify_tables(tables: dict[str, list[dict[str, str]]]) -> dict[str, object]:
    frozen = keyed(tables["source_universe"], "source_id", 18)
    sources = keyed(tables["source_verification"], "source_id", 18)
    arch = keyed(tables["architecture"], "architecture_id", 15)
    hypotheses = keyed(tables["hypotheses"], "hypothesis_id", 10)
    crosswalk = keyed(tables["crosswalk"], "target_id", 10)
    targets = keyed(tables["targets"], "target_id", 10)
    facts = keyed(tables["facts"], "fact_id", 12)

    expected_sources = {f"S{i:02d}" for i in range(1, 19)}
    if set(frozen) != expected_sources or set(sources) != expected_sources:
        raise AssertionError("source universe mismatch")
    if any(not row["primary_locator"].startswith("https://") for row in sources.values()):
        raise AssertionError("non-HTTPS primary locator")
    if sources["S11"]["access_grade"] != "PRIMARY_METADATA_ONLY":
        raise AssertionError("S11 access limitation was promoted")
    correction = (ROOT / "PREREGISTRATION_CORRECTION.md").read_text(encoding="utf-8")
    if "10.1112/plms/s2-32.1.241" not in correction or "incorrect" not in correction:
        raise AssertionError("S02 append-only correction absent")

    for row in arch.values():
        if any(row[name] not in {"0", "1"} for name in DEPENDENCIES):
            raise AssertionError(f"invalid dependency bit: {row['architecture_id']}")
        if not source_set(row["source_ids"]) <= expected_sources:
            raise AssertionError(f"unknown architecture source: {row['architecture_id']}")

    exact_bits = {
        "A02": {"METRIC_LOCAL": "1", "OBSERVER_EVENT": "1", "GAUGE_EQUIVALENCE": "1"},
        "A04": {"PATH_OR_CONGRUENCE": "1", "CONNECTION_TRANSPORT": "1", "GAUGE_EQUIVALENCE": "1"},
        "A05": {"PATH_OR_CONGRUENCE": "1", "CONNECTION_TRANSPORT": "1", "GLOBAL_HYPOTHESIS": "1"},
        "A06": {"OBSERVER_PAIR": "1", "PATH_OR_CONGRUENCE": "1", "GLOBAL_HYPOTHESIS": "1"},
        "A07": {"OBSERVER_EVENT": "1", "OBSERVER_PAIR": "1", "PATH_OR_CONGRUENCE": "1"},
        "A09": {"OPERATIONAL_POSTULATE": "1", "GAUGE_EQUIVALENCE": "1"},
        "A11": {"GLOBAL_HYPOTHESIS": "1", "DYNAMICS_AND_DATA": "1"},
        "A12": {"OBSERVER_EVENT": "1", "PATH_OR_CONGRUENCE": "1", "GLOBAL_HYPOTHESIS": "1"},
        "A14": {"OBSERVER_EVENT": "1", "OBSERVER_PAIR": "1", "GAUGE_EQUIVALENCE": "1"},
    }
    for aid, requirements in exact_bits.items():
        for field, expected in requirements.items():
            if arch[aid][field] != expected:
                raise AssertionError(f"{aid} lost required {field}")

    expected_outcomes = {
        "H01": "SUPPORTED_SCOPED",
        "H02": "SUPPORTED_SCOPED",
        "H03": "SUPPORTED_SCOPED",
        "H04": "SUPPORTED_EXACT_LOCAL_SCOPE",
        "H05": "SUPPORTED_SCOPED",
        "H06": "SUPPORTED_EXACT_LOCAL_SCOPE",
        "H07": "SUPPORTED_EXACT",
        "H08": "SUPPORTED_MATHEMATICAL_ARCHITECTURE",
        "H09": "SUPPORTED_SCOPED_INFERENCE",
        "H10": "LEAD_ONLY_CONSISTENT",
    }
    if {key: row["outcome"] for key, row in hypotheses.items()} != expected_outcomes:
        raise AssertionError("hypothesis outcomes changed")

    for fact in facts.values():
        if not source_set(fact["source_ids"]) <= expected_sources:
            raise AssertionError(f"unknown independent fact source: {fact['fact_id']}")
        refs = source_set(fact["required_architecture_or_hypothesis"])
        if not refs <= (set(arch) | set(hypotheses)):
            raise AssertionError(f"unresolved independent fact target: {fact['fact_id']}")

    if set(crosswalk) != set(targets):
        raise AssertionError("crosswalk target coverage mismatch")
    for uid, row in crosswalk.items():
        if row["current_UDT_status"] != targets[uid]["controlling_status"]:
            raise AssertionError(f"UDT status drift: {uid}")
    if crosswalk["U02"]["result"] != "REQUIRES_DERIVED_EQUIVALENCE_TEST":
        raise AssertionError("seven extension directions were silently gauged away")
    if "All seven directions are Lorentz gauge" not in crosswalk["U02"]["forbidden_inference"]:
        raise AssertionError("seven-direction anti-import disclosure absent")
    if crosswalk["U07"]["result"] != "TOP_RANKED_DERIVE_OR_FAIL_TARGET":
        raise AssertionError("ranked derive-or-fail target changed")
    if crosswalk["U10"]["result"] != "NO_STATUS_CHANGE":
        raise AssertionError("open downstream UDT statuses promoted")
    if "Einstein equations" not in crosswalk["U10"]["forbidden_inference"]:
        raise AssertionError("GR dynamics anti-import disclosure absent")

    return {
        "source_rows": len(sources),
        "architecture_rows": len(arch),
        "hypothesis_rows": len(hypotheses),
        "crosswalk_rows": len(crosswalk),
        "independent_fact_rows": len(facts),
        "dependency_cells": len(arch) * len(DEPENDENCIES),
    }


def load_tables() -> dict[str, list[dict[str, str]]]:
    return {
        "source_universe": read_tsv("SOURCE_UNIVERSE.tsv"),
        "source_verification": read_tsv("SOURCE_VERIFICATION.tsv"),
        "architecture": read_tsv("RELATIONAL_ARCHITECTURE_MATRIX.tsv"),
        "hypotheses": read_tsv("HYPOTHESIS_OUTCOMES.tsv"),
        "crosswalk": read_tsv("UDT_CROSSWALK.tsv"),
        "targets": read_tsv("UDT_TARGET_UNIVERSE.tsv"),
        "facts": read_tsv("INDEPENDENT_SOURCE_FACTS.tsv"),
    }


def run_catch_proofs(base: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    mutations = []

    def add(name: str, mutate) -> None:
        trial = copy.deepcopy(base)
        mutate(trial)
        rejected = False
        try:
            verify_tables(trial)
        except AssertionError:
            rejected = True
        if not rejected:
            raise AssertionError(f"catch proof escaped: {name}")
        mutations.append({"catch": name, "result": "REJECTED_AS_REQUIRED"})

    add("missing_source", lambda t: t["source_verification"].pop())
    add("duplicate_source", lambda t: t["source_verification"].append(copy.deepcopy(t["source_verification"][0])))
    add("bad_primary_locator", lambda t: t["source_verification"][0].update(primary_locator="secondary.example"))
    add("promote_metadata_only_source", lambda t: next(r for r in t["source_verification"] if r["source_id"] == "S11").update(access_grade="PRIMARY_FULL_TEXT"))
    add("drop_path_from_transport", lambda t: next(r for r in t["architecture"] if r["architecture_id"] == "A04").update(PATH_OR_CONGRUENCE="0"))
    add("drop_global_gate_from_world_function", lambda t: next(r for r in t["architecture"] if r["architecture_id"] == "A06").update(GLOBAL_HYPOTHESIS="0"))
    add("drop_observer_from_frequency_transfer", lambda t: next(r for r in t["architecture"] if r["architecture_id"] == "A07").update(OBSERVER_EVENT="0"))
    add("automatic_observer_space_quotient", lambda t: next(r for r in t["architecture"] if r["architecture_id"] == "A12").update(GLOBAL_HYPOTHESIS="0"))
    add("promote_H10_to_derived", lambda t: next(r for r in t["hypotheses"] if r["hypothesis_id"] == "H10").update(outcome="DERIVED"))
    add("gauge_away_seven_UDT_directions", lambda t: next(r for r in t["crosswalk"] if r["target_id"] == "U02").update(result="ALL_GAUGE"))
    add("remove_seven_direction_disclosure", lambda t: next(r for r in t["crosswalk"] if r["target_id"] == "U02").update(forbidden_inference=""))
    add("import_Einstein_equations", lambda t: next(r for r in t["crosswalk"] if r["target_id"] == "U10").update(result="GR_DYNAMICS_ADOPTED"))
    add("remove_GR_dynamics_disclosure", lambda t: next(r for r in t["crosswalk"] if r["target_id"] == "U10").update(forbidden_inference=""))
    add("promote_open_UDT_status", lambda t: next(r for r in t["crosswalk"] if r["target_id"] == "U03").update(current_UDT_status="DERIVED_PHYSICAL_FUNCTOR"))
    add("lose_independent_fact", lambda t: t["facts"].pop())
    return mutations


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def main() -> None:
    tables = load_tables()
    counts = verify_tables(tables)
    catches = run_catch_proofs(tables)
    hashed = [
        "SOURCE_VERIFICATION.tsv",
        "RELATIONAL_ARCHITECTURE_MATRIX.tsv",
        "HYPOTHESIS_OUTCOMES.tsv",
        "UDT_CROSSWALK.tsv",
        "INDEPENDENT_SOURCE_FACTS.tsv",
    ]
    result = {
        "verdict": "PASS",
        "grade_ceiling": "VERIFIED_WITH_CAVEATS_NO_FRESH_MODEL_CONTEXT",
        "counts": counts,
        "catch_proofs": catches,
        "hashes": {name: sha256(ROOT / name) for name in hashed},
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

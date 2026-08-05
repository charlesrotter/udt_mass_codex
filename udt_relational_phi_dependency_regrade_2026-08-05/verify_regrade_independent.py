#!/usr/bin/env python3
"""Independent standard-library reproduction of the regrade identity and family decisions."""

from __future__ import annotations

import csv
from collections import Counter
import hashlib
from pathlib import Path
import re


HERE = Path(__file__).resolve().parent


def load(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle, delimiter="\t")]


def applies(rule: dict[str, str], source: dict[str, str]) -> bool:
    path, kind, value = source["path"], rule["match_kind"], rule["match_value"]
    focus = sum(int(v) for k, v in source.items() if k.startswith("hits_") and k != "hits_broad_phi_depth")
    if kind == "EXACT_SET":
        return path in set(value.split(";"))
    if kind == "PREFIX_SET":
        return any(path.startswith(prefix) for prefix in value.split(";"))
    if kind == "REGEX":
        return bool(re.search(value, path))
    if kind == "ROW_FLAG":
        key, expected = value.split("=", 1)
        return (str(focus) if key == "focused_hits" else source[key]) == expected
    if kind == "ROW_DATE":
        return source["first_date"][:10] < value.split("<", 1)[1]
    if kind == "FALLBACK":
        return True
    raise AssertionError(kind)


def main() -> None:
    active, ledger, rules = load("ACTIVE_REGRADE_UNIVERSE.tsv"), load("ACTIVE_REGRADING_LEDGER.tsv"), load("SEMANTIC_FAMILY_RULES.tsv")
    assert len(active) == len(ledger) == 4762
    assert [row["path"] for row in active] == [row["path"] for row in ledger]
    assert len({row["path"] for row in ledger}) == 4762
    identity = hashlib.sha256(("\n".join(row["path"] for row in active) + "\n").encode()).hexdigest()
    assert identity == "e5e43aa069a1cfbda0db72346cb89023b530317c68049554bb11f5fe0e367518"

    rule_by_id = {rule["family_id"]: rule for rule in rules}
    assert len(rule_by_id) == len(rules)
    reproduced = []
    for source, recorded in zip(active, ledger):
        candidates = [rule for rule in rules if applies(rule, source)]
        maximum = max(int(rule["priority"]) for rule in candidates)
        winners = [rule for rule in candidates if int(rule["priority"]) == maximum]
        assert len(winners) == 1
        winner = winners[0]
        assert recorded["family_id"] == winner["family_id"]
        assert recorded["disposition"] == winner["disposition"]
        reproduced.append(f"{recorded['path']}\t{winner['family_id']}\t{winner['disposition']}\n")
    family_identity = hashlib.sha256("".join(reproduced).encode()).hexdigest()
    assert family_identity == "69408f2a5e9a65de2beb8a016c502de76b798afce18c116b9ef437f54c39279d"
    counts = Counter(row["disposition"] for row in ledger)
    assert counts["CONCLUSION_REGRADE_REQUIRED"] == 99
    assert counts["CONDITIONAL_REINTERPRETATION_ONLY"] == 1091
    assert counts["CONTROL_UPDATE_REQUIRED"] == 13
    assert counts["FROZEN_EVIDENCE_IMMUTABLE"] == 40
    assert counts["HISTORICAL_SUPERSEDED_NO_ACTION"] == 335
    assert counts.get("REDERIVATION_REQUIRED", 0) == 0
    assert not any(row["family_id"] == "F20_POSTJULY_UNMATCHED" for row in ledger)
    current_chain = {
        "UDT_NATIVE_ACTION_COLD_PACKET.md",
        "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md",
        "verify_udt_reciprocal_c_postulate.py",
    }
    assert {
        row["path"] for row in ledger if row["family_id"] == "F02A_CURRENT_FOUNDING_CHAIN"
    } == current_chain

    pointwise = [row for row in ledger if row["family_id"] == "F03_OWNER_LOCAL_PHI_OVERREACH"]
    assert len(pointwise) == 99
    assert len({row["path"].split("/", 1)[0] for row in pointwise}) == 7
    negatives = load("NEGATIVE_REGRADING.tsv")
    assert len(negatives) == 3
    assert all("NONBLOCKING" in row["current_authority"] for row in negatives)
    print(
        "PASS independent: active=4762, conclusion_regrade=99, conditional=1091, "
        "frozen=40, historical=335, rederive=0, seven packages, three negatives, "
        f"identity={identity}, family={family_identity}"
    )


if __name__ == "__main__":
    main()

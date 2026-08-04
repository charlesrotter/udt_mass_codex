#!/usr/bin/env python3
"""Fail-closed artifact verifier with exercised underlying-artifact mutations."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import subprocess
import argparse
from copy import deepcopy
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def table_path(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def table(name: str) -> list[dict[str, str]]:
    return table_path(HERE / name)


def keyed(name: str, key: str) -> dict[str, dict[str, str]]:
    rows = table(name)
    assert len(rows) == len({row[key] for row in rows})
    return {row[key]: row for row in rows}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--write", action="store_true", help="refresh recorded verifier outputs")
args = parser.parse_args()

raw = subprocess.check_output(["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"], cwd=ROOT)
unrelated = []
for item in raw.split(b"\0"):
    if not item.startswith(b"?? "):
        continue
    relative = os.fsdecode(item[3:])
    if relative.startswith(HERE.name + "/"):
        continue
    stat = (ROOT / relative).stat()
    unrelated.append({"path": relative, "bytes": str(stat.st_size), "mtime_ns": str(stat.st_mtime_ns)})
unrelated.sort(key=lambda row: row["path"])
baseline = table_path(ROOT / "udt_basic_vs_universal_query_residual_audit_2026-08-04/UNRELATED_UNTRACKED_METADATA.tsv")
recorded_unrelated = table("UNRELATED_UNTRACKED_METADATA.tsv")

state = {
    "sources": table("SOURCE_MANIFEST.tsv"),
    "candidates": keyed("CANDIDATE_OUTCOMES.tsv", "candidate_id"),
    "implications": keyed("CONDITIONAL_IMPLICATION_LEDGER.tsv", "implication_id"),
    "source_rulings": keyed("SOURCE_PROVENANCE_RULINGS.tsv", "source_id"),
    "source_adjudications": table("SOURCE_ADJUDICATION.tsv"),
    "loops": keyed("LOOP_OBJECT_SEPARATION.tsv", "object_id"),
    "premises": keyed("PREMISE_LEDGER.tsv", "premise_id"),
    "production": json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8")),
    "independent": json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8")),
    "completeness": (HERE / "COMPLETENESS_MAP.md").read_text(encoding="utf-8"),
    "next_step": (HERE / "NEXT_STEP.md").read_text(encoding="utf-8"),
    "unrelated": unrelated,
    "unrelated_baseline": baseline,
    "unrelated_recorded": recorded_unrelated,
}


def validate(item: dict) -> None:
    sources = item["sources"]
    assert len(sources) == 32 and len({row["path"] for row in sources}) == 32
    for row in sources:
        path = ROOT / row["path"]
        assert path.is_file()
        assert digest(path) == row["sha256"]
        assert str(path.stat().st_size) == row["bytes"]

    candidates = item["candidates"]
    assert sorted(candidates) == [f"C{index:02d}" for index in range(1, 13)]
    assert len(candidates) == 12
    assert candidates["C01"]["home"] == "CHARACTER_OPERATOR"
    assert candidates["C01"]["metric_residual"] == "NO"
    assert candidates["C02"]["metric_residual"] == "NO_WITHOUT_DEPTH_MAP"
    assert candidates["C03"]["outcome"] == "IDENTITY_FOR_EVERY_ENDPOINT_POTENTIAL"
    assert candidates["C03"]["foundation_status"] == "NONSELECTING"
    assert candidates["C04"]["outcome"] == "ADDITIVE_COCYCLE_IS_SUPPLIED_DATA_CLASS"
    assert candidates["C05"]["outcome"] == "PATH_ADDITIVITY_BY_INTEGRAL_CONCATENATION"
    assert candidates["C06"]["foundation_status"] == "CONDITIONAL_EXTRA_PREMISE"
    assert candidates["C07"]["foundation_status"] == "CONDITIONAL_EXTRA_PREMISE"
    assert candidates["C08"]["outcome"] == "FUNCTORIAL_TRANSPORT_IDENTITY"
    assert candidates["C09"]["outcome"] == "SEMIDIRECT_COMPOSITION_IDENTITY_GIVEN_INPUTS"
    assert candidates["C10"]["foundation_status"] == "NOT_FOUNDED_EXTRA"
    assert candidates["C11"]["outcome"] == "NATURALITY_GATE_ON_FUTURE_LAW"
    assert candidates["C12"]["foundation_status"] == "ADMISSIBLE_NOT_SELECTED"

    implications = item["implications"]
    assert sorted(implications) == [f"I{index:02d}" for index in range(1, 13)]
    assert implications["I04"]["status"] == "NOT_DERIVED"
    assert implications["I05"]["status"] == "NOT_DERIVED_GLOBAL"
    assert implications["I09"]["status"] == "NOT_DERIVED"

    loops = item["loops"]
    assert sorted(loops) == [f"L{index:02d}" for index in range(1, 6)]
    assert loops["L01"]["object"] == "reciprocal_period"
    assert loops["L02"]["object"] == "Levi_Civita_holonomy"
    assert loops["L01"]["owner"] == "SUPPLIED_DEPTH_COCYCLE"
    assert loops["L02"]["owner"] == "SUPPLIED_METRIC_AND_LOOP"
    assert loops["L03"]["identity_condition"] == "EXTRA_NOT_FOUNDED"

    source_rulings = item["source_rulings"]
    assert len(source_rulings) == 11
    assert source_rulings["S11"]["ruling"] == "NO_UPSTREAM_SELECTION"
    assert source_rulings["S07"]["ruling"] == "LAW_GATE_NOT_GENERATOR"

    premises = item["premises"]
    assert len(premises) == 16
    assert premises["P13"]["use"] == "none"
    assert premises["P14"]["use"] == "future compatibility only"
    assert premises["P15"]["use"] == "none"
    assert premises["P16"]["use"] == "outputs not inputs"

    production = item["production"]
    independent = item["independent"]
    assert production["status"] == independent["inferred_outcome"] == "COMPOSITION_IDENTITY_NONSELECTING"
    assert production["production_exact_checks"] == 53
    assert independent["independent_exact_checks"] == 35
    assert production["local_nonclosed_form_period"] == "1"
    assert "nonzero_character_witness" in production["check_names"]
    assert independent["dependencies"] == "stdlib_only"
    assert production["termination_ruling"] == independent["termination_ruling"]
    assert production["termination_ruling"].startswith("CURRENT_COMPOSITION_TO_NATIVE_RESIDUAL_ROUTE_TERMINATES")

    adjudications = item["source_adjudications"]
    assert len(adjudications) == 32
    assert [row["path"] for row in adjudications] == [row["path"] for row in sources]

    assert "one bounded algebraic/global provenance tile" in item["completeness"]
    assert "full solution space is complete" not in item["completeness"]
    assert "The reciprocal-composition route stops here" in item["next_step"]
    assert "Do not launch another composition" in item["next_step"]

    assert item["unrelated"] == item["unrelated_baseline"]
    assert item["unrelated"] == item["unrelated_recorded"]
    assert len(item["unrelated"]) == 83


validate(state)


def remove_source(item: dict) -> None:
    item["sources"].pop()


def remove_candidate(item: dict) -> None:
    del item["candidates"]["C12"]


def set_candidate(candidate: str, field: str, value: str):
    def mutate(item: dict) -> None:
        item["candidates"][candidate][field] = value
    return mutate


def set_implication(implication: str, field: str, value: str):
    def mutate(item: dict) -> None:
        item["implications"][implication][field] = value
    return mutate


def set_loop(loop: str, field: str, value: str):
    def mutate(item: dict) -> None:
        item["loops"][loop][field] = value
    return mutate


def set_source_ruling(source: str, value: str):
    def mutate(item: dict) -> None:
        item["source_rulings"][source]["ruling"] = value
    return mutate


def set_premise_use(premise: str, value: str):
    def mutate(item: dict) -> None:
        item["premises"][premise]["use"] = value
    return mutate


def mutate_period(item: dict) -> None:
    item["production"]["local_nonclosed_form_period"] = "0"


def remove_nonzero_witness(item: dict) -> None:
    item["production"]["check_names"].remove("nonzero_character_witness")


def share_engine(item: dict) -> None:
    item["independent"]["dependencies"] = "sympy_shared"


def reopen_route(item: dict) -> None:
    item["next_step"] = item["next_step"].replace("The reciprocal-composition route stops here", "The reciprocal-composition route continues")


def corrupt_source_hash(item: dict) -> None:
    item["sources"][0]["sha256"] = "0" * 64


def alter_untracked_metadata(item: dict) -> None:
    item["unrelated"][0]["bytes"] = str(int(item["unrelated"][0]["bytes"]) + 1)


def inflate_scope(item: dict) -> None:
    item["completeness"] += "\nfull solution space is complete\n"


mutations = {
    "F01": remove_source,
    "F02": remove_candidate,
    "F03": set_candidate("C01", "home", "METRIC_CONFIGURATION_SPACE"),
    "F04": set_candidate("C02", "metric_residual", "YES"),
    "F05": set_candidate("C03", "foundation_status", "SELECTED_PHI_PROFILE"),
    "F06": set_implication("I04", "status", "DERIVED_FROM_ADDITIVITY"),
    "F07": set_implication("I05", "status", "DERIVED_GLOBAL"),
    "F08": mutate_period,
    "F09": set_loop("L02", "owner", "SUPPLIED_DEPTH_COCYCLE"),
    "F10": set_loop("L02", "object", "reciprocal_period"),
    "F11": set_candidate("C04", "outcome", "ENDPOINT_INDEPENDENT"),
    "F12": set_candidate("C10", "foundation_status", "FOUNDED"),
    "F13": set_candidate("C11", "outcome", "UNIQUE_LAW_GENERATOR"),
    "F14": set_candidate("C12", "foundation_status", "SELECTED_DYNAMICS"),
    "F15": set_source_ruling("S11", "UPSTREAM_RESIDUAL_SELECTED"),
    "F16": set_premise_use("P13", "selects_residual"),
    "F17": inflate_scope,
    "F18": remove_nonzero_witness,
    "F19": share_engine,
    "F20": reopen_route,
    "F21": corrupt_source_hash,
    "F22": alter_untracked_metadata,
}

contract = keyed("FALSIFICATION_CONTRACT.tsv", "failure_id")
assert set(mutations) == set(contract)
catch_rows = []
for failure_id, operation in mutations.items():
    altered = deepcopy(state)
    operation(altered)
    caught = False
    try:
        validate(altered)
    except AssertionError:
        caught = True
    assert caught, failure_id
    catch_rows.append(
        {
            "failure_id": failure_id,
            "mutation": contract[failure_id]["forbidden_false_pass"],
            "mutation_target": {
                "F01": "SOURCE_MANIFEST.tsv row set",
                "F02": "CANDIDATE_OUTCOMES.tsv identity map",
                "F03": "CANDIDATE_OUTCOMES.tsv C01.home",
                "F04": "CANDIDATE_OUTCOMES.tsv C02.metric_residual",
                "F05": "CANDIDATE_OUTCOMES.tsv C03.foundation_status",
                "F06": "CONDITIONAL_IMPLICATION_LEDGER.tsv I04.status",
                "F07": "CONDITIONAL_IMPLICATION_LEDGER.tsv I05.status",
                "F08": "DERIVATION_RESULT.json nonclosed period",
                "F09": "LOOP_OBJECT_SEPARATION.tsv L02.owner",
                "F10": "LOOP_OBJECT_SEPARATION.tsv L02.object",
                "F11": "CANDIDATE_OUTCOMES.tsv C04.outcome",
                "F12": "CANDIDATE_OUTCOMES.tsv C10.foundation_status",
                "F13": "CANDIDATE_OUTCOMES.tsv C11.outcome",
                "F14": "CANDIDATE_OUTCOMES.tsv C12.foundation_status",
                "F15": "SOURCE_PROVENANCE_RULINGS.tsv S11.ruling",
                "F16": "PREMISE_LEDGER.tsv P13.use",
                "F17": "COMPLETENESS_MAP.md scope statement",
                "F18": "DERIVATION_RESULT.json check-name set",
                "F19": "INDEPENDENT_RESULT.json dependency declaration",
                "F20": "NEXT_STEP.md termination statement",
                "F21": "SOURCE_MANIFEST.tsv source digest",
                "F22": "live unrelated-checkout metadata state",
            }[failure_id],
            "result": "CAUGHT",
        }
    )

result = {
    "status": "PASS",
    "outcome": state["production"]["status"],
    "production_exact_checks": state["production"]["production_exact_checks"],
    "independent_exact_checks": state["independent"]["independent_exact_checks"],
    "artifact_level_catch_proofs": len(catch_rows),
    "sources": len(state["sources"]),
    "source_adjudications": len(state["source_adjudications"]),
    "candidates": len(state["candidates"]),
    "implications": len(state["implications"]),
    "loop_objects": len(state["loops"]),
    "unrelated_untracked_metadata_rows": len(state["unrelated"]),
    "source_manifest_sha256": digest(HERE / "SOURCE_MANIFEST.sha256"),
}
stdout = (
    f"PASS production={result['production_exact_checks']} independent={result['independent_exact_checks']} "
    f"artifact_catches={result['artifact_level_catch_proofs']} sources={result['sources']} "
    f"candidates={result['candidates']}\n"
    f"outcome={result['outcome']}\n"
)
if args.write:
    with (HERE / "UNRELATED_UNTRACKED_METADATA.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("path", "bytes", "mtime_ns"), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(unrelated)
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("failure_id", "mutation", "mutation_target", "result"), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(catch_rows)
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (HERE / "VERIFIER_STDOUT.txt").write_text(stdout, encoding="utf-8")
    (HERE / "VERIFIER_STDERR.txt").write_text("", encoding="utf-8")
print(stdout, end="")

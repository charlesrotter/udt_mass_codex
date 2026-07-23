#!/usr/bin/env python3
"""Fail-closed package verifier for the phi causal-interface atlas."""

from __future__ import annotations

import copy
import csv
import gzip
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "03e0e9407c756ad4cae2fbf4a4814c820aeaf5fc"


def rows(path):
    opener = gzip.open if Path(path).suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def digest(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def validate_state(state):
    require(state["identity_count"] == 3_072, "identity count")
    require(state["identity_unique"] == 3_072, "identity uniqueness")
    require(state["identity_census"] == {
        "IDENTICALLY_ZERO_DPHI_INTERVAL": 1_536,
        "UNIFORMLY_SPACELIKE": 1_152,
        "UNIFORMLY_TIMELIKE": 384,
    }, "identity census")
    require(state["interval_rows"] == 1_536, "interval certificate count")
    require(state["full_interval_boxes"] == 1_536, "full interval coverage")
    require(state["interface_rows"] == 0, "interface count")
    require(state["metric_degeneracies"] == 0, "metric degeneracy")
    require(state["path_count"] == 95_232, "path count")
    require(state["path_unique"] == 95_232, "path uniqueness")
    require(state["bank_partition"] == {
        "B0": "UNIFORMLY_SPACELIKE",
        "B1": "UNIFORMLY_SPACELIKE",
        "B2": "UNIFORMLY_SPACELIKE",
        "B3": "UNIFORMLY_TIMELIKE",
    }, "bank partition")
    require(state["bank_physical_labels"] == 0, "physical bank label")
    require(state["exact_spacelike_joins"] == 2_160, "spacelike join")
    require(state["exact_timelike_joins"] == 720, "timelike join")
    require(state["independent_spacelike_joins"] == 2_160, "independent spacelike join")
    require(state["independent_timelike_joins"] == 720, "independent timelike join")
    require(state["continuous_complete_motif_claim"] is False, "continuous motif overclaim")
    require(state["frozen_generator_probes"] == 13_824, "frozen generator probe coverage")
    require(state["completion_rows"] == 36, "completion cross")
    require(state["selected_completions"] == 0, "completion selection")
    require(state["actions_loaded"] == 0, "action import")
    require(state["matter_carriers_loaded"] == 0, "matter carrier import")
    require(state["atlas_deformation_vectors_loaded"] == 48, "atlas deformation vectors")
    require(state["carrier_key_meaning"] == "MATTER_CARRIERS_SELECTED", "carrier-key meaning")
    require(state["physical_labels"] == 0, "physical regime label")
    require(state["source_integrity"] is True, "source integrity")
    require(state["independent_pass"] is True, "independent verification")
    require(state["independent_catches"] == 8, "independent catches")
    require(state["report_guards"] is True, "report scope guards")


def mutation_catches(state):
    mutations = [
        ("P01_MISSING_IDENTITY", lambda value: value.__setitem__("identity_count", 3_071)),
        ("P02_DUPLICATE_IDENTITY", lambda value: value.__setitem__("identity_unique", 3_071)),
        ("P03_FLIP_CAUSAL_CLASS", lambda value: value["identity_census"].update({
            "UNIFORMLY_SPACELIKE": 1_151, "UNIFORMLY_TIMELIKE": 385
        })),
        ("P04_DROP_INTERVAL_CERTIFICATE", lambda value: value.__setitem__("interval_rows", 1_535)),
        ("P05_PARTIAL_INTERVAL", lambda value: value.__setitem__("full_interval_boxes", 1_535)),
        ("P06_INVENT_INTERFACE", lambda value: value.__setitem__("interface_rows", 1)),
        ("P07_INVENT_DEGENERACY", lambda value: value.__setitem__("metric_degeneracies", 1)),
        ("P08_STALE_PATH_JOIN", lambda value: value.__setitem__("path_unique", 95_231)),
        ("P09_PHYSICALIZE_BANK", lambda value: value.__setitem__("bank_physical_labels", 1)),
        ("P10_DROP_SPACELIKE_JOIN", lambda value: value.__setitem__("exact_spacelike_joins", 2_159)),
        ("P11_DROP_TIMELIKE_JOIN", lambda value: value.__setitem__("exact_timelike_joins", 719)),
        ("P12_SELECT_COMPLETION", lambda value: value.__setitem__("selected_completions", 1)),
        ("P13_IMPORT_ACTION", lambda value: value.__setitem__("actions_loaded", 1)),
        ("P14_ASSIGN_PHYSICAL_REGIME", lambda value: value.__setitem__("physical_labels", 1)),
        ("P15_MUTATE_SOURCE", lambda value: value.__setitem__("source_integrity", False)),
        ("P16_DISABLE_INDEPENDENT_ROUTE", lambda value: value.__setitem__("independent_pass", False)),
        ("P17_FALSE_CONTINUOUS_MOTIF", lambda value: value.__setitem__("continuous_complete_motif_claim", True)),
        ("P18_STALE_INDEPENDENT_JOIN", lambda value: value.__setitem__("independent_spacelike_joins", 2_159)),
        ("P19_DROP_FROZEN_GENERATOR_PROBE", lambda value: value.__setitem__("frozen_generator_probes", 13_823)),
        ("P20_HIDE_DEFORMATION_VECTORS", lambda value: value.__setitem__("atlas_deformation_vectors_loaded", 0)),
    ]
    output = []
    for catch_id, mutate in mutations:
        corrupted = copy.deepcopy(state)
        mutate(corrupted)
        try:
            validate_state(corrupted)
        except AssertionError as exc:
            output.append({
                "catch_id": catch_id,
                "validator": "validate_state",
                "rejection": str(exc),
                "result": "MUTATION_REJECTED_AS_REQUIRED",
            })
        else:
            raise AssertionError(f"mutation escaped {catch_id}")
    return output


def main():
    source = rows(HERE / "SOURCE_LEDGER.tsv")
    require(len(source) == 11, "source ledger count")
    source_integrity = True
    for row in source:
        path = ROOT / row["path"]
        require(path.exists(), f"source exists {row['path']}")
        observed_blob = subprocess.check_output(
            ["git", "rev-parse", f"{BASE}:{row['path']}"], cwd=ROOT, text=True
        ).strip()
        if digest(path) != row["sha256"] or observed_blob != row["base_blob"]:
            source_integrity = False

    identities = rows(HERE / "IDENTITY_CAUSAL_CERTIFICATES.tsv")
    intervals = rows(HERE / "INTERVAL_SIGN_CERTIFICATES.tsv.gz")
    interfaces = rows(HERE / "INTERFACE_ATLAS.tsv")
    paths = rows(HERE / "PATH_PRESENTATION_CAUSAL_ATLAS.tsv.gz")
    banks = rows(HERE / "REGISTERED_BANK_CAUSAL_PARTITION.tsv")
    joins = rows(HERE / "MOTIF_CAUSAL_JOIN_CENSUS.tsv")
    completions = rows(HERE / "COMPLETION_CAUSAL_COMPATIBILITY.tsv")
    exact = rows(HERE / "EXACT_IDENTITY_LEDGER.tsv")
    status = rows(HERE / "STATUS_LEDGER.tsv")
    premises = rows(HERE / "PREMISE_STATUS_LEDGER.tsv")
    result = json.loads((HERE / "RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
    report = (HERE / "AUDIT_REPORT.md").read_text()

    require(len(exact) == 5 and all(row["status"] == "DERIVED_EXACT" for row in exact), "exact ledger")
    require(len(status) == 16 and len(premises) == 20, "status/premise ledgers")
    full_box_ids = {
        row["identity_id"]
        for row in intervals
        if row["u_lo"] == "0" and row["u_hi"] == "1" and row["depth"] == "0"
    }
    exact_spacelike = sum(
        int(row["path_presentations"]) for row in joins
        if row["coframe_join_status"] == "EXACT_PHI_SPACELIKE_DEPTH_PROJECTOR_JOIN"
    )
    exact_timelike = sum(
        int(row["path_presentations"]) for row in joins
        if row["coframe_join_status"] == "EXACT_PHI_TIMELIKE_PROJECTOR_JOIN"
    )
    report_phrases = (
        "do **not** meet along any registered coordinate chord",
        "not** yet a particle",
        "chosen conditional registered Lorentzian coframe atlas",
        "were not interval-certified between those nodes",
        "No complete finite-cell witness",
        "Existing SNe results are unchanged",
        "not canonization",
    )
    state = {
        "identity_count": len(identities),
        "identity_unique": len({row["identity_id"] for row in identities}),
        "identity_census": dict(sorted(Counter(row["causal_status"] for row in identities).items())),
        "interval_rows": len(intervals),
        "full_interval_boxes": len(full_box_ids),
        "interface_rows": len(interfaces),
        "metric_degeneracies": result["metric_degeneracies"],
        "path_count": len(paths),
        "path_unique": len({(row["identity_id"], row["family_id"]) for row in paths}),
        "bank_partition": {row["bank"]: row["active_causal_status_set"] for row in banks},
        "bank_physical_labels": sum(
            row["interpretation_guard"] != "REGISTERED_ANALYTIC_BANK_AND_COORDINATE_CHORD__NOT_PHYSICAL_SCALE_OR_REGIME"
            for row in banks
        ),
        "exact_spacelike_joins": exact_spacelike,
        "exact_timelike_joins": exact_timelike,
        "independent_spacelike_joins": independent["phi_projector_join_verification"]["spacelike_path_presentations"],
        "independent_timelike_joins": independent["phi_projector_join_verification"]["timelike_path_presentations"],
        "continuous_complete_motif_claim": independent["phi_projector_join_verification"]["continuous_complete_motif_classification_certified"],
        "frozen_generator_probes": independent["frozen_generator_crosscheck"]["active_identity_probes"],
        "completion_rows": len(completions),
        "selected_completions": sum(row["selection_status"] != "NOT_SELECTED" for row in completions),
        "actions_loaded": result["actions_loaded"],
        "matter_carriers_loaded": result["carriers_loaded"],
        "atlas_deformation_vectors_loaded": result["atlas_deformation_vectors_loaded"],
        "carrier_key_meaning": result["carriers_loaded_meaning"],
        "physical_labels": result["physical_regime_labels_assigned"],
        "source_integrity": source_integrity,
        "independent_pass": independent["status"] == "PASS",
        "independent_catches": len(independent["mutation_catches"]),
        "report_guards": all(phrase in report for phrase in report_phrases),
    }
    validate_state(state)
    catches = mutation_catches(state)
    with (HERE / "PACKAGE_CATCH_PROOFS.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(catches[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(catches)
    package_result = {
        "status": "PASS_WITH_REGISTERED_SCOPE",
        "state": state,
        "package_catches_passed": len(catches),
        "independent_method": independent["method"],
        "independent_catches_passed": len(independent["mutation_catches"]),
        "maximum_conclusion": result["maximum_conclusion"],
    }
    (HERE / "PACKAGE_VERIFICATION.json").write_text(
        json.dumps(package_result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(package_result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

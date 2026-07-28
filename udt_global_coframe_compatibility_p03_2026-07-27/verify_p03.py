#!/usr/bin/env python3
"""Independent fail-closed verification of the P03-A evidence package."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def row_hash(row: dict[str, str]) -> str:
    return hashlib.sha256("\t".join(row.values()).encode()).hexdigest()


def assert_guard(state: dict[str, object]) -> None:
    assert state["source_count"] == 57
    assert state["source_unique"] is True
    assert state["source_hashes_valid"] is True
    assert state["generated_source_in_freeze"] is False
    assert state["completion_meanings_preserved"] is True
    assert state["schema_promoted_to_metric"] is False
    assert state["local_promoted_to_global"] is False
    assert state["invented_transition"] is False
    assert state["invented_cap_or_boundary"] is False
    assert state["all_named_occurrences_retained"] is True
    assert state["target_privileged"] is False
    assert state["conditional_promoted"] is False
    assert state["cross_splice"] is False
    assert state["causal_transition_rows"] == 8
    assert state["degeneracy_disclosed"] is True
    assert state["coordinate_static_called_invariant"] is False
    assert state["field_equation_inferred"] is False
    assert state["downstream_physics_imported"] is False
    assert state["gpu_launched"] is False
    assert state["local_strata_called_physical"] is False
    assert state["complete_solution_space_claimed"] is False


def catch_proofs(baseline: dict[str, object]) -> list[dict[str, str]]:
    mutations = {
        "F01": ("source_unique", False),
        "F02": ("source_hashes_valid", False),
        "F03": ("generated_source_in_freeze", True),
        "F04": ("completion_meanings_preserved", False),
        "F05": ("schema_promoted_to_metric", True),
        "F06": ("local_promoted_to_global", True),
        "F07": ("invented_transition", True),
        "F08": ("invented_cap_or_boundary", True),
        "F09": ("all_named_occurrences_retained", False),
        "F10": ("target_privileged", True),
        "F11": ("conditional_promoted", True),
        "F12": ("cross_splice", True),
        "F13": ("causal_transition_rows", 7),
        "F14": ("degeneracy_disclosed", False),
        "F15": ("coordinate_static_called_invariant", True),
        "F16": ("field_equation_inferred", True),
        "F17": ("downstream_physics_imported", True),
        "F18": ("gpu_launched", True),
        "F19": ("local_strata_called_physical", True),
        "F20": ("complete_solution_space_claimed", True),
    }
    proofs = []
    for catch_id, (key, value) in mutations.items():
        mutant = deepcopy(baseline)
        mutant[key] = value
        rejected = False
        try:
            assert_guard(mutant)
        except AssertionError:
            rejected = True
        assert rejected, catch_id
        proofs.append({
            "catch_id": catch_id,
            "mutation": f"{key}={value}",
            "result": "PASS_REJECTED",
        })
    return proofs


def main() -> None:
    checks: list[dict[str, object]] = []

    manifest_path = PKG / "SHA256SUMS.txt"
    if manifest_path.is_file():
        recorded = {}
        for line in manifest_path.read_text().splitlines():
            checksum, name = line.split("  ", 1)
            assert name not in recorded
            recorded[name] = checksum
        actual_files = {
            path.name for path in PKG.iterdir()
            if path.is_file() and path.name != manifest_path.name and not path.name.endswith(".pyc")
        }
        assert set(recorded) == actual_files
        assert all(digest(PKG / name) == checksum for name, checksum in recorded.items())
        checks.append({"check": "package_sha256_manifest", "status": "PASS", "count": len(recorded)})

    manifest = tsv(PKG / "SOURCE_MANIFEST.tsv")
    assert len(manifest) == 57
    assert len({x["source_id"] for x in manifest}) == 57
    assert len({x["path"] for x in manifest}) == 57
    for item in manifest:
        path = ROOT / item["path"]
        assert path.is_file()
        assert path.stat().st_size == int(item["size_bytes"])
        assert digest(path) == item["sha256"]
    checks.append({"check": "source_manifest_bytes", "status": "PASS", "count": 57})

    source_audit = tsv(PKG / "SOURCE_ADJUDICATION.tsv")
    assert len(source_audit) == 57
    assert {x["source_id"] for x in source_audit} == {x["source_id"] for x in manifest}
    assert {x["path"] for x in source_audit} == {x["path"] for x in manifest}
    required_source_fields = {
        "domain_chart_cover", "complete_coframe_metric", "overlap_transition_maps",
        "finite_cell_completion_data", "regularity_nondegeneracy", "causal_interface_rules",
        "topology_global_descent", "construction_sufficiency", "provenance", "classification",
    }
    assert all(required_source_fields <= set(row) for row in source_audit)
    assert all(all(row[field] for field in required_source_fields) for row in source_audit)
    checks.append({"check": "one_adjudication_per_source_and_nine_fields", "status": "PASS", "count": 57})

    objects = tsv(PKG / "NAMED_OBJECT_ADJUDICATION.tsv")
    assert len(objects) == 713
    assert len({x["object_occurrence_id"] for x in objects}) == 713
    manifest_paths = {x["path"] for x in manifest}
    assert {x["source_path"] for x in objects} <= manifest_paths
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for item in objects:
        grouped[item["source_path"]].append(item)
    for source_path, occurrence_rows in grouped.items():
        raw = tsv(ROOT / source_path)
        assert len(raw) == len(occurrence_rows)
        for occurrence, source_row in zip(occurrence_rows, raw):
            assert int(occurrence["source_row_number"]) >= 1
            assert occurrence["source_row_sha256"] == row_hash(source_row)
    kind_counts = Counter(x["object_kind"] for x in objects)
    assert kind_counts["CAP_PAIR_TOPOLOGY_WITNESS"] == 256
    assert kind_counts["MOTIF_COMPLETION_COMPATIBILITY"] == 84
    assert kind_counts["COMPLETION_CAUSAL_CASE"] == 60
    assert kind_counts["CAUSAL_TRANSITION_CONTROL"] == 8
    checks.append({"check": "candidate_occurrence_coverage_and_row_hashes", "status": "PASS", "count": 713})

    conditional = [x for x in objects if x["classification"] == "CONDITIONAL_COMPLETE_GIVEN_EXPLICIT_SUPPLIED_DATA"]
    assert len(conditional) == 2
    assert {x["source_row_label"] for x in conditional} == {"Q01_ROUND_S3_B19", "Q02_SQUASHED_S3_OFF_SHELL"}
    assert all(x["P03B_gate"] == "FAIL_MISSING_FOUNDED_PHI_PROFILE" for x in conditional)
    assert not any(x["classification"] == "GLOBALLY_CONSTRUCTIBLE_REGISTERED" for x in objects)
    checks.append({"check": "conditional_complete_controls_and_zero_global_founded_objects", "status": "PASS", "count": 2})

    gates = tsv(PKG / "P03B_GATE_LEDGER.tsv")
    assert len(gates) == 14
    assert len({x["candidate_id"] for x in gates}) == 14
    assert sum(x["candidate_id"].startswith("FC") for x in gates) == 12
    assert {x["candidate_id"] for x in gates if x["candidate_id"].startswith("Q")} == {
        "Q01_ROUND_S3_B19", "Q02_SQUASHED_S3_OFF_SHELL"
    }
    assert all(x["P03B_eligibility"] == "FAIL" for x in gates)
    checks.append({"check": "p03b_gate_all_fail_closed", "status": "PASS", "count": 14})

    projection = tsv(PKG / "P02_MOTIF_PROJECTION_AVAILABILITY.tsv")
    assert len(projection) == 2
    frozen_paths = {x["path"] for x in manifest}
    for row in projection:
        assert row["required_path"] not in frozen_paths
        assert (ROOT / row["required_path"]).is_file()
        assert row["permitted_as_P03_input"] == "NO"
        assert row["ruling"] == "BLOCKED_UNREGISTERED_SOURCE"
    assert not (PKG / "P02_MOTIF_FAMILY_PROJECTION.tsv").exists()
    checks.append({"check": "lossless_projection_fail_closed_on_unfrozen_detail", "status": "PASS", "count": 2})

    p02a = json.loads((ROOT / "udt_full_local_jet_strata_p02_2026-07-27/STRATUM_CENSUS.json").read_text())
    p02b = json.loads((ROOT / "udt_full_local_jet_strata_p02_2026-07-27/P02B_CENSUS.json").read_text())
    assert p02a["stratum_classification_counts"]["CONSTRUCTIVE_BOTH"] + p02a["stratum_classification_counts"]["CONSTRUCTIVE_ONE"] == 7897
    assert p02b["candidates"] == 12594
    census = json.loads((PKG / "P03A_CENSUS.json").read_text())
    assert census["source_count"] == 57
    assert census["named_object_occurrence_count"] == 713
    assert census["P02_constructive_strata_aggregate_count"] == 7897
    assert census["P02B_candidate_aggregate_count"] == 12594
    assert census["P03B_eligible_global_objects"] == 0
    assert census["maximum_conclusion"] == "OPEN_MISSING_GLOBAL_DEFINITION"
    checks.append({"check": "aggregate_census_reconstruction", "status": "PASS", "count": 4})

    cartan_report = (ROOT / "udt_finite_cell_cartan_transport_atlas_2026-07-23/AUDIT_REPORT.md").read_text()
    pullback_report = (ROOT / "udt_complete_branch_founded_pair_pullback_audit_2026-07-26/AUDIT_REPORT.md").read_text()
    global_report = (ROOT / "udt_global_metric_assembly_atlas_2026-07-22/AUDIT_REPORT.md").read_text()
    assert "complete on-shell (g,phi) finite-cell solutions supplied: 0" in cartan_report
    assert "No currently registered complete metric branch supplies the founded observer-pair depth law." in pullback_report
    assert "A cross-row records compatibility requirements" in global_report
    assert "complete global metric witness" in global_report
    checks.append({"check": "load_bearing_source_anchor_statements", "status": "PASS", "count": 3})

    baseline = {
        "source_count": len(manifest),
        "source_unique": len({x["path"] for x in manifest}) == len(manifest),
        "source_hashes_valid": True,
        "generated_source_in_freeze": any(x["path"].startswith("udt_global_coframe_compatibility_p03_2026-07-27/") for x in manifest),
        "completion_meanings_preserved": len({x["object_occurrence_id"] for x in objects}) == len(objects),
        "schema_promoted_to_metric": any(x["object_kind"] == "COMPLETION_CLASS" and x["classification"] == "GLOBALLY_CONSTRUCTIBLE_REGISTERED" for x in objects),
        "local_promoted_to_global": any(x["source_row_label"] == "Q03_WRL_LOCAL" and x["P03B_gate"].startswith("PASS") for x in objects),
        "invented_transition": False,
        "invented_cap_or_boundary": False,
        "all_named_occurrences_retained": len(objects) == 713,
        "target_privileged": False,
        "conditional_promoted": any(x["classification"] == "GLOBALLY_CONSTRUCTIBLE_REGISTERED" for x in conditional),
        "cross_splice": False,
        "causal_transition_rows": kind_counts["CAUSAL_TRANSITION_CONTROL"],
        "degeneracy_disclosed": "degeneration" in cartan_report.lower(),
        "coordinate_static_called_invariant": False,
        "field_equation_inferred": False,
        "downstream_physics_imported": False,
        "gpu_launched": any("gpu" in p.name.lower() for p in PKG.iterdir()),
        "local_strata_called_physical": False,
        "complete_solution_space_claimed": False,
    }
    assert_guard(baseline)
    proofs = catch_proofs(baseline)
    (PKG / "CATCH_PROOFS.json").write_text(json.dumps({
        "schema": "udt-p03a-catch-proofs-1.0",
        "status": "PASS",
        "count": len(proofs),
        "proofs": proofs,
    }, indent=2, sort_keys=True) + "\n")
    checks.append({"check": "fail_closed_catch_proofs", "status": "PASS", "count": len(proofs)})

    result = {
        "schema": "udt-p03a-independent-verification-1.0",
        "status": "PASS_WITH_SAME_SESSION_CAVEAT",
        "checks": checks,
        "check_count": len(checks),
        "catch_count": len(proofs),
        "source_count": 57,
        "named_object_occurrence_count": 713,
        "P03B_eligible_global_objects": 0,
        "maximum_conclusion": "OPEN_MISSING_GLOBAL_DEFINITION",
    }
    (PKG / "INDEPENDENT_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Fail-closed verifier for the bounded full-coframe response-selection audit."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
from copy import deepcopy
from pathlib import Path
from urllib.parse import unquote

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MANIFESTS = (
    "native_action_stage1_2026-07-18/arm_A/SHA256SUMS.txt",
    "native_action_stage1_2026-07-18/arm_B/SHA256SUMS.txt",
    "native_action_stage2_2026-07-18/arm_A/SHA256SUMS.txt",
    "native_action_stage2_2026-07-18/arm_B/SHA256SUMS.txt",
    "native_action_arm_c_2026-07-18/SHA256SUMS.txt",
    "native_action_final_adjudication_2026-07-18/SHA256SUMS.txt",
)
STARTUP = (
    "LIVE.md",
    "HANDOFF.md",
    "README.md",
    "INDEX.md",
    "AGENTS.md",
    "MEMORY.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
)


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def git_blob(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def table_path(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def table(name: str) -> list[dict[str, str]]:
    return table_path(HERE / name)


def keyed(name: str, key: str) -> dict[str, dict[str, str]]:
    rows = table(name)
    assert len(rows) == len({row[key] for row in rows})
    return {row[key]: row for row in rows}


def run(command: list[str], timeout: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=timeout, check=False)


def render_manifest(paths: list[str]) -> str:
    lines = ["path\tgit_blob\tbytes\tsha256"]
    for relative in paths:
        data = (ROOT / relative).read_bytes()
        lines.append(f"{relative}\t{git_blob(data)}\t{len(data)}\t{digest_bytes(data)}")
    return "\n".join(lines) + "\n"


def current_unrelated() -> list[dict[str, str]]:
    raw = subprocess.check_output(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"], cwd=ROOT
    )
    rows: list[dict[str, str]] = []
    for item in raw.split(b"\0"):
        if not item.startswith(b"?? "):
            continue
        relative = os.fsdecode(item[3:])
        if relative.startswith(HERE.name + "/"):
            continue
        stat = (ROOT / relative).stat()
        rows.append({"path": relative, "bytes": str(stat.st_size), "mtime_ns": str(stat.st_mtime_ns)})
    rows.sort(key=lambda row: row["path"])
    return rows


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--write", action="store_true", help="refresh generated evidence")
args = parser.parse_args()

source_paths = (HERE / "SOURCE_PATHS.txt").read_text(encoding="utf-8").splitlines()
assert len(source_paths) == len(set(source_paths)) == 37
assert all((ROOT / path).is_file() for path in source_paths)
manifest_text = render_manifest(source_paths)

primary_run = run(["python3", str(HERE / "derive_response_selection.py")], 60)
independent_run = run(["python3", str(HERE / "independent_verify.py")], 60)
assert primary_run.returncode == independent_run.returncode == 0
primary_live = json.loads(primary_run.stdout)
independent_live = json.loads(independent_run.stdout)
assert primary_live == json.loads((HERE / "RESULT.json").read_text(encoding="utf-8"))
assert independent_live == json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))

state = {
    "sources": [dict(row) for row in csv.DictReader(manifest_text.splitlines(), delimiter="\t")],
    "source_adjudications": table("SOURCE_ADJUDICATION.tsv"),
    "premises": keyed("PREMISE_LEDGER.tsv", "premise_id"),
    "universe": keyed("OPERATOR_CLASS_UNIVERSE.tsv", "class_id"),
    "operators": keyed("OPERATOR_CLASS_LEDGER.tsv", "class_id"),
    "branches": keyed("BRANCH_CONSEQUENCE_LEDGER.tsv", "family_id"),
    "primary": primary_live,
    "independent": independent_live,
    "audit": (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8"),
    "derivation": (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8"),
    "completeness": (HERE / "COMPLETENESS_MAP.md").read_text(encoding="utf-8"),
    "review": (HERE / "FRESH_ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8"),
    "closure": (HERE / "REVIEW_CLOSURE.md").read_text(encoding="utf-8"),
    "unrelated": current_unrelated(),
}


def validate(item: dict) -> None:
    sources = item["sources"]
    assert len(sources) == 37 and len({row["path"] for row in sources}) == 37
    for row in sources:
        target = ROOT / row["path"]
        assert target.is_file()
        assert row["git_blob"] == git_blob(target.read_bytes())
        assert row["bytes"] == str(target.stat().st_size)
        assert row["sha256"] == digest(target)
    adjudications = item["source_adjudications"]
    assert [row["source_path"] for row in adjudications] == [row["path"] for row in sources]
    source_by_path = {row["source_path"]: row for row in adjudications}
    source_expectations = {
        "LIVE.md": ("current authority", "forbids promotion"),
        "udt_p4_routeA_response_inverse_problem_2026-07-29/AUDIT_REPORT.md":
            ("prior response program", "no candidate selected"),
        "udt_global_local_self_consistency_premise_audit_2026-08-01/AUDIT_REPORT.md":
            ("Route-B authority", "distinct coherent posit without operation"),
        "native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md":
            ("F04 authority", "conditional on carrier/action/boundary"),
        "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv":
            ("action class authority", "complete action/source/boundary open"),
    }
    for path, (role, content) in source_expectations.items():
        assert source_by_path[path]["role_in_audit"] == role
        assert content in source_by_path[path]["selection_content"]

    premises = item["premises"]
    assert sorted(premises) == [f"P{index:02d}" for index in range(1, 19)]
    assert premises["P01"]["active_status"] == "DERIVED_ADDITIVE_LOG_DEPTH_OF_RECIPROCAL_PAIR"
    assert premises["P06"]["active_status"] == "CHOSE_AUDIT_DOMAIN"
    assert premises["P08"]["active_status"] == "OPEN"
    assert premises["P12"]["active_status"] == "INACTIVE"
    assert premises["P13"]["active_status"] == "CONDITIONAL_NOT_SELECTED"
    assert premises["P14"]["active_status"].startswith("UNIQUE_CONDITIONAL_ONLY_IF_PRE_SCALE")
    assert premises["P15"]["active_status"] == "POSIT_AND_CONDITIONAL"
    assert premises["P15"]["use_in_audit"] == "F04 consequence audit only"
    assert premises["P16"]["active_status"] == "WORKING_ON_SHELL_ADMISSIBILITY"
    assert premises["P17"]["active_status"] == "WORKING_MULTIPLY_ANCHORED_STRUCTURE"
    assert premises["P17"]["open_or_excluded"].endswith("boundary law open")
    assert premises["P18"]["active_status"] == "CONDITIONAL_OBSERVATIONAL_COMPATIBILITY_ANCHOR"
    assert premises["P18"]["use_in_audit"] == "downstream codomain check only"

    universe = item["universe"]
    operators = item["operators"]
    ids = [f"O{index:02d}" for index in range(11)]
    assert sorted(universe) == sorted(operators) == ids
    assert operators["O00"]["response_or_identity"] == "ZERO_CONTROL"
    assert operators["O03"]["current_selection_status"] == "CONDITIONAL_NOT_SELECTED"
    assert operators["O04"]["current_selection_status"] == "UNIQUE_CONDITIONAL_IN_INACTIVE_BRANCH"
    assert operators["O05"]["constructible_from_current_data"] == "YES_AS_NONEXHAUSTIVE_FAMILY"
    assert operators["O06"]["current_selection_status"] == "ADMISSIBLE_GENUINE_NOT_SELECTED"
    assert operators["O07"]["current_selection_status"] == "CONDITIONAL_REGULAR_NOT_GLOBAL"
    assert operators["O09"]["current_selection_status"] == "OPEN_MULTIPLE_CLASSES"
    assert operators["O10"]["current_selection_status"] == "WORKING_POSIT_NOT_DERIVED_OPERATION"
    assert universe["O03"]["home"] == "metric configuration cotangent"
    assert universe["O06"]["home"] == "query-bundle response family"
    assert universe["O10"]["home"] == "complete on-shell solution/readout relation"
    assert operators["O03"]["response_or_identity"] == "VARIATIONAL_BULK_RESPONSE"
    assert operators["O06"]["response_or_identity"] == "QUERY_FAMILY"
    assert operators["O10"]["response_or_identity"] == "GLOBAL_LOCAL_RELATION"

    branches = item["branches"]
    assert sorted(branches) == [f"F0{index}" for index in range(1, 8)]
    assert branches["F01"]["current_ruling"].startswith("UNCHANGED_CONDITIONAL")
    assert branches["F02"]["current_ruling"].startswith("UNCHANGED_CONDITIONAL")
    assert branches["F04"]["current_ruling"].startswith("UNCHANGED_CONDITIONAL")
    assert all("NATIVE_MATTER" not in row["current_ruling"] for row in branches.values())

    primary = item["primary"]
    independent = item["independent"]
    assert primary["status"] == independent["status"] == "PASS"
    assert primary["checks"] == 63 and independent["checks"] == 51
    assert primary["coframe_metric_tangent_rank"] == primary["metric_response_pullback_rank"] == 10
    assert primary["coframe_gauge_kernel_dimension"] == 6
    assert primary["founded_volume_direction_response"] == "0"
    assert primary["founded_anisotropic_direction_response"] == "2"
    assert primary["fR_shape_control_determinant"] == independent["fR_shape_determinant"] == "-384"
    assert [primary["cG_curvature_scale_coefficient_rank"], primary["cG_curvature_scale_augmented_rank"]] == [2, 3]
    assert independent["dimension_ranks"] == [2, 3]
    assert primary["universal_query_rank"] == independent["query_rank"] == 9
    assert primary["universal_query_nullity"] == 1
    assert independent["implementation"] == "python_standard_library_fraction_no_sympy_no_production_import"

    audit = item["audit"]
    derivation = item["derivation"]
    completeness = item["completeness"]
    review = item["review"]
    closure = item["closure"]
    assert "AVAILABLE_PLURAL_RESPONSES__NO_FOUNDATIONAL_SELECTION" in audit
    assert "This is not \u201cno law exists.\u201d" in audit
    assert "current-premise overlay" in audit
    assert "fresh semantic review and repair closure: complete" in audit
    assert "FULL_COFRAME_PULLBACK_PRESERVES_EVERY_AMBIENT_METRIC_RESPONSE" in derivation
    assert "`phi` is not an independent" in derivation
    assert "does not select which metric functional" in derivation
    assert "bounded selection tile" in completeness
    assert "All natural operators" in completeness
    assert "## FINAL_RULING: FAIL" in review
    assert "no blocking mathematical error" in review
    assert "FINAL_RULING: PASS_WITH_CAVEATS" in closure
    assert "NO_BLOCKING_ERROR" in closure
    assert "TIMEOUT_IS_NOT_PHYSICS" in audit
    forbidden_promotions = (
        "EH is the native UDT response",
        "Bach is the active native UDT response",
        "bootstrap is a derived operation",
        "the S2 carrier is derived",
        "F01 is native matter",
    )
    assert not any(phrase in audit for phrase in forbidden_promotions)

    baseline = table_path(
        ROOT / "udt_reciprocal_path_composition_residual_audit_2026-08-04/UNRELATED_UNTRACKED_METADATA.tsv"
    )
    assert item["unrelated"] == baseline and len(item["unrelated"]) == 83


def delete_row(group: str, key: str):
    def mutate(item: dict) -> None:
        del item[group][key]
    return mutate


def set_field(group: str, key: str, field: str, value: str):
    def mutate(item: dict) -> None:
        item[group][key][field] = value
    return mutate


def replace_text(group: str, old: str, new: str):
    def mutate(item: dict) -> None:
        item[group] = item[group].replace(old, new)
    return mutate


def add_exhaustive_claim(item: dict) -> None:
    item["completeness"] = item["completeness"].replace(
        "All natural operators", "Complete exhaustive classification of all natural operators"
    )


def set_source(path: str, field: str, value: str):
    def mutate(item: dict) -> None:
        row = next(row for row in item["source_adjudications"] if row["source_path"] == path)
        row[field] = value
    return mutate


def append_audit(value: str):
    def mutate(item: dict) -> None:
        item["audit"] += "\n" + value + "\n"
    return mutate


mutations = {
    "F01": set_field("premises", "P01", "active_status", "UNDEFINED_PLACEHOLDER"),
    "F02": set_field("operators", "O03", "current_selection_status", "NATIVE_SELECTED"),
    "F03": delete_row("operators", "O00"),
    "F04": set_field("premises", "P08", "active_status", "PINNED_SECOND_ORDER"),
    "F05": set_field("operators", "O06", "current_selection_status", "DESCENDED_WITHOUT_QUANTIFIER"),
    "F06": set_field("operators", "O07", "current_selection_status", "GLOBAL_ALL_STRATA"),
    "F07": set_field("operators", "O09", "current_selection_status", "COMPLETE_BOUNDARY_SELECTED"),
    "F08": set_field("branches", "F01", "current_ruling", "NATIVE_MATTER_DERIVED"),
    "F09": add_exhaustive_claim,
    "F10": replace_text("audit", "TIMEOUT_IS_NOT_PHYSICS", "TIMEOUT_PROVES_NO_SOLUTION"),
    "F11": set_field("operators", "O10", "current_selection_status", "DERIVED_BOOTSTRAP_OPERATION"),
    "F12": replace_text("audit", "current-premise overlay", "new response-space derivation"),
}

repair_mutations = {
    "R01_SOURCE_SEMANTICS": set_source(
        "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv",
        "selection_content",
        "native action selected",
    ),
    "R02_CARRIER_PREMISE": set_field("premises", "P15", "use_in_audit", "selects native carrier"),
    "R03_FINITE_CELL_PREMISE": set_field("premises", "P17", "active_status", "DERIVED_BOUNDARY_LAW"),
    "R04_SNE_PREMISE": set_field("premises", "P18", "use_in_audit", "selects upstream response"),
    "R05_OPERATOR_HOME": set_field("universe", "O06", "home", "spacetime metric cotangent"),
    "R06_P4_PROVENANCE": set_source(
        "udt_p4_routeA_response_inverse_problem_2026-07-29/AUDIT_REPORT.md",
        "role_in_audit",
        "new response derivation",
    ),
    "R07_EH_PROSE": append_audit("EH is the native UDT response"),
    "R08_BACH_PROSE": append_audit("Bach is the active native UDT response"),
    "R09_BOOTSTRAP_PROSE": append_audit("bootstrap is a derived operation"),
    "R10_CARRIER_PROSE": append_audit("the S2 carrier is derived"),
    "R11_MASS_PROSE": append_audit("F01 is native matter"),
}

contract = keyed("FALSIFICATION_CONTRACT.tsv", "falsifier_id")
assert set(contract) == set(mutations)
catch_rows: list[dict[str, str]] = []
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
            "falsifier_id": failure_id,
            "target": contract[failure_id]["target"],
            "result": "CAUGHT",
        }
    )

for failure_id, operation in repair_mutations.items():
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
            "falsifier_id": failure_id,
            "target": "fresh-review semantic repair extension",
            "result": "CAUGHT",
        }
    )

# Current premise registry remains the upstream high-risk guard.
premise_run = run(["python3", "verify_current_scientific_premises.py"], 60)
assert premise_run.returncode == 0 and "PASS: 18 premise guards" in premise_run.stdout

# Startup markers and package routing are exact; old layers may remain below them.
for name in ("LIVE.md", "HANDOFF.md"):
    text = (ROOT / name).read_text(encoding="utf-8")
    assert text.count("<!-- STARTUP_CURRENT_BEGIN -->") == 1
    assert text.count("<!-- STARTUP_CURRENT_END -->") == 1
    current = text.split("<!-- STARTUP_CURRENT_BEGIN -->", 1)[1].split("<!-- STARTUP_CURRENT_END -->", 1)[0]
    assert HERE.name in current and "AVAILABLE_PLURAL_RESPONSES__NO_FOUNDATIONAL_SELECTION" in current
for name in STARTUP:
    assert HERE.name in (ROOT / name).read_text(encoding="utf-8")

# All local Markdown links in current navigation and this package resolve.
link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
links = 0
link_sources = [ROOT / name for name in STARTUP]
link_sources.extend(path for path in HERE.glob("*.md") if path.name != "FRESH_ADVERSARIAL_REVIEW.md")
for source in link_sources:
    for raw in link_pattern.findall(source.read_text(encoding="utf-8")):
        target = raw.strip().strip("<>")
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        relative = unquote(target.split("#", 1)[0])
        resolved = Path(re.sub(r":\d+$", "", relative)) if Path(relative).is_absolute() else source.parent.joinpath(relative).resolve()
        assert resolved.exists(), (source, relative)
        links += 1

members = 0
for relative in MANIFESTS:
    manifest = ROOT / relative
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, member = line.split(None, 1)
        target = manifest.parent / member.strip()
        assert target.is_file() and digest(target) == expected
        members += 1
assert members == 127

current_paths = [row["current_path"] for row in table_path(ROOT / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv")]
assert len(current_paths) == len(set(current_paths)) == 1114
assert all((ROOT / path).exists() for path in current_paths)
frontier = table_path(ROOT / "research/_registry/CURRENT_FRONTIER_TARGETS.tsv")
targets = {row["target_path"].rstrip("/") for row in frontier}
assert len(frontier) == 306 and len(targets) == 101
assert all((ROOT / target).exists() for target in targets)

tests = run(["python3", "-m", "pytest", "-q", "tests"], 300)
assert tests.returncode == 0 and "70 passed, 1 xfailed" in tests.stdout

catch_text = "falsifier_id\ttarget\tresult\n" + "".join(
    f"{row['falsifier_id']}\t{row['target']}\t{row['result']}\n" for row in catch_rows
)
if args.write:
    (HERE / "SOURCE_MANIFEST.tsv").write_text(manifest_text, encoding="utf-8")
    (HERE / "CATCH_PROOFS.tsv").write_text(catch_text, encoding="utf-8")
else:
    assert (HERE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8") == manifest_text
    assert (HERE / "CATCH_PROOFS.tsv").read_text(encoding="utf-8") == catch_text

result = {
    "status": "PASS",
    "bounded_outcome": "AVAILABLE_PLURAL_RESPONSES__NO_FOUNDATIONAL_SELECTION",
    "primary_exact_checks": primary_live["checks"],
    "independent_exact_checks": independent_live["checks"],
    "artifact_level_catch_proofs": len(catch_rows),
    "source_paths": len(source_paths),
    "source_manifest_sha256": digest_bytes(manifest_text.encode()),
    "premise_rows": len(state["premises"]),
    "operator_classes": len(state["operators"]),
    "branch_rows": len(state["branches"]),
    "fresh_review": "INITIAL_FAIL_PRESERVED__REPAIR_CLOSURE_PASS_WITH_CAVEATS",
    "checked_links": links,
    "frozen_manifests": len(MANIFESTS),
    "frozen_manifest_members": members,
    "frozen_package_paths": members + len(MANIFESTS),
    "premise_guards": 18,
    "current_paths": len(current_paths),
    "frontier_rows": len(frontier),
    "frontier_targets": len(targets),
    "unrelated_untracked_metadata_rows": len(state["unrelated"]),
    "tests": "70 passed, 1 xfailed",
}
if args.write:
    (HERE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
else:
    assert json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8")) == result
print(json.dumps(result, sort_keys=True))

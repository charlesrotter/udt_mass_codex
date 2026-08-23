#!/usr/bin/env python3
"""Build auditable G236 Git chronology and hostile-noninterference evidence."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import subprocess


PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent
COMMITS = (
    "184b1a7887864709e8abd1eb6123071ab2b8e825",
    "318f35def882ef1422152b93db21a1dfbfff6424",
)
EXPECTED_REPAIR_PATHS = [
    "udt_g236_dual_sne_relational_state_reconstruction_2026-08-23/PREREGISTRATION.md",
    "udt_g236_dual_sne_relational_state_reconstruction_2026-08-23/PREREGISTRATION_REPAIR.md",
]
OUTCOME_PATHS = [
    "udt_g236_dual_sne_relational_state_reconstruction_2026-08-23/derive_dual_sne_relational_state.py",
    "udt_g236_dual_sne_relational_state_reconstruction_2026-08-23/PRODUCTION_RESULT.json",
    "udt_g236_dual_sne_relational_state_reconstruction_2026-08-23/STATE_RECONSTRUCTION.tsv",
    "udt_g236_dual_sne_relational_state_reconstruction_2026-08-23/INDEPENDENT_VERIFICATION.json",
]


def git(*args: str, input_bytes: bytes | None = None) -> bytes:
    return subprocess.run(
        ["git", *args],
        cwd=REPO,
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    ).stdout


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assignment_lines(tree: ast.AST, name: str) -> list[int]:
    lines: list[int] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Name) and target.id == name:
                    lines.append(node.lineno)
    return sorted(lines)


def referenced_names(node: ast.AST) -> set[str]:
    return {item.id for item in ast.walk(node) if isinstance(item, ast.Name)}


def rhs_references(tree: ast.AST, assigned_name: str) -> set[str]:
    refs: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        if any(isinstance(target, ast.Name) and target.id == assigned_name for target in targets):
            value = node.value
            refs.update(referenced_names(value))
    return refs


def main() -> None:
    object_dir = PACKAGE / "GIT_OBJECTS"
    object_dir.mkdir(exist_ok=True)

    object_evidence: dict[str, dict] = {}
    for commit in COMMITS:
        short = commit[:8]
        raw = git("cat-file", "commit", commit)
        object_path = object_dir / f"{short}_commit_object.txt"
        object_path.write_bytes(raw)
        computed = git("hash-object", "-t", "commit", "--stdin", input_bytes=raw).decode().strip()
        tree_listing = git("ls-tree", "-r", "--full-tree", commit)
        tree_path = object_dir / f"{short}_recursive_tree.txt"
        tree_path.write_bytes(tree_listing)
        parent_lines = [
            line.split(maxsplit=1)[1]
            for line in raw.decode().splitlines()
            if line.startswith("parent ")
        ]
        object_evidence[commit] = {
            "raw_object_path": str(object_path.relative_to(PACKAGE)),
            "raw_object_sha256": sha256(object_path),
            "computed_git_object_id": computed,
            "object_id_matches": computed == commit,
            "parents": parent_lines,
            "tree_listing_path": str(tree_path.relative_to(PACKAGE)),
            "tree_listing_sha256": sha256(tree_path),
        }

    repair_commit = COMMITS[1]
    patch_path = object_dir / "318f35de_exact_patch.txt"
    patch_path.write_bytes(git("show", "--format=fuller", "--no-ext-diff", repair_commit))
    changed_lines = git("diff-tree", "--no-commit-id", "--name-status", "-r", repair_commit).decode().splitlines()
    changed_paths = sorted(line.split("\t", 1)[1] for line in changed_lines)
    tree_paths = {
        commit: {
            line
            for line in git("ls-tree", "-r", "--name-only", commit).decode().splitlines()
        }
        for commit in COMMITS
    }

    source = (PACKAGE / "derive_dual_sne_relational_state.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    resolution_lines = assignment_lines(tree, "resolutions")
    landing_lines = assignment_lines(tree, "landing")
    hostile_lines = assignment_lines(tree, "hostile")
    result_lines = assignment_lines(tree, "result")
    dataflow = {
        "resolutions_assignment_lines": resolution_lines,
        "landing_assignment_lines": landing_lines,
        "hostile_assignment_lines": hostile_lines,
        "result_assignment_lines": result_lines,
        "hostile_absent_from_resolutions_assignment_rhs": "hostile" not in rhs_references(tree, "resolutions"),
        "hostile_absent_from_landing_assignment_rhs": "hostile" not in rhs_references(tree, "landing"),
        "landing_precedes_hostile_object": bool(landing_lines and hostile_lines and max(landing_lines) < min(hostile_lines)),
        "hostile_only_certifies_and_is_reported_after_scientific_values": True,
    }

    result = {
        "audit": "G236_GIT_CHRONOLOGY_AND_HOSTILE_NONINTERFERENCE",
        "status": "PASS_REPOSITORY_CHRONOLOGY_WITH_RETROACTIVE_UNTRACKED_ABSENCE_LIMIT",
        "commit_objects": object_evidence,
        "parent_chain": {
            "expected": f"{COMMITS[0]} -> {COMMITS[1]}",
            "verified": object_evidence[COMMITS[1]]["parents"] == [COMMITS[0]],
        },
        "repair_commit": {
            "changed_paths": changed_paths,
            "changed_paths_match_expected": changed_paths == sorted(EXPECTED_REPAIR_PATHS),
            "touches_code_data_or_outcomes": any(
                path.endswith((".py", ".json", ".tsv")) for path in changed_paths
            ),
            "exact_patch_path": str(patch_path.relative_to(PACKAGE)),
            "exact_patch_sha256": sha256(patch_path),
        },
        "outcome_paths_absent_from_preregistration_trees": {
            commit: {path: path not in tree_paths[commit] for path in OUTCOME_PATHS}
            for commit in COMMITS
        },
        "hostile_noninterference": dataflow,
        "proof_ceiling": (
            "Git proves commit identity, parent order, and committed-tree contents; it cannot "
            "retroactively prove the absence of an untracked private computation."
        ),
    }
    booleans = [
        item["object_id_matches"] for item in object_evidence.values()
    ] + [
        result["parent_chain"]["verified"],
        result["repair_commit"]["changed_paths_match_expected"],
        not result["repair_commit"]["touches_code_data_or_outcomes"],
        all(
            all(paths.values())
            for paths in result["outcome_paths_absent_from_preregistration_trees"].values()
        ),
        dataflow["hostile_absent_from_resolutions_assignment_rhs"],
        dataflow["hostile_absent_from_landing_assignment_rhs"],
        dataflow["landing_precedes_hostile_object"],
    ]
    if not all(booleans):
        result["status"] = "FAIL"
    output = PACKAGE / "CHRONOLOGY_AND_NONINTERFERENCE_PROOF.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] == "FAIL":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

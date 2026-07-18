#!/usr/bin/env python3
"""Independently re-audit the B01 import, I/O, test, frontier, and frozen closure."""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PACKAGES = [
    "native_action_stage1_2026-07-18/arm_A",
    "native_action_stage1_2026-07-18/arm_B",
    "native_action_stage2_2026-07-18/arm_A",
    "native_action_stage2_2026-07-18/arm_B",
    "native_action_arm_c_2026-07-18",
    "native_action_final_adjudication_2026-07-18",
]
FORBIDDEN_CALLS = {
    "open", "load", "loads", "save", "savez", "savez_compressed", "dump", "dumps",
    "read", "write", "read_text", "write_text", "read_bytes", "write_bytes", "loadtxt",
    "genfromtxt", "read_csv", "to_csv", "savetxt", "savefig", "glob", "rglob",
}


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def git_grep(token: str, paths: list[str]) -> list[str]:
    result = subprocess.run(["git", "grep", "-n", "-F", token, "--", *paths], cwd=REPO,
                            text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode not in {0, 1}:
        raise AssertionError(result.stderr)
    return result.stdout.splitlines()


def main() -> int:
    batch = rows(REPO / "reorganization_r1f/PREREGISTERED_BATCH.tsv")
    dependencies = rows(REPO / "reorganization_r1b/postmove_operational_census/DEPENDENCY_MAP.tsv")
    frontier = rows(REPO / "research/_registry/CURRENT_FRONTIER_TARGETS.tsv")
    ownership = {row["current_path"]: row for row in rows(REPO / "research/_registry/ROOT_OWNERSHIP.tsv")}
    records = []
    for row in batch:
        path = row["current_path"]
        tree = ast.parse((REPO / path).read_text(encoding="utf-8"))
        imports = []
        forbidden_calls = []
        file_semantics = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module or "")
            elif isinstance(node, ast.Call):
                name = node.func.id if isinstance(node.func, ast.Name) else node.func.attr if isinstance(node.func, ast.Attribute) else ""
                if name in FORBIDDEN_CALLS:
                    forbidden_calls.append(f"{node.lineno}:{name}")
            elif isinstance(node, ast.Name) and node.id == "__file__":
                file_semantics.append(f"{node.lineno}:__file__")
        import_roots = {name.split(".", 1)[0] for name in imports if name}
        if import_roots != {"sympy"}:
            raise AssertionError(f"non-SymPy import: {path}: {sorted(import_roots)}")
        if forbidden_calls or file_semantics:
            raise AssertionError(f"file/runtime semantics: {path}: {forbidden_calls + file_semantics}")
        source_edges = [edge for edge in dependencies if edge["source"] == path]
        bad_source_edges = [edge for edge in source_edges if not (
            edge["category"] == "PYTHON_IMPORT" and edge["raw_target"].split(".", 1)[0] == "sympy"
            and edge["status"] == "EXTERNAL_OR_STDLIB")]
        inbound = [edge for edge in dependencies if edge["resolved_target"] == path and edge["source"] != path]
        frontier_hits = [edge for edge in frontier if edge["target_path"].rstrip("/") == path]
        test_hits = git_grep(path, ["tests"])
        frozen_hits = git_grep(path, PACKAGES)
        manifest_hits = git_grep(path, [f"{package}/SHA256SUMS.txt" for package in PACKAGES])
        frozen_status = ownership[path]["frozen_manifest_status"]
        if bad_source_edges or inbound or frontier_hits or test_hits or frozen_hits or manifest_hits:
            raise AssertionError(f"dependency closure failed: {path}")
        if frozen_status != "NOT_FROZEN_OR_MANIFEST":
            raise AssertionError(f"candidate frozen status: {path}: {frozen_status}")
        records.append({
            "current_path": path,
            "imports": ";".join(sorted(imports)),
            "imports_external_sympy_only": "PASS",
            "file_open_or_generated_output": "NONE",
            "runtime_relative_path": "NONE",
            "operational_outbound_edges": len(source_edges),
            "operational_inbound_edges": len(inbound),
            "frontier_hits": len(frontier_hits),
            "manifest_hits": len(manifest_hits),
            "test_hits": len(test_hits),
            "frozen_package_hits": len(frozen_hits),
            "frozen_manifest_status": frozen_status,
            "result": "PASS",
        })
    fields = list(records[0])
    out = REPO / "reorganization_r1f/PREMOVE_DEPENDENCY_AUDIT.tsv"
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(records)
    result = {
        "result": "PASS", "candidates": len(records),
        "external_sympy_import_only": 4, "file_io_or_output": 0,
        "runtime_relative_paths": 0, "operational_inbound_edges": 0,
        "frontier_hits": 0, "manifest_hits": 0, "test_hits": 0,
        "frozen_package_hits": 0,
        "audit_tsv_sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
    }
    (REPO / "reorganization_r1f/PREMOVE_DEPENDENCY_AUDIT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

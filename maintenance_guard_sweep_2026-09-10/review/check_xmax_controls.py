#!/usr/bin/env python3
"""Actual isolated Xmax control-gate probes; maintenance, not scientific proof."""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
SOURCE = "udt_g163_xmax_dependency_reversal_audit_2026-08-18/AUDIT_REPORT.md"
ROUTE = "udt_g163_xmax_dependency_reversal_audit_2026-08-18/"
CONTROLS = ("AGENTS.md", "LIVE.md", "CURRENT_SCIENTIFIC_PREMISES.md", "INDEX.md")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assigned(node, name):
    return isinstance(node, ast.Assign) and any(
        isinstance(target, ast.Name) and target.id == name for target in node.targets)


def main():
    tree = ast.parse((ROOT / "verify_current_scientific_premises.py").read_text())
    helper = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "require")
    body = next(n.body for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main")
    start = next(i for i, n in enumerate(body) if assigned(n, "xmax_controls"))
    end = next(i for i, n in enumerate(body) if assigned(n, "adjudication"))
    code = compile(ast.Module(body=[helper] + body[start:end], type_ignores=[]), "<actual-Xmax-control-block>", "exec")
    paths = (*CONTROLS, SOURCE)
    before = {path: sha(ROOT / path) for path in paths}
    results = {"kind": "MAINTENANCE_NOT_SCIENTIFIC_PROOF", "model": "UNKNOWN",
               "python_version": sys.version, "harness_sha256": sha(Path(__file__)),
               "root_verifier_sha256": sha(ROOT / "verify_current_scientific_premises.py"),
               "source_hashes": before, "actual_block_ast": ast.dump(ast.Module(body=body[start:end], type_ignores=[])),
               "cases": []}
    with tempfile.TemporaryDirectory(prefix="xmax_controls_review_", dir="/tmp") as directory:
        scratch = Path(directory)
        for relative in paths:
            destination = scratch / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, destination)

        def probe(label, expected_message=None, limitation=False):
            try:
                exec(code, {"ROOT": scratch})
                message = None
            except SystemExit as exc:
                message = str(exc)
            if message != expected_message:
                raise RuntimeError(f"{label}: expected {expected_message!r}, observed {message!r}")
            results["cases"].append({"label": label, "passed": message is None,
                                      "message": message, "limitation_probe": limitation})

        probe("restored_controls")
        for relative in CONTROLS[:3]:
            path = scratch / relative
            original = path.read_text()
            if "asymptot" not in original.lower() or "X_max" not in original:
                raise RuntimeError(f"Mutation precondition absent: {relative}")
            path.write_text(original.replace("asymptot", "REMOVED_LIMITING_MEANING"))
            probe("limiting_qualifier_removed:" + relative, f"control lacks Xmax limiting meaning: {relative}")
            path.write_text(original.replace("X_max", "REMOVED_SCALE_SYMBOL"))
            probe("scale_symbol_removed:" + relative, f"control lacks Xmax guard: {relative}")
            path.write_text(original)
        index = scratch / "INDEX.md"
        original = index.read_text()
        if ROUTE not in original:
            raise RuntimeError("Restored G163 route absent")
        index.write_text(original.replace(ROUTE, "REMOVED_CONTROLLING_ROUTE/"))
        probe("source_route_removed", "INDEX lacks controlling Xmax dependency-reversal route")
        index.write_text(original)
        evidence = scratch / SOURCE
        original_evidence = evidence.read_bytes()
        evidence.unlink()
        probe("controlling_source_missing", "controlling Xmax correction source missing")
        evidence.write_bytes(original_evidence)
        live = scratch / "LIVE.md"
        original = live.read_text()
        live.write_text(original + "\nA finite physical separation maximum is now derived.\n")
        probe("token_preserving_overclaim_ISOLATED_BLOCK_LIMITATION", limitation=True)
        live.write_text(original)
        probe("restored_fixture")
    after = {path: sha(ROOT / path) for path in paths}
    if before != after:
        raise RuntimeError("Live sources changed during isolated probes")
    results["live_sources_unchanged"] = True
    results["status"] = "PASS_BOUNDED_CONTROLS_WITH_RECORDED_LIMITATION"
    results["limitations"] = [
        "Selected literal/existence control block only, not all full365 semantic controls.",
        "Token-preserving contradictory scope can pass this isolated block; no completeness claimed.",
        "G163 mathematics, numerical evidence and historical descendants were not re-proved."]
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

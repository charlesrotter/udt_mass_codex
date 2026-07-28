#!/usr/bin/env python3
"""Repository gates for the joint-selector provenance audit."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "5372ae9"
PACKAGE = HERE.name
CONTROLS = {
    "LIVE.md", "HANDOFF.md", "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
    "INDEX.md", "README.md", "MEMORY.md", "AGENTS.md",
}
EXPECTED_DIRTY_COUNT = 55
EXPECTED_DIRTY_SHA256 = "345d297e0ad849cd38f1d817c915922de653ca2d2befcf923af6f9d097b483e4"


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    environment = dict(os.environ)
    environment.update({"CUDA_VISIBLE_DEVICES": "", "PYTHONDONTWRITEBYTECODE": "1"})
    return subprocess.run(command, cwd=ROOT, env=environment, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)


def require(process: subprocess.CompletedProcess[str]) -> None:
    if process.returncode:
        raise AssertionError(process.stdout)


def generic_module():
    path = ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19/verify_repository_gates.py"
    spec = importlib.util.spec_from_file_location("joint_selector_generic_repository_gates", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.PACKAGE = PACKAGE
    return module


def main() -> None:
    scope_process = run(["git", "diff", "--name-only", f"{BASE}..HEAD"])
    require(scope_process)
    committed_scope = [line for line in scope_process.stdout.splitlines() if line]
    status = run(["git", "status", "--short"])
    require(status)
    task_worktree = [
        line[3:] for line in status.stdout.splitlines()
        if line[3:].startswith(PACKAGE + "/") or line[3:] in CONTROLS
    ]
    scope = sorted(set(committed_scope + task_worktree))
    allowed = [path for path in scope if path.startswith(PACKAGE + "/") or path in CONTROLS]
    if not scope or sorted(scope) != sorted(allowed):
        raise AssertionError(f"scope escaped package/navigation controls: {sorted(set(scope)-set(allowed))}")
    if run(["git", "diff", "--name-only", BASE, "--", "CANON.md"]).stdout.strip():
        raise AssertionError("CANON.md changed")

    unrelated = [
        line for line in status.stdout.splitlines()
        if not line[3:].startswith(PACKAGE + "/") and line[3:] not in CONTROLS
    ]
    unrelated_text = "".join(line + "\n" for line in unrelated)
    dirty_count = len(unrelated)
    dirty_sha = hashlib.sha256(unrelated_text.encode()).hexdigest()
    if dirty_count != EXPECTED_DIRTY_COUNT or dirty_sha != EXPECTED_DIRTY_SHA256:
        raise AssertionError(f"unrelated dirty metadata changed: {dirty_count} {dirty_sha}")

    generic = generic_module()
    frozen = generic.validate_frozen(ROOT)
    navigation = generic.validate_navigation(ROOT)
    package_manifest = generic.validate_package_manifest(ROOT)

    audit = run([sys.executable, str(HERE / "verify_audit.py")])
    premises = run([sys.executable, "verify_current_scientific_premises.py"])
    tests = run([sys.executable, "-m", "pytest", "-q", "tests/"])
    for process in (audit, premises, tests):
        require(process)
    match = re.search(r"(\d+) passed, (\d+) xfailed", tests.stdout)
    if match is None or tuple(map(int, match.groups())) != (70, 1):
        raise AssertionError(tests.stdout)

    result = {
        "schema": "udt-joint-selector-repository-gates-1.0",
        "status": "PASS",
        "verified_head": run(["git", "rev-parse", "HEAD"]).stdout.strip(),
        "scope_base": BASE,
        "scope_paths": scope,
        "dirty_checkout": {"paths": dirty_count, "metadata_sha256": dirty_sha, "contents_read": False, "result": "PASS"},
        "frozen": frozen,
        "navigation": navigation,
        "package_manifest": package_manifest,
        "audit": {
            "source_files": 3044, "groups": 80, "candidate_constructions": 16,
            "obligations": 15, "counterfamilies": 6, "catch_proofs": 30,
            "complete_joint_operations": 0,
            "status": "PASS_VERIFIED_WITH_CAVEATS_SAME_SESSION",
            "stdout_sha256": hashlib.sha256(audit.stdout.encode()).hexdigest(),
        },
        "current_premises": {"result": "PASS", "stdout_sha256": hashlib.sha256(premises.stdout.encode()).hexdigest()},
        "tests": {"passed": 70, "failed": 0, "xfailed": 1, "result": "PASS", "stdout_sha256": hashlib.sha256(tests.stdout.encode()).hexdigest()},
        "authority_boundary": {
            "GPU_launched": False, "P03B_launched": False, "ODE_PDE_time_live_launched": False,
            "action_source_carrier_boundary_density_bootstrap_selected": False,
            "physical_global_branch_selected": False, "canon_changed": False,
            "repository_reorganization_performed": False,
        },
    }
    (HERE / "REPOSITORY_GATES.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()

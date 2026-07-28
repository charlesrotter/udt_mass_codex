#!/usr/bin/env python3
"""Repository gates for P01 without reading unrelated dirty-file contents."""

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
BASE = "401805c"
PACKAGE = HERE.name
EXPECTED_DIRTY_COUNT = 55
EXPECTED_DIRTY_SHA256 = "345d297e0ad849cd38f1d817c915922de653ca2d2befcf923af6f9d097b483e4"


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    environment = dict(os.environ)
    environment.update({"CUDA_VISIBLE_DEVICES": "", "PYTHONDONTWRITEBYTECODE": "1"})
    return subprocess.run(command, cwd=ROOT, env=environment, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)


def require(process: subprocess.CompletedProcess[str]) -> None:
    if process.returncode:
        raise AssertionError(process.stdout)


def generic_module():
    path = ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19/verify_repository_gates.py"
    spec = importlib.util.spec_from_file_location("p01_generic_repository_gates", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.PACKAGE = PACKAGE
    return module


def main() -> None:
    scope_process = run(["git", "diff", "--name-only", f"{BASE}..HEAD"])
    require(scope_process)
    scope = [line for line in scope_process.stdout.splitlines() if line]
    if not scope or any(not path.startswith(PACKAGE + "/") for path in scope):
        raise AssertionError("committed scope escaped package")
    status = run(["git", "status", "--short"])
    require(status)
    dirty_count = len(status.stdout.splitlines())
    dirty_sha = hashlib.sha256(status.stdout.encode()).hexdigest()
    if dirty_count != EXPECTED_DIRTY_COUNT or dirty_sha != EXPECTED_DIRTY_SHA256:
        raise AssertionError("unrelated dirty metadata changed")
    generic = generic_module()
    frozen = generic.validate_frozen(ROOT)
    navigation = generic.validate_navigation(ROOT)
    package = run([sys.executable, str(HERE / "verify_package.py")])
    premises = run([sys.executable, "verify_current_scientific_premises.py"])
    tests = run([sys.executable, "-m", "pytest", "-q", "tests/"])
    for process in (package, premises, tests):
        require(process)
    match = re.search(r"(\d+) passed, (\d+) xfailed", tests.stdout)
    if match is None or tuple(map(int, match.groups())) != (70, 1):
        raise AssertionError(tests.stdout)
    package_result = json.loads((HERE / "VERIFICATION_RESULT.json").read_text())
    result = {
        "schema": "udt-complete-coframe-metric-telescope-p01-repository-gates-1.0",
        "status": "PASS",
        "head": run(["git", "rev-parse", "HEAD"]).stdout.strip(),
        "scope_base": BASE,
        "scope_paths": scope,
        "dirty_checkout": {"paths": dirty_count, "metadata_sha256": dirty_sha, "contents_read": False, "result": "PASS"},
        "frozen": frozen,
        "navigation": navigation,
        "package": {"checks_passed": package_result["checks_passed"], "checks_total": package_result["checks_total"], "result": package_result["status"], "stdout_sha256": hashlib.sha256(package.stdout.encode()).hexdigest()},
        "current_premises": {"result": "PASS", "stdout_sha256": hashlib.sha256(premises.stdout.encode()).hexdigest()},
        "tests": {"passed": 70, "failed": 0, "xfailed": 1, "result": "PASS", "stdout_sha256": hashlib.sha256(tests.stdout.encode()).hexdigest()},
        "authority_boundary": {
            "live_or_canon_changed": False,
            "background_equation_or_physical_time_evolution_derived": False,
            "action_source_carrier_density_boundary_or_bootstrap_selected": False,
            "p02_or_further_gpu_work_authorized": False,
        },
    }
    (HERE / "REPOSITORY_GATES.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()

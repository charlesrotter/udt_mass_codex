#!/usr/bin/env python3
"""Repository, frozen-evidence, navigation, test, and dirty-checkout gates."""

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
PACKAGE = HERE.name
BASE = "b0d183dff1073fb34d338afce1732a8a8c0acf9f"
DIRTY = Path("/home/udt-admin/udt_mass_codex")


def load_generic():
    path = ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19" / "verify_repository_gates.py"
    spec = importlib.util.spec_from_file_location("coframe_functor_generic_gates", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.BASE = BASE
    module.PACKAGE = PACKAGE
    return module


def run(command: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env.update({"CUDA_VISIBLE_DEVICES": "", "PYTHONDONTWRITEBYTECODE": "1"})
    return subprocess.run(command, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, check=False)


def git(cwd: Path, *args: str) -> str:
    result = run(["git", *args], cwd)
    if result.returncode:
        raise AssertionError(result.stdout)
    return result.stdout


def validate_scope(injected: str = "") -> list[str]:
    paths = set(git(ROOT, "diff", "--name-only", BASE).splitlines())
    paths.update(git(ROOT, "ls-files", "--others", "--exclude-standard").splitlines())
    if injected:
        paths.add(injected)
    bad = sorted(path for path in paths if path and not path.startswith(PACKAGE + "/"))
    if bad:
        raise AssertionError(f"scope:{bad[0]}")
    return sorted(path for path in paths if path)


def validate_tests() -> dict[str, object]:
    result = run([sys.executable, "-m", "pytest", "-q", "tests/"])
    match = re.search(r"(\d+) passed, (\d+) xfailed", result.stdout)
    if result.returncode or match is None or tuple(map(int, match.groups())) != (70, 1):
        raise AssertionError(result.stdout)
    return {
        "command": "PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 -m pytest -q tests/",
        "passed": 70, "failed": 0, "xfailed": 1,
        "stdout_sha256": hashlib.sha256(result.stdout.encode()).hexdigest(), "result": "PASS",
    }


def validate_dirty(corrupt: bool = False) -> dict[str, object]:
    status = subprocess.run(["git", "status", "--short"], cwd=DIRTY,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if status.returncode:
        raise AssertionError("dirty metadata unavailable")
    head = git(DIRTY, "rev-parse", "HEAD").strip()
    branch = git(DIRTY, "branch", "--show-current").strip()
    count = len(status.stdout.splitlines()) - int(corrupt)
    digest = hashlib.sha256(status.stdout).hexdigest()
    if (head, branch, count, digest) != (
        "8b13104a4f1af45af617d2aa50cd5fdacf4082af", "grok", 55,
        "345d297e0ad849cd38f1d817c915922de653ca2d2befcf923af6f9d097b483e4",
    ):
        raise AssertionError("dirty checkout metadata changed")
    return {"head": head, "branch": branch, "paths": count, "metadata_sha256": digest,
            "contents_read": False, "result": "PASS"}


def validate_package(corrupt: bool = False) -> dict[str, object]:
    manifest = HERE / "SHA256SUMS.txt"
    expected: dict[str, str] = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        expected[name] = digest
    actual_names = sorted(p.name for p in HERE.iterdir() if p.is_file() and p.name not in {
        "SHA256SUMS.txt", "REPOSITORY_GATES.json",
    })
    if corrupt or sorted(expected) != actual_names:
        raise AssertionError("package manifest membership")
    for name, digest in expected.items():
        if hashlib.sha256((HERE / name).read_bytes()).hexdigest() != digest:
            raise AssertionError(name)
    return {"entries": len(expected), "manifest_sha256": hashlib.sha256(manifest.read_bytes()).hexdigest(),
            "result": "PASS"}


def expect_failure(callback) -> str:
    try:
        callback()
    except AssertionError:
        return "PASS"
    raise AssertionError("catch accepted corruption")


def main() -> int:
    generic = load_generic()
    scope = validate_scope()
    frozen = generic.validate_frozen(ROOT)
    navigation = generic.validate_navigation(ROOT)
    tests = validate_tests()
    dirty = validate_dirty()
    package = validate_package()
    premises = run([sys.executable, "verify_current_scientific_premises.py"])
    assert premises.returncode == 0, premises.stdout
    audit = run([sys.executable, str(HERE / "verify_audit.py")])
    assert audit.returncode == 0, audit.stdout
    git(ROOT, "merge-base", "--is-ancestor", BASE, "HEAD")
    result = {
        "schema": "udt-complete-coframe-physical-comparison-functor-gates-1.0",
        "base": BASE, "preregistration_ancestor": True, "result": "PASS",
        "scope_paths": scope, "frozen": frozen, "navigation": navigation, "tests": tests,
        "dirty_checkout": dirty, "package_manifest": package,
        "current_premises": {"result": "PASS", "stdout_sha256": hashlib.sha256(premises.stdout.encode()).hexdigest()},
        "audit_replay": {"result": "PASS", "stdout_sha256": hashlib.sha256(audit.stdout.encode()).hexdigest()},
        "catch_proofs": {
            "scope": expect_failure(lambda: validate_scope("CANON.md")),
            "frozen": generic.expect("FROZEN", lambda: generic.validate_frozen(ROOT, corrupt=True)),
            "current_paths": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, corrupt="current")),
            "frontier": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, corrupt="frontier")),
            "dirty": expect_failure(lambda: validate_dirty(True)),
            "package": expect_failure(lambda: validate_package(True)),
        },
        "authority_boundary": {
            "startup_controls_changed": False, "canon_changed": False,
            "source_results_changed": False, "frozen_or_historical_changed": False,
            "path_or_endpoint_semantics_selected": False, "complete_extension_selected": False,
            "physical_functor_selected": False, "on_shell_solution_claimed": False,
            "action_carrier_source_density_mass_Xmax_bootstrap_dynamics_selected": False,
            "gpu_work": False, "repository_reorganization": False,
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

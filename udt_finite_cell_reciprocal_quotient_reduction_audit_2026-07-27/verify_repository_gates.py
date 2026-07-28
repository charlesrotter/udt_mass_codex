#!/usr/bin/env python3
"""Repository, frozen evidence, navigation, tests, and dirty-metadata gates."""

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
BASE = "12b4a42"
EXPECTED_DIRTY_COUNT = 55
EXPECTED_DIRTY_SHA256 = "345d297e0ad849cd38f1d817c915922de653ca2d2befcf923af6f9d097b483e4"


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env.update({"CUDA_VISIBLE_DEVICES": "", "PYTHONDONTWRITEBYTECODE": "1"})
    return subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def git(*args: str) -> str:
    result = run(["git", *args])
    if result.returncode:
        raise AssertionError(result.stdout)
    return result.stdout


def generic_module():
    path = ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19" / "verify_repository_gates.py"
    spec = importlib.util.spec_from_file_location("finite_cell_reduction_generic_gates", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.PACKAGE = PACKAGE
    return module


def verify_scope(injected: str = "") -> list[str]:
    changed = set(git("diff", "--name-only", f"{BASE}..HEAD").splitlines())
    if injected:
        changed.add(injected)
    bad = sorted(path for path in changed if path and not path.startswith(PACKAGE + "/"))
    if bad:
        raise AssertionError(f"out-of-scope committed path: {bad[0]}")
    return sorted(changed)


def verify_dirty(corrupt: bool = False) -> dict[str, object]:
    raw = git("status", "--short")
    count = len(raw.splitlines()) - int(corrupt)
    digest = hashlib.sha256(raw.encode()).hexdigest()
    if count != EXPECTED_DIRTY_COUNT or digest != EXPECTED_DIRTY_SHA256:
        raise AssertionError("dirty metadata changed")
    return {
        "paths": count,
        "metadata_sha256": digest,
        "contents_read": False,
        "result": "PASS",
    }


def verify_package(corrupt: bool = False) -> dict[str, object]:
    manifest = HERE / "SHA256SUMS.txt"
    expected = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        expected[name] = digest
    excluded = {"SHA256SUMS.txt", "REPOSITORY_GATES.json"}
    actual = sorted(
        path.name for path in HERE.iterdir() if path.is_file() and path.name not in excluded
    )
    if corrupt or sorted(expected) != actual:
        raise AssertionError("package membership mismatch")
    for name, digest in expected.items():
        if hashlib.sha256((HERE / name).read_bytes()).hexdigest() != digest:
            raise AssertionError(f"package hash mismatch: {name}")
    return {
        "entries": len(expected),
        "manifest_sha256": hashlib.sha256(manifest.read_bytes()).hexdigest(),
        "result": "PASS",
    }


def expect_failure(callback) -> str:
    try:
        callback()
    except AssertionError:
        return "PASS"
    raise AssertionError("catch accepted corruption")


def main() -> None:
    generic = generic_module()
    git("merge-base", "--is-ancestor", BASE, "HEAD")
    scope = verify_scope()
    frozen = generic.validate_frozen(ROOT)
    navigation = generic.validate_navigation(ROOT)
    dirty = verify_dirty()
    package = verify_package()
    production = run([sys.executable, str(HERE / "derive_finite_cell_reduction.py")])
    independent = run(
        [sys.executable, "-S", str(HERE / "verify_finite_cell_reduction_independent.py")]
    )
    audit = run([sys.executable, str(HERE / "verify_audit.py")])
    premises = run([sys.executable, "verify_current_scientific_premises.py"])
    for item in (production, independent, audit, premises):
        if item.returncode:
            raise AssertionError(item.stdout)
    tests = run([sys.executable, "-m", "pytest", "-q", "tests/"])
    match = re.search(r"(\d+) passed, (\d+) xfailed", tests.stdout)
    if tests.returncode or match is None or tuple(map(int, match.groups())) != (70, 1):
        raise AssertionError(tests.stdout)
    result = {
        "schema": "udt-finite-cell-reciprocal-quotient-reduction-repository-gates-1.0",
        "base": BASE,
        "head": git("rev-parse", "HEAD").strip(),
        "result": "PASS",
        "scope_paths": scope,
        "frozen": frozen,
        "navigation": navigation,
        "dirty_checkout": dirty,
        "package": package,
        "production": {"result": "PASS", "stdout_sha256": hashlib.sha256(production.stdout.encode()).hexdigest()},
        "independent": {"result": "PASS", "stdout_sha256": hashlib.sha256(independent.stdout.encode()).hexdigest()},
        "audit": {"result": "PASS", "stdout_sha256": hashlib.sha256(audit.stdout.encode()).hexdigest()},
        "current_premises": {"result": "PASS", "stdout_sha256": hashlib.sha256(premises.stdout.encode()).hexdigest()},
        "tests": {
            "passed": 70,
            "failed": 0,
            "xfailed": 1,
            "result": "PASS",
            "stdout_sha256": hashlib.sha256(tests.stdout.encode()).hexdigest(),
        },
        "catch_proofs": {
            "scope": expect_failure(lambda: verify_scope("CANON.md")),
            "dirty": expect_failure(lambda: verify_dirty(True)),
            "package": expect_failure(lambda: verify_package(True)),
            "frozen": generic.expect("FROZEN", lambda: generic.validate_frozen(ROOT, corrupt=True)),
            "current_paths": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, corrupt="current")),
            "frontier": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, corrupt="frontier")),
        },
        "authority_boundary": {
            "startup_controls_changed": False,
            "canon_changed": False,
            "frozen_sources_changed": False,
            "GR_or_SR_physics_imported": False,
            "physical_quotient_branch_lambda_flag_connection_or_path_selected": False,
            "action_carrier_source_boundary_bootstrap_density_Xmax_mass_changed": False,
            "GPU_work": False,
            "repository_reorganization": False,
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

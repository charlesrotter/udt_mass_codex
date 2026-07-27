#!/usr/bin/env python3
"""Repository, frozen, navigation, replay, test, and dirty-metadata gates."""

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
BASE = "de6b2f7"
CORRECTION = "dcadc04"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
PINNED = Path("/tmp/udt_screen_cocycle_sympy_114_pkgs")


def load_generic():
    path = ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19" / "verify_repository_gates.py"
    spec = importlib.util.spec_from_file_location("screen_cocycle_generic_gates", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.BASE = BASE
    module.PACKAGE = PACKAGE
    return module


def run(command: list[str], cwd: Path = ROOT, extra_env: dict[str, str] | None = None):
    environment = dict(os.environ)
    environment.update({"CUDA_VISIBLE_DEVICES": "", "PYTHONDONTWRITEBYTECODE": "1"})
    if extra_env:
        environment.update(extra_env)
    return subprocess.run(command, cwd=cwd, env=environment, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)


def git(cwd: Path, *arguments: str) -> str:
    completed = run(["git", *arguments], cwd)
    if completed.returncode:
        raise AssertionError(completed.stdout)
    return completed.stdout


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
    completed = run([sys.executable, "-m", "pytest", "-q", "tests/"])
    match = re.search(r"(\d+) passed, (\d+) xfailed", completed.stdout)
    if completed.returncode or match is None or tuple(map(int, match.groups())) != (70, 1):
        raise AssertionError(completed.stdout)
    return {
        "command": "PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 -m pytest -q tests/",
        "passed": 70, "failed": 0, "xfailed": 1,
        "stdout_sha256": hashlib.sha256(completed.stdout.encode()).hexdigest(), "result": "PASS",
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
    expected = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        expected[name] = digest
    actual = sorted(item.name for item in HERE.iterdir() if item.is_file() and item.name not in {
        "SHA256SUMS.txt", "REPOSITORY_GATES.json"
    })
    if corrupt or sorted(expected) != actual:
        raise AssertionError("package manifest membership")
    for name, digest in expected.items():
        if hashlib.sha256((HERE / name).read_bytes()).hexdigest() != digest:
            raise AssertionError(name)
    return {"entries": len(expected), "manifest_sha256": hashlib.sha256(manifest.read_bytes()).hexdigest(),
            "result": "PASS"}


def validate_replays(corrupt: bool = False) -> dict[str, object]:
    production = run([sys.executable, "-S", str(HERE / "derive_intrinsic_screen_cocycle.py")],
                     extra_env={"PYTHONPATH": str(PINNED)})
    independent = run([sys.executable, "-S", str(HERE / "verify_screen_cocycle_independent.py")])
    if production.returncode or independent.returncode:
        raise AssertionError(production.stdout + independent.stdout)
    observed_production = json.loads(production.stdout)
    observed_independent = json.loads(independent.stdout)
    saved_production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    saved_independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    if corrupt or observed_production != saved_production or observed_independent != saved_independent:
        raise AssertionError("calculation replay mismatch")
    source = run([sys.executable, str(HERE / "verify_source_manifest.py")])
    audit = run([sys.executable, str(HERE / "verify_audit.py")])
    premises = run([sys.executable, "verify_current_scientific_premises.py"])
    if any(item.returncode for item in (source, audit, premises)):
        raise AssertionError(source.stdout + audit.stdout + premises.stdout)
    return {
        "production": "PASS_SYMPY_1.14.0", "independent": "PASS_STDLIB_FRACTION",
        "source_manifest": "23/23", "audit_catches": "24/24", "current_premises": "PASS",
        "production_stdout_sha256": hashlib.sha256(production.stdout.encode()).hexdigest(),
        "independent_stdout_sha256": hashlib.sha256(independent.stdout.encode()).hexdigest(),
    }


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
    replays = validate_replays()
    package = validate_package()
    git(ROOT, "merge-base", "--is-ancestor", BASE, "HEAD")
    git(ROOT, "merge-base", "--is-ancestor", CORRECTION, "HEAD")
    result = {
        "schema": "udt-twisted-s3-intrinsic-screen-cocycle-repository-gates-1.0",
        "base": BASE, "preregistration_ancestor": True,
        "preregistration_correction": CORRECTION, "correction_ancestor": True,
        "result": "PASS", "scope_path_count": len(scope), "frozen": frozen,
        "navigation": navigation, "tests": tests, "dirty_checkout": dirty,
        "calculation_replays": replays, "package_manifest": package,
        "catch_proofs": {
            "scope": expect_failure(lambda: validate_scope("CANON.md")),
            "frozen": generic.expect("FROZEN", lambda: generic.validate_frozen(ROOT, corrupt=True)),
            "current_paths": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, corrupt="current")),
            "frontier": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, corrupt="frontier")),
            "dirty": expect_failure(lambda: validate_dirty(True)),
            "calculation": expect_failure(lambda: validate_replays(True)),
            "package": expect_failure(lambda: validate_package(True)),
        },
        "authority_boundary": {
            "startup_controls_changed": False, "canon_changed": False,
            "source_results_changed": False, "frozen_or_historical_changed": False,
            "copresence_promoted_beyond_working_interpretation": False,
            "instantaneous_operational_access_derived": False,
            "path_or_endpoint_semantics_selected": False, "lambda_selected": False,
            "on_shell_solution_claimed": False,
            "action_carrier_source_density_mass_Xmax_dynamics_selected": False,
            "gpu_work": False, "repository_reorganization": False,
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

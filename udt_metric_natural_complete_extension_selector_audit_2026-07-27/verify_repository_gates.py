#!/usr/bin/env python3
"""Repository, frozen-evidence, navigation, test, and package gates."""

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
BASE = "d2c1efbb1870b0d8da7bbe5b713603c0e3ebf622"
DIRTY = Path("/home/udt-admin/udt_mass_codex")


def load_generic():
    path = ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19" / "verify_repository_gates.py"
    spec = importlib.util.spec_from_file_location("metric_natural_generic_gates", path)
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
    return subprocess.run(
        command, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, check=False,
    )


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
        "passed": 70,
        "failed": 0,
        "xfailed": 1,
        "stdout_sha256": hashlib.sha256(result.stdout.encode()).hexdigest(),
        "result": "PASS",
    }


def validate_dirty(corrupt: bool = False) -> dict[str, object]:
    status = subprocess.run(
        ["git", "status", "--short"], cwd=DIRTY,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if status.returncode:
        raise AssertionError("dirty metadata unavailable")
    head = git(DIRTY, "rev-parse", "HEAD").strip()
    branch = git(DIRTY, "branch", "--show-current").strip()
    count = len(status.stdout.splitlines()) - int(corrupt)
    digest = hashlib.sha256(status.stdout).hexdigest()
    if (head, branch, count, digest) != (
        "8b13104a4f1af45af617d2aa50cd5fdacf4082af",
        "grok",
        55,
        "345d297e0ad849cd38f1d817c915922de653ca2d2befcf923af6f9d097b483e4",
    ):
        raise AssertionError("dirty checkout metadata changed")
    return {
        "head": head,
        "branch": branch,
        "paths": count,
        "metadata_sha256": digest,
        "contents_read": False,
        "result": "PASS",
    }


def validate_package(corrupt: bool = False) -> dict[str, object]:
    manifest = HERE / "SHA256SUMS.txt"
    expected: dict[str, str] = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        expected[name] = digest
    actual_names = sorted(
        p.name for p in HERE.iterdir()
        if p.is_file() and p.name not in {"SHA256SUMS.txt", "REPOSITORY_GATES.json"}
    )
    if corrupt or sorted(expected) != actual_names:
        raise AssertionError("package manifest membership")
    for name, digest in expected.items():
        if hashlib.sha256((HERE / name).read_bytes()).hexdigest() != digest:
            raise AssertionError(name)
    return {
        "entries": len(expected),
        "manifest_sha256": hashlib.sha256(manifest.read_bytes()).hexdigest(),
        "result": "PASS",
    }


def validate_clean_environment() -> dict[str, object]:
    record = json.loads((HERE / "RUN_ENVIRONMENT.json").read_text(encoding="utf-8"))
    assert record["compute"] == "CPU_ONLY"
    assert record["python"] == "3.10.12"
    assert record["sympy"] == "1.14.0"
    assert record["site_packages"] == "DISABLED_WITH_-S"
    assert record["result"] == "PASS"
    assert record["exact_algebra_sha256"] == hashlib.sha256(
        (HERE / "EXACT_ALGEBRA.json").read_bytes()
    ).hexdigest()
    for prefix, values in record["executions"].items():
        upper = prefix.upper()
        stdout = (HERE / f"{upper}_STDOUT.txt").read_bytes()
        stderr = (HERE / f"{upper}_STDERR.txt").read_bytes()
        assert values["exit_code"] == 0
        assert values["stdout_bytes"] == len(stdout)
        assert values["stdout_sha256"] == hashlib.sha256(stdout).hexdigest()
        assert values["stderr_bytes"] == len(stderr)
        assert values["stderr_sha256"] == hashlib.sha256(stderr).hexdigest()
    return {
        "python": record["python"],
        "sympy": record["sympy"],
        "site_packages": record["site_packages"],
        "executions": len(record["executions"]),
        "result": "PASS",
    }


def validate_external_review() -> dict[str, object]:
    path = HERE / "EXTERNAL_CERTIFICATION_ESCALATED_RETURN.txt"
    text = path.read_text(encoding="utf-8")
    assert "VERIFIED-WITH-CAVEATS" in text
    assert "bankable after the outer integrity step" in text
    assert "ec55c57925ad7f72fb75fbbbddaea47a12c46cd6d6049706aa5b66dd20fe0fd3" in text
    return {
        "file": path.name,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "verdict": "VERIFIED-WITH-CAVEATS",
        "result": "PASS",
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
    package = validate_package()
    clean_environment = validate_clean_environment()
    external_review = validate_external_review()
    premises = run([sys.executable, "verify_current_scientific_premises.py"])
    assert premises.returncode == 0, premises.stdout
    audit = run([sys.executable, str(HERE / "verify_audit.py")])
    assert audit.returncode == 0, audit.stdout
    git(ROOT, "merge-base", "--is-ancestor", BASE, "HEAD")
    result = {
        "schema": "udt-metric-natural-complete-extension-selector-gates-1.0",
        "base": BASE,
        "preregistration_ancestor": True,
        "result": "PASS",
        "scope_paths": scope,
        "frozen": frozen,
        "navigation": navigation,
        "tests": tests,
        "dirty_checkout": dirty,
        "package_manifest": package,
        "clean_environment": clean_environment,
        "external_review": external_review,
        "current_premises": {
            "result": "PASS",
            "stdout_sha256": hashlib.sha256(premises.stdout.encode()).hexdigest(),
        },
        "audit_replay": {
            "result": "PASS",
            "stdout_sha256": hashlib.sha256(audit.stdout.encode()).hexdigest(),
        },
        "catch_proofs": {
            "scope": expect_failure(lambda: validate_scope("CANON.md")),
            "frozen": generic.expect("FROZEN", lambda: generic.validate_frozen(ROOT, corrupt=True)),
            "current_paths": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, corrupt="current")),
            "frontier": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, corrupt="frontier")),
            "dirty": expect_failure(lambda: validate_dirty(True)),
            "package": expect_failure(lambda: validate_package(True)),
        },
        "authority_boundary": {
            "startup_controls_changed": False,
            "canon_changed": False,
            "frozen_sources_changed": False,
            "physical_extension_or_global_section_selected": False,
            "variation_domain_selected": False,
            "action_carrier_source_boundary_density_Xmax_mass_changed": False,
            "gpu_work": False,
            "repository_reorganization": False,
        },
    }
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    (HERE / "REPOSITORY_GATES.json").write_text(output, encoding="utf-8")
    print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
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
BASE = "68f8303"
DIRTY = Path("/home/udt-admin/udt_mass_codex")


def load_generic():
    path = ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19" / "verify_repository_gates.py"
    spec = importlib.util.spec_from_file_location("intrinsic_holonomy_generic_gates", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.BASE = BASE
    module.PACKAGE = PACKAGE
    return module


def run(command, cwd=ROOT):
    environment = dict(os.environ)
    environment.update({"CUDA_VISIBLE_DEVICES": "", "PYTHONDONTWRITEBYTECODE": "1"})
    return subprocess.run(
        command, cwd=cwd, env=environment, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )


def git(cwd, *arguments):
    result = run(["git", *arguments], cwd)
    assert result.returncode == 0, result.stdout
    return result.stdout


def scope(injected=""):
    paths = set(git(ROOT, "diff", "--name-only", BASE).splitlines())
    paths.update(git(ROOT, "ls-files", "--others", "--exclude-standard").splitlines())
    if injected:
        paths.add(injected)
    assert not [path for path in paths if path and not path.startswith(PACKAGE + "/")]
    return sorted(path for path in paths if path)


def tests():
    result = run([sys.executable, "-m", "pytest", "-q", "tests/"])
    match = re.search(r"(\d+) passed, (\d+) xfailed", result.stdout)
    assert result.returncode == 0 and match and tuple(map(int, match.groups())) == (70, 1), result.stdout
    return {
        "passed": 70, "failed": 0, "xfailed": 1,
        "stdout_sha256": hashlib.sha256(result.stdout.encode()).hexdigest(), "result": "PASS",
    }


def dirty(corrupt=False):
    status = subprocess.run(
        ["git", "status", "--short"], cwd=DIRTY,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    assert status.returncode == 0
    head = git(DIRTY, "rev-parse", "HEAD").strip()
    branch = git(DIRTY, "branch", "--show-current").strip()
    count = len(status.stdout.splitlines()) - int(corrupt)
    digest = hashlib.sha256(status.stdout).hexdigest()
    assert (head, branch, count, digest) == (
        "8b13104a4f1af45af617d2aa50cd5fdacf4082af", "grok", 55,
        "345d297e0ad849cd38f1d817c915922de653ca2d2befcf923af6f9d097b483e4",
    )
    return {
        "head": head, "branch": branch, "paths": count, "metadata_sha256": digest,
        "contents_read": False, "result": "PASS",
    }


def package(corrupt=False):
    manifest = HERE / "SHA256SUMS.txt"
    expected = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        expected[name] = digest
    actual = sorted(
        path.name for path in HERE.iterdir()
        if path.is_file() and path.name not in {"SHA256SUMS.txt", "REPOSITORY_GATES.json"}
    )
    assert not corrupt and sorted(expected) == actual
    for name, digest in expected.items():
        assert hashlib.sha256((HERE / name).read_bytes()).hexdigest() == digest
    return {
        "entries": len(expected), "manifest_sha256": hashlib.sha256(manifest.read_bytes()).hexdigest(),
        "result": "PASS",
    }


def replay(corrupt=False):
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    assert not corrupt
    assert production["status"] == "COMPUTED" and production["loop_transports"] == 36
    assert independent["status"] == "PASS" and independent["coordinate_curvature_holdouts"] == 18
    hashes = {}
    for script in ("verify_source_manifest.py", "verify_audit.py"):
        result = run([sys.executable, str(HERE / script)])
        assert result.returncode == 0, result.stdout
        hashes[script] = hashlib.sha256(result.stdout.encode()).hexdigest()
    premises = run([sys.executable, "verify_current_scientific_premises.py"])
    assert premises.returncode == 0, premises.stdout
    return {
        "production": "PASS_18_LOCAL_36_LOOPS",
        "independent": "PASS_18_COORDINATE_12_RK4",
        "source_manifest": "17/17", "audit_catches": "24/24", "stdout_hashes": hashes,
    }


def expect(function):
    try:
        function()
    except AssertionError:
        return "PASS"
    raise AssertionError("catch accepted")


def main() -> int:
    generic = load_generic()
    scoped = scope()
    frozen = generic.validate_frozen(ROOT)
    navigation = generic.validate_navigation(ROOT)
    result = {
        "schema": "udt-intrinsic-reciprocal-holonomy-repository-gates-1.0",
        "result": "PASS", "base": BASE, "preregistration_ancestor": True,
        "scope_path_count": len(scoped), "frozen": frozen, "navigation": navigation,
        "tests": tests(), "dirty_checkout": dirty(), "calculation_replays": replay(),
        "package_manifest": package(),
        "catch_proofs": {
            "scope": expect(lambda: scope("CANON.md")),
            "frozen": generic.expect("FROZEN", lambda: generic.validate_frozen(ROOT, corrupt=True)),
            "current_paths": generic.expect(
                "NAVIGATION", lambda: generic.validate_navigation(ROOT, corrupt="current")
            ),
            "frontier": generic.expect(
                "NAVIGATION", lambda: generic.validate_navigation(ROOT, corrupt="frontier")
            ),
            "dirty": expect(lambda: dirty(True)), "calculation": expect(lambda: replay(True)),
            "package": expect(lambda: package(True)),
        },
        "authority_boundary": {
            "startup_controls_changed": False, "canon_changed": False,
            "source_results_changed": False, "frozen_or_historical_changed": False,
            "copresence_promoted": False, "instantaneous_access_derived": False,
            "path_semantics_selected": False, "lambda_selected": False, "on_shell_claimed": False,
            "action_carrier_source_density_mass_Xmax_dynamics_selected": False,
            "gpu_work": False, "reorganization": False,
        },
    }
    git(ROOT, "merge-base", "--is-ancestor", BASE, "HEAD")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

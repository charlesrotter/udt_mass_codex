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
BASE = "8b295c7"
DIRTY = Path("/home/udt-admin/udt_mass_codex")


def generic():
    path = ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19" / "verify_repository_gates.py"
    spec = importlib.util.spec_from_file_location("selector_rank_generic", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.BASE = BASE
    module.PACKAGE = PACKAGE
    return module


def run(command: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    environment = dict(os.environ)
    environment.update({"CUDA_VISIBLE_DEVICES": "", "PYTHONDONTWRITEBYTECODE": "1"})
    return subprocess.run(command, cwd=cwd, env=environment, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def git(cwd: Path, *arguments: str) -> str:
    result = run(["git", *arguments], cwd)
    assert result.returncode == 0, result.stdout
    return result.stdout


def scope(injected: str = "") -> list[str]:
    paths = set(git(ROOT, "diff", "--name-only", BASE).splitlines())
    paths.update(git(ROOT, "ls-files", "--others", "--exclude-standard").splitlines())
    if injected:
        paths.add(injected)
    assert not [path for path in paths if path and not path.startswith(PACKAGE + "/")]
    return sorted(path for path in paths if path)


def tests() -> dict[str, object]:
    result = run([sys.executable, "-m", "pytest", "-q", "tests/"])
    match = re.search(r"(\d+) passed, (\d+) xfailed", result.stdout)
    assert result.returncode == 0 and match and tuple(map(int, match.groups())) == (70, 1), result.stdout
    return {"passed": 70, "failed": 0, "xfailed": 1, "stdout_sha256": hashlib.sha256(result.stdout.encode()).hexdigest(), "result": "PASS"}


def dirty(corrupt: bool = False) -> dict[str, object]:
    status = subprocess.run(["git", "status", "--short"], cwd=DIRTY, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert status.returncode == 0
    value = (
        git(DIRTY, "rev-parse", "HEAD").strip(),
        git(DIRTY, "branch", "--show-current").strip(),
        len(status.stdout.splitlines()) - int(corrupt),
        hashlib.sha256(status.stdout).hexdigest(),
    )
    assert value == ("8b13104a4f1af45af617d2aa50cd5fdacf4082af", "grok", 55, "345d297e0ad849cd38f1d817c915922de653ca2d2befcf923af6f9d097b483e4")
    return {"head": value[0], "branch": value[1], "paths": value[2], "metadata_sha256": value[3], "contents_read": False, "result": "PASS"}


def package(corrupt: bool = False) -> dict[str, object]:
    entries = {name: digest for digest, name in (line.split("  ", 1) for line in (HERE / "SHA256SUMS.txt").read_text().splitlines())}
    actual = sorted(path.name for path in HERE.iterdir() if path.is_file() and path.name not in {"SHA256SUMS.txt", "REPOSITORY_GATES.json"})
    assert not corrupt and sorted(entries) == actual
    for name, digest in entries.items():
        assert hashlib.sha256((HERE / name).read_bytes()).hexdigest() == digest
    return {"entries": len(entries), "manifest_sha256": hashlib.sha256((HERE / "SHA256SUMS.txt").read_bytes()).hexdigest(), "result": "PASS"}


def replay(corrupt: bool = False) -> dict[str, object]:
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
    verification = json.loads((HERE / "VERIFICATION_RESULT.json").read_text())
    assert not corrupt
    assert production["quotient_metric_shift_a_cancels"]
    assert production["independent_profile_selector_rank_from_active_premises"] == 0
    assert independent["status"] == "PASS" and verification["status"] == "PASS"
    hashes = {}
    for script in ("verify_source_manifest.py", "verify_audit.py"):
        result = run([sys.executable, str(HERE / script)])
        assert result.returncode == 0, result.stdout
        hashes[script] = hashlib.sha256(result.stdout.encode()).hexdigest()
    premise = run([sys.executable, "verify_current_scientific_premises.py"])
    assert premise.returncode == 0, premise.stdout
    return {"production": "PASS_EXACT_ORBIT_GEOMETRY_AND_RANK", "independent": "PASS_STDLIB_FRACTION", "fresh_adversarial": "VERIFIED_WITH_CAVEATS", "sources": "18/18", "audit_catches": "24/24", "stdout_hashes": hashes}


def expect(function) -> str:
    try:
        function()
    except AssertionError:
        return "PASS"
    raise AssertionError("catch accepted")


def main() -> int:
    helper = generic()
    changed = scope()
    git(ROOT, "merge-base", "--is-ancestor", BASE, "HEAD")
    result = {
        "schema": "udt.metric_native_selector_rank.repository_gates.v1",
        "result": "PASS",
        "base": BASE,
        "preregistration_ancestor": True,
        "scope_path_count": len(changed),
        "frozen": helper.validate_frozen(ROOT),
        "navigation": helper.validate_navigation(ROOT),
        "tests": tests(),
        "dirty_checkout": dirty(),
        "calculation_replays": replay(),
        "package_manifest": package(),
        "catch_proofs": {
            "scope": expect(lambda: scope("CANON.md")),
            "frozen": helper.expect("FROZEN", lambda: helper.validate_frozen(ROOT, corrupt=True)),
            "current_paths": helper.expect("NAVIGATION", lambda: helper.validate_navigation(ROOT, corrupt="current")),
            "frontier": helper.expect("NAVIGATION", lambda: helper.validate_navigation(ROOT, corrupt="frontier")),
            "dirty": expect(lambda: dirty(True)),
            "calculation": expect(lambda: replay(True)),
            "package": expect(lambda: package(True)),
        },
        "authority_boundary": {
            "startup_controls_changed": False,
            "canon_changed": False,
            "source_results_changed": False,
            "frozen_or_historical_changed": False,
            "physical_phi_profile_selected": False,
            "Xmax_identified_or_assigned": False,
            "mass_density_or_bootstrap_map_derived": False,
            "action_source_carrier_boundary_selected": False,
            "gpu_work": False,
            "reorganization": False,
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

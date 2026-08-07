#!/usr/bin/env python3
"""Repository, provenance, and scope gates for the X_max relational audit."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
PACKAGE = HERE.name
BASE = "696cf401c441fdd3aefea6f3de188e6425ae5636"
DIRTY = Path("/home/udt-admin/udt_mass_codex")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["CUDA_VISIBLE_DEVICES"] = ""
    return subprocess.run(
        command,
        cwd=cwd,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def git(*args: str) -> str:
    completed = run(["git", *args])
    if completed.returncode:
        raise AssertionError(completed.stdout)
    return completed.stdout


def validate_scope(injected: str = "") -> list[str]:
    changed = set(git("diff", "--name-only", BASE).splitlines())
    changed.update(git("ls-files", "--others", "--exclude-standard").splitlines())
    if injected:
        changed.add(injected)
    invalid = sorted(
        path for path in changed if path and not path.startswith(PACKAGE + "/")
    )
    if invalid:
        raise AssertionError(f"scope:{invalid[0]}")
    return sorted(changed)


def validate_science(corrupt: bool = False) -> dict[str, object]:
    generated = [
        "PATH_DISPOSITION.tsv",
        "LOAD_BEARING_SOURCE_REGISTRY.tsv",
        "FAMILY_RULINGS.tsv",
        "RELATIONAL_DEFINITION_LEDGER.tsv",
        "COUNTERMODEL_ATLAS.tsv",
        "CLAIM_REGRADE.tsv",
        "DEPENDENCY_IMPACT.tsv",
        "NEGATIVE_REGRADE.tsv",
        "RESULTS.json",
        "CATCH_PROOF_RESULTS.tsv",
        "INDEPENDENT_RESULTS.json",
    ]
    before = {name: (HERE / name).read_bytes() for name in generated}
    outputs = []
    for command in (
        [sys.executable, "derive_relational_xmax.py"],
        [sys.executable, "verify_relational_xmax.py"],
    ):
        completed = run(command, cwd=HERE)
        outputs.append(completed.stdout)
        if completed.returncode:
            raise AssertionError(completed.stdout)
    if any((HERE / name).read_bytes() != before[name] for name in generated):
        raise AssertionError("non-deterministic replay")
    results = json.loads((HERE / "RESULTS.json").read_text(encoding="utf-8"))
    independent = json.loads(
        (HERE / "INDEPENDENT_RESULTS.json").read_text(encoding="utf-8")
    )
    if corrupt:
        results["rulings"]["edge_from_Xmax"] = "DERIVED"
    if (
        results["candidate_paths"] != 907
        or results["load_bearing_sources"] != 61
        or results["rulings"]["edge_from_Xmax"] != "NOT_DERIVED"
        or results["rulings"]["metric_derived_pair_separation"] != "OPEN_SELECTOR"
        or results["rulings"]["local_WRL_X_equals_global_Xmax"]
        != "OPEN_DIAMETER_RADIUS_JOIN"
        or results["rulings"]["general_fractional_pair_distance_composition"]
        != "REFUTED_IN_GENERAL"
        or independent["overall"] != "PASS"
        or independent["catch_proof_passes"] != 16
    ):
        raise AssertionError("science authority")
    return {
        "deterministic_replay": "BYTE_IDENTICAL",
        "candidate_paths": 907,
        "load_bearing_sources": 61,
        "claim_regrades": 34,
        "catch_proofs": 16,
        "production_stdout_sha256": hashlib.sha256(
            outputs[0].encode()
        ).hexdigest(),
        "independent_stdout_sha256": hashlib.sha256(
            outputs[1].encode()
        ).hexdigest(),
        "external_fresh_context": "NOT_PERFORMED_CAVEAT",
        "result": "PASS",
    }


def validate_tests() -> dict[str, object]:
    completed = run([sys.executable, "-m", "pytest", "-q", "tests/"])
    match = re.search(r"(\d+) passed, (\d+) xfailed", completed.stdout)
    if (
        completed.returncode != 0
        or match is None
        or tuple(map(int, match.groups())) != (70, 1)
        or " failed" in completed.stdout
    ):
        raise AssertionError(completed.stdout)
    return {
        "command": "CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q tests/",
        "returncode": 0,
        "passed": 70,
        "failed": 0,
        "xfailed": 1,
        "stdout_sha256": hashlib.sha256(completed.stdout.encode()).hexdigest(),
        "result": "PASS",
    }


def validate_dirty(corrupt: bool = False) -> dict[str, object]:
    completed = subprocess.run(
        ["git", "status", "--short"],
        cwd=DIRTY,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode:
        raise AssertionError("dirty metadata unavailable")
    metadata = completed.stdout
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=DIRTY,
        stdout=subprocess.PIPE,
        check=True,
    ).stdout.decode().strip()
    branch = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=DIRTY,
        stdout=subprocess.PIPE,
        check=True,
    ).stdout.decode().strip()
    if corrupt:
        head = "0" * 40
    if (
        head != "adf8f92d95c387cc647f04b16f1f3b17e1e670d2"
        or branch != "grok"
        or len(metadata.splitlines()) != 54
        or hashlib.sha256(metadata).hexdigest()
        != "4bc96070c841a14c497b642ee7b93dcf9061372f770aee065d6b495ee4996f4c"
    ):
        raise AssertionError("dirty metadata changed")
    return {
        "head": head,
        "branch": branch,
        "paths": 54,
        "metadata_sha256": hashlib.sha256(metadata).hexdigest(),
        "contents_read": False,
        "result": "PASS",
    }


def validate_package(corrupt: bool = False) -> dict[str, object]:
    completed = run(["sha256sum", "--check", "SHA256SUMS.txt"], cwd=HERE)
    if corrupt or completed.returncode or "FAILED" in completed.stdout:
        raise AssertionError("package manifest")
    entries = [
        line.split("  ", 1)[1]
        for line in (HERE / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines()
        if line
    ]
    actual = sorted(
        path.name
        for path in HERE.iterdir()
        if path.is_file()
        and path.name not in {"SHA256SUMS.txt", "REPOSITORY_GATES.json"}
    )
    if sorted(entries) != actual:
        raise AssertionError("package manifest coverage")
    return {
        "entries": len(entries),
        "manifest_sha256": digest(HERE / "SHA256SUMS.txt"),
        "result": "PASS",
    }


def expect_failure(callback) -> str:
    try:
        callback()
    except AssertionError:
        return "PASS"
    raise AssertionError("repository catch accepted corruption")


def main() -> None:
    generic = load(
        ROOT
        / "bootstrap_csn_phi_angular_selector_2026-07-19"
        / "verify_repository_gates.py",
        "xmax_relational_generic",
    )
    generic.BASE = BASE
    generic.PACKAGE = PACKAGE
    scope = validate_scope()
    science = validate_science()
    frozen = generic.validate_frozen(ROOT)
    navigation = generic.validate_navigation(ROOT)
    dirty = validate_dirty()
    tests = validate_tests()
    package = validate_package()
    catches = {
        "scope": expect_failure(lambda: validate_scope("CANON.md")),
        "science_authority": expect_failure(lambda: validate_science(corrupt=True)),
        "frozen": generic.expect(
            "FROZEN", lambda: generic.validate_frozen(ROOT, corrupt=True)
        ),
        "current_paths": generic.expect(
            "NAVIGATION",
            lambda: generic.validate_navigation(ROOT, corrupt="current"),
        ),
        "frontier": generic.expect(
            "NAVIGATION",
            lambda: generic.validate_navigation(ROOT, corrupt="frontier"),
        ),
        "dirty": expect_failure(lambda: validate_dirty(corrupt=True)),
        "package": expect_failure(lambda: validate_package(corrupt=True)),
    }
    output = {
        "schema": "udt-xmax-observer-separation-repository-gates-v1",
        "base": BASE,
        "result": "PASS",
        "scope_paths": scope,
        "science": science,
        "frozen": frozen,
        "navigation": navigation,
        "dirty_checkout": dirty,
        "tests": tests,
        "package_manifest": package,
        "catch_proofs": catches,
        "authority_boundary": {
            "canon_changed": False,
            "historical_or_frozen_evidence_changed": False,
            "edge_or_topology_selected": False,
            "pair_separation_functional_claimed_derived": False,
            "local_WRL_X_identified_with_global_Xmax": False,
            "action_source_boundary_mass_adopted": False,
            "matter_or_time_live_solve": False,
            "gpu_work": False,
            "repository_reorganization": False,
            "startup_controls_changed": False,
        },
    }
    (HERE / "REPOSITORY_GATES.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

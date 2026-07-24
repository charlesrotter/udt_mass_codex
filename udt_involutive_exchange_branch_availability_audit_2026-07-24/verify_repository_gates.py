#!/usr/bin/env python3
"""Repository and authority gates for the branch-availability audit."""

from __future__ import annotations

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
BASE = "6e58a24ba41d7bf53ab89c7f963ba85c06275b48"
DIRTY = Path("/home/udt-admin/udt_mass_codex")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def run(command: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["CUDA_VISIBLE_DEVICES"] = ""
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
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
    paths = set(git("diff", "--name-only", BASE).splitlines())
    paths.update(git("ls-files", "--others", "--exclude-standard").splitlines())
    if injected:
        paths.add(injected)
    bad = sorted(path for path in paths if path and not path.startswith(PACKAGE + "/"))
    if bad:
        raise AssertionError(f"scope:{bad[0]}")
    return sorted(path for path in paths if path)


def validate_science(corrupt: str = "") -> dict[str, object]:
    generated = [
        "FAMILY_GATE_COUNTS.tsv",
        "STATUS_LEDGER.tsv",
        "RESULTS.json",
        "CATCH_PROOF_RESULTS.tsv",
        "INDEPENDENT_RESULTS.json",
    ]
    before = {name: (HERE / name).read_bytes() for name in generated}
    outputs = []
    for command in (
        [sys.executable, "derive_branch_availability.py"],
        [sys.executable, "verify_branch_availability_independent.py"],
    ):
        completed = run(command, cwd=HERE)
        outputs.append(completed.stdout)
        if completed.returncode:
            raise AssertionError(completed.stdout)
    if any((HERE / name).read_bytes() != before[name] for name in generated):
        raise AssertionError("science replay not byte-identical")

    result = json.loads((HERE / "RESULTS.json").read_text(encoding="utf-8"))
    independent = json.loads(
        (HERE / "INDEPENDENT_RESULTS.json").read_text(encoding="utf-8")
    )
    if corrupt == "pass":
        result["passing_families"] = ["B19"]
    elif corrupt == "lift":
        result["authority_boundary"]["lift_selected"] = True
    elif corrupt == "source":
        result["sources"] = 149
    if (
        result["result"] != "PASS"
        or result["families"] != 28
        or result["sources"] != 150
        or result["passing_families"]
        or result["native_action_gate_yes"] != 0
        or result["native_complete_on_shell_gate_yes"] != 0
        or result["strongest_near_pass"]["family_id"] != "B19"
        or result["catch_proofs"] != 12
        or any(result["authority_boundary"].values())
    ):
        raise AssertionError("production science")
    if (
        independent["result"] != "PASS"
        or independent["imports_production_module"] is not False
        or independent["imports_sympy"] is not False
        or independent["families"] != 28
        or independent["sources"] != 150
        or independent["passing_families"]
        or independent["strongest_near_pass"] != "B19"
        or independent["catch_proofs"] != 12
        or not all(independent["agreement"].values())
    ):
        raise AssertionError("independent science")
    return {
        "deterministic_replay": "BYTE_IDENTICAL",
        "families": 28,
        "sources": 150,
        "intersection_paths": 206,
        "report_level_paths": 14,
        "passing_families": 0,
        "strongest_near_pass": "B19",
        "catch_proofs": 12,
        "production_stdout_sha256": hashlib.sha256(
            outputs[0].encode("utf-8")
        ).hexdigest(),
        "independent_stdout_sha256": hashlib.sha256(
            outputs[1].encode("utf-8")
        ).hexdigest(),
        "fresh_external_semantic_review": "NOT_PERFORMED_CAVEAT",
        "result": "PASS",
    }


def validate_dirty(corrupt: bool = False) -> dict[str, object]:
    status = subprocess.run(
        ["git", "status", "--short"],
        cwd=DIRTY,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if status.returncode:
        raise AssertionError("dirty metadata unavailable")
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
        branch = "main"
    metadata_sha = hashlib.sha256(status.stdout).hexdigest()
    if (
        head != "adf8f92d95c387cc647f04b16f1f3b17e1e670d2"
        or branch != "grok"
        or len(status.stdout.splitlines()) != 54
        or metadata_sha
        != "4bc96070c841a14c497b642ee7b93dcf9061372f770aee065d6b495ee4996f4c"
    ):
        raise AssertionError("dirty checkout metadata changed")
    return {
        "head": head,
        "branch": branch,
        "paths": len(status.stdout.splitlines()),
        "metadata_sha256": metadata_sha,
        "contents_read": False,
        "result": "PASS",
    }


def validate_tests() -> dict[str, object]:
    completed = run([sys.executable, "-m", "pytest", "-q", "tests/"])
    match = re.search(r"(\d+) passed, (\d+) xfailed", completed.stdout)
    if (
        completed.returncode
        or match is None
        or tuple(map(int, match.groups())) != (70, 1)
        or " failed" in completed.stdout
    ):
        raise AssertionError(completed.stdout)
    return {
        "command": "CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q tests/",
        "passed": 70,
        "failed": 0,
        "xfailed": 1,
        "stdout_sha256": hashlib.sha256(completed.stdout.encode()).hexdigest(),
        "result": "PASS",
    }


def validate_package(corrupt: bool = False) -> dict[str, object]:
    completed = run(["sha256sum", "--check", "SHA256SUMS.txt"], cwd=HERE)
    if corrupt or completed.returncode or "FAILED" in completed.stdout:
        raise AssertionError("package manifest")
    entries = [
        line.split("  ", 1)[1]
        for line in (HERE / "SHA256SUMS.txt").read_text().splitlines()
        if line
    ]
    actual = sorted(
        path.name
        for path in HERE.iterdir()
        if path.is_file()
        and path.name not in {"SHA256SUMS.txt", "REPOSITORY_GATES.json"}
    )
    if sorted(entries) != actual:
        raise AssertionError("package coverage")
    return {
        "entries": len(entries),
        "manifest_sha256": hashlib.sha256(
            (HERE / "SHA256SUMS.txt").read_bytes()
        ).hexdigest(),
        "result": "PASS",
    }


def expect_failure(callback) -> str:
    try:
        callback()
    except AssertionError:
        return "PASS"
    raise AssertionError("catch accepted corruption")


def main() -> None:
    generic = load(
        ROOT
        / "bootstrap_csn_phi_angular_selector_2026-07-19"
        / "verify_repository_gates.py",
        "branch_availability_generic",
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
        "science_pass": expect_failure(lambda: validate_science("pass")),
        "science_lift": expect_failure(lambda: validate_science("lift")),
        "science_source": expect_failure(lambda: validate_science("source")),
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
        "dirty": expect_failure(lambda: validate_dirty(True)),
        "package": expect_failure(lambda: validate_package(True)),
    }
    output = {
        "schema": "udt-involutive-exchange-branch-repository-gates-v1",
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
            "startup_controls_changed": False,
            "canon_changed": False,
            "historical_or_frozen_changed": False,
            "action_selected": False,
            "lift_selected": False,
            "completion_selected": False,
            "carrier_or_source_selected": False,
            "density_or_mass_solve": False,
            "gpu_work": False,
            "repository_reorganization": False,
        },
    }
    (HERE / "REPOSITORY_GATES.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

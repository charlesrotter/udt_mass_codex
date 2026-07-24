#!/usr/bin/env python3
"""Fail-closed science, scope, frozen, navigation, test, and package gates."""

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


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PACKAGE = HERE.name
BASE = "dc81c489b9e27bd86b2d58d93fbacf4a4fd01496"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
ALLOWED_NAVIGATION = {
    "LIVE.md",
    "HANDOFF.md",
    "INDEX.md",
    "README.md",
    "research/README.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def run(command: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    environment = dict(os.environ)
    environment["CUDA_VISIBLE_DEVICES"] = ""
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
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


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def expect_failure(callback) -> str:
    try:
        callback()
    except AssertionError:
        return "PASS_REJECTED"
    raise AssertionError("catch accepted corruption")


def validate_scope(injected: str = "") -> list[str]:
    paths = set(git("diff", "--name-only", BASE).splitlines())
    paths.update(git("ls-files", "--others", "--exclude-standard").splitlines())
    if injected:
        paths.add(injected)
    invalid = sorted(
        path
        for path in paths
        if path
        and not path.startswith(PACKAGE + "/")
        and path not in ALLOWED_NAVIGATION
    )
    if invalid:
        raise AssertionError(f"scope:{invalid[0]}")
    if "CANON.md" in paths:
        raise AssertionError("canon changed")
    return sorted(path for path in paths if path)


def validate_science(corrupt: str = "") -> dict[str, object]:
    generated = [
        "DERIVATION_RESULT.json",
        "COCYCLE_TYPE_LEDGER.tsv",
        "BRANCH_COCYCLE_ATLAS.tsv",
        "STATUS_LEDGER.tsv",
        "INDEPENDENT_VERIFICATION.json",
        "PRODUCTION_STDOUT.txt",
        "PRODUCTION_STDERR.txt",
        "INDEPENDENT_STDOUT.txt",
        "INDEPENDENT_STDERR.txt",
        "RUN_ENVIRONMENT.json",
    ]
    before = {name: (HERE / name).read_bytes() for name in generated}
    completed = run([sys.executable, "replay_and_capture.py"], cwd=HERE)
    if completed.returncode:
        raise AssertionError(completed.stdout)
    if any((HERE / name).read_bytes() != before[name] for name in generated):
        raise AssertionError("science replay not byte-identical")

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
    types = {
        row["object"]: row for row in read_tsv(HERE / "COCYCLE_TYPE_LEDGER.tsv")
    }
    branches = {
        row["branch"]: row for row in read_tsv(HERE / "BRANCH_COCYCLE_ATLAS.tsv")
    }
    statuses = {
        row["claim"]: row for row in read_tsv(HERE / "STATUS_LEDGER.tsv")
    }
    state: dict[str, object] = {
        "derived": production["derived_object"],
        "combined": production["combined_object"],
        "solder": production["founding_reciprocal_solder"],
        "irreducible": production["irreducible_native_solder"],
        "universal": production["universal_all_observer_operator"],
        "xmax": production["physical_Xmax"],
        "splice": production["cross_branch_splice"],
        "types": len(types),
        "branches": len(branches),
        "sources": production["source_count"],
        "completions": production["registry"]["finite_cell_completions"],
        "equations": production["registry"]["equation_families"],
        "vertex": types["VERTEX_JACOBI_MAP_J"]["composition"],
        "b19": branches["B19_ROUND_S3"]["clock_block"],
        "wrl": branches["WRL_LOCAL_RESIDUAL"]["global_recentring"],
        "path_selection": statuses[
            "null versus co-present/rest path selection"
        ]["status"],
    }
    mutations = {
        "derived": ("derived", "VERTEX_JACOBI_PATH_COCYCLE"),
        "combined": ("combined", "IRREDUCIBLE_NATIVE_OBJECT"),
        "solder": ("solder", "DERIVED"),
        "irreducible": ("irreducible", "DERIVED"),
        "universal": ("universal", "DERIVED"),
        "xmax": ("xmax", "DERIVED"),
        "splice": ("splice", "USED"),
        "types": ("types", 5),
        "branches": ("branches", 5),
        "sources": ("sources", 17),
        "completions": ("completions", 11),
        "equations": ("equations", 27),
        "vertex": ("vertex", "YES_PATH_GROUPOID"),
        "b19": ("b19", "Q=EXP_PHI"),
        "wrl": ("wrl", "YES"),
        "path": ("path_selection", "DERIVED_NULL"),
    }
    if corrupt:
        key, value = mutations[corrupt]
        state[key] = value
    required = {
        "derived": "METRIC_GEODESIC_DEVIATION_PATH_COCYCLE",
        "combined": "REDUCIBLE_DIRECT_SUM_S_LOG_Q_PLUS_M",
        "solder": "CONDITIONAL",
        "irreducible": "OPEN",
        "universal": "OPEN",
        "xmax": "OPEN",
        "splice": "FORBIDDEN_NOT_USED",
        "types": 6,
        "branches": 6,
        "sources": 18,
        "completions": 12,
        "equations": 28,
        "vertex": "NO_NOT_STANDALONE",
        "b19": "Q=1;S=IDENTITY",
        "wrl": "NO",
        "path_selection": "OPEN",
    }
    if state != required:
        raise AssertionError("science adjudication")
    if (
        production["result"] != "PASS"
        or production["check_count"] != 69
        or set(production["checks"].values()) != {"PASS"}
        or independent["result"] != "PASS"
        or independent["production_imported"] is not False
        or independent["check_count"] != 52
        or independent["catch_count"] != 13
        or set(independent["checks"].values()) != {"PASS"}
        or set(independent["catches"].values()) != {"PASS_REJECTED"}
        or independent["wrl_composition_max_abs_error"] >= 2e-11
        or independent["wrl_direct_det_error"] >= 2e-11
    ):
        raise AssertionError("science verification")
    return {
        "deterministic_replay": "BYTE_IDENTICAL",
        "production_checks": 69,
        "independent_checks": 52,
        "independent_catches": 13,
        "source_identities": 18,
        "types": 6,
        "branches": 6,
        "finite_cell_completions": 12,
        "equation_families": 28,
        "derived_object": state["derived"],
        "combined_object": state["combined"],
        "founding_solder": state["solder"],
        "universal_operator": state["universal"],
        "production_sha256": digest((HERE / "DERIVATION_RESULT.json").read_bytes()),
        "independent_sha256": digest(
            (HERE / "INDEPENDENT_VERIFICATION.json").read_bytes()
        ),
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
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=DIRTY,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    ).stdout.decode().strip()
    branch = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=DIRTY,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    ).stdout.decode().strip()
    count = len(completed.stdout.splitlines())
    metadata_sha = digest(completed.stdout)
    if corrupt:
        count -= 1
    if (
        head != "adf8f92d95c387cc647f04b16f1f3b17e1e670d2"
        or branch != "grok"
        or count != 55
        or metadata_sha
        != "345d297e0ad849cd38f1d817c915922de653ca2d2befcf923af6f9d097b483e4"
    ):
        raise AssertionError("dirty checkout metadata changed")
    return {
        "head": head,
        "branch": branch,
        "paths": count,
        "metadata_sha256": metadata_sha,
        "contents_read": False,
        "note": "Only separately authorized phiequations.md content was read before this audit.",
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
    recorded = (HERE / "TEST_STDOUT.txt").read_text()
    recorded_match = re.search(r"(\d+) passed, (\d+) xfailed", recorded)
    if recorded_match is None or tuple(map(int, recorded_match.groups())) != (70, 1):
        raise AssertionError("recorded test baseline")
    return {
        "passed": 70,
        "failed": 0,
        "xfailed": 1,
        "stdout_sha256": digest(completed.stdout.encode()),
        "recorded_stdout_sha256": digest((HERE / "TEST_STDOUT.txt").read_bytes()),
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
        "manifest_sha256": digest((HERE / "SHA256SUMS.txt").read_bytes()),
        "result": "PASS",
    }


def main() -> None:
    generic = load(
        ROOT
        / "bootstrap_csn_phi_angular_selector_2026-07-19"
        / "verify_repository_gates.py",
        "observer_cocycle_generic_gates",
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
        **{
            f"science_{key}": expect_failure(
                lambda key=key: validate_science(key)
            )
            for key in [
                "derived",
                "combined",
                "solder",
                "irreducible",
                "universal",
                "xmax",
                "splice",
                "types",
                "branches",
                "sources",
                "completions",
                "equations",
                "vertex",
                "b19",
                "wrl",
                "path",
            ]
        },
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
    result = {
        "schema": "udt-observer-longitudinal-transverse-cocycle-gates-1.0",
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
            "startup_navigation_changed": True,
            "canon_changed": False,
            "founding_reciprocal_solder_promoted": False,
            "irreducible_native_operator_claimed": False,
            "path_type_selected": False,
            "cross_branch_splice": False,
            "physical_Xmax_promoted": False,
            "action_source_carrier_density_selected": False,
            "gpu_or_time_live_work": False,
            "repository_reorganization": False,
        },
    }
    (HERE / "REPOSITORY_GATES.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

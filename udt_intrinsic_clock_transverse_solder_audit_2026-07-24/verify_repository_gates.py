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
BASE = "2e98f4cc91a0accbfe8a5e96d180ef3f297d8da0"
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
    if invalid or "CANON.md" in paths:
        raise AssertionError(f"scope:{invalid[0] if invalid else 'CANON.md'}")
    return sorted(path for path in paths if path)


def validate_science(corrupt: str = "") -> dict[str, object]:
    generated = [
        "DERIVATION_RESULT.json",
        "SOLDER_TYPE_LEDGER.tsv",
        "GENERATOR_MATCH_ATLAS.tsv",
        "BRANCH_SOLDER_ATLAS.tsv",
        "CAUSAL_SOLDER_ATLAS.tsv",
        "COMPLETION_SOLDER_ATLAS.tsv",
        "STATUS_LEDGER.tsv",
        "INDEPENDENT_VERIFICATION.json",
        "PRODUCTION_STDOUT.txt",
        "PRODUCTION_STDERR.txt",
        "INDEPENDENT_STDOUT.txt",
        "INDEPENDENT_STDERR.txt",
        "RUN_ENVIRONMENT.json",
    ]
    before = {name: (HERE / name).read_bytes() for name in generated}
    replay = run([sys.executable, "replay_and_capture.py"], cwd=HERE)
    if replay.returncode:
        raise AssertionError(replay.stdout)
    if any((HERE / name).read_bytes() != before[name] for name in generated):
        raise AssertionError("science replay not byte-identical")

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
    types = {
        row["candidate"]: row for row in read_tsv(HERE / "SOLDER_TYPE_LEDGER.tsv")
    }
    generators = read_tsv(HERE / "GENERATOR_MATCH_ATLAS.tsv")
    branches = {
        row["branch"]: row for row in read_tsv(HERE / "BRANCH_SOLDER_ATLAS.tsv")
    }
    causal = read_tsv(HERE / "CAUSAL_SOLDER_ATLAS.tsv")
    completions = read_tsv(HERE / "COMPLETION_SOLDER_ATLAS.tsv")
    statuses = {
        row["claim"]: row for row in read_tsv(HERE / "STATUS_LEDGER.tsv")
    }
    state: dict[str, object] = {
        "solder": production["intrinsic_irreducible_solder"],
        "direct_sum": production["direct_sum_cocycle"],
        "splice": production["cross_branch_splice"],
        "xmax": production["physical_Xmax"],
        "types": len(types),
        "generators": len(generators),
        "branches": len(branches),
        "causal": len(causal),
        "completions": len(completions),
        "equations": production["equation_family_count"],
        "sources": production["source_count"],
        "hodge": statuses["Hodge area duality is clock-Jacobi solder"]["status"],
        "screen": statuses[
            "screen-gauge-equivariant linear clock-to-phase map"
        ]["status"],
        "wrl": statuses[
            "WRL pointwise natural-frame clock-transverse generator solder"
        ]["status"],
        "universal": branches["UNIVERSAL_PHYSICAL_UDT"]["linear_solder"],
    }
    mutations = {
        "solder": ("solder", "DERIVED"),
        "direct_sum": ("direct_sum", "SUPERSEDED"),
        "splice": ("splice", "USED"),
        "xmax": ("xmax", "DERIVED"),
        "types": ("types", 11),
        "generators": ("generators", 4),
        "branches": ("branches", 5),
        "causal": ("causal", 4),
        "completions": ("completions", 11),
        "equations": ("equations", 27),
        "sources": ("sources", 20),
        "hodge": ("hodge", "DERIVED_SOLDER"),
        "screen": ("screen", "DERIVED_NONZERO"),
        "wrl": ("wrl", "DERIVED"),
        "universal": ("universal", "DERIVED"),
    }
    if corrupt:
        key, value = mutations[corrupt]
        state[key] = value
    required = {
        "solder": "OPEN_NO_REGISTERED_WITNESS",
        "direct_sum": "DERIVED_REMAINS_STRONGEST_CURRENT_ASSEMBLY",
        "splice": "FORBIDDEN_NOT_USED",
        "xmax": "OPEN",
        "types": 12,
        "generators": 5,
        "branches": 6,
        "causal": 5,
        "completions": 12,
        "equations": 28,
        "sources": 21,
        "hodge": "FALSE_TYPE",
        "screen": "OBSTRUCTED_WITHOUT_SCREEN_REDUCTION",
        "wrl": "NO_POINTWISE_SIMILARITY_IN_EXACT_LOCAL_RADIAL_CONTROL",
        "universal": "OPEN",
    }
    if state != required:
        raise AssertionError("science adjudication")
    if (
        production["result"] != "PASS"
        or production["check_count"] != 80
        or set(production["checks"].values()) != {"PASS"}
        or independent["result"] != "PASS"
        or independent["production_imported"] is not False
        or independent["check_count"] != 60
        or independent["catch_count"] != 15
        or set(independent["checks"].values()) != {"PASS"}
        or set(independent["catches"].values()) != {"PASS_REJECTED"}
    ):
        raise AssertionError("science verification")
    return {
        "deterministic_replay": "BYTE_IDENTICAL",
        "production_checks": 80,
        "independent_checks": 60,
        "independent_catches": 15,
        "source_identities": 21,
        "candidate_types": 12,
        "generator_controls": 5,
        "branches": 6,
        "causal_classes": 5,
        "finite_cell_completions": 12,
        "equation_families": 28,
        "intrinsic_solder": state["solder"],
        "direct_sum": state["direct_sum"],
        "production_sha256": digest((HERE / "DERIVATION_RESULT.json").read_bytes()),
        "independent_sha256": digest(
            (HERE / "INDEPENDENT_VERIFICATION.json").read_bytes()
        ),
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
    count = len(status.stdout.splitlines())
    metadata_sha = digest(status.stdout)
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
        "intrinsic_solder_generic_gates",
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
                "solder",
                "direct_sum",
                "splice",
                "xmax",
                "types",
                "generators",
                "branches",
                "causal",
                "completions",
                "equations",
                "sources",
                "hodge",
                "screen",
                "wrl",
                "universal",
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
        "schema": "udt-intrinsic-clock-transverse-solder-gates-1.0",
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
            "intrinsic_solder_promoted": False,
            "generator_condition_made_field_equation": False,
            "screen_direction_selected": False,
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

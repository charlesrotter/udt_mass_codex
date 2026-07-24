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
BASE = "c67c0c1bcd94af6364d93f21fd9dd3a2194f5d3b"
DIRTY = Path("/home/udt-admin/udt_mass_codex")


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


def validate_scope(injected: str = "") -> list[str]:
    paths = set(git("diff", "--name-only", BASE).splitlines())
    paths.update(git("ls-files", "--others", "--exclude-standard").splitlines())
    if injected:
        paths.add(injected)
    invalid = sorted(
        path for path in paths if path and not path.startswith(PACKAGE + "/")
    )
    if invalid:
        raise AssertionError(f"scope:{invalid[0]}")
    return sorted(path for path in paths if path)


def validate_science(corrupt: str = "") -> dict[str, object]:
    generated = [
        "DERIVATION_RESULT.json",
        "OPTICAL_TYPE_LEDGER.tsv",
        "BRANCH_OPTICAL_ATLAS.tsv",
        "EQUATION_FAMILY_OPTICAL_SCREEN.tsv",
        "COMPLETION_OPTICAL_ATLAS.tsv",
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

    production = json.loads(
        (HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8")
    )
    independent = json.loads(
        (HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8")
    )
    types = {
        row["candidate"]: row for row in read_tsv(HERE / "OPTICAL_TYPE_LEDGER.tsv")
    }
    branches = {
        row["branch"]: row for row in read_tsv(HERE / "BRANCH_OPTICAL_ATLAS.tsv")
    }
    equations = read_tsv(HERE / "EQUATION_FAMILY_OPTICAL_SCREEN.tsv")
    completions = read_tsv(HERE / "COMPLETION_OPTICAL_ATLAS.tsv")
    statuses = {
        row["claim"]: row for row in read_tsv(HERE / "STATUS_LEDGER.tsv")
    }

    state: dict[str, object] = {
        "object": production["derived_object"]["type"],
        "universal": production["universal_operator"],
        "xmax": production["physical_Xmax"],
        "round_clock": branches["B19_ROUND_S3"]["clock_ratio"],
        "wrl_global": branches["WRL_LOCAL_RESIDUAL"]["physical_ruling"],
        "null_rest": statuses["null equals rest-space optical law"]["status"],
        "SNe_scope": statuses["WRL SNe readout is global center-free"]["status"],
        "type_count": len(types),
        "branch_count": len(branches),
        "equation_count": len(equations),
        "completion_count": len(completions),
        "source_count": production["source_count"],
    }
    mutations = {
        "object": ("object", "SCALAR"),
        "universal": ("universal", "DERIVED"),
        "xmax": ("xmax", "DERIVED"),
        "round_clock": ("round_clock", "exp(phi)"),
        "wrl_global": ("wrl_global", "GLOBAL_CENTER_FREE"),
        "null_rest": ("null_rest", "UNIVERSAL"),
        "sne": ("SNe_scope", "DERIVED_GLOBAL"),
        "types": ("type_count", 7),
        "branches": ("branch_count", 5),
        "equations": ("equation_count", 27),
        "completions": ("completion_count", 11),
        "sources": ("source_count", 18),
    }
    if corrupt:
        key, value = mutations[corrupt]
        state[key] = value

    if (
        production["result"] != "PASS"
        or production["check_count"] != 84
        or set(production["checks"].values()) != {"PASS"}
        or production["registry"]
        != {
            "complete_g_phi_completion_witnesses": 0,
            "equation_families": 28,
            "finite_cell_completions": 12,
        }
        or state["object"] != "SET_VALUED_OBSERVER_OPTICAL_CORRESPONDENCE"
        or state["universal"] != "OPEN_SELECTOR"
        or state["xmax"] != "OPEN"
        or state["round_clock"] != "1"
        or state["wrl_global"]
        != "EXISTING_SNE_READOUT_IS_CENTERED_RESIDUAL_NOT_GLOBAL_PAIR_OPERATOR"
        or state["null_rest"] != "CONDITIONAL_NOT_UNIVERSAL"
        or state["SNe_scope"] != "OPEN_NOT_ESTABLISHED"
        or state["type_count"] != 8
        or state["branch_count"] != 6
        or state["equation_count"] != 28
        or len({row["family_id"] for row in equations}) != 28
        or state["completion_count"] != 12
        or len({row["completion_id"] for row in completions}) != 12
        or state["source_count"] != 19
        or independent["result"] != "PASS"
        or independent["check_count"] != 72
        or independent["catch_count"] != 14
        or set(independent["checks"].values()) != {"PASS"}
        or set(independent["catches"].values()) != {"PASS_REJECTED"}
    ):
        raise AssertionError("science adjudication")

    return {
        "deterministic_replay": "BYTE_IDENTICAL",
        "production_checks": 84,
        "independent_checks": 72,
        "independent_catches": 14,
        "source_identities": 19,
        "optical_types": 8,
        "branches": 6,
        "equation_families": 28,
        "finite_cell_completions": 12,
        "derived_object": "SET_VALUED_OBSERVER_OPTICAL_CORRESPONDENCE",
        "universal_operator": "OPEN",
        "physical_Xmax": "OPEN",
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
    if corrupt:
        branch = "main"
    metadata_sha = digest(status.stdout)
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
        "paths": 54,
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
        "passed": 70,
        "failed": 0,
        "xfailed": 1,
        "stdout_sha256": digest(completed.stdout.encode()),
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
        "center_free_optical_generic_gates",
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
    science_catches = {
        key: expect_failure(lambda key=key: validate_science(key))
        for key in [
            "object",
            "universal",
            "xmax",
            "round_clock",
            "wrl_global",
            "null_rest",
            "sne",
            "types",
            "branches",
            "equations",
            "completions",
            "sources",
        ]
    }
    catches = {
        "scope": expect_failure(lambda: validate_scope("CANON.md")),
        **{f"science_{key}": value for key, value in science_catches.items()},
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
        "schema": "udt-center-free-optical-repository-gates-1.0",
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
            "null_or_rest_pairing_selected": False,
            "physical_signal_law_claimed": False,
            "WRL_promoted_global": False,
            "branch_spliced": False,
            "physical_Xmax_promoted": False,
            "observational_claim_added": False,
            "action_source_carrier_selected": False,
            "gpu_work": False,
            "repository_reorganization": False,
        },
    }
    (HERE / "REPOSITORY_GATES.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

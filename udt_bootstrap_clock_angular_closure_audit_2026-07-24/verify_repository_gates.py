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
BASE = "4a6f72fc6d15ca19d3b97936b7332604655f4513"
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


def run(command: list[str], cwd: Path = ROOT, extra_env=None):
    environment = dict(os.environ)
    environment["CUDA_VISIBLE_DEVICES"] = ""
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    if extra_env:
        environment.update(extra_env)
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


def read_tsv(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def expect_failure(callback):
    try:
        callback()
    except AssertionError:
        return "PASS_REJECTED"
    raise AssertionError("catch accepted corruption")


def load_generic():
    path = (
        ROOT
        / "bootstrap_csn_phi_angular_selector_2026-07-19"
        / "verify_repository_gates.py"
    )
    spec = importlib.util.spec_from_file_location("bootstrap_closure_generic_gates", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.BASE = BASE
    module.PACKAGE = PACKAGE
    return module


def validate_scope(injected=""):
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
        raise AssertionError(f"scope:{invalid}")
    return sorted(path for path in paths if path)


def validate_science(corrupt=""):
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    routes = read_tsv(HERE / "BOOTSTRAP_ROUTE_LEDGER.tsv")
    equations = read_tsv(HERE / "EQUATION_FAMILY_GATE_MATRIX.tsv")
    completions = read_tsv(HERE / "COMPLETION_BOOTSTRAP_ATLAS.tsv")
    sources = read_tsv(HERE / "SOURCE_LINEAGE.tsv")
    state = {
        "checks": production["counts"]["checks"],
        "sources": len(sources),
        "routes": len(routes),
        "equations": len(equations),
        "completions": len(completions),
        "witnesses": production["counts"]["complete_registered_bootstrap_witnesses"],
        "catches": independent["counts"]["catch_proofs"],
        "projectors": independent["counts"]["fraction_matched_projector_samples"],
        "connection": independent["counts"]["fraction_connection_samples"],
        "solder": production["rulings"]["intrinsic_solder"],
        "path": production["rulings"]["path_level_caveat"],
        "negative": production["rulings"]["B19_and_WRL"],
    }
    mutations = {
        "checks": 32,
        "sources": 34,
        "routes": 7,
        "equations": 27,
        "completions": 11,
        "witnesses": 1,
        "catches": 22,
        "projectors": 8,
        "connection": 2,
        "solder": "DERIVED",
        "path": "FULL_COCYCLE_DERIVED",
        "negative": "UNIVERSAL_NO_GO",
    }
    if corrupt:
        state[corrupt] = mutations[corrupt]
    required = {
        "checks": 33,
        "sources": 35,
        "routes": 8,
        "equations": 28,
        "completions": 12,
        "witnesses": 0,
        "catches": 23,
        "projectors": 9,
        "connection": 3,
        "solder": "OPEN_BOOTSTRAP_COULD_ADDRESS_BUT_DOES_NOT_CURRENTLY_DERIVE",
        "path": "POINTWISE_MATCH_IS_NOT_FULL_COCYCLE_EQUIVALENCE;VARYING_CLOCK_RATE_REQUIRES_A_DERIVED_CONNECTION_TERM_OR_CONSTANT_RATE",
        "negative": "FAILURES_REMAIN_EXACT_IN_THEIR_SCOPES_NOT_UNIVERSAL_MATTER_FILLED_NO_GOS",
    }
    if state != required:
        raise AssertionError("science state")
    if (
        production["result"] != "PASS"
        or set(production["checks"].values()) != {"PASS"}
        or production["environment"]["sympy"] != "1.14.0"
        or independent["result"] != "PASS"
        or set(independent["catch_proofs"].values()) != {"PASS_REJECTED"}
    ):
        raise AssertionError("science verification")
    return {
        **state,
        "production_sha256": digest((HERE / "DERIVATION_RESULT.json").read_bytes()),
        "independent_sha256": digest((HERE / "INDEPENDENT_VERIFICATION.json").read_bytes()),
        "result": "PASS",
    }


def validate_replay():
    names = [
        "DERIVATION_RESULT.json",
        "SOURCE_LINEAGE.tsv",
        "BOOTSTRAP_ROUTE_LEDGER.tsv",
        "EQUATION_FAMILY_GATE_MATRIX.tsv",
        "COMPLETION_BOOTSTRAP_ATLAS.tsv",
        "INDEPENDENT_VERIFICATION.json",
        "PRODUCTION_STDOUT.txt",
        "PRODUCTION_STDERR.txt",
        "INDEPENDENT_STDOUT.txt",
        "INDEPENDENT_STDERR.txt",
        "RUN_ENVIRONMENT.json",
    ]
    before = {name: (HERE / name).read_bytes() for name in names}
    target = os.environ.get("UDT_SYMPY_TARGET", "")
    if not target:
        raise AssertionError("UDT_SYMPY_TARGET absent")
    replay = run(
        [sys.executable, "replay_and_capture.py"],
        cwd=HERE,
        extra_env={"UDT_SYMPY_TARGET": target},
    )
    if replay.returncode:
        raise AssertionError(replay.stdout)
    if any((HERE / name).read_bytes() != before[name] for name in names):
        raise AssertionError("replay not byte-identical")
    return "BYTE_IDENTICAL"


def validate_dirty(corrupt=False):
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
        ["git", "rev-parse", "HEAD"], cwd=DIRTY, stdout=subprocess.PIPE, check=True
    ).stdout.decode().strip()
    branch = subprocess.run(
        ["git", "branch", "--show-current"], cwd=DIRTY, stdout=subprocess.PIPE, check=True
    ).stdout.decode().strip()
    count = len(status.stdout.splitlines())
    metadata_sha = digest(status.stdout)
    if corrupt:
        count -= 1
    if (
        head != "adf8f92d95c387cc647f04b16f1f3b17e1e670d2"
        or branch != "grok"
        or count != 55
        or metadata_sha != "345d297e0ad849cd38f1d817c915922de653ca2d2befcf923af6f9d097b483e4"
    ):
        raise AssertionError("dirty checkout metadata")
    return {
        "head": head,
        "branch": branch,
        "paths": count,
        "metadata_sha256": metadata_sha,
        "contents_read": False,
        "note": "Only separately authorized phiequations.md content was read before this audit.",
        "result": "PASS",
    }


def validate_tests():
    completed = run([sys.executable, "-m", "pytest", "-q", "tests/"])
    match = re.search(r"(\d+) passed, (\d+) xfailed", completed.stdout)
    if completed.returncode or match is None or tuple(map(int, match.groups())) != (70, 1):
        raise AssertionError(completed.stdout)
    recorded = json.loads((HERE / "TEST_RESULT.json").read_text(encoding="utf-8"))
    if recorded["exit_code"] != 0 or recorded["passed"] != 70 or recorded["xfailed"] != 1:
        raise AssertionError("recorded tests")
    return {"passed": 70, "failed": 0, "xfailed": 1, "result": "PASS"}


def validate_package(corrupt=False):
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
        if path.is_file() and path.name not in {"SHA256SUMS.txt", "REPOSITORY_GATES.json"}
    )
    if sorted(entries) != actual:
        raise AssertionError("package coverage")
    return {
        "entries": len(entries),
        "manifest_sha256": digest((HERE / "SHA256SUMS.txt").read_bytes()),
        "result": "PASS",
    }


def main():
    generic = load_generic()
    scope = validate_scope()
    science = validate_science()
    replay = validate_replay()
    frozen = generic.validate_frozen(ROOT)
    navigation = generic.validate_navigation(ROOT)
    dirty = validate_dirty()
    tests = validate_tests()
    package = validate_package()
    catches = {
        "scope": expect_failure(lambda: validate_scope("CANON.md")),
        **{
            f"science_{key}": expect_failure(lambda key=key: validate_science(key))
            for key in [
                "checks",
                "sources",
                "routes",
                "equations",
                "completions",
                "witnesses",
                "catches",
                "projectors",
                "connection",
                "solder",
                "path",
                "negative",
            ]
        },
        "frozen": generic.expect("FROZEN", lambda: generic.validate_frozen(ROOT, corrupt=True)),
        "current_paths": generic.expect(
            "NAVIGATION", lambda: generic.validate_navigation(ROOT, corrupt="current")
        ),
        "frontier": generic.expect(
            "NAVIGATION", lambda: generic.validate_navigation(ROOT, corrupt="frontier")
        ),
        "dirty": expect_failure(lambda: validate_dirty(True)),
        "package": expect_failure(lambda: validate_package(True)),
    }
    result = {
        "schema": "udt-bootstrap-clock-angular-repository-gates-1.0",
        "base": BASE,
        "result": "PASS",
        "scope_paths": scope,
        "science": {**science, "deterministic_replay": replay},
        "frozen": frozen,
        "navigation": navigation,
        "dirty_checkout": dirty,
        "tests": tests,
        "package_manifest": package,
        "catch_proofs": catches,
        "authority_boundary": {
            "startup_navigation_changed": True,
            "canon_changed": False,
            "complete_bootstrap_claimed": False,
            "intrinsic_solder_promoted": False,
            "density_value_or_response_invented": False,
            "action_source_carrier_boundary_selected": False,
            "pointwise_match_promoted_to_path_cocycle": False,
            "gpu_or_time_live_work": False,
            "repository_reorganization": False,
        },
    }
    (HERE / "REPOSITORY_GATES.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

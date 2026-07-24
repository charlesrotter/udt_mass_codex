#!/usr/bin/env python3
"""Fail-closed science, repository, package, test, and dirty-checkout gates."""

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
ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
PACKAGE = HERE.name
BASE = "7ce44aa"
DIRTY = Path("/home/udt-admin/udt_mass_codex")


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
    bad = sorted(path for path in paths if path and not path.startswith(PACKAGE + "/"))
    if bad:
        raise AssertionError(f"scope:{bad[0]}")
    return sorted(path for path in paths if path)


def validate_science(corrupt: str = "") -> dict[str, object]:
    generated = [
        "DERIVATION_RESULT.json",
        "OPERATOR_STATUS_LEDGER.tsv",
        "CLOCK_READOUT_LEDGER.tsv",
        "TRANSPORT_TYPE_LEDGER.tsv",
        "GLOBAL_EVALUATION_GATE.tsv",
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

    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    operators = {row["id"]: row for row in read_tsv(HERE / "OPERATOR_STATUS_LEDGER.tsv")}
    readouts = {row["id"]: row for row in read_tsv(HERE / "CLOCK_READOUT_LEDGER.tsv")}
    transports = {row["id"]: row for row in read_tsv(HERE / "TRANSPORT_TYPE_LEDGER.tsv")}
    gates = {row["gate"]: row for row in read_tsv(HERE / "GLOBAL_EVALUATION_GATE.tsv")}

    if corrupt == "operator":
        operators["O01"]["status"] = "OPEN"
    elif corrupt == "endpoint":
        operators["O03"]["status"] = "DERIVED_UNCONDITIONAL"
    elif corrupt == "orthonormal":
        transports["T03"]["spatial_transport"] = "nontrivial boost"
    elif corrupt == "mutual":
        readouts["R03"]["status"] = "DERIVED_PHYSICAL"
    elif corrupt == "global":
        operators["O07"]["status"] = "DERIVED_PHYSICAL"
    elif corrupt == "path":
        gates["global path-independent full operator"]["result"] = "PASS"
    elif corrupt == "Xmax":
        gates["physical Xmax mass or CMB"]["result"] = "PASS"

    if (
        result["check_count"] != 62
        or set(result["checks"].values()) != {"PASS"}
        or result["source_count"] != 11
        or result["abstract_operator"]["status"]
        != "DERIVED_CONDITIONAL_WITH_FOUNDING_PREMISE_STAMPS"
        or result["balanced_basis"]["status"] != "DERIVED_ALGEBRAIC_O11_BOOST"
        or result["balanced_basis"]["physical_K_readout"] != "OPEN"
        or result["endpoint_realization"]["status"]
        != "CONDITIONAL_ON_OPEN_PAIR_TO_LOCAL_FIELD_JOIN"
        or result["metric_transport_control"]["coordinate_covector"] != "MATCHES_S_DELTA_PHI"
        or result["metric_transport_control"]["orthonormal_spatial_frame"] != "IDENTITY"
        or result["global_status"]["physical_Xmax"] != "OPEN"
        or len(operators) != 7
        or operators["O01"]["status"]
        != "DERIVED_CONDITIONAL_WITH_FOUNDING_PREMISE_STAMPS"
        or "OPEN_PAIR_TO_LOCAL_FIELD_JOIN" not in operators["O03"]["status"]
        or operators["O07"]["status"] != "OPEN_TYPED_GLOBAL_JOIN"
        or len(readouts) != 5
        or not readouts["R03"]["status"].startswith("CONDITIONAL_")
        or len(transports) != 5
        or transports["T03"]["spatial_transport"] != "identity"
        or len(gates) != 7
        or gates["global path-independent full operator"]["result"] != "OPEN"
        or gates["physical Xmax mass or CMB"]["result"] != "NOT_IN_SCOPE"
    ):
        raise AssertionError("science adjudication")
    if (
        independent["result"] != "PASS"
        or independent["check_count"] != 74
        or independent["catch_count"] != 12
        or set(independent["checks"].values()) != {"PASS"}
        or set(independent["catches"].values()) != {"PASS"}
        or independent["ruling"]["orthonormal_spatial_transport"] != "IDENTITY"
        or independent["ruling"]["global_physical_clock_readout"] != "OPEN_TYPED_JOIN"
    ):
        raise AssertionError("independent verification")
    sources = read_tsv(HERE / "SOURCE_LINEAGE.tsv")
    if len(sources) != 11 or len({row["id"] for row in sources}) != 11:
        raise AssertionError("source census")
    for row in sources:
        if hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() != row["sha256"]:
            raise AssertionError("source identity")
    return {
        "deterministic_replay": "BYTE_IDENTICAL",
        "production_checks": 62,
        "independent_checks": 74,
        "independent_catches": 12,
        "source_identities": 11,
        "abstract_operator": "DERIVED_CONDITIONAL_WITH_FOUNDING_PREMISE_STAMPS",
        "balanced_form": "DERIVED_ALGEBRAIC_O11_BOOST",
        "orthonormal_spatial_transport": "IDENTITY",
        "physical_global_clock_readout": "OPEN_TYPED_JOIN",
        "result_sha256": hashlib.sha256((HERE / "DERIVATION_RESULT.json").read_bytes()).hexdigest(),
        "independent_sha256": hashlib.sha256((HERE / "INDEPENDENT_VERIFICATION.json").read_bytes()).hexdigest(),
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
        or metadata_sha != "4bc96070c841a14c497b642ee7b93dcf9061372f770aee065d6b495ee4996f4c"
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
        if path.is_file() and path.name not in {"SHA256SUMS.txt", "REPOSITORY_GATES.json"}
    )
    if sorted(entries) != actual:
        raise AssertionError("package coverage")
    return {
        "entries": len(entries),
        "manifest_sha256": hashlib.sha256((HERE / "SHA256SUMS.txt").read_bytes()).hexdigest(),
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
        ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19" / "verify_repository_gates.py",
        "observer_pair_clock_generic_gates",
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
        "science_operator": expect_failure(lambda: validate_science("operator")),
        "science_endpoint": expect_failure(lambda: validate_science("endpoint")),
        "science_orthonormal": expect_failure(lambda: validate_science("orthonormal")),
        "science_mutual": expect_failure(lambda: validate_science("mutual")),
        "science_global": expect_failure(lambda: validate_science("global")),
        "science_path": expect_failure(lambda: validate_science("path")),
        "science_Xmax": expect_failure(lambda: validate_science("Xmax")),
        "frozen": generic.expect("FROZEN", lambda: generic.validate_frozen(ROOT, corrupt=True)),
        "current_paths": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, corrupt="current")),
        "frontier": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, corrupt="frontier")),
        "dirty": expect_failure(lambda: validate_dirty(True)),
        "package": expect_failure(lambda: validate_package(True)),
    }
    output = {
        "schema": "udt-observer-pair-clock-operator-repository-gates-1.0",
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
            "physical_K_readout_promoted": False,
            "local_phi_pair_join_promoted": False,
            "path_rule_selected": False,
            "physical_Xmax_promoted": False,
            "mass_density_or_CMB_promoted": False,
            "action_source_carrier_selected": False,
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

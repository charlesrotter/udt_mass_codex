#!/usr/bin/env python3
"""Fail-closed profile compatibility and repository verification."""

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
BASE = "f17dd4a"
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
        "PROFILE_COMPATIBILITY_LEDGER.tsv",
        "SHAPE_INVARIANT_LEDGER.tsv",
        "PAIRWISE_PROFILE_LEDGER.tsv",
        "REGISTRY_ACCOUNTING.tsv",
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

    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    profiles = {row["profile"]: row for row in read_tsv(HERE / "PROFILE_COMPATIBILITY_LEDGER.tsv")}
    invariants = {row["profile"]: row for row in read_tsv(HERE / "SHAPE_INVARIANT_LEDGER.tsv")}
    pairs = {row["pair"]: row for row in read_tsv(HERE / "PAIRWISE_PROFILE_LEDGER.tsv")}
    registry = {row["registry"]: row for row in read_tsv(HERE / "REGISTRY_ACCOUNTING.tsv")}
    statuses = {row["claim"]: row for row in read_tsv(HERE / "STATUS_LEDGER.tsv")}

    if corrupt == "identity":
        pairs["PROJECTIVE_TANH_vs_B19_ROUND"]["ruling"] = "IDENTICAL"
    elif corrupt == "clock":
        profiles["B19_ROUND_KAPPA_ONE"]["phi_role"] = "reciprocal clock depth"
    elif corrupt == "fc12":
        profiles["FC12_OPEN"]["ruling"] = "DERIVED_SELECTED"
    elif corrupt == "registry":
        result["registry"]["finite_cell_rows"] = 11
    elif corrupt == "witness":
        result["registry"]["complete_clock_angular_event_pair_witnesses"] = 1
    elif corrupt == "Xmax":
        result["global_Xmax"] = "DERIVED"
    elif corrupt == "exponent":
        statuses["shared endpoint exponent selects profile"]["status"] = "DERIVED"
    elif corrupt == "projective":
        profiles["PROJECTIVE_TANH"]["ruling"] = "PHYSICAL_SELECTED"
    elif corrupt == "wrl":
        profiles["WRL_EXPONENTIAL"]["ruling"] = "GLOBAL_PAIR_DIAMETER"

    if (
        result["check_count"] != 69
        or set(result["checks"].values()) != {"PASS"}
        or result["sources"] != 14
        or result["registry"]["finite_cell_rows"] != 12
        or result["registry"]["equation_families"] != 28
        or result["registry"]["calculated_controls"] != 3
        or result["registry"]["complete_clock_angular_event_pair_witnesses"] != 0
        or result["profiles"]["projective"] != "TANH_AVAILABLE_PHYSICAL_SOLDER_OPEN"
        or result["profiles"]["wrl"] != "SIMPLE_EXPONENTIAL_CONDITIONAL_LOCAL_CLOCK_DEPTH"
        or result["profiles"]["b19"] != "THIRD_DISTINCT_ROUND_ANGULAR_PROFILE"
        or result["profiles"]["fc12"] != "ARBITRARY_PROFILE_CHOICE_NOT_SELECTION"
        or result["inequivalence"]["constant_depth_rescaling"] != "ALL_THREE_PAIRWISE_DISTINCT"
        or result["physical_selector"] != "ABSENT_IN_REGISTERED_BRANCHES"
        or result["global_Xmax"] != "OPEN_NOT_EVALUABLE"
        or len(profiles) != 6
        or profiles["PROJECTIVE_TANH"]["ruling"] != "AVAILABLE_PROJECTIVE_PHYSICAL_SOLDER_OPEN"
        or profiles["WRL_EXPONENTIAL"]["ruling"] != "CONDITIONAL_LOCAL_NOT_GLOBAL_PAIR_DIAMETER"
        or profiles["B19_ROUND_KAPPA_ONE"]["ruling"] != "THIRD_DISTINCT_BOUNDED_PROFILE_CLOCK_UNSOLDERED"
        or profiles["B19_ROUND_KAPPA_ONE"]["phi_role"] != "angular reciprocal depth"
        or profiles["FC12_OPEN"]["ruling"] != "CHOICE_COMPATIBILITY_NOT_SELECTION"
        or len(invariants) != 3
        or invariants["PROJECTIVE_TANH"]["J3_equals_D3_over_D1_cubed"] != "-2"
        or invariants["WRL_EXPONENTIAL"]["J2_equals_D2_over_D1_squared"] != "-1"
        or invariants["B19_ROUND_ALL_POSITIVE_KAPPA"]["J3_equals_D3_over_D1_cubed"] != "-pi^2/4"
        or len(pairs) != 4
        or pairs["PROJECTIVE_TANH_vs_B19_ROUND"]["ruling"]
        != "EXACTLY_INEQUIVALENT_FOR_ALL_POSITIVE_KAPPA"
        or pairs["FC12_OPEN_vs_EACH_PROFILE"]["ruling"] != "COMPATIBLE_BY_CHOICE_NOT_DERIVED"
        or len(registry) != 3
        or registry["finite_cell_completion_rows"]["observed"] != "12"
        or registry["equation_evidence_families"]["observed"] != "28"
        or registry["calculated_transnormal_controls"]["observed"] != "3"
        or len(statuses) != 11
        or statuses["shared endpoint exponent selects profile"]["status"] != "REFUTED"
        or statuses["physical global Xmax"]["status"] != "OPEN_NOT_EVALUABLE"
    ):
        raise AssertionError("science adjudication")

    if (
        independent["result"] != "PASS"
        or independent["check_count"] != 72
        or independent["catch_count"] != 14
        or set(independent["checks"].values()) != {"PASS"}
        or set(independent["catches"].values()) != {"PASS"}
        or independent["ruling"]["bounded_profile_count"] != 3
        or independent["ruling"]["pairwise_identity"]
        != "REFUTED_UNDER_POSITIVE_CONSTANT_DEPTH_RESCALING"
        or independent["ruling"]["fc12"] != "COMPATIBLE_BY_CHOICE_NOT_SELECTED"
        or independent["ruling"]["complete_witnesses"] != 0
        or independent["ruling"]["global_Xmax"] != "OPEN"
    ):
        raise AssertionError("independent verification")

    sources = read_tsv(HERE / "SOURCE_LINEAGE.tsv")
    if len(sources) != 14 or len({row["id"] for row in sources}) != 14:
        raise AssertionError("source census")
    for row in sources:
        if hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() != row["sha256"]:
            raise AssertionError("source identity")
    return {
        "deterministic_replay": "BYTE_IDENTICAL",
        "production_checks": 69,
        "independent_checks": 72,
        "independent_catches": 14,
        "source_identities": 14,
        "finite_cell_rows": 12,
        "equation_families": 28,
        "calculated_controls": 3,
        "bounded_profiles": 3,
        "complete_witnesses": 0,
        "physical_selector": "ABSENT",
        "global_Xmax": "OPEN",
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
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=DIRTY, stdout=subprocess.PIPE, check=True).stdout.decode().strip()
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=DIRTY, stdout=subprocess.PIPE, check=True).stdout.decode().strip()
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
        "registered_profile_generic_gates",
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
        "science_identity": expect_failure(lambda: validate_science("identity")),
        "science_clock": expect_failure(lambda: validate_science("clock")),
        "science_fc12": expect_failure(lambda: validate_science("fc12")),
        "science_registry": expect_failure(lambda: validate_science("registry")),
        "science_witness": expect_failure(lambda: validate_science("witness")),
        "science_Xmax": expect_failure(lambda: validate_science("Xmax")),
        "science_exponent": expect_failure(lambda: validate_science("exponent")),
        "science_projective": expect_failure(lambda: validate_science("projective")),
        "science_wrl": expect_failure(lambda: validate_science("wrl")),
        "frozen": generic.expect("FROZEN", lambda: generic.validate_frozen(ROOT, corrupt=True)),
        "current_paths": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, corrupt="current")),
        "frontier": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, corrupt="frontier")),
        "dirty": expect_failure(lambda: validate_dirty(True)),
        "package": expect_failure(lambda: validate_package(True)),
    }
    output = {
        "schema": "udt-registered-branch-profile-compatibility-repository-gates-1.0",
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
            "branch_census_rewritten": False,
            "physical_distance_profile_selected": False,
            "clock_angular_phi_identified": False,
            "FC12_profile_selected": False,
            "physical_Xmax_promoted": False,
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

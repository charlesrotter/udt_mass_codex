#!/usr/bin/env python3
"""Fail-closed depth-angle and repository verification."""

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
BASE = "70833e8"
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
        "PROJECTIVE_TRANSITION_LEDGER.tsv",
        "PROFILE_METRIC_LEDGER.tsv",
        "DEPTH_ANGLE_COMPOSITION_LEDGER.tsv",
        "SOLDER_GATE_LEDGER.tsv",
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
    projective = {row["object"]: row for row in read_tsv(HERE / "PROJECTIVE_TRANSITION_LEDGER.tsv")}
    profiles = {row["profile"]: row for row in read_tsv(HERE / "PROFILE_METRIC_LEDGER.tsv")}
    composition = {row["domain"]: row for row in read_tsv(HERE / "DEPTH_ANGLE_COMPOSITION_LEDGER.tsv")}
    solder = {row["candidate"]: row for row in read_tsv(HERE / "SOLDER_GATE_LEDGER.tsv")}
    statuses = {row["claim"]: row for row in read_tsv(HERE / "STATUS_LEDGER.tsv")}

    if corrupt == "projective":
        result["projective"]["physical_distance_join"] = "DERIVED"
    elif corrupt == "unique":
        profiles["EXPONENTIAL_SATURATION"]["status"] = "UNIQUE"
    elif corrupt == "exponent":
        statuses["exponential approach in reciprocal depth"]["scope"] = "same exponent"
    elif corrupt == "taylor":
        statuses["early first-order Taylor discrimination"]["status"] = "SELECTS_TANH"
    elif corrupt == "angular":
        composition["round S3 observer-relative chart"]["angular_data"] = "none"
    elif corrupt == "lorentz":
        result["solder"]["lorentz"] = "DERIVED"
    elif corrupt == "coframe":
        result["solder"]["coframe_product"] = "DERIVED"
    elif corrupt == "scale":
        result["solder"]["c_only"] = "DERIVED"
    elif corrupt == "Xmax":
        statuses["physical global Xmax"]["status"] = "DERIVED"
    elif corrupt == "local":
        result["owner_frame"]["local_physics_changed"] = True

    if (
        result["check_count"] != 70
        or set(result["checks"].values()) != {"PASS"}
        or result["sources"] != 14
        or result["projective"]["coordinate"] != "xi=tanh(rho)"
        or result["projective"]["status"] != "UNIQUE_GIVEN_ANCHORED_PROJECTIVE_INTERPRETATION"
        or result["projective"]["physical_distance_join"] != "OPEN"
        or result["profiles"]["tanh"] != "PROJECTIVE_AVAILABLE_PHYSICAL_DISTANCE_OPEN"
        or result["profiles"]["exponential"] != "WRL_RADIAL_PROPER_DERIVED_CONDITIONAL_NOT_GLOBAL"
        or result["profiles"]["first_order_taylor"] != "DEGENERATE_CANNOT_DISCRIMINATE"
        or result["depth_angle"]["noncollinear"] != "DOT_AND_CROSS_ANGULAR_DATA_REQUIRED"
        or result["solder"]["lorentz"] != "NOT_DERIVED_TYPE_BLOCKED"
        or result["solder"]["coframe_product"] != "CHOSE_NOT_DERIVED"
        or result["solder"]["c_only"] != "NOT_DERIVED"
        or result["owner_frame"]["self_depth"] != "ZERO_EVERY_OBSERVER"
        or result["owner_frame"]["local_physics_changed"] is not False
        or len(projective) != 5
        or projective["three-anchor projective coordinate"]["status"]
        != "UNIQUE_GIVEN_ANCHORED_PROJECTIVE_INTERPRETATION"
        or len(profiles) != 4
        or profiles["PROJECTIVE_TANH"]["status"] != "AVAILABLE_NOT_PHYSICAL_DISTANCE_SELECTED"
        or profiles["PROJECTIVE_TANH"]["endpoint_gap"] != "~2*Dmax*exp(-2rho)"
        or profiles["EXPONENTIAL_SATURATION"]["status"] != "DERIVED_CONDITIONAL_IN_WRL_SLICE_NOT_GLOBAL"
        or profiles["EXPONENTIAL_SATURATION"]["endpoint_gap"] != "Dmax*exp(-rho)"
        or len(composition) != 5
        or composition["round S3 observer-relative chart"]["angular_data"]
        != "dot and cross products required"
        or len(solder) != 5
        or solder["projective xi to physical distance"]["ruling"] != "OPEN_PROJECTIVE_POSITION_SOLDER"
        or solder["c-only physical normalization"]["ruling"] != "NOT_DERIVED_FROM_C_ALONE"
        or len(statuses) != 16
        or statuses["exponential approach in reciprocal depth"]["status"]
        != "DERIVED_FOR_BOTH_BOUNDED_REGISTERED_PROFILES"
        or statuses["exponential approach in reciprocal depth"]["scope"]
        != "gap exponent one for WR-L proper; exponent two for projective tanh"
        or statuses["early first-order Taylor discrimination"]["status"] != "IMPOSSIBLE_AT_LINEAR_ORDER"
        or statuses["physical global Xmax"]["status"] != "OPEN_NOT_PROMOTED"
    ):
        raise AssertionError("science adjudication")

    if (
        independent["result"] != "PASS"
        or independent["check_count"] != 80
        or independent["catch_count"] != 16
        or set(independent["checks"].values()) != {"PASS"}
        or set(independent["catches"].values()) != {"PASS"}
        or independent["ruling"]["reciprocal_response"] != "EXACT_EXPONENTIAL"
        or independent["ruling"]["projective_coordinate"]
        != "TANH_GIVEN_ANCHORED_PROJECTIVE_ROLE"
        or independent["ruling"]["physical_distance_profile"] != "OPEN_BRANCH_CONDITIONAL"
        or independent["ruling"]["physical_Xmax"] != "OPEN"
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
        "production_checks": 70,
        "independent_checks": 80,
        "independent_catches": 16,
        "source_identities": 14,
        "reciprocal_response": "EXACT_EXPONENTIAL",
        "projective_coordinate": "TANH_GIVEN_ANCHORED_PROJECTIVE_ROLE",
        "physical_distance_profile": "OPEN_BRANCH_CONDITIONAL",
        "angular_transition": "NONABELIAN_DATA_REQUIRED",
        "physical_Xmax": "OPEN",
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
        "observer_depth_angle_generic_gates",
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
        "science_projective": expect_failure(lambda: validate_science("projective")),
        "science_unique": expect_failure(lambda: validate_science("unique")),
        "science_exponent": expect_failure(lambda: validate_science("exponent")),
        "science_taylor": expect_failure(lambda: validate_science("taylor")),
        "science_angular": expect_failure(lambda: validate_science("angular")),
        "science_lorentz": expect_failure(lambda: validate_science("lorentz")),
        "science_coframe": expect_failure(lambda: validate_science("coframe")),
        "science_scale": expect_failure(lambda: validate_science("scale")),
        "science_Xmax": expect_failure(lambda: validate_science("Xmax")),
        "science_local": expect_failure(lambda: validate_science("local")),
        "frozen": generic.expect("FROZEN", lambda: generic.validate_frozen(ROOT, corrupt=True)),
        "current_paths": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, corrupt="current")),
        "frontier": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, corrupt="frontier")),
        "dirty": expect_failure(lambda: validate_dirty(True)),
        "package": expect_failure(lambda: validate_package(True)),
    }
    output = {
        "schema": "udt-observer-depth-angle-transition-repository-gates-1.0",
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
            "physical_distance_profile_selected": False,
            "physical_tanh_law_promoted": False,
            "unique_exponential_law_promoted": False,
            "local_physics_modified": False,
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

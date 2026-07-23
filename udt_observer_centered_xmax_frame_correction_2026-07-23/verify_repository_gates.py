#!/usr/bin/env python3
"""Repository gates for the observer-centered Xmax correction."""

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
BASE = "2ffafce"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
PARENT = "udt_wrl_xmax_lightcone_frame_audit_2026-07-23"
PARENT_MANIFEST_SHA256 = (
    "1401fe8da653c6e8016b915f5c13d2c0660bd199f7d6b1b32acabb1dd3fdfaee"
)
MAXIMUM = (
    "THE_WRL_ALGEBRA_DERIVES_A_CENTERED_RELATIONAL_CLOCK_RULER_ASYMPTOTE_AT_A_ZERO_"
    "AND_NO_ADMISSIBLE_CONTINUATION_PRESERVING_THE_SAME_CLOCK_RULER_POLARIZATION;"
    "THE_REGULAR_INGOING_EXTENSION_PROVES_ONLY_MANIFOLD_EXTENDIBILITY_NOT_A_PHYSICAL_"
    "OBSERVER_CROSSING;DISTINCT_OBSERVER_CENTERS_CANNOT_BE_STANDARD_OVERLAPPING_"
    "COORDINATE_CHARTS_OF_THE_SAME_NONHOMOGENEOUS_WRL_TENSOR_GEOMETRY;LOCAL_INERTIAL_"
    "FRAME_EQUIVALENCE_IS_DERIVED_BUT_GLOBAL_OBSERVER_RECENTERING_AND_COMMON_XMAX_"
    "REQUIRE_AN_OBSERVER_INDEXED_COMPOSITION_LAW_OR_COMPLETE_METRIC_NOT_YET_DERIVED;"
    "A_VARYING_COFRAME_CHANGES_CONNECTION_COMPONENTS_BUT_NOT_INVARIANT_CURVATURE_OR_"
    "CONES_WITHOUT_A_PHYSICAL_METRIC_RESPONSE_LAW"
)


def load(path: Path, name: str):
    specification = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(specification)
    assert specification.loader is not None
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def replay_parent(generic, corrupt: bool = False) -> dict[str, object]:
    parent_gate = load(
        ROOT / PARENT / "verify_repository_gates.py",
        "observer_center_parent_gate",
    )
    prior = parent_gate.replay_parent(generic, False)
    manifest = ROOT / PARENT / "MANIFEST.sha256"
    observed = digest(manifest)
    if corrupt:
        observed = "0" * 64
    if observed != PARENT_MANIFEST_SHA256:
        raise generic.GateError("PARENT", "manifest")
    replay = generic.run(manifest.parent, ["sha256sum", "--check", manifest.name])
    if replay.returncode or "FAILED" in str(replay.stdout):
        raise generic.GateError("PARENT", "replay")
    entries = len([line for line in manifest.read_text().splitlines() if line])
    packages = list(prior["packages"])
    packages.append(
        {
            "package": PARENT,
            "manifest": manifest.name,
            "manifest_sha256": observed,
            "entries": entries,
            "result": "PASS",
        }
    )
    if len(packages) != 102 or entries != 23:
        raise generic.GateError("PARENT", f"totals:{len(packages)}:{entries}")
    return {
        "packages": packages,
        "entries": int(prior["entries"]) + entries,
        "result": "PASS",
    }


def validate_tests() -> dict[str, object]:
    environment = dict(os.environ)
    environment["CUDA_VISIBLE_DEVICES"] = ""
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "tests/"],
        cwd=ROOT,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    match = re.search(r"(\d+) passed, (\d+) xfailed", completed.stdout)
    if (
        completed.returncode != 0
        or match is None
        or tuple(map(int, match.groups())) != (70, 1)
        or " failed" in completed.stdout
    ):
        raise AssertionError("repository test baseline changed")
    recorded = json.loads(HERE.joinpath("FULL_TEST_RESULT.json").read_text())
    if (recorded["passed"], recorded["failed"], recorded["xfailed"]) != (70, 0, 1):
        raise AssertionError("recorded test result")
    return {
        "command": (
            "CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 "
            "python3 -m pytest -q tests/"
        ),
        "passed": 70,
        "failed": 0,
        "xfailed": 1,
        "returncode": 0,
        "result": "PASS",
    }


def validate_package(generic, corrupt: bool = False) -> dict[str, object]:
    manifest = HERE / "MANIFEST.sha256"
    replay = generic.run(HERE, ["sha256sum", "--check", manifest.name])
    if corrupt or replay.returncode or "FAILED" in str(replay.stdout):
        raise generic.GateError("PACKAGE", "manifest-replay")
    entries = [
        line.split("  ", 1)[1]
        for line in manifest.read_text(encoding="utf-8").splitlines()
        if line
    ]
    excluded = {"MANIFEST.sha256", "REPOSITORY_GATES.json"}
    actual = sorted(
        path.name
        for path in HERE.iterdir()
        if path.is_file() and path.name not in excluded
    )
    if sorted(entries) != actual:
        raise generic.GateError("PACKAGE", "manifest-coverage")
    return {
        "entries": len(entries),
        "manifest_sha256": digest(manifest),
        "result": "PASS",
    }


def validate_science(mutation: str = "") -> dict[str, object]:
    production_module = load(
        HERE / "derive_observer_centered_xmax.py",
        "observer_center_production",
    )
    result = production_module.derive(ROOT)
    recorded = json.loads(HERE.joinpath("DERIVATION_RESULT.json").read_text())
    independent = json.loads(HERE.joinpath("INDEPENDENT_VERIFICATION.json").read_text())
    statuses = read_tsv(HERE / "STATUS_LEDGER.tsv")
    status = {row["claim_id"]: row["status"] for row in statuses}
    if mutation == "crossing":
        status["S13"] = "DERIVED"
    parent = read_tsv(HERE / "PARENT_REGRADE.tsv")
    centers = read_tsv(HERE / "CENTER_COMPATIBILITY.tsv")
    acceleration = read_tsv(HERE / "ACCELERATION_LEDGER.tsv")
    sources = read_tsv(HERE / "SOURCE_LINEAGE.tsv")
    catches = read_tsv(HERE / "CATCH_PROOFS.tsv")
    report = HERE.joinpath("AUDIT_REPORT.md").read_text()
    source_map = {row["path"]: row["sha256"] for row in sources}
    exact_sources = {row["path"]: row["sha256"] for row in result["source_hashes"]}
    if (
        result["maximum_conclusion"] != MAXIMUM
        or recorded["maximum_conclusion"] != MAXIMUM
        or result["check_count"] != 48
        or not result["all_checks_pass"]
        or not recorded["all_checks_pass"]
        or len(statuses) != 30
        or len(parent) != 15
        or len(centers) != 12
        or len(acceleration) != 10
        or len(sources) != 16
        or source_map != exact_sources
        or len(catches) != 18
        or any(row["expected_result"] != "FAIL" for row in catches)
        or status["S10"] != "DERIVED_CONDITIONAL_CENTERED_DOMAIN"
        or status["S13"] != "WITHDRAWN_INTERPRETATION"
        or status["S16"] != "REFUTED_IN_CLASS"
        or status["S21"] != "OPEN"
        or status["S24"] != "OWNER_LOCKED_CONDITIONAL_CONSISTENCY"
        or independent["all_checks_pass"] is not True
        or independent["check_count"] != 72
        or independent["catch_count"] != 18
        or independent["imports_production_module"] is not False
        or "Grade: `VERIFIED-WITH-CAVEATS`" not in report
    ):
        raise AssertionError("science contract")
    return {
        "grade": "VERIFIED-WITH-CAVEATS",
        "production_checks": result["check_count"],
        "production_semantic_catches": result["semantic_catch_count"],
        "independent_checks": independent["check_count"],
        "independent_catches": independent["catch_count"],
        "sources": len(sources),
        "statuses": len(statuses),
        "parent_regrades": len(parent),
        "center_rows": len(centers),
        "acceleration_rows": len(acceleration),
        "result": "PASS",
    }


def reject_crossing_mutation(generic) -> None:
    try:
        validate_science(mutation="crossing")
    except AssertionError as exc:
        raise generic.GateError("SCIENCE", "physical-crossing-promotion") from exc


def main() -> None:
    generic = load(
        ROOT
        / "bootstrap_csn_phi_angular_selector_2026-07-19"
        / "verify_repository_gates.py",
        "observer_center_generic_gate",
    )
    generic.BASE = BASE
    generic.PACKAGE = PACKAGE
    scope = generic.validate_scope(ROOT)
    frozen = generic.validate_frozen(ROOT)
    prior = replay_parent(generic)
    navigation = generic.validate_navigation(ROOT)
    dirty = generic.validate_dirty(ROOT, DIRTY)
    parent_head = load(
        ROOT
        / "udt_invariant_xmax_asymptotic_boundary_audit_2026-07-23"
        / "verify_repository_gates.py",
        "observer_center_dirty_head",
    )
    dirty.update(parent_head.validate_dirty_head(generic))
    tests = validate_tests()
    science = validate_science()
    package = validate_package(generic)
    catches = {
        "scope": generic.expect(
            "SCOPE", lambda: generic.validate_scope(ROOT, "LIVE.md")
        ),
        "frozen": generic.expect(
            "FROZEN", lambda: generic.validate_frozen(ROOT, corrupt=True)
        ),
        "parent": generic.expect(
            "PARENT", lambda: replay_parent(generic, corrupt=True)
        ),
        "current_paths": generic.expect(
            "NAVIGATION",
            lambda: generic.validate_navigation(ROOT, corrupt="current"),
        ),
        "frontier": generic.expect(
            "NAVIGATION",
            lambda: generic.validate_navigation(ROOT, corrupt="frontier"),
        ),
        "dirty": generic.expect(
            "DIRTY",
            lambda: generic.validate_dirty(ROOT, DIRTY, corrupt=True),
        ),
        "package": generic.expect(
            "PACKAGE", lambda: validate_package(generic, corrupt=True)
        ),
        "physical_crossing": generic.expect(
            "SCIENCE", lambda: reject_crossing_mutation(generic)
        ),
    }
    output = {
        "schema": "udt-observer-centered-xmax-repository-gates-1.0",
        "result": "PASS",
        "base": BASE,
        "authority_boundary": MAXIMUM,
        "scope_paths": scope,
        "science": science,
        "frozen": frozen,
        "prior_scientific_packages": prior,
        "navigation": navigation,
        "dirty_checkout": dirty,
        "tests": tests,
        "package_manifest": package,
        "catch_proofs": catches,
        "compute": {"cpu_only": True, "gpu_work_performed": False},
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

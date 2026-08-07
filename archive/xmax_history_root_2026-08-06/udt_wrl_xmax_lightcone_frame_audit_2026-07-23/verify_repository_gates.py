#!/usr/bin/env python3
"""Repository gates for the WR-L/Xmax light-cone frame audit."""

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
BASE = "44ebe4c"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
PARENT = "udt_xmax_dilation_asymptote_correction_2026-07-23"
PARENT_MANIFEST_SHA256 = (
    "44bac08d6cc37d1326193d357a91823c15da5de025eddba4dbef86882318cc6a"
)
MAXIMUM = (
    "THE_WRL_METRIC_DERIVES_A_FRAME_INVARIANT_NULL_SURFACE_AND_LOCAL_"
    "LORENTZIAN_OBSERVER_RECIPROCITY;STATIC_CLOCK_AND_OPTICAL_"
    "UNATTAINABILITY_ARE_EXACT;THE_REGULAR_INGOING_CHART_ADMITS_CROSSING_"
    "CURVES;THE_CONSTANT_DEPTH_RECENTERING_OF_THE_OLDER_PROJECTIVE_FRAME_"
    "FAILS_AS_A_FULL_WRL_METRIC_HOMOTHETY_IN_THE_AREAL_ANGULAR_SECTOR;"
    "UNIVERSAL_UNCROSSABILITY_AND_GLOBAL_OBSERVER_RECIPROCITY_REQUIRE_"
    "ADDITIONAL_COMPLETE_METRIC_OR_BOUNDARY_CONTENT"
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
        "wrl_lightcone_parent_gate",
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
    entries = len(
        [line for line in manifest.read_text(encoding="utf-8").splitlines() if line]
    )
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
    if len(packages) != 101 or entries != 22:
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


def validate_science() -> dict[str, object]:
    production = load(
        HERE / "derive_wrl_xmax_lightcone_frame.py",
        "wrl_lightcone_production",
    )
    result = production.build_result()
    recorded = json.loads(
        (HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8")
    )
    independent = json.loads(
        (HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8")
    )
    statuses = read_tsv(HERE / "STATUS_LEDGER.tsv")
    lightcone = read_tsv(HERE / "LIGHTCONE_ATLAS.tsv")
    distinctions = read_tsv(HERE / "FRAME_DISTINCTION_LEDGER.tsv")
    angular = read_tsv(HERE / "ANGULAR_OBSTRUCTION.tsv")
    prior = read_tsv(HERE / "PRIOR_WORK_REGRADE.tsv")
    sources = read_tsv(HERE / "SOURCE_LINEAGE.tsv")
    catches = read_tsv(HERE / "CATCH_PROOFS.tsv")
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    if (
        result["maximum_conclusion"] != MAXIMUM
        or recorded["maximum_conclusion"] != MAXIMUM
        or result["check_count"] != 67
        or recorded["check_count"] != 67
        or result["regular_extension"]["ruling"]
        != "METRIC_ADMITS_CROSSING;GLOBAL_EXTENSION_OR_BOUNDARY_SELECTION_OPEN"
        or result["global_recentering"]["ruling"]
        != "OLDER_CONSTANT_DEPTH_SHIFT_IS_NOT_A_FULL_WRL_HOMOTHETY_WITH_FIXED_ANGLES"
        or len(statuses) != 22
        or len(lightcone) != 9
        or len(distinctions) != 15
        or len(angular) != 9
        or len(prior) != 11
        or len(sources) != 14
        or len(catches) != 20
        or any(row["result"] != "PASS_REJECTED" for row in catches)
        or independent["all_checks_pass"] is not True
        or independent["check_count"] != 89
        or independent["catch_pass_count"] != 12
        or independent["imports_production_module"] is not False
        or "Grade: `VERIFIED-WITH-CAVEATS`" not in report
    ):
        raise AssertionError("science contract")
    return {
        "grade": "VERIFIED-WITH-CAVEATS",
        "production_checks": result["check_count"],
        "production_catches": len(catches),
        "independent_checks": independent["check_count"],
        "independent_catches": independent["catch_pass_count"],
        "sources": len(sources),
        "statuses": len(statuses),
        "prior_regrades": len(prior),
        "result": "PASS",
    }


def main() -> None:
    generic = load(
        ROOT
        / "bootstrap_csn_phi_angular_selector_2026-07-19"
        / "verify_repository_gates.py",
        "wrl_lightcone_generic_gate",
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
        "wrl_lightcone_dirty_head",
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
    }
    output = {
        "schema": "udt-wrl-xmax-lightcone-frame-repository-gates-1.0",
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

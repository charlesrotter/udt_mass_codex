#!/usr/bin/env python3
"""Repository gates for the metric-pure frame rederivation."""

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
BASE = "5b74105"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
PARENT = "udt_observer_centered_xmax_frame_correction_2026-07-23"
PARENT_MANIFEST_SHA256 = (
    "024e32b90f0ba6fe7ef56b957f04cc88d375a9325597832d60d887768b7ab57b"
)
MAXIMUM = (
    "THE_METRIC_PURE_PARENT_IS_THE_FOUR_DIMENSIONAL_CONFORMAL_LORENTZIAN_"
    "METRIC_COFRAME_CLASS_NOT_WRL;IT_DERIVES_NO_PREFERRED_LOCAL_TIMELIKE_"
    "OBSERVER_AND_EXACT_LOCAL_SO_PLUS_1_3_FRAME_RECIPROCITY_WITH_A_COMMON_"
    "NULL_CONE;IT_DOES_NOT_DERIVE_GLOBAL_ISOMETRIC_RECENTERING_OR_AN_"
    "OBSERVER_INDEXED_PAIR_METRIC;WRL_IS_A_ONE_FUNCTION_STATIC_SPHERICAL_"
    "DIAGONAL_AREAL_ZERO_SHIFT_REDUCTION_NOT_CLOSED_AS_A_COMPLETE_FRAME_"
    "RECIPROCAL_CONFIGURATION_SPACE;ITS_PROFILE_ASYMPTOTE_AND_SNE_READOUT_"
    "SURVIVE_ONLY_IN_THAT_REDUCTION;PHYSICAL_ACCELERATION_INDUCED_METRIC_"
    "WARPING_REMAINS_OPEN"
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
        "metric_pure_parent_gate",
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
    if len(packages) != 103 or entries != 22:
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
    module = load(HERE / "derive_metric_pure_frames.py", "metric_pure_production")
    result = module.derive(ROOT)
    recorded = json.loads(HERE.joinpath("DERIVATION_RESULT.json").read_text())
    independent = json.loads(HERE.joinpath("INDEPENDENT_VERIFICATION.json").read_text())
    statuses = read_tsv(HERE / "STATUS_LEDGER.tsv")
    status = {row["claim_id"]: row["status"] for row in statuses}
    if mutation == "screen":
        status["Q11"] = "OPEN"
    parent_ledger = read_tsv(HERE / "METRIC_PARENT_LEDGER.tsv")
    reduction = read_tsv(HERE / "WRL_REDUCTION_LEDGER.tsv")
    frames = read_tsv(HERE / "FRAME_RECIPROCITY_LEDGER.tsv")
    survival = read_tsv(HERE / "WRL_SURVIVAL_LEDGER.tsv")
    sources = read_tsv(HERE / "SOURCE_LINEAGE.tsv")
    catches = read_tsv(HERE / "CATCH_PROOFS.tsv")
    source_map = {row["path"]: row["sha256"] for row in sources}
    exact_sources = {row["path"]: row["sha256"] for row in result["source_hashes"]}
    report = HERE.joinpath("AUDIT_REPORT.md").read_text()
    if (
        result["maximum_conclusion"] != MAXIMUM
        or recorded["maximum_conclusion"] != MAXIMUM
        or result["check_count"] != 69
        or not result["all_checks_pass"]
        or not recorded["all_checks_pass"]
        or len(statuses) != 35
        or len(parent_ledger) != 12
        or len(reduction) != 16
        or len(frames) != 16
        or len(survival) != 16
        or len(sources) != 18
        or source_map != exact_sources
        or len(catches) != 22
        or any(row["expected_result"] != "FAIL" for row in catches)
        or status["Q01"] != "REFUTED_BY_SOURCE_CENSUS"
        or status["Q04"] != "DERIVED_LOCAL"
        or status["Q11"] != "DERIVED_LOCAL"
        or status["Q13"] != "OPEN_NOT_JOINED"
        or status["Q17"] != "DERIVED_REDUCTION_CENSUS"
        or status["Q30"] != "OPEN"
        or independent["all_checks_pass"] is not True
        or independent["check_count"] != 82
        or independent["catch_count"] != 22
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
        "metric_parent_rows": len(parent_ledger),
        "reduction_rows": len(reduction),
        "frame_rows": len(frames),
        "survival_rows": len(survival),
        "result": "PASS",
    }


def reject_screen_mutation(generic) -> None:
    try:
        validate_science(mutation="screen")
    except AssertionError as exc:
        raise generic.GateError("SCIENCE", "screen-rotation-demotion") from exc


def main() -> None:
    generic = load(
        ROOT
        / "bootstrap_csn_phi_angular_selector_2026-07-19"
        / "verify_repository_gates.py",
        "metric_pure_generic_gate",
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
        "metric_pure_dirty_head",
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
        "screen_rotation": generic.expect(
            "SCIENCE", lambda: reject_screen_mutation(generic)
        ),
    }
    output = {
        "schema": "udt-metric-pure-frame-repository-gates-1.0",
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
    rendered = json.dumps(output, indent=2, sort_keys=True) + "\n"
    HERE.joinpath("REPOSITORY_GATES.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()

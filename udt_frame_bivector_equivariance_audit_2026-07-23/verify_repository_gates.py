#!/usr/bin/env python3
"""Repository gates for the frame/bivector equivariance audit."""

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
BASE = "94c32e2"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
FRAME_PARENT = "udt_metric_pure_frame_rederivation_2026-07-23"
FRAME_MANIFEST_SHA256 = (
    "dd3b401794240c33a5af00f6004b76baca43d0148f7905fd904129cbd2684cb0"
)
DPHI_PARENT = "udt_complete_metric_intrinsic_object_audit_2026-07-23"
DPHI_MANIFEST_SHA256 = (
    "1857bde1fff72829487f56ddd9fb461a2d9cad7b777a51baa125529713c8bfd4"
)
MAXIMUM = (
    "THE_COLLINEAR_RECIPROCAL_EXPONENTIAL_IS_AN_EXACT_SO_PLUS_1_1_"
    "NULL_WEIGHT_BUT_HAS_NO_NONTRIVIAL_CONTINUOUS_SCALAR_CHARACTER_"
    "EXTENSION_TO_SO_PLUS_1_3;THE_FULL_REAL_BIVECTOR_REPRESENTATION_"
    "HAS_EXACT_COLLINEAR_WEIGHT_MULTIPLICITIES_2PLUS2PLUS2_NOT_THE_"
    "DPHI_3PLUS3_SPLIT;THE_NONNULL_DPHI_SPLIT_IS_A_LORENTZ_AND_CSN_"
    "EQUIVARIANT_FAMILY_NOT_A_FIXED_FULL_GROUP_INVARIANT;ON_TIMELIKE_"
    "DPHI_THE_SPLIT_IS_EXACTLY_THE_CARTAN_BOOST3_PLUS_ROTATION3_"
    "DECOMPOSITION_AND_BOOST_BOOST_COMMUTATORS_GENERATE_THE_ROTATION_"
    "SECTOR;ITS_SO3_STABILIZER_CARRIES_THE_EXACT_NONCOLLINEAR_SCREEN_"
    "ROTATION_ON_BOTH_HODGE_EXCHANGED_RANK3_SECTORS;THE_SECTOR_JOIN_"
    "IS_EXACT_BUT_NONTRIVIAL_RECIPROCAL_WEIGHTING_IS_NOT_A_LORENTZ_"
    "ALGEBRA_AUTOMORPHISM_OR_A_RAPIDITY_PHI_IDENTITY;SPACELIKE_NULL_ZERO_TYPECHANGE_"
    "CONNECTION_HOLONOMY_GLOBAL_AND_PHYSICAL_JOINS_REMAIN_SCOPED_"
    "OPEN_OR_DEGENERATE"
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
        ROOT / FRAME_PARENT / "verify_repository_gates.py",
        "frame_bivector_parent_gate",
    )
    prior = parent_gate.replay_parent(generic, False)
    manifest = ROOT / FRAME_PARENT / "MANIFEST.sha256"
    observed = digest(manifest)
    if corrupt:
        observed = "0" * 64
    if observed != FRAME_MANIFEST_SHA256:
        raise generic.GateError("PARENT", "frame-manifest")
    replay = generic.run(manifest.parent, ["sha256sum", "--check", manifest.name])
    if replay.returncode or "FAILED" in str(replay.stdout):
        raise generic.GateError("PARENT", "frame-replay")
    entries = len([line for line in manifest.read_text().splitlines() if line])
    packages = list(prior["packages"])
    packages.append(
        {
            "package": FRAME_PARENT,
            "manifest": manifest.name,
            "manifest_sha256": observed,
            "entries": entries,
            "result": "PASS",
        }
    )
    if len(packages) != 104 or entries != 23:
        raise generic.GateError("PARENT", f"totals:{len(packages)}:{entries}")
    dphi_manifest = ROOT / DPHI_PARENT / "MANIFEST.sha256"
    if digest(dphi_manifest) != DPHI_MANIFEST_SHA256:
        raise generic.GateError("PARENT", "dphi-manifest")
    dphi_replay = generic.run(
        dphi_manifest.parent, ["sha256sum", "--check", dphi_manifest.name]
    )
    if dphi_replay.returncode or "FAILED" in str(dphi_replay.stdout):
        raise generic.GateError("PARENT", "dphi-replay")
    return {
        "packages": packages,
        "entries": int(prior["entries"]) + entries,
        "explicit_dphi_parent": {
            "package": DPHI_PARENT,
            "manifest_sha256": DPHI_MANIFEST_SHA256,
            "result": "PASS",
        },
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
    stdout = HERE.joinpath("FULL_TEST_STDOUT.txt")
    if (
        (recorded["passed"], recorded["failed"], recorded["xfailed"])
        != (70, 0, 1)
        or digest(stdout) != recorded["stdout_sha256"]
    ):
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
        "stdout_sha256": recorded["stdout_sha256"],
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
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    replay = subprocess.run(
        [sys.executable, "derive_frame_bivector_equivariance.py"],
        cwd=HERE,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if replay.returncode:
        raise AssertionError("production replay")
    result = json.loads(HERE.joinpath("DERIVATION_RESULT.json").read_text())
    independent = json.loads(
        HERE.joinpath("INDEPENDENT_VERIFICATION.json").read_text()
    )
    if mutation:
        result["classifications"][mutation] = "CORRUPTED"
    statuses = read_tsv(HERE / "STATUS_LEDGER.tsv")
    status = {row["id"]: row["status"] for row in statuses}
    representations = read_tsv(HERE / "REPRESENTATION_LEDGER.tsv")
    strata = read_tsv(HERE / "DPHI_STRATUM_ATLAS.tsv")
    connections = read_tsv(HERE / "CONNECTION_DISTINCTION_LEDGER.tsv")
    premises = read_tsv(HERE / "PREMISE_LEDGER.tsv")
    sources = read_tsv(HERE / "SOURCE_LINEAGE.tsv")
    catches = read_tsv(HERE / "CATCH_PROOFS.tsv")
    source_map = {row["path"]: row["sha256"] for row in sources}
    exact_sources = {row["path"]: row["sha256"] for row in result["source_hashes"]}
    report = HERE.joinpath("AUDIT_REPORT.md").read_text()
    required_classes = {
        "full_group_scalar_extension": "OBSTRUCTED_NONTRIVIAL_CHARACTER",
        "full_bivector_representation": "EXACT_2PLUS2PLUS2_COLLINEAR_WEIGHTS_NOT_DPHI_3PLUS3",
        "timelike_dphi_algebra_join": "EXACT_CARTAN_3PLUS3_BOOST_ROTATION_DECOMPOSITION",
        "angular_generation": "BOOST_SECTOR_COMMUTATORS_SPAN_ROTATION_SECTOR",
        "reciprocal_weight_automorphism": "OBSTRUCTED_EXCEPT_TRIVIAL_WEIGHT",
        "timelike_dphi_congruence": "HYPERSURFACE_ORTHOGONAL_ZERO_FROBENIUS_TWIST",
        "rapidity_phi": "OPEN_NOT_IDENTIFIED",
        "physical_promotion": "NONE",
    }
    if (
        result["maximum_conclusion"] != MAXIMUM
        or result["check_count"] != 79
        or not result["all_checks_pass"]
        or any(
            result["classifications"].get(key) != value
            for key, value in required_classes.items()
        )
        or len(statuses) != 36
        or len(representations) != 20
        or len(strata) != 5
        or len(connections) != 12
        or len(premises) != 18
        or len(sources) != 14
        or source_map != exact_sources
        or len(catches) != 22
        or any(row["expected_result"] != "FAIL" for row in catches)
        or status["Q04"] != "OBSTRUCTED"
        or status["Q11"] != "DERIVED_CONDITIONAL"
        or status["Q12"] != "DERIVED_EXACT"
        or status["Q17"] != "OBSTRUCTED"
        or status["Q20"] != "OPEN_NOT_JOINED"
        or status["Q31"] != "OPEN"
        or status["Q36"] != "VERIFIED_WITH_CAVEATS"
        or independent["all_checks_pass"] is not True
        or independent["check_count"] != 65
        or independent["catch_count"] != 22
        or independent["imports_production_module"] is not False
        or "Grade: `VERIFIED-WITH-CAVEATS`" not in report
    ):
        raise AssertionError("science contract")
    return {
        "grade": "VERIFIED-WITH-CAVEATS",
        "production_checks": result["check_count"],
        "independent_checks": independent["check_count"],
        "independent_catches": independent["catch_count"],
        "sources": len(sources),
        "statuses": len(statuses),
        "representations": len(representations),
        "strata": len(strata),
        "connections": len(connections),
        "premises": len(premises),
        "result": "PASS",
    }


def reject_structure_mutation(generic) -> None:
    try:
        validate_science(mutation="timelike_dphi_algebra_join")
    except AssertionError as exc:
        raise generic.GateError("SCIENCE", "Cartan-join") from exc


def main() -> None:
    generic = load(
        ROOT
        / "bootstrap_csn_phi_angular_selector_2026-07-19"
        / "verify_repository_gates.py",
        "frame_bivector_generic_gate",
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
        "frame_bivector_dirty_head",
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
        "Cartan_join": generic.expect(
            "SCIENCE", lambda: reject_structure_mutation(generic)
        ),
    }
    output = {
        "schema": "udt-frame-bivector-repository-gates-1.0",
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

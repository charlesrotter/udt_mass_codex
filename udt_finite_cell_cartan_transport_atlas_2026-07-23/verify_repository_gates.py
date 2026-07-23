#!/usr/bin/env python3
"""Repository gates for the finite-cell Cartan transport atlas."""

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
BASE = "2a0a199"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
PARENT = "udt_frame_bivector_equivariance_audit_2026-07-23"
PARENT_MANIFEST_SHA256 = "1fcfc5f1a5c6a3171123ed6f0022fce797e612478b805a998fbc327009633ecc"
MAXIMUM = (
    "EXACT_LOCAL_PERSISTENCE_MIXING_KATO_TRANSPORT_AND_CAUSAL_"
    "DEGENERATION_RULES_FOR_THE_DPHI_ASSISTED_3PLUS3_REDUCTION_"
    "CROSSED_WITH_ALL_TWELVE_REGISTERED_FINITE_CELL_COMPLETION_"
    "FAMILIES__ZERO_COMPLETE_ONSHELL_BRANCHES_AND_NO_PHYSICAL_SELECTION"
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
    parent_gate = load(ROOT / PARENT / "verify_repository_gates.py", "cartan_transport_parent")
    prior = parent_gate.replay_parent(generic, False)
    manifest = ROOT / PARENT / "MANIFEST.sha256"
    observed = digest(manifest)
    if corrupt:
        observed = "0" * 64
    if observed != PARENT_MANIFEST_SHA256:
        raise generic.GateError("PARENT", "frame-bivector-manifest")
    replay = generic.run(manifest.parent, ["sha256sum", "--check", manifest.name])
    if replay.returncode or "FAILED" in str(replay.stdout):
        raise generic.GateError("PARENT", "frame-bivector-replay")
    entries = len([line for line in manifest.read_text().splitlines() if line])
    packages = list(prior["packages"])
    packages.append({
        "package": PARENT,
        "manifest": manifest.name,
        "manifest_sha256": observed,
        "entries": entries,
        "result": "PASS",
    })
    if len(packages) != 105 or entries != 22:
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
    if (
        (recorded["passed"], recorded["failed"], recorded["xfailed"]) != (70, 0, 1)
        or digest(HERE / "FULL_TEST_STDOUT.txt") != recorded["stdout_sha256"]
    ):
        raise AssertionError("recorded test result")
    return {**recorded, "result": "PASS"}


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
    actual = sorted(
        path.name
        for path in HERE.iterdir()
        if path.is_file() and path.name not in {"MANIFEST.sha256", "REPOSITORY_GATES.json"}
    )
    if sorted(entries) != actual:
        raise generic.GateError("PACKAGE", "manifest-coverage")
    return {"entries": len(entries), "manifest_sha256": digest(manifest), "result": "PASS"}


def validate_science(mutation: str = "") -> dict[str, object]:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    production = subprocess.run(
        [sys.executable, "derive_finite_cell_cartan_transport.py"],
        cwd=HERE,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    independent = subprocess.run(
        [sys.executable, "-s", "verify_finite_cell_cartan_independent.py"],
        cwd=HERE,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if production.returncode or independent.returncode:
        raise AssertionError("science replay")
    result = json.loads(HERE.joinpath("DERIVATION_RESULT.json").read_text())
    verify = json.loads(HERE.joinpath("INDEPENDENT_VERIFICATION.json").read_text())
    if mutation == "complete_branch":
        result["counts"]["complete_onshell_g_phi_branches"] = 1
    statuses = read_tsv(HERE / "STATUS_LEDGER.tsv")
    branches = read_tsv(HERE / "FINITE_CELL_CARTAN_TRANSPORT_ATLAS.tsv")
    cross = read_tsv(HERE / "COMPLETION_CAUSAL_CROSS.tsv")
    blocks = read_tsv(HERE / "CONNECTION_BLOCK_ATLAS.tsv")
    transitions = read_tsv(HERE / "CAUSAL_TRANSITION_ATLAS.tsv")
    premises = read_tsv(HERE / "PREMISE_LEDGER.tsv")
    sources = read_tsv(HERE / "SOURCE_LINEAGE.tsv")
    catches = read_tsv(HERE / "CATCH_PROOFS.tsv")
    source_map = {row["path"]: (row["sha256"], int(row["bytes"])) for row in sources}
    result_sources = {row["path"]: (row["sha256"], int(row["bytes"])) for row in result["source_hashes"]}
    clean = json.loads(HERE.joinpath("CLEAN_ENV_RESULT.json").read_text())
    if (
        result["maximum_conclusion"] != MAXIMUM
        or result["all_checks_pass"] is not True
        or result["check_count"] != 46
        or result["counts"] != {
            "causal_classes": 5,
            "complete_onshell_g_phi_branches": 0,
            "completion_causal_cross": 60,
            "completion_families": 12,
            "connection_domains": 4,
            "transition_witnesses": 8,
        }
        or verify["all_checks_pass"] is not True
        or verify["check_count"] != 26
        or verify["all_catches_pass"] is not True
        or verify["catch_count"] != 22
        or len(statuses) != 36
        or len(branches) != 12
        or len(cross) != 60
        or len({(row["completion_id"], row["causal_class"]) for row in cross}) != 60
        or len(blocks) != 4
        or len(transitions) != 8
        or len(premises) != 18
        or len(sources) != 22
        or source_map != result_sources
        or len(catches) != 22
        or any(row["actual"] != "rejected" for row in catches)
        or digest(HERE / "requirements.txt") != clean["requirements_sha256"]
        or digest(HERE / "CLEAN_ENV_STDOUT.txt") != clean["stdout_sha256"]
        or clean["sympy"] != "1.13.1"
        or "Grade: `VERIFIED-WITH-CAVEATS`" not in (HERE / "AUDIT_REPORT.md").read_text()
    ):
        raise AssertionError("science contract")
    return {
        "grade": "VERIFIED-WITH-CAVEATS",
        "production_checks": 46,
        "independent_checks": 26,
        "independent_catches": 22,
        "completion_families": 12,
        "causal_cross_rows": 60,
        "complete_onshell_branches": 0,
        "sources": 22,
        "statuses": 36,
        "clean_environment": "PASS",
        "result": "PASS",
    }


def reject_science_mutation(generic) -> None:
    try:
        validate_science("complete_branch")
    except AssertionError as exc:
        raise generic.GateError("SCIENCE", "complete-branch-overclaim") from exc


def main() -> None:
    generic = load(
        ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19" / "verify_repository_gates.py",
        "finite_cell_cartan_generic_gate",
    )
    generic.BASE = BASE
    generic.PACKAGE = PACKAGE
    scope = generic.validate_scope(ROOT)
    frozen = generic.validate_frozen(ROOT)
    prior = replay_parent(generic)
    navigation = generic.validate_navigation(ROOT)
    dirty = generic.validate_dirty(ROOT, DIRTY)
    dirty_head = load(
        ROOT / "udt_invariant_xmax_asymptotic_boundary_audit_2026-07-23" / "verify_repository_gates.py",
        "finite_cell_cartan_dirty_head",
    )
    dirty.update(dirty_head.validate_dirty_head(generic))
    tests = validate_tests()
    science = validate_science()
    package = validate_package(generic)
    catches = {
        "scope": generic.expect("SCOPE", lambda: generic.validate_scope(ROOT, "LIVE.md")),
        "frozen": generic.expect("FROZEN", lambda: generic.validate_frozen(ROOT, corrupt=True)),
        "parent": generic.expect("PARENT", lambda: replay_parent(generic, corrupt=True)),
        "current_paths": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, corrupt="current")),
        "frontier": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, corrupt="frontier")),
        "dirty": generic.expect("DIRTY", lambda: generic.validate_dirty(ROOT, DIRTY, corrupt=True)),
        "package": generic.expect("PACKAGE", lambda: validate_package(generic, corrupt=True)),
        "science": generic.expect("SCIENCE", lambda: reject_science_mutation(generic)),
    }
    output = {
        "schema": "udt-finite-cell-Cartan-repository-gates-1.0",
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

#!/usr/bin/env python3
"""Repository gates for the append-only Xmax correction layer."""

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
BASE = "94c6ee3eae92cc67a8e3f370c98e93d75da4d4f8"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
PARENT = "udt_invariant_xmax_asymptotic_boundary_audit_2026-07-23"
PARENT_MANIFEST_SHA256 = (
    "8798461fbd59891c1eff90c36311e38a29a3753dd4066d75360a813a859955c0"
)
MAXIMUM = (
    "XMAX_IS_OWNER_DEFINED_AS_THE_INVARIANT_POSITIONAL_SCALE_OF_THE_UDT_"
    "DILATION_ASYMPTOTE;THE_RECORDED_WRL_BRANCH_DERIVES_R_OVER_X_EQUALS_"
    "ONE_MINUS_EXP_MINUS_TWO_PHI_CONDITIONAL_ON_RESIDUAL_RECENTERING_AND_"
    "THE_ACCEPTED_WALL_REGULARITY_PACKAGE;PANTHEON_OBSERVATION_FAVORS_"
    "THAT_LINEAR_CEILING_OVER_THE_HYPERBOLIC_J1_DISPLAY_BUT_DOES_NOT_"
    "DERIVE_IT;GLOBAL_BRANCH_SELECTION_XMAX_VALUE_AND_NATIVE_MASS_REMAIN_OPEN"
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
        "xmax_correction_parent_gate",
    )
    prior = parent_gate.replay_prior(generic, False)
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
    if len(packages) != 100 or entries != 35:
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
        "returncode": completed.returncode,
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
        HERE / "derive_xmax_dilation_correction.py",
        "xmax_correction_production",
    )
    result = production.build_result()
    recorded = json.loads((HERE / "RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads(
        (HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8")
    )
    statuses = read_tsv(HERE / "STATUS_LEDGER.tsv")
    catches = read_tsv(HERE / "CATCH_PROOFS.tsv")
    sources = read_tsv(HERE / "SOURCE_LINEAGE.tsv")
    regrades = read_tsv(HERE / "PARENT_CLAIM_REGRADE.tsv")
    sne = read_tsv(HERE / "SNE_SOURCE_ADJUDICATION.tsv")
    graph = read_tsv(HERE / "FORMULA_DEPENDENCY_GRAPH.tsv")
    if (
        result["maximum_conclusion"] != MAXIMUM
        or recorded["maximum_conclusion"] != MAXIMUM
        or result["profile"]["wrl_profile"] != "r/X=1-exp(-2phi)"
        or recorded["profile"]["wrl_profile"] != "r/X=1-exp(-2phi)"
        or result["sne"]["derives_profile"] is not False
        or recorded["sne"]["derives_profile"] is not False
        or result["wrl_selector"]["survivor"] != "alpha=1"
        or len(statuses) != 18
        or len(catches) != 20
        or any(row["result"] != "PASS_REJECTED" for row in catches)
        or len(sources) != 23
        or len(regrades) != 16
        or len(sne) != 15
        or any(row["derives_profile"] != "NO" for row in sne)
        or len(graph) != 14
        or independent["all_checks_pass"] is not True
        or independent["check_count"] != 80
        or independent["catch_pass_count"] != 12
        or independent["grade"] != "VERIFIED-WITH-CAVEATS"
    ):
        raise AssertionError("science contract")
    return {
        "grade": "VERIFIED-WITH-CAVEATS",
        "sources": len(sources),
        "statuses": len(statuses),
        "production_catches": len(catches),
        "independent_checks": independent["check_count"],
        "independent_catches": independent["catch_pass_count"],
        "sne_sources": len(sne),
        "parent_regrades": len(regrades),
        "result": "PASS",
    }


def main() -> None:
    generic = load(
        ROOT
        / "bootstrap_csn_phi_angular_selector_2026-07-19"
        / "verify_repository_gates.py",
        "xmax_correction_generic_gate",
    )
    generic.BASE = BASE
    generic.PACKAGE = PACKAGE

    scope = generic.validate_scope(ROOT)
    frozen = generic.validate_frozen(ROOT)
    prior = replay_parent(generic)
    navigation = generic.validate_navigation(ROOT)
    dirty = generic.validate_dirty(ROOT, DIRTY)
    dirty.update(
        load(
            ROOT / PARENT / "verify_repository_gates.py",
            "xmax_correction_parent_head",
        ).validate_dirty_head(generic)
    )
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
        "schema": "udt-xmax-dilation-asymptote-repository-gates-1.0",
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

#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "df49e148dcf38d2ee1edeca0f1c0a67e7b0f27e2"
PACKAGE = "udt_founded_constraint_atlas_p03_2026-07-21"
P02 = ROOT / "udt_local_jet_atlas_p02_2026-07-21"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
P02_MANIFEST = "c56390eb26b80c54a3c3a09f4800086c8dbc00b5bfd40b2038e264e85bec8938"
P02_TREE = "1321107a72020019c421521732a0248e627e07eec77b70bdf64be71bc068b436"
P02_RESULT = "154c264b435004274841a144eb9ad1b853aa441628eb2b4706a6682d0a3496db"
P02_VERIFY = "9ff3a06b28397386d53a2c5f5bca0eccbfb2abe22efa3ef0dd92b76aaa6c9bde"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def scope(generic, inject=None):
    changed = set(str(generic.git(ROOT, "diff", "--name-only", BASE)).splitlines())
    changed.update(str(generic.git(ROOT, "ls-files", "--others", "--exclude-standard")).splitlines())
    if inject:
        changed.add(inject)
    bad = sorted(path for path in changed if path and not path.startswith(PACKAGE + "/"))
    if bad:
        raise generic.GateError("SCOPE", bad[0])
    return sorted(changed)


def constraint_verification():
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["CUDA_VISIBLE_DEVICES"] = ""
    main = subprocess.run(
        [sys.executable, "-B", str(HERE / "build_p03_constraint_atlas.py")],
        cwd=ROOT, env=environment, text=True, capture_output=True, timeout=300, check=False,
    )
    if main.returncode or main.stderr:
        raise AssertionError(main.stdout + main.stderr)
    independent = subprocess.run(
        [sys.executable, "-B", str(HERE / "verify_p03_constraint_atlas.py")],
        cwd=ROOT, env=environment, text=True, capture_output=True, timeout=300, check=False,
    )
    if independent.returncode or independent.stderr:
        raise AssertionError(independent.stdout + independent.stderr)
    result = json.loads((HERE / "ATLAS_RESULT.json").read_text(encoding="utf-8"))
    verification = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    if (
        result["status"] != "PASS"
        or result["check_count"] != 20
        or result["counts"]["P02_discrete_strata_accounted"] != 89
        or result["constraint_ruling"]["unconditional_point_local_metric_strata_removed"] != 0
        or verification["status"] != "PASS"
        or verification["check_count"] != 10
        or verification["catch_proof_count"] != 34
        or result["maximum_conclusion"]
        != "CURRENT_FOUNDATION_CONSTRAINED_CONFIGURATION_SPACE_CHARACTERIZED"
    ):
        raise AssertionError("P03 constraint verification")
    review = (HERE / "EXTERNAL_ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8")
    if review.strip().splitlines()[-1] != "`PASS_WITH_CAVEATS`" or "All 36 premise treatments" not in review:
        raise AssertionError("external review")
    return {
        "status": "PASS",
        "main_checks": result["check_count"],
        "independent_checks": verification["check_count"],
        "catch_proofs": verification["catch_proof_count"],
        "external_review": "PASS_WITH_CAVEATS_BANKING_GATES_THEN_CLOSED",
        "main_result_sha256": digest(HERE / "ATLAS_RESULT.json"),
        "verification_result_sha256": digest(HERE / "VERIFICATION_RESULT.json"),
        "maximum_conclusion": result["maximum_conclusion"],
    }


def p02_immutability():
    if digest(P02 / "SHA256SUMS.txt") != P02_MANIFEST:
        raise AssertionError("P02 manifest")
    if digest(P02 / "ATLAS_RESULT.json") != P02_RESULT or digest(P02 / "VERIFICATION_RESULT.json") != P02_VERIFY:
        raise AssertionError("P02 result")
    listing = subprocess.run(
        ["git", "ls-tree", "-r", BASE, str(P02.relative_to(ROOT))],
        cwd=ROOT, text=True, capture_output=True, check=True,
    ).stdout
    if hashlib.sha256(listing.encode()).hexdigest() != P02_TREE:
        raise AssertionError("P02 committed tree")
    if subprocess.run(
        ["git", "diff", "--quiet", BASE, "--", str(P02.relative_to(ROOT))],
        cwd=ROOT, check=False,
    ).returncode:
        raise AssertionError("P02 working-tree change")
    return {"status": "PASS", "manifest_sha256": P02_MANIFEST, "tree_sha256": P02_TREE, "entries": 33}


def prior_packages():
    record = json.loads((P02 / "REPOSITORY_GATES.json").read_text(encoding="utf-8"))
    prior = {
        row["package"]: row["manifest_sha256"]
        for row in record["prior_scientific_packages"]["packages"]
    }
    prior["udt_local_jet_atlas_p02_2026-07-21"] = P02_MANIFEST
    return prior


def main():
    generic = load(
        ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19/verify_repository_gates.py",
        "p03_generic_gates",
    )
    generic.BASE = BASE
    generic.PACKAGE = PACKAGE

    changed = scope(generic)
    atlas = constraint_verification()
    p02 = p02_immutability()
    frozen = generic.validate_frozen(ROOT)
    prior = prior_packages()
    replay = generic.replay_packages(ROOT, prior, "PRIOR")
    if len(prior) != 54 or replay["entries"] != 1301:
        raise generic.GateError("PRIOR", f"{len(prior)}:{replay['entries']}")
    navigation = generic.validate_navigation(ROOT)
    dirty = generic.validate_dirty(ROOT, DIRTY)
    tests = generic.validate_tests(ROOT)
    package = generic.validate_package_manifest(ROOT)
    catches = {
        "scope": generic.expect("SCOPE", lambda: scope(generic, "CANON.md")),
        "frozen": generic.expect("FROZEN", lambda: generic.validate_frozen(ROOT, True)),
        "prior": generic.expect("PRIOR", lambda: generic.replay_packages(ROOT, prior, "PRIOR", True)),
        "current": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, "current")),
        "frontier": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, "frontier")),
        "dirty": generic.expect("DIRTY", lambda: generic.validate_dirty(ROOT, DIRTY, True)),
        "package": generic.expect("PACKAGE", lambda: generic.validate_package_manifest(ROOT, True)),
    }
    output = {
        "schema": "udt-p03-founded-constraint-atlas-repository-gates-1.0",
        "base": BASE,
        "result": "PASS",
        "scope_paths": changed,
        "constraint_atlas_verifier": atlas,
        "P02_immutability": p02,
        "frozen": frozen,
        "prior_scientific_packages": replay,
        "navigation": navigation,
        "dirty_checkout": dirty,
        "tests": tests,
        "package_manifest": package,
        "catch_proofs": catches,
        "compute": {"cpu_only": True, "gpu_work_performed": False, "ODE_or_PDE_run": False},
        "authority_boundary": {
            "startup_controls_changed": False,
            "canon_changed": False,
            "native_dynamics_selected": False,
            "action_or_equation_loaded": False,
            "carrier_or_matter_adopted": False,
            "repository_reorganization_performed": False,
            "P04_launched": False,
        },
    }
    (HERE / "REPOSITORY_GATES.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("repository_gates=PASS")
    print(f"P03={atlas['main_checks']} main/{atlas['independent_checks']} independent/{atlas['catch_proofs']} catches")
    print(f"P02_manifest={p02['manifest_sha256']} tree={p02['tree_sha256']}")
    print(f"frozen_manifests=6 entries={frozen['entries']} paths={frozen['tracked_paths']}")
    print(f"prior_packages={len(prior)} entries={replay['entries']}")
    print(f"tests={tests['passed']} passed/{tests['failed']} known failed/{tests['xfailed']} xfailed")
    print(f"dirty_metadata_paths={dirty['paths']} hash={dirty['metadata_sha256']}")
    print(f"package_manifest={package['sha256']} entries={package['entries']}")


if __name__ == "__main__":
    main()

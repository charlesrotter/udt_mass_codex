#!/usr/bin/env python3
from __future__ import annotations

import csv
import importlib.util
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "ec8250935d74a2218f31a09f5611bd0e5e4f40e0"
PACKAGE = "udt_reciprocal_plane_projector_audit_2026-07-21"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
COMPLETE_SEAL_MANIFEST = "3a6cc83e40fe95951b19f37b68b1167a3683cf4f02c0fbf1f52f54d95db99b66"


def rows(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
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


def science():
    derivation = subprocess.run(
        [sys.executable, str(HERE / "derive_reciprocal_plane_projector.py")],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if derivation.returncode:
        raise AssertionError(derivation.stdout.decode("utf-8", "replace"))
    verification = subprocess.run(
        [sys.executable, str(HERE / "verify_reciprocal_plane_projector.py")],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if verification.returncode:
        raise AssertionError(verification.stdout.decode("utf-8", "replace"))
    result = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    if (
        result["result"] != "PASS_VERIFIED_WITH_CAVEATS"
        or result["derivation_check_count"] != 102
        or result["independent_check_count"] != 50
        or result["catch_proof_count"] != 24
    ):
        raise AssertionError("science")
    return {
        "result": result["result"],
        "derivation_checks": result["derivation_check_count"],
        "independent_checks": result["independent_check_count"],
        "catch_proofs": result["catch_proof_count"],
    }


def main():
    generic = load(
        ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19/verify_repository_gates.py",
        "projector_generic_gates",
    )
    failed_wrapper = load(
        ROOT / "c2_failed_basin_homotopy_2026-07-20/verify_repository_gates.py",
        "projector_failed_wrapper",
    )
    parent = load(
        ROOT / "udt_complete_seal_fixed_set_selector_audit_2026-07-21/verify_repository_gates.py",
        "projector_parent_gates",
    )
    generic.BASE = BASE
    generic.PACKAGE = PACKAGE
    universe = rows(ROOT / "udt_premise_reset_audit_2026-07-19/PACKAGE_UNIVERSE.tsv")
    prior = {row["package"]: row["manifest_sha256"] for row in universe}
    prior.update(failed_wrapper.ADD)
    prior["c2_failed_basin_homotopy_2026-07-20"] = parent.FAILED_BASIN_MANIFEST
    prior["c2_open_path_checkpoint_continuation_2026-07-20"] = parent.OPEN_PATH_MANIFEST
    prior["c2_reciprocal_transverse_twist_jacobi_2026-07-20"] = parent.TWIST_PARENT_MANIFEST
    prior["c2_coupled_reciprocal_twist_onshell_2026-07-20"] = parent.COUPLED_PARENT_MANIFEST
    prior["c2_intrinsic_angular_product_selector_2026-07-20"] = parent.INTRINSIC_PARENT_MANIFEST
    prior["c2_transverse_coframe_closure_2026-07-20"] = parent.TRANSVERSE_PARENT_MANIFEST
    prior["udt_global_reciprocal_closure_audit_2026-07-20"] = parent.GLOBAL_CLOSURE_PARENT_MANIFEST
    prior["udt_global_coframe_cocycle_audit_2026-07-20"] = parent.COFRAME_COCYCLE_PARENT_MANIFEST
    prior["udt_mixed_readout_anchor_soldering_audit_2026-07-20"] = parent.ANCHOR_SOLDERING_PARENT_MANIFEST
    prior["udt_clock_ruler_soldering_selector_audit_2026-07-20"] = parent.SEAL_SOLDERING_PARENT_MANIFEST
    prior["udt_complete_lift_mu_closure_audit_2026-07-20"] = parent.COMPLETE_LIFT_PARENT_MANIFEST
    prior["udt_time_extendability_constraint_audit_2026-07-20"] = parent.TIME_EXTENDABILITY_MANIFEST
    prior["udt_gr_subtraction_reciprocal_connection_audit_2026-07-21"] = parent.RECIPROCAL_CONNECTION_MANIFEST
    prior["udt_metric_native_two_pair_selector_audit_2026-07-21"] = parent.METRIC_TWO_PAIR_MANIFEST
    prior["udt_complete_seal_fixed_set_selector_audit_2026-07-21"] = COMPLETE_SEAL_MANIFEST

    changed = scope(generic)
    scientific = science()
    frozen = generic.validate_frozen(ROOT)
    replay = generic.replay_packages(ROOT, prior, "PRIOR")
    if len(prior) != 50 or replay["entries"] != 1199:
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
        "schema": "udt-reciprocal-plane-projector-repository-gates-1.0",
        "base": BASE,
        "result": "PASS",
        "scope_paths": changed,
        "science_verifier": scientific,
        "frozen": frozen,
        "prior_scientific_packages": replay,
        "navigation": navigation,
        "dirty_checkout": dirty,
        "tests": tests,
        "package_manifest": package,
        "catch_proofs": catches,
        "compute": {"cpu_only": True, "gpu_work_performed": False},
        "authority_boundary": {
            "startup_controls_changed": False,
            "canon_changed": False,
            "spacetime_reciprocal_plane_derived": False,
            "projector_parallelism_adopted": False,
            "integrable_umbilical_complete_metric_derived": False,
            "second_reciprocal_pair_or_Hopf_axis_selected": False,
            "action_boundary_charge_source_or_mass_derived": False,
            "external_model_review_performed": False,
            "repository_reorganization_performed": False,
        },
    }
    (HERE / "REPOSITORY_GATES.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("repository_gates=PASS")
    print(f"frozen_manifests=6 entries={frozen['entries']} paths={frozen['tracked_paths']}")
    print(f"prior_packages={len(prior)} entries={replay['entries']}")
    print(f"tests={tests['passed']} passed/{tests['failed']} known failed/{tests['xfailed']} xfailed")
    print(f"dirty_metadata_paths={dirty['paths']} hash={dirty['metadata_sha256']}")
    print(f"package_manifest={package['sha256']} entries={package['entries']}")


if __name__ == "__main__":
    main()

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
BASE = "0167b90438fbc13679b7a043066ab990ea54aa98"
PACKAGE = "udt_local_jet_atlas_p02_2026-07-21"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
COMPLETE_SEAL_MANIFEST = "3a6cc83e40fe95951b19f37b68b1167a3683cf4f02c0fbf1f52f54d95db99b66"
PROJECTOR_MANIFEST = "7d14a1cfda1135e3f34af48796d0ea3ea46930f2c94a1fb6ef80d2006c042ee6"
COMPLETE_MAP_MANIFEST = "1778e4dcfcf9ac0bd3574fb3ff5248f2990265fa40d0822ff964ac67c434ae38"
P01_MANIFEST = "b7d8917cb27627c7ad7767fcffbd5b5d7a9dc6da2171b2d8fba329d04014ffad"
ATLAS_SHA256 = "154c264b435004274841a144eb9ad1b853aa441628eb2b4706a6682d0a3496db"
VERIFY_SHA256 = "9ff3a06b28397386d53a2c5f5bca0eccbfb2abe22efa3ef0dd92b76aaa6c9bde"


def rows(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


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


def atlas_verification():
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["CUDA_VISIBLE_DEVICES"] = ""
    main = subprocess.run(
        [sys.executable, "-B", str(HERE / "run_p02_local_jet_atlas.py")],
        cwd=ROOT,
        env=environment,
        text=True,
        capture_output=True,
        timeout=600,
        check=False,
    )
    if main.returncode or main.stderr:
        raise AssertionError(main.stdout + main.stderr)
    independent = subprocess.run(
        [sys.executable, "-B", str(HERE / "verify_p02_local_jet_atlas.py")],
        cwd=ROOT,
        env=environment,
        text=True,
        capture_output=True,
        timeout=600,
        check=False,
    )
    if independent.returncode or independent.stderr:
        raise AssertionError(independent.stdout + independent.stderr)

    result = json.loads((HERE / "ATLAS_RESULT.json").read_text(encoding="utf-8"))
    verification = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    expected_counts = {
        "metric_inertia_strata": 15,
        "supplied_split_inertia_strata": 36,
        "dphi_strata": 8,
        "split_first_jet_rank_strata": 12,
        "curvature_operator_rank_strata": 7,
        "Ricci_rank_strata": 5,
        "Petrov_types": 6,
        "second_jet_direct_sum_basis": 20,
        "discrete_registered_strata_total": 89,
    }
    if (
        result["status"] != "PASS"
        or result["counts"] != expected_counts
        or result["check_count"] != 21
        or result["maximum_raw_residual"] >= 2e-10
        or verification["status"] != "PASS"
        or verification["check_count"] != 9
        or verification["catch_proof_count"] != 31
        or result["maximum_conclusion"]
        != "LOCAL_KINEMATIC_SOLUTION_SPACE_CHARACTERIZED_WITHOUT_DYNAMICS"
    ):
        raise AssertionError("P02 atlas verification")
    if digest(HERE / "ATLAS_RESULT.json") != ATLAS_SHA256 or digest(HERE / "ATLAS_TRANSCRIPT.txt") != ATLAS_SHA256:
        raise AssertionError("atlas hash")
    if digest(HERE / "VERIFICATION_RESULT.json") != VERIFY_SHA256 or digest(HERE / "VERIFICATION_TRANSCRIPT.txt") != VERIFY_SHA256:
        raise AssertionError("verification hash")

    external = (HERE / "EXTERNAL_ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8")
    if external.strip().splitlines()[-1] != "PASS" or "full 20D algebraic-curvature space" not in external:
        raise AssertionError("external review")
    api = json.loads((HERE / "API_SCHEMA.json").read_text(encoding="utf-8"))
    if api["schema"] != "udt-p02-local-jet-atlas-api-1.0" or len(api["second_jet_axes"]) != 5:
        raise AssertionError("API schema")
    formulae = (HERE / "FORMULAE_AND_CONVENTIONS.md").read_text(encoding="utf-8")
    for phrase in (
        "conditional bookkeeping",
        "representative selection and not an EH",
        "No quantity is set to zero by an EOM",
    ):
        if phrase not in formulae:
            raise AssertionError("formula scope")
    return {
        "status": "PASS",
        "main_checks": result["check_count"],
        "independent_checks": verification["check_count"],
        "catch_proofs": verification["catch_proof_count"],
        "maximum_raw_residual": result["maximum_raw_residual"],
        "external_review": "PASS",
        "maximum_conclusion": result["maximum_conclusion"],
    }


def main():
    generic = load(
        ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19/verify_repository_gates.py",
        "p02_generic_gates",
    )
    failed_wrapper = load(
        ROOT / "c2_failed_basin_homotopy_2026-07-20/verify_repository_gates.py",
        "p02_failed_wrapper",
    )
    parent = load(
        ROOT / "udt_complete_seal_fixed_set_selector_audit_2026-07-21/verify_repository_gates.py",
        "p02_parent_gates",
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
    prior["udt_reciprocal_plane_projector_audit_2026-07-21"] = PROJECTOR_MANIFEST
    prior["udt_complete_metric_solution_space_map_2026-07-21"] = COMPLETE_MAP_MANIFEST
    prior["udt_canonical_geometry_evaluator_p01_2026-07-21"] = P01_MANIFEST

    changed = scope(generic)
    atlas = atlas_verification()
    frozen = generic.validate_frozen(ROOT)
    replay = generic.replay_packages(ROOT, prior, "PRIOR")
    if len(prior) != 53 or replay["entries"] != 1268:
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
        "schema": "udt-p02-local-jet-atlas-repository-gates-1.0",
        "base": BASE,
        "result": "PASS",
        "scope_paths": changed,
        "atlas_verifier": atlas,
        "frozen": frozen,
        "prior_scientific_packages": replay,
        "navigation": navigation,
        "dirty_checkout": dirty,
        "tests": tests,
        "package_manifest": package,
        "catch_proofs": catches,
        "compute": {"cpu_only": True, "gpu_work_performed": False, "scientific_EOM_solved": False},
        "authority_boundary": {
            "startup_controls_changed": False,
            "canon_changed": False,
            "founded_constraints_applied": False,
            "native_dynamics_selected": False,
            "ODE_or_PDE_run": False,
            "carrier_or_matter_adopted": False,
            "repository_reorganization_performed": False,
            "P03_launched": False,
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

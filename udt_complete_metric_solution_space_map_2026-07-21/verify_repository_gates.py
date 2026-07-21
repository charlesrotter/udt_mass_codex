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
BASE = "fa3d3afda98b2516e58b83a4f383190df9a0aa68"
PACKAGE = "udt_complete_metric_solution_space_map_2026-07-21"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
COMPLETE_SEAL_MANIFEST = "3a6cc83e40fe95951b19f37b68b1167a3683cf4f02c0fbf1f52f54d95db99b66"
PROJECTOR_MANIFEST = "7d14a1cfda1135e3f34af48796d0ea3ea46930f2c94a1fb6ef80d2006c042ee6"


def rows(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


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


def map_verification():
    run = subprocess.run(
        [
            sys.executable,
            str(HERE / "verify_complete_metric_solution_space_map.py"),
            "--output",
            str(HERE / "VERIFICATION_RESULT.json"),
            "--transcript",
            str(HERE / "VERIFICATION_TRANSCRIPT.txt"),
        ],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if run.returncode:
        raise AssertionError(run.stdout.decode("utf-8", "replace"))
    result = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    counts = result["counts"]
    if (
        result["status"] != "PASS"
        or result["scientific_solve_executed"] is not False
        or result["maximum_conclusion"] != "EXECUTION_PLAN_READY_FOR_OWNER_REVIEW"
        or counts["metric_slots"] != 10
        or counts["stages"] != 14
        or counts["completeness_criteria"] != 10
        or counts["catch_proofs"] != 18
    ):
        raise AssertionError("map verification")
    return {
        "status": result["status"],
        "metric_slots": counts["metric_slots"],
        "stages": counts["stages"],
        "completeness_criteria": counts["completeness_criteria"],
        "catch_proofs": counts["catch_proofs"],
        "scientific_solve_executed": False,
    }


def main():
    generic = load(
        ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19/verify_repository_gates.py",
        "complete_map_generic_gates",
    )
    failed_wrapper = load(
        ROOT / "c2_failed_basin_homotopy_2026-07-20/verify_repository_gates.py",
        "complete_map_failed_wrapper",
    )
    parent = load(
        ROOT / "udt_complete_seal_fixed_set_selector_audit_2026-07-21/verify_repository_gates.py",
        "complete_map_parent_gates",
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

    changed = scope(generic)
    map_result = map_verification()
    frozen = generic.validate_frozen(ROOT)
    replay = generic.replay_packages(ROOT, prior, "PRIOR")
    if len(prior) != 51 or replay["entries"] != 1219:
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
        "schema": "udt-complete-metric-solution-space-map-repository-gates-1.0",
        "base": BASE,
        "result": "PASS",
        "scope_paths": changed,
        "map_verifier": map_result,
        "frozen": frozen,
        "prior_scientific_packages": replay,
        "navigation": navigation,
        "dirty_checkout": dirty,
        "tests": tests,
        "package_manifest": package,
        "catch_proofs": catches,
        "compute": {"cpu_only": True, "gpu_work_performed": False, "scientific_solve_executed": False},
        "authority_boundary": {
            "startup_controls_changed": False,
            "canon_changed": False,
            "native_dynamics_selected": False,
            "solution_space_explored": False,
            "ode_or_pde_run": False,
            "carrier_or_matter_adopted": False,
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

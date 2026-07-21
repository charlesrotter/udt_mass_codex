#!/usr/bin/env python3
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
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "7476fe32643e0e987982a4ba979aa5a4970e5858"
PACKAGE = "udt_canonical_geometry_evaluator_p01_2026-07-21"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
COMPLETE_SEAL_MANIFEST = "3a6cc83e40fe95951b19f37b68b1167a3683cf4f02c0fbf1f52f54d95db99b66"
PROJECTOR_MANIFEST = "7d14a1cfda1135e3f34af48796d0ea3ea46930f2c94a1fb6ef80d2006c042ee6"
COMPLETE_MAP_MANIFEST = "1778e4dcfcf9ac0bd3574fb3ff5248f2990265fa40d0822ff964ac67c434ae38"
MAIN_SHA256 = "a2bfefe3f22c4ca18e33301baad64e45e660dc631ea0a9627e13c670b6735734"
VERIFY_SHA256 = "073213581a4ac2021ab4b6d63c64a56df29f7621d3fde8d927d6d2fe982294e0"


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


def validate_navigation(generic, corrupt=None):
    current = rows(ROOT / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv")
    current_paths = [row["current_path"] for row in current]
    if corrupt == "current":
        current_paths = current_paths[:-1]
    if len(current) != 1114 or len(current_paths) != 1114 or len(set(current_paths)) != 1114:
        raise generic.GateError("NAVIGATION", "current-count")
    if not all((ROOT / path).exists() for path in current_paths):
        raise generic.GateError("NAVIGATION", "current-target")

    frontier = rows(ROOT / "research/_registry/CURRENT_FRONTIER_TARGETS.tsv")
    targets = {row["target_path"].rstrip("/") for row in frontier}
    if corrupt == "frontier":
        targets.pop()
    if len(frontier) != 306 or len(targets) != 101:
        raise generic.GateError("NAVIGATION", "frontier-count")
    if not all((ROOT / path).exists() for path in targets):
        raise generic.GateError("NAVIGATION", "frontier-target")

    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    links = []
    for source in sorted(HERE.glob("*.md")):
        for raw in link_pattern.findall(source.read_text(encoding="utf-8")):
            target = raw.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            if target.startswith("/"):
                target = re.sub(r":\d+$", "", target)
                links.append(Path(target))
            else:
                links.append(source.parent.joinpath(target).resolve())
    if not all(path.exists() for path in links):
        raise generic.GateError("NAVIGATION", "markdown-link")
    return {
        "current_paths": len(current),
        "frontier_rows": len(frontier),
        "frontier_targets": len(targets),
        "package_links": len(links),
    }


def evaluator_verification():
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["CUDA_VISIBLE_DEVICES"] = ""
    main = subprocess.run(
        [sys.executable, "-B", str(HERE / "run_p01_evaluator.py")],
        cwd=ROOT,
        env=environment,
        text=True,
        capture_output=True,
        timeout=120,
        check=False,
    )
    if main.returncode or main.stderr:
        raise AssertionError(main.stdout + main.stderr)
    independent = subprocess.run(
        [sys.executable, "-B", str(HERE / "verify_p01_evaluator.py")],
        cwd=ROOT,
        env=environment,
        text=True,
        capture_output=True,
        timeout=120,
        check=False,
    )
    if independent.returncode or independent.stderr:
        raise AssertionError(independent.stdout + independent.stderr)

    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    verification = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    if (
        result["status"] != "PASS"
        or result["check_count"] != 36
        or result["maximum_raw_residual"] >= 2e-10
        or verification["status"] != "PASS"
        or verification["check_count"] != 15
        or verification["catch_proof_count"] != 33
        or verification["maximum_independent_residual"] >= 2e-10
        or result["maximum_conclusion"]
        != "GEOMETRY_EVALUATOR_VERIFIED_NOT_SOLUTION_SPACE_EXPLORED"
    ):
        raise AssertionError("P01 evaluator verification")
    if digest(HERE / "DERIVATION_RESULT.json") != MAIN_SHA256:
        raise AssertionError("main result hash")
    if digest(HERE / "DERIVATION_TRANSCRIPT.txt") != MAIN_SHA256:
        raise AssertionError("main transcript hash")
    if digest(HERE / "VERIFICATION_RESULT.json") != VERIFY_SHA256:
        raise AssertionError("independent result hash")
    if digest(HERE / "VERIFICATION_TRANSCRIPT.txt") != VERIFY_SHA256:
        raise AssertionError("independent transcript hash")

    initial = (HERE / "EXTERNAL_ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8")
    final = (HERE / "EXTERNAL_ADVERSARIAL_REVIEW_FINAL.md").read_text(encoding="utf-8")
    adjudication = (HERE / "EXTERNAL_REVIEW_ADJUDICATION.md").read_text(encoding="utf-8")
    if "FAIL_BLOCKING" not in initial or "PREREGISTRATION.md" not in initial:
        raise AssertionError("historical external review")
    if final.strip().splitlines()[-1] != "PASS" or "No blocking defect" not in final:
        raise AssertionError("final external review")
    if "initial `FAIL_BLOCKING` is preserved" not in adjudication:
        raise AssertionError("external-review adjudication")
    return {
        "status": "PASS",
        "main_checks": result["check_count"],
        "main_maximum_raw_residual": result["maximum_raw_residual"],
        "independent_checks": verification["check_count"],
        "catch_proofs": verification["catch_proof_count"],
        "maximum_independent_residual": verification["maximum_independent_residual"],
        "external_review": "PASS",
        "maximum_conclusion": result["maximum_conclusion"],
    }


def main():
    generic = load(
        ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19/verify_repository_gates.py",
        "p01_generic_gates",
    )
    failed_wrapper = load(
        ROOT / "c2_failed_basin_homotopy_2026-07-20/verify_repository_gates.py",
        "p01_failed_wrapper",
    )
    parent = load(
        ROOT / "udt_complete_seal_fixed_set_selector_audit_2026-07-21/verify_repository_gates.py",
        "p01_parent_gates",
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

    changed = scope(generic)
    evaluator = evaluator_verification()
    frozen = generic.validate_frozen(ROOT)
    replay = generic.replay_packages(ROOT, prior, "PRIOR")
    if len(prior) != 52 or replay["entries"] != 1244:
        raise generic.GateError("PRIOR", f"{len(prior)}:{replay['entries']}")
    navigation = validate_navigation(generic)
    dirty = generic.validate_dirty(ROOT, DIRTY)
    tests = generic.validate_tests(ROOT)
    package = generic.validate_package_manifest(ROOT)
    catches = {
        "scope": generic.expect("SCOPE", lambda: scope(generic, "CANON.md")),
        "frozen": generic.expect("FROZEN", lambda: generic.validate_frozen(ROOT, True)),
        "prior": generic.expect("PRIOR", lambda: generic.replay_packages(ROOT, prior, "PRIOR", True)),
        "current": generic.expect("NAVIGATION", lambda: validate_navigation(generic, "current")),
        "frontier": generic.expect("NAVIGATION", lambda: validate_navigation(generic, "frontier")),
        "dirty": generic.expect("DIRTY", lambda: generic.validate_dirty(ROOT, DIRTY, True)),
        "package": generic.expect("PACKAGE", lambda: generic.validate_package_manifest(ROOT, True)),
    }
    output = {
        "schema": "udt-p01-canonical-geometry-repository-gates-1.0",
        "base": BASE,
        "result": "PASS",
        "scope_paths": changed,
        "evaluator_verifier": evaluator,
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
            "repository_reorganization_performed": False,
            "P02_launched": False,
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

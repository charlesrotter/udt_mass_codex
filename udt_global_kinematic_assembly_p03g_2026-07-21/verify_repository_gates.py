#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "c89708eec3e415e4f0a052d93c02ab4ad1088512"
PACKAGE = "udt_global_kinematic_assembly_p03g_2026-07-21"
P03 = ROOT / "udt_founded_constraint_atlas_p03_2026-07-21"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
P03_MANIFEST = "b0ec5cbb2be404084e1b1ed4eca98d53c9712a62cf1af0a48eb340b64467c3be"

PARENTS = {
    "udt_canonical_geometry_evaluator_p01_2026-07-21": "b7d8917cb27627c7ad7767fcffbd5b5d7a9dc6da2171b2d8fba329d04014ffad",
    "udt_local_jet_atlas_p02_2026-07-21": "c56390eb26b80c54a3c3a09f4800086c8dbc00b5bfd40b2038e264e85bec8938",
    "udt_founded_constraint_atlas_p03_2026-07-21": P03_MANIFEST,
    "udt_complete_metric_solution_space_map_2026-07-21": "1778e4dcfcf9ac0bd3574fb3ff5248f2990265fa40d0822ff964ac67c434ae38",
    "udt_global_coframe_cocycle_audit_2026-07-20": "1297e8f6773f863f426d66f6c4915741a742c1ee13230abf2b066421de49b04b",
    "finite_cell_seal_boundary_phase_join_2026-07-20": "704b084548a212eabcfb1ac051e89234a7fd91bbeaf7f70abcc28bf63edc7a3b",
    "udt_complete_seal_fixed_set_selector_audit_2026-07-21": "3a6cc83e40fe95951b19f37b68b1167a3683cf4f02c0fbf1f52f54d95db99b66",
}


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


def assembly_verification():
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["CUDA_VISIBLE_DEVICES"] = ""
    main = subprocess.run([sys.executable, "-B", str(HERE / "build_p03g_global_assembly.py")], cwd=ROOT, env=environment, text=True, capture_output=True, timeout=300, check=False)
    if main.returncode or main.stderr:
        raise AssertionError(main.stdout + main.stderr)
    independent = subprocess.run([sys.executable, "-B", str(HERE / "verify_p03g_global_assembly.py")], cwd=ROOT, env=environment, text=True, capture_output=True, timeout=300, check=False)
    if independent.returncode or independent.stderr:
        raise AssertionError(independent.stdout + independent.stderr)
    result = json.loads((HERE / "ASSEMBLY_RESULT.json").read_text(encoding="utf-8"))
    verification = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    if (
        result["status"] != "PASS"
        or result["check_count"] != 25
        or result["counts"]["preregistered_axes"] != 12
        or result["counts"]["local_realization_branches_retained"] != 7
        or result["counts"]["selected_global_branches"] != 0
        or result["evidence_grade"] != "LEAD_INDEPENDENT_REPLAY_FRESH_ADVERSARIAL_OPEN"
        or verification["status"] != "PASS"
        or verification["check_count"] != 8
        or verification["catch_proof_count"] != 24
        or result["maximum_conclusion"] != "CURRENT_GLOBAL_KINEMATIC_ASSEMBLY_CONDITIONS_AND_OPEN_BRANCHES_CHARACTERIZED"
    ):
        raise AssertionError("P03G assembly verification")
    review = (HERE / "EXTERNAL_ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8")
    if "Status: `NOT_COMPLETED`" not in review or "fresh adversarial-context gate: `OPEN`" not in review:
        raise AssertionError("fresh review status")
    return {
        "status": "PASS",
        "main_checks": result["check_count"],
        "independent_checks": verification["check_count"],
        "catch_proofs": verification["catch_proof_count"],
        "fresh_adversarial_review": "OPEN_NO_REVIEW_RETURNED",
        "evidence_grade": result["evidence_grade"],
        "main_result_sha256": digest(HERE / "ASSEMBLY_RESULT.json"),
        "verification_result_sha256": digest(HERE / "VERIFICATION_RESULT.json"),
        "maximum_conclusion": result["maximum_conclusion"],
    }


def parent_immutability():
    observed = {}
    for package, expected in PARENTS.items():
        value = digest(ROOT / package / "SHA256SUMS.txt")
        if value != expected:
            raise AssertionError(f"parent manifest: {package}")
        if subprocess.run(["git", "diff", "--quiet", BASE, "--", package], cwd=ROOT, check=False).returncode:
            raise AssertionError(f"parent working-tree change: {package}")
        observed[package] = value
    return {"status": "PASS", "packages": observed, "count": len(observed)}


def prior_packages():
    record = json.loads((P03 / "REPOSITORY_GATES.json").read_text(encoding="utf-8"))
    prior = {row["package"]: row["manifest_sha256"] for row in record["prior_scientific_packages"]["packages"]}
    prior["udt_founded_constraint_atlas_p03_2026-07-21"] = P03_MANIFEST
    return prior


def main():
    generic = load(ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19/verify_repository_gates.py", "p03g_generic_gates")
    generic.BASE = BASE
    generic.PACKAGE = PACKAGE

    changed = scope(generic)
    assembly = assembly_verification()
    parents = parent_immutability()
    frozen = generic.validate_frozen(ROOT)
    prior = prior_packages()
    replay = generic.replay_packages(ROOT, prior, "PRIOR")
    if len(prior) != 55 or replay["entries"] != 1331:
        raise generic.GateError("PRIOR", f"{len(prior)}:{replay['entries']}")
    navigation = generic.validate_navigation(ROOT)
    dirty = generic.validate_dirty(ROOT, DIRTY)
    tests = generic.validate_tests(ROOT)
    # Pytest's summary embeds elapsed wall time, so its raw stdout hash changes on every clean replay.
    # Certify the stable baseline tuple instead; the complete raw run is still emitted by pytest when
    # the gate fails and is not a load-bearing scientific artifact here.
    tests.pop("stdout_sha256", None)
    stable_test_signature = f"{tests['passed']}|{tests['failed']}|{tests['xfailed']}|{tests['failure']}"
    tests["result_signature_sha256"] = hashlib.sha256(stable_test_signature.encode("utf-8")).hexdigest()
    package = generic.validate_package_manifest(ROOT)
    catches = {
        "scope": generic.expect("SCOPE", lambda: scope(generic, "LIVE.md")),
        "frozen": generic.expect("FROZEN", lambda: generic.validate_frozen(ROOT, True)),
        "prior": generic.expect("PRIOR", lambda: generic.replay_packages(ROOT, prior, "PRIOR", True)),
        "current": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, "current")),
        "frontier": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, "frontier")),
        "dirty": generic.expect("DIRTY", lambda: generic.validate_dirty(ROOT, DIRTY, True)),
        "package": generic.expect("PACKAGE", lambda: generic.validate_package_manifest(ROOT, True)),
    }
    output = {
        "schema": "udt-p03g-global-kinematic-assembly-repository-gates-1.0",
        "base": BASE,
        "result": "PASS",
        "scope_paths": changed,
        "assembly_verifier": assembly,
        "parent_immutability": parents,
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
            "topology_selected": False,
            "global_solution_claimed": False,
            "carrier_or_matter_adopted": False,
            "repository_reorganization_performed": False,
            "P04_launched": False,
            "P11_launched": False,
        },
    }
    (HERE / "REPOSITORY_GATES.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("repository_gates=PASS")
    print(f"P03G={assembly['main_checks']} main/{assembly['independent_checks']} independent/{assembly['catch_proofs']} catches")
    print(f"fresh_adversarial={assembly['fresh_adversarial_review']} grade={assembly['evidence_grade']}")
    print(f"parents={parents['count']} frozen_manifests=6 entries={frozen['entries']} paths={frozen['tracked_paths']}")
    print(f"prior_packages={len(prior)} entries={replay['entries']}")
    print(f"tests={tests['passed']} passed/{tests['failed']} known failed/{tests['xfailed']} xfailed")
    print(f"dirty_metadata_paths={dirty['paths']} hash={dirty['metadata_sha256']}")
    print(f"package_manifest={package['sha256']} entries={package['entries']}")


if __name__ == "__main__":
    main()

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
BASE = "e608d98b2de9b827bb7dfa1aebf083511bc27643"
PACKAGE = "udt_dynamics_branch_ruling_p04_2026-07-21"
P03G = ROOT / "udt_global_kinematic_assembly_p03g_2026-07-21"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
P03G_MANIFEST = "62f9b3f33409b62fb841734e8a91e61d9b859247bf808c4a6cf3740b6a54b6c9"

SOURCES = {
    "udt_global_kinematic_assembly_p03g_2026-07-21/SHA256SUMS.txt": P03G_MANIFEST,
    "udt_founded_constraint_atlas_p03_2026-07-21/SHA256SUMS.txt": "b0ec5cbb2be404084e1b1ed4eca98d53c9712a62cf1af0a48eb340b64467c3be",
    "udt_complete_metric_solution_space_map_2026-07-21/SHA256SUMS.txt": "1778e4dcfcf9ac0bd3574fb3ff5248f2990265fa40d0822ff964ac67c434ae38",
    "native_action_final_adjudication_2026-07-18/SHA256SUMS.txt": "57be0046432c27046e84eaafd1706959558f43170d0f1e23dc3047966e512f33",
    "UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md": "db4a426b021e375fa4bca0d870aaf973de319de3b08072195d001a056630832d",
    "UDT_GR_TO_UDT_SELECTOR_AUDIT_PREREG_2026-07-18.md": "6a835388e8f7a82a4bb4b9496f99c4a5e4181f5e5ccb2637641a1b4346922cc6",
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


def ruling_verification():
    environment = dict(os.environ); environment["PYTHONDONTWRITEBYTECODE"] = "1"; environment["CUDA_VISIBLE_DEVICES"] = ""
    main = subprocess.run([sys.executable, "-B", str(HERE / "build_p04_ruling.py")], cwd=ROOT, env=environment, text=True, capture_output=True, timeout=300, check=False)
    if main.returncode or main.stderr:
        raise AssertionError(main.stdout + main.stderr)
    independent = subprocess.run([sys.executable, "-B", str(HERE / "verify_p04_ruling.py")], cwd=ROOT, env=environment, text=True, capture_output=True, timeout=300, check=False)
    if independent.returncode or independent.stderr:
        raise AssertionError(independent.stdout + independent.stderr)
    result = json.loads((HERE / "RULING_RESULT.json").read_text(encoding="utf-8"))
    verification = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    if (
        result["status"] != "PASS"
        or result["check_count"] != 19
        or result["controlling_scientific_status"] != "NO_DYNAMICS_DERIVED"
        or result["counts"] != {"authorized_lanes": 3, "derived_lanes": 0, "field_realization_pairs": 21, "field_realizations_removed": 0, "global_axes_carried_free": 12, "solve_authorizations": 0, "premise_rows": 18}
        or verification["status"] != "PASS"
        or verification["check_count"] != 6
        or verification["catch_proof_count"] != 22
        or result["maximum_conclusion"] != "DYNAMICS_LANES_AUTHORIZED_OR_REMAIN_OPEN"
    ):
        raise AssertionError("P04 ruling verification")
    return {"status": "PASS", "main_checks": result["check_count"], "independent_checks": verification["check_count"], "catch_proofs": verification["catch_proof_count"], "main_result_sha256": digest(HERE / "RULING_RESULT.json"), "verification_result_sha256": digest(HERE / "VERIFICATION_RESULT.json"), "maximum_conclusion": result["maximum_conclusion"]}


def source_immutability():
    observed = {}
    for relative, expected in SOURCES.items():
        value = digest(ROOT / relative)
        if value != expected:
            raise AssertionError(f"source hash: {relative}")
        if subprocess.run(["git", "diff", "--quiet", BASE, "--", relative], cwd=ROOT, check=False).returncode:
            raise AssertionError(f"source changed: {relative}")
        observed[relative] = value
    return {"status": "PASS", "sources": observed, "count": len(observed)}


def prior_packages():
    record = json.loads((P03G / "REPOSITORY_GATES.json").read_text(encoding="utf-8"))
    prior = {row["package"]: row["manifest_sha256"] for row in record["prior_scientific_packages"]["packages"]}
    prior["udt_global_kinematic_assembly_p03g_2026-07-21"] = P03G_MANIFEST
    return prior


def main():
    generic = load(ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19/verify_repository_gates.py", "p04_generic_gates")
    generic.BASE = BASE
    generic.PACKAGE = PACKAGE
    changed = scope(generic)
    ruling = ruling_verification()
    sources = source_immutability()
    frozen = generic.validate_frozen(ROOT)
    prior = prior_packages()
    replay = generic.replay_packages(ROOT, prior, "PRIOR")
    if len(prior) != 56 or replay["entries"] != 1359:
        raise generic.GateError("PRIOR", f"{len(prior)}:{replay['entries']}")
    navigation = generic.validate_navigation(ROOT)
    dirty = generic.validate_dirty(ROOT, DIRTY)
    tests = generic.validate_tests(ROOT)
    tests.pop("stdout_sha256", None)
    signature = f"{tests['passed']}|{tests['failed']}|{tests['xfailed']}|{tests['failure']}"
    tests["result_signature_sha256"] = hashlib.sha256(signature.encode("utf-8")).hexdigest()
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
        "schema": "udt-p04-dynamics-branch-ruling-repository-gates-1.0",
        "base": BASE,
        "result": "PASS",
        "scope_paths": changed,
        "ruling_verifier": ruling,
        "source_immutability": sources,
        "frozen": frozen,
        "prior_scientific_packages": replay,
        "navigation": navigation,
        "dirty_checkout": dirty,
        "tests": tests,
        "package_manifest": package,
        "catch_proofs": catches,
        "compute": {"cpu_only": True, "gpu_work_performed": False, "symbolic_variation": False, "ODE_or_PDE_run": False},
        "authority_boundary": {"startup_controls_changed": False, "canon_changed": False, "native_dynamics_derived": False, "conditional_lanes_authorized": 3, "P05_launched": False, "solve_authorized": False, "carrier_or_matter_adopted": False, "repository_reorganization_performed": False},
    }
    (HERE / "REPOSITORY_GATES.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("repository_gates=PASS")
    print(f"P04={ruling['main_checks']} main/{ruling['independent_checks']} independent/{ruling['catch_proofs']} catches")
    print(f"sources={sources['count']} frozen_manifests=6 entries={frozen['entries']} paths={frozen['tracked_paths']}")
    print(f"prior_packages={len(prior)} entries={replay['entries']}")
    print(f"tests={tests['passed']} passed/{tests['failed']} known failed/{tests['xfailed']} xfailed")
    print(f"dirty_metadata_paths={dirty['paths']} hash={dirty['metadata_sha256']}")
    print(f"package_manifest={package['sha256']} entries={package['entries']}")


if __name__ == "__main__":
    main()

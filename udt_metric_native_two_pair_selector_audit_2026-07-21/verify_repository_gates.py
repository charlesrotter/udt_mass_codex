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
BASE = "d5e04915640be3fdebff604f63cff96cb3ada325"
PACKAGE = "udt_metric_native_two_pair_selector_audit_2026-07-21"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
FAILED_BASIN_MANIFEST = "113fa557c2a8e0b3267974276809ebebfd41b18a5ec4c5fe7afa93b875367a95"
OPEN_PATH_MANIFEST = "e130b3e01583ac317643f7e3050979a8084cbf06f2700e190690f96957008c4d"
TWIST_PARENT_MANIFEST = "73a53266bd49b16593e0e55c05f65940b69687c9ca2a211c060bf5b9eafa9b0b"
COUPLED_PARENT_MANIFEST = "3fa442d93c4f69322f90504dd92dbbba5e8028195076e57e44c1bcf3b1347aa8"
INTRINSIC_PARENT_MANIFEST = "8b3a011bbb6c7821405ba1113d51238b72ddd8dc2d773f1e92a88f469ffb9e65"
TRANSVERSE_PARENT_MANIFEST = "21a72d4e2f1afdb582042b0378bb6e3006277b832fd1daec0ddcf11df2b75d2a"
GLOBAL_CLOSURE_PARENT_MANIFEST = "e11985e9afd9cefbb818e75aa1afe90acec48d60b2170e26c2fe712287742d48"
COFRAME_COCYCLE_PARENT_MANIFEST = "1297e8f6773f863f426d66f6c4915741a742c1ee13230abf2b066421de49b04b"
ANCHOR_SOLDERING_PARENT_MANIFEST = "6b190e97202755ce79e0b394a7fbd6a1e06d1199cecea4c193400ef9c9ec3798"
SEAL_SOLDERING_PARENT_MANIFEST = "48ecfbdd78ec44308a7d93309e68cc13b4293fd2d051a6dff11c832e0bc60450"
COMPLETE_LIFT_PARENT_MANIFEST = "15972da297739e299c6d1173e8b2989b98eb8416c067fdba9eb8d74c0697455e"
TIME_EXTENDABILITY_MANIFEST = "a937bcf290cb7964d54f8e358a56489a6c4015a0264fcb949103a2a6af31c72c"
RECIPROCAL_CONNECTION_MANIFEST = "6842b5f03d94ede4c880d565738a77905f53a6f221f5910be15d2dfa4f4d19a4"


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
        [sys.executable, str(HERE / "derive_metric_two_pair_selector.py")],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if derivation.returncode:
        raise AssertionError(derivation.stdout.decode("utf-8", "replace"))
    verification = subprocess.run(
        [sys.executable, str(HERE / "verify_metric_two_pair_selector.py")],
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
        or result["derivation_check_count"] != 62
        or result["independent_check_count"] != 34
        or result["catch_proof_count"] != 25
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
        "metric_two_pair_generic_gates",
    )
    failed_wrapper = load(
        ROOT / "c2_failed_basin_homotopy_2026-07-20/verify_repository_gates.py",
        "metric_two_pair_failed_wrapper",
    )
    generic.BASE = BASE
    generic.PACKAGE = PACKAGE
    universe = rows(ROOT / "udt_premise_reset_audit_2026-07-19/PACKAGE_UNIVERSE.tsv")
    prior = {row["package"]: row["manifest_sha256"] for row in universe}
    prior.update(failed_wrapper.ADD)
    prior["c2_failed_basin_homotopy_2026-07-20"] = FAILED_BASIN_MANIFEST
    prior["c2_open_path_checkpoint_continuation_2026-07-20"] = OPEN_PATH_MANIFEST
    prior["c2_reciprocal_transverse_twist_jacobi_2026-07-20"] = TWIST_PARENT_MANIFEST
    prior["c2_coupled_reciprocal_twist_onshell_2026-07-20"] = COUPLED_PARENT_MANIFEST
    prior["c2_intrinsic_angular_product_selector_2026-07-20"] = INTRINSIC_PARENT_MANIFEST
    prior["c2_transverse_coframe_closure_2026-07-20"] = TRANSVERSE_PARENT_MANIFEST
    prior["udt_global_reciprocal_closure_audit_2026-07-20"] = GLOBAL_CLOSURE_PARENT_MANIFEST
    prior["udt_global_coframe_cocycle_audit_2026-07-20"] = COFRAME_COCYCLE_PARENT_MANIFEST
    prior["udt_mixed_readout_anchor_soldering_audit_2026-07-20"] = ANCHOR_SOLDERING_PARENT_MANIFEST
    prior["udt_clock_ruler_soldering_selector_audit_2026-07-20"] = SEAL_SOLDERING_PARENT_MANIFEST
    prior["udt_complete_lift_mu_closure_audit_2026-07-20"] = COMPLETE_LIFT_PARENT_MANIFEST
    prior["udt_time_extendability_constraint_audit_2026-07-20"] = TIME_EXTENDABILITY_MANIFEST
    prior["udt_gr_subtraction_reciprocal_connection_audit_2026-07-21"] = RECIPROCAL_CONNECTION_MANIFEST

    changed = scope(generic)
    scientific = science()
    frozen = generic.validate_frozen(ROOT)
    replay = generic.replay_packages(ROOT, prior, "PRIOR")
    if len(prior) != 48 or replay["entries"] != 1157:
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
        "schema": "udt-metric-native-two-pair-selector-repository-gates-1.0",
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
            "complete_angular_seal_lift_selected": False,
            "physical_connection_or_transport_selected": False,
            "bulk_holonomy_reduction_derived": False,
            "unconditional_full_two_pair_reciprocity_derived": False,
            "Hopf_carrier_or_topology_selected": False,
            "action_or_field_equation_derived": False,
            "boundary_dynamics_selected": False,
            "carrier_source_or_mass_derived": False,
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

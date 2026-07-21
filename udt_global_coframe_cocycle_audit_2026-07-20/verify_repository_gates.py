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
BASE = "c8d337fb06b90126756483af86f105e2fbb4eabb"
PACKAGE = "udt_global_coframe_cocycle_audit_2026-07-20"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
FAILED_BASIN_MANIFEST = "113fa557c2a8e0b3267974276809ebebfd41b18a5ec4c5fe7afa93b875367a95"
OPEN_PATH_MANIFEST = "e130b3e01583ac317643f7e3050979a8084cbf06f2700e190690f96957008c4d"
TWIST_PARENT_MANIFEST = "73a53266bd49b16593e0e55c05f65940b69687c9ca2a211c060bf5b9eafa9b0b"
COUPLED_PARENT_MANIFEST = "3fa442d93c4f69322f90504dd92dbbba5e8028195076e57e44c1bcf3b1347aa8"
INTRINSIC_PARENT_MANIFEST = "8b3a011bbb6c7821405ba1113d51238b72ddd8dc2d773f1e92a88f469ffb9e65"
TRANSVERSE_PARENT_MANIFEST = "21a72d4e2f1afdb582042b0378bb6e3006277b832fd1daec0ddcf11df2b75d2a"
GLOBAL_CLOSURE_PARENT_MANIFEST = "e11985e9afd9cefbb818e75aa1afe90acec48d60b2170e26c2fe712287742d48"


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
        [sys.executable, str(HERE / "derive_global_coframe_cocycle.py")],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if derivation.returncode:
        raise AssertionError(derivation.stdout.decode("utf-8", "replace"))
    verification = subprocess.run(
        [sys.executable, str(HERE / "verify_global_coframe_cocycle.py")],
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
        or result["counts"]["derivation_checks"] != 63
        or result["counts"]["independent_checks"] != 19
        or result["counts"]["catch_proofs"] != 19
    ):
        raise AssertionError("science")
    return {"result": result["result"], **result["counts"]}


def main():
    generic = load(
        ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19/verify_repository_gates.py",
        "coframe_cocycle_generic_gates",
    )
    failed_wrapper = load(
        ROOT / "c2_failed_basin_homotopy_2026-07-20/verify_repository_gates.py",
        "coframe_cocycle_failed_wrapper",
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

    changed = scope(generic)
    scientific = science()
    frozen = generic.validate_frozen(ROOT)
    replay = generic.replay_packages(ROOT, prior, "PRIOR")
    if len(prior) != 42 or replay["entries"] != 1042:
        raise generic.GateError("PRIOR", f"{len(prior)}:{replay['entries']}")
    navigation = generic.validate_navigation(ROOT)
    dirty = generic.validate_dirty(ROOT, DIRTY)
    tests = generic.validate_tests(ROOT)
    package = generic.validate_package_manifest(ROOT)
    catches = {
        "scope": generic.expect("SCOPE", lambda: scope(generic, "CANON.md")),
        "frozen": generic.expect("FROZEN", lambda: generic.validate_frozen(ROOT, True)),
        "prior": generic.expect("PRIOR", lambda: generic.replay_packages(ROOT, prior, "PRIOR", True)),
        "current": generic.expect(
            "NAVIGATION", lambda: generic.validate_navigation(ROOT, "current")
        ),
        "frontier": generic.expect(
            "NAVIGATION", lambda: generic.validate_navigation(ROOT, "frontier")
        ),
        "dirty": generic.expect("DIRTY", lambda: generic.validate_dirty(ROOT, DIRTY, True)),
        "package": generic.expect(
            "PACKAGE", lambda: generic.validate_package_manifest(ROOT, True)
        ),
    }
    output = {
        "schema": "udt-global-coframe-cocycle-repository-gates-1.0",
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
            "mixed_readout_made_foundational": False,
            "mixed_modulus_or_observer_soldering_selected": False,
            "global_cover_or_topology_selected": False,
            "boundary_polarization_selected": False,
            "global_completion_map_derived": False,
            "action_or_bootstrap_selector_derived": False,
            "Xmax_or_scale_derived": False,
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

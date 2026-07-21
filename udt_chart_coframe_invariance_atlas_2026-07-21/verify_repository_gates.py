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
BASE = "ba572f589eae83c9f74de1b93b34d389529b27b7"
PACKAGE = "udt_chart_coframe_invariance_atlas_2026-07-21"
PARENT = ROOT / "udt_structural_ensemble_metric_atlas_2026-07-21"
PARENT_MANIFEST = "3d569ed31506f5f7ce44beac30e8419571f734b3973dcc34d6c474bf78636757"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
MAXIMUM = "BOUNDED_CHART_COFRAME_AND_SUPPLIED_SPLIT_INVARIANCE_ATLAS_CHARACTERIZED"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def scope(generic, inject: str | None = None) -> list[str]:
    changed = set(str(generic.git(ROOT, "diff", "--name-only", BASE)).splitlines())
    changed.update(str(generic.git(ROOT, "ls-files", "--others", "--exclude-standard")).splitlines())
    if inject:
        changed.add(inject)
    bad = sorted(path for path in changed if path and not path.startswith(PACKAGE + "/"))
    if bad:
        raise generic.GateError("SCOPE", bad[0])
    return sorted(path for path in changed if path != f"{PACKAGE}/REPOSITORY_GATES.json" and "__pycache__" not in path and not path.endswith(".pyc"))


def scientific_verification() -> dict[str, object]:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["CUDA_VISIBLE_DEVICES"] = ""
    main = subprocess.run([sys.executable, "-B", str(HERE / "build_invariance_atlas.py")], cwd=ROOT, env=env, text=True, capture_output=True, timeout=900, check=False)
    if main.returncode or main.stderr:
        raise AssertionError(main.stdout + main.stderr)
    independent = subprocess.run([sys.executable, "-B", str(HERE / "verify_invariance_atlas.py")], cwd=ROOT, env=env, text=True, capture_output=True, timeout=300, check=False)
    if independent.returncode or independent.stderr:
        raise AssertionError(independent.stdout + independent.stderr)
    result = json.loads((HERE / "ATLAS_RESULT.json").read_text(encoding="utf-8"))
    verify = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    uncertain = [row for row in tsv(HERE / "RANK_THRESHOLD_MARGIN_LEDGER.tsv") if row["rank_margin_status"] == "NUMERIC_UNCERTAIN"]
    if (
        result["checks"] != 41 or result["maximum_conclusion"] != MAXIMUM
        or result["configuration_orbit_records"] != 73728 or result["interaction_orbit_records"] != 69120
        or result["numeric_covariance_failures"] != 0 or result["discarded_records"] != 0
        or result["numeric_uncertain_span_rows"] != 1 or result["action_loaded"] is not False
        or result["full_group_exhaustiveness_claim"] is not False or result["split_selected_claim"] is not False
        or result["gpu_used"] is not False or verify["status"] != "PASS" or verify["checks"] != 1419862
        or verify["catch_proofs"] != 14 or verify["local_lorentz_anchor_checks"] != 3840
        or verify["coordinate_curvature_anchor_checks"] != 112 or verify["independent_cartan_anchor_checks"] != 3952
        or verify["independent_split_interaction_checks"] != 768 or len(uncertain) != 1
        or (uncertain[0]["transform_id"], uncertain[0]["target_mask"], uncertain[0]["payload"], uncertain[0]["span_rank"])
        != ("C05_SWAP_DEPTH_SCREEN", "M4", "split_slot_twojet", "130")
    ):
        raise AssertionError("scientific verification")
    return {
        "status": "PASS", "main_checks": result["checks"], "independent_checks": verify["checks"],
        "catch_proofs": verify["catch_proofs"], "cartan_anchors": verify["independent_cartan_anchor_checks"],
        "main_result_sha256": digest(HERE / "ATLAS_RESULT.json"),
        "verification_result_sha256": digest(HERE / "VERIFICATION_RESULT.json"),
        "rank_margin_sha256": digest(HERE / "RANK_THRESHOLD_MARGIN_LEDGER.tsv"),
        "maximum_conclusion": result["maximum_conclusion"],
    }


def source_immutability() -> dict[str, object]:
    observed = {}
    for row in tsv(HERE / "SOURCE_LINEAGE.tsv"):
        relative, expected, role = row["path"], row["sha256"], row["role"]
        path = HERE / relative if role == "PREREGISTRATION" else ROOT / relative
        if digest(path) != expected:
            raise AssertionError(f"source hash {relative}")
        if role == "IMMUTABLE_SOURCE" and subprocess.run(["git", "diff", "--quiet", BASE, "--", relative], cwd=ROOT, check=False).returncode:
            raise AssertionError(f"source changed {relative}")
        observed[relative] = expected
    if len(observed) != 5:
        raise AssertionError("source count")
    return {"status": "PASS", "count": len(observed), "sources": observed}


def prior_packages() -> dict[str, str]:
    record = json.loads((PARENT / "REPOSITORY_GATES.json").read_text(encoding="utf-8"))
    prior = {row["package"]: row["manifest_sha256"] for row in record["prior_scientific_packages"]["packages"]}
    prior[PARENT.name] = PARENT_MANIFEST
    return prior


def validate_package_manifest(generic, corrupt: bool = False) -> dict[str, object]:
    manifest = HERE / "SHA256SUMS.txt"
    replay = subprocess.run(["sha256sum", "--check", manifest.name], cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False)
    if corrupt or replay.returncode or "FAILED" in replay.stdout:
        raise generic.GateError("PACKAGE", "hash-replay")
    entries = [line.split("  ", 1)[1] for line in manifest.read_text(encoding="utf-8").splitlines() if line]
    excluded = {"SHA256SUMS.txt", "REPOSITORY_GATES.json"}
    actual = sorted(path.relative_to(HERE).as_posix() for path in HERE.rglob("*") if path.is_file() and path.relative_to(HERE).as_posix() not in excluded and "__pycache__" not in path.parts and path.suffix != ".pyc")
    if sorted(entries) != actual or len(entries) != len(set(entries)):
        raise generic.GateError("PACKAGE", "recursive coverage")
    return {"entries": len(entries), "sha256": digest(manifest), "result": "PASS"}


def main() -> None:
    generic = load(ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19/verify_repository_gates.py", "invariance_generic")
    generic.BASE = BASE
    generic.PACKAGE = PACKAGE
    changed = scope(generic)
    scientific = scientific_verification()
    sources = source_immutability()
    frozen = generic.validate_frozen(ROOT)
    prior = prior_packages()
    replay = generic.replay_packages(ROOT, prior, "PRIOR")
    if len(prior) != 66 or replay["entries"] != 1665:
        raise generic.GateError("PRIOR", f"{len(prior)}:{replay['entries']}")
    navigation = generic.validate_navigation(ROOT)
    dirty = generic.validate_dirty(ROOT, DIRTY)
    tests = generic.validate_tests(ROOT)
    tests.pop("stdout_sha256", None)
    signature = f"{tests['passed']}|{tests['failed']}|{tests['xfailed']}|{tests['failure']}"
    tests["result_signature_sha256"] = hashlib.sha256(signature.encode()).hexdigest()
    package = validate_package_manifest(generic)
    catches = {
        "scope": generic.expect("SCOPE", lambda: scope(generic, "LIVE.md")),
        "frozen": generic.expect("FROZEN", lambda: generic.validate_frozen(ROOT, True)),
        "prior": generic.expect("PRIOR", lambda: generic.replay_packages(ROOT, prior, "PRIOR", True)),
        "current": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, "current")),
        "frontier": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, "frontier")),
        "dirty": generic.expect("DIRTY", lambda: generic.validate_dirty(ROOT, DIRTY, True)),
        "package": generic.expect("PACKAGE", lambda: validate_package_manifest(generic, True)),
    }
    output = {
        "schema": "udt-chart-coframe-invariance-atlas-repository-gates-1.0", "base": BASE, "result": "PASS",
        "scope_paths": changed, "scientific_verifier": scientific, "source_immutability": sources,
        "frozen": frozen, "prior_scientific_packages": replay, "navigation": navigation,
        "dirty_checkout": dirty, "tests": tests, "package_manifest": package, "catch_proofs": catches,
        "compute": {"cpu_only": True, "gpu_work_performed": False, "ODE_or_PDE_run": False},
        "authority_boundary": {
            "startup_controls_changed": False, "canon_changed": False, "action_or_equations_loaded": False,
            "physical_interaction_claimed": False, "physical_split_selected": False,
            "physics_ranked": False, "physical_evolution_launched": False,
            "boundary_topology_or_scale_selected": False, "carrier_or_matter_adopted": False,
            "repository_reorganization_performed": False,
        },
    }
    (HERE / "REPOSITORY_GATES.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("repository_gates=PASS")
    print(f"scientific={scientific['main_checks']} main/{scientific['independent_checks']} independent/{scientific['catch_proofs']} catches")
    print(f"sources={sources['count']} frozen_manifests=6 entries={frozen['entries']} paths={frozen['tracked_paths']}")
    print(f"prior_packages={len(prior)} entries={replay['entries']}")
    print(f"tests={tests['passed']} passed/{tests['failed']} known failed/{tests['xfailed']} xfailed")
    print(f"dirty_metadata_paths={dirty['paths']} hash={dirty['metadata_sha256']}")
    print(f"package_manifest={package['sha256']} entries={package['entries']}")


if __name__ == "__main__":
    main()

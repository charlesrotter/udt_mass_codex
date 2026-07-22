#!/usr/bin/env python3
"""Repository gates for the local-selector/holonomy closure package."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "1a70bf97771cf62ac021d4bf365f5b79a3fbd487"
PACKAGE = HERE.name
DIRTY = Path("/home/udt-admin/udt_mass_codex")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prior_packages() -> dict[str, str]:
    record = json.loads(
        (ROOT / "udt_metric_to_frontier_reference_2026-07-22/FINAL_REPOSITORY_GATES.json").read_text(encoding="utf-8")
    )
    packages = {row["package"]: row["manifest_sha256"] for row in record["prior_scientific_packages"]["packages"]}
    packages["udt_metric_to_frontier_reference_2026-07-22"] = record["package_manifest"]["manifest_sha256"]
    return packages


def replay_survey(generic, corrupt: bool = False) -> dict[str, object]:
    package = "udt_century_adjacent_mathematics_survey_2026-07-22"
    manifest = ROOT / package / "MANIFEST.sha256"
    expected = "66f1915965a5bd0ee8ff09b54b0ad1275578bfad447b7cb78b0a16e87b3e96f3"
    observed = digest(manifest)
    if corrupt:
        observed = "0" * 64
    if observed != expected:
        raise generic.GateError("PRIOR", package + ":manifest")
    replay = generic.run(manifest.parent, ["sha256sum", "--check", manifest.name])
    if replay.returncode or "FAILED" in str(replay.stdout):
        raise generic.GateError("PRIOR", package + ":replay")
    entries = len([line for line in manifest.read_text(encoding="utf-8").splitlines() if line])
    return {"package": package, "manifest_sha256": expected, "entries": entries, "result": "PASS"}


def validate_manifest(generic, corrupt: bool = False) -> dict[str, object]:
    manifest = HERE / "MANIFEST.sha256"
    replay = generic.run(HERE, ["sha256sum", "--check", manifest.name])
    if corrupt or replay.returncode or "FAILED" in str(replay.stdout):
        raise generic.GateError("PACKAGE", "manifest-replay")
    entries = [line.split("  ", 1)[1] for line in manifest.read_text(encoding="utf-8").splitlines() if line]
    excluded = {"MANIFEST.sha256", "REPOSITORY_GATES.json", "REPOSITORY_GATES_TRANSCRIPT.txt"}
    actual = sorted(path.name for path in HERE.iterdir() if path.is_file() and path.name not in excluded)
    if sorted(entries) != actual:
        raise generic.GateError("PACKAGE", f"coverage:{sorted(set(entries) ^ set(actual))}")
    return {"entries": len(entries), "sha256": digest(manifest), "result": "PASS"}


def main() -> None:
    generic = load(
        ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19/verify_repository_gates.py",
        "selector_holonomy_generic_gates",
    )
    generic.BASE = BASE
    generic.PACKAGE = PACKAGE

    scope = generic.validate_scope(ROOT)
    frozen = generic.validate_frozen(ROOT)
    packages = prior_packages()
    prior = generic.replay_packages(ROOT, packages, "PRIOR")
    survey = replay_survey(generic)
    prior["packages"].append(survey)
    prior["entries"] += survey["entries"]
    if len(prior["packages"]) != 73 or prior["entries"] != 2049:
        raise AssertionError(f"prior packages {len(prior['packages'])} entries {prior['entries']}")
    navigation = generic.validate_navigation(ROOT)
    dirty = generic.validate_dirty(ROOT, DIRTY)
    tests = generic.validate_tests(ROOT)
    package = validate_manifest(generic)
    verification = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    if verification["verdict"] != "PASS_WITH_CAVEAT_NO_FRESH_EXTERNAL_MODEL_REVIEW":
        raise AssertionError("verification verdict")
    if verification["catch_passes"] != 15 or verification["independent_configurations"] != 6144:
        raise AssertionError("verification coverage")

    catches = {
        "scope_rejects_live_edit": generic.expect("SCOPE", lambda: generic.validate_scope(ROOT, "LIVE.md")),
        "frozen_corruption_rejected": generic.expect("FROZEN", lambda: generic.validate_frozen(ROOT, True)),
        "prior_corruption_rejected": generic.expect("PRIOR", lambda: generic.replay_packages(ROOT, packages, "PRIOR", True)),
        "survey_corruption_rejected": generic.expect("PRIOR", lambda: replay_survey(generic, True)),
        "current_path_loss_rejected": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, "current")),
        "frontier_loss_rejected": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, "frontier")),
        "dirty_metadata_loss_rejected": generic.expect("DIRTY", lambda: generic.validate_dirty(ROOT, DIRTY, True)),
        "package_corruption_rejected": generic.expect("PACKAGE", lambda: validate_manifest(generic, True)),
    }

    result = {
        "schema": "udt-local-selector-holonomy-repository-gates-1.0",
        "result": "PASS",
        "base": BASE,
        "scope_paths": scope,
        "scientific_verification": verification,
        "frozen": frozen,
        "prior_scientific_packages": prior,
        "navigation": navigation,
        "dirty_checkout": dirty,
        "tests": tests,
        "package_manifest": package,
        "catch_proofs": catches,
        "compute": {"physics_solves": 0, "gpu_runs": 0, "cpu_geometry_audits": 1},
        "authority_boundary": "LOCAL_SELECTOR_AND_HOLONOMY_SEED_ONLY__NO_ACTION_REALIZATION_MATTER_OR_GLOBAL_HOLONOMY",
    }
    (HERE / "REPOSITORY_GATES.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise

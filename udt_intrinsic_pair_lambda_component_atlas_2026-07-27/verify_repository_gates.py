#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PACKAGE = HERE.name
BASE = "6df7f07"
CORRECTION = "2ec7a4b"
PARENT_PATH = (
    ROOT / "udt_intrinsic_pair_deformation_neighborhood_audit_2026-07-27"
    / "verify_repository_gates.py"
)


def load_parent():
    spec = importlib.util.spec_from_file_location("lambda_atlas_parent_repository_gates", PARENT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.HERE = HERE
    module.ROOT = ROOT
    module.PACKAGE = PACKAGE
    module.BASE = BASE
    module.CORRECTION = CORRECTION
    return module


def main() -> int:
    parent = load_parent()
    generic = parent.load_generic()
    scope = parent.validate_scope()
    frozen = generic.validate_frozen(ROOT)
    navigation = generic.validate_navigation(ROOT)
    tests = parent.validate_tests()
    dirty = parent.validate_dirty()
    package = parent.validate_package()
    premises = parent.run([sys.executable, "verify_current_scientific_premises.py"])
    assert premises.returncode == 0, premises.stdout
    audit = parent.run([sys.executable, str(HERE / "verify_audit.py")])
    assert audit.returncode == 0, audit.stdout
    parent.git(ROOT, "merge-base", "--is-ancestor", BASE, "HEAD")
    parent.git(ROOT, "merge-base", "--is-ancestor", CORRECTION, "HEAD")
    result = {
        "schema": "udt-intrinsic-pair-lambda-component-atlas-gates-1.0",
        "base": BASE,
        "correction": CORRECTION,
        "preregistration_ancestor": True,
        "correction_ancestor": True,
        "result": "PASS",
        "scope_path_count": len(scope),
        "frozen": frozen,
        "navigation": navigation,
        "tests": tests,
        "dirty_checkout": dirty,
        "package_manifest": package,
        "current_premises": {
            "result": "PASS",
            "stdout_sha256": hashlib.sha256(premises.stdout.encode()).hexdigest(),
        },
        "audit_replay": {
            "result": "PASS",
            "stdout_sha256": hashlib.sha256(audit.stdout.encode()).hexdigest(),
        },
        "catch_proofs": {
            "scope": parent.expect_failure(lambda: parent.validate_scope("CANON.md")),
            "frozen": generic.expect("FROZEN", lambda: generic.validate_frozen(ROOT, corrupt=True)),
            "current_paths": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, corrupt="current")),
            "frontier": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, corrupt="frontier")),
            "dirty": parent.expect_failure(lambda: parent.validate_dirty(True)),
            "package": parent.expect_failure(lambda: parent.validate_package(True)),
        },
        "authority_boundary": {
            "startup_controls_changed": False,
            "canon_changed": False,
            "source_results_changed": False,
            "frozen_or_historical_changed": False,
            "copresence_promoted_beyond_working_interpretation": False,
            "instantaneous_operational_access_derived": False,
            "lambda_selected": False,
            "certificate_root_called_clock_loss_or_physical_phase": False,
            "full_configuration_component_claimed": False,
            "action_carrier_source_density_mass_Xmax_dynamics_selected": False,
            "gpu_work": False,
            "repository_reorganization": False,
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

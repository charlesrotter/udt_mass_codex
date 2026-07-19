#!/usr/bin/env python3
"""Repository/frozen/navigation/test/dirty-metadata gates for this bounded package."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "d0b5d824432e1ac621d5e198e9ac490b265d2ea6"
PACKAGE = "rung2_weld_postjuly_regrade_2026-07-19"
ORIGINAL_DIRTY = Path("/home/udt-admin/udt_mass_codex")


def load_gate_module():
    source = ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19/verify_repository_gates.py"
    spec = importlib.util.spec_from_file_location("prior_repository_gates", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load prior repository gate implementation")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.BASE = BASE
    module.PACKAGE = PACKAGE
    return module


def main() -> None:
    gate = load_gate_module()
    prior_packages = dict(gate.PRIOR_SCIENTIFIC_PACKAGES)
    prior_packages["bootstrap_csn_phi_angular_selector_2026-07-19"] = (
        "1a48e574835ee3838514294a7badd2415a74cdb0d10cf0545c30d3698ab022d2"
    )

    scope = gate.validate_scope(ROOT)
    frozen = gate.validate_frozen(ROOT)
    prior = gate.replay_packages(ROOT, prior_packages, "PRIOR")
    navigation = gate.validate_navigation(ROOT)
    dirty = gate.validate_dirty(ROOT, ORIGINAL_DIRTY)
    tests = gate.validate_tests(ROOT)
    package = gate.validate_package_manifest(ROOT)

    catches = {
        "out_of_scope_change_rejected": gate.expect(
            "SCOPE", lambda: gate.validate_scope(ROOT, "CANON.md")
        ),
        "frozen_manifest_corruption_rejected": gate.expect(
            "FROZEN", lambda: gate.validate_frozen(ROOT, True)
        ),
        "prior_science_manifest_corruption_rejected": gate.expect(
            "PRIOR", lambda: gate.replay_packages(ROOT, prior_packages, "PRIOR", True)
        ),
        "missing_current_path_rejected": gate.expect(
            "NAVIGATION", lambda: gate.validate_navigation(ROOT, "current")
        ),
        "missing_frontier_target_rejected": gate.expect(
            "NAVIGATION", lambda: gate.validate_navigation(ROOT, "frontier")
        ),
        "dirty_metadata_loss_rejected": gate.expect(
            "DIRTY", lambda: gate.validate_dirty(ROOT, ORIGINAL_DIRTY, True)
        ),
        "package_hash_failure_rejected": gate.expect(
            "PACKAGE", lambda: gate.validate_package_manifest(ROOT, True)
        ),
    }

    output = {
        "schema": "udt-rung2-weld-regrade-repository-gates-v1",
        "base": BASE,
        "result": "PASS",
        "scope_paths": scope,
        "frozen": frozen,
        "prior_scientific_packages": prior,
        "navigation": navigation,
        "dirty_checkout": dirty,
        "tests": tests,
        "package_manifest": package,
        "catch_proofs": catches,
        "compute": {
            "cpu_only": True,
            "gpu_work_performed": False,
        },
        "authority_boundary": {
            "canon_changed": False,
            "startup_controls_changed": False,
            "action_constructed": False,
            "carrier_adopted": False,
            "time_live_solve_performed": False,
            "repository_reorganization_performed": False,
        },
    }
    (HERE / "REPOSITORY_GATES.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

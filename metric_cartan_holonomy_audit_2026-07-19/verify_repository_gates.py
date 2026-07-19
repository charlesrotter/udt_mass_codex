#!/usr/bin/env python3
"""Repository, frozen, navigation, test, and dirty-metadata gates."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "ec24c135212d3121e2d5903a29ec669f0b8a982a"
PACKAGE = "metric_cartan_holonomy_audit_2026-07-19"
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
    prior_packages.update({
        "bootstrap_csn_phi_angular_selector_2026-07-19": "1a48e574835ee3838514294a7badd2415a74cdb0d10cf0545c30d3698ab022d2",
        "reciprocal_clock_optical_scale_selector_2026-07-19": "d4ce35881bfd79952083da84bd5bd7f80b6d21b0e69d698059e1695c6f90ba6d",
        "copresence_causal_accessibility_selector_2026-07-19": "14e13dd27aa7036a6fef7db9208681459b86c06186bfffc7990ee877947d8356",
        "copresence_gr_constraint_regrade_2026-07-19": "022f3c97916e38f29260812c14ad0136574d1908c70aabc7d4e56ae99d78f7bc",
        "rung2_weld_postjuly_regrade_2026-07-19": "5121270039c91c654bcd9bb5667cb06c31a5b91dec3747ddf015df0129081812",
    })

    scope = gate.validate_scope(ROOT)
    frozen = gate.validate_frozen(ROOT)
    prior = gate.replay_packages(ROOT, prior_packages, "PRIOR")
    navigation = gate.validate_navigation(ROOT)
    dirty = gate.validate_dirty(ROOT, ORIGINAL_DIRTY)
    tests = gate.validate_tests(ROOT)
    package = gate.validate_package_manifest(ROOT)

    catches = {
        "out_of_scope_change_rejected": gate.expect("SCOPE", lambda: gate.validate_scope(ROOT, "CANON.md")),
        "frozen_manifest_corruption_rejected": gate.expect("FROZEN", lambda: gate.validate_frozen(ROOT, True)),
        "prior_science_manifest_corruption_rejected": gate.expect("PRIOR", lambda: gate.replay_packages(ROOT, prior_packages, "PRIOR", True)),
        "missing_current_path_rejected": gate.expect("NAVIGATION", lambda: gate.validate_navigation(ROOT, "current")),
        "missing_frontier_target_rejected": gate.expect("NAVIGATION", lambda: gate.validate_navigation(ROOT, "frontier")),
        "dirty_metadata_loss_rejected": gate.expect("DIRTY", lambda: gate.validate_dirty(ROOT, ORIGINAL_DIRTY, True)),
        "package_hash_failure_rejected": gate.expect("PACKAGE", lambda: gate.validate_package_manifest(ROOT, True)),
    }

    output = {
        "schema": "udt-metric-cartan-holonomy-repository-gates-v1",
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
        "compute": {"cpu_only": True, "gpu_work_performed": False},
        "authority_boundary": {
            "canon_changed": False,
            "startup_controls_changed": False,
            "action_constructed": False,
            "carrier_adopted": False,
            "time_live_solve_performed": False,
            "repository_reorganization_performed": False,
        },
    }
    (HERE / "REPOSITORY_GATES.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Repository, frozen, navigation, test, and dirty-metadata gates."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "9f12b97349b09f7392edb4bd7204c52cbc597d10"
PACKAGE = "xmax_accelerating_finite_cell_cartan_2026-07-19"
ORIGINAL_DIRTY = Path("/home/udt-admin/udt_mass_codex")


def load_gate_module():
    source = ROOT / "xmax_dynamic_observer_frame_2026-07-19/verify_repository_gates.py"
    spec = importlib.util.spec_from_file_location("prior_repository_gates", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load prior repository gate implementation")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.BASE = BASE
    module.PACKAGE = PACKAGE
    return module


def main() -> None:
    dynamic_wrapper = load_gate_module()
    metric_wrapper = dynamic_wrapper.load_gate_module()
    base_gate = metric_wrapper.load_gate_module()
    prior_packages = dict(base_gate.PRIOR_SCIENTIFIC_PACKAGES)
    prior_packages.update({
        "bootstrap_csn_phi_angular_selector_2026-07-19": "1a48e574835ee3838514294a7badd2415a74cdb0d10cf0545c30d3698ab022d2",
        "reciprocal_clock_optical_scale_selector_2026-07-19": "d4ce35881bfd79952083da84bd5bd7f80b6d21b0e69d698059e1695c6f90ba6d",
        "copresence_causal_accessibility_selector_2026-07-19": "14e13dd27aa7036a6fef7db9208681459b86c06186bfffc7990ee877947d8356",
        "copresence_gr_constraint_regrade_2026-07-19": "022f3c97916e38f29260812c14ad0136574d1908c70aabc7d4e56ae99d78f7bc",
        "rung2_weld_postjuly_regrade_2026-07-19": "5121270039c91c654bcd9bb5667cb06c31a5b91dec3747ddf015df0129081812",
        "metric_cartan_holonomy_audit_2026-07-19": "0e630938c516a0e70cfdb97924ebd6501bd4a97223909b038a22c341a653f1f7",
        "xmax_reciprocity_audit_2026-07-19": "9b1dbd9a38176f9cc4996771485b3d459d83b425e64cd3ac63454350914c2fb3",
        "xmax_full_frame_realization_2026-07-19": "9b986d647b56283ba20dd25d4ae118bc42e775912656da70ef6237f1fbc83b5d",
        "xmax_dynamic_observer_frame_2026-07-19": "dfd3c1b7497ee0b24e82e4277afe700ae17629f1912dfa39bcfa15db501f34db",
    })

    scope = base_gate.validate_scope(ROOT)
    frozen = base_gate.validate_frozen(ROOT)
    prior = base_gate.replay_packages(ROOT, prior_packages, "PRIOR")
    navigation = base_gate.validate_navigation(ROOT)
    dirty = base_gate.validate_dirty(ROOT, ORIGINAL_DIRTY)
    tests = base_gate.validate_tests(ROOT)
    package = base_gate.validate_package_manifest(ROOT)
    catches = {
        "out_of_scope_change_rejected": base_gate.expect("SCOPE", lambda: base_gate.validate_scope(ROOT, "CANON.md")),
        "frozen_manifest_corruption_rejected": base_gate.expect("FROZEN", lambda: base_gate.validate_frozen(ROOT, True)),
        "prior_science_manifest_corruption_rejected": base_gate.expect("PRIOR", lambda: base_gate.replay_packages(ROOT, prior_packages, "PRIOR", True)),
        "missing_current_path_rejected": base_gate.expect("NAVIGATION", lambda: base_gate.validate_navigation(ROOT, "current")),
        "missing_frontier_target_rejected": base_gate.expect("NAVIGATION", lambda: base_gate.validate_navigation(ROOT, "frontier")),
        "dirty_metadata_loss_rejected": base_gate.expect("DIRTY", lambda: base_gate.validate_dirty(ROOT, ORIGINAL_DIRTY, True)),
        "package_hash_failure_rejected": base_gate.expect("PACKAGE", lambda: base_gate.validate_package_manifest(ROOT, True)),
    }

    output = {
        "schema": "udt-accelerating-finite-cell-cartan-repository-gates-v1",
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
            "new_principle_adopted": False,
            "equivalence_principle_derived": False,
            "physical_cell_selected": False,
            "action_constructed": False,
            "carrier_adopted": False,
            "time_live_field_solve_performed": False,
            "repository_reorganization_performed": False,
        },
    }
    (HERE / "REPOSITORY_GATES.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

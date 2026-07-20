#!/usr/bin/env python3
"""Repository, evidence, navigation, test, and dirty-metadata gates."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "d88e6fabd209e81f7c0ba0ef7e1743663bb1106e"
PACKAGE = "reciprocal_c_clock_channel_correction_2026-07-19"
ORIGINAL_DIRTY = Path("/home/udt-admin/udt_mass_codex")
ALLOWED_CONTROLS = {
    "LIVE.md",
    "HANDOFF.md",
    "INDEX.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
}


def load_gate_module():
    source = ROOT / "projective_position_direction_magnitude_correction_2026-07-19/verify_repository_gates.py"
    spec = importlib.util.spec_from_file_location("prior_repository_gates", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load prior repository gate implementation")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.BASE = BASE
    module.PACKAGE = PACKAGE
    return module


def changed_paths(base_gate, injected: str | None = None) -> list[str]:
    changed = set(str(base_gate.git(ROOT, "diff", "--name-only", BASE)).splitlines())
    changed.update(str(base_gate.git(ROOT, "ls-files", "--others", "--exclude-standard")).splitlines())
    if injected:
        changed.add(injected)
    invalid = sorted(
        path for path in changed
        if path and not path.startswith(PACKAGE + "/") and path not in ALLOWED_CONTROLS
    )
    if invalid:
        raise base_gate.GateError("SCOPE", invalid[0])
    missing = sorted(ALLOWED_CONTROLS - changed)
    if missing:
        raise base_gate.GateError("SCOPE", "missing-control:" + missing[0])
    if "CANON.md" in changed:
        raise base_gate.GateError("SCOPE", "CANON.md")
    return sorted(changed)


def validate_controls(base_gate, corrupt: bool = False) -> dict[str, object]:
    source = HERE / "verify_clock_channel.py"
    spec = importlib.util.spec_from_file_location("clock_channel_verifier", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load clock-channel verifier")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    overrides = None
    if corrupt:
        live = (ROOT / "LIVE.md").read_text(encoding="utf-8")
        overrides = {"LIVE.md": live.replace(PACKAGE, "missing_clock_correction")}
    try:
        details = module.validate_controls(overrides)
    except AssertionError as exc:
        raise base_gate.GateError("CONTROLS", str(exc)) from exc
    return {"files": details, "count": len(details), "result": "PASS"}


def validate_execution_ledger(base_gate, corrupt: bool = False) -> dict[str, object]:
    ledger = base_gate.rows(HERE / "EXECUTION_LEDGER.tsv")
    if len(ledger) != 4 or len({row["id"] for row in ledger}) != 4:
        raise base_gate.GateError("LEDGER", "row-census")
    expected_exit = {"E01": "0", "E02": "0", "E03": "0", "E04": "1_EXPECTED_BASELINE"}
    for number, row in enumerate(ledger):
        artifact = HERE / row["output_artifact"]
        observed = base_gate.digest(artifact.read_bytes())
        if corrupt and number == 0:
            observed = "0" * 64
        if row["compute"] != "CPU_ONLY" or row["exit_code"] != expected_exit[row["id"]]:
            raise base_gate.GateError("LEDGER", row["id"] + ":contract")
        if observed != row["output_sha256"]:
            raise base_gate.GateError("LEDGER", row["id"] + ":hash")
    return {"rows": len(ledger), "result": "PASS"}


def main() -> None:
    direction_wrapper = load_gate_module()
    projective_wrapper = direction_wrapper.load_gate_module()
    finite_wrapper = projective_wrapper.load_gate_module()
    dynamic_wrapper = finite_wrapper.load_gate_module()
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
        "xmax_accelerating_finite_cell_cartan_2026-07-19": "c36c5b9e58c4305c91dd52ccbcae42cbd77548f0d4d10d36eda85529e6eb754f",
        "projective_position_join_audit_2026-07-19": "bde786c168a2bf552a9720afa66a3615e66c0d63ffcfb78af680c88813198a84",
        "projective_position_direction_magnitude_correction_2026-07-19": "377eaa791ab93845f50c19d6eb30dadb0b10322ac0cbe405db55ca0a37ad3dfb",
    })

    scope = changed_paths(base_gate)
    controls = validate_controls(base_gate)
    execution = validate_execution_ledger(base_gate)
    frozen = base_gate.validate_frozen(ROOT)
    prior = base_gate.replay_packages(ROOT, prior_packages, "PRIOR")
    navigation = base_gate.validate_navigation(ROOT)
    dirty = base_gate.validate_dirty(ROOT, ORIGINAL_DIRTY)
    tests = base_gate.validate_tests(ROOT)
    package = base_gate.validate_package_manifest(ROOT)
    catches = {
        "out_of_scope_change_rejected": base_gate.expect("SCOPE", lambda: changed_paths(base_gate, "CANON.md")),
        "control_correction_layer_loss_rejected": base_gate.expect("CONTROLS", lambda: validate_controls(base_gate, True)),
        "execution_artifact_hash_corruption_rejected": base_gate.expect("LEDGER", lambda: validate_execution_ledger(base_gate, True)),
        "frozen_manifest_corruption_rejected": base_gate.expect("FROZEN", lambda: base_gate.validate_frozen(ROOT, True)),
        "prior_science_manifest_corruption_rejected": base_gate.expect("PRIOR", lambda: base_gate.replay_packages(ROOT, prior_packages, "PRIOR", True)),
        "missing_current_path_rejected": base_gate.expect("NAVIGATION", lambda: base_gate.validate_navigation(ROOT, "current")),
        "missing_frontier_target_rejected": base_gate.expect("NAVIGATION", lambda: base_gate.validate_navigation(ROOT, "frontier")),
        "dirty_metadata_loss_rejected": base_gate.expect("DIRTY", lambda: base_gate.validate_dirty(ROOT, ORIGINAL_DIRTY, True)),
        "package_hash_failure_rejected": base_gate.expect("PACKAGE", lambda: base_gate.validate_package_manifest(ROOT, True)),
    }

    output = {
        "schema": "udt-reciprocal-c-clock-channel-repository-gates-v1",
        "base": BASE,
        "result": "PASS",
        "scope_paths": scope,
        "controls": controls,
        "execution_ledger": execution,
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
            "startup_controls_changed": True,
            "prior_projective_packages_changed": False,
            "owner_clock_channel_clarification_recorded": True,
            "false_symmetric_clock_selector_withdrawn": True,
            "local_metric_readout_promoted_to_foundation": False,
            "global_distance_derived": False,
            "xmax_derived": False,
            "action_constructed": False,
            "source_or_boundary_constructed": False,
            "carrier_adopted": False,
            "unconditional_mass_derived": False,
            "time_live_field_solve_performed": False,
            "repository_reorganization_performed": False,
        },
    }
    (HERE / "REPOSITORY_GATES.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Repository, evidence, navigation, test, and dirty-metadata gates."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "3b6dedf9bd2692b0ff5ba9e871d7952cf8752aad"
PACKAGE = "udt_premise_reset_audit_2026-07-19"
ORIGINAL_DIRTY = Path("/home/udt-admin/udt_mass_codex")
ALLOWED_CONTROLS = {"LIVE.md", "HANDOFF.md", "INDEX.md", "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md"}


def load_gate_module():
    source = ROOT / "reciprocal_c_clock_channel_correction_2026-07-19/verify_repository_gates.py"
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
    invalid = sorted(path for path in changed if path and not path.startswith(PACKAGE + "/") and path not in ALLOWED_CONTROLS)
    if invalid:
        raise base_gate.GateError("SCOPE", invalid[0])
    if ALLOWED_CONTROLS - changed:
        raise base_gate.GateError("SCOPE", "missing-control")
    if "CANON.md" in changed:
        raise base_gate.GateError("SCOPE", "CANON.md")
    return sorted(changed)


def load_audit_verifier():
    source = HERE / "verify_premise_reset.py"
    spec = importlib.util.spec_from_file_location("premise_reset_verifier", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load premise-reset verifier")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_controls(base_gate, corrupt: bool = False) -> dict[str, object]:
    verifier = load_audit_verifier()
    overrides = None
    if corrupt:
        live = (ROOT / "LIVE.md").read_text(encoding="utf-8")
        overrides = {"LIVE.md": live.replace(PACKAGE, "missing_premise_reset")}
    try:
        details = verifier.validate_controls(overrides)
    except AssertionError as exc:
        raise base_gate.GateError("CONTROLS", str(exc)) from exc
    return {"count": len(details), "files": details, "result": "PASS"}


def validate_execution_ledger(base_gate, corrupt: bool = False) -> dict[str, object]:
    ledger = base_gate.rows(HERE / "EXECUTION_LEDGER.tsv")
    if len(ledger) != 4 or len({row["id"] for row in ledger}) != 4:
        raise base_gate.GateError("LEDGER", "row-census")
    expected_exit = {"E01": "0", "E02": "0", "E03": "0", "E04": "1_EXPECTED_BASELINE"}
    for number, row in enumerate(ledger):
        observed = base_gate.digest((HERE / row["output_artifact"]).read_bytes())
        if corrupt and number == 0:
            observed = "0" * 64
        if row["compute"] != "CPU_ONLY" or row["exit_code"] != expected_exit[row["id"]] or observed != row["output_sha256"]:
            raise base_gate.GateError("LEDGER", row["id"])
    return {"rows": len(ledger), "result": "PASS"}


def main() -> None:
    clock_wrapper = load_gate_module()
    direction_wrapper = clock_wrapper.load_gate_module()
    projective_wrapper = direction_wrapper.load_gate_module()
    finite_wrapper = projective_wrapper.load_gate_module()
    dynamic_wrapper = finite_wrapper.load_gate_module()
    metric_wrapper = dynamic_wrapper.load_gate_module()
    base_gate = metric_wrapper.load_gate_module()

    universe = base_gate.rows(HERE / "PACKAGE_UNIVERSE.tsv")
    prior_packages = {row["package"]: row["manifest_sha256"] for row in universe}
    scope = changed_paths(base_gate)
    controls = validate_controls(base_gate)
    execution = validate_execution_ledger(base_gate)
    frozen = base_gate.validate_frozen(ROOT)
    prior = base_gate.replay_packages(ROOT, prior_packages, "PRIOR")
    if prior["entries"] != 346:
        raise base_gate.GateError("PRIOR", f"entry-total:{prior['entries']}")
    navigation = base_gate.validate_navigation(ROOT)
    dirty = base_gate.validate_dirty(ROOT, ORIGINAL_DIRTY)
    tests = base_gate.validate_tests(ROOT)
    package = base_gate.validate_package_manifest(ROOT)
    catches = {
        "out_of_scope_change_rejected": base_gate.expect("SCOPE", lambda: changed_paths(base_gate, "CANON.md")),
        "navigation_quarantine_loss_rejected": base_gate.expect("CONTROLS", lambda: validate_controls(base_gate, True)),
        "execution_hash_corruption_rejected": base_gate.expect("LEDGER", lambda: validate_execution_ledger(base_gate, True)),
        "frozen_manifest_corruption_rejected": base_gate.expect("FROZEN", lambda: base_gate.validate_frozen(ROOT, True)),
        "prior_package_corruption_rejected": base_gate.expect("PRIOR", lambda: base_gate.replay_packages(ROOT, prior_packages, "PRIOR", True)),
        "missing_current_path_rejected": base_gate.expect("NAVIGATION", lambda: base_gate.validate_navigation(ROOT, "current")),
        "missing_frontier_target_rejected": base_gate.expect("NAVIGATION", lambda: base_gate.validate_navigation(ROOT, "frontier")),
        "dirty_metadata_loss_rejected": base_gate.expect("DIRTY", lambda: base_gate.validate_dirty(ROOT, ORIGINAL_DIRTY, True)),
        "package_hash_failure_rejected": base_gate.expect("PACKAGE", lambda: base_gate.validate_package_manifest(ROOT, True)),
    }

    output = {
        "schema": "udt-premise-reset-repository-gates-1.0",
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
            "prior_packages_changed": False,
            "scientific_artifacts_changed": False,
            "measured_c_and_G_accepted_as_observational_anchors": True,
            "scale_free_core_retained": True,
            "action_selected_by_G": False,
            "Xmax_formula_derived": False,
            "boundary_formula_derived": False,
            "local_density_source_derived": False,
            "carrier_or_mass_derived": False,
            "new_physics_solve_performed": False,
            "repository_reorganization_performed": False,
        },
    }
    (HERE / "REPOSITORY_GATES.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

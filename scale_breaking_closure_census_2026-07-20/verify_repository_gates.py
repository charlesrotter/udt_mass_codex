#!/usr/bin/env python3
"""Repository, frozen, prior-package, navigation, test, scope, and dirty-metadata gates."""

from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "ff1df31c10303ae8deb8438f36ce66f76130c819"
PACKAGE = "scale_breaking_closure_census_2026-07-20"
ORIGINAL_DIRTY = Path("/home/udt-admin/udt_mass_codex")
ALLOWED_CONTROLS = {"LIVE.md", "HANDOFF.md", "INDEX.md", "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md"}
PRIOR_ADDITIONS = {
    "udt_premise_reset_audit_2026-07-19": "6123253b9370bce674c626a863dc595c773da3905cb155a7fe2b77c4667fd3a7",
    "asymptotic_boundary_lineage_audit_2026-07-19": "3841492810a553cc07ae3107cc10c3c5584547db5dcb87757e377ebcdb335afb",
    "native_boundary_generator_scale_audit_2026-07-19": "39d335fbbc0367f206d77173f72d4b4485145dd0cb42aacc8c4491656e6d287c",
    "clock_curvature_selector_audit_2026-07-19": "62dd9fa82d19af1a065ffd45529b8cb0d7c4a814db66ea75759f1d19f159ea04",
    "boundary_bootstrap_representative_selector_audit_2026-07-19": "6cd896586dda87b8e9794818c34ccb392a2f5a004e7d88ba8e288db57e50c6c3",
}


def gate_module():
    source = ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19/verify_repository_gates.py"
    spec = importlib.util.spec_from_file_location("scale_closure_gate_base", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load gate base")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.BASE = BASE
    module.PACKAGE = PACKAGE
    return module


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def changed_paths(gate, injected: str | None = None) -> list[str]:
    changed = set(str(gate.git(ROOT, "diff", "--name-only", BASE)).splitlines())
    changed.update(str(gate.git(ROOT, "ls-files", "--others", "--exclude-standard")).splitlines())
    if injected:
        changed.add(injected)
    invalid = sorted(path for path in changed if path and not path.startswith(PACKAGE + "/") and path not in ALLOWED_CONTROLS)
    if invalid:
        raise gate.GateError("SCOPE", invalid[0])
    if ALLOWED_CONTROLS - changed:
        raise gate.GateError("SCOPE", "missing-control")
    if "CANON.md" in changed:
        raise gate.GateError("SCOPE", "CANON.md")
    return sorted(changed)


def validate_controls(gate, corrupt: bool = False) -> dict[str, object]:
    required = {
        "LIVE.md": [PACKAGE, "SOLE INDEPENDENT DIMENSIONLESS GROUP", "XMAX RECIPROCITY RETAINED", "41/41"],
        "HANDOFF.md": [PACKAGE, "mass per length", "no noncircular scale breaker", "endpoint-flat local CSN"],
        "INDEX.md": [PACKAGE, "has one null group", "positional compatibility law"],
        "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md": [PACKAGE, "one-dimensional nullspace", "NO_NONCIRCULAR_SCALE_BREAKER_FOUND_IN_AUDITED_CURRENT_FOUNDATION"],
    }
    details = []
    for number, (path, tokens) in enumerate(required.items()):
        content = (ROOT / path).read_text(encoding="utf-8")
        if corrupt and number == 0:
            content = content.replace(PACKAGE, "missing_scale_closure_audit")
        if not all(token in content for token in tokens):
            raise gate.GateError("CONTROLS", path)
        details.append({"path": path, "sha256": gate.digest(content.encode("utf-8"))})
    return {"count": len(details), "files": details, "result": "PASS"}


def validate_science() -> dict[str, object]:
    source = HERE / "verify_scale_breaking_closure.py"
    spec = importlib.util.spec_from_file_location("scale_closure_science", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load science verifier")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.main()
    result = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    if result["result"] != "PASS" or len(result["groups"]) != 8 or len(result["catch_proofs"]) != 20:
        raise AssertionError("science verifier failed")
    return {"result": "PASS", "groups": 8, "catch_proofs": 20}


def validate_execution(gate, corrupt: bool = False) -> dict[str, object]:
    ledger = rows(HERE / "EXECUTION_LEDGER.tsv")
    if len(ledger) != 5 or len({row["id"] for row in ledger}) != 5:
        raise gate.GateError("LEDGER", "census")
    for number, row in enumerate(ledger):
        if row["id"] == "E05":
            if row["compute"] != "EXTERNAL_REVIEW_NOT_PERFORMED" or row["exit_code"] != "AUTHORIZATION_NOT_GIVEN":
                raise gate.GateError("LEDGER", row["id"])
            continue
        observed = gate.digest((HERE / row["output_artifact"]).read_bytes())
        if corrupt and number == 0:
            observed = "0" * 64
        if row["compute"] != "CPU_ONLY" or row["exit_code"] not in {"0", "1_EXPECTED_BASELINE"} or observed != row["output_sha256"]:
            raise gate.GateError("LEDGER", row["id"])
    return {"rows": len(ledger), "result": "PASS"}


def main() -> None:
    gate = gate_module()
    universe = rows(ROOT / "udt_premise_reset_audit_2026-07-19/PACKAGE_UNIVERSE.tsv")
    prior = {row["package"]: row["manifest_sha256"] for row in universe}
    prior.update(PRIOR_ADDITIONS)
    scope = changed_paths(gate)
    controls = validate_controls(gate)
    science = validate_science()
    execution = validate_execution(gate)
    frozen = gate.validate_frozen(ROOT)
    prior_result = gate.replay_packages(ROOT, prior, "PRIOR")
    if len(prior) != 24 or prior_result["entries"] != 482:
        raise gate.GateError("PRIOR", f"totals:{len(prior)}:{prior_result['entries']}")
    navigation = gate.validate_navigation(ROOT)
    dirty = gate.validate_dirty(ROOT, ORIGINAL_DIRTY)
    tests = gate.validate_tests(ROOT)
    package = gate.validate_package_manifest(ROOT)
    catches = {
        "out_of_scope_change_rejected": gate.expect("SCOPE", lambda: changed_paths(gate, "CANON.md")),
        "control_overlay_loss_rejected": gate.expect("CONTROLS", lambda: validate_controls(gate, True)),
        "execution_hash_corruption_rejected": gate.expect("LEDGER", lambda: validate_execution(gate, True)),
        "frozen_manifest_corruption_rejected": gate.expect("FROZEN", lambda: gate.validate_frozen(ROOT, True)),
        "prior_package_corruption_rejected": gate.expect("PRIOR", lambda: gate.replay_packages(ROOT, prior, "PRIOR", True)),
        "missing_current_path_rejected": gate.expect("NAVIGATION", lambda: gate.validate_navigation(ROOT, "current")),
        "missing_frontier_target_rejected": gate.expect("NAVIGATION", lambda: gate.validate_navigation(ROOT, "frontier")),
        "dirty_metadata_loss_rejected": gate.expect("DIRTY", lambda: gate.validate_dirty(ROOT, ORIGINAL_DIRTY, True)),
        "package_hash_failure_rejected": gate.expect("PACKAGE", lambda: gate.validate_package_manifest(ROOT, True)),
    }
    output = {
        "schema": "udt-scale-breaking-closure-repository-gates-1.0",
        "base": BASE,
        "result": "PASS",
        "scope_paths": scope,
        "controls": controls,
        "science_verifier": science,
        "execution_ledger": execution,
        "frozen": frozen,
        "prior_scientific_packages": prior_result,
        "navigation": navigation,
        "dirty_checkout": dirty,
        "tests": tests,
        "package_manifest": package,
        "catch_proofs": catches,
        "compute": {"cpu_only": True, "gpu_work_performed": False},
        "authority_boundary": {
            "canon_changed": False,
            "physical_Xmax_or_mass_derived": False,
            "Xmax_reciprocity_promoted_to_physical_frame_law": False,
            "action_source_carrier_or_charge_derived": False,
            "external_model_review_performed": False,
            "gpu_work_performed": False,
            "repository_reorganization_performed": False,
        },
    }
    (HERE / "REPOSITORY_GATES.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("repository_gates=PASS")
    print(f"frozen_manifests=6 entries={frozen['entries']} paths={frozen['tracked_paths']}")
    print(f"prior_packages={len(prior)} entries={prior_result['entries']}")
    print(f"tests={tests['passed']} passed/{tests['failed']} known failed/{tests['xfailed']} xfailed")
    print(f"dirty_metadata_paths={dirty['paths']} hash={dirty['metadata_sha256']}")


if __name__ == "__main__":
    main()

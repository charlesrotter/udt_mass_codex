#!/usr/bin/env python3
"""Repository, evidence, navigation, test, and dirty-metadata gates."""

from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "85a0363b2bef9a1cfb0149dc1aaf20bcd44e1bd8"
PACKAGE = "asymptotic_boundary_lineage_audit_2026-07-19"
ORIGINAL_DIRTY = Path("/home/udt-admin/udt_mass_codex")
ALLOWED_CONTROLS = {"LIVE.md", "HANDOFF.md", "INDEX.md", "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md"}
PREMISE_PACKAGE = "udt_premise_reset_audit_2026-07-19"
PREMISE_MANIFEST = "6123253b9370bce674c626a863dc595c773da3905cb155a7fe2b77c4667fd3a7"


def load_gate_module():
    source = ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19/verify_repository_gates.py"
    spec = importlib.util.spec_from_file_location("repository_gate_base", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load repository gate base")
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
    invalid = sorted(
        path for path in changed
        if path and not path.startswith(PACKAGE + "/") and path not in ALLOWED_CONTROLS
    )
    if invalid:
        raise gate.GateError("SCOPE", invalid[0])
    if ALLOWED_CONTROLS - changed:
        raise gate.GateError("SCOPE", "missing-control")
    if "CANON.md" in changed:
        raise gate.GateError("SCOPE", "CANON.md")
    return sorted(changed)


def validate_controls(gate, corrupt: bool = False) -> dict[str, object]:
    required = {
        "LIVE.md": [PACKAGE, "WR-L WALL ARE DISTINCT", "VERIFIED-WITH-CAVEATS"],
        "HANDOFF.md": [PACKAGE, "finite proper radius `2X`", "scale-breaking condition"],
        "INDEX.md": [PACKAGE, "GLOBAL_CLOSURE_EQUATION_LEDGER.tsv"],
        "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md": [PACKAGE, "raw lapse flux", "common rescaling"],
    }
    details = []
    for number, (path, tokens) in enumerate(required.items()):
        text = (ROOT / path).read_text(encoding="utf-8")
        if corrupt and number == 0:
            text = text.replace(PACKAGE, "missing_boundary_audit")
        if not all(token in text for token in tokens):
            raise gate.GateError("CONTROLS", path)
        details.append({"path": path, "sha256": gate.digest(text.encode("utf-8"))})
    return {"count": len(details), "files": details, "result": "PASS"}


def validate_execution(gate, corrupt: bool = False) -> dict[str, object]:
    ledger = rows(HERE / "EXECUTION_LEDGER.tsv")
    expected = {
        "E01": ("CPU_ONLY", "0"),
        "E02": ("CPU_ONLY", "0"),
        "E03": ("CPU_ONLY", "0"),
        "E04": ("CPU_ONLY", "0"),
        "E05": ("EXTERNAL_REVIEW_NOT_PERFORMED", "1_AUTHORIZATION_GATE"),
        "E06": ("CPU_ONLY", "1_EXPECTED_BASELINE"),
    }
    if len(ledger) != 6 or {row["id"] for row in ledger} != set(expected):
        raise gate.GateError("LEDGER", "census")
    for number, row in enumerate(ledger):
        observed = gate.digest((HERE / row["output_artifact"]).read_bytes())
        if corrupt and number == 0:
            observed = "0" * 64
        if (row["compute"], row["exit_code"]) != expected[row["id"]] or observed != row["output_sha256"]:
            raise gate.GateError("LEDGER", row["id"])
    return {"rows": len(ledger), "result": "PASS"}


def validate_science() -> dict[str, object]:
    source = HERE / "verify_boundary_lineage.py"
    spec = importlib.util.spec_from_file_location("boundary_lineage_verifier", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load boundary verifier")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.main()
    result = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    if result["result"] != "PASS" or result["counts"]["catch_proofs"] != 12:
        raise AssertionError("science verifier failed")
    return {"result": "PASS", "checks": len(result["checks"]), "catch_proofs": 12}


def main() -> None:
    gate = load_gate_module()
    universe = rows(ROOT / PREMISE_PACKAGE / "PACKAGE_UNIVERSE.tsv")
    prior = {row["package"]: row["manifest_sha256"] for row in universe}
    prior[PREMISE_PACKAGE] = PREMISE_MANIFEST

    scope = changed_paths(gate)
    controls = validate_controls(gate)
    execution = validate_execution(gate)
    science = validate_science()
    frozen = gate.validate_frozen(ROOT)
    prior_result = gate.replay_packages(ROOT, prior, "PRIOR")
    if prior_result["entries"] != 368:
        raise gate.GateError("PRIOR", f"entries:{prior_result['entries']}")
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
        "schema": "udt-asymptotic-boundary-lineage-repository-gates-1.0",
        "base": BASE,
        "result": "PASS",
        "scope_paths": scope,
        "controls": controls,
        "execution_ledger": execution,
        "science_verifier": science,
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
            "startup_controls_changed": True,
            "fold_wrl_identity_claimed": False,
            "wrl_x_promoted_to_global_xmax": False,
            "raw_flux_promoted_to_mass": False,
            "gr_mass_promoted_to_native": False,
            "absolute_scale_derived": False,
            "external_model_review_performed": False,
            "action_source_carrier_or_boundary_constructed": False,
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

#!/usr/bin/env python3
"""Independent fail-closed verification of the consolidation checkpoint."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CONTROLS = (
    "LIVE.md",
    "HANDOFF.md",
    "INDEX.md",
    "README.md",
    "AGENTS.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
    "research/README.md",
    "MEMORY.md",
)
CHECKPOINT = "udt_scientific_consolidation_checkpoint_2026-07-23"
EXPECTED_STATUS = {
    "C01": "DERIVED",
    "C02": "DERIVED",
    "C03": "DERIVED",
    "C04": "DERIVED",
    "C05": "OPEN",
    "C06": "VERIFIED-WITH-CAVEATS",
    "C07": "UNIQUE-CONDITIONAL",
    "C08": "CONDITIONAL",
    "C09": "POSIT",
    "C10": "SETTLED_STATIC_FINITE_BOX_CONDITIONAL",
    "C11": "OPEN",
    "C12": "OPEN",
    "C13": "OPEN",
    "C14": "OPEN",
    "C15": "OPEN",
    "C16": "OPEN",
    "C17": "OPEN",
    "C18": "OPEN",
    "C19": "WORKING",
    "C20": "DERIVED-GEOMETRIC",
    "C21": "CONDITIONAL-STATIC-SLICE",
    "C22": "OPEN_NOT_JOINED",
    "C23": "OPEN",
    "C24": "OPEN",
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate(
    statuses: list[dict[str, str]],
    controls: dict[str, str],
    guards: list[dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    status_map = {row["id"]: row for row in statuses}
    if len(statuses) != 24 or len(status_map) != 24:
        errors.append("status_identity_coverage")
    for item, grade in EXPECTED_STATUS.items():
        if status_map.get(item, {}).get("status") != grade:
            errors.append(f"status:{item}")
    if status_map.get("C15", {}).get("evidence_path") != (
        "scale_breaking_closure_census_2026-07-20/STATUS_LEDGER.tsv"
    ):
        errors.append("status:C15_evidence")
    if len(guards) != 15 or len({row["id"] for row in guards}) != 15:
        errors.append("guard_identity_coverage")
    for path in CONTROLS:
        if CHECKPOINT not in controls.get(path, ""):
            errors.append(f"checkpoint_pointer:{path}")
    for path in ("LIVE.md", "HANDOFF.md"):
        text = controls.get(path, "")
        if text.count("STARTUP_CURRENT_BEGIN") != 1 or text.count("STARTUP_CURRENT_END") != 1:
            errors.append(f"startup_markers:{path}")
        else:
            bounded = text.split("STARTUP_CURRENT_BEGIN", 1)[1].split(
                "STARTUP_CURRENT_END", 1
            )[0]
            if len(bounded.splitlines()) > 60:
                errors.append(f"startup_not_lean:{path}")
    live = controls.get("LIVE.md", "")
    required_live = (
        "ZERO COMPLETE ONSHELL",
        "KATO TRANSPORT IS GEOMETRIC, NOT PHYSICAL TIME",
        "NO COMPLETION IS SELECTED",
        "REORGANIZATION:",
    )
    if any(token not in live for token in required_live):
        errors.append("live_scope_loss")
    handoff = controls.get("HANDOFF.md", "")
    if "no complete on-shell `(g,phi)` finite-cell branch" not in " ".join(
        handoff.split()
    ):
        errors.append("handoff_solution_overclaim")
    return errors


def validate_source_bindings(
    bindings: list[dict[str, str]],
    status_ids: set[str],
) -> list[str]:
    errors: list[str] = []
    binding_ids = [row.get("binding_id", "") for row in bindings]
    if len(bindings) != 30 or len(set(binding_ids)) != 30:
        errors.append("source_binding_identity_coverage")
    covered = {row.get("current_id", "") for row in bindings}
    if covered != status_ids:
        errors.append("source_binding_current_coverage")
    scale_expected = {
        ("S04", "REFUTED_BY_DIMENSION_AND_RANK"),
        ("S14", "NOT_FOUND_IN_AUDITED_CURRENT_FOUNDATION"),
        ("S15", "OPEN"),
    }
    scale_actual = {
        (row.get("key_value", ""), row.get("expected_value", ""))
        for row in bindings
        if row.get("current_id") == "C15"
        and row.get("source_path")
        == "scale_breaking_closure_census_2026-07-20/STATUS_LEDGER.tsv"
    }
    if scale_actual != scale_expected:
        errors.append("absolute_scale_binding_exactness")
    cache: dict[str, list[dict[str, str]]] = {}
    for binding in bindings:
        source = binding.get("source_path", "")
        path = ROOT / source
        if not path.exists():
            errors.append(f"source_binding_missing:{binding.get('binding_id', '')}")
            continue
        if source not in cache:
            cache[source] = read_tsv(path)
        key = binding.get("key_column", "")
        value = binding.get("key_value", "")
        matches = [row for row in cache[source] if row.get(key) == value]
        if len(matches) != 1:
            errors.append(f"source_binding_row:{binding.get('binding_id', '')}")
            continue
        field = binding.get("field", "")
        if matches[0].get(field) != binding.get("expected_value", ""):
            errors.append(f"source_binding_value:{binding.get('binding_id', '')}")
    return errors


def validate_source_additions(
    additions: list[dict[str, str]],
) -> list[str]:
    expected = {
        "id": "S26",
        "path": "scale_breaking_closure_census_2026-07-20/STATUS_LEDGER.tsv",
        "role": "absolute_scale_status_and_dimensional_theorem",
    }
    if additions != [expected]:
        return ["second_pass_source_addition"]
    if not ROOT.joinpath(expected["path"]).exists():
        return ["second_pass_source_addition_missing"]
    return []


def validate_rehearsal(rehearsal: dict[str, object]) -> list[str]:
    errors: list[str] = []
    checks = rehearsal.get("checks", {})
    context = rehearsal.get("repository_context", {})
    if rehearsal.get("all_checks_pass") is not True:
        errors.append("rehearsal_checks")
    if not isinstance(checks, dict) or len(checks) != 17:
        errors.append("rehearsal_check_count")
    if rehearsal.get("method") != (
        "deterministic_parser_no_conversational_context_no_external_model"
    ):
        errors.append("rehearsal_method")
    if "head" in rehearsal or "worktree_status" in rehearsal:
        errors.append("volatile_git_metadata")
    if not isinstance(context, dict) or context != {
        "git_state_verified_by": "verify_repository_gates.py",
        "required_branch": "grok",
        "volatile_git_metadata_embedded": False,
    }:
        errors.append("rehearsal_repository_context")
    return errors


def main() -> None:
    checks: list[dict[str, object]] = []

    def check(name: str, condition: bool, detail: object = "") -> None:
        checks.append({"name": name, "pass": bool(condition), "detail": detail})

    statuses = read_tsv(HERE / "CURRENT_STATUS_LEDGER.tsv")
    status_ids = {row["id"] for row in statuses}
    guards = read_tsv(HERE / "REGRESSION_GUARD_LEDGER.tsv")
    maps = read_tsv(HERE / "METRIC_TO_FRONTIER_MAP.tsv")
    controls = {path: ROOT.joinpath(path).read_text(encoding="utf-8") for path in CONTROLS}
    errors = validate(statuses, controls, guards)
    check("checkpoint_contract", not errors, errors)

    corrections = read_tsv(HERE / "POST_COMMIT_STATUS_CORRECTIONS.tsv")
    correction_map = {row["id"]: row for row in corrections}
    check(
        "post_commit_status_corrections",
        len(corrections) == 2
        and len(correction_map) == 2
        and correction_map.get("C10", {}).get("corrected_current_status")
        == "SETTLED_STATIC_FINITE_BOX_CONDITIONAL"
        and correction_map.get("C22", {}).get("corrected_current_status")
        == "OPEN_NOT_JOINED",
        correction_map,
    )

    bindings = read_tsv(HERE / "SOURCE_STATUS_BINDINGS.tsv")
    binding_errors = validate_source_bindings(bindings, status_ids)
    check("source_status_bindings", not binding_errors, binding_errors)
    lineage_paths = {
        row["path"] for row in read_tsv(HERE / "SOURCE_LINEAGE.tsv")
    }
    check(
        "source_binding_lineage_coverage",
        all(row["source_path"] in lineage_paths for row in bindings),
    )

    lineage = read_tsv(HERE / "SOURCE_LINEAGE.tsv")
    check(
        "source_lineage_count",
        len(lineage) == 26
        and len({row["id"] for row in lineage}) == 26
        and len({row["path"] for row in lineage}) == 26,
    )
    lineage_ok = all(
        ROOT.joinpath(row["path"]).exists()
        and len(ROOT.joinpath(row["path"]).read_bytes()) == int(row["bytes"])
        and hashlib.sha256(ROOT.joinpath(row["path"]).read_bytes()).hexdigest()
        == row["sha256"]
        for row in lineage
    )
    check("source_lineage_exact_bytes", lineage_ok)
    check("status_evidence_resolves", all(ROOT.joinpath(row["evidence_path"]).exists() for row in statuses))
    check("map_evidence_resolves", len(maps) == 13 and all(ROOT.joinpath(row["evidence_path"]).exists() for row in maps))
    check("guard_evidence_resolves", all(ROOT.joinpath(row["evidence_path"]).exists() for row in guards))

    finite = json.loads(
        ROOT.joinpath(
            "udt_finite_cell_cartan_transport_atlas_2026-07-23/DERIVATION_RESULT.json"
        ).read_text()
    )
    check("finite_cell_counts", finite["counts"] == {
        "causal_classes": 5,
        "complete_onshell_g_phi_branches": 0,
        "completion_causal_cross": 60,
        "completion_families": 12,
        "connection_domains": 4,
        "transition_witnesses": 8,
    }, finite["counts"])
    cross = read_tsv(
        ROOT
        / "udt_finite_cell_cartan_transport_atlas_2026-07-23"
        / "COMPLETION_CAUSAL_CROSS.tsv"
    )
    check("finite_cell_cross_unique", len(cross) == 60 and len({(row["completion_id"], row["causal_class"]) for row in cross}) == 60)

    current_paths = read_tsv(ROOT / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv")
    classifications = read_tsv(ROOT / "research/_registry/CURRENT_CLASSIFICATION.tsv")
    check("fixed_identity_counts", len(current_paths) == 1114 and len(classifications) == 1114, [len(current_paths), len(classifications)])

    corrected = read_tsv(HERE / "CORRECTED_SOURCE_UNIVERSE.tsv")
    corrected_map = {row["id"]: row["path"] for row in corrected}
    check(
        "preregistration_correction_exact",
        len(corrected) == 25
        and corrected_map["S21"]
        == "native_hopfion_topology_audit_2026-07-19/TOPOLOGY_STATUS_LEDGER.tsv",
    )
    additions = read_tsv(HERE / "SECOND_PASS_SOURCE_ADDITIONS.tsv")
    addition_errors = validate_source_additions(additions)
    check(
        "second_pass_source_addition",
        not addition_errors,
        addition_errors,
    )
    rehearsal = json.loads(
        HERE.joinpath("ZERO_STATE_REHEARSAL_RESULT.json").read_text(encoding="utf-8")
    )
    rehearsal_errors = validate_rehearsal(rehearsal)
    check(
        "zero_state_rehearsal",
        not rehearsal_errors,
        rehearsal_errors,
    )

    catches: list[dict[str, object]] = []

    def catch(name: str, mutator) -> None:
        s, c, g = deepcopy(statuses), deepcopy(controls), deepcopy(guards)
        mutator(s, c, g)
        catches.append({"name": name, "pass": bool(validate(s, c, g))})

    index = {row["id"]: i for i, row in enumerate(statuses)}
    catch("reject_missing_status", lambda s, c, g: s.pop())
    catch("reject_duplicate_status", lambda s, c, g: s.__setitem__(1, deepcopy(s[0])))
    catch("reject_action_promotion", lambda s, c, g: s[index["C11"]].__setitem__("status", "DERIVED"))
    catch("reject_representative_promotion", lambda s, c, g: s[index["C14"]].__setitem__("status", "SELECTED"))
    catch("reject_carrier_promotion", lambda s, c, g: s[index["C09"]].__setitem__("status", "DERIVED"))
    catch("reject_solved_branch_promotion", lambda s, c, g: s[index["C23"]].__setitem__("status", "DERIVED"))
    catch("reject_spacelike_observer_promotion", lambda s, c, g: s[index["C03"]].__setitem__("status", "DERIVED-OBSERVER"))
    catch("reject_null_semisimple_promotion", lambda s, c, g: s[index["C04"]].__setitem__("status", "DERIVED-SEMISIMPLE"))
    catch("reject_Kato_physical_time", lambda s, c, g: s[index["C20"]].__setitem__("status", "DERIVED-PHYSICAL-TIME"))
    catch("reject_C10_unconditional_promotion", lambda s, c, g: s[index["C10"]].__setitem__("status", "DERIVED"))
    catch("reject_C22_identity_promotion", lambda s, c, g: s[index["C22"]].__setitem__("status", "DERIVED_IDENTITY"))
    catch(
        "reject_stale_C15_evidence",
        lambda s, c, g: s[index["C15"]].__setitem__(
            "evidence_path",
            "matter_bootstrap_dimensional_inventory_2026-07-20/STATUS_LEDGER.tsv",
        ),
    )
    catch("reject_missing_regression_guard", lambda s, c, g: g.pop())
    catch("reject_stale_LIVE_pointer", lambda s, c, g: c.__setitem__("LIVE.md", c["LIVE.md"].replace(CHECKPOINT, "stale_checkpoint")))
    catch("reject_stale_HANDOFF_pointer", lambda s, c, g: c.__setitem__("HANDOFF.md", c["HANDOFF.md"].replace(CHECKPOINT, "stale_checkpoint")))
    catch("reject_duplicate_LIVE_marker", lambda s, c, g: c.__setitem__("LIVE.md", c["LIVE.md"] + "\nSTARTUP_CURRENT_BEGIN\n"))
    catch("reject_nonlean_HANDOFF", lambda s, c, g: c.__setitem__("HANDOFF.md", c["HANDOFF.md"].replace("STARTUP_CURRENT_END", "\n".join(["padding"] * 70) + "\nSTARTUP_CURRENT_END")))

    def source_catch(name: str, mutated: list[dict[str, str]]) -> None:
        catches.append(
            {
                "name": name,
                "pass": bool(validate_source_bindings(mutated, status_ids)),
            }
        )

    source_missing = deepcopy(bindings)
    source_missing.pop()
    source_catch("reject_missing_source_binding", source_missing)
    source_duplicate = deepcopy(bindings)
    source_duplicate[1]["binding_id"] = source_duplicate[0]["binding_id"]
    source_catch("reject_duplicate_source_binding", source_duplicate)
    source_wrong = deepcopy(bindings)
    source_wrong[0]["expected_value"] = "PROMOTED"
    source_catch("reject_wrong_parent_status", source_wrong)
    source_identity_loss = [
        row for row in deepcopy(bindings) if row["current_id"] != "C24"
    ]
    source_catch("reject_unbound_current_identity", source_identity_loss)
    source_scale_loss = [
        row for row in deepcopy(bindings) if row["current_id"] != "C15"
    ]
    source_catch("reject_missing_scale_binding", source_scale_loss)
    catches.append(
        {
            "name": "reject_missing_source_addition",
            "pass": bool(validate_source_additions([])),
        }
    )
    volatile_rehearsal = deepcopy(rehearsal)
    volatile_rehearsal["head"] = "0" * 40
    catches.append(
        {
            "name": "reject_volatile_rehearsal_metadata",
            "pass": bool(validate_rehearsal(volatile_rehearsal)),
        }
    )
    check("all_exercised_catches_pass", all(row["pass"] for row in catches), catches)

    output = {
        "schema": "udt-scientific-consolidation-independent-1.0",
        "python": sys.version.split()[0],
        "implementation": "stdlib_independent_no_builder_import",
        "all_checks_pass": all(row["pass"] for row in checks),
        "check_count": len(checks),
        "checks": checks,
        "all_catches_pass": all(row["pass"] for row in catches),
        "catch_count": len(catches),
        "catches": catches,
    }
    HERE.joinpath("INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "all_checks_pass": output["all_checks_pass"],
        "check_count": output["check_count"],
        "all_catches_pass": output["all_catches_pass"],
        "catch_count": output["catch_count"],
    }, indent=2, sort_keys=True))
    raise SystemExit(0 if output["all_checks_pass"] and output["all_catches_pass"] else 1)


if __name__ == "__main__":
    main()

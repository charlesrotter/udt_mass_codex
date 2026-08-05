#!/usr/bin/env python3
"""Fail-closed verifier for the relational-phi dependency regrade."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUTPUT = HERE / "VERIFICATION_RESULT.json"
EXPECTED_DISPOSITIONS = {
    "CONCLUSION_REGRADE_REQUIRED": 99,
    "CONDITIONAL_REINTERPRETATION_ONLY": 1091,
    "CONTROL_UPDATE_REQUIRED": 13,
    "FROZEN_EVIDENCE_IMMUTABLE": 40,
    "HISTORICAL_SUPERSEDED_NO_ACTION": 335,
    "NO_RELEVANT_SEMANTIC_DEPENDENCY": 1994,
    "OPEN_DEPENDENCY_ALREADY_STAMPED": 741,
    "UNCHANGED_NEGATIVE_NOW_EXPLANATORY": 418,
    "UNCHANGED_NO_OWNERSHIP_DEPENDENCY": 31,
}
EXPECTED_CONTROLS = {
    "AGENTS.md", "CURRENT_SCIENTIFIC_PREMISES.md", "CURRENT_SCIENTIFIC_PREMISES.tsv",
    "HANDOFF.md", "INDEX.md", "LIVE.md", "MEMORY.md", "NEGATIVES_REGISTRY.md", "README.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md", "research/README.md",
    "research/_registry/README.md", "verify_current_scientific_premises.py",
}
REGRADED_PREFIX_COUNTS = {
    "finite_cell_seal_boundary_phase_join_2026-07-20/": 18,
    "scale_breaking_closure_census_2026-07-20/": 5,
    "udt_phi_metric_ontology_audit_2026-07-22/": 19,
    "udt_premise_reset_audit_2026-07-19/": 11,
    "udt_reciprocal_c_metric_meaning_audit_2026-07-22/": 14,
    "udt_reciprocal_subbundle_ownership_audit_2026-07-22/": 15,
    "udt_two_frame_regime_metric_limit_audit_2026-07-22/": 17,
}
EXPECTED_ACTIVE_SHA = "e5e43aa069a1cfbda0db72346cb89023b530317c68049554bb11f5fe0e367518"
EXPECTED_FAMILY_SHA = "69408f2a5e9a65de2beb8a016c502de76b798afce18c116b9ef437f54c39279d"
EXPECTED_SIGN = "delta_K=log(N(p)/N(q))"
OLD_LEDGER_COMMIT = "b9497e3cf4c0b706db835c5edf7af17846838082"
OLD_LEDGER_SHA256 = "b77eea4240b7e3ab97ba97c5dbadfbfa10f5c1803785eb8790545050aedaf651"
EXPECTED_DATE_RULE_SHA = "e85e3a26940e9369dd7ff6b24da33c2cac493de9f19084e671d9f48870fc4e98"
CURRENT_FOUNDING_CHAIN = {
    "UDT_NATIVE_ACTION_COLD_PACKET.md",
    "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md",
    "verify_udt_reciprocal_c_postulate.py",
}


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity_sha(paths: list[str]) -> str:
    return hashlib.sha256(("\n".join(paths) + "\n").encode()).hexdigest()


def family_sha(ledger: list[dict[str, str]]) -> str:
    payload = "".join(
        f"{row['path']}\t{row['family_id']}\t{row['disposition']}\n" for row in ledger
    )
    return hashlib.sha256(payload.encode()).hexdigest()


def validate_ledger(ledger: list[dict[str, str]]) -> None:
    assert len(ledger) == 4762, "missing or extra active row"
    paths = [row["path"] for row in ledger]
    assert len(paths) == len(set(paths)), "duplicate active identity"
    assert paths == sorted(paths), "ledger order changed"
    assert Counter(row["disposition"] for row in ledger) == Counter(EXPECTED_DISPOSITIONS), "disposition drift"
    assert family_sha(ledger) == EXPECTED_FAMILY_SHA, "family identity drift"
    assert not any(row["family_id"] == "F20_POSTJULY_UNMATCHED" for row in ledger), "fallback family remains"
    assert not any(row["disposition"] == "REDERIVATION_REQUIRED" for row in ledger), "false rederivation promotion"


def validate_premise(g01: dict[str, str], sign: str) -> None:
    assert g01["current_status"] == "DERIVED_RECIPROCAL_CHARACTER_ON_SUPPLIED_ORDERED_DEPTH"
    assert "general observer/event/path-to-depth law" in g01["open_scope"]
    assert "universal pointwise physical scalar" in g01["forbidden_regression"]
    assert sign == EXPECTED_SIGN, "stationary Killing sign regression"


def validate_negatives(negatives: list[dict[str, str]]) -> None:
    assert len(negatives) == 3
    assert len({row["negative_id"] for row in negatives}) == 3
    assert all(row["current_authority"] == "CONDITIONS_CHANGED_NONBLOCKING_OUTSIDE_SUPPLIED_BRANCH" for row in negatives)


def expect_failure(name: str, operation, caught: list[str]) -> None:
    try:
        operation()
    except (AssertionError, KeyError, ValueError):
        caught.append(name)
        return
    raise AssertionError(f"mutation escaped: {name}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    frozen = json.loads((HERE / "FROZEN_UNIVERSE.json").read_text(encoding="utf-8"))
    active = rows("ACTIVE_REGRADE_UNIVERSE.tsv")
    ledger = rows("ACTIVE_REGRADING_LEDGER.tsv")
    validate_ledger(ledger)
    assert len(active) == 4762 and [row["path"] for row in active] == [row["path"] for row in ledger]
    assert identity_sha([row["path"] for row in active]) == EXPECTED_ACTIVE_SHA
    assert frozen["active_identity_sha256"] == EXPECTED_ACTIVE_SHA
    assert frozen["full_exposure_count"] == 5354 and frozen["active_regrade_count"] == 4762
    for name, expected in frozen["hashes"].items():
        assert digest(HERE / name) == expected, f"frozen preregistration/census drift: {name}"

    summary = json.loads((HERE / "REGRADING_SUMMARY.json").read_text(encoding="utf-8"))
    assert summary["disposition_counts"] == EXPECTED_DISPOSITIONS
    assert summary["family_identity_sha256"] == EXPECTED_FAMILY_SHA
    assert summary["focused_path_count"] == summary["manual_or_family_reviewed_count"] == 2152
    assert summary["rederivation_required_count"] == 0

    controls = {row["path"] for row in ledger if row["disposition"] == "CONTROL_UPDATE_REQUIRED"}
    assert controls == EXPECTED_CONTROLS
    assert {row["path"] for row in rows("CONTROL_CORRECTION_LEDGER.tsv")} == EXPECTED_CONTROLS

    regraded = [row for row in ledger if row["disposition"] == "CONCLUSION_REGRADE_REQUIRED"]
    actual_prefix_counts = Counter()
    for row in regraded:
        matching = [prefix for prefix in REGRADED_PREFIX_COUNTS if row["path"].startswith(prefix)]
        assert len(matching) == 1, f"unregistered conclusion regrade: {row['path']}"
        actual_prefix_counts[matching[0]] += 1
    assert dict(actual_prefix_counts) == REGRADED_PREFIX_COUNTS

    # Frozen and superseded evidence remains byte-identical to the frozen source ledger.
    immutable = [row for row in ledger if row["disposition"] in {
        "FROZEN_EVIDENCE_IMMUTABLE", "HISTORICAL_SUPERSEDED_NO_ACTION"
    }]
    assert len(immutable) == 375
    for row in immutable:
        assert digest(ROOT / row["path"]) == row["source_sha256"], f"immutable evidence drift: {row['path']}"

    premise = {row["premise_id"]: row for row in rows("../CURRENT_SCIENTIFIC_PREMISES.tsv")}
    validate_premise(premise["G01"], EXPECTED_SIGN)
    assert premise["G02"]["current_status"] == "DERIVED_DELTA_MAPS_TO_DIAG_EXP_MINUS_DELTA_EXP_PLUS_DELTA"
    validate_negatives(rows("NEGATIVE_REGRADING.tsv"))

    claims = rows("LOAD_BEARING_CLAIM_REGRADING.tsv")
    assert len(claims) == 15 and len({row["claim_id"] for row in claims}) == 15
    locators = rows("LOAD_BEARING_SOURCE_LOCATORS.tsv")
    assert len(locators) == 22 and len({row["locator_id"] for row in locators}) == 22
    for row in locators:
        assert row["snapshot_semantics"] in {"CURRENT_CITED_CONTENT", "BASE_682ADB6C_PRE_CORRECTION"}
        source = ROOT / row["path"]
        assert source.is_file()
        if row["snapshot_semantics"] == "BASE_682ADB6C_PRE_CORRECTION":
            content = subprocess.check_output(
                ["git", "show", f"682adb6c9d4cc7c9834cb5ea6a7712a32206650b:{row['path']}"],
                cwd=ROOT,
            ).decode("utf-8", errors="replace")
        else:
            content = source.read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines()
        assert 1 <= int(row["line_start"]) <= int(row["line_end"]) <= len(lines)
    assert {row["locator_id"] for row in locators if row["snapshot_semantics"] == "BASE_682ADB6C_PRE_CORRECTION"} == {
        "L13", "L14", "L15", "L16", "L17", "L18"
    }
    assert len(rows("POST_CORRECTION_SOURCE_LOCATORS.tsv")) == 7

    date_rows = rows("DATE_RULE_ADJUDICATION.tsv")
    assert len(date_rows) == 254 and len({row["path"] for row in date_rows}) == 254
    old_relative = f"{HERE.name}/ACTIVE_REGRADING_LEDGER.tsv"
    old_payload = subprocess.check_output(
        ["git", "show", f"{OLD_LEDGER_COMMIT}:{old_relative}"], cwd=ROOT
    )
    assert hashlib.sha256(old_payload).hexdigest() == OLD_LEDGER_SHA256
    old_ledger = list(csv.DictReader(io.StringIO(old_payload.decode("utf-8")), delimiter="\t"))
    old_f18_paths = [row["path"] for row in old_ledger if row["family_id"] == "F18_EARLY_POSTJULY_FIELD_SOLVER"]
    assert [row["path"] for row in date_rows] == old_f18_paths
    assert identity_sha(old_f18_paths) == EXPECTED_DATE_RULE_SHA
    corrected_current = {
        row["path"] for row in date_rows
        if row["corrected_disposition"] == "CONDITIONAL_REINTERPRETATION_ONLY"
    }
    assert corrected_current == CURRENT_FOUNDING_CHAIN
    by_path = {row["path"]: row for row in ledger}
    assert all(by_path[path]["family_id"] == "F02A_CURRENT_FOUNDING_CHAIN" for path in CURRENT_FOUNDING_CHAIN)
    assert all(by_path[path]["disposition"] == "CONDITIONAL_REINTERPRETATION_ONLY" for path in CURRENT_FOUNDING_CHAIN)

    rerun = json.loads((HERE / "RERUN_RESULT.json").read_text(encoding="utf-8"))
    assert rerun["commands_expected"] == rerun["commands_completed"] == 11 and rerun["all_exit_zero"]
    for record in rerun["records"]:
        assert record["exit_code"] == 0 and record["stderr_bytes"] == 0
        assert digest(HERE / record["stdout_file"]) == record["stdout_sha256"]
        assert digest(HERE / record["stderr_file"]) == record["stderr_sha256"]

    for name in ("LIVE.md", "HANDOFF.md"):
        text = (ROOT / name).read_text(encoding="utf-8")
        current = text.split("<!-- STARTUP_CURRENT_BEGIN -->", 1)[1].split("<!-- STARTUP_CURRENT_END -->", 1)[0]
        assert HERE.name in current and "general two-observer depth law" in current.lower()
        lowered = " ".join(current.lower().split())
        assert (
            "no current load-bearing algebra" in lowered
            or "zero current load-bearing algebra" in lowered
        )
    registry = (ROOT / "NEGATIVES_REGISTRY.md").read_text(encoding="utf-8")
    assert registry.count("CONDITIONS-CHANGED 2026-08-05") == 3
    assert "zero UDT-wide blocking authority" in registry

    caught: list[str] = []
    expect_failure("missing_active_row", lambda: validate_ledger(ledger[:-1]), caught)
    expect_failure("duplicate_active_identity", lambda: validate_ledger(ledger[:-1] + [ledger[0]]), caught)
    changed = [dict(row) for row in ledger]
    changed[0]["disposition"] = "REDERIVATION_REQUIRED"
    expect_failure("false_rederivation_promotion", lambda: validate_ledger(changed), caught)
    bad_g01 = dict(premise["G01"])
    bad_g01["current_status"] = "DERIVED_UNIVERSAL_POINTWISE_PHI_FIELD"
    expect_failure("pointwise_owner_promotion", lambda: validate_premise(bad_g01, EXPECTED_SIGN), caught)
    expect_failure("stationary_sign_reversal", lambda: validate_premise(premise["G01"], "delta_K=log(N(q)/N(p))"), caught)
    bad_negatives = [dict(row) for row in rows("NEGATIVE_REGRADING.tsv")]
    bad_negatives[0]["current_authority"] = "UDT_WIDE_BLOCKER"
    expect_failure("negative_authority_promotion", lambda: validate_negatives(bad_negatives), caught)
    frozen_probe = dict(frozen["hashes"])
    frozen_probe["PREREGISTRATION.md"] = "0" * 64
    expect_failure(
        "frozen_preregistration_mutation",
        lambda: [(_ for _ in ()).throw(AssertionError()) for name, expected in frozen_probe.items() if digest(HERE / name) != expected],
        caught,
    )
    bad_locator = [dict(row) for row in locators]
    bad_locator[12]["snapshot_semantics"] = ""
    expect_failure(
        "locator_snapshot_semantics_removed",
        lambda: [
            (_ for _ in ()).throw(AssertionError())
            for row in bad_locator
            if row["snapshot_semantics"] not in {"CURRENT_CITED_CONTENT", "BASE_682ADB6C_PRE_CORRECTION"}
        ],
        caught,
    )
    bad_chain = [dict(row) for row in ledger]
    next(row for row in bad_chain if row["path"] in CURRENT_FOUNDING_CHAIN)["disposition"] = "HISTORICAL_SUPERSEDED_NO_ACTION"
    expect_failure("founding_chain_rehistorized", lambda: validate_ledger(bad_chain), caught)
    assert len(caught) == 9

    result = {
        "schema": "udt.relational_phi_regrade.verification.v1",
        "status": "PASS",
        "active_rows": len(ledger),
        "active_identity_sha256": EXPECTED_ACTIVE_SHA,
        "family_identity_sha256": EXPECTED_FAMILY_SHA,
        "conclusion_regraded_rows": len(regraded),
        "control_rows": len(controls),
        "frozen_rows": 40,
        "historical_rows": 335,
        "rederivation_required_rows": 0,
        "clean_tree_reruns": 11,
        "catch_proofs": caught,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write:
        OUTPUT.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()

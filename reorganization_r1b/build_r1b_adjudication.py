#!/usr/bin/env python3
"""Apply the preregistered R1B classification and safety-stop contract."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ELIGIBLE = {
    "STEP2_timelive_matter_MAP.md": (
        "PRE_NATIVE_STEP2_FAMILY",
        "Pre-native scalar-tensor STEP2 family explicitly SUPERSEDED; the only operational root reference becomes a valid co-located archive reference.",
        "pre_native_era_census.md:78-80",
    ),
    "p4_VERIFIER.md": (
        "PRE_NATIVE_P2_P4_VERIFIER_FAMILY",
        "File banner and census identify this frame-B verifier as CONDITIONS-CHANGED/superseded; its one operational pointer is mutable navigation.",
        "p4_VERIFIER.md:1-5;pre_native_era_census.md:48-49",
    ),
}

MANUAL = {
    "AUDIT.md": (
        "ACTIVE_CROSS_ERA", "CANON_PROVENANCE", "Surviving native operator claim remains canon provenance; only the dispatch headline is conditions-changed.", "CANON.md:63-64;macro_spine_provenance_2026-07-06.md:38,52-54"
    ),
    "D1_FIX_DESIGN.md": (
        "HISTORICAL_SNAPSHOT", "PRE_NATIVE_REDIRECT_STUBS", "Root file is an intentional redirect stub to the archived original and is still named by frozen/code sources.", "D1_FIX_DESIGN.md:1-3"
    ),
    "F4_seal_boundary_MAP.md": (
        "ACTIVE_CROSS_ERA", "CURRENT_FOUNDATION_CROSS_ERA", "Finite-cell/seal boundary question remains an open native-action selector and is cited by formal frozen evidence.", "F4_seal_boundary_MAP.md:1,10;UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md"
    ),
    "GR_NUMERICS_RESEARCH_2026-06-29.md": (
        "SOFT_EVIDENCE_PATH_ONLY", "SOFT_CLEAN_TECHNIQUE", "Clean category-A numerical research, not affirmatively superseded as a whole; retain without prose edits.", "pre_native_era_census.md:90"
    ),
    "MATTER_SECTOR_MAP_new_foundation.md": (
        "ACTIVE_CROSS_ERA", "CURRENT_FOUNDATION_CROSS_ERA", "Cross-era matter provenance map remains cited by formal frozen foundation evidence.", "F2_closure_results.md:14-17"
    ),
    "P1_PURITY_HARNESS_MAP.md": (
        "ACTIVE_CROSS_ERA", "LIVE_GOVERNANCE_AND_TEST_INFRA", "Design remains coupled to the live solver-integrity test and frozen P1 result.", "P1_PURITY_HARNESS_MAP.md:122-129;tests/test_solver_integrity.py"
    ),
    "P5e_proper_results.md": (
        "BLOCKED", "SUPERSEDED_BUT_PATH_BLOCKED", "Explicitly superseded, but formal frozen evidence requires the root path.", "P5e_proper_results.md:1-4;F8_metric_choices_results.md"
    ),
    "QUANTIZATION_MAP.md": (
        "ACTIVE_CROSS_ERA", "CURRENT_FOUNDATION_CROSS_ERA", "Postulate-A boundary remains cited by the formal frozen F6 ledger and STATE.", "F6_postulate_A_ledger_results.md:10-13,49-55"
    ),
    "SOLVER_INTEGRITY_UPGRADES_SPEC.md": (
        "ACTIVE_CROSS_ERA", "LIVE_GOVERNANCE_AND_TEST_INFRA", "Implemented solver-integrity specification remains part of the live harness history and navigation.", "HANDOFF_ARCHIVE.md:50-54"
    ),
    "TRACTABILITY_ROUTES.md": (
        "ACTIVE_CROSS_ERA", "LIVE_GOVERNANCE_AND_TEST_INFRA", "Clean category-A technique guidance remains valid across eras; it is not superseded physics.", "pre_native_era_census.md:90"
    ),
    "external_input_notes.md": (
        "ACTIVE_CROSS_ERA", "CANON_PROVENANCE", "The file remains provenance for a canonized fork resolution and is also named by hard-frozen transcripts.", "CANON.md:145-148"
    ),
    "lepton_ladder_falsification_contract.md": (
        "BLOCKED", "SUPERSEDED_BUT_PATH_BLOCKED", "The ladder family is explicitly superseded, but a retained Python falsification harness requires this root path.", "macro_spine_provenance_2026-07-06.md:44;legacy/root_oneoffs_2026-07-01/native_lepton_ladder_frozen_test.py"
    ),
    "matter_amplitude_native_MAP_2026-06-29.md": (
        "SOFT_EVIDENCE_PATH_ONLY", "SOFT_CLEAN_FOUNDATION_MAP", "Census grades this MAP clean and no base record affirmatively supersedes it as a whole.", "pre_native_era_census.md:59"
    ),
    "matter_regrade_derived_operator_results.md": (
        "BLOCKED", "SUPERSEDED_BUT_PATH_BLOCKED", "Explicitly superseded, but formal frozen results, Python, and tests require the root path.", "matter_regrade_derived_operator_results.md:1-5"
    ),
    "nonstationary_opener_results.md": (
        "BLOCKED", "SUPERSEDED_BUT_PATH_BLOCKED", "Conditions changed, while formal frozen result and retained legacy runtime sources require the root path.", "nonstationary_opener_results.md:1-5"
    ),
    "p1_VERIFIER.md": (
        "HISTORICAL_SNAPSHOT", "PRE_NATIVE_REDIRECT_STUBS", "Root file is an intentional redirect stub to the archived original and remains named by formal frozen evidence.", "p1_VERIFIER.md:1-3"
    ),
    "p2_VERIFIER.md": (
        "BLOCKED", "SUPERSEDED_BUT_PATH_BLOCKED", "Explicitly conditions-changed, but a formal frozen P3 result requires the root path.", "p2_VERIFIER.md:1-5;p3_aphi_coupling_results.md"
    ),
    "p3_VERIFIER.md": (
        "BLOCKED", "SUPERSEDED_BUT_PATH_BLOCKED", "Explicitly conditions-changed, but a formal frozen result and retained Python source require the root path.", "p3_VERIFIER.md:1-5;p3_aphi_FIX_results.md"
    ),
    "p4_VERIFIER.md": ("ARCHIVE_ELIGIBLE",) + ELIGIBLE["p4_VERIFIER.md"],
    "scale_symmetry_bootstrap_analysis_results.md": (
        "BLOCKED", "SUPERSEDED_BUT_PATH_BLOCKED", "Explicitly superseded, but three formal frozen foundation results require the root path.", "scale_symmetry_bootstrap_analysis_results.md:1-5"
    ),
    "solution_space_map.md": (
        "ACTIVE_CROSS_ERA", "CANON_PROVENANCE", "Clean cross-era solution-space record remains explicit canon provenance.", "CANON.md:102-104;pre_native_era_census.md:89"
    ),
    "STEP2_timelive_matter_MAP.md": ("ARCHIVE_ELIGIBLE",) + ELIGIBLE["STEP2_timelive_matter_MAP.md"],
    "weld_status_results.md": (
        "BLOCKED", "SUPERSEDED_BUT_PATH_BLOCKED", "Explicitly superseded, but formal frozen and retained Python sources require the root path.", "weld_status_results.md:1-3;macro_spine_provenance_2026-07-06.md:43"
    ),
}


def load(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write(path: Path, rows: list[dict[str, Any]], fields: tuple[str, ...]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            delimiter="\t",
            lineterminator="\n",
            extrasaction="ignore",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {field: str(row.get(field, "-")).replace("\t", "\\t").replace("\n", "\\n") for field in fields}
            )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--candidate-evidence", type=Path, required=True)
    parser.add_argument("--operational-references", type=Path, required=True)
    parser.add_argument("--permanent-registry", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    repo = args.repo.resolve()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    evidence = load(args.candidate_evidence)
    references = load(args.operational_references)
    permanent = {
        row["path"] for row in load(args.permanent_registry)
        if row["candidate_universe_status"] == "IN_CANDIDATE_UNIVERSE"
    }
    assert len(evidence) == 99
    assert len(MANUAL) == 23

    adjudication = []
    for row in evidence:
        path = row["path"]
        r0_class = row["r0_classification"]
        if path in MANUAL:
            classification, family, rationale, affirmative = MANUAL[path]
        elif path in permanent:
            classification, family = "PERMANENT_ROOT", "PERMANENT_CONTROL"
            rationale = "Registered permanent control/navigation ledger; R1B never moves it."
            affirmative = "PERMANENT_ROOT_REGISTRY.tsv"
        elif r0_class == "ACTIVE":
            classification, family = "ACTIVE_CROSS_ERA", "R0_ACTIVE_CROSS_ERA"
            rationale = "Base inventory and current repository navigation retain this pre-cutoff record as active cross-era evidence."
            affirmative = "reorganization_r1b/base_forensic_census/ROOT_FILE_INVENTORY.tsv"
        elif r0_class == "FROZEN_EVIDENCE":
            classification, family = "HARD_FROZEN", "FORMAL_FROZEN_EVIDENCE"
            rationale = "Formally frozen evidence at the fixed base; neither bytes nor path move in R1B."
            affirmative = "reorganization_r1b/base_forensic_census/ROOT_FILE_INVENTORY.tsv"
        else:
            raise AssertionError(f"unclassified candidate: {path} ({r0_class})")
        adjudication.append(
            {
                **row,
                "classification": classification,
                "family": family,
                "rationale": rationale,
                "affirmative_evidence": affirmative,
                "move_authorized": "YES" if classification == "ARCHIVE_ELIGIBLE" else "NO",
            }
        )
    assert len({row["path"] for row in adjudication}) == 99

    eligible = {row["path"] for row in adjudication if row["classification"] == "ARCHIVE_ELIGIBLE"}
    assert eligible == set(ELIGIBLE)
    reference_by_target: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in references:
        reference_by_target[row["target"]].append(row)

    pointer_plan = []
    colocated_plan = []
    move_plan = []
    for path in sorted(eligible):
        destination = "archive/pre_2026-07-01/" + path
        source_path = repo / path
        move_plan.append(
            {
                "old_path": path,
                "new_path": destination,
                "git_blob_oid_before": next(row["git_blob_oid_at_base"] for row in adjudication if row["path"] == path),
                "sha256_before": sha256(source_path),
                "size_bytes": source_path.stat().st_size,
            }
        )
        for ref in reference_by_target[path]:
            if ref["reference_role"] == "QUALIFIED_PATH_SUFFIX":
                continue
            source = ref["source"]
            if source.startswith("archive/pre_2026-07-01/") or source in eligible:
                colocated_plan.append(
                    {
                        "source": source,
                        "target": path,
                        "line": ref["line"],
                        "column": ref["column"],
                        "reason": "SOURCE_AND_TARGET_RESOLVE_IN_ARCHIVE_PRE_2026_07_01",
                        "rewrite": "NO",
                    }
                )
                continue
            assert ref["source_immutability"] in {"MUTABLE_NAVIGATION_SOURCE", "SOFT_EVIDENCE_PATH_ONLY_SOURCE"}, ref
            pointer_plan.append(
                {
                    "source": source,
                    "old_target": path,
                    "new_target": destination,
                    "line": ref["line"],
                    "column": ref["column"],
                    "source_immutability": ref["source_immutability"],
                    "rewrite_mode": "EXACT_PATH_TOKEN_ONLY",
                }
            )
    assert len(pointer_plan) == 1
    assert pointer_plan[0]["source"] == "STATE.md" and pointer_plan[0]["old_target"] == "p4_VERIFIER.md"
    assert len(colocated_plan) == 1
    assert colocated_plan[0]["source"] == "archive/pre_2026-07-01/STEP2_timelive_matter_results.md"

    write(output / "CANDIDATE_ADJUDICATION.tsv", adjudication, tuple(adjudication[0]))
    write(
        output / "ELIGIBLE_MOVE_PLAN.tsv",
        move_plan,
        ("old_path", "new_path", "git_blob_oid_before", "sha256_before", "size_bytes"),
    )
    write(
        output / "POINTER_SUBSTITUTION_PLAN.tsv",
        pointer_plan,
        ("source", "old_target", "new_target", "line", "column", "source_immutability", "rewrite_mode"),
    )
    write(
        output / "COLOCATED_REFERENCE_PLAN.tsv",
        colocated_plan,
        ("source", "target", "line", "column", "reason", "rewrite"),
    )

    families = defaultdict(list)
    for row in adjudication:
        families[row["family"]].append(row["path"])
    family_rows = [
        {"family": family, "candidate_count": len(paths), "members": ";".join(sorted(paths))}
        for family, paths in sorted(families.items())
    ]
    write(output / "FAMILY_MAP.tsv", family_rows, ("family", "candidate_count", "members"))

    counts = Counter(row["classification"] for row in adjudication)
    report = {
        "result": "PASS",
        "mode": "R1B_PREMOVE_INDIVIDUAL_ADJUDICATION",
        "candidates": len(adjudication),
        "classification_counts": dict(sorted(counts.items())),
        "archive_eligible": len(eligible),
        "operational_live_substitutions": len(pointer_plan),
        "intentional_colocated_references": len(colocated_plan),
        "safety_stop": {
            "file_limit": 40,
            "substitution_limit": 400,
            "triggered": len(eligible) > 40 or len(pointer_plan) > 400,
        },
        "eligible_files": sorted(eligible),
    }
    assert report["safety_stop"]["triggered"] is False
    (output / "ADJUDICATION_SUMMARY.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    lines = [
        "# R1B pre-move adjudication report",
        "",
        "This report applies the preregistered seven-way classification to all 99 fixed-base candidates.",
        "Generated R1B records did not participate in selection, reference counts, rulings, or the safety stop.",
        "",
        "## Safety result",
        "",
        f"- Archive eligible: **{len(eligible)} / 40 maximum**.",
        f"- Operational live substitutions: **{len(pointer_plan)} / 400 maximum**.",
        f"- Intentional co-located unchanged references: **{len(colocated_plan)}**.",
        "- Safety stop: **NOT TRIGGERED**.",
        "",
        "## Classification counts",
        "",
    ]
    for classification, count in sorted(counts.items()):
        lines.append(f"- `{classification}`: {count}")
    lines.extend(
        [
            "",
            "## Individual rulings",
            "",
            "| Path | Classification | Family | Rationale | Affirmative evidence |",
            "|---|---|---|---|---|",
        ]
    )
    for row in adjudication:
        clean_rationale = row["rationale"].replace("|", "\\|")
        clean_evidence = row["affirmative_evidence"].replace("|", "\\|")
        lines.append(
            f"| `{row['path']}` | `{row['classification']}` | `{row['family']}` | "
            f"{clean_rationale} | `{clean_evidence}` |"
        )
    lines.extend(
        [
            "",
            "## Authorized batch",
            "",
            "Only `STEP2_timelive_matter_MAP.md` and `p4_VERIFIER.md` pass every gate. "
            "The former keeps one same-directory reference unchanged after relocation; the latter requires "
            "one exact path substitution in `STATE.md`. No other candidate has move authority.",
            "",
        ]
    )
    (output / "PREMOVE_ADJUDICATION_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

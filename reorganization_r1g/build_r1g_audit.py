#!/usr/bin/env python3
"""Build the additions-only R1G provenance correction overlay."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
from collections import Counter
from pathlib import Path


BASE = "8015342a81b2d27cc310dde95ab7f386c6441a77"
BOUNDARY = "f7664786d1e2340262ea5aa22336cf0c2f8b0dfc"
BOUNDARY_PARENT = "78939836326cb822e22b2a72bfd8097365185aa6"

MIXED_CANDIDATES = {
    "cascade_bv16_cas.py",
    "cascade_or_energy_cas.py",
    "phi_source_derivation.py",
    "homog_alpha_test.py",
    "verify_universe_bv2_f_einstein.py",
}
OPEN_CANDIDATES = {"verify_redshift_profile_derivation.py"}
PARTICLE_CANDIDATES = {"phi_source_derivation.py", "homog_alpha_test.py"}
MACRO_CANDIDATES = {
    "homog_universe_numeric.py", "homog_universe_solve.py",
    "verify_redshift_profile_derivation.py",
}

FAMILIES = {
    "876ea84a656b5428305b7ca5957184b32dd7fc3a": {
        "id": "C00_CHARACTERIZATION_MAP", "provenance": "NATIVE_2026-07-01",
        "lifecycle": "HISTORICAL", "evidence": "universe_cell_T3_closure_results.md;cascade_characterization_miniMAP.md;f766478",
        "note": "characterization map explicitly extends the native T3 universe-cell closure",
    },
    "5177aea9252af40278bcdea65569039de5309893": {
        "id": "C01_STAGE_A", "provenance": "NATIVE_2026-07-01", "lifecycle": "HISTORICAL",
        "evidence": "cascade_stageA_results.md;universe_cell_T3_closure_results.md;f766478",
        "note": "Stage-A persistence tests use the native round-static Branch-P universe-cell equations",
    },
    "20579ee944802b337195b43d55d1872a3e5a2e4e": {
        "id": "C02_STAGE_B", "provenance": "NATIVE_2026-07-01", "lifecycle": "HISTORICAL",
        "evidence": "cascade_stageB_results.md;cascade_stageA_results.md;f766478",
        "note": "Stage-B ladder continues the native Stage-A/T3 operator lineage",
    },
    "24671fabfc1e2e21a1d08c1b24ae4639c9e83263": {
        "id": "C03_STAGE_C", "provenance": "NATIVE_2026-07-01", "lifecycle": "HISTORICAL",
        "evidence": "cascade_stageC_results.md;cascade_stageB_results.md;f766478",
        "note": "Stage-C family universality continues the native universe-cell ladder",
    },
    "95f2d73efadfef2569189ac2e1c25547817866fb": {
        "id": "C04_LADDER_THEOREMS", "provenance": "NATIVE_2026-07-01", "lifecycle": "HISTORICAL",
        "evidence": "ladder_theorems_AB_C_results.md;cascade_stageC_results.md;f766478",
        "note": "theorems are derived from the native ladder closure and EOM identities",
    },
    "2836cc8694db1967ba0d03ee43184ab87238ae05": {
        "id": "C05_LEMMA_D", "provenance": "NATIVE_2026-07-01", "lifecycle": "HISTORICAL",
        "evidence": "ladder_lemmaD_sealing_amplitude_results.md;cascade_stageC_results.md;f766478",
        "note": "Lemma-D derives the seal amplitude from the native Branch-P ladder",
    },
    "add2f22217576fa96308c68bc459e8e271affddf": {
        "id": "C06_THETA0_ACCUMULATION", "provenance": "NATIVE_2026-07-01", "lifecycle": "HISTORICAL",
        "evidence": "ladder_theta0_accumulation_results.md;ladder_lemmaD_sealing_amplitude_results.md;f766478",
        "note": "second-order closure uses the native T3 EOM, Hamiltonian, flux law, and fold pins",
    },
    "48b50d402960f92aaa345daee26ae7dd14dca0c0": {
        "id": "C07_TWIN_LADDER", "provenance": "NATIVE_2026-07-01", "lifecycle": "HISTORICAL",
        "evidence": "twin_ladder_involution_results.md;ladder_theta0_accumulation_results.md;f766478",
        "note": "twin involution is derived on the native round-static Branch-P action",
    },
    "4ee798243b0911bdd8360710aa84ca75aefae039": {
        "id": "C08_STABILITY_STAGE1", "provenance": "NATIVE_2026-07-01", "lifecycle": "HISTORICAL",
        "evidence": "stability_operator_results.md;twin_ladder_involution_results.md;f766478",
        "note": "second variation and Jacobi operator are derived from the native reduced action",
    },
    "883a484b7385e8bd21d305f237236c6a66e0c340": {
        "id": "C09_STABILITY_STAGE2", "provenance": "NATIVE_2026-07-01", "lifecycle": "HISTORICAL",
        "evidence": "stability_stage2_results.md;stability_operator_results.md;f766478",
        "note": "stage-2 inertia census consumes the native stability operator",
    },
    "7a09b800a2f3f5a375c21cb66fdc8f173a23dcb7": {
        "id": "C10_SOFTMODE_PROVISIONAL", "provenance": "NATIVE_2026-07-01", "lifecycle": "HISTORICAL",
        "evidence": "ladder_softmode_results.md;stability_stage2_results.md;f766478",
        "note": "provisional soft-mode scripts were later adjudicated in the same native stability family",
    },
    "1c7ff8f0455bbf8502bb5572d06e6ba44c58f4d3": {
        "id": "C11_SOFTMODE_VERIFIED", "provenance": "NATIVE_2026-07-01", "lifecycle": "HISTORICAL",
        "evidence": "ladder_softmode_results.md;stability_stage2_results.md;f766478",
        "note": "verified soft-mode family remains scoped to the native round-static action",
    },
    "5a82fbbd657402126c8f74af6b70bab92d02e274": {
        "id": "C12_ENERGY_ORIENTATION", "provenance": "MIXED", "lifecycle": "HISTORICAL",
        "evidence": "ladder_energy_orientation_results.md;CANON.md:C-2026-07-03-1;f766478;GR_REFERENCE:Einstein_tensor+Misner-Sharp",
        "note": "native action/EOM identities are combined with explicitly reference-only Einstein/MS readouts",
    },
    "34d1b6b1c4469f1fccf77eb6a212fc90cc766ee2": {
        "id": "C13_STAGED_PREREG", "provenance": "NATIVE_2026-07-01", "lifecycle": "FROZEN",
        "evidence": "cascade_stageD_prereg.md;cascade_stageC_results.md;f766478",
        "note": "hash-frozen Stage-D prediction contract on the native cascade lineage",
    },
    "6cb6e306c0549f14f775ac956ffde7cc119267c9": {
        "id": "C14_STAGED_DATA", "provenance": "NATIVE_2026-07-01", "lifecycle": "HISTORICAL",
        "evidence": "cascade_stageD_results.md;cascade_stageD_prereg.md;f766478",
        "note": "Stage-D sweep machinery evaluates the preregistered native-cascade forecast",
    },
}


def git(repo: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(["git", *args], cwd=repo, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, check=False)
    if check and result.returncode:
        raise AssertionError(f"git {' '.join(args)} failed: {result.stderr}")
    return result.stdout


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_rows(path: Path, data: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(data[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(data)


def is_descendant(repo: Path, ancestor: str, descendant: str) -> bool:
    result = subprocess.run(["git", "merge-base", "--is-ancestor", ancestor, descendant], cwd=repo)
    return result.returncode == 0


def candidate_classification(path: str, intro: str) -> dict[str, str]:
    if path in OPEN_CANDIDATES:
        return {
            "operator_provenance": "OPEN",
            "operator_lineage_evidence": "2239a142:verify_redshift_profile_derivation.py uses a separate proper-distance homogeneity postulate and no field equation;luminosity_distance_n2_optics_results.md",
            "provenance_note": "post-July kinematic/optics check; no operator lineage to classify as pre-native or July-1-native",
        }
    if path in {"cascade_bv16_cas.py", "cascade_or_energy_cas.py"}:
        return {
            "operator_provenance": "MIXED",
            "operator_lineage_evidence": FAMILIES[intro]["evidence"],
            "provenance_note": "native July-1 action/EOM plus explicitly reference-only Einstein tensor and Misner-Sharp readout",
        }
    if path == "verify_universe_bv2_f_einstein.py":
        return {
            "operator_provenance": "MIXED",
            "operator_lineage_evidence": "ef2423d:universe_cell_fold_jc_sigma_results.md:D3;f766478;GR_REFERENCE:Einstein_tensor+Misner-Sharp",
            "provenance_note": "native EOM substitutions are combined with a non-native Einstein/MS reading audited as such",
        }
    if path in {"phi_source_derivation.py", "homog_alpha_test.py"}:
        return {
            "operator_provenance": "MIXED",
            "operator_lineage_evidence": "28bff7da:udt_phi_blindness_relaxation_results.md;f766478;alpha=-2 IMPORTED;alpha=-1/-0.5 FREE",
            "provenance_note": "July-1 native Branch-P baseline extended across a free/imported alpha coupling family",
        }
    if path.startswith("cascade_"):
        family = FAMILIES[intro]
        return {"operator_provenance": family["provenance"],
                "operator_lineage_evidence": family["evidence"],
                "provenance_note": family["note"]}
    if path == "stageD_bv_forecast_check.py":
        return {
            "operator_provenance": "NATIVE_2026-07-01",
            "operator_lineage_evidence": "de090cdf:cascade_stageD_results.md;cascade_stageD_prereg.md;f766478",
            "provenance_note": "independent replay of the native cascade's preregistered Stage-D forecast",
        }
    if path.startswith("verify_universe_bv2_"):
        return {
            "operator_provenance": "NATIVE_2026-07-01",
            "operator_lineage_evidence": "ef2423d:universe_cell_fold_jc_sigma_results.md;native_field_equations_constrained_two_player_results.md;f766478",
            "provenance_note": "independent reduction/variation of the July-1 native round-cell action",
        }
    if path.startswith("homog_universe_"):
        return {
            "operator_provenance": "NATIVE_2026-07-01",
            "operator_lineage_evidence": "70962d60:udt_no_homogeneous_universe_results.md;native_field_equations_constrained_two_player_results.md;f766478",
            "provenance_note": "static homogeneity test directly evaluates the July-1 native Branch-P field equation",
        }
    raise AssertionError(f"unadjudicated candidate: {path}")


def candidate_owner(path: str) -> tuple[str, str]:
    if path in PARTICLE_CANDIDATES:
        return "PARTICLE_MASS", "MACRO;FOUNDATIONS"
    if path in MACRO_CANDIDATES:
        return "MACRO", "FOUNDATIONS"
    return "FOUNDATIONS", "MACRO;PARTICLE_MASS"


def candidate_destination(path: str, provenance: str, owner: str) -> tuple[str, str]:
    name = Path(path).name
    if owner == "PARTICLE_MASS":
        root = "archive/post_2026-07-01/particle_mass/phi_sourcing/"
        why = "post-July mixed/free coupling study; historical particle-sourcing record"
    elif owner == "MACRO" and provenance == "NATIVE_2026-07-01":
        root = "archive/native_2026-07-01/macro/homogeneity_detour/"
        why = "historical macro homogeneity test explicitly using the July-1 native operator"
    elif owner == "MACRO":
        root = "archive/post_2026-07-01/macro/kinematic_optics/"
        why = "post-July operator-neutral kinematic/optics history"
    elif provenance == "MIXED":
        root = "archive/post_2026-07-01/foundations/mixed_native_gr_readout/"
        why = "historical native-action calculation containing explicitly non-native GR/MS readout"
    else:
        root = "archive/native_2026-07-01/foundations/universe_cell/"
        why = "historical July-1-native universe-cell/cascade foundation"
    return root + name, why


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args(); repo = args.repo.resolve(); out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)

    if git(repo, "rev-parse", f"{BOUNDARY}^").strip() != BOUNDARY_PARENT:
        raise AssertionError("boundary parent mismatch")
    boundary_names = set(git(repo, "diff-tree", "--no-commit-id", "--name-status", "-r", BOUNDARY).splitlines())
    required = {"A\tnative_field_equations_constrained_two_player_results.md", "A\tverify_native_fieldeq.py"}
    if not required.issubset(boundary_names):
        raise AssertionError("boundary commit does not add its field-equation record and verifier")

    frozen = rows(out / "PREREGISTERED_B02_B03_UNIVERSE.tsv")
    candidate_rows = []
    for row in frozen:
        path, intro = row["current_path"], row["introducing_commit"]
        if not is_descendant(repo, BOUNDARY, intro):
            raise AssertionError(f"candidate introduction does not descend from boundary: {path}")
        classified = candidate_classification(path, intro)
        owner, secondary = candidate_owner(path)
        destination, destination_why = candidate_destination(path, classified["operator_provenance"], owner)
        candidate_rows.append({
            "batch_id": row["batch_id"], "current_path": path,
            "git_blob_oid": row["git_blob_oid"], "sha256": row["sha256"],
            "introducing_commit": intro, "introducing_commit_date": row["introducing_commit_date"],
            "first_commit": row["first_commit"], "first_commit_date": row["first_commit_date"],
            "last_commit": row["last_commit"], "last_commit_date": row["last_commit_date"],
            "r1e_destination": row["proposed_destination"],
            "operator_provenance": classified["operator_provenance"],
            "operator_lineage_evidence": classified["operator_lineage_evidence"],
            "pre_native_lineage_commit": "",
            "provenance_note": classified["provenance_note"],
            "scientific_lifecycle": "HISTORICAL",
            "lifecycle_evidence": "archive/LIVE_historical_frontier_through_2026-07-08.md;archive/INDEX_pre_simple_metric_WR_L_2026-07-09.md",
            "primary_owner": owner, "secondary_consumers": secondary,
            "migration_safety": "BLOCKED_PROVENANCE_CORRECTION_REQUIRED",
            "corrected_destination_proposal": destination,
            "destination_justification": destination_why,
        })
    write_rows(out / "B02_B03_ADJUDICATION.tsv", candidate_rows)

    affected = rows(out / "PREREGISTERED_AFFECTED_CASCADE_UNIVERSE.tsv")
    file_census = []; grouped: dict[str, list[dict[str, str]]] = {}
    for row in affected:
        intro = row["introducing_commit"]
        if intro not in FAMILIES:
            raise AssertionError(f"unadjudicated cascade introducing commit: {intro}")
        if not is_descendant(repo, BOUNDARY, intro):
            raise AssertionError(f"cascade family is not descended from native boundary: {row['current_path']}")
        family = FAMILIES[intro]; grouped.setdefault(intro, []).append(row)
        if family["lifecycle"] == "FROZEN":
            safety, destination = "IMMUTABLE_PATH_RETAIN", row["current_path"]
        elif family["provenance"] == "MIXED":
            safety = "BLOCKED_PROVENANCE_CORRECTION_REQUIRED"
            destination = "archive/post_2026-07-01/foundations/mixed_native_gr_readout/" + Path(row["current_path"]).name
        else:
            safety = "BLOCKED_PROVENANCE_CORRECTION_REQUIRED"
            destination = "archive/native_2026-07-01/foundations/universe_cell/" + Path(row["current_path"]).name
        file_census.append({
            "current_path": row["current_path"], "introducing_commit": intro,
            "introducing_commit_date": row["introducing_commit_date"],
            "last_commit": row["last_commit"], "last_commit_date": row["last_commit_date"],
            "family_id": family["id"], "operator_provenance": family["provenance"],
            "operator_lineage_evidence": family["evidence"], "pre_native_lineage_commit": "",
            "scientific_lifecycle": family["lifecycle"],
            "lifecycle_evidence": "archive/INDEX_pre_simple_metric_WR_L_2026-07-09.md:SUPERSEDED_as_frontier;family_result_record",
            "primary_owner": "FOUNDATIONS", "secondary_consumers": "MACRO;PARTICLE_MASS",
            "migration_safety": safety, "corrected_destination_proposal": destination,
            "family_note": family["note"],
        })
    write_rows(out / "AFFECTED_CASCADE_FILE_CENSUS.tsv", file_census)

    summary = []
    for intro, members in sorted(grouped.items(), key=lambda item: (item[1][0]["introducing_commit_date"], item[0])):
        family = FAMILIES[intro]
        summary.append({
            "family_id": family["id"], "introducing_commit": intro,
            "introducing_commit_date": members[0]["introducing_commit_date"],
            "introducing_subject": members[0]["introducing_subject"], "file_count": str(len(members)),
            "operator_provenance": family["provenance"], "operator_lineage_evidence": family["evidence"],
            "scientific_lifecycle": family["lifecycle"], "primary_owner": "FOUNDATIONS",
            "migration_safety": "IMMUTABLE_PATH_RETAIN" if family["lifecycle"] == "FROZEN" else "BLOCKED_PROVENANCE_CORRECTION_REQUIRED",
            "destination_root_proposal": ("CURRENT_PATH" if family["lifecycle"] == "FROZEN" else
                "archive/post_2026-07-01/foundations/mixed_native_gr_readout/" if family["provenance"] == "MIXED" else
                "archive/native_2026-07-01/foundations/universe_cell/"),
            "family_note": family["note"],
        })
    write_rows(out / "AFFECTED_CASCADE_FAMILY_SUMMARY.tsv", summary)

    boundary = {
        "result": "PASS", "last_pre_boundary_ancestor": BOUNDARY_PARENT,
        "native_field_equation_boundary": BOUNDARY,
        "boundary_author_and_commit_date": git(repo, "show", "-s", "--format=%aI|%cI", BOUNDARY).strip(),
        "boundary_subject": git(repo, "show", "-s", "--format=%s", BOUNDARY).strip(),
        "boundary_adds": sorted(required),
        "semantic_evidence": [
            "native_field_equations_constrained_two_player_results.md:3-10",
            "branch_operator_contamination_ledger.md:10-33",
            "PURSUIT_CHARTER_2026-07-04.md:175-179",
        ],
        "note": "f766478 is the first native-field-equation commit; af286a6 later adds the native geometric action and does not move this boundary",
    }
    (out / "JULY1_NATIVE_BOUNDARY.json").write_text(
        json.dumps(boundary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    rules = {
        "result": "PROPOSED_NOT_APPLIED", "separate_axes": ["operator_provenance", "scientific_lifecycle", "path_migration_safety"],
        "operator_labels": ["PRE_NATIVE", "NATIVE_2026-07-01", "MIXED", "OPEN"],
        "lifecycle_labels": ["ACTIVE", "SUPERSEDED", "HISTORICAL", "FROZEN"],
        "rules_in_precedence_order": [
            {"rule": "hard_frozen_or_manifest", "effect": "retain immutable path; do not infer operator provenance"},
            {"rule": "explicit_operator_lineage", "effect": "classify from operator-bearing commits and primary records"},
            {"rule": "mixed_lineage", "effect": "MIXED when native operators and imported/reference operators share the artifact"},
            {"rule": "insufficient_lineage", "effect": "OPEN; filename and dates may not promote or demote"},
            {"rule": "lifecycle", "effect": "classify independently from current controls/result status"},
            {"rule": "migration_safety", "effect": "evaluate dependencies and immutable constraints independently"},
        ],
        "destination_taxonomy": {
            "archive/pre_2026-07-01/": "only PRE_NATIVE with explicit path-specific operator lineage predating f766478",
            "archive/native_2026-07-01/": "historical/superseded artifacts explicitly descended from the f766478 native operator",
            "archive/post_2026-07-01/": "post-July MIXED or operator-OPEN historical artifacts, partitioned by owner/family",
            "research/<lane>/": "ACTIVE artifacts only after dependency-closed migration authority",
            "current_path": "FROZEN/manifest-constrained artifacts unless separately authorized",
        },
        "forbidden_inference": "No prefix, including cascade_, may establish PRE_NATIVE or any destination.",
    }
    (out / "CORRECTED_CLASSIFIER_RULES.json").write_text(
        json.dumps(rules, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    result = {
        "result": "PASS", "base": BASE, "boundary": BOUNDARY, "boundary_parent": BOUNDARY_PARENT,
        "candidate_rows": len(candidate_rows), "candidate_batch_counts": dict(Counter(row["batch_id"] for row in candidate_rows)),
        "candidate_provenance_counts": dict(Counter(row["operator_provenance"] for row in candidate_rows)),
        "candidate_lifecycle_counts": dict(Counter(row["scientific_lifecycle"] for row in candidate_rows)),
        "candidate_owner_counts": dict(Counter(row["primary_owner"] for row in candidate_rows)),
        "affected_cascade_rows": len(file_census), "affected_family_rows": len(summary),
        "affected_provenance_counts": dict(Counter(row["operator_provenance"] for row in file_census)),
        "affected_lifecycle_counts": dict(Counter(row["scientific_lifecycle"] for row in file_census)),
        "pre_native_candidate_rows": sum(row["operator_provenance"] == "PRE_NATIVE" for row in candidate_rows),
        "pre_native_affected_cascade_rows": sum(row["operator_provenance"] == "PRE_NATIVE" for row in file_census),
        "archive_pre_destination_rows": sum(row["corrected_destination_proposal"].startswith("archive/pre_2026-07-01/") for row in candidate_rows + file_census),
        "moves_authorized": False,
    }
    (out / "AUDIT_SUMMARY.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

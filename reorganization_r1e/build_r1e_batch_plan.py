#!/usr/bin/env python3
"""Build the R1E plan-only candidate, family, and batch records.

This program is intentionally read-only outside reorganization_r1e/.  Candidate
selection is not performed here: it consumes the candidate universe frozen and
committed by the R1E preregistration.
"""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "reorganization_r1e"
CANDIDATES = OUT / "PREREGISTERED_CANDIDATE_UNIVERSE.tsv"
DEPENDENCIES = REPO / "reorganization_r1b/postmove_operational_census/DEPENDENCY_MAP.tsv"
FORENSIC_DEPENDENCIES = REPO / "reorganization_r1b/postmove_forensic_census/DEPENDENCY_MAP.tsv"
OWNERSHIP = REPO / "research/_registry/ROOT_OWNERSHIP.tsv"
FRONTIER = REPO / "research/_registry/CURRENT_FRONTIER_TARGETS.tsv"

DISPOSITIONS = {
    "SAFE_BYTE_IDENTICAL",
    "SAFE_WITH_PATH_POINTER_CHANGES",
    "BLOCKED_IMMUTABLE_COMPANION",
    "BLOCKED_RUNTIME_OR_MISSING_INPUT",
    "BLOCKED_TEST_SCOPE",
    "BLOCKED_FRONTIER_OR_CONTROL",
    "NEEDS_MANUAL_ADJUDICATION",
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=REPO, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    if result.returncode:
        raise RuntimeError(result.stderr)
    return result.stdout.strip()


# The three proposals.  The four-file active family is deliberately below the
# preferred lower bound: active/legacy separation and atomic family coherence
# forbid padding it with legacy scripts.
SAFE_BATCHES: dict[str, list[str]] = {
    "B01_ACTIVE_MACRO_SYMPY_QUARTET": [
        "verify_center_escape.py",
        "verify_center_nogo.py",
        "verify_eos_dS_window.py",
        "verify_wrl_canon.py",
    ],
    "B02_LEGACY_STANDALONE_ALGEBRA_A": [
        "cascade_bv10_E2_period.py",
        "cascade_bv10_E2_symbolic.py",
        "cascade_bv10_E3_bottom.py",
        "cascade_bv10_cas.py",
        "cascade_bv11_v4_cas.py",
        "cascade_bv13_w1_classes.py",
        "cascade_bv13_w2_w3cas.py",
        "cascade_bv13_w5_homothety.py",
        "cascade_bv16_cas.py",
        "cascade_lemD_cas.py",
        "cascade_or_energy_cas.py",
        "cascade_sf_cas1_bulk.py",
        "cascade_sf_cas4_zeromodes.py",
        "cascade_th2_cas_checks.py",
        "cascade_th2_cas_kappa.py",
        "cascade_tw_cas.py",
        "phi_source_derivation.py",
        "stageD_bv_forecast_check.py",
    ],
    "B03_LEGACY_STANDALONE_ALGEBRA_B": [
        "cascade_th2_bottom_beta.py",
        "cascade_th2_bottom_system.py",
        "cascade_th2_launch.py",
        "homog_alpha_test.py",
        "homog_universe_numeric.py",
        "homog_universe_solve.py",
        "verify_redshift_profile_derivation.py",
        "verify_universe_bv2_a_reduction.py",
        "verify_universe_bv2_b_ident.py",
        "verify_universe_bv2_c_folds.py",
        "verify_universe_bv2_d_budget.py",
        "verify_universe_bv2_e_sigma.py",
        "verify_universe_bv2_f_einstein.py",
        "verify_universe_bv2_g_transv_toy.py",
    ],
}


def group(paths: list[str], disposition: str, reason: str, companions: str = "NONE",
          unresolved: str = "NONE", generated: str = "NONE", test_scope: str = "NONE") -> dict[str, object]:
    return {
        "paths": paths,
        "disposition": disposition,
        "reason": reason,
        "companions": companions,
        "unresolved": unresolved,
        "generated": generated,
        "test_scope": test_scope,
    }


# Families below are dependency closures, not filename-only groupings.  Shared
# imports, producer/output relations, or an explicit runtime companion connect
# each multi-file family.  Independent scripts remain singleton components.
BLOCKED_FAMILIES: dict[str, dict[str, object]] = {
    "F_BV10_RESHOOT_RUNTIME": group(
        ["cascade_bv10_reshoot.py"], "BLOCKED_IMMUTABLE_COMPANION",
        "imports retained root solver libraries and generates a root-relative NPY",
        "cell_solver_universe_T3.py;cascade_stageC_lib.py",
        generated="bv10_reshoot_results.npy"),
    "F_BV11_RUNTIME": group(
        ["cascade_bv11_lib.py", "cascade_bv11_v1_root.py", "cascade_bv11_v1_tolcheck.py",
         "cascade_bv11_v2_desert.py", "cascade_bv11_v3_cap.py"],
        "BLOCKED_RUNTIME_OR_MISSING_INPUT",
        "unprefixed bv11_lib import, hard-coded root module load, and producer/output closure are unresolved",
        "cell_solver_universe_T3.py", "bv11_lib;absolute root cell_solver path",
        "bv11_fundamental_traj.npz;bv11_root.json"),
    "F_BV13_RUNTIME": group(
        ["cascade_bv13_su_trans.py", "cascade_bv13_vhat_probe.py"],
        "BLOCKED_RUNTIME_OR_MISSING_INPUT", "both consumers require absent generated background files",
        unresolved="bv13_bg.npz;bv13_bg.json"),
    "F_BV14_RUNTIME": group(
        ["cascade_bv14_counts.py", "cascade_bv14_spare_a_sens.py", "cascade_bv14_su.py",
         "cascade_bv14_summary.py", "cascade_bv14_tolsweep.py", "cascade_bv14_validate.py"],
        "BLOCKED_RUNTIME_OR_MISSING_INPUT", "unprefixed bv14_lib import and dynamic SCR ledger/output paths",
        "cascade_bv14_lib.py", "bv14_lib;dynamic SCR paths"),
    "F_BV15_RUNTIME": group(
        ["cascade_bv15_asm.py", "cascade_bv15_x1_ladder.py", "cascade_bv15_x1_validate.py",
         "cascade_bv15_x2_anatomy.py", "cascade_bv15_x3_c2.py"],
        "BLOCKED_RUNTIME_OR_MISSING_INPUT", "unprefixed module imports, missing ray module, and dynamic scratch outputs",
        unresolved="bv15_asm;bv15_x3_ray;dynamic SCR paths"),
    "F_BV5_RUNTIME": group(
        ["cascade_bv5_common.py", "cascade_bv5_c1_scan.py", "cascade_bv5_c1c2c3_roots.py",
         "cascade_bv5_c4_bigN.py", "cascade_bv5_c4_floor_audit.py", "cascade_bv5_c5_stuck.py"],
        "BLOCKED_RUNTIME_OR_MISSING_INPUT", "five scripts import the candidate helper under a non-resolving unprefixed name",
        unresolved="bv5_common"),
    "F_BV6_RUNTIME": group(
        ["cascade_bv6_c1_refine.py", "cascade_bv6_c1_sweep.py", "cascade_bv6_probe.py", "cascade_bv6_xcheck.py"],
        "BLOCKED_IMMUTABLE_COMPANION", "retained library plus sweep/refine producer-output chain must move together",
        "cascade_bv6_lib.py", "bv6_lib", "bv6_c1_sweep.json;bv6_c1_roots.json;bv6_xcheck.json"),
    "F_BV7_RUNTIME": group(
        ["cascade_bv7_t1_refine.py", "cascade_bv7_t2.py", "cascade_bv7_t3.py", "cascade_bv7_validate.py"],
        "BLOCKED_IMMUTABLE_COMPANION", "retained core module and missing sweep input block the root-relative chain",
        "cascade_bv7_core.py", "bv7_core;bv7_t1_sweep.json", "bv7_t1_roots.json"),
    "F_BV9_RUNTIME": group(
        ["cascade_bv9_reshoot_Z1.py", "cascade_bv9_tables.py"],
        "BLOCKED_IMMUTABLE_COMPANION", "retained universe solver and dynamic table-input set are outside the candidates",
        "cell_solver_universe_T3.py", "dynamic REPO table inputs"),
    "F_LEMD_RUNTIME": group(
        ["cascade_lemD_bessel.py", "cascade_lemD_final.py", "cascade_lemD_reshoot.py", "cascade_lemD_table.py"],
        "BLOCKED_IMMUTABLE_COMPANION", "retained solver and frozen stage-B output are runtime inputs",
        "cell_solver_universe_T3.py;cascade_stageB_rungs.json", "dynamic BASE inputs"),
    "F_OR_ENERGY_RUNTIME": group(
        ["cascade_or_energy_numeric.py", "cascade_or_energy_rung1_and_alignment.py"],
        "BLOCKED_IMMUTABLE_COMPANION", "hard-coded root stage-B output and retained solver are runtime inputs",
        "cell_solver_universe_T3.py;cascade_stageB_rungs.json", "absolute workstation path"),
    "F_S2_RUNTIME": group(
        ["cascade_s2_aggregate.py", "cascade_s2_core.py", "cascade_s2_validate.py"],
        "BLOCKED_RUNTIME_OR_MISSING_INPUT", "unprefixed candidate-core import and aggregation inputs are unresolved",
        unresolved="s2_core;dynamic aggregation inputs"),
    "F_S3_RUNTIME": group(
        ["cascade_s3_lib.py", "cascade_s3_t2_t3.py", "cascade_s3_t5.py", "cascade_s3_validate.py"],
        "BLOCKED_RUNTIME_OR_MISSING_INPUT", "unprefixed candidate-library import and generated-family paths are unresolved",
        unresolved="s3_lib;generated s3 family paths"),
    "F_SF_D5_RUNTIME": group(
        ["cascade_sf_d5_spotcheck.py", "cascade_sf_d5b_extra.py"],
        "BLOCKED_RUNTIME_OR_MISSING_INPUT", "consumer imports candidate producer under a non-resolving unprefixed name",
        unresolved="sf_d5_spotcheck"),
    "F_STAGE_A_RUNTIME": group(
        ["cascade_stageA_extra.py", "cascade_stageA_run.py"],
        "BLOCKED_IMMUTABLE_COMPANION", "retained stage-A library and shared results file close the runtime family",
        "cascade_stageA_lib.py", "stageA_lib", "stageA_results.json"),
    "F_STAGE_B_RUNTIME": group(
        ["cascade_stageB_above.py", "cascade_stageB_analysis.py", "cascade_stageB_bisect.py", "cascade_stageB_sanity.py"],
        "BLOCKED_IMMUTABLE_COMPANION", "retained solver/common modules and frozen rung data close the family",
        "cell_solver_universe_T3.py;cascade_stageB_common.py;cascade_stageB_rungs.json",
        "stageB_common;dynamic SCR paths"),
    "F_STAGE_C_RUNTIME": group(
        ["cascade_stageC_run.py"], "BLOCKED_IMMUTABLE_COMPANION",
        "retained stage-C library is a runtime import", "cascade_stageC_lib.py", "stageC_lib"),
    "F_TH2_FINAL_RUNTIME": group(
        ["cascade_th2_final_table.py"], "BLOCKED_RUNTIME_OR_MISSING_INPUT",
        "missing predictor module and missing th2 producer output", unresolved="th2_predict_measure;th2_results.json",
        generated="th2_final_table.json"),
    "F_TW_RUNTIME": group(
        ["cascade_tw_confirm.py", "cascade_tw_pred.py", "cascade_tw_reshoot.py"],
        "BLOCKED_IMMUTABLE_COMPANION", "retained solver/common and hard-coded frozen rung file remain at root",
        "cell_solver_universe_T3.py;cascade_stageB_common.py;cascade_stageB_rungs.json",
        "absolute workstation path"),
    "F_E2C_RUNTIME": group(
        ["e2c_bv_gauntlet.py"], "BLOCKED_IMMUTABLE_COMPANION",
        "imports retained composite solver", "cell_solver_composite.py"),
    "F_E2D_RUNTIME": group(
        ["e2d_bv_cert.py", "e2d_bv_checks.py"], "BLOCKED_IMMUTABLE_COMPANION",
        "both scripts import retained composite solver and continuation driver",
        "cell_solver_composite.py;e2d_continuation_driver.py"),
    "F_UNIVERSE_BV4_RUNTIME": group(
        ["verify_universe_bv4_shoot.py", "verify_universe_bv4_q1_validate.py",
         "verify_universe_bv4_q2_powers.py", "verify_universe_bv4_q3_bisect.py",
         "verify_universe_bv4_q3_scan.py", "verify_universe_bv4_q4_q5.py"],
        "BLOCKED_RUNTIME_OR_MISSING_INPUT",
        "five consumers import the candidate shooter under a non-resolving unprefixed name",
        unresolved="bv4_shoot"),
    "F_VERIFY_SNE_RUNTIME": group(
        ["verify_sne_adversarial.py"], "BLOCKED_RUNTIME_OR_MISSING_INPUT",
        "loads an absolute external Pantheon+ data path", unresolved="/home/udt-admin/UDT/data/Pantheon+SH0ES.dat"),
    "F_MACRO_DOTTED_OUTPUT": group(
        ["simple_metric_dotted_line.py"], "BLOCKED_IMMUTABLE_COMPANION",
        "__file__-relative write would strand or overwrite an immutable result",
        "simple_metric_dotted_line_out.json", generated="simple_metric_dotted_line_out.json"),
    "F_MACRO_ZOOM_OUTPUT": group(
        ["simple_metric_promising_candidates_zoom.py"], "BLOCKED_IMMUTABLE_COMPANION",
        "__file__-relative write would strand or overwrite an immutable result",
        "simple_metric_promising_candidates_zoom_out.json", generated="simple_metric_promising_candidates_zoom_out.json"),
    "F_MACRO_ROOMS_OUTPUT": group(
        ["simple_metric_relational_rooms_continue.py"], "BLOCKED_IMMUTABLE_COMPANION",
        "__file__-relative write would strand or overwrite an immutable result",
        "simple_metric_relational_rooms_continue_out.json", generated="simple_metric_relational_rooms_continue_out.json"),
    "F_MACRO_LEGACY_TEST_SCOPE": group(
        ["simple_metric_legacy_double_fix_side_excursion.md"], "BLOCKED_TEST_SCOPE",
        "root-only hygiene glob would silently stop testing the document after a move",
        test_scope="tests/test_hygiene_header.py:simple_metric_legacy_*_excursion.md"),
    "F_PARTICLE_CONTROLLED": group(
        ["controlled_relax_hessian.py"], "BLOCKED_IMMUTABLE_COMPANION",
        "root module/input/output family includes an immutable output and absent inputs",
        "controlled_relax_hessian_out.json;hopfion_arc_scripts_2026-07-05/fs_hopfion.py",
        "prod_relax256uncon.npz or hopfion_arc_scripts_2026-07-05/prod_an256.npz",
        "controlled_best_field.npz;controlled_relax_hessian_out.json"),
    "F_PARTICLE_HOPFION_HESSIAN": group(
        ["hopfion_static_mass_hessian_256driver.py"], "BLOCKED_IMMUTABLE_COMPANION",
        "common module is referenced by frozen packages and output JSON is immutable",
        "hopfion_static_mass_common.py;hopfion_static_mass_hessian_out.json",
        "prod_an256.npz", "hopfion_static_mass_hessian_out.json"),
    "F_PARTICLE_LONG_RELAX": group(
        ["long_relax_256.py"], "BLOCKED_RUNTIME_OR_MISSING_INPUT",
        "root-CWD module/input/checkpoint/output family is incomplete",
        "hopfion_arc_scripts_2026-07-05/fs_hopfion.py", "prod_relax256uncon.npz",
        "long_relax_256_ckpt.npz;long_relax_256_final.npz;long_relax_256_out.json"),
    "F_PARTICLE_NONULL": group(
        ["noNull_evidence_checker.py"], "BLOCKED_IMMUTABLE_COMPANION",
        "six absent inputs feed immutable evidence and output records",
        "noNull_stability_evidence.json;noNull_evidence_checker_output.txt",
        "six refine NPZ inputs", "noNull_evidence_checker_output.txt"),
    "F_STAGED_RAW_OUTPUT": group(
        ["stageD_sweep_results_raw.md"], "BLOCKED_IMMUTABLE_COMPANION",
        "raw result is coupled to retained producer scripts and generated JSON records",
        "cascade_stageD_sweep_scan.py;cascade_stageD_sweep_refine.py;stageD_sweep_results_raw.json"),
    "F_CELL_BUILD_NOTES_MANUAL": group(
        ["cell_solver_f2d_BUILDNOTES.md"], "NEEDS_MANUAL_ADJUDICATION",
        "dense literal solver/test/provenance references need a future path-semantics ruling"),
    "F_R2_LEAD_MANUAL": group(
        ["r2_prereg_s_dependence_LEAD.md"], "NEEDS_MANUAL_ADJUDICATION",
        "lead document has unresolved family companions and banked-status references"),
    "F_SOLVER_MAP_MANUAL": group(
        ["solver_build_MAP.md"], "NEEDS_MANUAL_ADJUDICATION",
        "map remains a historical physics navigation surface with unresolved companion semantics"),
}


ALIAS_TO_CANDIDATE = {
    "bv11_lib": "cascade_bv11_lib.py",
    "bv15_asm": "cascade_bv15_asm.py",
    "bv5_common": "cascade_bv5_common.py",
    "s2_core": "cascade_s2_core.py",
    "s3_lib": "cascade_s3_lib.py",
    "sf_d5_spotcheck": "cascade_sf_d5_spotcheck.py",
    "bv4_shoot": "verify_universe_bv4_shoot.py",
}


def ast_imports(path: Path) -> list[tuple[int, str]]:
    if path.suffix != ".py":
        return []
    tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    result: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            result.extend((node.lineno, alias.name) for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            result.append((node.lineno, node.module))
    return sorted(set(result))


def main() -> int:
    candidates = read_tsv(CANDIDATES)
    assert len(candidates) == 119
    by_path = {row["current_path"]: row for row in candidates}
    assert len(by_path) == 119
    ownership = {row["current_path"]: row for row in read_tsv(OWNERSHIP)}
    frontier = {row["target_path"].rstrip("/") for row in read_tsv(FRONTIER)}
    tracked = set(git("ls-files").splitlines())
    module_paths = {Path(path).stem: path for path in tracked if path.endswith(".py") and "/" not in path}

    batch_for: dict[str, str] = {}
    for batch_id, paths in SAFE_BATCHES.items():
        for path in paths:
            assert path not in batch_for
            batch_for[path] = batch_id

    assignment: dict[str, tuple[str, dict[str, object]]] = {}
    for family_id, meta in BLOCKED_FAMILIES.items():
        assert meta["disposition"] in DISPOSITIONS
        for path in meta["paths"]:  # type: ignore[index]
            assert path not in assignment and path not in batch_for, path
            assignment[path] = (family_id, meta)

    for path, batch_id in batch_for.items():
        family_id = "F_SAFE_" + Path(path).stem.upper().replace("-", "_")
        assignment[path] = (
            family_id,
            group([path], "SAFE_BYTE_IDENTICAL",
                  "standalone external-library/stdout-only script; no operational inbound, local runtime path, generated output, test glob, frontier target, or required companion"),
        )

    missing = sorted(set(by_path) - set(assignment))
    extra = sorted(set(assignment) - set(by_path))
    assert not missing and not extra, {"missing": missing, "extra": extra}

    dep_rows = read_tsv(DEPENDENCIES)
    by_source: dict[str, list[dict[str, str]]] = defaultdict(list)
    inbound_operational: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in dep_rows:
        by_source[row["source"]].append(row)
        if row["resolved_target"] in by_path and row["source"] != row["resolved_target"]:
            inbound_operational[row["resolved_target"]].append(row)
    assert sum(map(len, inbound_operational.values())) == 0
    inbound_forensic: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_tsv(FORENSIC_DEPENDENCIES):
        if row["resolved_target"] in by_path and row["source"] != row["resolved_target"]:
            inbound_forensic[row["resolved_target"]].append(row)

    evidence: list[dict[str, object]] = []
    graph_nodes: dict[str, dict[str, object]] = {}
    graph_edges: list[dict[str, object]] = []
    ledger: list[dict[str, object]] = []

    family_members: dict[str, list[str]] = defaultdict(list)
    for path, (family_id, _) in assignment.items():
        family_members[family_id].append(path)

    for family_id, members in family_members.items():
        members.sort()
        for left, right in zip(members, members[1:]):
            graph_edges.append({
                "source": left, "target": right, "kind": "FAMILY_CLOSURE",
                "required_for_migration": True,
                "evidence": "shared import, producer/output, runtime companion, or manually audited atomic closure",
            })

    for path in sorted(by_path):
        candidate = by_path[path]
        family_id, meta = assignment[path]
        disposition = str(meta["disposition"])
        own = ownership[path]
        assert own["frozen_manifest_status"] == "NOT_FROZEN_OR_MANIFEST"
        assert path not in frontier
        destination = candidate["recommended_destination"]
        assert destination != "-" and not (REPO / destination).exists()
        assert sha256(REPO / path) == candidate["fixed_base_sha256"]
        assert git("hash-object", "--no-filters", path) == candidate["fixed_base_blob_oid"]

        imports: list[str] = []
        for line, imported in ast_imports(REPO / path):
            root_name = imported.split(".", 1)[0]
            target = ALIAS_TO_CANDIDATE.get(root_name) or module_paths.get(root_name)
            if target:
                imports.append(f"{imported}->{target}")
                graph_nodes.setdefault(target, {"id": target, "kind": "candidate" if target in by_path else "companion"})
                graph_edges.append({
                    "source": path, "target": target, "kind": "PYTHON_IMPORT",
                    "required_for_migration": True, "evidence": f"AST line {line}: {imported}",
                })
                evidence.append({
                    "candidate_path": path, "line": line, "evidence_type": "PYTHON_IMPORT",
                    "raw_target": imported, "resolved_target": target,
                    "status": "CANDIDATE_ALIAS" if target in by_path else "TRACKED_COMPANION",
                    "load_bearing": "YES", "detail": "AST import closure",
                })

        runtime_rows = [row for row in by_source[path] if row["category"] == "FILE_PATH"]
        runtime_summary = sorted({
            f'{row["raw_target"]}[{row["status"]}]' for row in runtime_rows
            if row["raw_target"] not in {"__file__"}
        })
        for row in runtime_rows:
            evidence.append({
                "candidate_path": path, "line": row["line"], "evidence_type": "RUNTIME_FILE_PATH",
                "raw_target": row["raw_target"], "resolved_target": row["resolved_target"],
                "status": row["status"], "load_bearing": "YES",
                "detail": row["detail"],
            })
        # Markdown links and literal tokens are part of the graph even when they
        # are informational rather than path-resolution dependencies.  The
        # manual family rulings above decide when a literal token is load-bearing.
        for row in by_source[path]:
            if row["category"] not in {"MARKDOWN_LINK", "TEXT_REFERENCE", "STARTUP"}:
                continue
            target = row["resolved_target"]
            required = row["category"] in {"MARKDOWN_LINK", "STARTUP"}
            evidence.append({
                "candidate_path": path, "line": row["line"], "evidence_type": row["category"],
                "raw_target": row["raw_target"], "resolved_target": target,
                "status": row["status"], "load_bearing": "YES" if required else "NO_INFORMATIONAL",
                "detail": row["detail"],
            })
            if target and target != "-" and row["status"] in {"RESOLVED_TRACKED", "RESOLVED_DIRECTORY"}:
                graph_nodes.setdefault(target, {
                    "id": target, "kind": "candidate" if target in by_path else "reference_target",
                    "tracked": target in tracked, "exists": (REPO / target.rstrip("/")).exists(),
                })
                graph_edges.append({
                    "source": path, "target": target, "kind": row["category"],
                    "required_for_migration": required,
                    "evidence": f'operational census line {row["line"]}: {row["raw_target"]}',
                })

        companions = str(meta["companions"])
        frozen_companions: list[str] = []
        if companions != "NONE":
            for companion in companions.split(";"):
                node = {
                    "id": companion,
                    "kind": "companion",
                    "tracked": companion in tracked,
                    "exists": (REPO / companion).exists(),
                    "frozen_manifest_status": ownership.get(companion, {}).get(
                        "frozen_manifest_status", "NOT_REGISTERED_ROOT_PATH"),
                }
                graph_nodes.setdefault(companion, node)
                status = str(node["frozen_manifest_status"])
                if status not in {"NOT_FROZEN_OR_MANIFEST", "NOT_REGISTERED_ROOT_PATH"}:
                    frozen_companions.append(f"{companion}:{status}")
                graph_edges.append({
                    "source": path, "target": companion, "kind": "REQUIRED_COMPANION",
                    "required_for_migration": True, "evidence": str(meta["reason"]),
                })
                evidence.append({
                    "candidate_path": path, "line": 0, "evidence_type": "REQUIRED_COMPANION",
                    "raw_target": companion, "resolved_target": companion,
                    "status": status, "load_bearing": "YES", "detail": str(meta["reason"]),
                })

        lane_class = "LEGACY" if candidate["primary_owner"] == "LEGACY_FROZEN" else "ACTIVE"
        batch_id = batch_for.get(path, "-")
        pointer_changes = (
            "CURRENT_ARTIFACT_PATHS.tsv current_path+status;MIGRATION_LEDGER.tsv append"
            + (";research/macro/ROOT_INVENTORY.tsv current_path" if candidate["primary_owner"] == "MACRO" else "")
        ) if disposition.startswith("SAFE_") else "-"
        ledger.append({
            "candidate_path": path,
            "original_path": candidate["original_path"],
            "destination": destination,
            "primary_owner": candidate["primary_owner"],
            "lane_class": lane_class,
            "artifact_type": candidate["artifact_type"],
            "git_blob_oid": candidate["fixed_base_blob_oid"],
            "sha256": candidate["fixed_base_sha256"],
            "atomic_family_id": family_id,
            "disposition": disposition,
            "proposed_batch_id": batch_id,
            "operational_inbound_count": len(inbound_operational[path]),
            "forensic_inbound_count": len(inbound_forensic[path]),
            "forensic_inbound_sources": ";".join(sorted({row["source"] for row in inbound_forensic[path]})) or "NONE",
            "outbound_imports": ";".join(sorted(set(imports))) or "NONE",
            "runtime_paths": ";".join(runtime_summary) or "NONE",
            "generated_outputs": str(meta["generated"]),
            "required_companions": companions,
            "frozen_companions": ";".join(frozen_companions) or "NONE",
            "unresolved_runtime_paths": str(meta["unresolved"]),
            "test_scope": str(meta["test_scope"]),
            "frontier_or_control": "NONE",
            "future_exact_pointer_changes": pointer_changes,
            "ruling_basis": str(meta["reason"]),
        })
        graph_nodes[path] = {
            "id": path, "kind": "candidate", "owner": candidate["primary_owner"],
            "lane_class": lane_class, "family_id": family_id, "disposition": disposition,
            "destination": destination,
        }

    ledger.sort(key=lambda row: str(row["candidate_path"]))
    evidence.sort(key=lambda row: (str(row["candidate_path"]), int(row["line"]), str(row["evidence_type"]), str(row["raw_target"])))
    ledger_fields = [
        "candidate_path", "original_path", "destination", "primary_owner", "lane_class",
        "artifact_type", "git_blob_oid", "sha256", "atomic_family_id", "disposition",
        "proposed_batch_id", "operational_inbound_count", "forensic_inbound_count",
        "forensic_inbound_sources", "outbound_imports", "runtime_paths",
        "generated_outputs", "required_companions", "frozen_companions",
        "unresolved_runtime_paths", "test_scope", "frontier_or_control",
        "future_exact_pointer_changes", "ruling_basis",
    ]
    write_tsv(OUT / "COMPLETE_CANDIDATE_LEDGER.tsv", ledger, ledger_fields)
    write_tsv(OUT / "DEPENDENCY_EVIDENCE.tsv", evidence,
              ["candidate_path", "line", "evidence_type", "raw_target", "resolved_target",
               "status", "load_bearing", "detail"])

    graph_families = []
    by_ledger_path = {str(row["candidate_path"]): row for row in ledger}
    for family_id, members in sorted(family_members.items()):
        dispositions = {str(by_ledger_path[path]["disposition"]) for path in members}
        assert len(dispositions) == 1
        graph_families.append({
            "family_id": family_id,
            "candidate_members": sorted(members),
            "candidate_count": len(members),
            "disposition": next(iter(dispositions)),
            "lane_class": by_ledger_path[members[0]]["lane_class"],
        })
    graph = {
        "schema": "R1E_ATOMIC_FAMILY_GRAPH_V1",
        "base": "b59005dba9acaf6c575185876655bd6a5c792094",
        "candidate_universe_sha256": sha256(CANDIDATES),
        "candidate_count": len(ledger),
        "family_count": len(graph_families),
        "nodes": sorted(graph_nodes.values(), key=lambda node: str(node["id"])),
        "edges": sorted(graph_edges, key=lambda edge: (str(edge["source"]), str(edge["target"]), str(edge["kind"]))),
        "families": graph_families,
    }
    (OUT / "ATOMIC_FAMILY_GRAPH.json").write_text(json.dumps(graph, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    plan_rows: list[dict[str, object]] = []
    ranking_rows: list[dict[str, object]] = []
    for rank, (batch_id, paths) in enumerate(SAFE_BATCHES.items(), 1):
        rows = [by_ledger_path[path] for path in paths]
        lane = str(rows[0]["lane_class"])
        assert {row["lane_class"] for row in rows} == {lane}
        assert all(row["disposition"] == "SAFE_BYTE_IDENTICAL" for row in rows)
        for row in rows:
            plan_rows.append({
                "batch_id": batch_id,
                "lane_class": lane,
                "current_path": row["candidate_path"],
                "destination": row["destination"],
                "atomic_family_id": row["atomic_family_id"],
                "git_blob_oid": row["git_blob_oid"],
                "sha256": row["sha256"],
                "artifact_content_edit": "NONE_BYTE_IDENTICAL_GIT_MV_ONLY",
                "exact_future_pointer_plan": row["future_exact_pointer_changes"],
            })
        ranking_rows.append({
            "rank": rank,
            "batch_id": batch_id,
            "lane_class": lane,
            "file_count": len(rows),
            "atomic_family_count": len({row["atomic_family_id"] for row in rows}),
            "disposition": "SAFE_BYTE_IDENTICAL",
            "size_preference": "EXCEPTION_ATOMIC_ACTIVE_QUARTET" if len(rows) < 5 else "WITHIN_5_TO_25",
            "status": "PROPOSED_NOT_AUTHORIZED",
            "rationale": (
                "four independently audited SymPy/stdout verifiers; active/legacy separation forbids padding"
                if rank == 1 else
                "dependency-free legacy standalone scripts; no runtime paths, outputs, test globs, or operational inbound pointers"
            ),
        })
    write_tsv(OUT / "PROPOSED_BATCH_FILE_PLAN.tsv", plan_rows,
              ["batch_id", "lane_class", "current_path", "destination", "atomic_family_id",
               "git_blob_oid", "sha256", "artifact_content_edit", "exact_future_pointer_plan"])
    write_tsv(OUT / "BATCH_RANKING.tsv", ranking_rows,
              ["rank", "batch_id", "lane_class", "file_count", "atomic_family_count",
               "disposition", "size_preference", "status", "rationale"])

    schema_rows = [
        (1, "migration_id", "YES", "globally unique append-only event identifier", "R1F-YYYYMMDD-NNN"),
        (2, "committed_at_utc", "YES", "commit timestamp in UTC", "ISO-8601"),
        (3, "phase", "YES", "authorized migration phase", "R1F_OR_LATER"),
        (4, "batch_id", "YES", "preregistered batch identifier", "non-empty"),
        (5, "original_path", "YES", "fixed-base artifact identity", "CURRENT_ARTIFACT_PATHS.original_path"),
        (6, "old_current_path", "YES", "path immediately before migration", "tracked path"),
        (7, "new_current_path", "YES", "path immediately after migration", "tracked path"),
        (8, "rename_score", "YES", "Git rename identity", "R100"),
        (9, "git_blob_oid_before", "YES", "pre-move blob", "40 hex"),
        (10, "git_blob_oid_after", "YES", "post-move blob", "same as before"),
        (11, "sha256_before", "YES", "pre-move bytes", "64 hex"),
        (12, "sha256_after", "YES", "post-move bytes", "same unless separately authorized pointer-only source"),
        (13, "pointer_change_record", "YES", "exact path-only changes outside fixed history", "path:before_sha:after_sha or NONE"),
        (14, "verification_record", "YES", "machine verification artifact", "tracked relative path"),
        (15, "commit", "YES", "migration commit", "40 hex"),
        (16, "rollback_parent", "YES", "parent restoring pre-migration tree", "40 hex"),
        (17, "notes", "NO", "non-authoritative operational note", "single line"),
    ]
    write_tsv(OUT / "PROPOSED_MIGRATION_LEDGER_SCHEMA.tsv",
              [{"ordinal": a, "column": b, "required": c, "semantics": d, "allowed_or_format": e}
               for a, b, c, d, e in schema_rows],
              ["ordinal", "column", "required", "semantics", "allowed_or_format"])

    summary = {
        "candidate_count": len(ledger),
        "family_count": len(graph_families),
        "disposition_counts": dict(sorted(Counter(str(row["disposition"]) for row in ledger).items())),
        "owner_counts": dict(sorted(Counter(str(row["primary_owner"]) for row in ledger).items())),
        "proposed_batch_counts": {key: len(value) for key, value in SAFE_BATCHES.items()},
        "operational_inbound_edges": 0,
        "frontier_candidates": 0,
        "destination_collisions": 0,
        "candidate_universe_sha256": sha256(CANDIDATES),
    }
    (OUT / "PLAN_SUMMARY.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

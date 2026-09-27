#!/usr/bin/env python3
"""Bounded literal-reference evidence; findings need human consumer adjudication."""
import collections
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
BASE = "8aac11e13a2311347771e11f507f4f2042ea02a2"
EXCLUDED = [
    "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/",
    "udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/",
    "udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/",
]
CANDIDATES = [
    "ANGULAR_TORIC_HANDOFF_UPDATE_PREREG_2026-07-19.md",
    "CODEX_ZERO_CONTEXT_STARTUP_REHEARSAL_2026-07-19.md",
    "CODEX_ZERO_CONTEXT_STARTUP_REHEARSAL_PREREG_2026-07-19.md",
    "REORGANIZATION_R0_PREREG_2026-07-18.md",
    "UDT_GR_TO_UDT_SELECTOR_AUDIT_PREREG_2026-07-18.md",
    "UDT_NATIVE_HOPFION_STARTUP_INTEGRATION_PREREG_2026-07-19.md",
    "UDT_SCIENTIFIC_CHECKPOINT_INTEGRATION_PREREG_2026-07-19.md",
    "UDT_WORKSTATION_TRANSFER_MANIFEST_2026-07-17.md",
    "cognitive_corral_triggers_results.md",
    "p3_discipline_skills_results.md",
    "p4_cross_model_verify_results.md",
    "p5_live_state_shrink_results.md",
    "COGNITIVE_CORRAL_TRIGGERS_SETUP.md",
    "simple_metric_session_self_audit_2026-07-09.md",
    "macro_pathB_dust_WP1_results.md",
    "UDT_NATIVE_ACTION_WORKSTATION_SYNC_DISPATCH.md",
    "UDT_NATIVE_ACTION_STAGE1_LAUNCH_RECORD_2026-07-17.md",
    "UDT_NATIVE_ACTION_STAGE2_LAUNCH_RECORD_2026-07-18.md",
    "UDT_NATIVE_ACTION_ARM_C_LAUNCH_RECORD_2026-07-18.md",
    "UDT_H3_STATIC_MASS_BACKREACTION_DISPATCH.md",
    "threadB_WORKSTATION_DISPATCH.md",
    "verify_udt_reciprocal_c_postulate_out.txt",
    "cascade_bv8_falsifiers_out.txt",
    "SOLVER_INTEGRITY_UPGRADES_SPEC.md",
    "UDT_METRIC_KERNEL_DEVELOPMENT_FIDELITY_REVIEW_2026-09-05.md",
    "UDT_METRIC_KERNEL_FOUNDATIONS_FIDELITY_REVIEW_2026-09-05.md",
    "UDT_METRIC_KERNEL_OBSERVER_PAIR_FIDELITY_REVIEW_2026-09-05.md",
    "UDT_NATIVE_ACTION_ARM_C_RETURN_2026-07-18.md",
    "UDT_NATIVE_ACTION_COLD_ARM_DISPATCH.md",
    "UDT_NATIVE_ACTION_COLD_PACKET.md",
    "UDT_NATIVE_ACTION_DERIVATION_DISPATCH.md",
    "UDT_NATIVE_ACTION_FINAL_ADJUDICATION_PREREG_2026-07-18.md",
    "UDT_NATIVE_ACTION_FINAL_ADJUDICATION_RETURN_2026-07-18.md",
    "UDT_NATIVE_ACTION_STAGE1_RETURN_2026-07-18.md",
    "UDT_NATIVE_ACTION_STAGE2_RETURN_2026-07-18.md",
    "UDT_NATIVE_ACTION_WORKSTATION_SYNC_AUDIT_2026-07-17.md",
    "UDT_F_POSTRETURN_AUDIT_AND_CODEX_TRANSITION_DISPATCH.md",
    "UDT_H3_BOUNDARY_AUDIT_PATCH_THEN_F_DISPATCH.md",
    "UDT_H3_BOUNDARY_VIRIAL_CLOSURE_BEFORE_F_DISPATCH.md",
    "UDT_H3_CORRECTED_G_THEN_F_SEQUENCING_DISPATCH.md",
    "hopfion_WORKSTATION_DISPATCH_GP_switch.md",
    "hopfion_WORKSTATION_DISPATCH_phase2_metric.md",
    "threadB_WORKSTATION_DISPATCH_mirror_vs_wall.md",
    "P4_COLD_ADVERSARIAL_REVIEW_SUGGESTION_2026-08-01.md",
    "UDT_EXTERNAL_AI_REVIEW_BRIEF_2026-07-28.md",
    "EXTERNAL_REVIEW_RETURN_2026-07-28_fresh_perspective.md",
    "relay_claudeai_2026-07-02.md",
    "UDT_COMPLETION_REPORT.md",
    "P4_ARC_SUMMARY_2026-07-31.md",
    "UDT_DOTTED_LINE.md",
    "UDT_ELEGANCE_UNCOVER.md",
    "UDT_METHOD_MUSIC.md",
    "UDT_NATURE_LEAN_FRAME.md",
    "ROADMAP_LINEAR_TIME_2026-07-31.md",
    "PONDER_100KLY_VIEW_2026-07-31.md",
]

def run(args, *, allow_grep_empty=False):
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
    if result.returncode and not (allow_grep_empty and result.returncode == 1):
        raise RuntimeError(result.stderr)
    return result.stdout

def table(name, rows, columns):
    with (OUT / name).open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

def main():
    assert run(["git", "rev-parse", "HEAD"]).strip() == BASE
    tracked = run(["git", "ls-tree", "-r", "--full-tree", BASE]).splitlines()
    index = {}
    for line in tracked:
        mode_kind_oid, path = line.split("\t", 1)
        mode, kind, oid = mode_kind_oid.split()
        index[path] = {"mode": mode, "kind": kind, "oid": oid}
    roots = {path for path in index if "/" not in path}
    assert set(CANDIDATES) <= roots
    excludes = [":(exclude)" + path + "**" for path in EXCLUDED]
    patterns = ["*.py", "*.md", "*.tsv", "*.json", "*.txt", "*.sh", "*.ini", "*.yml", "*.yaml", "*.toml", "*.cfg", "*.rst", "*.sha256", "*SHA256*", "*MANIFEST*"]
    references, summary = [], []
    for candidate in CANDIDATES:
        command = ["git", "grep", "-I", "-n", "-F", candidate, "--", *patterns, *excludes]
        output = run(command, allow_grep_empty=True)
        paths = set()
        # splitlines also splits literal Unicode paragraph separators inside a
        # source line, which destroys git grep's path:line:text record framing.
        for line in output.split("\n"):
            if not line:
                continue
            source, number, text = line.split(":", 2)
            assert not any(source.startswith(path) for path in EXCLUDED)
            paths.add(source)
            references.append({"candidate": candidate, "source": source,
                               "line": number, "literal_text": text})
        summary.append({"candidate": candidate, "reference_files": len(paths),
                        "python_files": ";".join(sorted(p for p in paths if p.endswith(".py"))),
                        "manifest_or_pin_files": ";".join(sorted(p for p in paths if any(t in p.upper() for t in ("MANIFEST", "SHA256", "HASH", "SOURCE_PIN")))),
                        "search_status": "LITERAL_MATCHES_NOT_DEPENDENCY_ADJUDICATION"})
    table("LITERAL_REFERENCES.tsv", references, ["candidate", "source", "line", "literal_text"])
    table("CANDIDATE_REFERENCE_SUMMARY.tsv", summary, ["candidate", "reference_files", "python_files", "manifest_or_pin_files", "search_status"])
    # Known original paths only: do not expose or dump the full historical ledger.
    with (ROOT / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv").open() as handle:
        relocation = list(csv.DictReader(handle, delimiter="\t"))
    selected = [row for row in relocation if row["original_path"] in CANDIDATES]
    table("SELECTED_RELOCATION_ROWS.tsv", selected, list(relocation[0]))
    by_oid = collections.defaultdict(list)
    for path, entry in index.items():
        if not any(path.startswith(e) for e in EXCLUDED):
            by_oid[entry["oid"]].append(path)
    duplicates = [{"candidate": candidate, "git_blob_oid": index[candidate]["oid"], "same_blob_path": other}
                  for candidate in CANDIDATES for other in by_oid[index[candidate]["oid"]] if other != candidate]
    table("SELECTED_DUPLICATE_BLOBS.tsv", duplicates, ["candidate", "git_blob_oid", "same_blob_path"])
    metadata = {"baseline": BASE, "branch": run(["git", "branch", "--show-current"]).strip(),
                "tracked_paths": len(index), "root_files": len(roots),
                "root_extensions": dict(collections.Counter(Path(p).suffix for p in roots)),
                "selected_candidates": len(CANDIDATES), "relocation_matches": len(selected),
                "literal_reference_rows": len(references), "python_version": sys.version,
                "git_version": run(["git", "--version"]).strip(), "excluded_content": EXCLUDED,
                "method": "git tracked text fixed-string search; no protected content; no untracked source reads; metadata-only Git object identity comparison; literal matches require consumer review"}
    (OUT / "SCAN_METADATA.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(json.dumps(metadata, indent=2))

if __name__ == "__main__":
    main()

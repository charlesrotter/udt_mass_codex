#!/usr/bin/env python3
"""Fail closed on current foundational premise and startup-precedence regressions."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent

PREMISE_REGISTRY_CONTROLS = (
    "AGENTS.md",
    "LIVE.md",
    "HANDOFF.md",
    "INDEX.md",
    "MEMORY.md",
    "README.md",
    "research/README.md",
    "research/_registry/README.md",
    "CURRENT_RESEARCH_PROGRAM.md",
    "CURRENT_SCIENTIFIC_PREMISES.md",
    "CLAUDE.md",
    "INFLIGHT_STATE.md",
)

CURRENT_ORIENTATION_CONTROLS = (
    "AGENTS.md",
    "LIVE.md",
    "HANDOFF.md",
    "INDEX.md",
    "MEMORY.md",
    "README.md",
    "research/README.md",
    "research/_registry/README.md",
    "CURRENT_RESEARCH_PROGRAM.md",
    "CURRENT_SCIENTIFIC_PREMISES.md",
    "CLAUDE.md",
)

RETIRED_COMPATIBILITY_CONTROLS = (
    "INFLIGHT_STATE.md",
)

HISTORICAL_ROOT_GUARDS = (
    "STATE.md",
    "HANDOFF_ARCHIVE.md",
    "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
    "PURSUIT_CHARTER_2026-07-04.md",
    "UDT_ELEGANT_FRAME.md",
    "SIMPLE_METRIC_MACRO.md",
    "PROBLEM_STATEMENT.md",
    "CODEX_ZERO_CONTEXT_STARTUP_REHEARSAL_2026-07-19.md",
    "CODEX_ZERO_CONTEXT_STARTUP_REHEARSAL_PREREG_2026-07-19.md",
)

FIXED_ROOT_PROVENANCE_PATHS = (
    "CODEX_STARTUP_REHEARSAL_2026-07-17.md",
    "codex_rehearsal_final.md",
    "codex_rehearsal_transcript.txt",
)

STARTUP_ARCHIVE_CONTROLS = (
    "archive/startup_surface_2026-08-22_pre_cleanup/README.md",
    "archive/startup_surface_2026-08-22_pre_cleanup/BASELINE_REHEARSAL_LEDGER.tsv",
    "archive/startup_surface_2026-08-22_pre_cleanup/POST_REPAIR_REHEARSAL_LEDGER.tsv",
    "archive/startup_surface_2026-08-22_pre_cleanup/REPAIR_SCOPE.md",
)

STARTUP_SURFACE_CONTROLS = (
    CURRENT_ORIENTATION_CONTROLS
    + RETIRED_COMPATIBILITY_CONTROLS
    + HISTORICAL_ROOT_GUARDS
    + STARTUP_ARCHIVE_CONTROLS
)

MAPPED_SKILL_FILES = (
    ".claude/skills/no-shortcuts/SKILL.md",
    ".claude/skills/solver-first/SKILL.md",
    ".claude/skills/completeness-map/SKILL.md",
    ".claude/skills/verifier-before-record/SKILL.md",
    ".claude/skills/solution-space-not-imposition/SKILL.md",
)

STALE_STARTUP_TOKENS = (
    "CMB PEAK OPTIMIZATION",
    "ACTIVE ARC =",
    "G86 remains the latest",
    "fresh restart pending",
    "x_max O1 pending",
    "global cell assembly lane is active",
    "udt-r3-covariance-patchlists-20260813.service",
    "Complete R3 -> assemble -> independently verify",
    "194 component cells -> assembly -> independent verification -> outcome inspection",
    "external review pending",
    "first end-to-end house test",
    "R5 data-only common-subspace assembly",
    "Preregister the asymptotic-response classes of G153",
    "Preregister a bounded asymptotic-response classification of G153",
    "culminates in the G129--G133 reconstruction/ownership chain",
    "Current artifact locations come from `research/_registry/CURRENT_ARTIFACT_PATHS.tsv`",
)

ARCHIVED_STARTUP_SNAPSHOTS = {
    "AGENTS_before_cleanup.md": ("4c4acf412daeb2761a19a3877ac1e589c69572d9c65c8a6fc5756789f7945bb3", 347),
    "LIVE_before_cleanup.md": ("4edd35923db884a14ca8d1995119184044abbc9d3897229d1a2fee5dab63928a", 1314),
    "HANDOFF_before_cleanup.md": ("2f307c1a4c8972a9b8e6aa9cb66a8f30b33a0d2d9427621f66dbb05e8738b56f", 839),
    "INDEX_before_cleanup.md": ("abb7bb9a9bf46478ca21a5fa8ff51f594ee0a370e081aaae0c6fb580b9b2f386", 527),
    "MEMORY_before_cleanup.md": ("fc9aef1bcd82e25f3e0f09bd7aed16fd2def3d85c0f8823c7439bce865b50f71", 471),
    "CURRENT_RESEARCH_PROGRAM_before_cleanup.md": ("714a6d3fde1709289863f19cd3e134cc968a3f6972df8671d111eee5d4e7b3e8", 759),
    "CURRENT_SCIENTIFIC_PREMISES_before_cleanup.md": ("e4e936e4408ced06ce2633462c0b9aaf3491e0a2ce56a2e5b484f53fe68dfcdb", 917),
    "README_before_cleanup.md": ("d25c29b891a702345c06bc9767ccb38cdb345c0dc53cef106768f3dc2baf8ea9", 452),
    "research_README_before_cleanup.md": ("a66a5653ead353b6c124ae2fa451ff61aef22080519a8ad05e64e4ad742ddfe8", 308),
    "research_registry_README_before_cleanup.md": ("74ca21670526a7b6a1731b514b35be32ec0d93a415627c4140f0337f7db16224", 232),
    "INFLIGHT_STATE_before_cleanup.md": ("0ab4394549b72f17a4fbdee75425d1da91a75d8d5cb13da5bb8051e7a748704f", 278),
    "verify_current_scientific_premises_before_cleanup.py": ("f2abb9928bab03960fdfe7bb1283419abd3c04d63eab301eaa7326f10adb236c", 1411),
    "test_startup_surface_before_cleanup.py": ("4e293c1d2204d2ec4d4c1b71f9f3dec62a43ce75ca32e899b15dcb195c0aee76", 420),
}

PRE_ZOOMOUT_STARTUP_SNAPSHOTS = {
    "AGENTS.md": ("b8281460b0661c9a8a3d129eefc3ea2bdf7617ca55f2270acb366fe70836d10d", 195),
    "LIVE.md": ("708e52f3bb97b2f70dcf43e31c4ee4e0d42ee466a7f86d3d720cfb3a1ea9fac1", 170),
    "HANDOFF.md": ("3f243e99bd1a6ccde29376c1e31bff739e946ea3251289651a9146b8cc60b50c", 130),
    "CURRENT_RESEARCH_PROGRAM.md": ("c871d62c0f768706da914099dafbdcc62afc806454c59210f827a8d549aa3957", 170),
    "CURRENT_SCIENTIFIC_PREMISES.md": ("5259b543f6dc179e91f2760901ac6903534bba5e520152cc64f7fc1ce187e999", 150),
    "INDEX.md": ("d48def69cbcf64c6115991b11fb8466e1f838dede8ced111293d6480e262004b", 100),
    "MEMORY.md": ("3ac19868b3bf431e5b44d8f877cbcb089cf2e3b8bff6864c64a5cad168bdecb5", 80),
    "root_README.md": ("d5b684dcb5ff0b97a411274943261e54bb06c3c741d4502c145feb6c77d41868", 49),
    "research_README.md": ("43819d472fd76d873e26f2922e55d0ba4af6c8bb78fa12b2dadd1b4e00c4912e", 35),
    "research_registry_README.md": ("1d409ee70bd45eb7839b8ea6d4c9a223367019536dfd7e5078125d800e4debe9", 31),
    "INFLIGHT_STATE.md": ("ea0a37eab7d264d0ae32ad784b3850110fdab3a164af92e3a5342b066514c75b", 17),
    "verify_current_scientific_premises.py": ("d129e654e3a7833ffb38f5e21cc6206aecfa864c4c31257f5affd0b5825fe291", 2710),
    "test_startup_surface.py": ("19c079a1bb448943b5456c644c9ae15bf178c158b239fa8aaef49a316ecc7326", 265),
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def require_ordered_tokens(text: str, tokens: tuple[str, ...], name: str) -> None:
    """Require each startup-routing token to occur after its predecessor."""
    text = " ".join(text.split())
    cursor = 0
    for token in tokens:
        position = text.find(token, cursor)
        require(position >= 0, f"startup order broken at {token}: {name}")
        cursor = position + len(token)


def marked_current_block(path: Path) -> str:
    """Return the bounded startup block; fail closed on missing or duplicate markers."""
    text = path.read_text(encoding="utf-8")
    begin = "<!-- STARTUP_CURRENT_BEGIN -->"
    end = "<!-- STARTUP_CURRENT_END -->"
    require(text.count(begin) == 1, f"current-block begin marker count: {path.name}")
    require(text.count(end) == 1, f"current-block end marker count: {path.name}")
    start = text.index(begin) + len(begin)
    stop = text.index(end, start)
    return text[start:stop]


def validate_startup_surface(root: Path) -> None:
    """Fail closed on current routing while preserving, not rereading, historical detail."""
    controls: dict[str, str] = {}
    for relative in STARTUP_SURFACE_CONTROLS:
        path = root / relative
        require(path.is_file(), f"missing startup control: {relative}")
        controls[relative] = path.read_text(encoding="utf-8")

    for control in PREMISE_REGISTRY_CONTROLS:
        require(
            "CURRENT_SCIENTIFIC_PREMISES.tsv" in controls[control],
            f"control lacks premise registry: {control}",
        )

    live = marked_current_block(root / "LIVE.md")
    handoff = marked_current_block(root / "HANDOFF.md")
    for name, block in (("LIVE.md", live), ("HANDOFF.md", handoff)):
        normalized = " ".join(block.split())
        for token in (
            "udt_uncompressed_pair_kernel_reconstruction_2026-08-14",
            "B,Q,S,Y,Z",
            "phi_pair",
            "c_eff",
            "G166--G221",
            "G197",
            "G215",
            "G216",
            "G217",
            "G218",
            "G219",
            "G220",
            "G221",
            "G190--G198",
            "WORKING_FOUNDATIONAL_CLARIFICATION",
            "supplied",
            "formula-level regression",
            "G116/G189",
            "construction inputs",
            "udt_observed_angular_pattern_raw_restart_2026-08-12",
            "/media/udt-admin/ScratchDisk/Data/UDT_BOSS_R3_2026-08-14/",
            "184,300",
            "CURRENT_SCIENTIFIC_PREMISES.tsv",
            "archive/startup_surface_2026-08-17_pre_zoomout",
            "archive/startup_surface_2026-08-21_pre_g197",
            "archive/startup_surface_2026-08-22_pre_cleanup",
            "higher/full",
            "OPEN",
        ):
            require(token in normalized, f"marked current block lacks {token}: {name}")
        require("R2--R5" in normalized and "verified with caveats" in normalized.lower(), f"R2--R5 grade absent: {name}")
        require(
            "no preferred" in normalized.lower(),
            f"observational no-preferred-selection guard absent: {name}",
        )

    for token in (
        "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/",
        "udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/",
        "udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/",
        "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/",
    ):
        require(token in live, f"LIVE lacks protected local path: {token}")
        require(token in handoff, f"HANDOFF lacks protected local path: {token}")
    require("udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/" in controls["AGENTS.md"],
            "AGENTS lacks protected curvature-atlas guard")
    require("Primary-kernel regression gate" in controls["AGENTS.md"],
            "AGENTS guard absent: Primary-kernel regression gate")
    require("WORKING_FOUNDATIONAL_CLARIFICATION` (G176)" in controls["AGENTS.md"],
            "AGENTS lacks G176 completed-pair clarification")

    required_routes = {
        "AGENTS.md": (
            "Stop the startup read here",
            "does not make full scripts",
            "205-row exact registry",
            "without dumping its wide rows into model context",
            "1,114 data rows plus its header",
            "not a startup read or a current-frontier index",
            "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md",
            "SIMPLE_METRIC_MACRO.md",
            "pointwise-`phi`",
        ),
        "INDEX.md": (
            "udt_observed_angular_pattern_raw_restart_2026-08-12/",
            "R5_OUTCOME_REPORT.md",
            "R5_EXTERNAL_FOLLOWUP_REVIEW.md",
            "R5_FINAL_EVIDENCE_MANIFEST.tsv",
            "udt_uncompressed_pair_kernel_reconstruction_2026-08-14/",
            "udt_pair_first_relational_plane_reconstruction_2026-08-12/",
            "udt_pair_terminal_reachability_atlas_2026-08-12/",
            "udt_pair_chord_network_descent_audit_2026-08-12/",
            "udt_g116_calibrated_frequency_terminal_pair_junction_2026-08-16/",
            "udt_g119_finite_radius_timelive_spherical_screen_theorem_2026-08-16/",
            "udt_g166_primary_metric_ordered_pair_kernel_descent_2026-08-18/",
            "udt_g167_primary_metric_full_pair_pullback_orchestra_2026-08-18/",
            "udt_g176_completed_pair_dual_reciprocity_consolidation_2026-08-19/",
            "udt_g177_completed_pair_kernel_scaffolding_regression_audit_2026-08-19/",
            "udt_g178_completed_pair_kernel_fresh_adversarial_review_2026-08-19/",
            "udt_g179_complete_coframe_pair_pullback_extension_2026-08-19/",
            "udt_g184_regular_branch_equivalence_classification_2026-08-19/",
            "udt_g188_complete_coframe_null_jacobi_extension_2026-08-20/",
            "udt_g190_completed_pair_timelive_frequency_screen_join_2026-08-20/",
            "udt_g195_antisymmetric_screen_rotation_boundary_2026-08-20/",
            "udt_g196_longitudinal_screen_mixing_descent_2026-08-20/",
            "udt_g197_native_kernel_provenance_and_startup_integrity_audit_2026-08-21/",
            "udt_g198_bidirectional_null_germ_map_2026-08-21/",
            "udt_g199_primary_metric_bidirectional_radial_null_2026-08-21/",
            "udt_g200_primary_metric_bidirectional_nonradial_null_2026-08-21/",
            "udt_g201_primary_metric_phi_jet_regime_amplitude_2026-08-21/",
            "udt_g202_quiet_overlap_profile_anchor_classification_2026-08-21/",
            "udt_g203_quiet_overlap_parameter_ownership_classification_2026-08-21/",
            "udt_g204_primary_metric_global_regularity_asymptotic_profile_2026-08-21/",
            "udt_g205_primary_metric_geodesic_causal_completion_2026-08-21/",
            "udt_g206_g205_conformal_timelive_nonspherical_robustness_2026-08-21/",
            "udt_g207_g205_tracefree_screen_timelive_robustness_2026-08-21/",
            "udt_g208_g205_radial_screen_mixing_robustness_2026-08-21/",
            "udt_g209_g205_timespace_shift_robustness_2026-08-21/",
            "udt_g210_g205_spatial_volume_robustness_2026-08-21/",
            "udt_g211_complete_diagonal_scalar_basis_closure_2026-08-22/",
            "udt_g212_observer_equivalence_history_bridge_whiteboard_2026-08-22/",
            "udt_g213_determinant_one_spatial_remainder_and_completed_rank_closure_2026-08-22/",
            "udt_g214_completed_tuple_overlap_and_three_observer_carry_2026-08-22/",
            "udt_g215_completed_scalar_shared_clock_incidence_descent_2026-08-22/",
            "udt_g216_observer_event_comparison_clock_rate_ownership_2026-08-22/",
            "udt_g217_founded_depth_event_pair_first_jet_ownership_2026-08-22/",
            "udt_g218_query_indexed_clock_correspondence_whiteboard_2026-08-22/",
            "udt_g219_clock_arrow_dynamic_protocol_discrimination_2026-08-22/",
            "udt_g220_covariant_null_clock_arrow_timelive_lift_2026-08-22/",
            "udt_g221_complete_coframe_null_clock_chord_2026-08-22/",
            "archive/startup_surface_2026-08-17_pre_zoomout/INDEX.md",
            "archive/startup_surface_2026-08-21_pre_g197/",
            "archive/startup_surface_2026-08-22_pre_cleanup/",
            "archive/scaffolded_kernel_controls_2026-08-19/README.md",
            "Historical negative controls",
            "CLAUDE.md",
            "MEMORY.md",
            "stop and give the orientation report",
            "After orientation",
            "verify_current_scientific_premises.py",
        ),
        "MEMORY.md": (
            "B,Q,S,Y,Z",
            "G166--G221",
            "G197",
            "G198",
            "G199",
            "G200",
            "G201",
            "G202",
            "G203",
            "G204",
            "G205",
            "G206",
            "G207",
            "G208",
            "G209",
            "G210",
            "G211",
            "G212",
            "G213",
            "G214",
            "G215",
            "G216",
            "G216",
            "G217",
            "G218",
            "G219",
            "G220",
            "G221",
            "formula-level regression",
            "off-ray",
            "R2--R5",
            "/media/udt-admin/ScratchDisk/Data/UDT_BOSS_R3_2026-08-14/",
            "CURRENT_SCIENTIFIC_PREMISES.tsv",
            "archive/startup_surface_2026-08-17_pre_zoomout/",
            "archive/startup_surface_2026-08-21_pre_g197/",
        ),
        "CURRENT_RESEARCH_PROGRAM.md": (
            "udt_uncompressed_pair_kernel_reconstruction_2026-08-14/",
            "G129--G165",
            "G166--G184",
            "G185--G189",
            "G190--G198",
            "G197",
            "G198",
            "G199",
            "G200",
            "G201",
            "G202",
            "G203",
            "G204",
            "G205",
            "G206",
            "G207",
            "G208",
            "G209",
            "G210",
            "G211",
            "G212",
            "G213",
            "G214",
            "G215",
            "G216",
            "G217",
            "G218",
            "G219",
            "G220",
            "G221",
            "WORKING_FOUNDATIONAL_CLARIFICATION",
            "STANDARD_GEOMETRIC_EVALUATOR",
            "formula-level regression",
            "184,300",
        ),
        "CURRENT_SCIENTIFIC_PREMISES.md": (
            "working asymptotic global-completion consequence target",
            "CHALLENGED_OWNER_POSTULATE_NOT_DERIVED",
            "CURRENT_SCIENTIFIC_PREMISES.tsv",
            "G129--G165",
            "G166--G175",
            "G176--G180",
            "G181--G184",
            "G185--G189",
            "G190--G198",
            "G199",
            "G200",
            "G201",
            "G202",
            "G203",
            "G204",
            "G205",
            "G206",
            "G207",
            "G208",
            "G209",
            "G210",
            "G211",
            "G212",
            "G213",
            "G214",
            "G215",
            "G220",
            "G221",
            "positive conformal class",
            "Founded pair common scale",
            "bivector area bilinear",
            "205-row",
        ),
        "README.md": (
            "LIVE.md",
            "CURRENT_SCIENTIFIC_PREMISES.tsv",
            "verify_current_scientific_premises.py",
            "after orientation",
            "AGENTS.md",
            "CLAUDE.md",
            "How we work",
            "DRIVER TRIGGERS",
            "Repo discipline",
            "INDEX.md",
            "MEMORY.md",
            "stop and give the orientation report",
            "archive/startup_surface_2026-08-22_pre_cleanup/",
            "codex_rehearsal_final.md",
            "historical/search-only evidence",
            "common-scale, elegant-frame, simple-metric, problem-statement",
        ),
        "CLAUDE.md": (
            "This file is binding method, not scientific status",
            "CURRENT_SCIENTIFIC_PREMISES.tsv",
            "verify_current_scientific_premises.py",
            "without dumping the exact registry into context",
            "stop and give the orientation report",
            "mnemonic trigger labels, not filesystem paths",
            ".claude/skills/no-shortcuts/SKILL.md",
            ".claude/skills/solver-first/SKILL.md",
            ".claude/skills/completeness-map/SKILL.md",
            ".claude/skills/verifier-before-record/SKILL.md",
            "historical relocation ledger",
            "not a current-frontier index",
            "Use `INDEX.md` for current evidence routes",
        ),
        "research/README.md": (
            "CURRENT_ARTIFACT_PATHS.tsv",
            "CURRENT_SCIENTIFIC_PREMISES.tsv",
            "After orientation",
            "verify_current_scientific_premises.py",
            "1,114 data rows plus header",
            "How we work",
            "DRIVER TRIGGERS",
            "Repo discipline",
            "stop and give the orientation report",
            "not a startup read",
        ),
        "research/_registry/README.md": (
            "CURRENT_ARTIFACT_PATHS.tsv",
            "CURRENT_SCIENTIFIC_PREMISES.tsv",
            "1,114 data rows plus its header",
            "not a startup read",
            "not a current-frontier index",
        ),
        "INFLIGHT_STATE.md": (
            "retired compatibility pointer",
            "INFLIGHT_STATE_before_cleanup.md",
            "After orientation",
            "verify_current_scientific_premises.py",
            "CLAUDE.md",
            "How we work",
            "DRIVER TRIGGERS",
            "Repo discipline",
            "INDEX.md",
            "MEMORY.md",
            "stop and give the orientation report",
        ),
    }
    for control, tokens in required_routes.items():
        for token in tokens:
            require(token in controls[control], f"current route lacks {token}: {control}")

    ordered_routes = {
        "AGENTS.md": (
            "1. `LIVE.md`",
            "2. `HANDOFF.md`",
            "3. `CURRENT_RESEARCH_PROGRAM.md`",
            "4. `CURRENT_SCIENTIFIC_PREMISES.md`",
            "python3 verify_current_scientific_premises.py",
            "5. `CLAUDE.md`",
            "6. `INDEX.md` and `MEMORY.md`",
            "7. **Stop the startup read",
        ),
        "README.md": (
            "1. `LIVE.md`",
            "2. `HANDOFF.md`",
            "3. `CURRENT_RESEARCH_PROGRAM.md`",
            "4. `CURRENT_SCIENTIFIC_PREMISES.md`",
            "python3 verify_current_scientific_premises.py",
            "5. `CLAUDE.md`",
            "6. `INDEX.md` and `MEMORY.md`",
            "7. stop and give the orientation report",
        ),
        "INFLIGHT_STATE.md": (
            "1. `LIVE.md`",
            "2. `HANDOFF.md`",
            "3. `CURRENT_RESEARCH_PROGRAM.md`",
            "4. `CURRENT_SCIENTIFIC_PREMISES.md`",
            "python3 verify_current_scientific_premises.py",
            "5. `CLAUDE.md`",
            "6. `INDEX.md` and `MEMORY.md`",
            "7. stop and give the orientation report",
        ),
        "research/README.md": (
            "1. the current blocks in `../LIVE.md` and `../HANDOFF.md`",
            "2. `../CURRENT_RESEARCH_PROGRAM.md`",
            "3. `../CURRENT_SCIENTIFIC_PREMISES.md`",
            "python3 ../verify_current_scientific_premises.py",
            "4. `../CLAUDE.md`",
            "5. `../INDEX.md` and `../MEMORY.md`",
            "6. stop and give the orientation report",
        ),
        "INDEX.md": (
            "1. Follow `AGENTS.md`",
            "2. Read the current blocks in `LIVE.md` and `HANDOFF.md`",
            "3. Read `CURRENT_RESEARCH_PROGRAM.md`",
            "4. Read `CURRENT_SCIENTIFIC_PREMISES.md`",
            "python3 verify_current_scientific_premises.py",
            "5. Read `CLAUDE.md` sections `How we work`, `DRIVER TRIGGERS`, and `Repo discipline`",
            "6. Read `INDEX.md` and `MEMORY.md`",
            "7. After orientation",
        ),
    }
    for control, tokens in ordered_routes.items():
        require_ordered_tokens(controls[control], tokens, control)

    claude_orientation = controls["CLAUDE.md"].split("## Orientation", 1)
    require(len(claude_orientation) == 2, "CLAUDE orientation section missing")
    require_ordered_tokens(
        claude_orientation[1],
        (
            "Work on `grok`",
            "`LIVE.md` is the first read",
            "`HANDOFF.md`",
            "`CURRENT_RESEARCH_PROGRAM.md`",
            "`CURRENT_SCIENTIFIC_PREMISES.md`",
            "python3 verify_current_scientific_premises.py",
            "Always read `How we work`, `DRIVER TRIGGERS`, and `Repo discipline`",
            "`INDEX.md` and `MEMORY.md`",
            "stop and give the orientation report",
        ),
        "CLAUDE.md Orientation",
    )

    normalized_claude = " ".join(controls["CLAUDE.md"].split())
    skill_mapping_phrases = (
        "`apply-purist-logic-proactively` and `derive-natively-not-inherited-form` use `.claude/skills/no-shortcuts/SKILL.md`",
        "`solver-first-not-mechanism` uses `.claude/skills/solver-first/SKILL.md`",
        "`sweep-whole-not-fragments` uses `.claude/skills/completeness-map/SKILL.md`",
        "`session-handoff-pointer` uses `.claude/skills/verifier-before-record/SKILL.md`",
        "`solution-space-not-imposition` maps to its same-named live skill",
    )
    for phrase in skill_mapping_phrases:
        require(phrase in normalized_claude, f"CLAUDE skill mapping missing or changed: {phrase}")
    for relative in MAPPED_SKILL_FILES:
        require((root / relative).is_file(), f"mapped CLAUDE skill missing: {relative}")
    completeness_skill = (root / ".claude/skills/completeness-map/SKILL.md").read_text(encoding="utf-8")
    solver_first_skill = (root / ".claude/skills/solver-first/SKILL.md").read_text(encoding="utf-8")
    require(
        "`archive/SOLVER_COMPLETENESS_MAP.md`" in completeness_skill,
        "completeness skill still targets missing live root instrument",
    )
    require(
        (root / "archive/SOLVER_COMPLETENESS_MAP.md").is_file(),
        "completeness skill archive target missing",
    )
    require(
        "`archive/SOLVER_COMPLETENESS_MAP.md`" in solver_first_skill
        and "- `SOLVER_COMPLETENESS_MAP.md`" not in solver_first_skill,
        "solver-first skill targets missing live completeness map",
    )
    require(
        "update every push" not in completeness_skill,
        "completeness skill retains obsolete update-every-push instruction",
    )

    require(
        re.search(r"\budt_g\d+", controls["README.md"], flags=re.IGNORECASE) is None,
        "README hard-codes a moving G-frontier package",
    )

    require_ordered_tokens(
        controls["INDEX.md"],
        (
            "Chosen-family evaluators/controls:",
            "udt_g196_longitudinal_screen_mixing_descent_2026-08-20/",
            "Historical negative controls — never kernel inputs",
            "udt_g164_scaffold_subtraction_anchor_sufficiency_whiteboard_2026-08-18/",
            "archive/scaffolded_kernel_controls_2026-08-19/README.md",
        ),
        "INDEX chosen-family/scaffold quarantine",
    )

    require(
        "Use root `INDEX.md` for the compact current-frontier path list. It is not a startup read"
        not in controls["research/README.md"],
        "research README ambiguously says INDEX.md is not a startup read",
    )

    relocation = root / "research" / "_registry" / "CURRENT_ARTIFACT_PATHS.tsv"
    require(relocation.is_file(), "relocation ledger missing")
    relocation_lines = relocation.read_text(encoding="utf-8").splitlines()
    require(len(relocation_lines) == 1115, "relocation ledger must have 1,114 data rows plus header")
    relocation_header = (
        "original_path",
        "current_path",
        "path_status",
        "fixed_base_blob_oid",
        "fixed_base_sha256",
    )
    require(
        tuple(relocation_lines[0].split("\t")) == relocation_header,
        "relocation ledger header changed",
    )
    relocation_rows = read_tsv(relocation)
    require(len(relocation_rows) == 1114, "relocation ledger must contain 1,114 parsed data rows")
    require(
        all(None not in row and all((row.get(column) or "").strip() for column in relocation_header)
            for row in relocation_rows),
        "relocation ledger contains a malformed or blank data row",
    )
    require(
        len({row["original_path"] for row in relocation_rows}) == 1114
        and len({row["current_path"] for row in relocation_rows}) == 1114,
        "relocation ledger path columns must remain unique",
    )
    relocation_by_current = {row["current_path"]: row for row in relocation_rows}
    for relative in FIXED_ROOT_PROVENANCE_PATHS:
        require(
            relative in relocation_by_current
            and relocation_by_current[relative]["path_status"] == "ROOT_RETAINED",
            f"fixed root provenance disposition changed: {relative}",
        )

    for control in CURRENT_ORIENTATION_CONTROLS + RETIRED_COMPATIBILITY_CONTROLS:
        lowered = controls[control].lower()
        for token in STALE_STARTUP_TOKENS:
            require(token.lower() not in lowered, f"stale startup token {token}: {control}")

    for relative in HISTORICAL_ROOT_GUARDS:
        opening = " ".join(controls[relative].splitlines()[:12]).lower()
        require(
            ("historical" in opening or "superseded" in opening) and "not current" in opening,
            f"historical root guard missing or weak: {relative}",
        )

    for relative in FIXED_ROOT_PROVENANCE_PATHS:
        require((root / relative).is_file(), f"fixed root provenance missing: {relative}")
        require(relative in controls["AGENTS.md"], f"AGENTS lacks fixed-root quarantine: {relative}")
        require(relative in controls["README.md"], f"README lacks fixed-root quarantine: {relative}")
    require("memory_export.md" in controls["AGENTS.md"], "AGENTS lacks optional memory-export quarantine")
    require("memory_export.md" in controls["README.md"], "README lacks optional memory-export quarantine")
    optional_memory = root / "memory_export.md"
    if optional_memory.is_file():
        opening = " ".join(optional_memory.read_text(encoding="utf-8").splitlines()[:12]).lower()
        require(
            "historical" in opening and ("not current" in opening or "not startup" in opening),
            "optional memory export lacks historical guard",
        )

    archive_pointer = controls["archive/startup_surface_2026-08-22_pre_cleanup/README.md"]
    for token in (
        "4c532da4acb3dd951489f7506d24ded58a205e7f",
        "git show 4c532da4:<path>",
        "Fixed-base July 17 rehearsal files remain at root",
        "changes no scientific verdict",
        "POST_REPAIR_REHEARSAL_LEDGER.tsv",
    ):
        require(token in archive_pointer, f"pre-cleanup archive pointer lacks {token}")

    post_rehearsal = controls[
        "archive/startup_surface_2026-08-22_pre_cleanup/POST_REPAIR_REHEARSAL_LEDGER.tsv"
    ]
    for token in ("C_final", "ROOT_final", "PASS", "122_full_tests"):
        require(token in post_rehearsal, f"post-repair rehearsal ledger lacks {token}")

    for relative in (
        "CURRENT_SCIENTIFIC_PREMISES.tsv",
        "udt_observed_angular_pattern_raw_restart_2026-08-12/R2_OUTCOME_REPORT.md",
        "udt_observed_angular_pattern_raw_restart_2026-08-12/R3_OUTCOME_REPORT.md",
        "udt_observed_angular_pattern_raw_restart_2026-08-12/R3_VERIFICATION_RESULT.json",
        "udt_observed_angular_pattern_raw_restart_2026-08-12/R4_OUTCOME_REPORT.md",
        "udt_observed_angular_pattern_raw_restart_2026-08-12/R4_VERIFICATION_RESULT.json",
        "udt_observed_angular_pattern_raw_restart_2026-08-12/R5_OUTCOME_REPORT.md",
        "udt_observed_angular_pattern_raw_restart_2026-08-12/R5_VERIFICATION_RESULT.json",
        "udt_observed_angular_pattern_raw_restart_2026-08-12/R5_EXTERNAL_FOLLOWUP_REVIEW.md",
        "udt_observed_angular_pattern_raw_restart_2026-08-12/R5_FINAL_EVIDENCE_MANIFEST.tsv",
        "udt_boss_primary_method_crosswalk_2026-08-13/AUDIT_REPORT.md",
        "udt_pair_first_relational_plane_reconstruction_2026-08-12/AUDIT_REPORT.md",
        "udt_pair_terminal_reachability_atlas_2026-08-12/AUDIT_REPORT.md",
        "udt_pair_chord_network_descent_audit_2026-08-12/AUDIT_REPORT.md",
        "udt_uncompressed_pair_kernel_reconstruction_2026-08-14/AUDIT_REPORT.md",
        "udt_g116_calibrated_frequency_terminal_pair_junction_2026-08-16/AUDIT_REPORT.md",
        "udt_g119_finite_radius_timelive_spherical_screen_theorem_2026-08-16/AUDIT_REPORT.md",
        "udt_g129_copresent_relational_network_faithfulness_2026-08-16/AUDIT_REPORT.md",
        "udt_g130_copresence_rank_complete_network_ownership_2026-08-16/AUDIT_REPORT.md",
        "udt_g131_all_plane_terminal_reciprocal_scalar_faithfulness_2026-08-16/AUDIT_REPORT.md",
        "udt_g132_common_scale_owner_and_anchor_audit_2026-08-16/AUDIT_REPORT.md",
        "udt_g133_fixed_K_two_density_overlap_descent_2026-08-16/AUDIT_REPORT.md",
        "udt_g141_endpoint_triangular_transition_inverse_join_2026-08-17/AUDIT_REPORT.md",
        "udt_g142_abstract_carrier_physical_carry_join_2026-08-17/AUDIT_REPORT.md",
        "udt_g143_single_pair_domain_carry_ownership_2026-08-17/AUDIT_REPORT.md",
        "udt_g144_cross_query_overlap_carry_descent_2026-08-17/AUDIT_REPORT.md",
        "udt_g145_copresent_relation_history_descent_equivalence_2026-08-17/AUDIT_REPORT.md",
        "udt_g146_multidirectional_relational_position_composition_2026-08-17/AUDIT_REPORT.md",
        "udt_g147_pair_directional_metric_screen_solder_2026-08-17/AUDIT_REPORT.md",
        "udt_g148_relation_first_pair_first_jet_decomposition_2026-08-17/AUDIT_REPORT.md",
        "udt_g149_genuine_spacetime_pair_first_jet_join_2026-08-17/AUDIT_REPORT.md",
        "udt_g150_first_order_pair_chord_freedom_ceiling_2026-08-17/AUDIT_REPORT.md",
        "udt_g151_pair_chord_generalized_deviation_join_2026-08-17/AUDIT_REPORT.md",
        "udt_g152_pair_immersion_variational_chord_ownership_2026-08-17/AUDIT_REPORT.md",
        "udt_g153_relational_position_ruler_differential_join_2026-08-17/AUDIT_REPORT.md",
        "udt_g188_complete_coframe_null_jacobi_extension_2026-08-20/AUDIT_REPORT.md",
        "udt_g207_g205_tracefree_screen_timelive_robustness_2026-08-21/AUDIT_REPORT.md",
        "udt_g208_g205_radial_screen_mixing_robustness_2026-08-21/AUDIT_REPORT.md",
    ):
        require((root / relative).is_file(), f"current startup target missing: {relative}")

    archive = root / "archive" / "startup_surface_2026-08-14"
    require((archive / "SHA256_MANIFEST.tsv").is_file(), "startup archive manifest missing")
    for name, (expected_hash, expected_lines) in ARCHIVED_STARTUP_SNAPSHOTS.items():
        path = archive / name
        require(path.is_file(), f"startup archive snapshot missing: {name}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        require(digest == expected_hash, f"startup archive hash mismatch: {name}")
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        require(line_count == expected_lines, f"startup archive line-count mismatch: {name}")

    pre_zoomout = root / "archive" / "startup_surface_2026-08-17_pre_zoomout"
    require((pre_zoomout / "SHA256_MANIFEST.tsv").is_file(), "pre-zoomout archive manifest missing")
    for name, (expected_hash, expected_lines) in PRE_ZOOMOUT_STARTUP_SNAPSHOTS.items():
        path = pre_zoomout / name
        require(path.is_file(), f"pre-zoomout startup snapshot missing: {name}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        require(digest == expected_hash, f"pre-zoomout archive hash mismatch: {name}")
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        require(line_count == expected_lines, f"pre-zoomout archive line-count mismatch: {name}")


def main() -> None:
    rows = read_tsv(ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv")
    require(len(rows) == 205, "premise registry must contain exactly 205 rows")
    by_id = {row["premise_id"]: row for row in rows}
    require(len(by_id) == 205, "duplicate premise id")
    require(
        by_id["G196"]["current_status"].startswith(
            "EXTERNALLY_REVIEWED_VERIFIED_WITH_CAVEATS__REPAIR_FOLLOWUP_ACCEPTED__PREREGISTERED"
        ),
        "G196 external-review/repair grade changed",
    )
    for guard in (
        "ARBITRARY_REAL_C2_M_OF_ETA_Z_IN_DECLARED_AFFINE_FAMILY",
        "CENTRAL_OUTGOING_GERM_SELECTS_DPLUS_EQUALS_PARTIAL_ETA_PLUS_PARTIAL_Z",
        "ORDERED_FACTORIZATION_AND_POSITIVE_GRAM_NO_NONVERTEX_CAUSTIC_SURVIVE",
        "SAME_RAY_ALIAS_PROVES_ONE_GERM_DOES_NOT_RECONSTRUCT_OFF_RAY_FIELD",
        "NO_P1_G116_G189_XMAX_TRANSFER_SOURCE_FIT_OR_POST_READOUT_ORCHESTRA",
    ):
        require(guard in by_id["G196"]["current_status"], f"G196 guard absent: {guard}")
    g196 = ROOT / "udt_g196_longitudinal_screen_mixing_descent_2026-08-20"
    for name in (
        "AUDIT_REPORT.md",
        "EXACT_DERIVATION.md",
        "PRODUCTION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "PACKAGE_VERIFICATION_RESULT.json",
        "EXTERNAL_REVIEW_RAW.md",
        "EXTERNAL_REVIEW_ADJUDICATION.md",
        "EXTERNAL_REPAIR_FOLLOWUP_RAW.md",
        "REPAIR_FOLLOWUP_ADJUDICATION.md",
        "REVIEW_REPAIR_PREREGISTRATION.md",
        "REPAIR_VERIFICATION_RESULT.json",
        "SOURCE_MANIFEST.tsv",
    ):
        require((g196 / name).is_file(), f"G196 evidence missing: {name}")
    g196_package = json.loads((g196 / "PACKAGE_VERIFICATION_RESULT.json").read_text())
    require(g196_package["status"] == "PASS", "G196 package verification failed")
    require(
        g196_package["grade"]
        == "EXTERNALLY_REVIEWED_VERIFIED_WITH_CAVEATS",
        "G196 package grade changed",
    )
    require(g196_package["no_write_replay"] is True, "G196 repaired no-write replay absent")
    require(g196_package["independent_histories"] == 204, "G196 history count changed")
    require(g196_package["independent_assertions"] == 5313, "G196 assertion count changed")
    require(g196_package["mutation_catches"] == 9, "G196 hostile count changed")
    g196_repair = json.loads((g196 / "REPAIR_VERIFICATION_RESULT.json").read_text())
    require(g196_repair["status"] == "PASS", "G196 repair verification failed")
    require(g196_repair["r1_independence_scope_corrected"] is True, "G196 R1 absent")
    require(g196_repair["r2_torch_import_read_only_replay"] is True, "G196 R2 absent")
    require(
        g196_repair["external_followup_landing"]
        == "G196_REPAIRS_ACCEPTED__BOUNDED_LANDING_RETAINED",
        "G196 repair follow-up acceptance absent",
    )
    require(
        g196_repair["repair_only_external_followup"] is True,
        "G196 repair follow-up gate absent",
    )
    require(
        g196_repair["ivp_evidence_type"]
        == "formula_level_regression_from_shared_candidate_matrices",
        "G196 IVP evidence scope changed",
    )
    require(
        by_id["G198"]["current_status"].startswith(
            "INDEPENDENTLY_VERIFIED_WITH_CAVEATS__PREREGISTERED__EXACT_FULL_METRIC_23_OF_23_PASS"
        ),
        "G198 bounded grade changed or promoted",
    )
    for guard in (
        "OPPOSITE_GERM_HAS_ZERO_M_DEPENDENT_SCREEN_CONNECTION_AND_TIDE",
        "COMMON_SCALE_TAU0_REMAINS",
        "DIRECT_COORDINATE_JACOBI_DMINUS_SQUARED_Y_EQUALS_ZERO",
        "PHYSICAL_VERTEX_MAP_A_U_TIMES_U_I_HAS_POSITIVE_NONVERTEX_DETERMINANT",
        "TWO_RAY_ALIAS_PROVES_NO_OFFRAY_RECONSTRUCTION",
        "INDEPENDENT_CETA_CZ_FAMILY_MAPPED_NOT_ACTIVE",
        "NO_P1_G116_G189_XMAX_TRANSFER_SOURCE_FIT_OR_PROTECTED_PAYLOAD",
    ):
        require(guard in by_id["G198"]["current_status"], f"G198 guard absent: {guard}")
    g198 = ROOT / "udt_g198_bidirectional_null_germ_map_2026-08-21"
    for name in (
        "AUDIT_REPORT.md",
        "EXACT_DERIVATION.md",
        "PRODUCTION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "PACKAGE_VERIFICATION_RESULT.json",
        "PREREGISTRATION.md",
        "FALSIFICATION_CONTRACT.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_MANIFEST.tsv",
    ):
        require((g198 / name).is_file(), f"G198 evidence missing: {name}")
    g198_package = json.loads((g198 / "PACKAGE_VERIFICATION_RESULT.json").read_text())
    require(g198_package["status"] == "PASS", "G198 package verification failed")
    require(
        g198_package["grade"] == "INDEPENDENTLY_VERIFIED_WITH_CAVEATS",
        "G198 package grade changed",
    )
    require(g198_package["production_assertions"] == 23, "G198 production count changed")
    require(g198_package["independent_histories"] == 68, "G198 history count changed")
    require(g198_package["independent_assertions"] == 1838, "G198 assertion count changed")
    require(g198_package["base_residual_evaluations"] == 816, "G198 base-residual count changed")
    require(g198_package["mutation_catches"] == 9, "G198 hostile count changed")
    require(
        by_id["G199"]["current_status"].startswith(
            "INDEPENDENTLY_VERIFIED_WITH_CAVEATS__PREREGISTERED_AT_1514ED99"
        ),
        "G199 bounded grade changed or promoted",
    )
    for guard in (
        "PRIMARY_STATIC_SPHERICAL_RECIPROCAL_AREAL_METRIC_ONLY",
        "BOTH_NORMALIZED_FUTURE_RADIAL_NULL_GERMS_AFFINE",
        "SAME_ENDPOINT_FREQUENCY_LAW",
        "ZERO_RADIAL_OPTICAL_TIDE_DESPITE_NONZERO_AMBIENT_CURVATURE",
        "BOTH_VERTEX_JACOBI_MAPS_EQUAL_LAMBDA_I",
        "NO_NATIVE_CHIRAL_RADIAL_SPLIT",
        "G198_ASYMMETRY_RETAINED_AS_CHOSEN_COMPLETE_COFRAME_CONTROL",
        "NO_CETA_CZ_EXTENSION_P1_G116_G189_XMAX_TRANSFER_SOURCE_FIT_OR_PROTECTED_PAYLOAD",
    ):
        require(guard in by_id["G199"]["current_status"], f"G199 guard absent: {guard}")
    require(
        by_id["G199"]["active_use"]
        == "ACTIVE_BOUNDED_TWO_RADIAL_NULL_GERMS_OF_THE_DECLARED_PRIMARY_STATIC_SPHERICAL_UDT_METRIC_ONLY",
        "G199 active scope widened",
    )
    require(
        by_id["G199"]["controlling_source"]
        == "udt_g199_primary_metric_bidirectional_radial_null_2026-08-21/AUDIT_REPORT.md",
        "G199 controlling source changed",
    )
    g199 = ROOT / "udt_g199_primary_metric_bidirectional_radial_null_2026-08-21"
    for name in (
        "AUDIT_REPORT.md",
        "EXACT_DERIVATION.md",
        "PRODUCTION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "PACKAGE_VERIFICATION_RESULT.json",
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_MANIFEST.tsv",
    ):
        require((g199 / name).is_file(), f"G199 evidence missing: {name}")
    g199_package = json.loads((g199 / "PACKAGE_VERIFICATION_RESULT.json").read_text())
    require(g199_package["all_pass"] is True, "G199 package verification failed")
    require(g199_package["no_write_replay"] is True, "G199 no-write replay absent")
    require(g199_package["production_assertions"] == 65, "G199 production count changed")
    require(g199_package["independent_assertions"] == 60000, "G199 assertion count changed")
    require(g199_package["independent_nonflat_cases"] == 2000, "G199 nonflat count changed")
    require(g199_package["mutation_catches"] == 9, "G199 hostile count changed")
    require(g199_package["source_hashes"] == 12, "G199 source count changed")
    require(
        by_id["G200"]["current_status"].startswith(
            "INDEPENDENTLY_VERIFIED_WITH_CAVEATS__PREREGISTERED_AT_7B92835E"
        ),
        "G200 bounded grade changed or promoted",
    )
    for guard in (
        "PRIMARY_STATIC_SPHERICAL_RECIPROCAL_AREAL_METRIC_ONLY",
        "BOTH_REVERSED_FUTURE_NONRADIAL_NULL_GERMS_AFFINE",
        "SAME_EVENT_FREQUENCY_LAW",
        "SAME_EVENT_TWO_MODE_TIDAL_MATRIX",
        "COMMON_VERTEX_CUBIC_DISTORTION",
        "FIRST_FINITE_DIFFERENCE_AT_QUARTIC_ORDER_EQUALS_RADIAL_TIDAL_GRADIENT_SAMPLING",
        "STRICT_RADIAL_FLAT_AND_TURNING_CONTROLS_VANISH",
        "NO_NATIVE_CHIRAL_NONRADIAL_SWITCH",
        "NO_CETA_CZ_EXTENSION_P1_G116_G189_XMAX_TRANSFER_SOURCE_FIT_OR_PROTECTED_PAYLOAD",
    ):
        require(guard in by_id["G200"]["current_status"], f"G200 guard absent: {guard}")
    require(
        by_id["G200"]["active_use"]
        == "ACTIVE_BOUNDED_TWO_REVERSED_EQUATORIAL_NONRADIAL_NULL_GERMS_OF_THE_DECLARED_PRIMARY_STATIC_SPHERICAL_UDT_METRIC_THROUGH_VERTEX_ORDER_FOUR_ONLY",
        "G200 active scope widened",
    )
    require(
        by_id["G200"]["controlling_source"]
        == "udt_g200_primary_metric_bidirectional_nonradial_null_2026-08-21/AUDIT_REPORT.md",
        "G200 controlling source changed",
    )
    g200 = ROOT / "udt_g200_primary_metric_bidirectional_nonradial_null_2026-08-21"
    for name in (
        "AUDIT_REPORT.md",
        "EXACT_DERIVATION.md",
        "PRODUCTION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "PACKAGE_VERIFICATION_RESULT.json",
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_MANIFEST.tsv",
    ):
        require((g200 / name).is_file(), f"G200 evidence missing: {name}")
    g200_package = json.loads((g200 / "PACKAGE_VERIFICATION_RESULT.json").read_text())
    require(g200_package["all_pass"] is True, "G200 package verification failed")
    require(g200_package["no_write_replay"] is True, "G200 no-write replay absent")
    require(g200_package["production_assertions"] == 64, "G200 production count changed")
    require(g200_package["independent_assertions"] == 38160, "G200 assertion count changed")
    require(g200_package["independent_cases"] == 2000, "G200 case count changed")
    require(
        g200_package["independent_nonzero_gradient_cases"] == 2000,
        "G200 nonzero-gradient count changed",
    )
    require(g200_package["flat_controls"] == 40, "G200 flat control count changed")
    require(g200_package["mutation_catches"] == 9, "G200 hostile count changed")
    require(g200_package["source_hashes"] == 9, "G200 source count changed")
    require(
        by_id["G201"]["current_status"].startswith(
            "INDEPENDENTLY_VERIFIED_WITH_CAVEATS__PREREGISTERED_AT_28D48506"
        ),
        "G201 bounded grade changed or promoted",
    )
    for guard in (
        "SIMULTANEOUS_DERIVATIVE_SUBSTITUTION_REPAIR_AFTER_FIRST_RUN_FAILED_CLOSED",
        "PRIMARY_STATIC_SPHERICAL_RECIPROCAL_AREAL_METRIC_ONLY",
        "PHI_ZERO_QUIET_IFF_P_AND_Q_ZERO",
        "ARBITRARY_PHI_ZERO_TIDE_JETS_EXIST",
        "EXACT_SMOOTH_F_EQUALS_1_PLUS_C_R2_ZERO_TIDE_FAMILY_REACHES_EITHER_SIGNED_PHI_EXTREME_ON_POSITIVE_DOMAINS",
        "RECIPROCAL_BLOCK_CONTRAST_IS_TWO_SIDED_ALGEBRAIC_DIAGNOSTIC_NOT_NEW_OBSERVABLE",
        "ANGULAR_VOLUME_IS_PHI_JET_DEPENDENT",
        "NO_LOCKSTEP_LOUDNESS_FORCED",
        "NO_PROFILE_FIT_XMAX_TRANSFER_CHIRAL_COFRAME_OR_PROTECTED_PAYLOAD",
    ):
        require(guard in by_id["G201"]["current_status"], f"G201 guard absent: {guard}")
    require(
        by_id["G201"]["active_use"]
        == "ACTIVE_BOUNDED_LOCAL_PRIMARY_METRIC_NONRADIAL_TWO_MODE_PHI_SECOND_JET_AMPLITUDE_AND_EXACT_ZERO_TIDE_FAMILY_CLASSIFICATION_ONLY",
        "G201 active scope widened",
    )
    require(
        by_id["G201"]["controlling_source"]
        == "udt_g201_primary_metric_phi_jet_regime_amplitude_2026-08-21/AUDIT_REPORT.md",
        "G201 controlling source changed",
    )
    g201 = ROOT / "udt_g201_primary_metric_phi_jet_regime_amplitude_2026-08-21"
    for name in (
        "AUDIT_REPORT.md",
        "EXACT_DERIVATION.md",
        "PRODUCTION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "PACKAGE_VERIFICATION_RESULT.json",
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_MANIFEST.tsv",
    ):
        require((g201 / name).is_file(), f"G201 evidence missing: {name}")
    g201_package = json.loads((g201 / "PACKAGE_VERIFICATION_RESULT.json").read_text())
    require(g201_package["all_pass"] is True, "G201 package verification failed")
    require(g201_package["no_write_replay"] is True, "G201 no-write replay absent")
    require(g201_package["production_assertions"] == 20, "G201 production count changed")
    require(g201_package["independent_assertions"] == 23606, "G201 assertion count changed")
    require(g201_package["independent_cases"] == 10000, "G201 case count changed")
    require(g201_package["cancellation_cases"] == 1000, "G201 cancellation count changed")
    require(g201_package["family_controls"] == 400, "G201 family count changed")
    require(g201_package["mutation_catches"] == 9, "G201 hostile count changed")
    require(g201_package["source_hashes"] == 9, "G201 source count changed")
    require(
        by_id["G202"]["current_status"].startswith(
            "INDEPENDENTLY_VERIFIED_WITH_CAVEATS__PREREGISTERED_AT_8503A413"
        ),
        "G202 bounded grade changed or promoted",
    )
    for guard in (
        "SYMBOLIC_NONNEGATIVE_LIMIT_REPLACED_BY_EXACT_LOWER_BOUND_FACTORIZATION_AFTER_FIRST_RUN_FAILED_CLOSED",
        "QUIET_ZERO_DEPTH_OVERLAP_IFF_PHI_P_AND_Q_ZERO",
        "NONTRIVIAL_ANALYTIC_SIGN_CROSSING_FIRST_ACTIVE_ORDER_ODD_AT_LEAST_THREE",
        "CUBIC_IS_MINIMAL_CHOSEN_CONTROL_NOT_SELECTED_HISTORY",
        "INFINITE_POSITIVE_ODD_PROFILE_FAMILY_HAS_QUIET_SECOND_JET_MONOTONE_TWO_SIDED_GROWTH",
        "FINITE_ANCHOR_JETS_DO_NOT_SELECT_UNRESTRICTED_SMOOTH_GLOBAL_PROFILE",
        "CE_AND_GOBS_ALONE_CANNOT_FORM_LENGTH",
        "MASS_PERMITS_GM_OVER_CE2_AND_DENSITY_PERMITS_CE_OVER_SQRT_G_RHO_AS_DIMENSIONAL_CANDIDATES_ONLY",
        "NO_FIT_XMAX_TRANSFER_PROFILE_SELECTION_OR_PROTECTED_PAYLOAD",
    ):
        require(guard in by_id["G202"]["current_status"], f"G202 guard absent: {guard}")
    require(
        by_id["G202"]["active_use"]
        == "ACTIVE_BOUNDED_PRIMARY_METRIC_LOG_RADIUS_QUIET_OVERLAP_ANALYTIC_CROSSING_FINITE_ANCHOR_AND_DIMENSIONAL_CANDIDATE_CLASSIFICATION_ONLY",
        "G202 active scope widened",
    )
    require(
        by_id["G202"]["controlling_source"]
        == "udt_g202_quiet_overlap_profile_anchor_classification_2026-08-21/AUDIT_REPORT.md",
        "G202 controlling source changed",
    )
    g202 = ROOT / "udt_g202_quiet_overlap_profile_anchor_classification_2026-08-21"
    for name in (
        "AUDIT_REPORT.md",
        "EXACT_DERIVATION.md",
        "PRODUCTION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "PACKAGE_VERIFICATION_RESULT.json",
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_MANIFEST.tsv",
    ):
        require((g202 / name).is_file(), f"G202 evidence missing: {name}")
    g202_package = json.loads((g202 / "PACKAGE_VERIFICATION_RESULT.json").read_text())
    require(g202_package["all_pass"] is True, "G202 package verification failed")
    require(g202_package["no_write_replay"] is True, "G202 no-write replay absent")
    require(g202_package["production_assertions"] == 32, "G202 production count changed")
    require(g202_package["independent_assertions"] == 170003, "G202 assertion count changed")
    require(g202_package["independent_cases"] == 20000, "G202 case count changed")
    require(g202_package["anchor_controls"] == 1000, "G202 anchor control count changed")
    require(g202_package["mutation_catches"] == 9, "G202 hostile count changed")
    require(g202_package["source_hashes"] == 9, "G202 source count changed")
    require(
        by_id["G203"]["current_status"].startswith(
            "INDEPENDENTLY_VERIFIED_WITH_CAVEATS__PREREGISTERED_AT_F1FA632A"
        ),
        "G203 bounded grade changed or promoted",
    )
    for guard in (
        "STRUCTURAL_EXPRESSION_ORDER_REPLACED_BY_EXACT_ALGEBRAIC_ZERO_AFTER_FIRST_RUN_FAILED_CLOSED",
        "VANISHING_ORDER_INVARIANT_UNDER_ANALYTIC_GERM_REPARAMETERIZATION",
        "POSITIVE_AREAL_RADIUS_RIGID",
        "QUIET_ORBIT_AREA_RECOVERS_R0",
        "LEADING_LOG_AREAL_STEEPNESS_DIMENSIONLESS_AFTER_DEPTH_AND_AREAL_CALIBRATION",
        "ORDER_LOCATION_AND_STEEPNESS_VALUES_UNSELECTED",
        "EXACT_ODD_N_GE3_R0_POSITIVE_A_POSITIVE_COUNTERFAMILY",
        "RECIPROCAL_REVERSAL_DOES_NOT_FORCE_GLOBAL_RADIAL_ODDNESS",
        "OBSERVATIONS_MAY_CALIBRATE_DECLARED_FINITE_FAMILY_NOT_UNRESTRICTED_HISTORY",
        "NO_FIT_XMAX_TRANSFER_PROFILE_SELECTION_OR_PROTECTED_PAYLOAD",
    ):
        require(guard in by_id["G203"]["current_status"], f"G203 guard absent: {guard}")
    require(
        by_id["G203"]["active_use"]
        == "ACTIVE_BOUNDED_PRIMARY_SPHERICAL_ANALYTIC_QUIET_CROSSING_ORDER_AREAL_LOCATION_AND_LOG_AREAL_STEEPNESS_OWNERSHIP_CLASSIFICATION_ONLY",
        "G203 active scope widened",
    )
    require(
        by_id["G203"]["controlling_source"]
        == "udt_g203_quiet_overlap_parameter_ownership_classification_2026-08-21/AUDIT_REPORT.md",
        "G203 controlling source changed",
    )
    g203 = ROOT / "udt_g203_quiet_overlap_parameter_ownership_classification_2026-08-21"
    for name in (
        "AUDIT_REPORT.md",
        "EXACT_DERIVATION.md",
        "PRODUCTION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "PACKAGE_VERIFICATION_RESULT.json",
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_MANIFEST.tsv",
    ):
        require((g203 / name).is_file(), f"G203 evidence missing: {name}")
    g203_package = json.loads((g203 / "PACKAGE_VERIFICATION_RESULT.json").read_text())
    require(g203_package["all_pass"] is True, "G203 package verification failed")
    require(g203_package["no_write_replay"] is True, "G203 no-write replay absent")
    require(g203_package["production_assertions"] == 70, "G203 production count changed")
    require(g203_package["independent_assertions"] == 280011, "G203 assertion count changed")
    require(g203_package["independent_cases"] == 20000, "G203 case count changed")
    require(g203_package["distinct_cases"] == 20000, "G203 distinct-case count changed")
    require(g203_package["mutation_catches"] == 10, "G203 hostile count changed")
    require(g203_package["source_hashes"] == 8, "G203 source count changed")
    require(
        by_id["G204"]["current_status"].startswith(
            "INDEPENDENTLY_VERIFIED_WITH_CAVEATS__PREREGISTERED_AT_EA91F45E"
        ),
        "G204 bounded grade changed or promoted",
    )
    for guard in (
        "POST_FAILURE_REPAIR_PREREGISTERED_AT_785B0447",
        "ORIGINAL_X2_XMINUS1N_CONTROL_CENTER_CURVATURE_BOUNDED_NOT_CARTESIAN_SMOOTH",
        "BOUNDED_CENTER_K_FORCES_PHI_O_R2",
        "LOG_MONOMIAL_CENTER_CURVATURE_SINGULAR_AT_FINITE_AFFINE_REACH",
        "EVEN_AREAL_REPAIR_ANALYTIC_IN_R2",
        "ONE_NEGATIVE_INNER_TROUGH_AT_R_OVER_R0_EQUALS_ONE_OVER_SQRT_NPLUS1",
        "QUIET_CROSSING_AND_LEADING_STEEPNESS_RETAINED",
        "OUTER_K_TENDS_ZERO_AT_INFINITE_SPATIAL_AND_NULL_AFFINE_REACH",
        "NOT_STANDARD_ASYMPTOTIC_FLATNESS_HORIZON_WALL_XMAX_OR_COMPLETION",
        "GLOBAL_REGULARITY_DOES_NOT_SELECT_N_R0_A_OR_PROFILE",
        "NO_FIT_TRANSFER_SOURCE_OR_PROTECTED_PAYLOAD",
    ):
        require(guard in by_id["G204"]["current_status"], f"G204 guard absent: {guard}")
    require(
        by_id["G204"]["active_use"]
        == "ACTIVE_BOUNDED_PRIMARY_STATIC_SPHERICAL_POSITIVE_AREAL_CENTER_CURVATURE_SMOOTHNESS_REGISTERED_PROFILE_AND_OUTER_ASYMPTOTIC_CLASSIFICATION_ONLY",
        "G204 active scope widened",
    )
    require(
        by_id["G204"]["controlling_source"]
        == "udt_g204_primary_metric_global_regularity_asymptotic_profile_2026-08-21/AUDIT_REPORT.md",
        "G204 controlling source changed",
    )
    g204 = ROOT / "udt_g204_primary_metric_global_regularity_asymptotic_profile_2026-08-21"
    for name in (
        "AUDIT_REPORT.md",
        "EXACT_DERIVATION.md",
        "PRODUCTION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "BOUNDARY_DIAGNOSTICS.json",
        "CATCH_PROOF_RESULT.json",
        "PACKAGE_VERIFICATION_RESULT.json",
        "PREREGISTRATION.md",
        "CORRECTION_PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_MANIFEST.tsv",
    ):
        require((g204 / name).is_file(), f"G204 evidence missing: {name}")
    g204_package = json.loads((g204 / "PACKAGE_VERIFICATION_RESULT.json").read_text())
    require(g204_package["all_pass"] is True, "G204 package verification failed")
    require(g204_package["no_write_replay"] is True, "G204 no-write replay absent")
    require(g204_package["repair_preregistered"] is True, "G204 repair preregistration absent")
    require(g204_package["production_assertions"] == 113, "G204 production count changed")
    require(g204_package["independent_assertions"] == 160010, "G204 assertion count changed")
    require(g204_package["independent_cases"] == 10000, "G204 case count changed")
    require(g204_package["distinct_cases"] == 10000, "G204 distinct-case count changed")
    require(g204_package["diagnostic_precision_digits"] == 80, "G204 diagnostic precision changed")
    require(g204_package["mutation_catches"] == 13, "G204 hostile count changed")
    require(g204_package["source_hashes"] == 7, "G204 source count changed")
    require(
        by_id["G205"]["current_status"].startswith(
            "EXTERNALLY_VERIFIED_WITH_CAVEATS__PREREGISTERED_AT_932155C1"
        ),
        "G205 bounded grade changed or promoted",
    )
    for guard in (
        "EVIDENCE_REPAIR_PREREGISTERED_AT_012FA064",
        "REPAIR_FOLLOWUP_GPT54_REPAIRS_VERIFIED_LANDING_RETAINED",
        "GENERAL_ANALYTIC_FULL_GEODESIC_COMPLETENESS_AND_GLOBAL_HYPERBOLICITY",
        "FINITE_SCRIPTS_VERIFY_ALGEBRAIC_CORE_ONLY",
        "EIGHTY_DIGIT_FINITE_DIAGNOSTICS_NOT_LIMIT_PROOF",
        "NO_FINITE_RADIUS_KILLING_HORIZON",
        "NULL_CIRCULAR_ORBITS_ZERO_ONE_TWO_ACROSS_EXACT_ACRIT_N",
        "SUPERCRITICAL_INNER_STABLE_OUTER_UNSTABLE",
        "NO_PARAMETER_PROFILE_PHYSICAL_HISTORY_MAXIMAL_EXTENSION_EVENT_HORIZON_XMAX",
    ):
        require(guard in by_id["G205"]["current_status"], f"G205 guard absent: {guard}")
    require(
        by_id["G205"]["active_use"]
        == "ACTIVE_BOUNDED_DECLARED_G204_STATIC_SPHERICAL_FAMILY_GEODESIC_OPTICAL_GLOBAL_HYPERBOLICITY_AND_NULL_TRAPPING_CLASSIFICATION_ONLY",
        "G205 active scope widened",
    )
    require(
        by_id["G205"]["controlling_source"]
        == "udt_g205_primary_metric_geodesic_causal_completion_2026-08-21/AUDIT_REPORT.md",
        "G205 controlling source changed",
    )
    g205 = ROOT / "udt_g205_primary_metric_geodesic_causal_completion_2026-08-21"
    for name in (
        "AUDIT_REPORT.md",
        "EXACT_DERIVATION.md",
        "PRODUCTION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "BOUNDARY_DIAGNOSTICS.json",
        "CATCH_PROOF_RESULT.json",
        "SOURCE_PROVENANCE_VERIFICATION.json",
        "PACKAGE_VERIFICATION_RESULT.json",
        "PREREGISTRATION.md",
        "REPAIR_PREREGISTRATION.md",
        "EXTERNAL_REVIEW_RAW.md",
        "EXTERNAL_REPAIR_FOLLOWUP.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_MANIFEST.tsv",
    ):
        require((g205 / name).is_file(), f"G205 evidence missing: {name}")
    g205_package = json.loads((g205 / "PACKAGE_VERIFICATION_RESULT.json").read_text())
    require(g205_package["all_pass"] is True, "G205 package verification failed")
    require(g205_package["no_write_replay"] is True, "G205 no-write replay absent")
    require(g205_package["production_assertions"] == 112, "G205 production count changed")
    require(g205_package["independent_assertions"] == 150000, "G205 assertion count changed")
    require(g205_package["independent_cases"] == 10000, "G205 case count changed")
    require(g205_package["distinct_cases"] == 10000, "G205 distinct-case count changed")
    require(g205_package["diagnostic_precision_digits"] == 80, "G205 diagnostic precision changed")
    require(g205_package["mutation_catches"] == 17, "G205 hostile count changed")
    require(g205_package["live_source_hashes_recorded"] == 7, "G205 source count changed")
    require(g205_package["registered_repairs"] == "VERIFIED", "G205 repairs not closed")
    require(
        g205_package["repair_only_followup"] == "REPAIRS_VERIFIED__LANDING_RETAINED",
        "G205 external repair follow-up absent",
    )
    require(
        by_id["G206"]["current_status"].startswith(
            "EXTERNALLY_VERIFIED_WITH_CAVEATS__PREREGISTERED_AT_62728402__"
            "FRESH_EXTERNAL_GPT54_VERIFIED_WITH_CAVEATS_NO_MATHEMATICAL_ERROR"
        ),
        "G206 bounded grade changed or promoted",
    )
    for guard in (
        "CAUSAL_CURVES_CAUCHY_SLICES_AND_GLOBAL_HYPERBOLICITY_PRESERVED",
        "NULL_AFFINE_WEIGHT_DLAMBDATILDE_EQUALS_EXP_2OMEGA_DLAMBDA",
        "NULL_COMPLETENESS_IFF_WEIGHTED_INTEGRAL_DIVERGES_AT_BOTH_ENDS",
        "BOUNDED_TIMELIVE_NONSHPERICAL_QUADRUPOLAR_WITNESS_NULL_COMPLETE",
        "SMOOTH_MINUS_R2_DECAYING_WITNESS_GLOBALLY_HYPERBOLIC_BUT_NULL_INCOMPLETE",
        "COMPLETED_PAIR_PHI_TILDE_EQUALS_PHI_MINUS_OMEGA_PULLBACK",
        "ANALYTIC_GLOBAL_THEOREMS_NOT_MECHANIZED",
        "NO_TIMELIKE_SPACELIKE_COMPLETENESS_TRACEFREE_SCREEN_MIXING_PHYSICAL_OMEGA_HISTORY_XMAX",
    ):
        require(guard in by_id["G206"]["current_status"], f"G206 guard absent: {guard}")
    require(by_id["G206"]["epistemic_label"] == "MIXED", "G206 label changed")
    require(
        by_id["G206"]["active_use"]
        == "ACTIVE_BOUNDED_COMMON_CONFORMAL_TIMELIVE_NONSHPERICAL_CAUSAL_NULL_AFFINE_AND_COMPLETED_PAIR_TRANSFORMATION_CLASSIFICATION_OVER_THE_SUPPLIED_G205_FAMILY_ONLY",
        "G206 active scope widened",
    )
    require(
        by_id["G206"]["controlling_source"]
        == "udt_g206_g205_conformal_timelive_nonspherical_robustness_2026-08-21/AUDIT_REPORT.md",
        "G206 controlling source changed",
    )
    g206 = ROOT / "udt_g206_g205_conformal_timelive_nonspherical_robustness_2026-08-21"
    for name in (
        "AUDIT_REPORT.md",
        "EXACT_DERIVATION.md",
        "PRODUCTION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "BOUNDARY_DIAGNOSTICS.json",
        "CATCH_PROOF_RESULT.json",
        "SOURCE_PROVENANCE_VERIFICATION.json",
        "PACKAGE_VERIFICATION_RESULT.json",
        "PREREGISTRATION.md",
        "EXTERNAL_REVIEW_RAW.md",
        "TRANSMISSION_RECORD.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_MANIFEST.tsv",
    ):
        require((g206 / name).is_file(), f"G206 evidence missing: {name}")
    g206_package = json.loads((g206 / "PACKAGE_VERIFICATION_RESULT.json").read_text())
    require(g206_package["all_pass"] is True, "G206 package verification failed")
    require(g206_package["no_write_replay"] is True, "G206 no-write replay absent")
    require(g206_package["production_assertions"] == 27, "G206 production count changed")
    require(g206_package["independent_assertions"] == 160006, "G206 assertion count changed")
    require(g206_package["independent_cases"] == 10000, "G206 case count changed")
    require(g206_package["distinct_cases"] == 10000, "G206 distinct-case count changed")
    require(g206_package["diagnostic_precision_digits"] == 160, "G206 diagnostic precision changed")
    require(g206_package["mutation_catches"] == 19, "G206 hostile count changed")
    require(g206_package["live_source_hashes_recorded"] == 7, "G206 source count changed")
    require(
        g206_package["external_adversarial_review"] == "VERIFIED_WITH_CAVEATS",
        "G206 external review absent",
    )
    require(
        by_id["G207"]["current_status"].startswith(
            "EXTERNALLY_VERIFIED_WITH_CAVEATS__PREREGISTERED_AT_F7F9D92D__"
            "FRESH_EXTERNAL_GPT54_VERIFIED_WITH_CAVEATS_NO_MATHEMATICAL_ERROR_OR_HIDDEN_MATERIAL_OVERCLAIM"
        ),
        "G207 bounded grade changed or promoted",
    )
    for guard in (
        "LORENTZ_SIGNATURE_AMBIENT_DETERMINANT_AND_RADIAL_CAUSAL_BOUND_PRESERVED",
        "ALL_SMOOTH_DECLARED_S_PRESERVE_G205_CAUCHY_SLICES_AND_GLOBAL_HYPERBOLICITY",
        "ALL_SMOOTH_STATIC_MEMBERS_NULL_COMPLETE",
        "COMPACT_TIME_LIVE_CENTER_REGULAR_NONSPHERICAL_WITNESS_NULL_COMPLETE",
        "SMOOTH_UNBOUNDED_TIME_LIVE_SUPERCRITICAL_CIRCULAR_ORBIT_WITNESS_GLOBALLY_HYPERBOLIC_BUT_NULL_INCOMPLETE",
        "STATIC_CLOCK_STRATUM_BLIND",
        "GENERIC_SCREEN_BEARING_CLOCK_PAIR_AREA_AND_SHIFT_RESPOND",
        "ANALYTIC_GLOBAL_THEOREMS_NOT_MECHANIZED",
        "NO_TIMELIKE_SPACELIKE_COMPLETENESS_COMBINED_COMMON_SCALE_RADIAL_SCREEN_MIXING_SHIFT_PHYSICAL_S_HISTORY_XMAX",
    ):
        require(guard in by_id["G207"]["current_status"], f"G207 guard absent: {guard}")
    require(by_id["G207"]["epistemic_label"] == "MIXED", "G207 label changed")
    require(
        by_id["G207"]["active_use"]
        == "ACTIVE_BOUNDED_PURE_TRACEFREE_ANGULAR_SCREEN_TIMELIVE_CAUSAL_NULL_AFFINE_AND_COMPLETED_PAIR_CLASSIFICATION_OVER_THE_SUPPLIED_G205_FAMILY_ONLY",
        "G207 active scope widened",
    )
    require(
        by_id["G207"]["controlling_source"]
        == "udt_g207_g205_tracefree_screen_timelive_robustness_2026-08-21/AUDIT_REPORT.md",
        "G207 controlling source changed",
    )
    g207 = ROOT / "udt_g207_g205_tracefree_screen_timelive_robustness_2026-08-21"
    for name in (
        "AUDIT_REPORT.md",
        "EXACT_DERIVATION.md",
        "PRODUCTION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "BOUNDARY_DIAGNOSTICS.json",
        "CATCH_PROOF_RESULT.json",
        "SOURCE_PROVENANCE_VERIFICATION.json",
        "PACKAGE_VERIFICATION_RESULT.json",
        "PREREGISTRATION.md",
        "EXTERNAL_REVIEW_RAW.md",
        "TRANSMISSION_RECORD.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_MANIFEST.tsv",
    ):
        require((g207 / name).is_file(), f"G207 evidence missing: {name}")
    g207_package = json.loads((g207 / "PACKAGE_VERIFICATION_RESULT.json").read_text())
    require(g207_package["all_pass"] is True, "G207 package verification failed")
    require(g207_package["no_write_replay"] is True, "G207 no-write replay absent")
    require(g207_package["production_assertions"] == 36, "G207 production count changed")
    require(g207_package["independent_assertions"] == 110009, "G207 assertion count changed")
    require(g207_package["independent_cases"] == 10000, "G207 case count changed")
    require(g207_package["distinct_cases"] == 10000, "G207 distinct-case count changed")
    require(g207_package["diagnostic_precision_digits"] == 100, "G207 diagnostic precision changed")
    require(g207_package["mutation_catches"] == 24, "G207 hostile count changed")
    require(g207_package["live_source_hashes_recorded"] == 7, "G207 source count changed")
    require(
        g207_package["external_adversarial_review"] == "VERIFIED_WITH_CAVEATS",
        "G207 external review absent",
    )
    require(
        by_id["G208"]["current_status"].startswith(
            "EXTERNALLY_VERIFIED_WITH_CAVEATS__PREREGISTERED_AT_FB1AF9DF__"
            "FRESH_EXTERNAL_GPT54_VERIFIED_WITH_CAVEATS_NO_MATHEMATICAL_REFUTATION"
        ),
        "G208 bounded grade changed or promoted",
    )
    for guard in (
        "COMMON_CONFORMAL_SCALE_COMPOSES_EXACTLY_WITH_ANY_SUPPLIED_SHAPE_METRIC",
        "PURE_H0_SELFADJOINT_RADIAL_SCREEN_C_CHOSE_EXTENSION_CLASS",
        "LORENTZ_SIGNATURE_AND_AMBIENT_DETERMINANT_PRESERVED",
        "SHARP_RADIAL_CAUSAL_BOUND_ABS_DRDT_LE_F_SQRT_COSH_2S",
        "GROWTH_CONTROLLED_SLAB_CLASS_GLOBALLY_HYPERBOLIC",
        "ALL_GLOBALLY_BOUNDED_SMOOTH_STATIC_MIXERS_NULL_COMPLETE",
        "COMPACT_TIME_LIVE_UNIFORMLY_CONTROLLED_CLASS_NULL_COMPLETE",
        "SMOOTH_CENTER_REGULAR_UNBOUNDED_STATIC_MIXER_FAILURE_CLASS_NOT_GLOBALLY_HYPERBOLIC_AND_NOT_NULL_COMPLETE",
        "COMPLETED_PAIR_PULLBACK_HEARS_RADIAL_AND_GENERIC_MIXING_BEFORE_READOUT",
        "STATIC_CLOCK_AND_UNTOUCHED_SCREEN_KERNEL_BLIND_STRATA",
        "ANALYTIC_GLOBAL_THEOREMS_EXTERNALLY_REVIEWED_NOT_MECHANIZED",
        "NO_TIMELIKE_SPACELIKE_COMPLETENESS_TRACECHANGE_SHIFT_ARBITRARY_FULL_SPATIAL_MAP_PHYSICAL_C_HISTORY_XMAX",
    ):
        require(guard in by_id["G208"]["current_status"], f"G208 guard absent: {guard}")
    require(by_id["G208"]["epistemic_label"] == "MIXED", "G208 label changed")
    require(
        by_id["G208"]["active_use"]
        == "ACTIVE_BOUNDED_PURE_RADIAL_SCREEN_MIXING_CAUSAL_NULL_AFFINE_FAILURE_AND_COMPLETED_PAIR_CLASSIFICATION_OVER_THE_SUPPLIED_G205_FAMILY_ONLY",
        "G208 active scope widened",
    )
    require(
        by_id["G208"]["controlling_source"]
        == "udt_g208_g205_radial_screen_mixing_robustness_2026-08-21/AUDIT_REPORT.md",
        "G208 controlling source changed",
    )
    g208 = ROOT / "udt_g208_g205_radial_screen_mixing_robustness_2026-08-21"
    for name in (
        "AUDIT_REPORT.md",
        "EXACT_DERIVATION.md",
        "PRODUCTION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "BOUNDARY_DIAGNOSTICS.json",
        "CATCH_PROOF_RESULT.json",
        "SOURCE_PROVENANCE_VERIFICATION.json",
        "PACKAGE_VERIFICATION_RESULT.json",
        "PREREGISTRATION.md",
        "PREREGISTRATION_EXECUTION_NOTE.md",
        "EXTERNAL_REVIEW_RAW.md",
        "TRANSMISSION_RECORD.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_MANIFEST.tsv",
    ):
        require((g208 / name).is_file(), f"G208 evidence missing: {name}")
    g208_package = json.loads((g208 / "PACKAGE_VERIFICATION_RESULT.json").read_text())
    require(g208_package["status"] == "PASS", "G208 package verification failed")
    require(g208_package["no_write_replay"] is True, "G208 no-write replay absent")
    require(g208_package["production_assertions"] == 20, "G208 production count changed")
    require(g208_package["independent_assertions"] == 120004, "G208 assertion count changed")
    require(g208_package["independent_cases"] == 10000, "G208 case count changed")
    require(g208_package["diagnostic_precision_digits"] == 240, "G208 diagnostic precision changed")
    require(g208_package["mutation_catches"] == 23, "G208 hostile count changed")
    require(g208_package["live_source_hashes_recorded"] == 9, "G208 source count changed")
    require(
        g208_package["live_source_hash_check"] == "SEPARATE_REPOSITORY_CONTEXT_GATE",
        "G208 provenance/replay separation absent",
    )
    require(
        g208_package["global_theorem_evidence"]
        == "ANALYTIC_EXTERNALLY_REVIEWED_NOT_MECHANIZED",
        "G208 analytic evidence ceiling absent",
    )
    require(
        g208_package["external_adversarial_review"] == "VERIFIED_WITH_CAVEATS",
        "G208 external review absent",
    )
    require(
        by_id["G209"]["current_status"].startswith(
            "EXTERNALLY_VERIFIED_WITH_CAVEATS__PREREGISTERED_AT_B5C40CC2__"
            "FRESH_EXTERNAL_GPT54_VERIFIED_WITH_CAVEATS_NO_MATHEMATICAL_REFUTATION__"
            "REPAIR_FOLLOWUP_GPT54_ACCEPTED_SCIENTIFIC_LANDING_UNCHANGED"
        ),
        "G209 bounded grade changed or promoted",
    )
    for guard in (
        "FULL_THREE_COMPONENT_TIMESPACE_SHIFT_FOR_ARBITRARY_POSITIVE_SUPPLIED_HA",
        "EXACT_ADM_CONGRUENCE",
        "LORENTZ_SIGNATURE_AMBIENT_DETERMINANT_AND_TEMPORAL_DT_PRESERVED",
        "CAUSAL_VELOCITY_ELLIPSOID_TRANSLATED_BY_MINUS_B_WITH_HA_CONTROLLED_SHAPE",
        "GROWTH_CONTROLLED_CLASS_GLOBALLY_HYPERBOLIC",
        "UNIFORMLY_METRIC_SUBLUMINAL_SMOOTH_STATIC_CLASS_NULL_COMPLETE",
        "CONTROLLED_COMPACT_TIME_LIVE_CLASS_NULL_COMPLETE",
        "SMOOTH_CENTER_REGULAR_BOUNDED_COORDINATE_SHIFT_WITNESS_GLOBALLY_HYPERBOLIC_BUT_NONRADIAL_NULL_INCOMPLETE",
        "COMPLETED_PAIR_PULLBACK_HEARS_SHIFT_BEFORE_READOUT",
        "EULERIAN_NORMAL_GERM_BLIND_STRATUM",
        "ANALYTIC_GLOBAL_THEOREMS_EXTERNALLY_REVIEWED_NOT_MECHANIZED",
        "NO_TIMELIKE_SPACELIKE_COMPLETENESS_ARBITRARY_LIVE_SHIFT_TRACECHANGING_PHYSICAL_B_HISTORY_XMAX",
    ):
        require(guard in by_id["G209"]["current_status"], f"G209 guard absent: {guard}")
    require(by_id["G209"]["epistemic_label"] == "MIXED", "G209 label changed")
    require(
        by_id["G209"]["active_use"]
        == "ACTIVE_BOUNDED_FULL_LOCAL_TIMESPACE_SHIFT_AND_DECLARED_G205_GLOBAL_SUBCLASS_CLASSIFICATION_ONLY",
        "G209 active scope widened",
    )
    require(
        by_id["G209"]["controlling_source"]
        == "udt_g209_g205_timespace_shift_robustness_2026-08-21/AUDIT_REPORT.md",
        "G209 controlling source changed",
    )
    g209 = ROOT / "udt_g209_g205_timespace_shift_robustness_2026-08-21"
    for name in (
        "AUDIT_REPORT.md",
        "EXACT_DERIVATION.md",
        "PRODUCTION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "BOUNDARY_DIAGNOSTICS.json",
        "CATCH_PROOF_RESULT.json",
        "SOURCE_PROVENANCE_VERIFICATION.json",
        "PACKAGE_VERIFICATION_RESULT.json",
        "PREREGISTRATION.md",
        "PREREGISTRATION_EXECUTION_NOTE.md",
        "EXTERNAL_REVIEW_RAW.md",
        "EXTERNAL_REPAIR_FOLLOWUP_RAW.md",
        "REVIEW_REPAIR_PREREGISTRATION.md",
        "TRANSMISSION_RECORD.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_MANIFEST.tsv",
    ):
        require((g209 / name).is_file(), f"G209 evidence missing: {name}")
    g209_package = json.loads((g209 / "PACKAGE_VERIFICATION_RESULT.json").read_text())
    require(g209_package["status"] == "PASS", "G209 package verification failed")
    require(g209_package["core_no_write_replay"] is True, "G209 no-write replay absent")
    require(g209_package["production_assertions"] == 21, "G209 production count changed")
    require(g209_package["independent_assertions"] == 100001, "G209 assertion count changed")
    require(g209_package["independent_cases"] == 10000, "G209 case count changed")
    require(g209_package["diagnostic_precision_digits"] == 120, "G209 diagnostic precision changed")
    require(g209_package["mutation_catches"] == 25, "G209 hostile count changed")
    require(g209_package["provenance_manifest_rows"] == 8, "G209 source count changed")
    require(
        g209_package["first_external_review"] == "VERIFIED_WITH_CAVEATS",
        "G209 first external review absent",
    )
    require(
        g209_package["repair_followup"]
        == "G209_REPAIR_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED",
        "G209 repair follow-up absent",
    )
    require(g209_package["scientific_landing_changed"] is False, "G209 landing changed")
    require(
        by_id["G210"]["current_status"].startswith(
            "EXTERNALLY_VERIFIED_WITH_CAVEATS__PREREGISTERED_AT_D1458D37__"
            "FRESH_EXTERNAL_GPT54_VERIFIED_WITH_CAVEATS_NO_MATHEMATICAL_REFUTATION_NO_REPAIRS_REQUIRED"
        ),
        "G210 bounded grade changed or promoted",
    )
    for guard in (
        "UNIQUE_RELATIVE_SPATIAL_DETERMINANT_SCALAR_SIGMA_EQUALS_ONE_SIXTH_LOG_DETK_OVER_DETH_AFTER_POSITIVE_REFERENCE_H_SUPPLIED",
        "DETERMINANT_ONE_REMAINDER_UNIQUE_BUT_NOT_FULLY_CLASSIFIED_BY_G207_G208",
        "ARBITRARY_POSITIVE_HA_AND_SUPPLIED_FULL_SHIFT",
        "LORENTZ_SIGNATURE_AND_TEMPORAL_DT_PRESERVED",
        "AMBIENT_DETERMINANT_SCALES_EXP_6SIGMA",
        "CAUSAL_CENTER_REMAINS_MINUS_B_AND_ALL_WIDTHS_SCALE_EXP_MINUS_SIGMA",
        "GROWTH_CONTROLLED_CLASS_GLOBALLY_HYPERBOLIC",
        "ALL_SMOOTH_STATIC_GLOBALLY_LOWER_BOUNDED_SIGMA_NULL_COMPLETE",
        "DECLARED_LOWER_BOUNDED_BOUNDED_DERIVATIVE_COMPACT_TIME_LIVE_CLASS_NULL_COMPLETE",
        "SIGMA_EQUALS_MINUS_PHI_SMOOTH_GLOBALLY_HYPERBOLIC_BUT_RADIAL_NULL_INCOMPLETE",
        "COMPLETED_PAIR_PULLBACK_HEARS_SPATIAL_VOLUME_BEFORE_READOUT_ON_SPATIALLY_BEARING_CLOCKS",
        "UNSHIFTED_STATIC_AND_EULERIAN_NORMAL_CLOCK_BLIND_STRATA",
        "SPATIAL_SCALE_EQUALS_COMMON_CONFORMAL_SCALE_PLUS_COMPENSATING_LAPSE_DEPENDENCY_IDENTITY",
        "ANALYTIC_GLOBAL_THEOREMS_EXTERNALLY_REVIEWED_NOT_MECHANIZED_END_TO_END",
        "NO_TIMELIKE_SPACELIKE_COMPLETENESS_ARBITRARY_DETERMINANT_ONE_OR_LIVE_HISTORY_PHYSICAL_SIGMA_LAPSE_PROFILE_XMAX_TRANSFER_SOURCE_FIT_OR_PROTECTED_PAYLOAD",
    ):
        require(guard in by_id["G210"]["current_status"], f"G210 guard absent: {guard}")
    require(by_id["G210"]["epistemic_label"] == "MIXED", "G210 label changed")
    require(
        by_id["G210"]["active_use"]
        == "ACTIVE_BOUNDED_FULL_LOCAL_SPATIAL_VOLUME_SCALAR_AND_DECLARED_G205_GLOBAL_SUBCLASS_CLASSIFICATION_ONLY",
        "G210 active scope widened",
    )
    require(
        by_id["G210"]["controlling_source"]
        == "udt_g210_g205_spatial_volume_robustness_2026-08-21/AUDIT_REPORT.md",
        "G210 controlling source changed",
    )
    g210 = ROOT / "udt_g210_g205_spatial_volume_robustness_2026-08-21"
    for name in (
        "AUDIT_REPORT.md",
        "EXACT_DERIVATION.md",
        "PRODUCTION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "BOUNDARY_DIAGNOSTICS.json",
        "CATCH_PROOF_RESULT.json",
        "SOURCE_PROVENANCE_VERIFICATION.json",
        "PACKAGE_VERIFICATION_RESULT.json",
        "PREREGISTRATION.md",
        "PREREGISTRATION_EXECUTION_NOTE.md",
        "EXTERNAL_REVIEW_RAW.md",
        "TRANSMISSION_RECORD.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_MANIFEST.tsv",
    ):
        require((g210 / name).is_file(), f"G210 evidence missing: {name}")
    g210_package = json.loads((g210 / "PACKAGE_VERIFICATION_RESULT.json").read_text())
    require(g210_package["status"] == "PASS", "G210 package verification failed")
    require(g210_package["core_no_write_replay"] is True, "G210 no-write replay absent")
    require(g210_package["production_assertions"] == 24, "G210 production count changed")
    require(g210_package["independent_assertions"] == 250001, "G210 assertion count changed")
    require(g210_package["independent_cases"] == 10000, "G210 case count changed")
    require(g210_package["diagnostic_precision_digits"] == 120, "G210 diagnostic precision changed")
    require(g210_package["mutation_catches"] == 25, "G210 hostile count changed")
    require(g210_package["provenance_manifest_rows"] == 9, "G210 source count changed")
    require(
        g210_package["external_review"] == "VERIFIED_WITH_CAVEATS",
        "G210 external review absent",
    )
    require(g210_package["required_repairs"] == 0, "G210 unexpected repair count")
    require(g210_package["scientific_landing_changed"] is False, "G210 landing changed")
    require(
        by_id["G211"]["current_status"].startswith(
            "EXTERNALLY_VERIFIED_WITH_CAVEATS__PREREGISTERED_AT_7220E71F__"
            "FRESH_EXTERNAL_GPT54_VERIFIED_WITH_CAVEATS_NO_REFUTING_DEFECT_NO_REPAIRS_REQUIRED"
        ),
        "G211 bounded grade changed or promoted",
    )
    for guard in (
        "SUPPLIED_CALIBRATED_1PLUS3_SPLIT_POSITIVE_REFERENCE_LAPSE_AND_POSITIVE_SPATIAL_REFERENCE",
        "COMPLETE_LOCAL_DIAGONAL_SCALAR_SECTOR_RANK_TWO",
        "OMEGA_EQUALS_ELL_AND_Q_EQUALS_SIGMA_MINUS_ELL_EXACT_BASIS",
        "LAPSE_ONLY_OMEGA_EQUALS_ELL_Q_EQUALS_MINUS_ELL_NOT_THIRD_TILE",
        "V_EQUALS_ELL_PLUS_3SIGMA_AND_W_EQUALS_ELL_MINUS_SIGMA_EXACT_VOLUME_CONE_BASIS",
        "CAUSAL_CENTER_MINUS_B_WIDTHS_EXP_MINUS_Q_COMMON_SCALE_CANCELS_CONES",
        "CAUCHY_TRANSFER_CONDITIONAL_ON_SUPPLIED_GQ_ONLY",
        "NULL_AFFINE_DLAMBDAG_EQUALS_EXP_2OMEGA_DLAMBDAQ",
        "STATIC_RADIAL_AFFINE_DENSITY_EXP_2OMEGA_PLUS_Q_OVER_E",
        "COMPENSATED_CONTROL_RADIAL_RESTORATION_ONLY_NOT_FULL_NULL_COMPLETENESS",
        "GENERIC_SPATIAL_CLOCKS_HEAR_BOTH_MODES",
        "EULERIAN_NORMAL_AND_UNSHIFTED_STATIC_Q_BLIND_NOT_OMEGA_BLIND",
        "ANALYTIC_GLOBAL_CAUSAL_AND_ALL_NULL_THEOREMS_NOT_MECHANIZED_END_TO_END",
        "NO_FOLIATION_SPLIT_SCALAR_FUNCTION_DETERMINANT_ONE_HISTORY_GLOBAL_REALIZATION_XMAX_TRANSFER_SOURCE_FIT_OR_PROTECTED_PAYLOAD",
    ):
        require(guard in by_id["G211"]["current_status"], f"G211 guard absent: {guard}")
    require(by_id["G211"]["epistemic_label"] == "MIXED", "G211 label changed")
    require(
        by_id["G211"]["active_use"]
        == "ACTIVE_BOUNDED_COMPLETE_LOCAL_DIAGONAL_SCALAR_BASIS_AND_DECLARED_G205_RADIAL_CONTROLS_ONLY",
        "G211 active scope widened",
    )
    require(
        by_id["G211"]["controlling_source"]
        == "udt_g211_complete_diagonal_scalar_basis_closure_2026-08-22/AUDIT_REPORT.md",
        "G211 controlling source changed",
    )
    g211 = ROOT / "udt_g211_complete_diagonal_scalar_basis_closure_2026-08-22"
    for name in (
        "AUDIT_REPORT.md",
        "EXACT_DERIVATION.md",
        "PRODUCTION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "RADIAL_CONTROLS.json",
        "CATCH_PROOF_RESULT.json",
        "SOURCE_PROVENANCE_VERIFICATION.json",
        "CORE_VERIFICATION_RESULT.json",
        "PACKAGE_VERIFICATION_RESULT.json",
        "PREREGISTRATION.md",
        "PREREGISTRATION_EXECUTION_NOTE.md",
        "EXTERNAL_REVIEW_RAW.md",
        "TRANSMISSION_RECORD.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_MANIFEST.tsv",
    ):
        require((g211 / name).is_file(), f"G211 evidence missing: {name}")
    g211_package = json.loads((g211 / "PACKAGE_VERIFICATION_RESULT.json").read_text())
    require(g211_package["status"] == "PASS", "G211 package verification failed")
    require(g211_package["core_no_write_replay"] is True, "G211 no-write replay absent")
    require(g211_package["production_assertions"] == 29, "G211 production count changed")
    require(g211_package["independent_assertions"] == 280003, "G211 assertion count changed")
    require(g211_package["independent_cases"] == 10000, "G211 case count changed")
    require(g211_package["radial_precision_digits"] == 120, "G211 radial precision changed")
    require(g211_package["radial_profiles"] == 4, "G211 radial profile count changed")
    require(g211_package["mutation_catches"] == 31, "G211 hostile count changed")
    require(g211_package["provenance_manifest_rows"] == 8, "G211 source count changed")
    require(
        g211_package["external_review"] == "VERIFIED_WITH_CAVEATS",
        "G211 external review absent",
    )
    require(g211_package["required_repairs"] == 0, "G211 unexpected repair count")
    require(g211_package["scientific_landing_changed"] is False, "G211 landing changed")
    require(
        by_id["G212"]["current_status"].startswith(
            "MULTIAGENT_VERIFIED_WITH_CAVEATS__PREREGISTERED_AT_8C7A0B5C__"
            "THREE_INDEPENDENT_WHITEBOARD_ROLES"
        ),
        "G212 bounded grade changed or promoted",
    )
    for guard in (
        "RANK_COMPLETE_VALUED_FULL_PAIR_NETWORK_EQUIVALENT_TO_METRIC_STATE_IN_G129_G130_SCOPE",
        "NO_SECOND_HISTORY_SELECTOR_AFTER_FAITHFUL_RECONSTRUCTION",
        "CURRENT_RECIPROCITY_COMPATIBILITY_CAUSAL_AND_SMOOTH_DESCENT_IDENTITIES_DO_NOT_GENERATE_NETWORK_VALUES_FROM_FINITE_ANCHORS",
        "TWO_GENERIC_COMPLETED_CLOCKS_RECONSTRUCT_OMEGA_AND_Q_POINTWISE_WHEN_TOMOGRAPHY_DETERMINANT_NONZERO_AND_SOLUTIONS_POSITIVE",
        "STATIC_EULERIAN_CLOCKS_RANK_DEFICIENT",
        "MATCHED_PAIR_COCYCLE_GIVES_ENDPOINT_POTENTIAL_WITH_ARBITRARY_PROFILE",
        "G171_GENERIC_PAIR_GERMS_DO_NOT_HAVE_UNIVERSAL_TRIANGLE_ADDITIVITY",
        "ARBITRARY_SMOOTH_OMEGA_Q_COUNTERFAMILY_PRESERVES_COMPLETED_RECIPROCITY_AND_COMPATIBILITY",
        "FULL_ALL_GERM_TWO_JET_ISOTROPY_FORCES_CONSTANT_CURVATURE_ONLY_CONDITIONALLY",
        "ALL_GERM_ISOTROPY_NOT_UDT_OWNED_AND_WOULD_BE_ADDED_SCAFFOLDING",
        "NO_PHYSICAL_POPULATION_GLOBAL_COMPLETED_NETWORK_FINITE_DIMENSIONAL_HISTORY_FLOW_XMAX_TRANSFER_SOURCE_ACTION_MATTER_OR_OBSERVATION",
    ):
        require(guard in by_id["G212"]["current_status"], f"G212 guard absent: {guard}")
    require(by_id["G212"]["epistemic_label"] == "MIXED", "G212 label changed")
    require(
        by_id["G212"]["active_use"]
        == "ACTIVE_BOUNDED_RELATIONAL_STATE_RECONCILIATION_LOCAL_TWO_MODE_TOMOGRAPHY_AND_CONDITIONAL_SPACE_FORM_CONTROL_ONLY",
        "G212 active scope widened",
    )
    require(
        by_id["G212"]["controlling_source"]
        == "udt_g212_observer_equivalence_history_bridge_whiteboard_2026-08-22/AUDIT_REPORT.md",
        "G212 controlling source changed",
    )
    g212 = ROOT / "udt_g212_observer_equivalence_history_bridge_whiteboard_2026-08-22"
    for name in (
        "AUDIT_REPORT.md",
        "EXACT_DERIVATION.md",
        "WHITEBOARD_SYNTHESIS.md",
        "LAY_REPORT.md",
        "VERIFICATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "PACKAGE_VERIFICATION_RESULT.json",
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_MANIFEST.tsv",
        "STATUS_LEDGER.tsv",
    ):
        require((g212 / name).is_file(), f"G212 evidence missing: {name}")
    g212_package = json.loads((g212 / "PACKAGE_VERIFICATION_RESULT.json").read_text())
    require(g212_package["status"] == "PASS", "G212 package verification failed")
    require(g212_package["core_no_write_replay"] is True, "G212 no-write replay absent")
    require(g212_package["symbolic_checks"] == 29, "G212 symbolic count changed")
    require(g212_package["independent_trials"] == 10000, "G212 trial count changed")
    require(g212_package["independent_assertions"] == 290000, "G212 assertion count changed")
    require(g212_package["source_manifest_rows"] == 6, "G212 source count changed")
    require(g212_package["whiteboard_roles"] == 3, "G212 whiteboard role count changed")
    require(g212_package["required_repairs"] == 0, "G212 unexpected repair count")
    require(
        by_id["G213"]["current_status"].startswith(
            "INDEPENDENTLY_VERIFIED_WITH_CAVEATS__PREREGISTERED_AT_C96A273F__"
            "EXTERNAL_REVIEW_REPAIRS_ACCEPTED__BOUNDED_LANDING_UNCHANGED__NO_BOUNDED_SCIENTIFIC_DEFECT"
        ),
        "G213 bounded grade changed or promoted",
    )
    for guard in (
        "SUPPLIED_CALIBRATED_1PLUS3_AND_RADIAL_SCREEN_SPLITS",
        "EXACT_ONE_PLUS_TWO_PLUS_TWO_DECOMPOSITION_INTO_RADIAL_SCREEN_GRADING_RADIAL_SCREEN_MIXING_AND_TRACEFREE_SCREEN_SHAPE",
        "TOTAL_FIVE_MODES",
        "G207_COVERS_TWO_SCREEN_SHAPE_LOGARITHMIC_COORDINATES",
        "G208_COVERS_TWO_RADIAL_SCREEN_MIXING_LOGARITHMIC_COORDINATES",
        "MISSING_INDEPENDENT_COORDINATE_IS_RADIAL_VERSUS_SCREEN_GRADING_DISTINCT_FROM_G211_Q",
        "NO_MODE_AMPLITUDE_OR_HISTORY_SELECTED",
        "COMPLETED_TUPLE_AND_FULL_AUXILIARY_PULLBACK_EXACTLY_BIJECTIVE_ON_REGULAR_POSITIVE_DENSITY_STRATUM",
        "G129_SIX_KNOWN_PAIR_DESIGN_RETAINS_EXACT_RANK_TEN",
        "NORMALIZED_COMPLETED_METRICS_WITHOUT_DENSITIES_NOT_FAITHFUL",
        "POSITIVE_COMMON_SPATIAL_RESCALING_IS_EXACT_BLIND_COUNTERFAMILY",
        "NO_PHYSICAL_PAIR_POPULATION_GLOBAL_DESCENT_NETWORK_VALUE_GENERATION_FINITE_ANCHOR_FLOW_XMAX_TRANSFER_SOURCE_ACTION_MATTER_MASS_OR_OBSERVATION",
    ):
        require(guard in by_id["G213"]["current_status"], f"G213 guard absent: {guard}")
    require(by_id["G213"]["epistemic_label"] == "MIXED", "G213 label changed")
    require(
        by_id["G213"]["active_use"]
        == "ACTIVE_BOUNDED_LOCAL_DETERMINANT_ONE_SPATIAL_MODE_CENSUS_AND_COMPLETED_PAIR_INFORMATION_RANK_CLOSURE_ONLY",
        "G213 active scope widened",
    )
    require(
        by_id["G213"]["controlling_source"]
        == "udt_g213_determinant_one_spatial_remainder_and_completed_rank_closure_2026-08-22/AUDIT_REPORT.md",
        "G213 controlling source changed",
    )
    g213 = ROOT / "udt_g213_determinant_one_spatial_remainder_and_completed_rank_closure_2026-08-22"
    for name in (
        "AUDIT_REPORT.md",
        "EXACT_DERIVATION.md",
        "LAY_REPORT.md",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "VERIFICATION_RESULT.json",
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_MANIFEST.tsv",
        "STATUS_LEDGER.tsv",
        "EXTERNAL_REPAIR_FOLLOWUP_RAW.md",
        "EXTERNAL_REPAIR_FOLLOWUP_ADJUDICATION.md",
    ):
        require((g213 / name).is_file(), f"G213 evidence missing: {name}")
    g213_package = json.loads((g213 / "VERIFICATION_RESULT.json").read_text())
    require(
        "G213_REPAIR_ONLY_ACCEPTED__REGISTERED_REPAIRS_VERIFIED__BOUNDED_LANDING_UNCHANGED"
        in (g213 / "EXTERNAL_REPAIR_FOLLOWUP_RAW.md").read_text(),
        "G213 repair follow-up acceptance absent",
    )
    require(g213_package["status"] == "PASS", "G213 package verification failed")
    require(g213_package["no_write_replay"] is True, "G213 no-write replay absent")
    require(g213_package["core_files_hashed"] == 25, "G213 core file count changed")
    require(g213_package["exact_algebra_checks"] == 23, "G213 exact algebra count changed")
    require(g213_package["independent_cases"] == 10000, "G213 case count changed")
    require(g213_package["independent_assertions"] == 300004, "G213 assertion count changed")
    require(g213_package["hostile_catches"] == 32, "G213 hostile count changed")
    require(g213_package["source_count"] == 12, "G213 source count changed")
    require(g213_package["g129_design_rank"] == 10, "G213 rank changed")
    require(g213_package["independent_mode_census_rank"] == 5, "G213 mode census rank changed")
    require(g213_package["independent_g207_g208_union_rank"] == 4, "G213 prior-tile rank changed")
    require(g213_package["independent_grading_completion_rank"] == 5, "G213 grading completion rank changed")
    require(
        by_id["G214"]["current_status"].startswith(
            "EXTERNALLY_REVIEWED_VERIFIED_WITH_CAVEATS__PREREGISTERED_AT_B15D5B4D__"
            "FRESH_GPT54_REVIEW_ACCEPTED_NO_REPAIR__SUPPLIED_REGULAR_LORENTZ_PAIR_PULLBACK"
        ),
        "G214 bounded grade changed or promoted",
    )
    for guard in (
        "G176_WORKING_COMPLETION",
        "POSITIVE_OVERLAP_DENSITY_WEIGHT_MJ_EQUALS_DET_P_MI",
        "INDUCED_C_EQUALS_JI_P_JJINVERSE_HAS_DETERMINANT_ONE",
        "HSJ_EQUALS_CTRANSPOSE_HSI_C",
        "RECONSTRUCTION_SQUARE_COMMUTES",
        "TRIPLE_OVERLAP_C_COCYCLE_EXACT",
        "PURE_RULER_REPARAMETERIZATION_ABSORBED_BY_DENSITY",
        "GENERAL_RECHART_EQUIVARIANT_NOT_INVARIANT",
        "G130_COMPATIBLE_COVER_RECONSTRUCTION_TRANSFERS_WITHOUT_DENSITY_LOSS",
        "DISTINCT_PAIR_SURFACES_HAVE_NO_NATIVE_METRIC_PRODUCT",
        "G171_UNMATCHED_INCIDENCE_DEFECT_SURVIVES",
        "NO_PHYSICAL_GERM_POPULATION_NETWORK_VALUE_GENERATION_CROSS_PAIR_INCIDENCE_OWNER_HISTORY_FLOW_XMAX_TRANSFER_SOURCE_ACTION_MATTER_MASS_OR_OBSERVATION",
    ):
        require(guard in by_id["G214"]["current_status"], f"G214 guard absent: {guard}")
    require(by_id["G214"]["epistemic_label"] == "MIXED", "G214 label changed")
    require(
        by_id["G214"]["active_use"]
        == "ACTIVE_BOUNDED_REGULAR_CALIBRATED_PAIR_CHART_DESCENT_AND_THREE_OBSERVER_TYPE_BOUNDARY_ONLY",
        "G214 active scope widened",
    )
    require(
        by_id["G214"]["controlling_source"]
        == "udt_g214_completed_tuple_overlap_and_three_observer_carry_2026-08-22/AUDIT_REPORT.md",
        "G214 controlling source changed",
    )
    g214 = ROOT / "udt_g214_completed_tuple_overlap_and_three_observer_carry_2026-08-22"
    for name in (
        "AUDIT_REPORT.md",
        "EXACT_DERIVATION.md",
        "LAY_REPORT.md",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "VERIFICATION_RESULT.json",
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_MANIFEST.tsv",
        "STATUS_LEDGER.tsv",
        "ADVERSARIAL_REVIEW_REQUEST.md",
        "EXTERNAL_REVIEW_RAW.md",
        "EXTERNAL_REVIEW_ADJUDICATION.md",
        "TRANSMISSION_RECORD.md",
    ):
        require((g214 / name).is_file(), f"G214 evidence missing: {name}")
    require(
        "G214_VERIFIED_WITH_CAVEATS__LOCAL_TO_COVER_DESCENT_CLOSES__THREE_PAIR_PRODUCT_NOT_DERIVED"
        in (g214 / "EXTERNAL_REVIEW_RAW.md").read_text(),
        "G214 external-review acceptance absent",
    )
    g214_package = json.loads((g214 / "VERIFICATION_RESULT.json").read_text())
    require(g214_package["status"] == "PASS", "G214 package verification failed")
    require(g214_package["no_write_replay"] is True, "G214 no-write replay absent")
    require(g214_package["core_files_hashed"] == 16, "G214 core file count changed")
    require(g214_package["exact_checks"] == 23, "G214 exact check count changed")
    require(g214_package["independent_cases"] == 10000, "G214 case count changed")
    require(g214_package["independent_assertions"] == 200000, "G214 assertion count changed")
    require(g214_package["hostile_catches"] == 10, "G214 hostile count changed")
    require(g214_package["source_count"] == 14, "G214 source count changed")
    require(
        g214_package["landing"]
        == "TYPED_COMPLETED_TUPLE_DESCENDS__G130_TRANSFERS__ARBITRARY_THREE_PAIR_PRODUCT_NOT_DERIVED",
        "G214 landing changed",
    )
    require(
        by_id["G215"]["current_status"].startswith(
            "EXTERNALLY_REVIEWED_VERIFIED_WITH_CAVEATS__PREREGISTERED_AT_F7FAA1C2__"
            "FRESH_GPT54_REVIEW_ACCEPTED_NO_SCIENTIFIC_REPAIR__G176_WORKING_COMPLETION__SUPPLIED_REGULAR_COMPLETED_PAIR_GERMS"
        ),
        "G215 bounded grade changed or promoted",
    )
    for guard in (
        "SHARED_CALIBRATED_OBSERVER_CLOCK_GERM_MEANS_IDENTICAL_CLOCK_TANGENT_AND_PARAMETER_ACROSS_INCIDENCES",
        "PHI_COMPLETED_EQUALS_MINUS_LOG_T",
        "T_SQUARED_EQUALS_MINUS_G_U_U",
        "INCIDENT_RULER_DIRECTION_ANGULAR_PARTICIPATION_DENSITY_AND_SHIFT_DO_NOT_CHANGE_COMPLETED_SCALAR_WHEN_CLOCK_GERM_SHARED",
        "OBSERVER_NETWORK_DELTA_XY_EQUALS_VARPHI_Y_MINUS_VARPHI_X",
        "ALL_COMMON_CLOCK_CYCLES_TELESCOPE",
        "G171_RAW_ANGULAR_SCALAR_VALUES_ONE_AND_59_OVER_25_RETAINED_AS_UNCOMPLETED_CONTROL",
        "G171_G176_COMPLETED_SCALAR_VALUES_BOTH_ONE",
        "DENSITY_AND_SHIFT_DIFFERENCES_RETAINED",
        "INDEPENDENT_EDGE_CLOCK_RECALIBRATION_RETAINS_EXACT_INCIDENCE_DEFECT",
        "G214_FULL_PAIR_METRIC_NONPRODUCT_RETAINED",
        "NO_PHYSICAL_GERM_POPULATION_METRIC_VALUES_PROFILES_FULL_GERM_CARRY_HISTORY_FLOW_XMAX_TRANSFER_OBSERVATION_ACTION_SOURCE_MATTER_BOOTSTRAP_MASS_OR_SIGNALLING",
    ):
        require(guard in by_id["G215"]["current_status"], f"G215 guard absent: {guard}")
    require(by_id["G215"]["epistemic_label"] == "MIXED", "G215 label changed")
    require(
        by_id["G215"]["active_use"]
        == "ACTIVE_BOUNDED_REGULAR_G176_COMPLETED_SHARED_CALIBRATED_CLOCK_SCALAR_INCIDENCE_DESCENT_ONLY",
        "G215 active scope widened",
    )
    require(
        by_id["G215"]["controlling_source"]
        == "udt_g215_completed_scalar_shared_clock_incidence_descent_2026-08-22/AUDIT_REPORT.md",
        "G215 controlling source changed",
    )
    g215 = ROOT / "udt_g215_completed_scalar_shared_clock_incidence_descent_2026-08-22"
    for name in (
        "AUDIT_REPORT.md",
        "EXACT_DERIVATION.md",
        "LAY_REPORT.md",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "VERIFICATION_RESULT.json",
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_MANIFEST.tsv",
        "STATUS_LEDGER.tsv",
        "ADVERSARIAL_REVIEW_REQUEST.md",
        "PREREGISTRATION_EXECUTION_NOTE.md",
        "EXTERNAL_REVIEW_RAW.md",
        "EXTERNAL_REVIEW_ADJUDICATION.md",
        "TRANSMISSION_RECORD.md",
    ):
        require((g215 / name).is_file(), f"G215 evidence missing: {name}")
    require(
        "G215_VERIFIED_WITH_CAVEATS__SHARED_CLOCK_SCALAR_DESCENT_CLOSES__FULL_GERM_CARRY_REMAINS_OPEN"
        in (g215 / "EXTERNAL_REVIEW_RAW.md").read_text(),
        "G215 external-review acceptance absent",
    )
    g215_package = json.loads((g215 / "VERIFICATION_RESULT.json").read_text())
    require(g215_package["status"] == "PASS", "G215 package verification failed")
    require(g215_package["no_write_replay"] is True, "G215 no-write replay absent")
    require(g215_package["core_files_hashed"] == 17, "G215 core file count changed")
    require(g215_package["exact_checks"] == 28, "G215 exact check count changed")
    require(g215_package["independent_cases"] == 10000, "G215 case count changed")
    require(g215_package["independent_assertions"] == 190000, "G215 assertion count changed")
    require(g215_package["hostile_catches"] == 13, "G215 hostile count changed")
    require(g215_package["source_count"] == 14, "G215 source count changed")
    require(g215_package["g171_raw_k"] == ["1", "59/25"], "G215 G171 raw witness changed")
    require(g215_package["g171_completed_k"] == ["1", "1"], "G215 G171 completion regrade changed")
    require(
        g215_package["landing"]
        == "COMPLETED_SCALAR_DESCENDS_TO_SHARED_CLOCK__G171_REGRADED__FULL_PAIR_CARRY_REMAINS_STRONGER",
        "G215 landing changed",
    )
    require(
        by_id["G216"]["current_status"].startswith(
            "EXTERNALLY_REVIEWED_VERIFIED_WITH_CAVEATS__PREREGISTERED_AT_65C5CFE7__"
            "FRESH_GPT54_ACCEPTED_NO_SCIENTIFIC_REPAIR__G176_WORKING_COMPLETION__"
            "SUPPLIED_REGULAR_TIMELIKE_OBSERVER_WORLDLINES_EVENTS_AND_EVENT_PAIR_GERM"
        ),
        "G216 bounded grade changed or promoted",
    )
    for guard in (
        "METRIC_PROPER_TIME_UNIT_TANGENT_U_SATISFIES_G_U_U_MINUS_ONE",
        "T_X_EQUALS_DTAU_X_DY",
        "UNIT_PROPER_CLOCK_HAS_T_ONE_PHI_ZERO",
        "ENDPOINT_RELATIVE_DELTA_AB_EQUALS_MINUS_LOG_DTAU_B_DTAU_A",
        "COMMON_POSITIVE_PAIR_REPARAMETERIZATION_CANCELS",
        "INDEPENDENT_INCIDENCE_REPARAMETERIZATION_RETAINS_G215_DEFECT",
        "REVERSAL_IS_INVERSE_FUNCTION_RULE",
        "COMPOSITION_IS_CHAIN_RULE_WHEN_DIRECT_GERM_IS_ACTUAL_COMPOSITE",
        "PRIMARY_STATIC_X0_EQUALS_CE_T_GIVES_DTAU_DX0_EQUALS_EXP_MINUS_PHI_AND_RECOVERS_PHI",
        "G215_SHARED_CLOCK_REGRADED_TO_OBSERVER_INCIDENCE_COMPARISON_CLOCK_NOT_BARE_UNIT_FOUR_VELOCITY",
        "NO_EXTRA_SCALAR_CLOCK_COEFFICIENT_AFTER_CALIBRATED_PAIR_MAP_SUPPLIED",
        "NO_PHYSICAL_EVENT_PAIR_GERM_POPULATION_METRIC_VALUES_PROFILES_HISTORY_FLOW_FULL_NONSCALAR_CARRY_XMAX_TRANSFER_OBSERVATION_ACTION_SOURCE_MATTER_BOOTSTRAP_MASS_OR_SIGNALLING",
    ):
        require(guard in by_id["G216"]["current_status"], f"G216 guard absent: {guard}")
    require(by_id["G216"]["epistemic_label"] == "MIXED", "G216 label changed")
    require(
        "external review described as canonization" in by_id["G216"]["forbidden_regression"],
        "G216 external-review scope guard absent",
    )
    require(
        by_id["G216"]["active_use"]
        == "ACTIVE_BOUNDED_REGULAR_G176_COMPLETED_EVENT_PAIR_PROPER_CLOCK_RATE_LAW_ONLY",
        "G216 active scope widened",
    )
    require(
        by_id["G216"]["controlling_source"]
        == "udt_g216_observer_event_comparison_clock_rate_ownership_2026-08-22/AUDIT_REPORT.md",
        "G216 controlling source changed",
    )
    g216 = ROOT / "udt_g216_observer_event_comparison_clock_rate_ownership_2026-08-22"
    for name in (
        "AUDIT_REPORT.md",
        "EXACT_DERIVATION.md",
        "LAY_REPORT.md",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "VERIFICATION_RESULT.json",
        "PREREGISTRATION.md",
        "PREREGISTRATION_EXECUTION_NOTE.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_MANIFEST.tsv",
        "STATUS_LEDGER.tsv",
        "EVIDENCE_GATES.md",
        "ADVERSARIAL_REVIEW_REQUEST.md",
        "EXTERNAL_REVIEW_RAW.md",
        "EXTERNAL_REVIEW_ADJUDICATION.md",
        "TRANSMISSION_RECORD.md",
        "build_review_intake.py",
    ):
        require((g216 / name).is_file(), f"G216 evidence missing: {name}")
    require(
        "G216_VERIFIED_WITH_CAVEATS__PAIR_GERM_PROPER_CLOCK_RATE_LAW_CLOSES__PHYSICAL_PAIR_GERM_OWNERSHIP_REMAINS_OPEN"
        in (g216 / "EXTERNAL_REVIEW_RAW.md").read_text(),
        "G216 external-review acceptance absent",
    )
    g216_package = json.loads((g216 / "VERIFICATION_RESULT.json").read_text())
    require(g216_package["status"] == "PASS", "G216 package verification failed")
    require(g216_package["no_write_replay"] is True, "G216 no-write replay absent")
    require(g216_package["core_files_hashed"] == 17, "G216 core file count changed")
    require(g216_package["exact_checks"] == 36, "G216 exact check count changed")
    require(g216_package["independent_cases"] == 10000, "G216 case count changed")
    require(g216_package["independent_assertions"] == 190000, "G216 assertion count changed")
    require(g216_package["hostile_catches"] == 17, "G216 hostile count changed")
    require(g216_package["source_count"] == 12, "G216 source count changed")
    require(g216_package["unit_clock_q"] == "1", "G216 unit-clock control changed")
    require(g216_package["pairing_derivative"] == "20/21", "G216 pairing derivative changed")
    require(g216_package["edge_exp_delta"] == "21/20", "G216 edge depth proxy changed")
    require(
        g216_package["landing"]
        == "PAIR_GERM_PROPER_CLOCK_RATE_LAW__UNIT_CLOCK_TRIVIALIZATION__COMMON_REPARAMETERIZATION_CANCELLATION",
        "G216 landing changed",
    )
    require(
        by_id["G217"]["current_status"].startswith(
            "EXTERNALLY_REVIEWED_VERIFIED_WITH_CAVEATS__PREREGISTERED_AT_CB40B4E9__"
            "FRESH_GPT54_ACCEPTED_NO_SCIENTIFIC_REPAIR__G176_WORKING_COMPLETION__"
            "SUPPLIED_FUTURE_TIMELIKE_OBSERVER_WORLDLINES_PAIRED_EVENTS_AND_ORDERED_DEPTH"
        ),
        "G217 bounded grade changed or promoted",
    )
    for guard in (
        "PROPER_CLOCK_TANGENT_AXES_ARE_ORIENTED_ONE_DIMENSIONAL_LINES",
        "POSITIVE_FIRST_JET_UNIQUE_AFTER_SOURCE_EVENT_TARGET_EVENT_AND_MULTIPLIER_FIXED",
        "LAMBDA_AB_EQUALS_DTAU_B_DTAU_A_EQUALS_EXP_MINUS_DELTA_AB",
        "WRONG_EXP_PLUS_SIGN_EXCLUDED",
        "REVERSAL_IS_MULTIPLICATIVE_INVERSE",
        "ACTUAL_COMPOSITE_FIRST_JET_IS_LAMBDA_BC_TIMES_LAMBDA_AB",
        "COMMON_PAIR_PARAMETER_CANCELS",
        "INDEPENDENT_INCIDENCE_REPARAMETERIZATION_CHANGES_CALIBRATED_INPUT",
        "SAME_DEPTH_CAN_PAIR_DISTINCT_TARGET_EVENTS",
        "DISTINCT_SMOOTH_GERMS_CAN_SHARE_PAIRED_EVENTS_AND_FIRST_JET",
        "INDEPENDENT_DIRECT_AC_NOT_FORCED_TO_EQUAL_ACTUAL_COMPOSITE",
        "NO_EVENT_OR_DEPTH_POPULATION_HIGHER_GERM_FULL_CARRY_HISTORY_XMAX_TRANSFER_OBSERVATION_ACTION_SOURCE_MATTER_BOOTSTRAP_MASS_OR_SIGNALLING",
    ):
        require(guard in by_id["G217"]["current_status"], f"G217 guard absent: {guard}")
    require(by_id["G217"]["epistemic_label"] == "MIXED", "G217 label changed")
    require(
        "external review described as canonization" in by_id["G217"]["forbidden_regression"],
        "G217 external-review scope guard absent",
    )
    require(
        by_id["G217"]["active_use"]
        == "ACTIVE_BOUNDED_POSITIVE_PROPER_CLOCK_FIRST_JET_ON_SUPPLIED_PAIRED_EVENTS_AND_DEPTH_ONLY",
        "G217 active scope widened",
    )
    require(
        by_id["G217"]["controlling_source"]
        == "udt_g217_founded_depth_event_pair_first_jet_ownership_2026-08-22/AUDIT_REPORT.md",
        "G217 controlling source changed",
    )
    g217 = ROOT / "udt_g217_founded_depth_event_pair_first_jet_ownership_2026-08-22"
    for name in (
        "AUDIT_REPORT.md",
        "EXACT_DERIVATION.md",
        "LAY_REPORT.md",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "VERIFICATION_RESULT.json",
        "PREREGISTRATION.md",
        "PREREGISTRATION_EXECUTION_NOTE.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_MANIFEST.tsv",
        "STATUS_LEDGER.tsv",
        "EVIDENCE_GATES.md",
        "ADVERSARIAL_REVIEW_REQUEST.md",
        "EXTERNAL_REVIEW_RAW.md",
        "EXTERNAL_REVIEW_ADJUDICATION.md",
        "TRANSMISSION_RECORD.md",
        "build_review_intake.py",
        "derive_first_jet_ownership.py",
        "verify_first_jet_independent.py",
        "run_catch_proofs.py",
        "verify_source_manifest_repository.py",
        "verify_package.py",
    ):
        require((g217 / name).is_file(), f"G217 evidence missing: {name}")
    require(
        "G217_VERIFIED_WITH_CAVEATS__POSITIVE_FIRST_JET_CLOSES_ON_SUPPLIED_PAIRED_EVENTS_AND_DEPTH__EVENT_INCIDENCE_AND_FULL_GERM_REMAIN_OPEN"
        in (g217 / "EXTERNAL_REVIEW_RAW.md").read_text(),
        "G217 external-review acceptance absent",
    )
    g217_package = json.loads((g217 / "VERIFICATION_RESULT.json").read_text())
    require(g217_package["status"] == "PASS", "G217 package verification failed")
    require(g217_package["no_write_replay"] is True, "G217 no-write replay absent")
    require(g217_package["core_files_hashed"] == 17, "G217 core file count changed")
    require(g217_package["exact_checks"] == 37, "G217 exact check count changed")
    require(g217_package["independent_cases"] == 10000, "G217 case count changed")
    require(g217_package["independent_assertions"] == 190000, "G217 assertion count changed")
    require(g217_package["hostile_catches"] == 16, "G217 hostile count changed")
    require(g217_package["source_count"] == 13, "G217 source count changed")
    require(g217_package["exp_depth_ab"] == "7/3", "G217 depth control changed")
    require(g217_package["first_jet_multiplier_ab"] == "3/7", "G217 first-jet control changed")
    require(g217_package["actual_composite_multiplier"] == "15/77", "G217 composite changed")
    require(g217_package["independent_direct_multiplier"] == "4/9", "G217 direct control changed")
    require(
        g217_package["landing"]
        == "FOUNDED_DEPTH_COMPLETES_POSITIVE_FIRST_JET_ON_SUPPLIED_PAIRED_EVENTS__EVENT_SELECTION_AND_FULL_GERM_REMAIN_OPEN",
        "G217 landing changed",
    )
    require(
        by_id["G218"]["current_status"].startswith(
            "PONDER_CONSENSUS__MULTI_AGENT_CROSS_EXAMINED__NOT_DERIVATION_OR_CANON__"
            "QUERY_INDEXED_REGULAR_CORRESPONDENCE_UNIFIES_EVENT_INCIDENCE_DEPTH_AND_POSITIVE_CLOCK_JET"
        ),
        "G218 ponder grade changed or promoted",
    )
    for guard in (
        "DELTA_IS_MINUS_LOG_PROPER_CLOCK_SLOPE",
        "SUPPLIED_OR_INDEPENDENTLY_METRIC_OWNED_SMOOTH_DEPTH_FIELD_PLUS_DECLARED_OBSERVER_CURVES_AND_ONE_EVENT_ANCHOR_INTEGRATES_LOCAL_ARROW",
        "CLOCK_ORIGIN_COORDINATES_ARE_GAUGE_BUT_ORDERED_EMBEDDED_EVENT_PAIR_AND_BRANCH_ARE_NOT_ERASED",
        "PRIMARY_STATIC_DECLARED_CONGRUENCE_GIVES_DELTA_AB_EQUALS_PHI_B_MINUS_PHI_A_MODULO_CLOCK_ORIGIN",
        "NULL_INCIDENCE_IS_EXACT_METRIC_NATIVE_CAUSAL_QUERY",
        "OBSERVATIONAL_STATUS_REQUIRES_EMISSION_RECEPTION_BRANCH_AND_CLOCK_READOUT",
        "NULL_NOT_FOUNDATIONALLY_PRIVILEGED_AS_UNIVERSAL_POSITIONAL_RELATION",
        "MOVING_FLAT_NULL_AND_FERMI_SLOPES_DIFFER",
        "FUTURE_CAUSAL_RETURN_NOT_MATHEMATICAL_INVERSE",
        "HIGHER_FULL_GERM_ORCHESTRA_QUERY_POPULATION_HISTORY_XMAX_AND_DOWNSTREAM_PHYSICS_OPEN",
    ):
        require(guard in by_id["G218"]["current_status"], f"G218 guard absent: {guard}")
    require(by_id["G218"]["epistemic_label"] == "MIXED", "G218 label changed")
    require(
        "PONDER called derivation theorem canon" in by_id["G218"]["forbidden_regression"],
        "G218 anti-promotion guard absent",
    )
    require(
        by_id["G218"]["active_use"]
        == "ACTIVE_PONDER_FRAME_FOR_CLOCK_ARROW_FACTORIZATION_AND_PROTOCOL_DISCRIMINATION_ONLY",
        "G218 active scope widened",
    )
    require(
        by_id["G218"]["controlling_source"]
        == "udt_g218_query_indexed_clock_correspondence_whiteboard_2026-08-22/WHITEBOARD_REPORT.md",
        "G218 controlling source changed",
    )
    g218 = ROOT / "udt_g218_query_indexed_clock_correspondence_whiteboard_2026-08-22"
    for name in (
        "MAP.md",
        "WHITEBOARD_REPORT.md",
        "DEBATE_LEDGER.tsv",
        "NEXT_AUDIT_PREREGISTRATION.md",
        "STATUS_LEDGER.tsv",
        "SOURCE_MANIFEST.tsv",
        "VERIFICATION_RESULT.json",
        "verify_whiteboard.py",
    ):
        require((g218 / name).is_file(), f"G218 evidence missing: {name}")
    g218_package = json.loads((g218 / "VERIFICATION_RESULT.json").read_text())
    require(g218_package["status"] == "PASS", "G218 whiteboard verification failed")
    require(g218_package["source_count"] == 9, "G218 source count changed")
    require(g218_package["debate_rows"] == 10, "G218 debate count changed")
    require(g218_package["status_rows"] == 7, "G218 status count changed")
    require(
        g218_package["landing"] == "QUERY_INDEXED_CLOCK_CORRESPONDENCE_PONDER_CONSENSUS",
        "G218 landing changed",
    )
    require(all(g218_package["checks"].values()), "G218 integrity check failed")
    require(
        by_id["G219"]["current_status"].startswith(
            "FRESHLY_ADVERSARIALLY_VERIFIED_WITH_REPAIRS_AND_CAVEATS__PREREGISTERED_AT_A8AC1A65__"
            "EXACT_FLAT_1PLUS1_INERTIAL_MOVING_OBSERVER_CONTROL"
        ),
        "G219 bounded grade or preregistration changed",
    )
    for guard in (
        "DELTA_EQUALS_MINUS_LOG_R",
        "NO_SECOND_RECIPROCAL_KERNEL_SCALAR_COEFFICIENT",
        "DENSITY_SHIFT_INCIDENCE_PAIR_PLANE_AND_HIGHER_GERM_REMAIN_SEPARATELY_TYPED",
        "OUTGOING_NULL_SLOPE_EXP_ETA",
        "A_FERMI_AND_INERTIAL_A_RADAR_SLOPE_SECH_ETA",
        "B_FERMI_SLOPE_COSH_ETA",
        "MATHEMATICAL_INVERSE_EXP_MINUS_ETA_DISTINCT_FROM_FUTURE_RETURN_EXP_ETA_AND_ECHO_EXP_2ETA",
        "FROZEN_FOUNDING_SOURCES_SELECT_NO_UNIVERSAL_MOVING_PROTOCOL",
        "LOCAL_CONNECTED_FUTURE_RIGHT_NULL_BRANCH_ONLY",
        "44822_EXPLICIT_EXACT_CHECKS",
        "PROTOCOL_MUTATION_GUARD",
        "NO_FULL_TIMELIVE_ORCHESTRA_PHYSICAL_PROTOCOL_HISTORY_XMAX_TRANSFER_OBSERVATION_ACTION_SOURCE_MATTER_BOOTSTRAP_MASS_OR_SIGNALLING",
    ):
        require(guard in by_id["G219"]["current_status"], f"G219 guard absent: {guard}")
    require(by_id["G219"]["epistemic_label"] == "MIXED", "G219 label changed")
    require(
        by_id["G219"]["active_use"]
        == "ACTIVE_BOUNDED_FLAT_INERTIAL_MOVING_CLOCK_ARROW_FACTORIZATION_AND_PROTOCOL_DISCRIMINATION_ONLY",
        "G219 active scope widened",
    )
    require(
        "flat control called a full time-live UDT history"
        in by_id["G219"]["forbidden_regression"],
        "G219 time-live anti-promotion guard absent",
    )
    require(
        "no extra reciprocal scalar coefficient used to erase density shift incidence pair-plane or higher germs"
        in by_id["G219"]["forbidden_regression"],
        "G219 typed-data preservation guard absent",
    )
    require(
        by_id["G219"]["controlling_source"]
        == "udt_g219_clock_arrow_dynamic_protocol_discrimination_2026-08-22/AUDIT_REPORT.md",
        "G219 controlling source changed",
    )
    g219 = ROOT / "udt_g219_clock_arrow_dynamic_protocol_discrimination_2026-08-22"
    for name in (
        "MAP.md",
        "PREMISE_LEDGER.tsv",
        "PREREGISTRATION.md",
        "REPAIR_PREREGISTRATION.md",
        "SOURCE_MANIFEST.tsv",
        "derive_clock_arrow_protocols.py",
        "verify_clock_arrow_independent.py",
        "run_catch_proofs.py",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "PROTOCOL_ATLAS.tsv",
        "EXACT_DERIVATION.md",
        "AUDIT_REPORT.md",
        "EVIDENCE_GATES.md",
        "STATUS_LEDGER.tsv",
        "ADVERSARIAL_REVIEW_REQUEST.md",
        "FRESH_ADVERSARIAL_REVIEW.md",
        "VERIFICATION_RESULT.json",
        "verify_package.py",
    ):
        require((g219 / name).is_file(), f"G219 evidence missing: {name}")
    g219_package = json.loads((g219 / "VERIFICATION_RESULT.json").read_text())
    require(g219_package["status"] == "PASS", "G219 package verification failed")
    require(g219_package["source_count"] == 11, "G219 source count changed")
    require(g219_package["exact_checks"] == 18, "G219 exact count changed")
    require(g219_package["independent_cases"] == 3684, "G219 case count changed")
    require(g219_package["independent_exact_checks"] == 44822, "G219 exact replay count changed")
    require(g219_package["hostile_catches"] == 10, "G219 catch count changed")
    require(g219_package["protocol_mutation_guard"] is True, "G219 protocol mutation guard absent")
    require(g219_package["no_write_replay"] is True, "G219 no-write replay absent")
    require(
        g219_package["fresh_adversarial_review"]
        == "ACCEPT_AFTER_PREREGISTERED_EVIDENCE_REPAIRS",
        "G219 fresh-review acceptance absent",
    )
    require(not g219_package["physical_protocol_selected"], "G219 protocol falsely selected")
    require(not g219_package["full_timelive_orchestra_derived"], "G219 widened to full time-live")
    require(
        g219_package["landing"]
        == "SCALAR_CHAIN_FACTORS_THROUGH_ONE_CLOCK_ARROW__PROTOCOL_REMAINS_QUERY_TYPED",
        "G219 landing changed",
    )
    require(
        by_id["G220"]["current_status"].startswith(
            "FRESHLY_ADVERSARIALLY_VERIFIED_AFTER_REPAIRS_WITH_CAVEATS__PREREGISTERED_AT_F24BF4DB__"
            "REPAIRS_PREREGISTERED_AT_98A13C7B__SUPPLIED_SMOOTH_LORENTZ_METRIC"
        ),
        "G220 bounded grade or preregistration changed",
    )
    for guard in (
        "WORLD_FUNCTION_IMPLICIT_SLOPE_R_EQUALS_MINUS_SIGMA_A_UA_OVER_SIGMA_AP_UB_EQUALS_KA_UA_OVER_KB_UB_EQUALS_OMEGA_A_OVER_OMEGA_B_POSITIVE",
        "RIGHT_NULL_CHORD_CPLUS_EQUALS_A_MINUS_N_BETA_POSITIVE",
        "PROPER_CLOCK_SLOPE_EQUALS_CPLUS_B_OVER_CPLUS_A",
        "SAME_CORRESPONDENCE_COMPLETED_CLOCK_LEG_TB_EQUALS_R_IS_COMPATIBILITY_IDENTITY_NOT_INDEPENDENT_G176_CONFIRMATION_OR_FULL_PAIR_PLANE",
        "AFFINE_WITNESS_D_EQUALS_A1_MINUS_S_DIRECTLY",
        "LATER_LEFT_RETURN_USES_CMINUS_EQUALS_A_PLUS_N_BETA_AT_ITS_OWN_EVENTS_NOT_GENERIC_OUTGOING_INVERSE",
        "111343_EXACT_CHECKS",
        "5000_DIRECT_COORDINATE_WORLD_FUNCTION_RECONSTRUCTIONS",
        "15_INJECTED_MUTATION_CATCHES",
        "OPTIMIZED_MODE_REJECTED",
        "NULL_REMAINS_QUERY_TYPED",
        "NO_PHYSICAL_PROTOCOL_BRANCH_POPULATION_FULL_PAIR_PLANE_ANGULAR_SCREEN_MIXING_HISTORY_XMAX_TRANSFER_OBSERVATION_ACTION_SOURCE_MATTER_BOOTSTRAP_MASS_OR_SIGNALLING",
    ):
        require(guard in by_id["G220"]["current_status"], f"G220 guard absent: {guard}")
    require(by_id["G220"]["epistemic_label"] == "MIXED", "G220 label changed")
    require(
        by_id["G220"]["active_use"]
        == "ACTIVE_BOUNDED_COVARIANT_CLOCK_SLOPE_ON_ONE_SUPPLIED_REGULAR_NULL_BRANCH_AND_EXACT_TIME_ONLY_TRIANGULAR_BASE_CONTROL_ONLY",
        "G220 active scope widened",
    )
    require(
        "completed clock-leg compatibility called independent confirmation of G176 or construction of a full pair pullback"
        in by_id["G220"]["forbidden_regression"],
        "G220 completed-clock-leg compatibility guard absent",
    )
    require(
        "time-only triangular base called the full dynamic orchestra"
        in by_id["G220"]["forbidden_regression"],
        "G220 full-orchestra anti-promotion guard absent",
    )
    require(
        by_id["G220"]["controlling_source"]
        == "udt_g220_covariant_null_clock_arrow_timelive_lift_2026-08-22/AUDIT_REPORT.md",
        "G220 controlling source changed",
    )
    g220 = ROOT / "udt_g220_covariant_null_clock_arrow_timelive_lift_2026-08-22"
    for name in (
        "MAP.md",
        "PREMISE_LEDGER.tsv",
        "PREREGISTRATION.md",
        "REPAIR_PREREGISTRATION.md",
        "SOURCE_MANIFEST.tsv",
        "derive_covariant_null_clock_arrow.py",
        "verify_null_clock_arrow_independent.py",
        "run_catch_proofs.py",
        "verify_package.py",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "CONTROL_ATLAS.tsv",
        "EXACT_DERIVATION.md",
        "AUDIT_REPORT.md",
        "EVIDENCE_GATES.md",
        "STATUS_LEDGER.tsv",
        "ADVERSARIAL_REVIEW_REQUEST.md",
        "FRESH_ADVERSARIAL_REVIEW.md",
        "REPAIR_FOLLOWUP_REVIEW.md",
        "VERIFICATION_RESULT.json",
    ):
        require((g220 / name).is_file(), f"G220 evidence missing: {name}")
    g220_package = json.loads((g220 / "VERIFICATION_RESULT.json").read_text())
    require(g220_package["status"] == "PASS", "G220 package verification failed")
    require(g220_package["source_count"] == 11, "G220 source count changed")
    require(g220_package["symbolic_checks"] == 28, "G220 symbolic count changed")
    require(g220_package["independent_cases"] == 11171, "G220 case count changed")
    require(g220_package["independent_exact_checks"] == 111343, "G220 exact replay count changed")
    require(
        g220_package["direct_world_function_coordinate_cases"] == 5000,
        "G220 direct world-function reconstruction count changed",
    )
    require(g220_package["affine_positive_d_cases"] == 500, "G220 positive-d count changed")
    require(g220_package["affine_negative_d_cases"] == 500, "G220 negative-d count changed")
    require(g220_package["injected_mutation_catches"] == 15, "G220 catch count changed")
    require(g220_package["payload_contract_mutation_guard"] is True, "G220 payload guard absent")
    require(g220_package["optimized_mode_rejected"] is True, "G220 optimized-mode guard absent")
    require(g220_package["no_write_replay"] is True, "G220 no-write replay absent")
    require(
        g220_package["fresh_adversarial_review"] == "ACCEPT_AFTER_PREREGISTERED_REPAIRS",
        "G220 fresh-review acceptance absent",
    )
    require(
        g220_package["completed_clock_leg_compatibility_only"] is True,
        "G220 completed-clock-leg compatibility ceiling absent",
    )
    require(not g220_package["physical_protocol_selected"], "G220 protocol falsely selected")
    require(not g220_package["full_dynamic_orchestra_derived"], "G220 widened to full orchestra")
    require(
        g220_package["landing"]
        == "COVARIANT_NULL_CLOCK_ARROW_DERIVED__COMPLETED_CLOCK_LEG_COMPATIBLE__NULL_REMAINS_QUERY_TYPED",
        "G220 landing changed",
    )
    require(
        by_id["G221"]["current_status"].startswith(
            "FRESHLY_ADVERSARIALLY_VERIFIED_WITH_CAVEATS__PREREGISTERED_AT_58F01F2C__"
            "SUPPLIED_SMOOTH_COMPLETE_COFRAME_FIXED_REGULAR_2PLUS2_CHART"
        ),
        "G221 bounded grade or preregistration changed",
    )
    for guard in (
        "UNIQUE_FUTURE_COFRAME_ROOT_PHAT0_EQUALS_MINUS_N_BETA_PI_MINUS_A_R_OVER_D",
        "MEASURED_FREQUENCY_W_EQUALS_MINUS_PT_OVER_P",
        "Q_SX_AND_ST_ENTER_UPSTREAM_BEFORE_SCALAR_READOUT",
        "HAMILTON_JACOBI_INCIDENCE_VELOCITY_COMES_FROM_SAME_FUTURE_ENERGY_ROOT",
        "TRANSVERSE_OFF_LIMIT_RECOVERS_G220_W_EQUALS_PX_OVER_A_MINUS_N_BETA_AND_R_EQUALS_CPLUS_B_OVER_CPLUS_A",
        "SAME_CORRESPONDENCE_COMPLETED_CLOCK_LEG_TB_EQUALS_RAB_IS_COMPATIBILITY_ONLY",
        "154000_EXACT_CHECKS",
        "18_INJECTED_MUTATION_CATCHES",
        "FRESH_EXTERNAL_GPT54_ACCEPTED_NO_REPAIRS",
        "NULL_AND_FULL_PAIR_REMAIN_QUERY_TYPED",
        "NO_PHYSICAL_PROTOCOL_BRANCH_POPULATION_FULL_PAIR_PLANE_SCREEN_JACOBI_HISTORY_XMAX_TRANSFER_OBSERVATION_ACTION_SOURCE_MATTER_BOOTSTRAP_MASS_OR_SIGNALLING",
    ):
        require(guard in by_id["G221"]["current_status"], f"G221 guard absent: {guard}")
    require(by_id["G221"]["epistemic_label"] == "MIXED", "G221 label changed")
    require(
        by_id["G221"]["active_use"]
        == "ACTIVE_BOUNDED_COMPLETE_COFRAME_NULL_CLOCK_CHORD_ON_ONE_SUPPLIED_REGULAR_QUERY_AND_EXACT_G220_REDUCTION_ONLY",
        "G221 active scope widened",
    )
    require(
        "screen Jacobi transport collapsed into the scalar chord"
        in by_id["G221"]["forbidden_regression"],
        "G221 screen/Jacobi separation guard absent",
    )
    require(
        by_id["G221"]["controlling_source"]
        == "udt_g221_complete_coframe_null_clock_chord_2026-08-22/AUDIT_REPORT.md",
        "G221 controlling source changed",
    )
    g221 = ROOT / "udt_g221_complete_coframe_null_clock_chord_2026-08-22"
    for name in (
        "MAP.md",
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_MANIFEST.tsv",
        "derive_complete_coframe_null_chord.py",
        "verify_complete_coframe_null_chord_independent.py",
        "run_catch_proofs.py",
        "build_review_intake.py",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "CONTROL_ATLAS.tsv",
        "EXACT_DERIVATION.md",
        "AUDIT_REPORT.md",
        "EVIDENCE_GATES.md",
        "STATUS_LEDGER.tsv",
        "ADVERSARIAL_REVIEW_REQUEST.md",
        "FRESH_ADVERSARIAL_REVIEW.md",
        "VERIFICATION_RESULT.json",
        "verify_package.py",
    ):
        require((g221 / name).is_file(), f"G221 evidence missing: {name}")
    g221_package = json.loads((g221 / "VERIFICATION_RESULT.json").read_text())
    require(g221_package["status"] == "PASS", "G221 package verification failed")
    require(g221_package["source_count"] == 12, "G221 source count changed")
    require(g221_package["symbolic_checks"] == 21, "G221 symbolic count changed")
    require(g221_package["independent_cases"] == 12000, "G221 case count changed")
    require(g221_package["independent_exact_checks"] == 154000, "G221 exact count changed")
    require(g221_package["full_sector_cases"] == 10000, "G221 full-sector count changed")
    require(g221_package["screen_covariance_cases"] == 10000, "G221 covariance count changed")
    require(g221_package["future_past_branch_cases"] == 10000, "G221 branch count changed")
    require(g221_package["G220_reduction_pairs"] == 2000, "G221 G220 reduction count changed")
    require(g221_package["injected_mutation_catches"] == 18, "G221 catch count changed")
    require(g221_package["payload_contract_mutation_guard"] is True, "G221 payload guard absent")
    require(g221_package["optimized_mode_rejected"] is True, "G221 optimized guard absent")
    require(g221_package["no_write_replay"] is True, "G221 no-write replay absent")
    require(
        g221_package["fresh_adversarial_review"] == "ACCEPT_NO_REPAIRS",
        "G221 fresh-review acceptance absent",
    )
    require(g221_package["completed_clock_leg_compatibility_only"] is True, "G221 clock ceiling absent")
    require(not g221_package["physical_protocol_selected"], "G221 protocol falsely selected")
    require(not g221_package["full_pair_plane_constructed"], "G221 widened to full pair plane")
    require(not g221_package["screen_Jacobi_collapsed"], "G221 collapsed screen Jacobi")
    require(
        g221_package["landing"]
        == "COMPLETE_COFRAME_NULL_CLOCK_CHORD_DERIVED_CONDITIONALLY__SCREEN_AND_MIXING_ENTER_UPSTREAM__G220_RECOVERED__NULL_AND_FULL_PAIR_REMAIN_QUERY_TYPED",
        "G221 landing changed",
    )
    require(
        "R1_FINAL_RETRY_GPT54_TWO_LIVE_NO_WRITE_REPLAYS_EXIT_ZERO_JSON_IDENTICAL_38_HASHES_UNCHANGED_RUNTIME_EMPTY"
        in by_id["G195"]["current_status"],
        "G195 external R1 acceptance absent",
    )
    require(
        "ARBITRARY_REAL_C2_M_EQUALS_S_PLUS_OMEGA"
        in by_id["G195"]["current_status"],
        "G195 arbitrary real matrix family absent",
    )
    require(
        "NO_NONVERTEX_CAUSTIC_ONLY_IN_DECLARED_CONNECTED_REGULAR_DISPLAYED_FAMILY"
        in by_id["G195"]["current_status"],
        "G195 displayed-family no-caustic guard absent",
    )
    require(
        "NOT_FULL_END_TO_END_METRIC_JACOBI_INTERVAL_PROPAGATION"
        in by_id["G195"]["current_status"],
        "G195 independent-evidence ceiling absent",
    )
    require(
        "NO_P1_G116_G189_XMAX_TRANSFER_SOURCE_FIT_OR_POST_READOUT_ORCHESTRA"
        in by_id["G195"]["current_status"],
        "G195 scaffold exclusion absent",
    )
    g195 = ROOT / "udt_g195_antisymmetric_screen_rotation_boundary_2026-08-20"
    for name in (
        "AUDIT_REPORT.md",
        "EXTERNAL_REVIEW_ADJUDICATION.md",
        "EXTERNAL_REPAIR_RETRY_RAW.md",
        "EXTERNAL_REPAIR_RETRY_TRANSCRIPT.txt.gz",
        "NO_WRITE_REPLAY_RESULT.json",
        "PACKAGE_VERIFICATION_RESULT.json",
        "REPAIR_VERIFICATION_RESULT.json",
        "TRANSMISSION_RECORD.md",
    ):
        require((g195 / name).is_file(), f"G195 evidence missing: {name}")
    require(
        "G195_NO_WRITE_EVIDENCE_REPAIR_ACCEPTED__BOUNDED_LANDING_RETAINED"
        in (g195 / "EXTERNAL_REVIEW_ADJUDICATION.md").read_text(),
        "G195 external R1 acceptance missing",
    )
    require(
        '"external_review": "G195_NO_WRITE_EVIDENCE_REPAIR_ACCEPTED__BOUNDED_LANDING_RETAINED"'
        in (g195 / "PACKAGE_VERIFICATION_RESULT.json").read_text(),
        "G195 accepted package state absent",
    )
    require(
        "R5_REPAIR_FOLLOWUP_GPT54_ACCEPTED_BOUNDED_LANDING_RETAINED"
        in by_id["G194"]["current_status"],
        "G194 external R5 repair acceptance absent",
    )
    require(
        "ARBITRARY_REAL_C2_SYMMETRIC_M_OF_ETA"
        in by_id["G194"]["current_status"],
        "G194 arbitrary symmetric family absent",
    )
    require(
        "NO_NONVERTEX_CAUSTIC_ONLY_IN_DECLARED_CONNECTED_REGULAR_SYMMETRIC_FAMILY"
        in by_id["G194"]["current_status"],
        "G194 symmetric-family no-caustic guard absent",
    )
    require(
        "NOT_FULL_END_TO_END_METRIC_JACOBI_INTERVAL_PROPAGATION"
        in by_id["G194"]["current_status"],
        "G194 independent-evidence ceiling absent",
    )
    require(
        "NO_P1_G116_G189_XMAX_TRANSFER_SOURCE_FIT_OR_POST_READOUT_ORCHESTRA"
        in by_id["G194"]["current_status"],
        "G194 scaffold exclusion absent",
    )
    g194 = ROOT / "udt_g194_general_symmetric_screen_mixing_closure_2026-08-20"
    for name in (
        "AUDIT_REPORT.md",
        "EXTERNAL_REVIEW_ADJUDICATION.md",
        "EXTERNAL_R5_REVIEW_RAW.md",
        "EXTERNAL_R5_REVIEW_TRANSCRIPT.txt.gz",
        "PACKAGE_VERIFICATION_RESULT.json",
        "REPAIR_VERIFICATION_RESULT.json",
        "TRANSMISSION_RECORD.md",
    ):
        require((g194 / name).is_file(), f"G194 evidence missing: {name}")
    require(
        "G194_R5_REPAIRS_ACCEPTED__BOUNDED_LANDING_RETAINED"
        in (g194 / "EXTERNAL_REVIEW_ADJUDICATION.md").read_text(),
        "G194 external R5 repair acceptance missing",
    )
    require(
        '"external_review": "G194_R5_REPAIRS_ACCEPTED__BOUNDED_LANDING_RETAINED"'
        in (g194 / "PACKAGE_VERIFICATION_RESULT.json").read_text(),
        "G194 accepted package state absent",
    )
    require(
        "REPAIR_FOLLOWUP_GPT54_ACCEPTED_BOUNDED_LANDING_RETAINED"
        in by_id["G193"]["current_status"],
        "G193 external repair follow-up acceptance absent",
    )
    require(
        "FULL_SELF_ADJOINT_TIDE_TAU0_I_PLUS_2MPRIME_MINUS4M2_OVER_A4"
        in by_id["G193"]["current_status"],
        "G193 full matrix tide absent",
    )
    require(
        "NO_NONVERTEX_CAUSTIC_ONLY_IN_DECLARED_CONNECTED_REGULAR_SYMMETRIC_FAMILY"
        in by_id["G193"]["current_status"],
        "G193 symmetric-family no-caustic guard absent",
    )
    require(
        "NOT_FULL_END_TO_END_METRIC_JACOBI_INTERVAL_PROPAGATION"
        in by_id["G193"]["current_status"],
        "G193 independent-evidence ceiling absent",
    )
    require(
        "NO_P1_G116_G189_XMAX_TRANSFER_SOURCE_FIT_OR_POST_READOUT_ORCHESTRA"
        in by_id["G193"]["current_status"],
        "G193 scaffold exclusion absent",
    )
    g193 = ROOT / "udt_g193_noncommuting_transverse_mixing_extension_2026-08-20"
    for name in (
        "AUDIT_REPORT.md",
        "EXTERNAL_REVIEW_ADJUDICATION.md",
        "EXTERNAL_REVIEW_RAW.md",
        "EXTERNAL_REVIEW_TRANSCRIPT.txt.gz",
        "EXTERNAL_REPAIR_REVIEW_RAW.md",
        "EXTERNAL_REPAIR_REVIEW_TRANSCRIPT.txt.gz",
        "PACKAGE_VERIFICATION_RESULT.json",
        "TRANSMISSION_RECORD.md",
    ):
        require((g193 / name).is_file(), f"G193 evidence missing: {name}")
    require(
        "G193_REPAIRS_ACCEPTED__BOUNDED_LANDING_RETAINED"
        in (g193 / "EXTERNAL_REVIEW_ADJUDICATION.md").read_text(),
        "G193 external repair acceptance missing",
    )
    require(
        '"external_review": "G193_REPAIRS_ACCEPTED__BOUNDED_LANDING_RETAINED"'
        in (g193 / "PACKAGE_VERIFICATION_RESULT.json").read_text(),
        "G193 accepted package state absent",
    )
    require(
        "REPAIR_FOLLOWUP_GPT54_ACCEPTED_WITH_STATED_BOUNDS_NO_REMAINING_REPAIR"
        in by_id["G192"]["current_status"],
        "G192 external repair follow-up acceptance absent",
    )
    require(
        "FREQUENCY_Z_EQUALS_ONE_OVER_A_AND_TURNS_AT_SIGN_CHANGING_ZEROS_OF_A_PRIME"
        in by_id["G192"]["current_status"],
        "G192 frequency-turn classification absent",
    )
    require(
        "FULL_ORIGINAL_SCREEN_TIDE_WITH_C_EQUALS_SQRT2_MU_PRIME_MINUS4MU2_OVER_A4"
        in by_id["G192"]["current_status"],
        "G192 full live mixing tide absent",
    )
    require(
        "NO_NONVERTEX_CAUSTIC_ONLY_IN_DECLARED_CONNECTED_REGULAR_FAMILY"
        in by_id["G192"]["current_status"],
        "G192 family-scoped no-caustic guard absent",
    )
    require(
        "NO_P1_G116_G189_STATIC_PROFILE_XMAX_TRANSFER_SOURCE_FIT_OR_POST_READOUT_ORCHESTRA"
        in by_id["G192"]["current_status"],
        "G192 scaffold exclusion absent",
    )
    g192 = ROOT / "udt_g192_smooth_timelive_mixing_family_classification_2026-08-20"
    for name in (
        "AUDIT_REPORT.md",
        "EXTERNAL_REVIEW_ADJUDICATION.md",
        "EXTERNAL_REVIEW_RAW.md",
        "EXTERNAL_REVIEW_TRANSCRIPT.txt.gz",
        "EXTERNAL_FOLLOWUP_REVIEW_RAW.md",
        "EXTERNAL_FOLLOWUP_REVIEW_TRANSCRIPT.txt.gz",
        "PACKAGE_VERIFICATION_RESULT.json",
        "TRANSMISSION_RECORD.md",
    ):
        require((g192 / name).is_file(), f"G192 evidence missing: {name}")
    require(
        "G192_ACCEPTED_WITH_STATED_BOUNDS"
        in (g192 / "EXTERNAL_REVIEW_ADJUDICATION.md").read_text(),
        "G192 external acceptance missing",
    )
    require(
        '"external_review": "G192_ACCEPTED_WITH_STATED_BOUNDS"'
        in (g192 / "PACKAGE_VERIFICATION_RESULT.json").read_text(),
        "G192 accepted package state absent",
    )
    require(
        "REPAIR_FOLLOWUP_GPT54_ACCEPTED_WITH_STATED_BOUNDS_NO_REMAINING_REPAIR"
        in by_id["G191"]["current_status"],
        "G191 external repair follow-up acceptance absent",
    )
    require(
        "NONCONFORMALLY_FLAT_FOR_MU_NONZERO" in by_id["G191"]["current_status"],
        "G191 nonconformal witness absent",
    )
    require(
        "LIVE_TRACEFREE_OFFDIAGONAL_MINUS4MU2_OVER_Q2" in by_id["G191"]["current_status"],
        "G191 live cross-screen channel absent",
    )
    require(
        "SCIENTIFIC_ARTIFACTS_BYTE_IDENTICAL" in by_id["G191"]["current_status"],
        "G191 repair byte-identity guard absent",
    )
    require(
        "NO_P1_G116_G189_STATIC_PHI_OF_R_R_OF_Z_XMAX_FIT_TRANSFER_OR_POST_READOUT_ORCHESTRA"
        in by_id["G191"]["current_status"],
        "G191 scaffold exclusion absent",
    )
    g191 = ROOT / "udt_g191_nonconformal_timelive_mixing_join_2026-08-20"
    for name in (
        "AUDIT_REPORT.md",
        "EXTERNAL_REVIEW_ADJUDICATION.md",
        "EXTERNAL_REVIEW_RAW.md",
        "EXTERNAL_REVIEW_TRANSCRIPT.txt.gz",
        "EXTERNAL_FOLLOWUP_REVIEW_RAW.md",
        "EXTERNAL_FOLLOWUP_REVIEW_TRANSCRIPT.txt.gz",
        "PACKAGE_VERIFICATION_RESULT.json",
        "TRANSMISSION_RECORD.md",
    ):
        require((g191 / name).is_file(), f"G191 evidence missing: {name}")
    require(
        "G191_ACCEPTED_WITH_STATED_BOUNDS"
        in (g191 / "EXTERNAL_REVIEW_ADJUDICATION.md").read_text(),
        "G191 external acceptance missing",
    )
    require(
        '"external_review": "G191_ACCEPTED_WITH_STATED_BOUNDS"'
        in (g191 / "PACKAGE_VERIFICATION_RESULT.json").read_text(),
        "G191 accepted package state absent",
    )
    require(
        "FRESH_EXTERNAL_GPT54_ACCEPTED_WITH_STATED_BOUNDS_NO_REPAIRS"
        in by_id["G190"]["current_status"],
        "G190 external bounded acceptance absent",
    )
    require(
        "JOINT_NATIVE_OUTPUT_LAMBDA_TO_Z_D_DA" in by_id["G190"]["current_status"],
        "G190 parametric joint evaluator absent",
    )
    require(
        "DA_OF_Z_DESCENDS_ONLY_WHERE_Z_IS_LOCALLY_ONE_TO_ONE_AND_SCREEN_NONCAUSTIC"
        in by_id["G190"]["current_status"],
        "G190 local descent boundary absent",
    )
    require(
        "NO_P1_STATIC_PHI_OF_R_R_OF_Z_XMAX_FIT_OR_POST_READOUT_ANGULAR_FACTOR"
        in by_id["G190"]["current_status"],
        "G190 scaffold exclusion absent",
    )
    g190 = ROOT / "udt_g190_completed_pair_timelive_frequency_screen_join_2026-08-20"
    for name in (
        "AUDIT_REPORT.md",
        "EXTERNAL_REVIEW_ADJUDICATION.md",
        "EXTERNAL_REVIEW_RAW.md",
        "EXTERNAL_REVIEW_TRANSCRIPT.txt.gz",
        "PACKAGE_VERIFICATION_RESULT.json",
        "TRANSMISSION_RECORD.md",
    ):
        require((g190 / name).is_file(), f"G190 evidence missing: {name}")
    require(
        "G190_ACCEPTED_WITH_STATED_BOUNDS"
        in (g190 / "EXTERNAL_REVIEW_ADJUDICATION.md").read_text(),
        "G190 external acceptance missing",
    )
    require(
        '"external_review": "G190_ACCEPTED_WITH_STATED_BOUNDS"'
        in (g190 / "PACKAGE_VERIFICATION_RESULT.json").read_text(),
        "G190 accepted package state absent",
    )
    require(
        "REPAIR_FOLLOWUP_ACCEPTED_SCIENTIFIC_LANDING_UNCHANGED"
        in by_id["G189"]["current_status"],
        "G189 external repair follow-up acceptance absent",
    )
    require(
        "R_EQUALS_R0_TANH_PHI_PROVISIONAL_CONTROL_HAS_NONZERO_CENTER_DERIVATIVE"
        in by_id["G189"]["current_status"],
        "G189 regular-center type boundary absent",
    )
    require(
        "IMPORTED_TRANSPARENT_TRANSFER" in by_id["G189"]["current_status"],
        "G189 imported-transfer ownership guard absent",
    )
    require(
        "FRESH_EXTERNAL_GPT54_ACCEPTED_WITH_STATED_BOUNDS" in by_id["G188"]["current_status"],
        "G188 external bounded acceptance absent",
    )
    require(
        "WITNESS_FAMILY_LEVEL_NOT_GENERIC_ARBITRARY_COFRAME_PARSER"
        in by_id["G188"]["current_status"],
        "G188 independent-replay scope caveat absent",
    )
    require(
        "CERTIFICATION_REPAIR_FOLLOWUP_ACCEPTED_SCIENTIFIC_LANDING_UNCHANGED"
        in by_id["G187"]["current_status"],
        "G187 external repair follow-up acceptance absent",
    )
    require(
        "FRESH_EXTERNAL_GPT54_ACCEPTED_WITH_STATED_BOUNDS" in by_id["G186"]["current_status"],
        "G186 external bounded acceptance absent",
    )
    require(
        by_id["G01"]["current_status"] == "DERIVED_RECIPROCAL_CHARACTER_ON_SUPPLIED_ORDERED_DEPTH",
        "founded relational character",
    )
    require(
        by_id["G02"]["current_status"]
        == "DERIVED_DELTA_MAPS_TO_DIAG_EXP_MINUS_DELTA_EXP_PLUS_DELTA",
        "founded relational character action",
    )
    require("physical complete-pair cocycle selection" in by_id["G02"]["open_scope"], "complete-pair target absent")
    require("general observer/event/path-to-depth law" in by_id["G01"]["open_scope"], "depth law promoted")
    require("universal pointwise physical scalar" in by_id["G01"]["forbidden_regression"], "pointwise owner guard absent")
    require(by_id["G03"]["active_use"] == "COMPARISON_ONLY_NOT_NATIVE", "independent phi promoted")
    require(by_id["G04"]["current_status"] == "CHALLENGED_OWNER_POSTULATE_NOT_DERIVED", "strong local CSN status")
    require(by_id["G04"]["active_use"] == "INACTIVE_UNLESS_CHARLES_EXPLICITLY_REAUTHORIZES", "strong local CSN activated")
    require(by_id["G05"]["active_use"] == "ALGEBRA_ONLY", "common cancellation promoted")
    require(by_id["G06"]["active_use"] == "ACTIVE_CALIBRATION", "c/G anchors dropped")
    require(by_id["G07"]["active_use"] == "GENERIC_ARENA_BASELINE_ONLY", "generic metric count promoted")
    require(by_id["G08"]["epistemic_label"] == "OPEN", "4D extension promoted")
    require(by_id["G09"]["epistemic_label"] == "POSIT", "carrier promoted")
    require(by_id["G10"]["active_use"] == "INACTIVE_WITHOUT_STRONG_CSN_PREMISE", "C2/Bach promoted")
    require(by_id["G11"]["active_use"] == "NOT_SELECTED", "EH promoted")
    require(
        by_id["G12"]["current_status"]
        == "WORKING_MUTUAL_ADMISSIBILITY_POSIT__PARTIAL_KINEMATIC_JOIN_DERIVED__SMOOTH_EXTENSION_CARTAN_NONSELECTION__FULL_FIRST_AND_SECOND_JET_CURVATURE_ATLASES_DERIVED__CONDITIONAL_LOCAL_SAME_SOLUTION_PHI_CURVATURE_COMPATIBILITY__GLOBAL_FACTORIZATION_GROUPOID_AND_OVERLAP_NONSELECTION_DERIVED__FOUNDING_RELATIONAL_CHARACTER_ON_SUPPLIED_DEPTH_DERIVED__POINTWISE_PHI_PRESENTATION_POTENTIAL_ON_SUPPLIED_FACTORIZATION__CONDITIONAL_STATIONARY_KILLING_DEPTH__COMPLETE_PAIR_ORCHESTRA_MODULATION_AND_GROUPOID_COCYCLE_HOME_DERIVED__PHYSICAL_COMPLETE_PAIR_COCYCLE_AND_COMPLETE_RETURN_OPEN",
        "bootstrap status regressed or promoted",
    )
    require(by_id["G12"]["active_use"] == "FALSIFIABLE_RELATIONAL_ARCHITECTURE_ONLY", "bootstrap use changed")
    require("complete-arrow strain or spectral magnitude promoted" in by_id["G12"]["forbidden_regression"], "orchestra promotion guard absent")
    require(by_id["G13"]["active_use"] == "TORIC_GEOMETRY_ONLY", "Maxwell promoted")
    require(
        by_id["G14"]["current_status"].startswith(
            "OWNER_REFRAMED_WORKING_GLOBAL_COMPLETION_CONSEQUENCE_TARGET"
        ),
        "Xmax consequence frame reopened or promoted",
    )
    require(
        by_id["G14"]["active_use"]
        == "OWNER_RATIFIED_LIMIT_MEANING__INACTIVE_AS_LOCAL_KERNEL_INPUT__GLOBAL_SUPREMUM_TARGET_ONLY",
        "Xmax dependency reversal mistyped",
    )
    require("numerical value" in by_id["G14"]["open_scope"], "numerical Xmax promoted")
    require("all-frame recentering theorem" in by_id["G14"]["open_scope"], "Xmax frame theorem promoted")
    require("material wall" in by_id["G14"]["forbidden_regression"], "Xmax wall guard absent")
    require("native kernel input" in by_id["G14"]["forbidden_regression"], "Xmax kernel-input guard absent")
    require(by_id["G15"]["active_use"] == "STATIC_FINITE_BOX_AND_CARRIER_CONDITIONAL", "Hopfion promoted")
    require(by_id["G16"]["current_status"] == "OPEN", "complete physics promoted")
    require(
        by_id["G17"]["current_status"] == "KEPT_MULTIPLY_ANCHORED_SPLIT_FROM_MIRROR_CLAUSE",
        "finite-cell split reading changed",
    )
    require(by_id["G17"]["active_use"] == "ACTIVE_FOUNDATION_SPLIT_READING", "finite-cell split inactive")
    require(
        by_id["G18"]["current_status"] == "OWNER_RATIFIED_PROPOSAL_NOT_DERIVED_SPLIT_RULED_2026-07-30",
        "mirror closure promoted or dropped",
    )
    require(
        by_id["G18"]["active_use"] == "WORKING_PREMISE_ONLY_STAMPS_TRAVEL_VIA_CONSUMER_LEDGER",
        "mirror closure use changed",
    )
    require(by_id["G19"]["active_use"] == "CONFIGURATION_ARENA_ONLY", "coframe promoted")
    require(by_id["G20"]["active_use"] == "NO_UNIVERSAL_VARIATION_DOMAIN_SELECTED", "variation owner promoted")
    require("query varied as field" in by_id["G20"]["forbidden_regression"], "query variation guard absent")
    require(by_id["G21"]["current_status"] == "OPEN_RESPONSE_OR_CURRENT_ROLE_NOT_SUBSTANCE", "source mistyped")
    require(by_id["G22"]["active_use"] == "NO_UNCONDITIONAL_MASS_CLAIM", "mass promoted")
    require(by_id["G23"]["active_use"] == "SEMANTIC_FRAME_ONLY", "copresence promoted")
    require("instantaneous access" in by_id["G23"]["forbidden_regression"], "copresence signal guard absent")
    require(by_id["G24"]["active_use"] == "GEOMETRIC_REACHABILITY_ONLY", "causal access promoted")
    require(by_id["G25"]["active_use"] == "TYPE_GUARD_ONLY", "boundary type guard promoted")
    require("Xmax" in by_id["G25"]["forbidden_regression"], "Xmax/boundary guard absent")
    require(by_id["G26"]["active_use"] == "NO_CARRIER_EMERGENCE_CLAIM", "angular carrier promoted")
    require(by_id["G27"]["active_use"] == "NO_ORDER_SELECTED", "action/closure order selected")
    require(
        by_id["G28"]["current_status"]
        == "DERIVED_COMPLETE_ARROW_MODULATION_AND_GROUPOID_COCYCLE_HOME__UNIQUE_PHYSICAL_COCYCLE_OPEN",
        "complete-pair orchestra status regressed or promoted",
    )
    require(by_id["G28"]["epistemic_label"] == "DERIVED", "complete-pair orchestra label changed")
    require(by_id["G28"]["active_use"] == "ACTIVE_RELATIONAL_STRUCTURE", "complete-pair orchestra use changed")
    require("metric-natural physical cocycle selection" in by_id["G28"]["open_scope"], "physical cocycle open scope absent")
    require("angular sector held external" in by_id["G28"]["forbidden_regression"], "prior counterexample narrowing guard absent")
    require("stationary screen-modulated family promoted" in by_id["G28"]["forbidden_regression"], "stationary premise guard absent")
    require(
        by_id["G28"]["controlling_source"]
        == "udt_complete_pair_phi_orchestra_audit_2026-08-05/AUDIT_REPORT.md",
        "complete-pair orchestra source changed",
    )
    require(
        by_id["G29"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__THREE_INTERLEAVED_ANGULAR_LADDERS__OLD_SAME_INDEX_MULTIPLET_WINDOW_WITHDRAWN",
        "corrected FD1 status regressed or promoted",
    )
    require(by_id["G29"]["epistemic_label"] == "OBSERVED", "corrected FD1 label changed")
    require(
        by_id["G29"]["active_use"] == "CORRECTED_SCALAR_SLICE_BACKGROUND_GEOMETRY_ONLY",
        "corrected FD1 use promoted",
    )
    require("mode-family ownership" in by_id["G29"]["open_scope"], "FD1 mode-family gate absent")
    require(
        "old FD1 open compatibility window revived" in by_id["G29"]["forbidden_regression"],
        "old FD1 window revival guard absent",
    )
    require(
        "best standalone ladder postselected" in by_id["G29"]["forbidden_regression"],
        "FD1 postselection guard absent",
    )
    require(
        by_id["G29"]["controlling_source"]
        == "udt_fd1_corrected_full_spectral_atlas_2026-08-09/FINAL_REPORT.md",
        "corrected FD1 source changed",
    )
    require(
        by_id["G30"]["current_status"]
        == "DERIVED_CONDITIONAL_U1_MODE_DECOMPOSITION__FD1_ROOTS_DO_NOT_LIFT__PHYSICAL_COMPLETE_LIFT_AND_POPULATION_PROJECTION_OPEN",
        "complete-angular ownership status regressed or promoted",
    )
    require(by_id["G30"]["epistemic_label"] == "MIXED", "complete-angular ownership label changed")
    require(by_id["G30"]["active_use"] == "FULL_ANGULAR_REGRESSION_GATE_ONLY", "complete-angular ownership use promoted")
    require("physical complete angular screen" in by_id["G30"]["open_scope"], "complete-angular lift promoted")
    require("equatorial roots relabeled full-angular" in by_id["G30"]["forbidden_regression"], "full-angular relabel guard absent")
    require("symmetry projector promoted to population law" in by_id["G30"]["forbidden_regression"], "population projection guard absent")
    require(
        by_id["G30"]["controlling_source"]
        == "udt_cmb_complete_angular_mode_ownership_2026-08-09/AUDIT_REPORT.md",
        "complete-angular ownership source changed",
    )
    require(
        by_id["G31"]["current_status"]
        == "VERIFIED_DESIGN_MAP__GENERAL_STATIONARY_SCREEN_OPERATOR_DERIVED__PHYSICAL_SCREEN_AND_SOLVES_OPEN",
        "complete-angular family-map status regressed or promoted",
    )
    require(by_id["G31"]["epistemic_label"] == "MIXED", "complete-angular family-map label changed")
    require(by_id["G31"]["active_use"] == "ARCHITECTURE_AND_REGRESSION_GATE_ONLY", "family map promoted")
    require("physical complete angular screen" in by_id["G31"]["open_scope"], "physical screen promoted")
    require("axial shortcut applied" in by_id["G31"]["forbidden_regression"], "general-shift guard absent")
    require("C1 promoted to native screen" in by_id["G31"]["forbidden_regression"], "C1 promotion guard absent")
    require("FD2 called authorized" in by_id["G31"]["forbidden_regression"], "FD2 authorization guard absent")
    require(
        by_id["G31"]["controlling_source"]
        == "udt_cmb_complete_angular_family_atlas_map_2026-08-09/AUDIT_REPORT.md",
        "complete-angular family-map source changed",
    )
    require(
        by_id["G32"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__CONDITIONAL_C1_FIXED_ABS_M_PARITY_MATRIX_ARCHITECTURE__NO_EIGENSOLVE",
        "N01 coupling status regressed or promoted",
    )
    require(by_id["G32"]["epistemic_label"] == "MIXED", "N01 coupling label changed")
    require(
        by_id["G32"]["active_use"] == "BOUNDED_COUPLING_ARCHITECTURE_AND_REGRESSION_CONTROL_ONLY",
        "N01 coupling use promoted",
    )
    require("physical B(r)" in by_id["G32"]["open_scope"], "N01 physical profile promoted")
    require("negative m discarded" in by_id["G32"]["forbidden_regression"], "N01 sign guard absent")
    require("scalar Box_g promoted" in by_id["G32"]["forbidden_regression"], "N01 probe guard absent")
    require("FD2" in by_id["G32"]["forbidden_regression"], "N01 FD2 guard absent")
    require(
        by_id["G32"]["controlling_source"]
        == "udt_cmb_N01_C1_harmonic_coupling_matrix_atlas_2026-08-09/AUDIT_REPORT.md",
        "N01 coupling source changed",
    )
    require(
        by_id["G33"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__NO_BANKED_P1_REGULAR_COMPLETE_C1_C2_CENTER_TO_WALL_ANCHOR__NO_EIGENSOLVE",
        "N02 admissibility status regressed or promoted",
    )
    require(by_id["G33"]["epistemic_label"] == "MIXED", "N02 admissibility label changed")
    require(
        by_id["G33"]["active_use"] == "RADIAL_ADMISSIBILITY_AND_REGRESSION_GATE_ONLY",
        "N02 admissibility use promoted",
    )
    require("regular complete profile" in by_id["G33"]["open_scope"], "N02 regular profile promoted")
    require("P1 relational or SNe role called invalid" in by_id["G33"]["forbidden_regression"], "N02 P1 role guard absent")
    require("D or N called physically selected" in by_id["G33"]["forbidden_regression"], "N02 boundary guard absent")
    require("N02 eigensolve" in by_id["G33"]["forbidden_regression"], "N02 execution guard absent")
    require(
        by_id["G33"]["controlling_source"]
        == "udt_cmb_N02_radial_anchor_admissibility_2026-08-09/AUDIT_REPORT.md",
        "N02 admissibility source changed",
    )
    require(
        by_id["G34"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__NO_MAPPED_ROLE_CORRECT_COMPLETE_GLOBAL_PROFILE__REGULAR_C1_LOCAL_JETS_NONEMPTY__PHYSICAL_GROUPOID_COCYCLE_OPEN",
        "N03 profile-role status regressed or promoted",
    )
    require(by_id["G34"]["epistemic_label"] == "MIXED", "N03 profile-role label changed")
    require(
        by_id["G34"]["active_use"] == "PROFILE_ROLE_CENTER_REGULARITY_AND_REGRESSION_GATE_ONLY",
        "N03 profile-role use promoted",
    )
    require("metric-natural physical groupoid cocycle" in by_id["G34"]["open_scope"], "N03 cocycle selected")
    require("P1 observer-pair or SNe role called invalid" in by_id["G34"]["forbidden_regression"], "N03 P1 role guard absent")
    require("k0 called selected invariant" in by_id["G34"]["forbidden_regression"], "N03 k0 guard absent")
    require("transport or connection called derived" in by_id["G34"]["forbidden_regression"], "N03 transport guard absent")
    require("Xmax called a wall" in by_id["G34"]["forbidden_regression"], "N03 Xmax guard absent")
    require(
        by_id["G34"]["controlling_source"]
        == "udt_cmb_N03_profile_role_regular_center_map_2026-08-09/AUDIT_REPORT.md",
        "N03 profile-role source changed",
    )
    require(
        by_id["G35"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__ABSTRACT_RECIPROCAL_CALIBRATION_SEED_DERIVED__RECIPROCAL_ROOT_CONDITIONAL_UNIQUE_UNIVERSAL_ORDER_ZERO_READOUT__PHYSICAL_FLAG_ARROW_CALIBRATION_OPEN",
        "reciprocal-flag ownership status regressed or promoted",
    )
    require(by_id["G35"]["epistemic_label"] == "MIXED", "reciprocal-flag label changed")
    require(
        by_id["G35"]["active_use"] == "FOUNDATION_OWNERSHIP_AND_REGRESSION_GATE_ONLY",
        "reciprocal-flag result promoted",
    )
    require("pair-relative physical flag" in by_id["G35"]["open_scope"], "physical flag selected")
    require("physical comparison or calibration morphism" in by_id["G35"]["open_scope"], "physical arrow selected")
    require("timelike-strain eigenvalue called a general cocycle" in by_id["G35"]["forbidden_regression"], "strain cocycle guard absent")
    require("K called a causal Lorentz exchange" in by_id["G35"]["forbidden_regression"], "K type guard absent")
    require("arbitrary higher-jet nonmetric connection selected" in by_id["G35"]["forbidden_regression"], "connection-selection guard absent")
    require(
        by_id["G35"]["controlling_source"]
        == "udt_reciprocal_flag_foundation_ownership_audit_2026-08-09/AUDIT_REPORT.md",
        "reciprocal-flag ownership source changed",
    )
    require(
        by_id["G36"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__ABSTRACT_CALIBRATION_LINE_DERIVED__PAIR_FLAG_CONDITIONAL_REGULAR_QUERY__NO_NONZERO_ORDER_ZERO_OR_FIRST_METRIC_JET_NATURAL_SOLDER__STATIONARY_KILLING_SOLDER_CONDITIONAL__GENERAL_BILOCAL_GLOBAL_FUNCTOR_OPEN",
        "calibration-state solder status regressed or promoted",
    )
    require(by_id["G36"]["epistemic_label"] == "MIXED", "calibration-state solder label changed")
    require(
        by_id["G36"]["active_use"] == "LOCAL_SOLDER_NOGO_AND_GLOBAL_OWNER_ROUTING_GATE_ONLY",
        "calibration-state solder result promoted",
    )
    require("complete-branch calibration owner" in by_id["G36"]["open_scope"], "global owner selected")
    require("physical c_eff trivialization" in by_id["G36"]["open_scope"], "physical c_eff join selected")
    require("coordinate identity called physical" in by_id["G36"]["forbidden_regression"], "coordinate identity guard absent")
    require("stationary Killing ratio called universal" in by_id["G36"]["forbidden_regression"], "Killing branch promoted")
    require("scoped local no-go generalized to all geometry" in by_id["G36"]["forbidden_regression"], "no-go scope guard absent")
    require(
        by_id["G36"]["controlling_source"]
        == "udt_reciprocal_calibration_state_solder_audit_2026-08-09/AUDIT_REPORT.md",
        "calibration-state solder source changed",
    )
    require(
        by_id["G37"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__PAIR_METRIC_DECOMPOSITION_DERIVED_ON_SUPPLIED_REGULAR_A_CALIBRATED_PAIR_METRIC__PHI_UNIQUE_RECIPROCAL_LOG_IMBALANCE_WITHIN_FIXED_CALIBRATION__PHYSICAL_PAIR_MAP_CEFF_AND_CALIBRATION_OWNER_OPEN",
        "terminal pair-metric readout status regressed or promoted",
    )
    require(by_id["G37"]["epistemic_label"] == "MIXED", "terminal pair readout label changed")
    require(
        by_id["G37"]["active_use"] == "ACTIVE_TERMINAL_READOUT_AND_PAIR_MAP_ROUTING_GATE_ONLY",
        "terminal pair readout use promoted",
    )
    require("physical calibrated pair surface" in by_id["G37"]["open_scope"], "pair surface selected")
    require("physical calibration-state owner" in by_id["G37"]["open_scope"], "calibration owner selected")
    require("signed cocycle-type composition" in by_id["G37"]["open_scope"], "signed composition selected")
    require("universal mixed-geometry c_eff" in by_id["G37"]["open_scope"], "physical c_eff promoted")
    require("pair metric claimed derived from complete metric alone" in by_id["G37"]["forbidden_regression"], "pair-map type guard absent")
    require("calibration state called eliminated" in by_id["G37"]["forbidden_regression"], "calibration-state guard absent")
    require("signed cocycle requirement withdrawn" in by_id["G37"]["forbidden_regression"], "signed-cocycle guard absent")
    require(
        by_id["G37"]["controlling_source"]
        == "udt_terminal_reciprocal_ce_positional_derivation_2026-08-09/AUDIT_REPORT.md",
        "terminal pair-metric readout source changed",
    )
    require(
        by_id["G38"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__LOCAL_ORTHOGONAL_EXPONENTIAL_TUBE_DERIVED_FROM_METRIC_AND_FULL_DECLARED_QUERY__NO_UNIQUE_UNIVERSAL_PAIR_MAP_FROM_BARE_ENDPOINTS__PHYSICAL_CALIBRATED_PAIR_RELATION_FUNCTOR_OPEN",
        "pair-map owner atlas status changed",
    )
    require(by_id["G38"]["epistemic_label"] == "MIXED", "pair-map atlas label changed")
    require(
        by_id["G38"]["active_use"]
        == "ACTIVE_PAIR_MAP_OWNERSHIP_AND_NEXT_FUNCTOR_ROUTING_GATE_ONLY",
        "pair-map atlas use changed",
    )
    require("event pairing" in by_id["G38"]["open_scope"], "event pairing selected")
    require("middle calibration-state update" in by_id["G38"]["open_scope"], "middle update selected")
    require("branch-labelled global relation" in by_id["G38"]["open_scope"], "global branch selected")
    require("local exponential tube called universally selected" in by_id["G38"]["forbidden_regression"], "local-to-global guard absent")
    require("Killing norm called terminal pair depth without TL=1" in by_id["G38"]["forbidden_regression"], "stationary join guard absent")
    require("reciprocal reset called common-scale gauge" in by_id["G38"]["forbidden_regression"], "reset guard absent")
    require(
        by_id["G38"]["controlling_source"]
        == "udt_calibrated_pair_map_owner_atlas_2026-08-09/AUDIT_REPORT.md",
        "pair-map owner atlas source changed",
    )
    require(
        by_id["G39"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__FOUNDED_ORDERED_DEPTH_CHARACTER_DERIVED__COMPLETE_CALIBRATED_QUERY_CONDITIONAL_LOCAL_ENRICHMENT__CE_CALIBRATION_NOT_RELATION_SELECTOR__ASSOCIATIVE_MIDDLE_CARRY_OPEN",
        "founding pair-relation ownership status changed",
    )
    require(by_id["G39"]["epistemic_label"] == "MIXED", "pair-relation ownership label changed")
    require(
        by_id["G39"]["active_use"]
        == "ACTIVE_QUERY_OWNERSHIP_AND_THREE_OBSERVER_OVERLAP_ROUTING_GATE_ONLY",
        "pair-relation ownership use changed",
    )
    require("associative calibration carry" in by_id["G39"]["open_scope"], "middle carry promoted")
    require("triple-overlap and loop obstruction" in by_id["G39"]["open_scope"], "overlap gate absent")
    require("ordering called a unique physical arrow" in by_id["G39"]["forbidden_regression"], "ordered-pair guard absent")
    require("c_E called a simultaneity path or branch selector" in by_id["G39"]["forbidden_regression"], "c_E selector guard absent")
    require("Reciprocity called an existence or uniqueness theorem" in by_id["G39"]["forbidden_regression"], "Reciprocity selector guard absent")
    require(
        by_id["G39"]["controlling_source"]
        == "udt_founding_pair_relation_functor_ownership_audit_2026-08-09/AUDIT_REPORT.md",
        "pair-relation ownership source changed",
    )
    require(
        by_id["G40"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__CARRY_ASSOCIATIVITY_DERIVED_ON_MATCHED_ENRICHED_OBJECTS__DIRECT_EQUALS_COMPOSITE_IS_CECH_DESCENT_OR_PATH_INDEPENDENCE__TRIANGLE_LOOP_OBSTRUCTION_TYPED__PHYSICAL_GLOBAL_RELATION_FAMILY_AND_SCALAR_REDUCTION_OPEN",
        "three-observer overlap status regressed or promoted",
    )
    require(by_id["G40"]["epistemic_label"] == "MIXED", "three-observer overlap label changed")
    require(
        by_id["G40"]["active_use"]
        == "ACTIVE_OVERLAP_TYPE_AND_GLOBAL_RELATION_FAMILY_ROUTING_GATE_ONLY",
        "three-observer overlap use promoted",
    )
    require("global relation-family type" in by_id["G40"]["open_scope"], "global family selected")
    require("reciprocal scalar reduction" in by_id["G40"]["open_scope"], "scalar reduction selected")
    require("associativity conflated with path independence" in by_id["G40"]["forbidden_regression"], "associativity type guard absent")
    require("M_B set to identity" in by_id["G40"]["forbidden_regression"], "middle-transition guard absent")
    require("atlas called fully independently re-derived" in by_id["G40"]["forbidden_regression"], "independent-scope guard absent")
    require(
        by_id["G40"]["controlling_source"]
        == "udt_three_observer_overlap_calibration_carry_audit_2026-08-10/AUDIT_REPORT.md",
        "three-observer overlap source changed",
    )
    require("G40_OPERATIONALLY_REFINES_G39" in by_id["G40"]["precedence_rule"], "G39 refinement absent")
    require(
        by_id["G41"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__24_IDENTITIES_57_ALIASES__PATH_HOLONOMY_ENDPOINT_CLOCK_AND_STRATIFIED_SET_VALUED_GEOMETRIC_FAMILIES_SURVIVE__PHYSICAL_NONISOMETRIC_PAIR_FUNCTOR_AND_SCALAR_REDUCTION_OPEN",
        "global relation-family branch status regressed or promoted",
    )
    require(by_id["G41"]["epistemic_label"] == "MIXED", "global family classification label changed")
    require(
        by_id["G41"]["active_use"]
        == "ACTIVE_COMPLETE_BRANCH_FAMILY_CLASSIFICATION_AND_ROUTING_GATE_ONLY",
        "global family classification use promoted",
    )
    require("branch-derived non-isometric calibration transition" in by_id["G41"]["open_scope"], "non-isometric transition selected")
    require("mixed scalar reciprocal character" in by_id["G41"]["open_scope"], "mixed scalar selected")
    require("geometric Levi-Civita path groupoid called physical depth" in by_id["G41"]["forbidden_regression"], "path/depth guard absent")
    require("W02 clock coboundary called complete pair without TL=1" in by_id["G41"]["forbidden_regression"], "clock-only scope guard absent")
    require("toric projector set called calibrated pair arrow" in by_id["G41"]["forbidden_regression"], "toric type guard absent")
    require(
        by_id["G41"]["controlling_source"]
        == "udt_global_relation_family_branch_classification_2026-08-10/AUDIT_REPORT.md",
        "global family classification source changed",
    )
    require("G41_REFINES_G40_GLOBAL_FAMILY_TYPE" in by_id["G41"]["precedence_rule"], "G40 refinement absent")
    require(
        by_id["G42"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__R17_SEMIDIRECT_FORMULA_EXACT_ON_MATCHED_PATH_CARRIED_STATES__CONDITIONAL_ASSEMBLY_NOT_BRANCH_OWNED__ZERO_BRANCH_OWNED_COMPLETE_TRANSITIONS",
        "branch-transition ownership correction regressed or promoted",
    )
    require(by_id["G42"]["epistemic_label"] == "MIXED", "branch-transition label changed")
    require(
        by_id["G42"]["active_use"]
        == "ACTIVE_BRANCH_TRANSITION_OWNERSHIP_CORRECTION_AND_NEXT_MIDDLE_MORPHISM_GATE_ONLY",
        "branch-transition use promoted",
    )
    require("carried-to-rebuilt middle morphism M_B" in by_id["G42"]["open_scope"], "M_B selected")
    require("pair-surface integrability" in by_id["G42"]["open_scope"], "pair surface selected")
    require("R17 semidirect assembly called branch-owned" in by_id["G42"]["forbidden_regression"], "R17 ownership guard absent")
    require("M_B set to identity" in by_id["G42"]["forbidden_regression"], "G42 middle-transition guard absent")
    require("terminal carried-flag equality called universal mixed-geometry c_eff" in by_id["G42"]["forbidden_regression"], "G42 c_eff guard absent")
    require(
        by_id["G42"]["controlling_source"]
        == "udt_branch_nonisometric_calibration_transition_audit_2026-08-10/AUDIT_REPORT.md",
        "branch-transition source changed",
    )
    require("G42_REFINES_G41_TRANSITION_OWNERSHIP" in by_id["G42"]["precedence_rule"], "G41 transition refinement absent")
    require(
        by_id["G43"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__REGULAR_C01_C06_PROJECTOR_ALIGNMENTS_FORM_PATH_LABELLED_SO2_BITORSORS__BALANCED_REPRESENTATIVE_FREE_COMPOSITION_EXACT__NO_SCREEN_PHASE_SELECTED__CALIBRATION_AND_SCALAR_DESCENT_OPEN",
        "middle-morphism ownership status regressed or promoted",
    )
    require(by_id["G43"]["epistemic_label"] == "MIXED", "middle-morphism label changed")
    require(
        by_id["G43"]["active_use"]
        == "ACTIVE_PROJECTOR_ALIGNMENT_GAUGE_GROUPOID_AND_NEXT_SCALAR_CALIBRATION_DESCENT_GATE_ONLY",
        "middle-morphism use promoted",
    )
    require("calibration-density descent" in by_id["G43"]["open_scope"], "calibration descent selected")
    require("terminal reciprocal scalar descent" in by_id["G43"]["open_scope"], "scalar descent selected")
    require("double-coset shadow called a group" in by_id["G43"]["forbidden_regression"], "double-coset guard absent")
    require("path labels or holonomy erased" in by_id["G43"]["forbidden_regression"], "path-label guard absent")
    require("projector alignment called calibration-density alignment" in by_id["G43"]["forbidden_regression"], "calibration-promotion guard absent")
    require(
        by_id["G43"]["controlling_source"]
        == "udt_carried_intrinsic_middle_morphism_ownership_audit_2026-08-10/AUDIT_REPORT.md",
        "middle-morphism controlling source changed",
    )
    require("G43_REFINES_G42_MIDDLE_MORPHISM" in by_id["G43"]["precedence_rule"], "G42 middle-morphism refinement absent")
    require(
        by_id["G44"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__SUPPLIED_RECIPROCAL_READOUTS_DESCEND_THROUGH_REGULAR_C01_C06_SO2_ALIGNMENT_BITORSORS__BALANCED_DENSITY_TELESCOPING_EXACT__ISOMETRIC_ALIGNMENT_GENERATES_ZERO_CALIBRATION__PHYSICAL_NONISOMETRIC_MAGNITUDE_OWNER_OPEN",
        "reciprocal scalar descent status regressed or promoted",
    )
    require(by_id["G44"]["epistemic_label"] == "MIXED", "reciprocal scalar descent label changed")
    require(
        by_id["G44"]["active_use"]
        == "ACTIVE_SCALAR_DESCENT_CORRECTION_AND_NEXT_NONISOMETRIC_CALIBRATION_OWNER_GATE_ONLY",
        "reciprocal scalar descent use promoted",
    )
    require("physical non-isometric calibration magnitude and its owner" in by_id["G44"]["open_scope"], "calibration owner selected")
    require("selection of delta_RF or R17 as the physical law" in by_id["G44"]["open_scope"], "conditional readout selected")
    require("terminal determinant formula used without normalized source calibration" in by_id["G44"]["forbidden_regression"], "source-normalization guard absent")
    require("isometric alignment called a nonzero magnitude generator" in by_id["G44"]["forbidden_regression"], "zero-generation guard absent")
    require("path labels or holonomy erased" in by_id["G44"]["forbidden_regression"], "G44 path-label guard absent")
    require(
        by_id["G44"]["controlling_source"]
        == "udt_reciprocal_scalar_calibration_bitorsor_descent_audit_2026-08-10/AUDIT_REPORT.md",
        "reciprocal scalar descent source changed",
    )
    require("G44_REFINES_G43_BY_DERIVING_SCREEN_GAUGE_DESCENT" in by_id["G44"]["precedence_rule"], "G43 scalar-descent refinement absent")
    require(
        by_id["G45"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__R17_R18_OWN_BRANCH_CONDITIONAL_ENDPOINT_CLOCK_MAGNITUDES__ZERO_COMPLETE_PHYSICAL_MAGNITUDE_OWNERS__R17_RECIPROCAL_LIFT_SELECTION_AND_R18_RULER_COMPLETION_OPEN",
        "magnitude-owner status regressed or promoted",
    )
    require(by_id["G45"]["epistemic_label"] == "MIXED", "magnitude-owner label changed")
    require(
        by_id["G45"]["active_use"]
        == "ACTIVE_BRANCH_CONDITIONAL_MAGNITUDE_OWNER_CORRECTION_AND_NEXT_R17_MAGNITUDE_TO_GRADING_SELECTION_GATE_ONLY",
        "magnitude-owner use promoted",
    )
    require("R17 selection of the non-isometric reciprocal lift" in by_id["G45"]["open_scope"], "R17 lift selected")
    require("R18 intrinsic ruler scale" in by_id["G45"]["open_scope"], "R18 ruler completion selected")
    require("native dynamical or bootstrap calibration return" in by_id["G45"]["open_scope"], "bootstrap return invented")
    require("R17 delta_K ownership confused with semidirect assembly ownership" in by_id["G45"]["forbidden_regression"], "R17 type guard absent")
    require("R18 clock magnitude called a complete reciprocal law" in by_id["G45"]["forbidden_regression"], "R18 completion guard absent")
    require("bounded 24x5 negative generalized to all metrics" in by_id["G45"]["forbidden_regression"], "bounded-scope guard absent")
    require(
        by_id["G45"]["controlling_source"]
        == "udt_nonisometric_calibration_magnitude_owner_audit_2026-08-10/AUDIT_REPORT.md",
        "magnitude-owner source changed",
    )
    require("G45_REFINES_G44_BY_LOCATING_TWO_BRANCH_CONDITIONAL_CLOCK_MAGNITUDES" in by_id["G45"]["precedence_rule"], "G44 magnitude-owner refinement absent")
    require(
        by_id["G46"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__FOUNDED_NONZERO_DEPTH_FIXES_CLOCK_RULER_WEIGHTS__SUPPLIED_COMPLETE_C01_C06_COFRAME_FIXES_VERTICAL_RECIPROCAL_METRIC_CLASS_MOD_SO2__FULL_PHYSICAL_ARROW_OPEN",
        "R17 magnitude-to-grading result regressed or promoted",
    )
    require(by_id["G46"]["epistemic_label"] == "MIXED", "R17 selector label changed")
    require(
        by_id["G46"]["active_use"]
        == "ACTIVE_COMPLETE_COFRAME_CONDITIONAL_VERTICAL_METRIC_CLASS_AND_NEXT_R17_INTEGRABILITY_PAIR_SURFACE_GATE_ONLY",
        "R17 selector use promoted",
    )
    require("metric-owned R17 integrability or relation-family condition" in by_id["G46"]["open_scope"], "R17 integrability invented")
    require("physical pair-surface family" in by_id["G46"]["open_scope"], "R17 pair surface selected")
    require("R17 branch and lambda selection" in by_id["G46"]["open_scope"], "R17 branch or lambda selected")
    require("pair-only Reciprocity said to fix the screen" in by_id["G46"]["forbidden_regression"], "pair-only screen guard absent")
    require("vertical metric factor called the complete physical arrow" in by_id["G46"]["forbidden_regression"], "vertical/full-arrow type guard absent")
    require("G42 demotion reversed" in by_id["G46"]["forbidden_regression"], "G42 precedence guard absent")
    require(
        by_id["G46"]["controlling_source"]
        == "udt_r17_magnitude_to_grading_selection_audit_2026-08-10/AUDIT_REPORT.md",
        "R17 selector source changed",
    )
    require("G46_REFINES_G45_BY_FIXING_THE_COMPLETE_COFRAME_CONDITIONAL_VERTICAL_METRIC_CLASS_MOD_SO2" in by_id["G46"]["precedence_rule"], "G45 R17 selector refinement absent")
    require(
        by_id["G47"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__GLOBAL_R_X_S1_INTRINSIC_PAIR_FOLIATION_ON_SUPPLIED_C01_C06__LEAF_METRIC_DET_MINUS1_AND_TERMINAL_PHI__4D_SCREEN_NONINTEGRABLE_NORMAL_BUNDLE__FULL_NORMAL_CARRY_AND_PHYSICAL_ARROW_OPEN",
        "R17 pair-foliation status regressed or promoted",
    )
    require(by_id["G47"]["epistemic_label"] == "MIXED", "R17 pair-foliation label changed")
    require(
        by_id["G47"]["active_use"]
        == "ACTIVE_R17_PAIR_SURFACE_CLOSURE_AND_NEXT_NORMAL_BUNDLE_HOLONOMY_GATE_ONLY",
        "R17 pair-foliation use promoted",
    )
    require("cross-leaf common pair surface" in by_id["G47"]["open_scope"], "cross-leaf surface selected")
    require("normal-bundle connection carry and holonomy" in by_id["G47"]["open_scope"], "normal carry promoted")
    require("four-dimensional normal bundle called a literal contact structure" in by_id["G47"]["forbidden_regression"], "4D contact type guard absent")
    require("endpoint scalar called a common cross-leaf pair surface" in by_id["G47"]["forbidden_regression"], "same-leaf depth promotion guard absent")
    require(
        by_id["G47"]["controlling_source"]
        == "udt_r17_intrinsic_pair_foliation_integrability_audit_2026-08-10/AUDIT_REPORT.md",
        "R17 pair-foliation source changed",
    )
    require("G47_REFINES_G46_BY_CLOSING_THE_SUPPLIED_R17_PAIR_FOLIATION_AND_LEAF_DEPTH" in by_id["G47"]["precedence_rule"], "G46 pair-foliation refinement absent")
    require(
        by_id["G48"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__METRIC_PROJECTED_NORMAL_CONNECTION_AND_LEAF_CURVATURE_DERIVED_ON_SUPPLIED_C01_C06__LAMBDA_MINUS_ONE_FLAT_AND_LAMBDA_ZERO_HOPF_BASIC_ROLES_DISTINCT__PHYSICAL_PATH_AND_COMPLETE_ARROW_OPEN",
        "R17 normal-holonomy status regressed or promoted",
    )
    require(by_id["G48"]["epistemic_label"] == "MIXED", "R17 normal-holonomy label changed")
    require(
        by_id["G48"]["active_use"]
        == "ACTIVE_R17_NORMAL_HOLONOMY_CLASSIFICATION_AND_NEXT_GLOBAL_CONNECTION_DECOMPOSITION_GATE_ONLY",
        "R17 normal-holonomy use promoted",
    )
    require("physical cross-leaf base path" in by_id["G48"]["open_scope"], "cross-leaf path selected")
    require("vertical horizontal and mixed curvature decomposition" in by_id["G48"]["open_scope"], "global connection decomposition invented")
    require("lambda minus one flatness called branch selection" in by_id["G48"]["forbidden_regression"], "flat-branch selection guard absent")
    require("lambda zero Hopf-basicness called branch selection" in by_id["G48"]["forbidden_regression"], "Hopf-basic branch-selection guard absent")
    require("wound holonomy erased because curvature is zero" in by_id["G48"]["forbidden_regression"], "winding holonomy guard absent")
    require("horizontal lift said to select a base path" in by_id["G48"]["forbidden_regression"], "horizontal-lift ownership guard absent")
    require(
        by_id["G48"]["controlling_source"]
        == "udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/AUDIT_REPORT.md",
        "R17 normal-holonomy source changed",
    )
    require("G48_REFINES_G47_BY_DERIVING_THE_SUPPLIED_R17_PAIR_LEAF_NORMAL_CONNECTION_AND_HOLONOMY_CLASSIFICATION" in by_id["G48"]["precedence_rule"], "G47 normal-holonomy refinement absent")
    require(
        by_id["G49"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__COMPLETE_METRIC_PROJECTED_H_CONNECTION_AND_PATH_FUNCTOR_ON_SUPPLIED_REGULAR_STATIONARY_R17__FULL_CURVATURE_GENERALLY_NONZERO__PATH_SELECTION_AND_PHYSICAL_ARROW_OPEN",
        "R17 complete path-connection status regressed or promoted",
    )
    require(by_id["G49"]["epistemic_label"] == "MIXED", "R17 complete path-connection label changed")
    require(
        by_id["G49"]["active_use"]
        == "ACTIVE_R17_COMPLETE_PATH_CONNECTION_CLASSIFICATION_AND_NEXT_SUBLOCUS_OWNERSHIP_GATE_ONLY",
        "R17 complete path-connection use promoted",
    )
    require("flat base-basic or reduced-holonomy compatible stationary jet subloci" in by_id["G49"]["open_scope"], "R17 sublocus classification invented")
    require("physical path and non-isometric observer arrow" in by_id["G49"]["open_scope"], "physical observer arrow promoted")
    require("lambda minus one called completely flat" in by_id["G49"]["forbidden_regression"], "complete-flatness guard absent")
    require("lambda zero called a descended base connection" in by_id["G49"]["forbidden_regression"], "base-descent guard absent")
    require("isometric normal carry called physical non-isometric observer arrow" in by_id["G49"]["forbidden_regression"], "isometric/non-isometric guard absent")
    require(
        by_id["G49"]["controlling_source"]
        == "udt_r17_path_labelled_connection_decomposition_audit_2026-08-10/AUDIT_REPORT.md",
        "R17 complete path-connection source changed",
    )
    require("G49_REFINES_G48_BY_DERIVING_THE_COMPLETE_PROJECTED_NORMAL_CONNECTION_ALL_SIX_CURVATURE_PLANES_AND_SUPPLIED_PATH_FUNCTOR" in by_id["G49"]["precedence_rule"], "G48 complete path-connection refinement absent")
    require(
        by_id["G50"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__GLOBAL_CURVATURE_HORIZONTALITY_IFF_CONSTANT_PHI__FLAT_AND_ABSTRACT_DESCENT_LOCI_EXPLICIT__NO_REGULAR_CANONICAL_HOPF_TANGENT_DESCENT__COMPLETE_HOLONOMY_TRIVIAL_OR_SO2__MANIFEST_BACKED_R17_SOURCES_SELECT_NONE",
        "R17 stationary sublocus status regressed or promoted",
    )
    require(by_id["G50"]["epistemic_label"] == "MIXED", "R17 stationary sublocus label changed")
    require(
        by_id["G50"]["active_use"]
        == "ACTIVE_STATIONARY_SUBLOCUS_CLASSIFICATION_AND_NEXT_GENERIC_JOINT_INVARIANT_GATE_ONLY",
        "R17 stationary sublocus use promoted",
    )
    require("generic full-SO2 joint invariant" in by_id["G50"]["open_scope"], "generic joint invariant selected")
    require("repo-wide independent selector exhaustion" in by_id["G50"]["open_scope"], "ownership scope widened")
    require("flat or integer-descent locus called physically selected" in by_id["G50"]["forbidden_regression"], "special-locus selection guard absent")
    require("supporting local census called independently reviewed authority" in by_id["G50"]["forbidden_regression"], "external-review fence guard absent")
    require("full SO2 carry erased" in by_id["G50"]["forbidden_regression"], "generic holonomy guard absent")
    require(
        by_id["G50"]["controlling_source"]
        == "udt_r17_stationary_connection_sublocus_ownership_audit_2026-08-10/AUDIT_REPORT.md",
        "R17 stationary sublocus source changed",
    )
    require("G50_REFINES_G49_BY_CLASSIFYING_ALL_STATIONARY_SPECIAL_SUBLOCI" in by_id["G50"]["precedence_rule"], "G49 stationary sublocus refinement absent")
    require(
        by_id["G51"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__ENDPOINT_DEPTH_AND_NORMAL_ISOMETRY_FORM_EXACT_PRODUCT_GROUPOID__COMPLETE_COFRAME_FIXES_SCREEN_CO2_WEIGHTS_BY_VARIANCE__UNIQUE_NORMALIZED_CONTINUOUS_REAL_ORDER_ZERO_CHARACTER_IS_DELTA_K__LOOP_AND_RELATIVE_PATH_HOLONOMY_SURVIVE__PHYSICAL_PATH_ARROW_AND_STATIONARY_HIGHER_JET_SELECTION_OPEN",
        "R17 depth/holonomy joint status regressed or promoted",
    )
    require(by_id["G51"]["epistemic_label"] == "MIXED", "R17 joint-invariant label changed")
    require(
        by_id["G51"]["active_use"]
        == "ACTIVE_R17_JOINT_KINEMATIC_CLASSIFICATION_AND_NEXT_NATIVE_ONE_FORM_SELECTION_GATE_ONLY",
        "R17 joint-invariant use promoted",
    )
    require("stationary R17-owned endpoint-frame-invariant non-exact scalar one-form" in by_id["G51"]["open_scope"], "stationary higher-jet owner promoted")
    require("physical path or query" in by_id["G51"]["open_scope"], "physical path selected")
    require("global normal carry called one fixed SO2 matrix group" in by_id["G51"]["forbidden_regression"], "global groupoid type guard absent")
    require("general rectangle control called an R17 solution witness" in by_id["G51"]["forbidden_regression"], "higher-jet scope guard absent")
    require("screen CO2 representation called the physical observer arrow" in by_id["G51"]["forbidden_regression"], "screen/full-arrow guard absent")
    require(
        by_id["G51"]["controlling_source"]
        == "udt_r17_depth_holonomy_joint_invariant_audit_2026-08-10/AUDIT_REPORT.md",
        "R17 joint-invariant source changed",
    )
    require("G51_REFINES_G50_BY_DERIVING_THE_TYPED_DEPTH_NORMAL_ISOMETRY_PRODUCT_GROUPOID" in by_id["G51"]["precedence_rule"], "G50 joint-invariant refinement absent")
    require(
        by_id["G52"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__CANONICAL_LOCAL_FORMS_BEYOND_dphi_AND_GENERIC_FIRST_JET_FULL_COTANGENT_DERIVED__CONSTRUCTIVE_NONUNIQUENESS_ONLY__NONCLOSED_PAIR_LEAF_AND_EXACT_PAIR_PURE_FAMILIES_SURVIVE__NO_DISTINGUISHED_ADDITIONAL_RECIPROCAL_TRANSGRESSION_SELECTED",
        "R17 stationary local one-form status regressed or promoted",
    )
    require(by_id["G52"]["epistemic_label"] == "MIXED", "R17 one-form label changed")
    require(
        by_id["G52"]["active_use"]
        == "ACTIVE_STATIONARY_R17_LOCAL_ONE_FORM_NONSELECTION_AND_NEXT_FOUNDING_QUERY_MEASUREMENT_SELECTOR_GATE_ONLY",
        "R17 one-form use promoted",
    )
    require("explicit physical query or measurement selection rule" in by_id["G52"]["open_scope"], "query selector invented")
    require("exhaustive higher-jet classification" in by_id["G52"]["open_scope"], "constructive scope widened")
    require("constructive families called an exhaustive finite-jet classification" in by_id["G52"]["forbidden_regression"], "constructive scope guard absent")
    require("metric-owned form called selected physical transgression" in by_id["G52"]["forbidden_regression"], "ownership/selection guard absent")
    require("line-integral composition or path independence called a coefficient selector" in by_id["G52"]["forbidden_regression"], "composition selection guard absent")
    require(
        by_id["G52"]["controlling_source"]
        == "udt_r17_stationary_local_one_form_selection_audit_2026-08-10/AUDIT_REPORT.md",
        "R17 stationary local one-form source changed",
    )
    require("G52_REFINES_G51_BY_DERIVING_MULTIPLE_STATIONARY_R17_LOCAL_FORMS" in by_id["G52"]["precedence_rule"], "G51 local one-form refinement absent")
    require(
        by_id["G53"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__REGULAR_CALIBRATED_PAIR_METRIC_HAS_UNIQUE_KAPPA_PHI_BETA_STATE_COORDINATES__MATCHED_DELTA_KAPPA_AND_DELTA_PHI_ADD__ANGULAR_U_PATH_CHANNEL_DISTINCT__CONDITIONAL_MINIMAL_BANKED_ASSEMBLY__PHYSICAL_QUERY_PROJECTION_PATH_REGIME_AND_CONDUCTOR_OPEN",
        "multi-channel assembly status regressed or promoted",
    )
    require(by_id["G53"]["epistemic_label"] == "MIXED", "multi-channel assembly label changed")
    require(
        by_id["G53"]["active_use"]
        == "ACTIVE_CONDITIONAL_MULTICHANNEL_ASSEMBLY_AND_NEXT_ORDERED_QUERY_PROJECTION_OWNERSHIP_GATE_ONLY",
        "multi-channel assembly use promoted",
    )
    require("physical ordered-query projection or measurement rule" in by_id["G53"]["open_scope"], "query projection owner invented")
    require("physical pair map and path" in by_id["G53"]["open_scope"], "physical pair map/path promoted")
    require("physical regime map" in by_id["G53"]["open_scope"], "physical regime map invented")
    require("on-shell or global bootstrap conductor" in by_id["G53"]["open_scope"], "conductor invented")
    require("conditional state assembly called a selected physical observer arrow" in by_id["G53"]["forbidden_regression"], "conditional/physical-arrow guard absent")
    require("kappa deleted by strong CSN or calibration cancellation" in by_id["G53"]["forbidden_regression"], "common-scale retention guard absent")
    require("beta called a standalone additive character" in by_id["G53"]["forbidden_regression"], "shift state/arrow guard absent")
    require("U_gamma scalarized or path labels erased" in by_id["G53"]["forbidden_regression"], "angular path guard absent")
    require("bounded minimality widened to full metric reconstruction" in by_id["G53"]["forbidden_regression"], "minimality scope guard absent")
    require(
        by_id["G53"]["controlling_source"]
        == "udt_multichannel_observer_relation_assembly_audit_2026-08-10/AUDIT_REPORT.md",
        "multi-channel assembly source changed",
    )
    require("G53_REFINES_G52_BY_REPLACING_THE_ONE_SCALAR_SEARCH_WITH_A_BOUNDED_TYPED_MULTICHANNEL_ASSEMBLY" in by_id["G53"]["precedence_rule"], "G52 multi-channel refinement absent")
    require(
        by_id["G54"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__AFTER_COMPLETE_CALIBRATED_QUERY_SUPPLIES_REGULAR_PAIR_RELATION_REALIZED_FOUNDING_RECIPROCAL_PROJECTION_IS_UNIQUELY_DELTA_PHI_WITHIN_CONTINUOUS_MATCHED_TWO_DENSITY_CHARACTERS__BROADER_MEASUREMENTS_AND_PAIR_OWNER_OPEN",
        "ordered-query projection status regressed or promoted",
    )
    require(by_id["G54"]["epistemic_label"] == "MIXED", "ordered-query projection label changed")
    require(
        by_id["G54"]["active_use"]
        == "ACTIVE_CONDITIONAL_RECIPROCAL_PROJECTION_AND_NEXT_PAIR_RELATION_OR_MEASUREMENT_OWNER_GATE_ONLY",
        "ordered-query projection use promoted",
    )
    require("calibrated physical observer-query and pair-relation selector" in by_id["G54"]["open_scope"], "pair-relation owner invented")
    require("physical path" in by_id["G54"]["open_scope"], "physical path promoted")
    require("bare observer endpoints said to select Delta_phi" in by_id["G54"]["forbidden_regression"], "bare-endpoint selection guard absent")
    require("uniqueness widened beyond continuous two-density characters" in by_id["G54"]["forbidden_regression"], "conditional uniqueness scope guard absent")
    require("endpoint coboundaries called impossible" in by_id["G54"]["forbidden_regression"], "coboundary survival guard absent")
    require("kappa deleted" in by_id["G54"]["forbidden_regression"], "common-scale retention guard absent")
    require("phi orchestra reduced to pure block" in by_id["G54"]["forbidden_regression"], "phi-orchestra upstream guard absent")
    require(
        by_id["G54"]["controlling_source"]
        == "udt_ordered_observer_query_projection_ownership_audit_2026-08-10/AUDIT_REPORT.md",
        "ordered-query projection source changed",
    )
    require("G54_REFINES_G53_BY_SELECTING_DELTA_PHI_ONLY_AS_THE_CONDITIONAL_REALIZATION_OF_THE_FOUNDED_RECIPROCAL_PROJECTION" in by_id["G54"]["precedence_rule"], "G53 ordered-query projection refinement absent")
    require(
        by_id["G55"]["current_status"]
        == "VERIFIED_WITH_CORRECTIONS__24_BY_6_BRANCH_MEASUREMENT_ATLAS__11_MATHEMATICAL_APPARATUS_PATTERNS__FIVE_RESTRICTED_GLOBAL_RELATION_TYPES__R17_ONLY_FULL_PANEL_CONDITIONAL__ZERO_PHYSICAL_PAIR_ARROW_SELECTOR_OR_REGIME_OWNERS",
        "multi-regime admissibility status regressed or promoted",
    )
    require(by_id["G55"]["epistemic_label"] == "MIXED", "multi-regime admissibility label changed")
    require(
        by_id["G55"]["active_use"]
        == "ACTIVE_BRANCH_DEPENDENT_APPARATUS_AVAILABILITY_MAP_AND_NEXT_ON_SHELL_GLOBAL_DESCENT_BOOTSTRAP_OR_PREMISE_DECISION_GATE_ONLY",
        "multi-regime admissibility use promoted",
    )
    require("time-live or on-shell realized branch/query selection" in by_id["G55"]["open_scope"], "on-shell owner invented")
    require("global descent selecting pair surfaces or middle resets" in by_id["G55"]["open_scope"], "global descent invented")
    require("bootstrap closure correlating background completion with local admissibility" in by_id["G55"]["open_scope"], "bootstrap closure invented")
    require("R04 aggregate said to inherit one member's instrument panel" in by_id["G55"]["forbidden_regression"], "R04 aggregate guard absent")
    require("mathematical apparatus patterns called physical micro ordinary or cosmological regimes" in by_id["G55"]["forbidden_regression"], "physical regime guard absent")
    require("pinned static-corpus workflow exhaustion called a theorem about all static geometry" in by_id["G55"]["forbidden_regression"], "static no-go scope guard absent")
    require(
        by_id["G55"]["controlling_source"]
        == "udt_multiregime_pair_relation_admissibility_audit_2026-08-10/AUDIT_REPORT.md",
        "multi-regime admissibility source changed",
    )
    require("G55_REFINES_G54_BY_MAPPING_THE_COMPLETE_PINNED_24_BRANCH_CORPUS" in by_id["G55"]["precedence_rule"], "G54 multi-regime refinement absent")
    require(
        by_id["G56"]["current_status"]
        == "VERIFIED_WITH_CORRECTIONS__24_BY_10_GLOBAL_DESCENT_ATLAS__R17_GLOBAL_PAIR_FOLIATION_PATH_FUNCTOR_AND_SO2_ALIGNMENT_BITORSOR_OWNED__R18_CLOCK_ONLY_ENDPOINT_DESCENT_OWNED__CALIBRATION_RESET_PAIR_QUERY_AND_COMPLETE_SELECTOR_OPEN",
        "global descent status regressed or promoted",
    )
    require(by_id["G56"]["epistemic_label"] == "MIXED", "global descent label changed")
    require(
        by_id["G56"]["active_use"]
        == "ACTIVE_BOUNDED_GLOBAL_DESCENT_OWNERSHIP_MAP_AND_NEXT_NATIVE_ON_SHELL_OR_TIME_LIVE_EQUATION_OWNERSHIP_GATE_ONLY",
        "global descent use promoted",
    )
    require("R17 calibration-bearing representative and scalar reset" in by_id["G56"]["open_scope"], "R17 calibration reset invented")
    require("physical pair leaf path winding and query selector" in by_id["G56"]["open_scope"], "physical pair query invented")
    require("native on-shell or time-live equation" in by_id["G56"]["open_scope"], "native evolution equation invented")
    require("SO2 alignment bitorsor called one selected calibration representative" in by_id["G56"]["forbidden_regression"], "bitorsor/representative guard absent")
    require("R18 clock-only chain silently spliced into R17" in by_id["G56"]["forbidden_regression"], "R17/R18 splice guard absent")
    require("no complete selector in pinned corpus called a universal no-go" in by_id["G56"]["forbidden_regression"], "bounded no-go guard absent")
    require(
        by_id["G56"]["controlling_source"]
        == "udt_global_descent_pair_surface_reset_ownership_audit_2026-08-10/AUDIT_REPORT.md",
        "global descent source changed",
    )
    require("G56_REFINES_G55_BY_CONSOLIDATING_GLOBAL_PAIR_SURFACE_PATH_CARRY_ALIGNMENT_AND_CLOCK_ONLY_DESCENT" in by_id["G56"]["precedence_rule"], "G55 global descent refinement absent")
    require(
        by_id["G57"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__LOCAL_LINEAR_POSITIVE_LINE_TRANSPORTS_AFFINE__CANONICAL_METRIC_AND_COMPLETE_COFRAME_TRANSPORTS_ISOMETRIC_ZERO__SUPPLIED_REGULAR_CALIBRATED_PAIR_FAMILY_INDUCES_EXACT_FULL_COFRAME_dPHI_PAIR_WITH_TIME_AND_MIXING__PHYSICAL_FAMILY_TRANSITION_AND_GLOBAL_OWNER_OPEN",
        "complete-coframe calibration transport status regressed or promoted",
    )
    require(by_id["G57"]["epistemic_label"] == "MIXED", "calibration transport label changed")
    require(
        by_id["G57"]["active_use"]
        == "ACTIVE_CONDITIONAL_PAIR_FAMILY_TRANSPORT_RESULT_AND_NEXT_ON_SHELL_GLOBAL_FAMILY_OWNER_GATE_ONLY",
        "calibration transport use promoted",
    )
    require("physical calibrated observer-pair family or query selector" in by_id["G57"]["open_scope"], "physical pair-family owner invented")
    require("lawful transitions among independently rebuilt families" in by_id["G57"]["open_scope"], "pair-family transitions promoted")
    require("null rank-changing cut-locus and nonlocal strata" in by_id["G57"]["open_scope"], "degenerate/global scope erased")
    require("supplied calibrated pair family called metric-selected" in by_id["G57"]["forbidden_regression"], "conditional family guard absent")
    require("algebraically live time dependence called an on-shell time-live solution" in by_id["G57"]["forbidden_regression"], "time-live ownership guard absent")
    require("catch-proof harness called independent derivation" in by_id["G57"]["forbidden_regression"], "independence guard absent")
    require("an extra scalar reset equation invented after a common family is supplied" in by_id["G57"]["forbidden_regression"], "scalar-reset reduction guard absent")
    require(
        by_id["G57"]["controlling_source"]
        == "udt_complete_coframe_calibration_transport_from_scratch_2026-08-10/AUDIT_REPORT.md",
        "calibration transport source changed",
    )
    require("G57_REFINES_G56_BY_DERIVING_THE_FULL_DECLARED_LOCAL_TRANSPORT_CLASS" in by_id["G57"]["precedence_rule"], "G56 calibration transport refinement absent")
    require(
        by_id["G58"]["current_status"]
        == "VERIFIED_WITH_CORRECTIONS__SUPPLIED_PAIR_CONE_EXACTLY_JOINS_BETA_PHI_PAIR_AND_CONDITIONAL_CEFF__LOCAL_BIDIRECTIONAL_CAUSAL_ISOMORPHISMS_RETAIN_INFINITE_TRANSITION_CALIBRATION_FREEDOM__NO_AMBIENT_PHYSICAL_FAMILY_MULTIPLICITY_OR_SELECTOR_THEOREM",
        "co-present causal pair gate regressed or promoted",
    )
    require(by_id["G58"]["epistemic_label"] == "MIXED", "causal pair gate label changed")
    require(
        by_id["G58"]["active_use"]
        == "ACTIVE_SCOPED_PAIR_CONE_CAUSAL_JOIN_AND_NEXT_AMBIENT_PHYSICAL_PAIR_SELECTOR_GATE_ONLY",
        "causal pair gate use promoted",
    )
    require("metric/query construction of ambiently distinct pair immersions" in by_id["G58"]["open_scope"], "ambient pair construction silently closed")
    require("global causal order reflection and faithfulness" in by_id["G58"]["open_scope"], "global causal scope erased")
    require("local transition or profile freedom called physically distinct ambient pair families" in by_id["G58"]["forbidden_regression"], "physical-family overclaim guard absent")
    require("one-way causal maps included in the bidirectional classification" in by_id["G58"]["forbidden_regression"], "causal-class scope guard absent")
    require("sampled smoke test called theorem-strength independent proof" in by_id["G58"]["forbidden_regression"], "verification-grade guard absent")
    require(
        by_id["G58"]["controlling_source"]
        == "udt_copresent_causal_pair_functor_selector_audit_2026-08-10/AUDIT_REPORT.md",
        "causal pair source changed",
    )
    require("G58_REFINES_G57_BY_DERIVING_THE_EXACT_COMPLETE_PAIR_CONE_PHI_CEFF_JOIN" in by_id["G58"]["precedence_rule"], "G57 causal pair refinement absent")
    require(
        by_id["G59"]["current_status"]
        == "VERIFIED_WITH_CORRECTIONS__CONDITIONAL_SPLIT_RELATIVE_MATRIX_ORCHESTRA_H_EQUALS_HR_PLUS_HA__GENERIC_CONTINUOUS_ORBIT_AND_SIGNED_AREA_LOCKS_DERIVED__ANGULAR_MODULATES_KAPPA_PHI_PAIR_BETA__POSITIVE_WEIGHTS_AND_PHYSICAL_REGIME_CURVE_OPEN",
        "pair-instrument mixing atlas status regressed or promoted",
    )
    require(by_id["G59"]["epistemic_label"] == "MIXED", "pair-instrument atlas label changed")
    require(
        by_id["G59"]["active_use"]
        == "ACTIVE_CONDITIONAL_POINTWISE_ORCHESTRA_ATLAS_AND_NEXT_OWNED_BRANCH_CURVE_GATE_ONLY",
        "pair-instrument atlas use promoted",
    )
    require("universal ownership of reciprocal/angular split" in by_id["G59"]["open_scope"], "split ownership silently closed")
    require("actual time-live or scale-live curve s to (H_R,H_A)" in by_id["G59"]["open_scope"], "physical curve silently closed")
    require("positive measurement weights" in by_id["G59"]["open_scope"], "positive weights invented")
    require("signed R A M called positive probabilities or importance weights" in by_id["G59"]["forbidden_regression"], "signed-channel guard absent")
    require("off-shell algebra called time-live evolution" in by_id["G59"]["forbidden_regression"], "time-live ownership guard absent")
    require("catch harness called independent proof" in by_id["G59"]["forbidden_regression"], "independence-scope guard absent")
    require(
        by_id["G59"]["controlling_source"]
        == "udt_pair_instrument_mixing_solution_space_audit_2026-08-10/AUDIT_REPORT.md",
        "pair-instrument atlas source changed",
    )
    require("G59_REFINES_G58_BY_DERIVING_THE_COMPLETE_SPLIT_RELATIVE_MATRIX_AND_SIGNED_AREA_ORCHESTRA_ATLAS" in by_id["G59"]["precedence_rule"], "G58 pair-instrument refinement absent")
    require(
        by_id["G60"]["current_status"]
        == "VERIFIED_WITH_CORRECTIONS__FULL_REGULAR_PAIR_ADAPTED_COFRAME_MOVIES_OBEY_EXACT_BASE_ANGULAR_MIXING_COMPATIBILITY__ARBITRARY_TIME_ONLY_FREQUENCIES_SURVIVE__NO_NATIVE_EVOLUTION_CHARACTERISTIC_OR_REGIME_SELECTED",
        "time-live orchestra status regressed or promoted",
    )
    require(by_id["G60"]["epistemic_label"] == "MIXED", "time-live orchestra label changed")
    require(
        by_id["G60"]["active_use"]
        == "ACTIVE_LOCAL_TIMELIVE_KINEMATIC_PARENT_AND_NEXT_OWNED_HISTORY_RESTRICTION_GATE_ONLY",
        "time-live orchestra use promoted",
    )
    require("an owned principal differential relation or equivalent global-completion rule" in by_id["G60"]["open_scope"], "history-selection owner silently closed")
    require("characteristics dispersion frequencies and regime map" in by_id["G60"]["open_scope"], "time-live physical outputs silently selected")
    require("bootstrap tuning only after a history restriction is owned" in by_id["G60"]["open_scope"], "bootstrap sequencing guard absent")
    require("Maurer-Cartan compatibility called an equation of motion" in by_id["G60"]["forbidden_regression"], "identity-versus-EOM guard absent")
    require("the metric null cone called a field characteristic without a principal operator" in by_id["G60"]["forbidden_regression"], "cone-versus-characteristic guard absent")
    require("local nonselection widened to a theorem that no native or global law exists" in by_id["G60"]["forbidden_regression"], "bounded nonselection guard absent")
    require(
        by_id["G60"]["controlling_source"]
        == "udt_complete_timelive_orchestra_compatibility_audit_2026-08-10/AUDIT_REPORT.md",
        "time-live orchestra source changed",
    )
    require("G60_REFINES_G59_BY_TURNING_ON_ALL_DECLARED_TIME_AND_SPACE_CHANNELS" in by_id["G60"]["precedence_rule"], "G59 time-live refinement absent")
    require(
        by_id["G61"]["current_status"]
        == "VERIFIED_WITH_CORRECTIONS__COMPLETE_REGULAR_CHART_LOCALLY_FINITE_JET_OPEN_ON_DECLARED_POSITIVE_SCREEN_TIME_ORIENTED_COMPONENT__NO_OWNED_NONIDENTITY_HISTORY_RESTRICTION_FOUND_IN_TEN_FROZEN_SOURCES",
        "native history restriction status regressed or promoted",
    )
    require(by_id["G61"]["epistemic_label"] == "MIXED", "native history restriction label changed")
    require(
        by_id["G61"]["active_use"]
        == "ACTIVE_CHART_AND_SOURCE_BOUNDED_HISTORY_NONSELECTION_AND_NEXT_GLOBAL_SELECTOR_TYPE_GATE_ONLY",
        "native history restriction use promoted",
    )
    require("other chart components and split-changing null rank-changing cut-locus strata" in by_id["G61"]["open_scope"], "other chart/strata silently closed")
    require("global causal faithfulness chronology hyperbolicity completeness and descent" in by_id["G61"]["open_scope"], "global gates silently closed")
    require("preservation of a boundary germ called preservation of global causality or completion" in by_id["G61"]["forbidden_regression"], "boundary/global guard absent")
    require("the type signature R(j^k g;G_global)=0 called a formula or derived law" in by_id["G61"]["forbidden_regression"], "selector type guard absent")
    require(
        by_id["G61"]["controlling_source"]
        == "udt_native_history_restriction_from_scratch_2026-08-10/AUDIT_REPORT.md",
        "native history restriction source changed",
    )
    require("G61_REFINES_G60_BY_PROVING_FINITE_JET_OPENNESS" in by_id["G61"]["precedence_rule"], "G60 history restriction refinement absent")
    require(
        by_id["G62"]["current_status"]
        == "VERIFIED_WITH_CORRECTIONS__FINITE_REGULAR_OBSERVER_NETWORK_HAS_EXACT_ENDPOINT_ATLAS_AND_PATH_LABELLED_ASSEMBLY_IDENTITIES__ROUTE_DEPENDENCE_ALLOWED__UNIVERSAL_FLAT_DESCENT_UNOWNED",
        "observer-network assembly status regressed or promoted",
    )
    require(by_id["G62"]["epistemic_label"] == "MIXED", "observer-network label changed")
    require(
        by_id["G62"]["active_use"]
        == "ACTIVE_NETWORK_ASSEMBLY_AND_PHYSICAL_RELATION_FAMILY_ROUTE_POLICY_OWNERSHIP_GATE_ONLY",
        "observer-network use promoted",
    )
    require("physical calibrated observer pair query relation family" in by_id["G62"]["open_scope"], "physical relation-family owner silently closed")
    require("endpoint descended path labelled or path quotient policy branch by branch" in by_id["G62"]["open_scope"], "route policy silently selected")
    require("K4 d2 or abelian Bianchi bookkeeping called new physics or a history law" in by_id["G62"]["forbidden_regression"], "four-face novelty guard absent")
    require("continuum curvature inferred without a chosen smooth local connection" in by_id["G62"]["forbidden_regression"], "continuum-flatness hypothesis guard absent")
    require("route policy used before relation family ownership" in by_id["G62"]["forbidden_regression"], "relation-family ordering guard absent")
    require(
        by_id["G62"]["controlling_source"]
        == "udt_complete_observer_network_assembly_from_scratch_2026-08-11/AUDIT_REPORT.md",
        "observer-network source changed",
    )
    require("G62_REFINES_G61_AND_G40_BY_ASSEMBLING_THE_FINITE_REGULAR_NETWORK" in by_id["G62"]["precedence_rule"], "G62 assembly refinement absent")
    require(
        by_id["G63"]["current_status"]
        == "VERIFIED_WITH_CORRECTIONS__BOUNDED_14_WITNESS_SOLVED_ATLAS_RETAINS_ENDPOINT_DEPTH_CAUSAL_PROPAGATORS_FULL_COFRAME_HOLONOMY_AND_R17_NORMAL_HOLONOMY__MULTIPLE_GEOMETRIC_SURVIVOR_FAMILIES__NO_PHYSICAL_SELECTOR_DYNAMICS_OR_STABILITY",
        "solved-geometry survivor status regressed or promoted",
    )
    require(by_id["G63"]["epistemic_label"] == "OBSERVED", "solved-geometry label changed")
    require(
        by_id["G63"]["active_use"]
        == "ACTIVE_BOUNDED_SOLVED_GEOMETRY_AND_NEXT_COUPLED_CHANNEL_RELATION_GATE_ONLY",
        "solved-geometry use promoted",
    )
    require("metric-native relation or independence among endpoint depth causal propagator full-coframe holonomy and normal holonomy" in by_id["G63"]["open_scope"], "coupled-channel relation silently closed")
    require("native on-shell equation and time-live global completion" in by_id["G63"]["open_scope"], "on-shell/global completion silently closed")
    require("bounded persistence called physical or dynamical stability" in by_id["G63"]["forbidden_regression"], "stability overclaim guard absent")
    require("endpoint scalar and path holonomy forced to compete" in by_id["G63"]["forbidden_regression"], "typed coexistence guard absent")
    require("arbitrary wider scan launched before channel invariants and independence contract" in by_id["G63"]["forbidden_regression"], "next-step ordering guard absent")
    require(
        by_id["G63"]["controlling_source"]
        == "udt_solved_geometry_relation_family_survivor_atlas_2026-08-11/AUDIT_REPORT.md",
        "solved-geometry source changed",
    )
    require("G63_REFINES_G62_G47_G49_G51_G60_BY_SOLVING_THE_EXACT_BOUNDED_WITNESS_ATLAS" in by_id["G63"]["precedence_rule"], "G63 solved-atlas refinement absent")
    require(
        by_id["G64"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__QUERY_CLASS_DEPENDENT_CHANNEL_ARCHITECTURE__COMMON_QUERY_CHANNELS_COMPATIBILITY_LINKED_WITH_RETAINED_EXTRINSIC_DATA__PHYSICAL_QUERY_BRANCH_AND_DYNAMICS_OPEN",
        "common-query architecture status regressed or promoted",
    )
    require(by_id["G64"]["epistemic_label"] == "MIXED", "common-query label changed")
    require("universal preferred path search resumed" in by_id["G64"]["forbidden_regression"], "preferred-path guard absent")
    require("unresolved Q2 Codazzi certification" in by_id["G64"]["open_scope"], "Codazzi caveat silently closed")
    require(
        by_id["G64"]["controlling_source"]
        == "udt_common_query_pair_immersion_reconstruction_2026-08-11/AUDIT_REPORT.md",
        "common-query source changed",
    )
    require("G64_REFINES_G63_BY_PLACING_COEXISTING_ENDPOINT_EXTRINSIC_JACOBI_AND_TRANSPORT_CHANNELS" in by_id["G64"]["precedence_rule"], "G64 query refinement absent")
    require(
        by_id["G65"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__ALL_18_FROZEN_M3_SNE_FITS_AND_443_LEAVES_BIT_IDENTICAL__NATIVE_OBSERVER_QUERY_RETYPING_ALGEBRAICALLY_IDENTICAL__NO_OWNED_COMPLETE_SNE_QUERY_CORRECTION",
        "native-query SNe status regressed or promoted",
    )
    require(by_id["G65"]["epistemic_label"] == "MIXED", "native-query SNe label changed")
    require("physical complete SNe query and pair immersion" in by_id["G65"]["open_scope"], "complete SNe query silently owned")
    require("P1 promoted to centered CMB lapse" in by_id["G65"]["forbidden_regression"], "P1 role guard absent")
    require("conditional pair c_eff called material signal speed" in by_id["G65"]["forbidden_regression"], "conditional c_eff guard absent")
    require(
        by_id["G65"]["controlling_source"]
        == "udt_sne_native_observer_query_replay_2026-08-11/AUDIT_REPORT.md",
        "native-query SNe source changed",
    )
    require("G65_REFINES_G64_AND_THE_FROZEN_M3_SNE_UNIVERSE" in by_id["G65"]["precedence_rule"], "G65 SNe refinement absent")
    require(
        by_id["G66"]["current_status"]
        == "VERIFIED_AFTER_SPECIFIED_CORRECTIONS__16_SOURCE_F00_F17_QUERY_ARCHITECTURE_MAPPED__NO_COMPLETE_PHYSICAL_CMB_REALIZATION_OWNED__F00_COMPATIBILITY_ONLY",
        "complete CMB query-map status regressed or promoted",
    )
    require(by_id["G66"]["epistemic_label"] == "MIXED", "complete CMB query-map label changed")
    require("physical CMB observer-sky query and pair immersion" in by_id["G66"]["open_scope"], "physical CMB query silently owned")
    require("local artifact checker called independent semantic derivation" in by_id["G66"]["forbidden_regression"], "artifact/semantic evidence guard absent")
    require("eigenvalues called nonzero power" in by_id["G66"]["forbidden_regression"], "spectrum/power type guard absent")
    require("pair c_eff called local signal speed" in by_id["G66"]["forbidden_regression"], "pair/local speed guard absent")
    require(
        by_id["G66"]["controlling_source"]
        == "udt_cmb_complete_observation_query_map_2026-08-11/AUDIT_REPORT.md",
        "complete CMB query-map source changed",
    )
    require("G66_REFINES_G65_G64_AND_THE_F00_F17_CMB_FAMILY_UNIVERSE" in by_id["G66"]["precedence_rule"], "G66 CMB refinement absent")
    require(
        by_id["G74"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__EXACT_21_PROFILE_WHOLE_SKY_CONTROL_CENSUS__3_F01_GLOBAL_DIFFEO__6_PERSISTENT_SAMPLED_REGULAR_ONLY__12_CENTER_C2_BLOCKED_NO_REPAIR",
        "G74 topology status regressed or promoted",
    )
    require(by_id["G74"]["epistemic_label"] == "MIXED", "G74 topology label changed")
    require("globally center-regular complete-metric profile family" in by_id["G74"]["open_scope"], "G74 center-regular profile silently owned")
    require("sampled regularity promoted to global theorem" in by_id["G74"]["forbidden_regression"], "G74 sampled/global guard absent")
    require("direct Christoffel replay called clean-room independent" in by_id["G74"]["forbidden_regression"], "G74 independence caveat absent")
    require(
        by_id["G74"]["controlling_source"]
        == "udt_cmb_G74_symbolic_sky_relation_topology_atlas_2026-08-11/AUDIT_REPORT.md",
        "G74 topology source changed",
    )
    require("G74_COMPLETES_G73_SYMBOLIC_SKY_TOPOLOGY_GATE" in by_id["G74"]["precedence_rule"], "G74 topology refinement absent")
    require(
        by_id["G75"]["current_status"]
        == "EXTERNALLY_VERIFIED_BOUNDED_FAMILY__49_EXACT_PRIMITIVE_QUADRATIC_SHAPES__591_CENTER_C_INFINITY_LORENTZ_REGULAR_CONTROLS__ZERO_ROW_MISMATCHES__LOCAL_EVIDENCE_CAVEATS_CLOSED",
        "G75 center-regular family status regressed or promoted",
    )
    require(by_id["G75"]["epistemic_label"] == "MIXED", "G75 family label changed")
    require("all smooth center-regular axial profiles" in by_id["G75"]["open_scope"], "G75 bounded family promoted to full smooth space")
    require("original local replay called a fresh or fully independent reconstruction" in by_id["G75"]["forbidden_regression"], "G75 independence guard absent")
    require("original local catch layer called catch-complete" in by_id["G75"]["forbidden_regression"], "G75 catch-completeness guard absent")
    require("G74 blocked rows called repaired" in by_id["G75"]["forbidden_regression"], "G75 no-repair guard absent")
    require(
        by_id["G75"]["controlling_source"]
        == "udt_cmb_G75_center_regular_axial_profile_family_2026-08-11/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G75 family source changed",
    )
    require("G75_EXTERNALLY_VERIFIES_THE_BOUNDED_CENTER_REGULAR_PROFILE_FAMILY_MAP" in by_id["G75"]["precedence_rule"], "G75 family refinement absent")
    require(
        by_id["G76"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__587_SAMPLED_COMPLETE_ORIENTATION_PRESERVING__4_HISTORICAL_NUMERICALLY_UNRESOLVED_UNDER_FROZEN_G76_GATE",
        "G76 historical whole-sky status rewritten",
    )
    require(by_id["G76"]["epistemic_label"] == "OBSERVED", "G76 historical label changed")
    require("four G76 rows silently promoted" in by_id["G76"]["forbidden_regression"], "G76 immutable-history guard absent")
    require(
        by_id["G76"]["controlling_source"]
        == "udt_cmb_G76_complete_family_whole_sky_relation_atlas_2026-08-11/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G76 historical source changed",
    )
    require(
        by_id["G77"]["current_status"]
        == "VERIFIED_FULL_FAMILY_DIRECT_REPLAY__590_STRONG__1_REGISTERED__0_UNRESOLVED__FOUR_G76_EXCEPTIONS_RESOLVED_IN_G77",
        "G77 direct-replay status regressed or promoted",
    )
    require(by_id["G77"]["epistemic_label"] == "OBSERVED", "G77 direct-replay label changed")
    require("continuum injectivity" in by_id["G77"]["open_scope"], "G77 finite-mesh scope promoted")
    require("G77 used to rewrite G76 history" in by_id["G77"]["forbidden_regression"], "G77/G76 history guard absent")
    require(
        by_id["G77"]["controlling_source"]
        == "udt_cmb_G77_full_family_direct_christoffel_replay_2026-08-11/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G77 direct-replay source changed",
    )
    require("G77_STRENGTHENS_G76" in by_id["G77"]["precedence_rule"], "G77 refinement absent")
    require(
        by_id["G78"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__NO_PHYSICAL_PROFILE_ENDPOINT_SCALE_OR_SOURCE_OWNER_IN_EXACT_20_SOURCE_G78_UNIVERSE",
        "G78 bounded owner-join status regressed or promoted",
    )
    require(by_id["G78"]["epistemic_label"] == "MIXED", "G78 owner-join label changed")
    require("exhaustive current repository" in by_id["G78"]["open_scope"], "G78 source scope promoted")
    require("internal route-status regression check" in by_id["G78"]["forbidden_regression"], "G78 semantic independence caveat absent")
    require("dimensionless R factorization called CSN" in by_id["G78"]["forbidden_regression"], "G78 scale guard absent")
    require(
        by_id["G78"]["controlling_source"]
        == "udt_cmb_G78_profile_endpoint_source_owner_join_2026-08-11/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G78 owner-join source changed",
    )
    require("G78_REFINES_G77" in by_id["G78"]["precedence_rule"], "G78 refinement absent")
    require(
        by_id["G79"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__BOUNDED_SAME_GEOMETRY_REDSHIFT_AND_ANGULAR_DISTANCE_QUERY",
        "G79 bounded dimensional-query status regressed or promoted",
    )
    require(by_id["G79"]["epistemic_label"] == "MIXED", "G79 dimensional-query label changed")
    require("physical profile and scale R" in by_id["G79"]["open_scope"], "G79 physical-owner scope promoted")
    require("cmb_temp or CMB spectrum" in by_id["G79"]["open_scope"], "G79 thermal deferral absent")
    require("control profile called physical" in by_id["G79"]["forbidden_regression"], "G79 control-profile guard absent")
    require("neighboring-ray route called fully end-to-end independent" in by_id["G79"]["forbidden_regression"], "G79 independence caveat absent")
    require(
        by_id["G79"]["controlling_source"]
        == "udt_cmb_G79_same_geometry_dimensional_sne_query_2026-08-11/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G79 dimensional-query source changed",
    )
    require("G79_COMPLETES_G78" in by_id["G79"]["precedence_rule"], "G79 refinement absent")
    require(
        by_id["G80"]["current_status"] == "VERIFIED_AS_BOUNDED_GEOMETRIC_RECIPROCITY",
        "G80 bounded reciprocity status regressed or promoted",
    )
    require(by_id["G80"]["epistemic_label"] == "MIXED", "G80 reciprocity label changed")
    require("nonradial and general endpoint-screen branches" in by_id["G80"]["open_scope"], "G80 screen scope promoted")
    require("generic Jacobi theorem called a UDT-specific selector" in by_id["G80"]["forbidden_regression"], "G80 genericity guard absent")
    require("past-directed reversal called a future signal" in by_id["G80"]["forbidden_regression"], "G80 signal guard absent")
    require("bare transpose identity applied across arbitrary screen gauges" in by_id["G80"]["forbidden_regression"], "G80 screen-gauge guard absent")
    require(
        by_id["G80"]["controlling_source"]
        == "udt_cmb_G80_reverse_pair_reciprocity_2026-08-11/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G80 reciprocity source changed",
    )
    require("G80_COMPLETES_G79" in by_id["G80"]["precedence_rule"], "G80 refinement absent")
    require(
        by_id["G81"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__DERIVED_CONDITIONAL_SCREEN_COVARIANCE_ON_TWO_FIXED_CONTROLS",
        "G81 bounded covariance status regressed or promoted",
    )
    require(by_id["G81"]["epistemic_label"] == "MIXED", "G81 covariance label changed")
    require("METHOD_CAVEAT_CLOSED_BY_G82" in by_id["G81"]["active_use"], "G81 method closure absent")
    require("integrator families" in by_id["G81"]["open_scope"], "G81 method scope promoted")
    require("two fixed controls called a generic UDT selector" in by_id["G81"]["forbidden_regression"], "G81 bounded-scope guard absent")
    require("bounded neighboring-ray independence called absolute" in by_id["G81"]["forbidden_regression"], "G81 independence guard absent")
    require("reviewer said to have reopened nine source bytes" in by_id["G81"]["forbidden_regression"], "G81 source-review boundary absent")
    require(
        by_id["G81"]["controlling_source"]
        == "udt_cmb_G81_nonradial_screen_covariance_2026-08-12/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G81 covariance source changed",
    )
    require("G81_COMPLETES_G80" in by_id["G81"]["precedence_rule"], "G81 refinement absent")
    require(
        by_id["G82"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__G81_C1_SCREEN_COVARIANCE_SURVIVES_ONE_FIXED_NON_DOP853_RADAU_REPLAY",
        "G82 bounded method-support status regressed or promoted",
    )
    require(by_id["G82"]["epistemic_label"] == "OBSERVED", "G82 support label changed")
    require("absolute method independence" in by_id["G82"]["open_scope"], "G82 method scope promoted")
    require("original 15 catches called exhaustive" in by_id["G82"]["forbidden_regression"], "G82 catch caveat absent")
    require("literal packaged CLI rerun" in by_id["G82"]["forbidden_regression"], "G82 rerun caveat absent")
    require(
        by_id["G82"]["controlling_source"]
        == "udt_cmb_G82_fixed_c1_radau_replay_2026-08-12/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G82 support source changed",
    )
    require("G82_CLOSES_ONLY_G81S_REGISTERED" in by_id["G82"]["precedence_rule"], "G82 refinement absent")
    require(
        by_id["G87"]["current_status"]
        == "ACCEPT__VERIFIED_WITH_CAVEATS__EXACT_ENDPOINT_TRANSITIONS_AND_PSD_PARTIAL_ORDER_SEPARATED__PHYSICAL_GLOBAL_FAMILY_OPEN",
        "G87 chord-network status regressed or promoted",
    )
    require(by_id["G87"]["epistemic_label"] == "MIXED", "G87 chord-network label changed")
    require("physical common calibrated global state family" in by_id["G87"]["open_scope"], "G87 global-family owner promoted")
    require("PSD reachability called Reciprocity" in by_id["G87"]["forbidden_regression"], "G87 order/Reciprocity guard absent")
    require("independent derivation of the coframe transition" in by_id["G87"]["forbidden_regression"], "G87 replay-independence caveat absent")
    require(
        by_id["G87"]["controlling_source"]
        == "udt_pair_chord_network_descent_audit_2026-08-12/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G87 chord-network source changed",
    )
    require("G87_CLOSES_THE_ZERO_ORDER_CHORD_COMPOSITION_QUESTION" in by_id["G87"]["precedence_rule"], "G87 refinement absent")
    require(
        by_id["G89"]["current_status"]
        == "EXTERNALLY_VERIFIED_WITH_CAVEATS__FULL_B_Q_S_Y_Z_PULLBACK_AND_FIRST_VARIATION__TERMINAL_PHI_PAIR_AND_CEFF_OVER_CE_DERIVED__NO_UNIQUE_SCALAR_MU_OWNED__PHYSICAL_PAIR_AND_HISTORY_OPEN",
        "G89 uncompressed evaluator status regressed or promoted",
    )
    require(by_id["G89"]["epistemic_label"] == "MIXED", "G89 evaluator label changed")
    require("physical pair realization and live history" in by_id["G89"]["open_scope"], "G89 pair/history promoted")
    require("overlapping-pair compatibility law" in by_id["G89"]["open_scope"], "G89 compatibility-law gate absent")
    require("modern four-component S identified with July mu_old" in by_id["G89"]["forbidden_regression"], "G89 mu type guard absent")
    require("fixed-P convexity called a derived quiet-middle regime" in by_id["G89"]["forbidden_regression"], "G89 fixed-P promotion guard absent")
    require("external review described as canonization" in by_id["G89"]["forbidden_regression"], "G89 external-review scope guard absent")
    require(
        by_id["G89"]["controlling_source"]
        == "udt_uncompressed_pair_kernel_reconstruction_2026-08-14/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G89 evaluator source changed",
    )
    require("G89_FRESH_SEALED_REVIEW_REPRODUCED_THE_COMPLETE_SUPPLIED_PAIR_EVALUATOR" in by_id["G89"]["precedence_rule"], "G89 review refinement absent")
    require(
        by_id["G90"]["current_status"]
        == "INTERNALLY_VERIFIED_WITH_CAVEATS__NONIDENTITY_SIMULTANEOUS_OVERLAP_COMPATIBILITY__ALL_INSTRUMENTS_ACTIVITY_ALONE_DOES_NOT_SELECT_RESPONSE_SHAPE__LOUD_QUIET_LOUD_SURVIVES_DECLARED_ALL_ACTIVE_CLASS",
        "G90 overlap/loud-quiet status regressed or promoted",
    )
    require(by_id["G90"]["epistemic_label"] == "MIXED", "G90 overlap label changed")
    require("fresh semantic review" in by_id["G90"]["open_scope"], "G90 semantic review falsely closed")
    require("physical pair family and metric/query history owner" in by_id["G90"]["open_scope"], "G90 physical history promoted")
    require("original explicit lifts called fully live" in by_id["G90"]["forbidden_regression"], "G90 activity correction guard absent")
    require("flat or monotone C2 lifts omitted" in by_id["G90"]["forbidden_regression"], "G90 C2 counterfamily guard absent")
    require("quiet-middle survivor called universal physical law" in by_id["G90"]["forbidden_regression"], "G90 selection guard absent")
    require(
        by_id["G90"]["controlling_source"]
        == "udt_overlapping_pair_live_compatibility_audit_2026-08-14/AUDIT_REPORT.md",
        "G90 overlap source changed",
    )
    require("G90_CORRECTS_THE_EXPLICIT_LIFT_ALL_ACTIVE_CATEGORY_ERROR" in by_id["G90"]["precedence_rule"], "G90 correction refinement absent")
    require(
        by_id["G91"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__ONE_SCREEN_COMPARISON_ARROW_MU_LOCK_IS_GENERIC_SPECTRAL_RECIPROCAL_LOCK_DEFECT_FOR_s_NE_r__EXACT_GAUGE_CARVEOUT_ON_PART_OF_s_EQ_r__COUPLING_INERT_FOR_PHI_PROFILE_SELECTION__COMPLETE_KERNEL_CROSSWALK_OPEN",
        "G91 scoped mu_lock result regressed or promoted",
    )
    require(by_id["G91"]["epistemic_label"] == "MIXED", "G91 mu_lock label changed")
    require("type-correct map into complete B Q S Y Z pair evaluator" in by_id["G91"]["open_scope"], "G91 complete-kernel crosswalk falsely closed")
    require("mu_lock collapsed into July mu_old" in by_id["G91"]["forbidden_regression"], "G91 mu type guard absent")
    require("s equals r gauge carve-out omitted" in by_id["G91"]["forbidden_regression"], "G91 gauge carve-out guard absent")
    require("physical depth cocycle" in by_id["G91"]["forbidden_regression"], "G91 physical-depth promotion guard absent")
    require(
        by_id["G91"]["controlling_source"]
        == "udt_mixing_channel_lane_2026-08-06/BLIND_VERIFICATION_FINAL.md",
        "G91 mu_lock source changed",
    )
    require("G91_RECOVERS_THE_DISTINCT_AUGUST6_SCOPED_RECIPROCAL_LOCK_DEFECT" in by_id["G91"]["precedence_rule"], "G91 recovery precedence absent")
    require(
        by_id["G92"]["current_status"]
        == "INTERNALLY_VERIFIED_WITH_CAVEATS__RESTRICTED_MU_LOCK_IS_SIGNED_COMPONENT_OF_SUPPLIED_ENDPOINT_TRANSITION__NO_UNIQUE_FULL_2X2_SCALAR_EXTENSION__NOT_UNIVERSALLY_RECOVERABLE_FROM_TERMINAL_PAIR_METRIC__FRESH_SEMANTIC_REVIEW_OPEN",
        "G92 mu crosswalk status regressed or promoted",
    )
    require(by_id["G92"]["epistemic_label"] == "MIXED", "G92 crosswalk label changed")
    require("fresh semantic adversary" in by_id["G92"]["open_scope"], "G92 fresh review falsely closed")
    require("physical endpoint carry" in by_id["G92"]["open_scope"], "G92 endpoint carry promoted")
    require("restricted component promoted to universal scalar" in by_id["G92"]["forbidden_regression"], "G92 scalar-promotion guard absent")
    require("terminal h or phi_pair identified with full-arrow strain" in by_id["G92"]["forbidden_regression"], "G92 channel-type guard absent")
    require("S/Z pullback fiber ignored" in by_id["G92"]["forbidden_regression"], "G92 pullback-fiber guard absent")
    require("s equals r gauge carve-out omitted" in by_id["G92"]["forbidden_regression"], "G92 old gauge carve-out guard absent")
    require(
        by_id["G92"]["controlling_source"]
        == "udt_august6_mu_complete_kernel_crosswalk_2026-08-15/AUDIT_REPORT.md",
        "G92 crosswalk source changed",
    )
    require("G92_DERIVES_THE_RESTRICTED_ENDPOINT_TRANSITION_COMPONENT_BRIDGE" in by_id["G92"]["precedence_rule"], "G92 crosswalk precedence absent")
    require(
        by_id["G93"]["current_status"]
        == "EXTERNALLY_VERIFIED_WITH_CAVEATS__G87_G89_G90_G92_KERNEL_INTERFACES_COHERENT__AMBIENT_AND_TERMINAL_TRANSITIONS_COMPOSE_SEPARATELY__ALL_FIVE_CHANNELS_PRECEDE_READOUT__NO_FIT_GEOMETRY_REPLAY_JUSTIFIED__PHYSICAL_HISTORY_AND_FLUX_OPEN",
        "G93 release-candidate status regressed or promoted",
    )
    require(by_id["G93"]["epistemic_label"] == "MIXED", "G93 release-candidate label changed")
    require("witness-independent state ensemble" in by_id["G93"]["open_scope"], "G93 shared-witness caveat silently closed")
    require("semantic mutations beyond status guards" in by_id["G93"]["open_scope"], "G93 catch-proof caveat silently closed")
    require("physical complete history and pair family" in by_id["G93"]["open_scope"], "G93 physical history promoted")
    require("native flux source and luminosity law" in by_id["G93"]["open_scope"], "G93 flux owner promoted")
    require("ambient and terminal arrows identified" in by_id["G93"]["forbidden_regression"], "G93 arrow-type guard absent")
    require("mu_lock appended after phi_pair" in by_id["G93"]["forbidden_regression"], "G93 mu double-count guard absent")
    require("frozen P1 retype called rebuilt-kernel replay" in by_id["G93"]["forbidden_regression"], "G93 replay-identity guard absent")
    require("geometry readiness called full SNe validation" in by_id["G93"]["forbidden_regression"], "G93 validation-promotion guard absent")
    require(
        by_id["G93"]["controlling_source"]
        == "udt_reciprocal_kernel_release_candidate_interface_audit_2026-08-15/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G93 release-candidate source changed",
    )
    require("G93_FRESH_SEALED_REVIEW_REPRODUCES_THE_JOINED_KERNEL" in by_id["G93"]["precedence_rule"], "G93 external-review precedence absent")
    require(
        by_id["G94"]["current_status"]
        == "EXTERNALLY_VERIFIED_WITH_CAVEATS__Z3_GEOMETRIC_CLOCK_FACTOR_DERIVED_ON_REGULAR_SUPPLIED_QUERY__TRANSFER_PRODUCT_ETA_EPSILON_OPEN__HISTORICAL_Z2_LAW_COMPATIBLE_CONDITIONAL",
        "G94 flux ownership status regressed or promoted",
    )
    require(by_id["G94"]["epistemic_label"] == "MIXED", "G94 flux label changed")
    require("physical radiative carrier current and conserved measure" in by_id["G94"]["open_scope"], "G94 current ownership promoted")
    require("energy-frequency law" in by_id["G94"]["open_scope"], "G94 energy ownership promoted")
    require("caustics multiple images" in by_id["G94"]["open_scope"], "G94 singular/global scope promoted")
    require("clock or frequency ratio identified with energy ratio" in by_id["G94"]["forbidden_regression"], "G94 clock-energy type guard absent")
    require("eta set to one" in by_id["G94"]["forbidden_regression"], "G94 survival guard absent")
    require("historical dL equals Z2 dA called unconditional" in by_id["G94"]["forbidden_regression"], "G94 luminosity-law guard absent")
    require(
        by_id["G94"]["controlling_source"]
        == "udt_native_flux_luminosity_law_ownership_audit_2026-08-15/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G94 flux source changed",
    )
    require("G94_FRESH_SEALED_REVIEW_RECONSTRUCTS_WRONSKIAN" in by_id["G94"]["precedence_rule"], "G94 external-review precedence absent")
    require(
        by_id["G95"]["current_status"]
        == "EXTERNALLY_VERIFIED_WITH_CAVEATS__GEOMETRIC_RESPONSE_AND_PHASESPACE_TRANSPORT_ONLY__PHYSICAL_TRANSFER_OPEN__EPSILON_ONE_OVER_Z_ONLY_AFTER_ONE_CARRIER_COVECTOR_IDENTIFICATION",
        "G95 current-energy status regressed or promoted",
    )
    require(by_id["G95"]["epistemic_label"] == "MIXED", "G95 current-energy label changed")
    require("physical radiative carrier and populated conserved measure" in by_id["G95"]["open_scope"], "G95 physical carrier promoted")
    require("energy-covector identification" in by_id["G95"]["open_scope"], "G95 energy premise promoted")
    require("Maxwell-shaped response called physical Maxwell theory or cargo" in by_id["G95"]["forbidden_regression"], "G95 response-cargo guard absent")
    require("Liouville volume called a populated conserved distribution" in by_id["G95"]["forbidden_regression"], "G95 population guard absent")
    require("package consistency verifier called independent derivation" in by_id["G95"]["forbidden_regression"], "G95 evidence-scope repair absent")
    require(
        by_id["G95"]["controlling_source"]
        == "udt_native_radiative_current_energy_owner_audit_2026-08-15/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G95 current-energy source changed",
    )
    require("G95_FRESH_SEALED_REVIEW_RECONSTRUCTS_RESPONSE_COUNTEREXAMPLE" in by_id["G95"]["precedence_rule"], "G95 external-review precedence absent")
    require(
        by_id["G96"]["current_status"]
        == "EXTERNALLY_REVIEWED_WITH_CAVEATS__LABEL_CURRENT_VALID_BUT_TAUTOLOGICAL__NO_NEW_OWNERSHIP_BEYOND_QUERY_TYPING__PHYSICAL_ETA_OPEN",
        "G96 label-current status regressed or promoted",
    )
    require(by_id["G96"]["epistemic_label"] == "MIXED", "G96 label-current label changed")
    require("physical radiative carrier identification" in by_id["G96"]["open_scope"], "G96 carrier identification promoted")
    require("physical zero side flux" in by_id["G96"]["open_scope"], "G96 physical side-flux premise promoted")
    require("query label closure called new metric dynamics" in by_id["G96"]["forbidden_regression"], "G96 tautology guard absent")
    require("eta_label equals one substituted for physical eta equals one" in by_id["G96"]["forbidden_regression"], "G96 eta type guard absent")
    require("det D called the full spacetime current" in by_id["G96"]["forbidden_regression"], "G96 Jacobian type guard absent")
    require(
        by_id["G96"]["controlling_source"]
        == "udt_null_carrier_measure_ownership_audit_2026-08-15/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G96 label-current source changed",
    )
    require("G96_FRESH_SEALED_REVIEW_CONFIRMS_THE_LABEL_PUSHFORWARD_ALGEBRA" in by_id["G96"]["precedence_rule"], "G96 external-review precedence absent")
    require(
        by_id["G97"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__ONE_PRESELECTED_G79_CONTROL_STRONGLY_INCOMPATIBLE_WITH_REGISTERED_SNE_MEAN_RELATION__END_TO_END_CONDITIONAL_INTERFACE_OPERATIONAL__NO_HISTORY_OR_NATIVE_TRANSFER",
        "G97 scoped SNe control result regressed or promoted",
    )
    require(by_id["G97"]["epistemic_label"] == "MIXED", "G97 SNe label changed")
    require("all other complete geometries directions skies histories and branches" in by_id["G97"]["open_scope"], "G97 one-control scope promoted")
    require("native radiative carrier transfer luminosity and source law" in by_id["G97"]["open_scope"], "G97 provisional transfer promoted")
    require("one control negative called rejection of reciprocal kernel or UDT" in by_id["G97"]["forbidden_regression"], "G97 kernel/theory rejection guard absent")
    require("one equatorial curve called all-sky isotropy" in by_id["G97"]["forbidden_regression"], "G97 all-sky guard absent")
    require("another geometry fitted or tuned to repair the mismatch" in by_id["G97"]["forbidden_regression"], "G97 mismatch-tuning guard absent")
    require("scope guards called independent numerical evidence" in by_id["G97"]["forbidden_regression"], "G97 evidence-scope guard absent")
    require(
        by_id["G97"]["controlling_source"]
        == "udt_reciprocal_kernel_release_candidate_interface_audit_2026-08-15/SNE_EXTERNAL_REVIEW_ADJUDICATION.md",
        "G97 SNe source changed",
    )
    require("G97_FRESH_SEALED_REVIEW_REBUILDS_THE_FULL_CURVE_AND_RAW_LIKELIHOOD" in by_id["G97"]["precedence_rule"], "G97 external-review precedence absent")
    require(
        by_id["G98"]["current_status"]
        == "INTERNALLY_VERIFIED_WITH_CAVEATS__PERMITTED_NOT_OWNED__EXACT_FLAT_MONOTONE_AND_LOUD_QUIET_LOUD_CONTRIBUTION_LIVE_HISTORIES_SURVIVE__NO_ACTIVE_NATIVE_SELECTOR_IN_FROZEN_SOURCE_UNIVERSE",
        "G98 continuation-owner status regressed or promoted",
    )
    require(by_id["G98"]["epistemic_label"] == "MIXED", "G98 continuation label changed")
    require("fresh external semantic review" in by_id["G98"]["open_scope"], "G98 review scope silently closed")
    require("physical metric history and query family" in by_id["G98"]["open_scope"], "G98 physical owner promoted")
    require("permitted loud quiet loud family called selected UDT history" in by_id["G98"]["forbidden_regression"], "G98 survivor-selection guard absent")
    require("kinematic identity called dynamics" in by_id["G98"]["forbidden_regression"], "G98 identity/dynamics guard absent")
    require("one SNe mismatch called native history equation" in by_id["G98"]["forbidden_regression"], "G98 observation-owner guard absent")
    require("source-bounded result called generic no-go" in by_id["G98"]["forbidden_regression"], "G98 scope guard absent")
    require(
        by_id["G98"]["controlling_source"]
        == "udt_complete_history_regime_continuation_ownership_audit_2026-08-15/AUDIT_REPORT.md",
        "G98 source changed",
    )
    require("G98_CONSTRUCTIVELY_PROVES_THAT_CURRENT_COMPLETE_EQUATIONS_PERMIT" in by_id["G98"]["precedence_rule"], "G98 precedence absent")
    require(
        by_id["G99"]["current_status"]
        == "INTERNALLY_VERIFIED_WITH_CAVEATS__OBSERVED_CONDITIONAL_TERMINAL_CALIBRATION_FROZEN__NO_OPTIMIZER_OR_HOLDOUT_READ__COMPLETE_HISTORY_TRANSFER_AND_JOINT_UNCERTAINTY_OPEN",
        "G99 calibration status regressed or promoted",
    )
    require(by_id["G99"]["epistemic_label"] == "MIXED", "G99 calibration label changed")
    require("full joint n X_eff covariance" in by_id["G99"]["open_scope"], "G99 joint covariance promoted")
    require("complete B Q S Y Z history" in by_id["G99"]["open_scope"], "G99 history promoted")
    require("P1 called metric-derived or a complete history" in by_id["G99"]["forbidden_regression"], "G99 history guard absent")
    require("BAO CMB or endpoint used to retune" in by_id["G99"]["forbidden_regression"], "G99 holdout guard absent")
    require("SNe domain called Xmax" in by_id["G99"]["forbidden_regression"], "G99 Xmax guard absent")
    require(
        by_id["G99"]["controlling_source"]
        == "udt_observed_middle_regime_pair_calibration_2026-08-15/AUDIT_REPORT.md",
        "G99 source changed",
    )
    require("G99_FREEZES_THE_ALREADY_VERIFIED_P1_CENTRAL_LUMINOSITY_RELATION" in by_id["G99"]["precedence_rule"], "G99 precedence absent")
    require(
        by_id["G101"]["current_status"]
        == "INTERNALLY_VERIFIED_WITH_CAVEATS__PARTIAL_CONCEPTUAL_INTEGRATION_ONLY__OBSERVER_CENTERED_TWO_SOURCE_BAO_QUERY_CLARIFIED__MEGAMASER_LOCAL_SLOPE_SOURCE_LEAD__NO_BRANCH_MERGE_OR_XMAX_PROMOTION",
        "G101 integration status regressed or promoted",
    )
    require(by_id["G101"]["epistemic_label"] == "MIXED", "G101 integration label changed")
    require("raw megamaser table and uncertainty replay" in by_id["G101"]["open_scope"], "G101 raw maser replay promoted")
    require("profile selection" in by_id["G101"]["open_scope"], "G101 profile selection promoted")
    require("tanh profile called derived" in by_id["G101"]["forbidden_regression"], "G101 tanh guard absent")
    require("c over H0 or nearby maser slope identified with Xmax" in by_id["G101"]["forbidden_regression"], "G101 Xmax guard absent")
    require("single Earth-source arrow called a two-point angular statistic" in by_id["G101"]["forbidden_regression"], "G101 query-type guard absent")
    require(
        by_id["G101"]["controlling_source"]
        == "udt_grok2_parallel_branch_integration_audit_2026-08-15/AUDIT_REPORT.md",
        "G101 source changed",
    )
    require("G101_RETAINS_ONLY_THE_CORRECTED_OBSERVER_CENTERED_TWO_SOURCE_QUERY" in by_id["G101"]["precedence_rule"], "G101 precedence absent")
    require(
        by_id["G102"]["current_status"]
        == "EXTERNALLY_VERIFIED_WITH_CAVEATS__COMPLETE_TWO_SOURCE_OBSERVABLE_EVALUATOR_DERIVED__DIRECTION_IDENTIFICATION_QUERY_OWNED__ENDPOINT_DEPTH_CARRY_CONDITIONAL__PHYSICAL_HISTORY_AND_SOURCE_PAIR_MEASURE_OPEN",
        "G102 evaluator status regressed or promoted",
    )
    require(by_id["G102"]["epistemic_label"] == "MIXED", "G102 evaluator label changed")
    require("source one and two point measures" in by_id["G102"]["open_scope"], "G102 source measure promoted")
    require("physical complete history" in by_id["G102"]["open_scope"], "G102 history promoted")
    require("conditional evaluator called BAO prediction" in by_id["G102"]["forbidden_regression"], "G102 prediction guard absent")
    require("observer-local h reused as accumulated redshift" in by_id["G102"]["forbidden_regression"], "G102 endpoint guard absent")
    require("image/support qualification dropped" in by_id["G102"]["forbidden_regression"], "G102 support guard absent")
    require(
        by_id["G102"]["controlling_source"]
        == "udt_bao_G102_complete_two_source_observable_map_2026-08-15/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G102 source changed",
    )
    require("G102_FRESH_SEALED_REVIEW_REPLAYS_THE_EXACT_TWO_SOURCE_JOIN" in by_id["G102"]["precedence_rule"], "G102 precedence absent")
    require(
        by_id["G103"]["current_status"].startswith(
            "EXTERNALLY_VERIFIED_WITH_CAVEATS__LOCAL_REGULAR_ZERO_AND_FIRST_JET_OBSERVABLE_SURJECTION_DERIVED"
        ),
        "G103 restriction status regressed or promoted",
    )
    require(by_id["G103"]["epistemic_label"] == "MIXED", "G103 restriction label changed")
    require("global singular critical" in by_id["G103"]["open_scope"], "G103 global caveat promoted")
    require("bootstrap or joint source-history" in by_id["G103"]["open_scope"], "G103 bootstrap caveat promoted")
    require("source-bounded local result called a generic no-go" in by_id["G103"]["forbidden_regression"], "G103 no-go guard absent")
    require(
        by_id["G103"]["controlling_source"]
        == "udt_bao_G103_source_independent_restriction_ownership_audit_2026-08-15/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G103 source changed",
    )
    require("G103_FRESH_SEALED_REVIEW_REPRODUCES_LOCAL_ZERO_AND_FIRST_JET_SURJECTION" in by_id["G103"]["precedence_rule"], "G103 precedence absent")
    require(
        by_id["G104"]["current_status"].startswith(
            "EXTERNALLY_VERIFIED_WITH_CAVEATS__FACTORIZED_REGULAR_KALEIDOSCOPE_NULL_DERIVED"
        ),
        "G104 kaleidoscope status regressed or promoted",
    )
    require(by_id["G104"]["epistemic_label"] == "MIXED", "G104 kaleidoscope label changed")
    require("physical nonzero one-point modulation m" in by_id["G104"]["open_scope"], "G104 modulation promoted")
    require("nonfactorizing positive connected operator H" in by_id["G104"]["open_scope"], "G104 connected operator promoted")
    require("dormant coefficients activated before a basis exists" in by_id["G104"]["forbidden_regression"], "G104 coefficient guard absent")
    require("null source posit called metric-derived" in by_id["G104"]["forbidden_regression"], "G104 source-posit guard absent")
    require(
        by_id["G104"]["controlling_source"]
        == "udt_bao_G104_kaleidoscope_forward_operator_2026-08-15/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G104 source changed",
    )
    require("G104_FRESH_SEALED_REVIEW_REPRODUCES_THE_FACTORIZED_NULL" in by_id["G104"]["precedence_rule"], "G104 precedence absent")
    require(
        by_id["G105"]["current_status"].startswith(
            "EXTERNALLY_VERIFIED_WITH_CAVEATS__COMPLETE_ORCHESTRA_ONE_POINT_OBSERVER_ARTIFACT_CHANNEL_DERIVED_CONDITIONALLY"
        ),
        "G105 Jacobian artifact status regressed or promoted",
    )
    require(by_id["G105"]["epistemic_label"] == "MIXED", "G105 Jacobian artifact label changed")
    require("physical complete history and relation family" in by_id["G105"]["open_scope"], "G105 history promoted")
    require("actual survey-random projection" in by_id["G105"]["open_scope"], "G105 reference projection promoted")
    require("global nonfactorizing H" in by_id["G105"]["open_scope"], "G105 H promoted")
    require("conditional existence witness called a physical BAO prediction" in by_id["G105"]["forbidden_regression"], "G105 prediction guard absent")
    require("coefficients activated before a selected basis" in by_id["G105"]["forbidden_regression"], "G105 coefficient guard absent")
    require(
        by_id["G105"]["controlling_source"]
        == "udt_bao_G105_complete_orchestra_two_route_lift_2026-08-15/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G105 source changed",
    )
    require("G105_FRESH_SEALED_REVIEW_REPRODUCES_THE_FACTORIZED_NULL" in by_id["G105"]["precedence_rule"], "G105 precedence absent")
    require(
        by_id["G106"]["current_status"].startswith(
            "EXTERNALLY_VERIFIED_WITH_CAVEATS__COMPLETE_SKY_DEPTH_REFERENCE_PROJECTOR_DERIVED_CONDITIONALLY"
        ),
        "G106 sky-depth projector status regressed or promoted",
    )
    require(by_id["G106"]["epistemic_label"] == "MIXED", "G106 projector label changed")
    require("physical complete history and common all-sector realization" in by_id["G106"]["open_scope"], "G106 history promoted")
    require("exact finite random catalog weight and stratum projection" in by_id["G106"]["open_scope"], "G106 finite reference promoted")
    require("angular mode basis and coefficients" in by_id["G106"]["open_scope"], "G106 coefficients promoted")
    require("pure radial abundance called an observable angular pattern" in by_id["G106"]["forbidden_regression"], "G106 radial-null guard absent")
    require("constructive P2 witness called a physical history or BAO prediction" in by_id["G106"]["forbidden_regression"], "G106 witness guard absent")
    require("independent per-window retuning" in by_id["G106"]["forbidden_regression"], "G106 one-history guard absent")
    require("ideal reference operator called the exact finite survey pipeline" in by_id["G106"]["forbidden_regression"], "G106 finite-pipeline guard absent")
    require(
        by_id["G106"]["controlling_source"]
        == "udt_bao_G106_complete_sky_depth_reference_projection_2026-08-15/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G106 source changed",
    )
    require("G106_FRESH_SEALED_REVIEW_REPLAYS_ALL_FOUR_EXECUTABLES" in by_id["G106"]["precedence_rule"], "G106 precedence absent")
    require(
        by_id["G107"]["current_status"].startswith(
            "EXTERNALLY_VERIFIED_WITH_CAVEATS__CONSTANT_ZERO_ORDER_O2_SO2_EXTENSION_CENSUS_COMPLETE"
        ),
        "G107 representation census status regressed or promoted",
    )
    require(by_id["G107"]["epistemic_label"] == "MIXED", "G107 census label changed")
    require("physical active action and E/J carry" in by_id["G107"]["open_scope"], "G107 active carry promoted")
    require("field-dependent or query-reduced generators" in by_id["G107"]["open_scope"], "G107 field-dependent scope silently closed")
    require("coefficients" in by_id["G107"]["open_scope"], "G107 coefficient scope promoted")
    require("constant bounded census called the complete orchestra score" in by_id["G107"]["forbidden_regression"], "G107 score-promotion guard absent")
    require("screen dilation a fitted or promoted as physical" in by_id["G107"]["forbidden_regression"], "G107 dilation-promotion guard absent")
    require("complete determinant pairing or exchange silently promoted" in by_id["G107"]["forbidden_regression"], "G107 complete-gate guard absent")
    require(
        by_id["G107"]["controlling_source"]
        == "udt_complete_reciprocal_representation_extension_census_2026-08-16/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G107 source changed",
    )
    require("G107_FRESH_SEALED_REVIEW_AND_CORRECTED_FOLLOWUP_VERIFY" in by_id["G107"]["precedence_rule"], "G107 precedence absent")
    require(
        by_id["G108"]["current_status"].startswith(
            "EXTERNALLY_VERIFIED_WITH_CAVEATS__CONDITIONAL_SCREEN_DILATION_RATE_DERIVED"
        ),
        "G108 screen propagation status regressed or promoted",
    )
    require(by_id["G108"]["epistemic_label"] == "MIXED", "G108 label changed")
    require("delta(lambda) ownership" in by_id["G108"]["open_scope"], "G108 depth map promoted")
    require("initial screen and branch" in by_id["G108"]["open_scope"], "G108 initial data promoted")
    require("universal identification" in by_id["G108"]["open_scope"], "G108 query tie promoted")
    require("automatically called the physical Jacobi map" in by_id["G108"]["forbidden_regression"], "G108 type-tie guard absent")
    require("universal distance-only law" in by_id["G108"]["forbidden_regression"], "G108 distance-law guard absent")
    require("G68 affine rates called dimensionless G107 coefficients" in by_id["G108"]["forbidden_regression"], "G108 unit guard absent")
    require("while shear survives" in by_id["G108"]["forbidden_regression"], "G108 full-family guard absent")
    require(
        by_id["G108"]["controlling_source"]
        == "udt_complete_screen_jacobi_riccati_propagation_atlas_2026-08-16/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G108 source changed",
    )
    require("G108_FRESH_SEALED_REVIEW_AND_CORRECTED_FOLLOWUP_VERIFY" in by_id["G108"]["precedence_rule"], "G108 precedence absent")
    require(
        by_id["G109"]["current_status"].startswith(
            "EXTERNALLY_VERIFIED_WITH_CAVEATS__CONDITIONAL_SAME_QUERY_DEPTH_JOIN_DERIVED"
        ),
        "G109 same-query depth status regressed or promoted",
    )
    require(by_id["G109"]["epistemic_label"] == "MIXED", "G109 label changed")
    require("physical complete metric history and observer query" in by_id["G109"]["open_scope"], "G109 history/query promoted")
    require("branch and initial screen" in by_id["G109"]["open_scope"], "G109 branch/initial data promoted")
    require("global endpoint descent" in by_id["G109"]["open_scope"], "G109 global descent promoted")
    require("conditional same-query endpoint depth called a universal spacetime scalar" in by_id["G109"]["forbidden_regression"], "G109 universal-scalar guard absent")
    require("matched middle calibration omitted" in by_id["G109"]["forbidden_regression"], "G109 middle-reset guard absent")
    require("through dot(phi_pair)=0" in by_id["G109"]["forbidden_regression"], "G109 turning-point guard absent")
    require("through det(W)=0" in by_id["G109"]["forbidden_regression"], "G109 caustic guard absent")
    require(
        by_id["G109"]["controlling_source"]
        == "udt_same_query_terminal_depth_screen_propagation_join_2026-08-16/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G109 source changed",
    )
    require("G109_TWO_SEALED_REVIEWS_VERIFY" in by_id["G109"]["precedence_rule"], "G109 precedence absent")
    require(
        by_id["G110"]["current_status"].startswith(
            "BLIND_VERIFIED_WITH_CAVEATS__OBSERVER_EXPONENTIAL_FULL_DIFFERENTIAL_RECONSTRUCTION_DERIVED_CONDITIONALLY"
        ),
        "G110 full-differential status regressed or promoted",
    )
    require(by_id["G110"]["epistemic_label"] == "MIXED", "G110 label changed")
    require(
        "POINT_OBSERVER_FULL_DIFFERENTIAL" in by_id["G110"]["active_use"],
        "G110 active use changed",
    )
    for token in (
        "physical complete metric history",
        "time-dependent celestial trivialization",
        "global endpoint preimage",
        "actual complete UDT mixed-block replay",
    ):
        require(token in by_id["G110"]["open_scope"], f"G110 open scope promoted: {token}")
    for token in (
        "equal 2x2 size called intrinsic equality",
        "rank-two Jacobi map",
        "universal sky propagation coordinate",
        "basis-free identity",
        "G93 terminal or G108 Jacobi algebra discarded",
    ):
        require(token in by_id["G110"]["forbidden_regression"], f"G110 guard absent: {token}")
    require(
        by_id["G110"]["controlling_source"]
        == "udt_observer_exponential_full_differential_type_audit_2026-08-16/AUDIT_REPORT.md",
        "G110 source changed",
    )
    require(
        "G110_REFINES_G93_G98_G103_G107_G108_G109" in by_id["G110"]["precedence_rule"],
        "G110 precedence absent",
    )
    require(
        by_id["G111"]["current_status"].startswith(
            "BLIND_VERIFIED_WITH_REPAIRS__G110_DISTINCT_PAIR_ANGULAR_AND_MIXED_BLOCKS_SURVIVE"
        ),
        "G111 nonflat replay status regressed or promoted",
    )
    require(by_id["G111"]["epistemic_label"] == "MIXED", "G111 label changed")
    require("physical ownership of R17" in by_id["G111"]["open_scope"], "G111 R17 ownership promoted")
    require("bounded 192 or 1152 census called all complete histories or skies" in by_id["G111"]["forbidden_regression"], "G111 bounded-scope guard absent")
    require(
        by_id["G111"]["controlling_source"]
        == "udt_g111_nonflat_r17_full_differential_replay_2026-08-16/AUDIT_REPORT.md",
        "G111 source changed",
    )
    require(
        by_id["G112"]["current_status"].startswith(
            "BLIND_VERIFIED_WITH_CAVEATS__FIXED_P1_FULL_DIFFERENTIAL_RETYPE_BIT_LEVEL_NONREGRESSIVE"
        ),
        "G112 SNe nonregression status regressed or promoted",
    )
    require(by_id["G112"]["epistemic_label"] == "MIXED", "G112 label changed")
    require("one complete metric and observer exponential jointly producing" in by_id["G112"]["open_scope"], "G112 one-F history promoted")
    require("pointwise algebraic identity called an independent physical prediction" in by_id["G112"]["forbidden_regression"], "G112 regression-identity guard absent")
    require("Pantheon called a holdout" in by_id["G112"]["forbidden_regression"], "G112 calibration guard absent")
    require(
        by_id["G112"]["controlling_source"]
        == "udt_g112_full_differential_dual_sne_invariance_2026-08-16/AUDIT_REPORT.md",
        "G112 source changed",
    )
    require(
        by_id["G113"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__ONE_FULL_OBSERVER_DIFFERENTIAL_IS_THE_SMALLEST_LOCAL_ASSEMBLY"
        ),
        "G113 orchestra synthesis status regressed or promoted",
    )
    require(by_id["G113"]["epistemic_label"] == "MIXED", "G113 label changed")
    require("physical complete time-live metric history" in by_id["G113"]["open_scope"], "G113 time-live history promoted")
    require("observed P1 null-cone chord promoted to a smooth static spatial phi profile" in by_id["G113"]["forbidden_regression"], "G113 null-cone/static guard absent")
    require("exact center singularity called rejection of P1 or UDT" in by_id["G113"]["forbidden_regression"], "G113 scoped-negative guard absent")
    require(
        by_id["G113"]["controlling_source"]
        == "udt_g113_metric_native_orchestra_whiteboard_2026-08-16/AUDIT_REPORT.md",
        "G113 source changed",
    )
    require(
        by_id["G114"]["current_status"].startswith(
            "BLIND_VERIFIED_WITH_CAVEATS__COMMON_SOURCE_FULL_PHASE_NETWORK_DERIVED_CONDITIONALLY"
        ),
        "G114 network status regressed or promoted",
    )
    require(by_id["G114"]["epistemic_label"] == "MIXED", "G114 label changed")
    require("physical complete time-live metric history" in by_id["G114"]["open_scope"], "G114 history promoted")
    require("physical matched-beam condition" in by_id["G114"]["open_scope"], "G114 source matching promoted")
    require("identity full-phase loop called physical beam alignment" in by_id["G114"]["forbidden_regression"], "G114 beam-alignment guard absent")
    require("Q direct sum Q used without affine frequency calibration" in by_id["G114"]["forbidden_regression"], "G114 affine guard absent")
    require(
        by_id["G114"]["controlling_source"]
        == "udt_g114_common_source_three_observer_network_2026-08-16/AUDIT_REPORT.md",
        "G114 source changed",
    )
    require(
        by_id["G115"]["current_status"].startswith(
            "BLIND_VERIFIED_WITH_CAVEATS__REGULAR_CENTRAL_TIMELIVE_PAIR_AND_PHASE_JETS_DERIVED"
        ),
        "G115 time-live jet status regressed or promoted",
    )
    require(by_id["G115"]["epistemic_label"] == "MIXED", "G115 label changed")
    require("physical complete history" in by_id["G115"]["open_scope"], "G115 history promoted")
    require("individual n ell b q called invariants" in by_id["G115"]["forbidden_regression"], "G115 residual-gauge guard absent")
    require("source frequency silently identified" in by_id["G115"]["forbidden_regression"], "G115 frequency/depth guard absent")
    require(
        by_id["G115"]["controlling_source"]
        == "udt_g115_regular_timelive_spherical_source_boundary_jet_census_2026-08-16/AUDIT_REPORT.md",
        "G115 source changed",
    )
    require(
        by_id["G116"]["current_status"].startswith(
            "BLIND_VERIFIED_WITH_CAVEATS__COEFFICIENT_FREE_METRIC_QUERY_JUNCTION_DERIVED_CONDITIONALLY"
        ),
        "G116 junction status regressed or promoted",
    )
    require(by_id["G116"]["epistemic_label"] == "MIXED", "G116 label changed")
    require("physical complete history" in by_id["G116"]["open_scope"], "G116 history promoted")
    require("catalog frequency-query adoption" in by_id["G116"]["open_scope"], "G116 query ownership promoted")
    require("universal z equals exp phi_pair" in by_id["G116"]["forbidden_regression"], "G116 live-query type guard absent")
    require("full R2 character theorem applied to lower-dimensional co-descent" in by_id["G116"]["forbidden_regression"], "G116 theorem-scope guard absent")
    require(
        by_id["G116"]["controlling_source"]
        == "udt_g116_calibrated_frequency_terminal_pair_junction_2026-08-16/AUDIT_REPORT.md",
        "G116 source changed",
    )
    require(
        by_id["G117"]["current_status"].startswith(
            "BLIND_VERIFIED_WITH_CAVEATS__FROZEN_P1_DUAL_SNE_NUMERICS_PRESERVED"
        ),
        "G117 SNe regrade status regressed or promoted",
    )
    require(by_id["G117"]["epistemic_label"] == "MIXED", "G117 label changed")
    require("physical complete history" in by_id["G117"]["open_scope"], "G117 history promoted")
    require(
        "direct mapping from release coordinate" in by_id["G117"]["open_scope"],
        "G117 release-coordinate ownership promoted",
    )
    require(
        "zCMB or zHD called raw one-ray ratios" in by_id["G117"]["forbidden_regression"],
        "G117 release-coordinate type guard absent",
    )
    require(
        "G116 local witness extrapolated across SNe" in by_id["G117"]["forbidden_regression"],
        "G117 local-to-global guard absent",
    )
    require(
        by_id["G117"]["controlling_source"]
        == "udt_g117_operational_frequency_dual_sne_regrade_2026-08-16/AUDIT_REPORT.md",
        "G117 source changed",
    )
    require(
        by_id["G118"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__ONE_FULL_DF_MINIMAL_LOCAL_POINT_OBSERVER_ASSEMBLY"
        ),
        "G118 scaffolding-removal status regressed or promoted",
    )
    require(by_id["G118"]["epistemic_label"] == "MIXED", "G118 label changed")
    require(
        "arbitrary finite-radius time-live proof" in by_id["G118"]["open_scope"],
        "G118 finite-radius theorem promoted",
    )
    require(
        "finite-radius D_sky equals R O called already derived"
        in by_id["G118"]["forbidden_regression"],
        "G118 finite-radius scope guard absent",
    )
    require(
        "interface fiber called metric gauge" in by_id["G118"]["forbidden_regression"],
        "G118 interface-fiber type guard absent",
    )
    require(
        by_id["G118"]["controlling_source"]
        == "udt_g118_metric_native_scaffolding_removal_whiteboard_2026-08-16/AUDIT_REPORT.md",
        "G118 source changed",
    )
    require(
        by_id["G119"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__FINITE_RADIUS_TIMELIVE_CENTRAL_SPHERICAL_SCREEN_THEOREM_DERIVED"
        ),
        "G119 finite-radius screen status regressed or promoted",
    )
    require(by_id["G119"]["epistemic_label"] == "MIXED", "G119 label changed")
    require(
        "displaced observers" in by_id["G119"]["open_scope"],
        "G119 central-observer scope promoted",
    )
    require(
        "D_sky equals R O promoted outside central radial point-observer spherical class"
        in by_id["G119"]["forbidden_regression"],
        "G119 scope guard absent",
    )
    require(
        "transfer derived" in by_id["G119"]["forbidden_regression"],
        "G119 transfer guard absent",
    )
    require(
        by_id["G119"]["controlling_source"]
        == "udt_g119_finite_radius_timelive_spherical_screen_theorem_2026-08-16/AUDIT_REPORT.md",
        "G119 source changed",
    )
    require(
        by_id["G120"]["current_status"].startswith(
            "BLIND_VERIFIED_WITH_CAVEATS__G119_DA_EQUALS_R_PLUS_IMPORTED_ETA_ONE_EPSILON_ONE_OVER_Z"
        ),
        "G120 conditional SNe radius retyping regressed or promoted",
    )
    require(by_id["G120"]["epistemic_label"] == "MIXED", "G120 label changed")
    require(
        "native UDT carrier" in by_id["G120"]["open_scope"],
        "G120 native-light boundary absent",
    )
    require(
        "R_P1 extended into zero less than Z less than one"
        in by_id["G120"]["forbidden_regression"],
        "G120 outgoing-domain guard absent",
    )
    require(
        "formal n X_eff limit called measured or Xmax"
        in by_id["G120"]["forbidden_regression"],
        "G120 Xmax guard absent",
    )
    require(
        by_id["G120"]["controlling_source"]
        == "udt_g120_exact_screen_imported_transfer_dual_sne_recomposition_2026-08-16/AUDIT_REPORT.md",
        "G120 source changed",
    )
    require(
        by_id["G121"]["current_status"].startswith(
            "BLIND_VERIFIED_WITH_CAVEATS__LOCAL_CAUSAL_COMPOSITION_IDENTITIES_ONLY"
        ),
        "G121 causal/pair closure status regressed or promoted",
    )
    require(by_id["G121"]["epistemic_label"] == "MIXED", "G121 label changed")
    require(
        "physical metric-to-direct-pair relation family" in by_id["G121"]["open_scope"],
        "G121 metric-to-pair owner promoted",
    )
    require(
        "antisymmetric edges called a cocycle before triangle closure"
        in by_id["G121"]["forbidden_regression"],
        "G121 noncircular descent guard absent",
    )
    require(
        "direct pair differential multiplied by four-dimensional phase map without common carrier"
        in by_id["G121"]["forbidden_regression"],
        "G121 mixed-carrier type guard absent",
    )
    require(
        "pair-scalar descent said to flatten screen holonomy"
        in by_id["G121"]["forbidden_regression"],
        "G121 screen-holonomy guard absent",
    )
    require(
        by_id["G121"]["controlling_source"]
        == "udt_g121_copresent_reciprocal_causal_history_consistency_2026-08-16/AUDIT_REPORT.md",
        "G121 source changed",
    )
    require(
        by_id["G122"]["current_status"].startswith(
            "BLIND_VERIFIED_WITH_CAVEATS__COMMON_OBSERVER_EXPONENTIAL_PATHWISE_DEPENDENCY_RECORD"
        ),
        "G122 common-dependency status regressed or promoted",
    )
    require(by_id["G122"]["epistemic_label"] == "MIXED", "G122 label changed")
    require(
        "independent direct A-B co-present immersion" in by_id["G122"]["open_scope"],
        "G122 direct-pair open boundary absent",
    )
    require(
        "bounded O2 no-go extended to full-jet screen or mixed covariants"
        in by_id["G122"]["forbidden_regression"],
        "G122 bounded no-go scope guard absent",
    )
    require(
        "G116 local O(R2) junction called a full square or finite-radius law"
        in by_id["G122"]["forbidden_regression"],
        "G122 local-junction guard absent",
    )
    require(
        "direct A-B pair map called analyzed" in by_id["G122"]["forbidden_regression"],
        "G122 direct-map guard absent",
    )
    require(
        by_id["G122"]["controlling_source"]
        == "udt_g122_mixed_causal_copresent_common_carrier_2026-08-16/AUDIT_REPORT.md",
        "G122 source changed",
    )
    require(
        by_id["G123"]["current_status"].startswith(
            "BLIND_VERIFIED_WITH_REPAIRS__DECLARED_COMMON_EVENT_INCIDENCE_RELATION"
        ),
        "G123 declared-query incidence status regressed or promoted",
    )
    require(by_id["G123"]["epistemic_label"] == "MIXED", "G123 label changed")
    require(
        "universal physical meaning of co-presence" in by_id["G123"]["open_scope"],
        "G123 universal co-presence boundary absent",
    )
    require(
        "declared common-event query called universal co-presence"
        in by_id["G123"]["forbidden_regression"],
        "G123 query-scope guard absent",
    )
    require(
        "basis-free physical mixing magnitude"
        in by_id["G123"]["forbidden_regression"],
        "G123 split-relative mixing guard absent",
    )
    require(
        "regular multiple preimages conflated with nontransverse singular fibers"
        in by_id["G123"]["forbidden_regression"],
        "G123 regular-versus-singular guard absent",
    )
    require(
        "four-dimensional query tangent graph called full Jacobi phase"
        in by_id["G123"]["forbidden_regression"],
        "G123 query-tangent/phase guard absent",
    )
    require(
        "no history selector in declared test called universal no-go"
        in by_id["G123"]["forbidden_regression"],
        "G123 bounded selector-negative guard absent",
    )
    require(
        by_id["G123"]["controlling_source"]
        == "udt_g123_direct_copresent_incidence_relation_2026-08-16/AUDIT_REPORT.md",
        "G123 source changed",
    )
    require(
        by_id["G124"]["current_status"].startswith(
            "BLIND_VERIFIED_WITH_REPAIRS__EXACT_FINITE_RADIUS_KAPPA_PHI_SOURCE_CLOCK_JUNCTION"
        ),
        "G124 finite-radius junction status regressed or promoted",
    )
    require(by_id["G124"]["epistemic_label"] == "MIXED", "G124 label changed")
    require(
        "physical complete metric history" in by_id["G124"]["open_scope"],
        "G124 history boundary absent",
    )
    require(
        "endpoint source-clock" in by_id["G124"]["open_scope"],
        "G124 source-clock boundary absent",
    )
    require(
        "conditional normalized radial-null central-spherical theorem called universal observer law"
        in by_id["G124"]["forbidden_regression"],
        "G124 query-scope guard absent",
    )
    require(
        "kappa expansion magnitude treated as signed orientation"
        in by_id["G124"]["forbidden_regression"],
        "G124 orientation/magnitude guard absent",
    )
    require(
        "areal turning said to prove frequency finiteness or divergence"
        in by_id["G124"]["forbidden_regression"],
        "G124 turning-point guard absent",
    )
    require(
        "initial observer vertex conflated with later spherical caustic"
        in by_id["G124"]["forbidden_regression"],
        "G124 vertex/caustic guard absent",
    )
    require(
        "active fixed-label phi paired with quotient chi or vice versa"
        in by_id["G124"]["forbidden_regression"],
        "G124 matched-clock guard absent",
    )
    require(
        by_id["G124"]["controlling_source"]
        == "udt_g124_finite_radius_live_observer_transition_junction_2026-08-16/AUDIT_REPORT.md",
        "G124 source changed",
    )
    require(
        by_id["G125"]["current_status"].startswith(
            "BLIND_VERIFIED_WITH_REPAIRS__EXACT_CONDITIONAL_SNE_TOTAL_SCORE_DERIVED"
        ),
        "G125 total-score status regressed or promoted",
    )
    require(by_id["G125"]["epistemic_label"] == "MIXED", "G125 label changed")
    require(
        "terminal phi screen-rate and source-clock allocation"
        in by_id["G125"]["open_scope"],
        "G125 allocation boundary absent",
    )
    require(
        "conditional P1 total score called a universal live UDT history constraint"
        in by_id["G125"]["forbidden_regression"],
        "G125 conditional-history guard absent",
    )
    require(
        "exact frozen functional continuation called observational support outside evaluated SNe range"
        in by_id["G125"]["forbidden_regression"],
        "G125 observational-range guard absent",
    )
    require(
        "terminal allocation witnesses called realized histories"
        in by_id["G125"]["forbidden_regression"],
        "G125 terminal/global guard absent",
    )
    require(
        "Rinf called Xmax" in by_id["G125"]["forbidden_regression"],
        "G125 Xmax guard absent",
    )
    require(
        "likelihoods claimed newly revalidated rather than unchanged by identity"
        in by_id["G125"]["forbidden_regression"],
        "G125 anti-loop guard absent",
    )
    require(
        by_id["G125"]["controlling_source"]
        == "udt_g125_exact_sne_score_history_recomposition_2026-08-16/AUDIT_REPORT.md",
        "G125 source changed",
    )
    require(
        by_id["G126"]["current_status"].startswith(
            "BLIND_VERIFIED_WITH_REPAIRS__NO_CURRENT_R5_TO_K_OR_PHASE_BRIDGE"
        ),
        "G126 angular bridge status regressed or promoted",
    )
    require(by_id["G126"]["epistemic_label"] == "MIXED", "G126 label changed")
    require(
        "metric-owned nonspherical or displaced query on the same complete history"
        in by_id["G126"]["open_scope"],
        "G126 same-history bridge boundary absent",
    )
    require(
        "bounded current-bridge negative called a universal no-go"
        in by_id["G126"]["forbidden_regression"],
        "G126 bounded-negative guard absent",
    )
    require(
        "R5 two-point curve inverted to K or phase"
        in by_id["G126"]["forbidden_regression"],
        "G126 two-point inversion guard absent",
    )
    require(
        "fitting R5 used to manufacture bridge"
        in by_id["G126"]["forbidden_regression"],
        "G126 no-fit bridge guard absent",
    )
    require(
        "SNe comparison dataset called a metric branch history owner or selector"
        in by_id["G126"]["forbidden_regression"],
        "G126 SNe category guard absent",
    )
    require(
        by_id["G126"]["controlling_source"]
        == "udt_g126_angular_lane_same_query_bridge_2026-08-16/AUDIT_REPORT.md",
        "G126 source changed",
    )
    require(
        by_id["G127"]["current_status"].startswith(
            "BLIND_VERIFIED__LOCAL_SAME_HISTORY_RADIAL_TILTED_SCREEN_EMERGENCE_DERIVED"
        ),
        "G127 same-history screen result regressed or promoted",
    )
    require(by_id["G127"]["epistemic_label"] == "MIXED", "G127 label changed")
    require(
        "finite affine and time-live propagation" in by_id["G127"]["open_scope"],
        "G127 finite-propagation boundary absent",
    )
    require(
        "tidal eigenvalue contrast called optical shear"
        in by_id["G127"]["forbidden_regression"],
        "G127 tidal/shear type guard absent",
    )
    require(
        "shared finite-radius radial query called literal G119 center vertex"
        in by_id["G127"]["forbidden_regression"],
        "G127 observer-query type guard absent",
    )
    require(
        "supplied witness phi called the selected physical history"
        in by_id["G127"]["forbidden_regression"],
        "G127 history-selection guard absent",
    )
    require(
        by_id["G127"]["controlling_source"]
        == "udt_g127_same_history_radial_displaced_screen_emergence_2026-08-16/AUDIT_REPORT.md",
        "G127 source changed",
    )
    require(
        by_id["G128"]["current_status"].startswith(
            "EXTERNALLY_VERIFIED_BOUNDED__SECOND_FOLLOWUP_PASS"
        ),
        "G128 finite-path screen result regressed or promoted",
    )
    require(by_id["G128"]["epistemic_label"] == "MIXED", "G128 label changed")
    require(
        "complete nonspherical coframe propagation" in by_id["G128"]["open_scope"],
        "G128 nonspherical-completion boundary absent",
    )
    require(
        "free H0-H3 certification histories called selected physical histories"
        in by_id["G128"]["forbidden_regression"],
        "G128 history-selection guard absent",
    )
    require(
        "bounded all-family observation called a universal theorem"
        in by_id["G128"]["forbidden_regression"],
        "G128 bounded-observation guard absent",
    )
    require(
        "no caustic in the finite interval called global caustic freedom"
        in by_id["G128"]["forbidden_regression"],
        "G128 global-caustic guard absent",
    )
    require(
        "bounded second-followup pass called universal physical validation"
        in by_id["G128"]["forbidden_regression"],
        "G128 bounded-second-followup guard absent",
    )
    require(
        by_id["G128"]["controlling_source"]
        == "udt_g128_finite_path_timelive_radial_tilted_screen_2026-08-16/AUDIT_REPORT.md",
        "G128 source changed",
    )
    require(
        by_id["G129"]["current_status"].startswith(
            "FRESH_ADVERSARIAL_FOLLOWUP_PASS__PAIR_NETWORK_METRIC_FAITHFUL_IFF_RANK_TEN"
        ),
        "G129 relational-network faithfulness result regressed or promoted",
    )
    require(by_id["G129"]["epistemic_label"] == "MIXED", "G129 label changed")
    require(
        "founding ownership of rank-complete calibrated pair family"
        in by_id["G129"]["open_scope"],
        "G129 founding-ownership boundary absent",
    )
    require(
        "rank-complete reconstruction called derivation of network values"
        in by_id["G129"]["forbidden_regression"],
        "G129 supplied-values guard absent",
    )
    require(
        "quiet middle and endpoint behavior called unique continuation"
        in by_id["G129"]["forbidden_regression"],
        "G129 continuation guard absent",
    )
    require(
        by_id["G129"]["controlling_source"]
        == "udt_g129_copresent_relational_network_faithfulness_2026-08-16/AUDIT_REPORT.md",
        "G129 source changed",
    )
    require(
        by_id["G130"]["current_status"].startswith(
            "FRESH_ADVERSARIAL_FOLLOWUP_PASS__COPRESENCE_DENOTES_EVENT_COMEMBERSHIP_IN_SUPPLIED_S"
        ),
        "G130 co-presence/network ownership result regressed or promoted",
    )
    require(by_id["G130"]["epistemic_label"] == "MIXED", "G130 label changed")
    require(
        "physical query family and calibrated plane embeddings" in by_id["G130"]["open_scope"],
        "G130 query-family ownership boundary absent",
    )
    require(
        "co-presence said to select or construct S or its domain"
        in by_id["G130"]["forbidden_regression"],
        "G130 conditional co-membership guard absent",
    )
    require(
        "all-plane certification family called a derived physical observer population"
        in by_id["G130"]["forbidden_regression"],
        "G130 certification-domain guard absent",
    )
    require(
        "compatible numerical matrices without known embeddings or overlap data called the metric"
        in by_id["G130"]["forbidden_regression"],
        "G130 typed representation-equivalence guard absent",
    )
    require(
        "terminal reciprocal depths called rank-complete without proof"
        in by_id["G130"]["forbidden_regression"],
        "G130 scalar-faithfulness guard absent",
    )
    require(
        by_id["G130"]["controlling_source"]
        == "udt_g130_copresence_rank_complete_network_ownership_2026-08-16/AUDIT_REPORT.md",
        "G130 source changed",
    )
    require(
        by_id["G131"]["current_status"].startswith(
            "FRESH_ADVERSARIAL_FOLLOWUP_PASS__ALL_PLANE_TERMINAL_SCALAR_CONFORMAL_FAITHFUL_ONLY"
        ),
        "G131 terminal-scalar conformal result regressed or promoted",
    )
    require(by_id["G131"]["epistemic_label"] == "MIXED", "G131 label changed")
    require(
        "physical ownership of the all-plane query family and scalar values"
        in by_id["G131"]["open_scope"],
        "G131 query/value ownership boundary absent",
    )
    require(
        "fixed-clock slice called all-plane coverage" in by_id["G131"]["forbidden_regression"],
        "G131 clock-tilt guard absent",
    )
    require(
        "equality on a lower-dimensional or unlabeled domain called conformal faithfulness"
        in by_id["G131"]["forbidden_regression"],
        "G131 shared-domain guard absent",
    )
    require(
        "positive conformal factor said to be fixed by c_E alone"
        in by_id["G131"]["forbidden_regression"],
        "G131 c_E common-scale guard absent",
    )
    require(
        "scalar readout common-scale blindness called scale-free UDT"
        in by_id["G131"]["forbidden_regression"],
        "G131 scale-free regression guard absent",
    )
    require(
        by_id["G131"]["controlling_source"]
        == "udt_g131_all_plane_terminal_reciprocal_scalar_faithfulness_2026-08-16/AUDIT_REPORT.md",
        "G131 source changed",
    )
    require(
        by_id["G132"]["current_status"].startswith(
            "FRESH_ADVERSARIAL_FOLLOWUP_PASS__FIXED_K_RECIPROCAL_TRANSFORMATION_HAS_NO_INTERNAL_COMMON_FACTOR"
        ),
        "G132 scale-type result regressed or promoted",
    )
    require(by_id["G132"]["epistemic_label"] == "MIXED", "G132 label changed")
    require(
        "query-independent physical two-density or overlap descent for fixed K"
        in by_id["G132"]["open_scope"],
        "G132 fixed-K descent boundary absent",
    )
    require(
        "fixed K representation normalization called physical conformal scale ownership"
        in by_id["G132"]["forbidden_regression"],
        "G132 representation/physical-scale guard absent",
    )
    require(
        "kappa_pair said to source or select scale rather than retain supplied h"
        in by_id["G132"]["forbidden_regression"],
        "G132 kappa ownership guard absent",
    )
    require(
        "areal coordinate called independently calibrated orbit area"
        in by_id["G132"]["forbidden_regression"],
        "G132 areal calibration guard absent",
    )
    require(
        "c_E and G_obs alone said to form a length"
        in by_id["G132"]["forbidden_regression"],
        "G132 dimensional-anchor guard absent",
    )
    require(
        by_id["G132"]["controlling_source"]
        == "udt_g132_common_scale_owner_and_anchor_audit_2026-08-16/AUDIT_REPORT.md",
        "G132 source changed",
    )
    require(
        by_id["G133"]["current_status"].startswith(
            "FRESH_ADVERSARIAL_FOLLOWUP_PASS__FIXED_K_INTERNAL_UNIMODULAR_DENSITY_DERIVED"
        ),
        "G133 fixed-K density result regressed or promoted",
    )
    require(by_id["G133"]["epistemic_label"] == "MIXED", "G133 label changed")
    require(
        "physical soldering and ownership of the complete observer network"
        in by_id["G133"]["open_scope"],
        "G133 physical-network ownership boundary absent",
    )
    require(
        "fixed K called a query-independent spacetime two-form physical scale or observer-network owner"
        in by_id["G133"]["forbidden_regression"],
        "G133 internal-K promotion guard absent",
    )
    require(
        "kappa_pair called an unrestricted scalar under independent endpoint retrivializations"
        in by_id["G133"]["forbidden_regression"],
        "G133 kappa density-weight guard absent",
    )
    require(
        "full-g bivector area bilinear called an alternating two-form"
        in by_id["G133"]["forbidden_regression"],
        "G133 area-bilinear type guard absent",
    )
    require(
        by_id["G133"]["controlling_source"]
        == "udt_g133_fixed_K_two_density_overlap_descent_2026-08-16/AUDIT_REPORT.md",
        "G133 source changed",
    )
    require(
        by_id["G134"]["current_status"].startswith(
            "FRESH_ADVERSARIAL_FOLLOWUP_PASS__AREA_BILINEAR_METRIC_FAITHFUL_UP_TO_SIGN"
        ),
        "G134 area-faithfulness result regressed or promoted",
    )
    require(by_id["G134"]["epistemic_label"] == "MIXED", "G134 label changed")
    require(
        "physical ownership of complete valued area or metric history" in by_id["G134"]["open_scope"],
        "G134 physical-history ownership boundary absent",
    )
    require(
        "individual plane self-areas called sufficient" in by_id["G134"]["forbidden_regression"],
        "G134 full-cross-area guard absent",
    )
    require(
        "local codimension eleven called eleven equations of motion"
        in by_id["G134"]["forbidden_regression"],
        "G134 metricity-versus-dynamics guard absent",
    )
    require(
        "faithfulness called a law selecting numerical metric values or one universe"
        in by_id["G134"]["forbidden_regression"],
        "G134 faithfulness-selection guard absent",
    )
    require(
        by_id["G134"]["controlling_source"]
        == "udt_g134_full_metric_area_history_reframe_audit_2026-08-17/AUDIT_REPORT.md",
        "G134 source changed",
    )
    require(
        by_id["G135"]["current_status"].startswith(
            "FRESH_ZERO_CONTEXT_FOLLOWUP_PASS__COMPLETE_PAIR_OWNS_ANCHORED_PROJECTIVE_RECIPROCAL_COORDINATE"
        ),
        "G135 projective pair readout regressed or promoted",
    )
    require(by_id["G135"]["epistemic_label"] == "MIXED", "G135 label changed")
    require(
        "physical normalized pair position is the anchored projective readout"
        in by_id["G135"]["open_scope"],
        "G135 constitutive-ownership boundary absent",
    )
    require(
        "chi called the unique physical distance or proper length"
        in by_id["G135"]["forbidden_regression"],
        "G135 physical-distance promotion guard absent",
    )
    require(
        "first-degree projective uniqueness promoted to unrestricted smooth uniqueness"
        in by_id["G135"]["forbidden_regression"],
        "G135 restricted-uniqueness guard absent",
    )
    require(
        "common-scale blindness called strong local CSN or scale-free UDT"
        in by_id["G135"]["forbidden_regression"],
        "G135 common-scale guard absent",
    )
    require(
        "x/Xmax=tanh(phi_pair) called unconditionally derived or numerically fixed"
        in by_id["G135"]["forbidden_regression"],
        "G135 Xmax constitutive guard absent",
    )
    require(
        by_id["G135"]["controlling_source"]
        == "udt_g135_projective_pair_separation_constitution_audit_2026-08-17/AUDIT_REPORT.md",
        "G135 source changed",
    )
    require(
        by_id["G136"]["current_status"].startswith(
            "FRESH_ADVERSARIAL_FOLLOWUP_PASS__SAME_NATIVE_MOBIUS_CONTINUOUS_ORDERED_POSITION_COORDINATES_ARE_TANH_K_PHI"
        ),
        "G136 continuous position classification regressed or promoted",
    )
    require(by_id["G136"]["epistemic_label"] == "MIXED", "G136 label changed")
    require(
        "owner adoption of physical normalized position as a continuous strictly increasing same-native-Mobius coordinate"
        in by_id["G136"]["open_scope"],
        "G136 owner-adoption boundary absent",
    )
    require(
        "chosen phi unit or c_E said to impose physical-position slope one"
        in by_id["G136"]["forbidden_regression"],
        "G136 normalization ownership guard absent",
    )
    require(
        "same-law classification called proof that physical position has that type"
        in by_id["G136"]["forbidden_regression"],
        "G136 classification-versus-constitution guard absent",
    )
    require(
        "tanh or projective coordinate named inside the minimal premise"
        in by_id["G136"]["forbidden_regression"],
        "G136 noncircular-premise guard absent",
    )
    require(
        "numerical/source replay called a second proof of the continuous theorem"
        in by_id["G136"]["forbidden_regression"],
        "G136 independent-replay scope guard absent",
    )
    require(
        by_id["G136"]["controlling_source"]
        == "udt_g136_copresent_projective_distance_constitution_2026-08-17/AUDIT_REPORT.md",
        "G136 source changed",
    )
    require(
        by_id["G137"]["current_status"].startswith(
            "OWNER_ADOPTED_WORKING_NORMALIZED_POSITION_CONSTITUTION__FRESH_G163_ADVERSARIAL_PASS_WITH_REPAIRS__SIGNED_CHI_EQUALS_TANH_PHI_PAIR"
        ),
        "G137 adopted position constitution regressed or promoted",
    )
    require(by_id["G137"]["epistemic_label"] == "MIXED", "G137 label changed")
    require(
        "numerical Xmax dimensional owner profile and global realization" in by_id["G137"]["open_scope"],
        "G137 Xmax owner boundary absent",
    )
    for guard in (
        "working normalized constitution called algebraically forced or canonized",
        "x equals Xmax chi called native or used to derive its supplied factor",
        "x or s called proper length areal radius signal distance universe size",
        "unsigned magnitudes composed without orientation",
        "conditional pair c_eff called local signal speed",
        "supplied pair realization network or history called selected",
    ):
        require(guard in by_id["G137"]["forbidden_regression"], f"G137 guard absent: {guard}")
    require(
        by_id["G137"]["controlling_source"]
        == "udt_g163_xmax_dependency_reversal_audit_2026-08-18/AUDIT_REPORT.md",
        "G137 source changed",
    )
    require(
        by_id["G138"]["current_status"].startswith(
            "FRESH_ADVERSARIAL_FOLLOWUP_PASS__ENDPOINT_DESCENT_IFF_ALL_MATCHED_CYCLE_RESIDUALS_VANISH"
        ),
        "G138 network descent classification regressed or promoted",
    )
    require(by_id["G138"]["epistemic_label"] == "MIXED", "G138 label changed")
    require(
        "endpoint-descended versus path-labelled global relation type" in by_id["G138"]["open_scope"],
        "G138 global relation-type fork absent",
    )
    for guard in (
        "finite observer-rooted chart set called a torsor for the full continuous group",
        "no coordinate root selected called proof no physical observer or feature can be distinguished",
        "any nonzero cycle called holonomy when routes are identified",
        "nonzero cycle called inconsistency when routes remain distinct",
        "Xmax value inferred from normalized closure",
        "scalar positional skeleton called full spacetime metric proper length",
    ):
        require(guard in by_id["G138"]["forbidden_regression"], f"G138 guard absent: {guard}")
    require(
        by_id["G138"]["controlling_source"]
        == "udt_g138_copresent_relational_position_network_descent_2026-08-17/AUDIT_REPORT.md",
        "G138 source changed",
    )
    require(
        by_id["G139"]["current_status"].startswith(
            "FRESH_ADVERSARIAL_FOLLOWUP_PASS__PROVISIONAL_ENDPOINT_POSITION_OWNER"
        ),
        "G139 provisional endpoint owner regressed or promoted",
    )
    require(by_id["G139"]["epistemic_label"] == "MIXED", "G139 label changed")
    for open_item in (
        "composition-and-inversion-compatible positional route congruence",
        "complete observer network values pair realizations routes branches and metric history",
        "singular null calibration-mismatched undefined and noncomposable strata",
        "numerical Xmax dimensional owner profile and global realization",
    ):
        require(open_item in by_id["G139"]["open_scope"], f"G139 open boundary absent: {open_item}")
    for guard in (
        "provisional owner called DERIVED CANON or universal selection",
        "endpoint constancy said to construct the quotient or prove closure",
        "categorical product called a physical metric decomposition or global fiber bundle",
        "path transport said to alter endpoint position inside one identified family",
        "angular screen mixing removed from the complete pullback or bolted on after phi_pair",
        "different terminal depths silently averaged absorbed into transport or left unlabelled",
        "bounded dichotomy extended to singular mismatched undefined or noncomposable cases",
        "zero positional loop return said to force trivial angular holonomy",
    ):
        require(guard in by_id["G139"]["forbidden_regression"], f"G139 guard absent: {guard}")
    require(
        by_id["G139"]["controlling_source"]
        == "udt_g139_endpoint_position_transport_join_2026-08-17/AUDIT_REPORT.md",
        "G139 source changed",
    )
    require(
        by_id["G140"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_FOLLOWUP_PASS__POOLED_RANK_TEN"
        ),
        "G140 bounded status regressed or promoted",
    )
    require(by_id["G140"]["epistemic_label"] == "MIXED", "G140 label changed")
    for open_item in (
        "physical ordered inverse observer query and congruent relation family",
        "generic varying-metric pointwise atlas",
        "numerical Xmax proper length physical scale and history",
    ):
        require(open_item in by_id["G140"]["open_scope"], f"G140 open boundary absent: {open_item}")
    for guard in (
        "pooled separated-strip rank called generic G129 pointwise rank completeness",
        "terminal bar_phi called an oriented depth",
        "affine strip reversal called the physical inverse query",
        "supplied delta lift called metric-derived",
        "arbitrary ell_0 called a physical scale or Xmax",
        "zero of eight sign lifts called a universal no-go",
        "same-metric controls called a selected universe",
    ):
        require(guard in by_id["G140"]["forbidden_regression"], f"G140 guard absent: {guard}")
    require(
        by_id["G140"]["controlling_source"]
        == "udt_g140_rank_complete_atlas_positional_congruence_2026-08-17/AUDIT_REPORT.md",
        "G140 source changed",
    )
    require(
        by_id["G141"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_FOLLOWUP_PASS__SUPPLIED_SHARED_CARRIER"
        ),
        "G141 bounded status regressed or promoted",
    )
    require(by_id["G141"]["epistemic_label"] == "MIXED", "G141 label changed")
    for open_item in (
        "physical identification with observer-pair inverse and G123 full chart transition",
        "derivation of shared carrier compatible endpoint family and matched calibration carry",
        "numerical Xmax proper length physical scale and history",
    ):
        require(open_item in by_id["G141"]["open_scope"], f"G141 open boundary absent: {open_item}")
    for guard in (
        "positive triangular factor called arbitrary-coordinate invariant or metric-canonical",
        "C_BA or D_BA called the full G123 transition",
        "independent endpoint planes called a realized common-event transition",
        "A-normalized constructed metric called a new physical pullback",
        "Phi difference called invariant under independent endpoint gauges",
        "nonzero channel coefficients called channel sensitivity without removal controls",
        "calibration algebra called selection of family history or physical inverse",
    ):
        require(guard in by_id["G141"]["forbidden_regression"], f"G141 guard absent: {guard}")
    require(
        by_id["G141"]["controlling_source"]
        == "udt_g141_endpoint_triangular_transition_inverse_join_2026-08-17/AUDIT_REPORT.md",
        "G141 source changed",
    )
    require(
        by_id["G142"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_FOLLOWUP_PASS__ON_SUPPLIED_REGULAR_ORDERED_BPLUS2"
        ),
        "G142 bounded status regressed or promoted",
    )
    require(by_id["G142"]["epistemic_label"] == "MIXED", "G142 label changed")
    for open_item in (
        "physical derivation or restriction to Bplus2",
        "physical tangent-plane soldering carry query family and history",
        "single-query versus cross-query carry ownership",
        "numerical Xmax proper length",
    ):
        require(open_item in by_id["G142"]["open_scope"], f"G142 open boundary absent: {open_item}")
    for guard in (
        "abstract two-channel representation called a derived physical carrier",
        "K called derived rather than posited",
        "carry neutrality called gauge invariant under independent endpoint gauges",
        "nonidentity neutral carry called recovery of G141 full transition",
        "Bplus2 called a derived physical restriction",
        "formal same-endpoint countermodel called two realized physical carries",
        "total C called universal physical law or selector",
    ):
        require(guard in by_id["G142"]["forbidden_regression"], f"G142 guard absent: {guard}")
    require(
        by_id["G142"]["controlling_source"]
        == "udt_g142_abstract_carrier_physical_carry_join_2026-08-17/AUDIT_REPORT.md",
        "G142 source changed",
    )
    require(
        by_id["G143"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_PASS__ONE_SUPPLIED_CALIBRATED_PAIR_CHART"
        ),
        "G143 bounded status regressed or promoted",
    )
    require(by_id["G143"]["epistemic_label"] == "MIXED", "G143 label changed")
    for open_item in (
        "physical selection of query realization or spanning chart",
        "cross-query cross-branch and network overlap or gluing",
        "universal path-independent tangent identity",
        "history Xmax proper length",
    ):
        require(open_item in by_id["G143"]["open_scope"], f"G143 open boundary absent: {open_item}")
    for guard in (
        "identity carry on coordinate coefficient model called coordinate-free tangent transport",
        "chart covariance called dynamics selection or metric history",
        "pair metric said not to own Levi-Civita transport along a supplied path",
        "local unique geodesic denied where its hypotheses hold",
        "nonidentity chart carry called new physical effect",
        "one query chart used to glue distinct queries or branches",
        "Bplus2 called derived physical restriction",
    ):
        require(guard in by_id["G143"]["forbidden_regression"], f"G143 guard absent: {guard}")
    require(
        by_id["G143"]["controlling_source"]
        == "udt_g143_single_pair_domain_carry_ownership_2026-08-17/AUDIT_REPORT.md",
        "G143 source changed",
    )
    require(
        by_id["G144"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_PASS__BRANCH_RESOLVED_EMBEDDED_OPEN_OVERLAP"
        ),
        "G144 bounded status regressed or promoted",
    )
    require(by_id["G144"]["epistemic_label"] == "MIXED", "G144 label changed")
    for open_item in (
        "physical population and selection of nonoverlapping relation sheets",
        "cross-branch gluing at self-intersections without branch labels",
        "physical query family complete metric history Xmax proper length",
    ):
        require(open_item in by_id["G144"]["open_scope"], f"G144 open boundary absent: {open_item}")
    for guard in (
        "branch-resolved overlap differential called a new force or nonisometric physical effect",
        "Lorentz-isometric overlap carry called positional depth",
        "positive triangular identity called a universal relation selector",
        "common endpoint observers called sufficient to identify interiors or create carry",
        "distinct sheets silently glued without overlap or branch labels",
    ):
        require(guard in by_id["G144"]["forbidden_regression"], f"G144 guard absent: {guard}")
    require(
        by_id["G144"]["controlling_source"]
        == "udt_g144_cross_query_overlap_carry_descent_2026-08-17/AUDIT_REPORT.md",
        "G144 source changed",
    )
    require(
        by_id["G145"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_PASS__RANK_COMPLETE_FULL_PULLBACK_VALUATION"
        ),
        "G145 bounded status regressed or promoted",
    )
    require(by_id["G145"]["epistemic_label"] == "MIXED", "G145 label changed")
    for open_item in (
        "physical query atlas calibrations numerical valuation and realization",
        "global topology singular null cut or non-Hausdorff strata",
        "numerical Xmax proper length and completion",
        "initial boundary observational or native value law",
    ):
        require(open_item in by_id["G145"]["open_scope"], f"G145 open boundary absent: {open_item}")
    for guard in (
        "two-dimensional pair sheets called a four-dimensional manifold atlas",
        "rank completeness called selection of query population numerical values evolution or one universe",
        "coherent relation network called literally identical to bare metric",
        "compatibility composition or causality called a numerical value law",
        "zero-jet orchestra called frozen after fixed nonzero cubic liveness",
        "cE and G called sufficient to form a length or profile",
        "reversible comparison equated with future causal propagation",
        "bounded local counterfamily promoted to a global no-go",
    ):
        require(guard in by_id["G145"]["forbidden_regression"], f"G145 guard absent: {guard}")
    require(
        by_id["G145"]["controlling_source"]
        == "udt_g145_copresent_relation_history_descent_equivalence_2026-08-17/AUDIT_REPORT.md",
        "G145 source changed",
    )
    require(
        by_id["G146"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_PASS__TWO_INEQUIVALENT_SMOOTH_SO3_COVARIANT"
        ),
        "G146 bounded status regressed or promoted",
    )
    require(by_id["G146"]["epistemic_label"] == "MIXED", "G146 label changed")
    for open_item in (
        "metric-derived physical three-position carrier and full observer-arrow lift",
        "rank-two solder sigma from directional sphere tangent to pair screen",
        "comparison of conjugated positional gyration with metric U_gamma",
    ):
        require(open_item in by_id["G146"]["open_scope"], f"G146 open boundary absent: {open_item}")
    for guard in (
        "Mobius or Einstein ball control selected as UDT physics",
        "reciprocal phi identified with Lorentz rapidity",
        "element inverse minus u called complete observer-arrow reversal",
        "three-dimensional position ball silently identified with rank-two pair screen",
        "algebraic gyration equated with U_gamma without a common carrier and typed path order",
    ):
        require(guard in by_id["G146"]["forbidden_regression"], f"G146 guard absent: {guard}")
    require(
        by_id["G146"]["controlling_source"]
        == "udt_g146_multidirectional_relational_position_composition_2026-08-17/AUDIT_REPORT.md",
        "G146 source changed",
    )
    require(
        by_id["G147"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_FOLLOWUP_PASS__WITHIN_DEFINED_QUERY_RELATIVE_REST_SPACE_LIFT"
        ),
        "G147 bounded status regressed or promoted",
    )
    require(by_id["G147"]["epistemic_label"] == "MIXED", "G147 label changed")
    for open_item in (
        "physical multidirectional three-position carrier and whether it is the query rest-space relation ball",
        "solder from an independently owned ball carrier including O2 freedom",
        "oriented solder and ordered-pair reversal",
        "cross-query middle-observer carry and comparison with U_gamma",
    ):
        require(open_item in by_id["G147"]["open_scope"], f"G147 open boundary absent: {open_item}")
    for guard in (
        "defined xi equals rho n called a derived physical three-position or spacetime displacement",
        "conditional rest-space identity called a universal metric solder",
        "O2 freedom called mere gauge before a common carrier is owned",
        "flag-preserving domain reparameterization called full calibrated-position covariance",
        "tangent screen said to retain rho sign or derive reversal",
        "conditional identity used to select a ball law equate gyration with U_gamma",
    ):
        require(guard in by_id["G147"]["forbidden_regression"], f"G147 guard absent: {guard}")
    require(
        by_id["G147"]["controlling_source"]
        == "udt_g147_pair_directional_metric_screen_solder_2026-08-17/AUDIT_REPORT.md",
        "G147 source changed",
    )
    require(
        by_id["G148"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_FOLLOWUP_PASS__WORKING_RELATION_FIRST_REPRESENTATION_ONLY"
        ),
        "G148 bounded status regressed or promoted",
    )
    require(by_id["G148"]["epistemic_label"] == "MIXED", "G148 label changed")
    for open_item in (
        "physical multidirectional carrier and independent O2 solder",
        "concrete Levi-Civita a_n Omega and dot phi computed from one common complete B Q S Y Z spacetime history and query",
        "realized amplitudes and their boundedness near neutral or asymptotic limits",
        "coincidence direction reversal cross-query carry U_gamma null cut singular and global strata",
    ):
        require(open_item in by_id["G148"]["open_scope"], f"G148 open boundary absent: {open_item}")
    for guard in (
        "working xi equals rho n called derived physical carrier displacement or proper length",
        "lambda matrix-family derivative identified with covariant query-clock flow",
        "coordinate projector derivative called independent derivation of Levi-Civita connection Omega or a_n",
        "sech squared or tanh coefficient limits called native physical loud quiet loud regime law without history amplitudes",
        "first-jet identity called equation of motion history selection Xmax law or downstream prediction",
    ):
        require(guard in by_id["G148"]["forbidden_regression"], f"G148 guard absent: {guard}")
    require(
        by_id["G148"]["controlling_source"]
        == "udt_g148_relation_first_pair_first_jet_decomposition_2026-08-17/AUDIT_REPORT.md",
        "G148 source changed",
    )
    require(
        by_id["G149"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_FOLLOWUP_PASS__EXPLICIT_SMOOTH_COMPLETE_SPACETIME_QUERY_WITNESS"
        ),
        "G149 bounded status regressed or promoted",
    )
    require(by_id["G149"]["epistemic_label"] == "MIXED", "G149 label changed")
    for open_item in (
        "physical multidirectional carrier and independent O2 solder",
        "relations involving other first-order objects",
        "next pair-frame jet metric curvature and Jacobi",
        "sigma-direction pair first jet",
        "physical history query family dynamics and selection",
    ):
        require(open_item in by_id["G149"]["open_scope"], f"G149 open boundary absent: {open_item}")
    for guard in (
        "one rational witness called selected physical history or universe",
        "registered liveness called universal dependence or a loud quiet loud law",
        "Y Z clock-direction controls called full two-direction pair-jet coverage",
        "fixture-specific lambda mismatch called a coordinate-invariant theorem",
        "exact first-jet identity called dynamics history selection Xmax law or downstream prediction",
    ):
        require(guard in by_id["G149"]["forbidden_regression"], f"G149 guard absent: {guard}")
    require(
        by_id["G149"]["controlling_source"]
        == "udt_g149_genuine_spacetime_pair_first_jet_join_2026-08-17/AUDIT_REPORT.md",
        "G149 source changed",
    )
    require(
        by_id["G150"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_FOLLOWUP_PASS__NO_NONTRIVIAL_UNIVERSAL_POINTWISE_ALGEBRAIC_RELATION"
        ),
        "G150 bounded status regressed or promoted",
    )
    require(by_id["G150"]["epistemic_label"] == "MIXED", "G150 label changed")
    for open_item in (
        "other first-order objects and unused jet kernel combinations",
        "physical query restrictions",
        "next pair-frame jet metric curvature Jacobi and differential relations",
        "global completion physical history dynamics regime amplitudes",
    ):
        require(open_item in by_id["G150"]["open_scope"], f"G150 open boundary absent: {open_item}")
    for guard in (
        "four-output surjectivity called exhaustion of first-order geometry",
        "absence of pointwise algebraic relation called no-go against differential curvature query global dynamical or regime laws",
        "flat counterfamily called evidence that curvature is irrelevant",
        "separate implementation replay called substantially independent",
        "phi zero pair-frame freedom called a nonzero positional chord",
    ):
        require(guard in by_id["G150"]["forbidden_regression"], f"G150 guard absent: {guard}")
    require(
        by_id["G150"]["controlling_source"]
        == "udt_g150_first_order_pair_chord_freedom_ceiling_2026-08-17/AUDIT_REPORT.md",
        "G150 source changed",
    )
    require(
        by_id["G151"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_FOLLOWUP_PASS__EXACT_GENERIC_SECOND_DERIVATIVE_DECOMPOSITION"
        ),
        "G151 bounded status regressed or promoted",
    )
    require(by_id["G151"]["epistemic_label"] == "MIXED", "G151 label changed")
    for open_item in (
        "whether complete pair immersion owns variational identification xi",
        "necessity versus exceptional nonzero C cancellation",
        "active screen and acceleration-gradient independent coordinate witness",
        "physical query population history dynamics regime amplitudes and selection",
    ):
        require(open_item in by_id["G151"]["open_scope"], f"G151 open boundary absent: {open_item}")
    for guard in (
        "terminal pair readout called a connecting or Jacobi field without smooth two-parameter query",
        "connecting C zero called necessary rather than canonical sufficient",
        "a_n retained nonzero in rho nonzero connecting family",
        "screen acceleration A called next jet rather than omitted first-order readout",
        "radial warped witness called active-screen or acceleration-gradient verification",
        "curvature commutator called field equation dynamics history selector force or regime law",
    ):
        require(guard in by_id["G151"]["forbidden_regression"], f"G151 guard absent: {guard}")
    require(
        by_id["G151"]["controlling_source"]
        == "udt_g151_pair_chord_generalized_deviation_join_2026-08-17/AUDIT_REPORT.md",
        "G151 source changed",
    )
    require(
        by_id["G152"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_PASS__PAIR_IMMERSION_OWNS_COORDINATE_AND_ORTHOGONAL_RULER_VARIATIONS"
        ),
        "G152 bounded status regressed or promoted",
    )
    require(by_id["G152"]["epistemic_label"] == "MIXED", "G152 label changed")
    for open_item in (
        "whether adopted pair-position semantics identifies xi with oriented metric ruler",
        "universal constancy and sufficiency of conditional Xmax candidate",
        "physical query population history dynamics regime amplitudes and selection",
        "numerical Xmax proper length areal radius",
    ):
        require(open_item in by_id["G152"]["open_scope"], f"G152 open boundary absent: {open_item}")
    for guard in (
        "pair immersion said to automatically own xi",
        "collinearity called equality of magnitude",
        "orthogonal ruler silently equated with coordinate variation when beta nonzero",
        "coordinate and normalized-u bracket coefficients confused",
        "equality said to imply connecting carry or carry said to imply equality",
        "conditional Xmax candidate called universal constant or physical value",
        "metric ruler called proper length or areal radius",
    ):
        require(guard in by_id["G152"]["forbidden_regression"], f"G152 guard absent: {guard}")
    require(
        by_id["G152"]["controlling_source"]
        == "udt_g152_pair_immersion_variational_chord_ownership_2026-08-17/AUDIT_REPORT.md",
        "G152 source changed",
    )
    require(
        by_id["G153"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__FRESH_G163_ADVERSARIAL_PASS_WITH_REPAIRS__FINITE_DIMENSIONAL_DISPLAY_NOT_METRIC_PROPER_LENGTH"
        ),
        "G153 bounded status regressed or promoted",
    )
    require(by_id["G153"]["epistemic_label"] == "MIXED", "G153 label changed")
    for open_item in (
        "physical history and query family",
        "Xmax realization profile modulation and numerical value",
        "proper length areal radius signal distance and unit-ruler calibration",
        "asymptotic regularity and global completion",
    ):
        require(open_item in by_id["G153"]["open_scope"], f"G153 open boundary absent: {open_item}")
    for guard in (
        "dchi identity called a dimensionful proper-length law",
        "finite dimensional display called local metric proper length or spacetime displacement",
        "G147 conditional lift promoted to physical chord",
        "Xmax silently inserted into the native kernel",
        "conditional live dXmax product rule erased",
        "sech squared coefficient alone called a physical loud quiet loud amplitude law",
        "exact differential called history selection dynamics global asymptote realization numerical Xmax",
        "common-scale covariance called scale-free metric physics or strong local CSN",
    ):
        require(guard in by_id["G153"]["forbidden_regression"], f"G153 guard absent: {guard}")
    require(
        by_id["G153"]["controlling_source"]
        == "udt_g163_xmax_dependency_reversal_audit_2026-08-18/AUDIT_REPORT.md",
        "G153 source changed",
    )
    require(
        by_id["G154"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__G163_REGRADING__COLD_EXTERNAL_REVIEW__INDEPENDENT_LOCAL_REPLAY_PASS__XMAX_INDEPENDENT_CONFORMAL_NETWORK_NONSELECTION"
        ),
        "G154 bounded status regressed or promoted",
    )
    require(by_id["G154"]["epistemic_label"] == "MIXED", "G154 label changed")
    for open_item in (
        "physical fixed-scale descent or scale carry law",
        "selected common-scale complete metric realization",
        "relation between additive depth and normalized clock or ruler rate",
        "diffeomorphism-natural nonidentity common-scale or realization admissibility law",
        "all-frame shared Xmax numerical value angular or bootstrap modulation",
    ):
        require(open_item in by_id["G154"]["open_scope"], f"G154 open boundary absent: {open_item}")
    for guard in (
        "normalized Mobius composition called derivation of one fixed dimensionful Xmax",
        "conditional fixed-scale consistency theorem promoted to ownership",
        "live dXmax discarded when a dimensional realization is supplied",
        "fixed-scale response probes called native kernel theorems",
        "sech squared coefficient alone called physical loud quiet loud response",
        "conformal twins called the same complete network or common scale called gauge",
        "reciprocal-position network faithfulness called complete-network realization selection",
        "endpoint kappa bookkeeping called universal physical descent",
        "compatibility metricity Cartan Bianchi causal overlap transport or rank identities called a nonidentity realization law",
        "bounded counterfamilies called physical realizations",
        "sign-paired witnesses called universal reversal without carried frame",
    ):
        require(guard in by_id["G154"]["forbidden_regression"], f"G154 guard absent: {guard}")
    require(
        by_id["G154"]["controlling_source"]
        == "udt_g163_xmax_dependency_reversal_audit_2026-08-18/AUDIT_REPORT.md",
        "G154 source changed",
    )
    require(
        by_id["G155"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__INTERNAL_ADVERSARIAL_REPAIR_FOLLOWUP_PASS__FROZEN_41_SOURCE_EQUATION_ROLE_CENSUS"
        ),
        "G155 bounded status regressed or promoted",
    )
    require(by_id["G155"]["epistemic_label"] == "MIXED", "G155 label changed")
    for open_item in (
        "positive scale line or torsor and lawful three-observer scale carry",
        "future native common-scale constraint evolution equation or joint relational law",
        "actual initial boundary or observational data",
        "singular null cut locus topology-changing and global-completion strata",
    ):
        require(open_item in by_id["G155"]["open_scope"], f"G155 open boundary absent: {open_item}")
    for guard in (
        "rank zero called proof that no native UDT scale law can exist",
        "common scale called gauge",
        "source-bounded role census widened beyond the frozen 41 sources",
        "finite initial data called sufficient without an evolution equation",
        "G121 supplied-edge closure called metric-only scale selection",
        "G134 metricity called history evolution",
        "G151 Jacobi principal part assigned to the metric",
        "fixed K reciprocal determinant promoted to physical volume",
    ):
        require(guard in by_id["G155"]["forbidden_regression"], f"G155 guard absent: {guard}")
    require(
        by_id["G155"]["controlling_source"]
        == "udt_g155_scale_sector_closure_whiteboard_2026-08-18/AUDIT_REPORT.md",
        "G155 source changed",
    )
    require(
        by_id["G156"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_REPAIR_FOLLOWUP_PASS__PREREGISTERED__INDEPENDENT_EXACT_REPLAY_PASS__CANONICAL_PAIR_HALF_DENSITY_DERIVED"
        ),
        "G156 bounded status regressed or promoted",
    )
    require(by_id["G156"]["epistemic_label"] == "MIXED", "G156 label changed")
    for open_item in (
        "physical nonisometric cross-query carry or path-labelled scale connection",
        "complete reciprocal scale shift screen and mixing carry closure",
        "nonidentity common-scale constraint evolution or joint relational law",
        "physical query population and history",
    ):
        require(open_item in by_id["G156"]["open_scope"], f"G156 open boundary absent: {open_item}")
    for guard in (
        "positive half-density section called a selected history fixed volume or common scale gauge",
        "conditional determinant character called a metric-selected physical cross-query carry",
        "zero scalar scale defect called full matrix carry closure",
        "determinant-one shear reciprocal or mixing data erased",
        "Levi-Civita or genuine overlap transport assigned nonzero scale dilation",
        "shared endpoints called an overlap",
    ):
        require(guard in by_id["G156"]["forbidden_regression"], f"G156 guard absent: {guard}")
    require(
        by_id["G156"]["controlling_source"]
        == "udt_g156_three_observer_scale_carry_audit_2026-08-18/AUDIT_REPORT.md",
        "G156 source changed",
    )
    require(
        by_id["G157"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_REPAIR_FOLLOWUP_PASS__PREREGISTERED__INDEPENDENT_EXACT_REPLAY_PASS__BPLUS2_UNIQUE_THREE_CHANNEL_FACTORIZATION"
        ),
        "G157 bounded status regressed or promoted",
    )
    require(by_id["G157"]["epistemic_label"] == "MIXED", "G157 label changed")
    for open_item in (
        "full B Q S Y Z screen and mixing composition law",
        "physical regime-dependent channel functions and their history evolution",
        "physical nonisometric cross-query carry and query population",
        "singular null degenerate cut topology-changing and global-completion strata",
    ):
        require(open_item in by_id["G157"]["open_scope"], f"G157 open boundary absent: {open_item}")
    for guard in (
        "Bplus2 theorem called full orchestra composition",
        "lawful composition called fixed channel ratios",
        "founded reciprocal D promoted to the full positive-triangular or complete-metric transition",
        "changing-balance endpoint family called a physical loud quiet loud prediction",
        "supplied valued-network reconstruction called dynamics physical-history selection or value law",
        "G155 common-scale rank-zero gap erased",
        "G142-G144 cross-query carry gap erased",
        "full screen or mixing balance claimed derived",
    ):
        require(guard in by_id["G157"]["forbidden_regression"], f"G157 guard absent: {guard}")
    require(
        by_id["G157"]["controlling_source"]
        == "udt_g157_regime_dependent_channel_balance_regrading_2026-08-18/AUDIT_REPORT.md",
        "G157 source changed",
    )
    require(
        by_id["G158"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_REPAIR_FOLLOWUP_PASS__PREREGISTERED__INDEPENDENT_EXACT_REPLAY_PASS__GAUGE_FIXED_COMPLETE_COFRAME_SEMIDIRECT_SCORE_DERIVED"
        ),
        "G158 bounded status regressed or promoted",
    )
    require(by_id["G158"]["epistemic_label"] == "MIXED", "G158 label changed")
    for open_item in (
        "physical nonisometric cross-query carry",
        "gauge-independent observable score",
        "physical E and J histories and lambda ownership",
        "singular null degenerate cut topology-changing and global-completion strata",
    ):
        require(open_item in by_id["G158"]["open_scope"], f"G158 open boundary absent: {open_item}")
    for guard in (
        "gauge-fixed structured matrix group called the physical observer functor",
        "right or left logarithmic velocity called a gauge-independent observable",
        "Y Z query blocks promoted to ambient group coordinates",
        "fixed generator called generic composition",
        "changing-score witness called a physical loud quiet loud prediction",
        "determinant closure called full carry closure",
        "algebraic score called history evolution or selection",
    ):
        require(guard in by_id["G158"]["forbidden_regression"], f"G158 guard absent: {guard}")
    require(
        by_id["G158"]["controlling_source"]
        == "udt_g158_complete_coframe_semidirect_score_audit_2026-08-18/AUDIT_REPORT.md",
        "G158 source changed",
    )
    require(
        by_id["G159"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_REPAIR_FOLLOWUP_PASS__PREREGISTERED__INDEPENDENT_DUAL_NUMBER_EXACT_REPLAY_PASS__CALIBRATED_PAIR_FIRST_JET_DERIVED"
        ),
        "G159 bounded status regressed or promoted",
    )
    require(by_id["G159"]["epistemic_label"] == "MIXED", "G159 label changed")
    for open_item in (
        "physical E and J histories query population and lambda ownership",
        "physical nonisometric cross-query calibration carry",
        "gauge-independent observable extraction beyond h and doth",
        "singular null degenerate cut topology-changing and global-completion strata",
    ):
        require(open_item in by_id["G159"]["open_scope"], f"G159 open boundary absent: {open_item}")
    for guard in (
        "calibrated pair coefficients called arbitrary GL2 invariants or gauge-independent observables",
        "live Lorentz inhomogeneous score term omitted",
        "dot J frozen or appended after terminal readout",
        "conditional pair c_eff called a local signal speed",
        "local first-jet descent called history evolution selection dynamics or physical loud quiet loud prediction",
        "supplied lambda called time distance affine parameter or evolution",
        "calibration carry called derived",
    ):
        require(guard in by_id["G159"]["forbidden_regression"], f"G159 guard absent: {guard}")
    require(
        by_id["G159"]["controlling_source"]
        == "udt_g159_complete_score_terminal_descent_2026-08-18/AUDIT_REPORT.md",
        "G159 source changed",
    )
    require(
        by_id["G160"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_REPAIR_FOLLOWUP_PASS__PREREGISTERED__INDEPENDENT_FRACTION_DUAL_EXACT_REPLAY_PASS__FULL_GLPLUS2_PAIR_FIRST_JET_CARRY_AND_RIGHT_RATE_COMPOSITION_DERIVED"
        ),
        "G160 bounded status regressed or promoted",
    )
    require(by_id["G160"]["epistemic_label"] == "MIXED", "G160 label changed")
    for open_item in (
        "physical nonisometric cross-query carry and query population",
        "physical E and J histories and lambda ownership",
        "full stabilizer quotient and classification of every terminal-law subgroup",
        "oriented screen normal carry and comparison with U_gamma",
        "singular null degenerate cut topology-changing and global-completion strata",
    ):
        require(open_item in by_id["G160"]["open_scope"], f"G160 open boundary absent: {open_item}")
    for guard in (
        "carry closure inferred from equality of carried h and doth",
        "Lorentz stabilizer declared physically trivial or erased",
        "positive Bplus2 called necessary for every reciprocal or shift law",
        "unrestricted GL2 phi or beta change called a carry-only character",
        "intrinsic and connection split called gauge-independent",
        "source-gauge covariance called invariance",
        "scalar rate closure called full matrix closure",
        "supplied carry called physical",
        "local first-order kinematics called history evolution dynamics selection or prediction",
    ):
        require(guard in by_id["G160"]["forbidden_regression"], f"G160 guard absent: {guard}")
    require(
        by_id["G160"]["controlling_source"]
        == "udt_g160_three_observer_timelive_first_jet_carry_2026-08-18/AUDIT_REPORT.md",
        "G160 source changed",
    )
    require(
        by_id["G161"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_REPAIR_FOLLOWUP_PASS__PREREGISTERED__INDEPENDENT_RAW_FRACTION_AND_DUAL_EXACT_REPLAY_PASS__PAIR_METRIC_AND_FIRST_JET_ARE_EXACT_LEFT_LORENTZ_STABILIZER_QUOTIENTS"
        ),
        "G161 bounded status regressed or promoted",
    )
    require(by_id["G161"]["epistemic_label"] == "MIXED", "G161 label changed")
    for open_item in (
        "physical nonisometric cross-query carry query population and history",
        "ownership and global compatibility of supplied pair immersions",
        "extrinsic eigenflag composition across observer networks",
        "null past-clock degenerate eigen-crossing cut topology-changing and global-completion strata",
    ):
        require(open_item in by_id["G161"]["open_scope"], f"G161 open boundary absent: {open_item}")
    for guard in (
        "left quotient written as right quotient",
        "positive Bplus2 quotient section called the physical carry",
        "distance sweep said to fix vertical rapidity",
        "Lorentz stabilizer declared physically trivial rather than coframe-equivalent on the bounded evaluator",
        "screen metric normal connection or holonomy claimed to universally fix tangent boost",
        "bare pair plane called owner of II",
        "simple CII spectrum assumed on all physical pairs",
        "conditional eigenflag called query or history selection",
    ):
        require(guard in by_id["G161"]["forbidden_regression"], f"G161 guard absent: {guard}")
    require(
        by_id["G161"]["controlling_source"]
        == "udt_g161_pair_carry_lorentz_quotient_screen_resolution_2026-08-18/AUDIT_REPORT.md",
        "G161 source changed",
    )
    require(
        by_id["G162"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__ORIGINAL_TYPE_FAILURE_AND_FIRST_REPAIR_FAILURE_PRESERVED__FRESH_ADVERSARIAL_SECOND_REPAIR_PASS__PREREGISTERED_POST_COMMIT_FINAL_RERUN__INDEPENDENT_FRACTION_DUAL_AND_SOURCE_CROSSWALK_PASS__BOUNDED_SCALAR_RECIPROCAL_KERNEL_AND_FIRST_JET_LAMBDA_INVARIANT"
        ),
        "G162 bounded status regressed or promoted",
    )
    require(by_id["G162"]["epistemic_label"] == "MIXED", "G162 label changed")
    for open_item in (
        "physical query path carry and complete relation assignment",
        "physical values and evolution of B Q S Y Z and kappa",
        "ownership of route Lambda C Gamma and carry defects",
        "relation among normal holonomy Jacobi ambient and extrinsic channels",
        "null past-clock degenerate cut topology-changing and global-completion strata",
        "Xmax value profile and completion",
    ):
        require(open_item in by_id["G162"]["open_scope"], f"G162 open boundary absent: {open_item}")
    for guard in (
        "original type failure or first repair failure erased",
        "volume density conflated with half-density",
        "joined sigma conflated with raw half-log determinant grading",
        "complete-coframe score called path or extrinsic data",
        "canonical endpoint section called physical overlap path or carry",
        "residual rapidity reintroduced as a scalar-kernel input",
        "supplied C Gamma carry defects or route memory erased",
        "normal Jacobi ambient and extrinsic channels collapsed into tangent Lambda",
        "bounded regular result promoted to history selection global completion Xmax dynamics or prediction",
    ):
        require(guard in by_id["G162"]["forbidden_regression"], f"G162 guard absent: {guard}")
    require(
        by_id["G162"]["controlling_source"]
        == "udt_g162_lambda_dependence_frontier_census_2026-08-18/AUDIT_REPORT.md",
        "G162 source changed",
    )
    require(
        by_id["G163"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_PASS_WITH_REPAIRS__PREREGISTERED__INDEPENDENT_FRACTION_REPLAY_PASS__DIMENSIONLESS_RECIPROCAL_KERNEL_CLOSES_WITHOUT_XMAX"
        ),
        "G163 dependency reversal regressed or promoted",
    )
    require(by_id["G163"]["epistemic_label"] == "MIXED", "G163 label changed")
    for open_item in (
        "independent metric-natural dimensionful separation and physical relation domain",
        "all-frame recentering and overlap theorem",
        "global completion finite positive supremum and divergent-depth correspondence",
        "numerical Xmax value",
    ):
        require(open_item in by_id["G163"]["open_scope"], f"G163 open boundary absent: {open_item}")
    for guard in (
        "Xmax inserted into the native pair kernel",
        "structural zero Jacobian called independent identifiability evidence",
        "dimensionless projective boundary called a finite length",
        "x equals Xmax chi or any Xmax-weighted response called native",
        "G153 conditional product rule erased",
        "G154 fixed-scale probes called derivations",
        "Xmax-independent full-metric results called scale-free metric physics",
        "unbounded control called an admissible physical model",
        "supremum criterion called a derived completion theorem",
    ):
        require(guard in by_id["G163"]["forbidden_regression"], f"G163 guard absent: {guard}")
    require(
        by_id["G163"]["controlling_source"]
        == "udt_g163_xmax_dependency_reversal_audit_2026-08-18/AUDIT_REPORT.md",
        "G163 source changed",
    )
    require(
        by_id["G165"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__PREREGISTERED__19_SOURCE_FREEZE__59_ROW_CENSUS__NO_ACTIVE_SOURCE_OWNED_METRIC_RESTRICTOR"
        ),
        "G165 conformal-fiber landing regressed or promoted",
    )
    require(by_id["G165"]["epistemic_label"] == "MIXED", "G165 label changed")
    for open_item in (
        "future native relative-scale carry global admissibility",
        "physical query and relation domain",
        "finite-moduli theorem and lawful observational calibration bridge",
        "scale holonomy and singular null cut topology-changing strata",
        "proper distance numerical Xmax",
    ):
        require(open_item in by_id["G165"]["open_scope"], f"G165 open boundary absent: {open_item}")
    for guard in (
        "proof that no future native UDT scale law exists",
        "common scale called gauge",
        "evaluator reconstruction metricity Cartan Bianchi overlap composition or supplied carry promoted to a metric law",
        "full valued network called finite-anchor prediction",
        "c_E and G_obs alone called a length",
        "finite anchors called sufficient for an arbitrary function",
        "compact bump called physical UDT",
        "conventional evolution equation called uniquely necessary",
        "protected work inserted",
    ):
        require(guard in by_id["G165"]["forbidden_regression"], f"G165 guard absent: {guard}")
    require(
        by_id["G165"]["controlling_source"]
        == "udt_g165_conformal_fiber_rank_audit_2026-08-18/AUDIT_REPORT.md",
        "G165 source changed",
    )
    require(
        by_id["G166"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__PREREGISTERED__13_SOURCE_FREEZE__PRIMARY_UDT_ORDERED_PAIR_KERNEL_DESCENDS_ALGEBRAICALLY"
        ),
        "G166 primary-metric pair-kernel landing regressed or promoted",
    )
    require(by_id["G166"]["epistemic_label"] == "MIXED", "G166 label changed")
    for open_item in (
        "native nonspherical angular screen mixing shift-bearing time-live and micro 3plus1 assembly",
        "physical pair values and bare observer event calibration typing",
        "cross-query and arbitrary-network calibration carry",
        "singular null cut topology-changing and global-completion strata",
        "dimensionful separation numerical Xmax",
    ):
        require(open_item in by_id["G166"]["open_scope"], f"G166 open boundary absent: {open_item}")
    for guard in (
        "fixed path or pre-existing operational distance inserted before the kernel",
        "reciprocal kernel called an independent post-metric profile",
        "orchestra attached after phi_pair q_pair or chi_pair",
        "unrestricted complete coframe envelope called the derived UDT solution space",
        "G165 conformal twins called infinitely many physical UDT metrics",
        "static spherical realization promoted to the general nonspherical time-live assembly",
        "arbitrary observer-network carry called solved",
        "common-scale cancellation called physical scale gauge",
        "Xmax inserted into the local kernel",
        "conditional pair c_eff called local material signal speed",
        "protected work inserted",
    ):
        require(guard in by_id["G166"]["forbidden_regression"], f"G166 guard absent: {guard}")
    require(
        by_id["G166"]["controlling_source"]
        == "udt_g166_primary_metric_ordered_pair_kernel_descent_2026-08-18/AUDIT_REPORT.md",
        "G166 source changed",
    )
    require(
        by_id["G167"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__PREREGISTERED__FRESH_EXTERNAL_REPAIR_FOLLOWUP_PASS__PRIMARY_STATIC_SPHERICAL_UDT_METRIC_OWNS_FULL_LOCAL_REGULAR_PAIR_PULLBACK_ORCHESTRA"
        ),
        "G167 bounded primary-metric pair-pullback landing regressed or promoted",
    )
    require(by_id["G167"]["epistemic_label"] == "MIXED", "G167 label changed")
    for open_item in (
        "physical observer event calibration pair realization and query population",
        "cross-query calibration carry and global relation network",
        "general nonspherical angular mixed shift-bearing ambient time-dependent and micro 3plus1 metric",
        "singular null rank-changing cut topology-changing and global-completion strata",
        "connection Jacobi normal transport holonomy and route-labelled observables",
        "dimensionful separation numerical Xmax",
    ):
        require(open_item in by_id["G167"]["open_scope"], f"G167 open boundary absent: {open_item}")
    for guard in (
        "bounded static spherical pullback promoted to a general ambient global or complete-universe theorem",
        "supplied pair immersion Y or Z called a selected physical observer relation or fixed path",
        "angular Gram attached after terminal phi_pair c_eff or chi readout",
        "independent scalar mu inserted in place of the full metric-derived angular Gram",
        "S equals zero in the primary coframe called proof that general ambient mixing cannot exist",
        "pair h01 or beta_pair called an invariant ambient shift field",
        "query-live derivative called ambient time evolution dynamics or a field equation",
        "central radial Z equals zero called proof that the angular sector is absent",
        "local pair metric called reconstruction of connection Jacobi normal transport or holonomy",
        "conditional pair c_eff called a local material signal speed",
        "protected work inserted",
    ):
        require(guard in by_id["G167"]["forbidden_regression"], f"G167 guard absent: {guard}")
    require(
        by_id["G167"]["controlling_source"]
        == "udt_g167_primary_metric_full_pair_pullback_orchestra_2026-08-18/AUDIT_REPORT.md",
        "G167 source changed",
    )
    require(
        by_id["G168"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__PREREGISTERED__FRESH_EXTERNAL_REPAIR_FOLLOWUP_PASS__SUPPLIED_ORDERED_COPRESENT_PAIR_GERM_DERIVES_LOCAL_CALIBRATED_PAIR_PLANE__NO_PATH_REQUIRED__PHYSICAL_GERM_OWNERSHIP_PROPOSED_WORKING_POSTULATE_NOT_DERIVED"
        ),
        "G168 supplied-germ pair-plane landing regressed or promoted",
    )
    require(by_id["G168"]["epistemic_label"] == "MIXED", "G168 label changed")
    for open_item in (
        "derivation of physical calibrated pair germ from founding postulates or bare observer labels",
        "event pairing local one-jet ownership and query population",
        "cross-query reversal calibration carry and global relation network",
        "general nonspherical angular mixed shift-bearing ambient time-dependent and micro 3plus1 metric",
        "coincidence null degenerate rank-changing cut topology-changing and global-completion strata",
        "connection Jacobi normal transport holonomy and route-labelled observables",
        "dimensionful separation numerical Xmax",
    ):
        require(open_item in by_id["G168"]["open_scope"], f"G168 open boundary absent: {open_item}")
    for guard in (
        "supplied pair germ called founded automatically physical or selected by bare observer labels",
        "metric projection formula called derivation of event pairing or global realization",
        "path or complete pair surface required after a regular germ is supplied",
        "same boundary observers and event pairing called sufficient to select one local plane",
        "B velocity forced into the A-side positional plane",
        "local ruler reversal called full reciprocal observer reversal",
        "coincidence treated as regular rank two",
        "G168 called general ambient global dynamics completion or numerical Xmax",
        "protected work inserted",
    ):
        require(guard in by_id["G168"]["forbidden_regression"], f"G168 guard absent: {guard}")
    require(
        by_id["G168"]["controlling_source"]
        == "udt_g168_ordered_copresent_pair_plane_ownership_2026-08-18/AUDIT_REPORT.md",
        "G168 source changed",
    )
    require(
        by_id["G169"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__PREREGISTERED__FRESH_EXTERNAL_TYPE_FAILURE__TWO_REPAIR_FOLLOWUPS_FINAL_PASS__CONDITIONAL_REVERSAL_QUOTIENT_ON_SUPPLIED_TWO_ENDED_RELATION__NOT_YET_PHYSICAL_UDT_DISTANCE"
        ),
        "G169 conditional reversal landing regressed or promoted",
    )
    require(by_id["G169"]["epistemic_label"] == "MIXED", "G169 label changed")
    for open_item in (
        "derivation that physical co-presence supplies both endpoint germs and inverse carry",
        "event pairing query population and global relation category",
        "full reversal parity of every angular screen shift and mixing channel",
        "coincidence identity completion",
        "arbitrary noncollinear triangle calibration",
        "general ambient time-dependent micro and global extension",
        "route transport holonomy connection Jacobi and normal channels",
        "dimensionful separation numerical Xmax",
    ):
        require(open_item in by_id["G169"]["open_scope"], f"G169 open boundary absent: {open_item}")
    for guard in (
        "reversal quotient called physical UDT distance",
        "supplied two-ended relation called derived from bare observers co-presence or one endpoint germ",
        "ordinary surface reversal or endpoint exchange called reciprocal inversion",
        "arbitrary noncollinear triangles forced to obey one-dimensional additive depth",
        "absolute delta or chi called a point-separating metric distance",
        "scalar closure called complete carry closure",
        "coincidence treated as regular rank two",
        "endpoint orchestra parities invented",
        "path Xmax dynamics observations or protected work inserted",
    ):
        require(guard in by_id["G169"]["forbidden_regression"], f"G169 guard absent: {guard}")
    require(
        by_id["G169"]["controlling_source"]
        == "udt_g169_bidirectional_copresent_metric_distance_2026-08-18/AUDIT_REPORT.md",
        "G169 source changed",
    )
    require(
        by_id["G170"]["current_status"].startswith(
            "EXTERNALLY_VERIFIED_WITH_CAVEATS__PREREGISTERED__FINAL_MECHANICAL_CLOSURE_PASS__ENDPOINT_RELATIVE_DEPTH_EQUALS_PHI_B_MINUS_PHI_A_IN_ONE_CONSISTENT_RECIPROCAL_CALIBRATION_CLASS"
        ),
        "G170 endpoint-relative landing regressed or promoted",
    )
    require(by_id["G170"]["epistemic_label"] == "MIXED", "G170 label changed")
    for open_item in (
        "cross-query reciprocal calibration carry and zero alignment",
        "event selection and query population",
        "full screen shift orientation connection holonomy and non-scalar carry",
        "arbitrary triangle and route closure",
        "positive metric-space distance identity separation and triangle axioms",
        "general ambient time-live micro and global extension",
        "coincidence null singular and cut strata",
        "dimensionful separation numerical Xmax",
    ):
        require(open_item in by_id["G170"]["open_scope"], f"G170 open boundary absent: {open_item}")
    for guard in (
        "single endpoint density called directed arrow depth",
        "G169 equal nonzero endpoint densities called a reversal counterexample after endpoint differencing",
        "independently recalibrated endpoint densities subtracted without lawful carry",
        "endpoint swap called a positive metric-space distance theorem",
        "scalar telescoping called full non-scalar carry closure",
        "angular Gram or shift appended after terminal readout or replaced by scalar mu",
        "co-presence called load-bearing",
        "supplied endpoint arguments called a metric selection law",
        "path Xmax fit dynamics observations or protected work inserted",
    ):
        require(guard in by_id["G170"]["forbidden_regression"], f"G170 guard absent: {guard}")
    require(
        by_id["G170"]["controlling_source"]
        == "udt_g170_endpoint_relative_bidirectional_pair_response_2026-08-19/AUDIT_REPORT.md",
        "G170 source changed",
    )
    require(
        by_id["G171"]["current_status"].startswith(
            "RECLASSIFIED_BY_G215__PRE_G176_RAW_PAIR_INCIDENCE_SCALAR_DEFECT_RETAINED_AS_UNCOMPLETED_CONTROL__UNDER_G176_WORKING_COMPLETION_SHARED_CALIBRATED_CLOCK_GERM_FORCES_SCALAR_DESCENT"
        ),
        "G171 current reclassification regressed or promoted",
    )
    require(by_id["G171"]["epistemic_label"] == "MIXED", "G171 label changed")
    require(
        by_id["G171"]["active_use"]
        == "RECLASSIFIED_BOUNDED_RAW_UNCOMPLETED_INCIDENCE_AND_INDEPENDENT_CLOCK_CALIBRATION_CONTROL_ONLY",
        "G171 active scope changed",
    )
    for open_item in (
        "physical pair-germ realization and global extendability",
        "ownership of common calibrated observer clocks beyond supplied germs",
        "equivalence of separately rebuilt reverse experiments",
        "full pair-metric and immersion-germ incidence maps",
        "nonscalar screen connection orientation and holonomy response",
        "general nonspherical time-dependent micro and ambient extension",
        "coincidence null degenerate singular cut and topology-changing strata",
        "completion dimensionful separation numerical Xmax",
    ):
        require(open_item in by_id["G171"]["open_scope"], f"G171 open boundary absent: {open_item}")
    for guard in (
        "G171 raw pre-G176 angular scalar mismatch reused as a completed-kernel counterexample",
        "shared observer label confused with one shared calibrated clock germ",
        "independent edge-clock recalibrations silently identified",
        "scalar equality promoted to full pair-metric or immersion-germ equality",
        "density shift angular or screen channels called erased",
        "arbitrary full-tuple triangle product imposed",
        "G176 working clarification called canon",
        "G142 through G160 carry score or selected-history scaffolding reintroduced as the native kernel",
        "pair response called positive metric-space distance",
        "supplied local germ network called globally physical",
        "path Xmax fit dynamics observations or protected work inserted",
    ):
        require(guard in by_id["G171"]["forbidden_regression"], f"G171 guard absent: {guard}")
    require(
        by_id["G171"]["controlling_source"]
        == "udt_g215_completed_scalar_shared_clock_incidence_descent_2026-08-22/AUDIT_REPORT.md",
        "G171 source changed",
    )
    require(
        by_id["G172"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__EXTERNAL_GPT54_ACCEPTED_WITH_STATED_BOUNDS__PREREGISTERED__SMOOTH_FAMILY_CLOSURE_ON_STATIC_TIME_ORTHOGONAL_MONOTONE_AREAL_CLASS"
        ),
        "G172 smooth pair-family landing regressed or promoted",
    )
    require(by_id["G172"]["epistemic_label"] == "MIXED", "G172 label changed")
    for open_item in (
        "physical angular-family realization",
        "formal arbitrary a2 converse realization from a free-standing nonnegative speed field",
        "turning and pure-angular charts at dr/dsigma equals zero",
        "non-scalar screen connection orientation and holonomy transport",
        "nonspherical time-live micro and ambient extension",
        "smooth center and global completion",
        "dimensionful separation numerical Xmax",
    ):
        require(open_item in by_id["G172"]["open_scope"], f"G172 open boundary absent: {open_item}")
    for guard in (
        "supplied smooth angular family called selected physical path or universe",
        "arbitrary a2 replaced by fitted constant",
        "angular Gram dropped or appended after terminal readout",
        "raw pair-coordinate Phi called reparameterization invariant without areal calibration",
        "monotone-areal theorem widened through dr/dsigma equals zero",
        "one-sided r-to-zero limit called smooth-center completion",
        "finite regular interval called global completion",
        "scalar telescoping called complete non-scalar transport closure",
        "conditional pair c_eff called local signal speed",
        "co-presence Xmax observations or G142 through G160 scaffolds inserted",
    ):
        require(guard in by_id["G172"]["forbidden_regression"], f"G172 guard absent: {guard}")
    require(
        by_id["G172"]["controlling_source"]
        == "udt_g172_primary_metric_smooth_pair_family_integrability_2026-08-19/AUDIT_REPORT.md",
        "G172 source changed",
    )
    require(
        by_id["G173"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__EXTERNAL_GPT54_ACCEPTED_WITH_STATED_BOUNDS__PREREGISTERED__PULLBACK_EXTENDS_THROUGH_RADIAL_TURN_WHEN_ANGULAR_TANGENT_NONZERO"
        ),
        "G173 turning-chart calibration-atlas landing regressed or promoted",
    )
    require(by_id["G173"]["epistemic_label"] == "MIXED", "G173 label changed")
    for open_item in (
        "physical calibration and pair-family ownership",
        "whether a future native relation law selects one calibration-atlas chart",
        "cross-calibration carry",
        "time-live pair shift and nonspherical micro ambient extension",
        "center coincidence null singular cut focal and topology-changing strata",
        "smooth and global completion",
        "non-scalar screen connection Jacobi orientation and holonomy transport",
        "positive global distance dimensionful separation numerical Xmax",
    ):
        require(open_item in by_id["G173"]["open_scope"], f"G173 open boundary absent: {open_item}")
    for guard in (
        "radial turn with angular motion called metric or rank singularity",
        "zero radial component conflated with zero complete spatial tangent",
        "raw coordinate Phi called scalar without a weight-one calibration density",
        "m_A or m_P selected as the physical ruler",
        "bounded calibration nonuniqueness called proof that physical UDT has multiple rulers",
        "arbitrary m_f promoted to physics",
        "finite nonareal scalar claimed numerically identical to G172 throughout a punctured turn",
        "exact calibration transition erased",
        "G172 overwritten rather than retained as the areal overlap chart",
        "cross-calibration or arbitrary triangle closure imposed",
        "scalar reversal called non-scalar transport closure",
        "local atlas globalized",
        "conditional pair c_eff called local signal speed",
        "co-presence Xmax observations or G142 through G160 scaffolds inserted",
    ):
        require(guard in by_id["G173"]["forbidden_regression"], f"G173 guard absent: {guard}")
    require(
        by_id["G173"]["controlling_source"]
        == "udt_g173_primary_metric_turning_chart_calibration_atlas_2026-08-19/AUDIT_REPORT.md",
        "G173 source changed",
    )
    require(
        by_id["G174"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__EXTERNAL_GPT54_ACCEPTED_WITH_STATED_BOUNDS__PREREGISTERED__M_IS_EXACT_JACOBIAN_FROM_AUXILIARY_PARAMETER_TO_SUPPLIED_CALIBRATED_RULER_COORDINATE"
        ),
        "G174 calibrated-germ ownership landing regressed or promoted",
    )
    require(by_id["G174"]["epistemic_label"] == "MIXED", "G174 label changed")
    for open_item in (
        "which physical ordered pair supplies the calibrated germ and ruler coordinate",
        "how calibration is carried across independently constructed pair tapes",
        "whether A-fixed c_E calibration alone owns one relation-wide calibration class",
        "time-live shift nonspherical micro and ambient extension",
        "center coincidence null singular cut focal topology-changing and global strata",
        "non-scalar screen connection Jacobi orientation and holonomy transport",
        "positive distance dimensionful separation numerical Xmax",
    ):
        require(open_item in by_id["G174"]["open_scope"], f"G174 open boundary absent: {open_item}")
    for guard in (
        "calibrated-germ uniqueness called selection of a physical ruler or pair family",
        "bare line plane or pair image called fully calibrated",
        "m_A or m_P selected",
        "distinct positive m called two outputs for one fixed calibrated vector",
        "auxiliary m held fixed under reparameterization",
        "position-dependent recalibration called gauge or erased from endpoint depth",
        "local calibrated germ claimed to determine remote or cross-query carry",
        "G173 tensor and rank theorem erased",
        "bounded local typing theorem globalized",
        "scalar reversal called non-scalar transport closure",
        "conditional pair c_eff called local signal speed",
        "co-presence Xmax observations or G142 through G160 scaffolds inserted",
    ):
        require(guard in by_id["G174"]["forbidden_regression"], f"G174 guard absent: {guard}")
    require(
        by_id["G174"]["controlling_source"]
        == "udt_g174_native_calibrated_pair_germ_chart_ownership_2026-08-19/AUDIT_REPORT.md",
        "G174 source changed",
    )
    require(
        by_id["G175"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__EXTERNAL_GPT54_ACCEPTED_WITH_STATED_BOUNDS__PREREGISTERED__EXACT_RECALIBRATION_PHI_N_EQUALS_PHI_M_MINUS_ONE_HALF_LOG_F"
        ),
        "G175 calibration-equivalence landing regressed or promoted",
    )
    require(by_id["G175"]["epistemic_label"] == "MIXED", "G175 label changed")
    for open_item in (
        "which physical ordered pair supplies the relation-wide calibrated map and ruler",
        "carry between independently constructed tapes",
        "whether the founded determinant-one radial normalization uniquely extends to the complete angular pair pullback",
        "time-live shift nonspherical micro and ambient extension",
        "center coincidence null singular cut focal topology-changing and global strata",
        "non-scalar screen connection Jacobi orientation and holonomy transport",
        "positive distance dimensionful separation numerical Xmax",
    ):
        require(open_item in by_id["G175"]["open_scope"], f"G175 open boundary absent: {open_item}")
    for guard in (
        "A-local calibration called a relation-wide propagation theorem",
        "supplied full coordinate sufficiency called derivation",
        "position-dependent recalibration called gauge or erased from endpoint depth",
        "endpoint-depth equality allowed under nonconstant ruler ratio on a connected tape",
        "metric-unit arclength identified with the founded carried reciprocal ruler",
        "determinant-one m_P selected as physical without a premise",
        "c_E or reciprocal character claimed to supply an m differential or continuation equation",
        "G170 G171 G173 or G174 erased",
        "bounded static theorem globalized",
        "scalar equivalence called non-scalar carry closure",
        "conditional pair c_eff called local signal speed",
        "co-presence Xmax observations or G142 through G160 scaffolds inserted",
    ):
        require(guard in by_id["G175"]["forbidden_regression"], f"G175 guard absent: {guard}")
    require(
        by_id["G175"]["controlling_source"]
        == "udt_g175_relation_wide_calibration_equivalence_audit_2026-08-19/AUDIT_REPORT.md",
        "G175 source changed",
    )
    require(
        by_id["G176"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__WORKING_FOUNDATIONAL_CLARIFICATION_NOT_CANON__PREREGISTERED_AT_EB306A0D"
        ),
        "G176 completed-pair clarification regressed or promoted",
    )
    require(by_id["G176"]["epistemic_label"] == "MIXED", "G176 label changed")
    require(
        by_id["G176"]["active_use"]
        == "ACTIVE_GENERIC_LOCAL_REGULAR_COMPLETED_PHYSICAL_UDT_RECIPROCAL_PAIR_NORMALIZATION_AND_BOUNDED_G173_STATIC_SPECIALIZATION_ONLY",
        "G176 active scope widened",
    )
    for open_item in (
        "which observer events and pair germs are physically realized",
        "complete nonspherical timelive micro and ambient history ownership beyond supplied pullback",
        "coincidence null degenerate singular cut focal topology-changing and global strata",
        "non-scalar screen orientation connection Jacobi and holonomy transport",
        "cross-query and global relation population",
        "positive dimensionful separation numerical Xmax and global completion",
        "observations radiative transfer dynamics action source matter bootstrap mass and signalling",
    ):
        require(open_item in by_id["G176"]["open_scope"], f"G176 open boundary absent: {open_item}")
    for guard in (
        "working clarification called canon or derived from bare metric",
        "determinant-one applied before angular screen mixing or shift contributions enter",
        "arbitrary arclength or calibrated curves restored as rival reciprocal kernels",
        "post-readout angular correction bolted onto Phi",
        "shift erased because determinant is shift-blind",
        "unique ruler theorem called event or pair-germ selection",
        "G173 G174 or G175 historical controls erased",
        "local regular theorem globalized",
        "physical pair c_eff called local signal speed",
        "non-scalar transport collapsed into scalar",
        "co-presence Xmax fits G142 through G160 action source matter or bootstrap inserted",
    ):
        require(guard in by_id["G176"]["forbidden_regression"], f"G176 guard absent: {guard}")
    require(
        by_id["G176"]["controlling_source"]
        == "udt_g176_completed_pair_dual_reciprocity_consolidation_2026-08-19/AUDIT_REPORT.md",
        "G176 source changed",
    )
    require(
        by_id["G177"]["current_status"].startswith(
            "VERIFIED_WITH_CAVEATS__PREREGISTERED_AT_07DC6319__MINIMAL_CHAIN_PRIMARY_METRIC"
        ),
        "G177 scaffold-regression landing changed",
    )
    require(by_id["G177"]["epistemic_label"] == "MIXED", "G177 label changed")
    require(
        by_id["G177"]["active_use"]
        == "ACTIVE_BOUNDED_LOCAL_REGULAR_COMPLETED_PAIR_KERNEL_DEPENDENCY_AND_SCAFFOLD_SUBTRACTION_ONLY",
        "G177 active scope widened",
    )
    for open_item in (
        "physical observer event and pair-germ population",
        "complete nonspherical timelive micro and ambient history beyond supplied pullback",
        "coincidence null degenerate singular cut focal topology-changing and global strata",
        "route frame screen orientation connection Jacobi and holonomy transport",
        "cross-query relation population and global completion",
        "positive dimensionful distance numerical Xmax",
        "observations radiative transfer dynamics action source matter bootstrap mass and signalling",
    ):
        require(open_item in by_id["G177"]["open_scope"], f"G177 open boundary absent: {open_item}")
    for guard in (
        "G177 called unconditional native canon or a global theory closure",
        "working G176 clarification called derived from bare metric",
        "supplied pair germ called selected",
        "scaffold deletion called proof that scaffolds can never appear in downstream physics",
        "Xmax path score carry observer potential post-readout angular term fit action source or hidden calibration restored as kernel antecedent",
        "shift erased",
        "non-scalar transport collapsed into scalar",
        "AST lexical census called sole mathematical proof",
        "bounded rational replay globalized",
        "G166 G167 G173 G174 G175 or G176 erased",
        "physical pair c_eff called local signal speed",
    ):
        require(guard in by_id["G177"]["forbidden_regression"], f"G177 guard absent: {guard}")
    require(
        by_id["G177"]["controlling_source"]
        == "udt_g177_completed_pair_kernel_scaffolding_regression_audit_2026-08-19/AUDIT_REPORT.md",
        "G177 source changed",
    )
    require(
        by_id["G178"]["current_status"].startswith(
            "FRESH_ADVERSARIAL_PASS__PREREGISTERED_AT_561C4268__SEALED_50_FILE_INTAKE"
        ),
        "G178 external-review landing changed",
    )
    require(by_id["G178"]["epistemic_label"] == "MIXED", "G178 label changed")
    require(
        by_id["G178"]["active_use"]
        == "ACTIVE_FRESH_EXTERNAL_CERTIFICATION_OF_G176_G177_BOUNDED_COMPLETED_PAIR_KERNEL_ONLY",
        "G178 active scope widened",
    )
    for open_item in (
        "physical observer event and pair-germ population",
        "explicit complete nonspherical timelive micro and mixed ambient realizations beyond supplied pullback",
        "coincidence null degenerate singular cut focal topology-changing and global strata",
        "observer-pair reversal remains controlled separately by G170 G171",
        "non-scalar route frame screen connection Jacobi and holonomy transport",
        "cross-query relation population and global completion",
        "positive dimensionful distance numerical Xmax",
        "observations radiative transfer dynamics action source matter bootstrap mass and signalling",
    ):
        require(open_item in by_id["G178"]["open_scope"], f"G178 open boundary absent: {open_item}")
    for guard in (
        "G178 called canon unconditional native global closure or event germ selector",
        "working clarification called derived from bare metric",
        "external acceptance used to erase conditional premise",
        "spatial-coordinate reversal called observer-pair reversal",
        "orchestra applied after readout",
        "shift erased",
        "arbitrary calibrated controls restored as rival kernels",
        "scaffold deletion globalized beyond scalar antecedents",
        "physical pair c_eff called local signal speed",
        "observations completion Xmax dynamics or source inferred",
    ):
        require(guard in by_id["G178"]["forbidden_regression"], f"G178 guard absent: {guard}")
    require(
        by_id["G178"]["controlling_source"]
        == "udt_g178_completed_pair_kernel_fresh_adversarial_review_2026-08-19/AUDIT_REPORT.md",
        "G178 source changed",
    )
    require(
        (ROOT / "udt_g178_completed_pair_kernel_fresh_adversarial_review_2026-08-19/EXTERNAL_REVIEW_ADJUDICATION.md").is_file(),
        "G178 external adjudication missing",
    )
    require(
        by_id["G179"]["current_status"].startswith(
            "DERIVED_CONDITIONAL__FRESH_EXTERNALLY_ACCEPTED_WITH_STATED_BOUNDS__"
            "PREREGISTERED_AT_C8070ADB"
        ),
        "G179 complete-coframe landing changed",
    )
    require(by_id["G179"]["epistemic_label"] == "MIXED", "G179 label changed")
    require(
        by_id["G179"]["active_use"]
        == "ACTIVE_GENERIC_LOCAL_COMPLETE_COFRAME_EXTENSION_OF_THE_WORKING_COMPLETED_PAIR_SCALAR_KERNEL_ON_SUPPLIED_REGULAR_RANK_TWO_GERMS_ONLY",
        "G179 active scope widened",
    )
    for open_item in (
        "physical observer event and pair-germ realization",
        "coincidence null degenerate singular cut focal topology-changing and global strata",
        "observer-pair reversal remains controlled separately by G170 G171",
        "non-scalar route frame screen connection Jacobi and holonomy transport",
        "cross-query relation population and global completion",
        "positive dimensionful distance numerical Xmax",
        "observations radiative transfer dynamics action source matter bootstrap mass and signalling",
    ):
        require(open_item in by_id["G179"]["open_scope"], f"G179 open boundary absent: {open_item}")
    for guard in (
        "G179 called canon unconditional native global closure event or germ selector",
        "working clarification called derived from bare metric",
        "arbitrary E and J called selected physical history",
        "block complete chart called uniquely physical split",
        "Y inverse introduced",
        "Q S Z or shift deleted scalarized frozen or appended after readout",
        "arbitrary-calibration phi_pair substituted for completed Phi",
        "auxiliary spatial reversal called observer-pair reversal",
        "time-live chain rule called dynamics",
        "Xmax fit source action matter bootstrap or signalling imported",
        "physical pair c_eff called local signal speed",
    ):
        require(guard in by_id["G179"]["forbidden_regression"], f"G179 guard absent: {guard}")
    require(
        by_id["G179"]["controlling_source"]
        == "udt_g179_complete_coframe_pair_pullback_extension_2026-08-19/AUDIT_REPORT.md",
        "G179 source changed",
    )
    require(
        (ROOT / "udt_g179_complete_coframe_pair_pullback_extension_2026-08-19/VERIFICATION_RESULT.json").is_file(),
        "G179 verification result missing",
    )
    require(
        (ROOT / "udt_g179_complete_coframe_pair_pullback_extension_2026-08-19/EXTERNAL_REVIEW_ADJUDICATION.md").is_file(),
        "G179 external adjudication missing",
    )
    require(
        by_id["G180"]["current_status"].startswith(
            "DERIVED_CONDITIONAL__EXTERNALLY_ACCEPTED_WITH_STATED_BOUNDS__"
            "REPAIR_ACCEPTED__"
            "PREREGISTERED_AT_AE24EBBC"
        ),
        "G180 smooth-family landing changed",
    )
    require(by_id["G180"]["epistemic_label"] == "MIXED", "G180 label changed")
    require(
        by_id["G180"]["active_use"]
        == "ACTIVE_INTERVAL_WIDE_DESCENT_OF_ACCEPTED_COMPLETED_PAIR_KERNEL_ON_SUPPLIED_SMOOTH_REGULAR_FAMILIES_ONLY",
        "G180 active scope widened",
    )
    for open_item in (
        "physical observer event pair-germ and family realization",
        "cross-family matching and global completion",
        "null degenerate zero-tangent singular cut focal topology-changing strata",
        "non-scalar route frame screen connection Jacobi and holonomy transport",
        "supplied metric and common-scale profile selection",
        "positive metric-space distance numerical Xmax",
        "observations radiative transfer dynamics action source matter bootstrap mass and signalling",
    ):
        require(open_item in by_id["G180"]["open_scope"], f"G180 open boundary absent: {open_item}")
    for guard in (
        "G180 called canon unconditional native global completion family selector or metric-space distance",
        "working clarification called derived from bare metric",
        "supplied smooth family called selected physical history",
        "integral origin called fitted coefficient",
        "angular contribution deleted from completed tape or bolted onto Phi after readout",
        "G172 arbitrary-coordinate control restored as completed physical scalar",
        "common-scale sensitivity called common-scale profile selection",
        "auxiliary orientation called observer-pair reversal",
        "same-family telescoping globalized across independent families",
        "zero tangent called regular",
        "chain rule called dynamics",
        "G142 through G160 Xmax fit observation action source matter bootstrap or signalling imported",
        "pair c_eff called local signal speed",
    ):
        require(guard in by_id["G180"]["forbidden_regression"], f"G180 guard absent: {guard}")
    require(
        by_id["G180"]["controlling_source"]
        == "udt_g180_completed_pair_smooth_family_descent_2026-08-19/AUDIT_REPORT.md",
        "G180 source changed",
    )
    require(
        (ROOT / "udt_g180_completed_pair_smooth_family_descent_2026-08-19/VERIFICATION_RESULT.json").is_file(),
        "G180 verification result missing",
    )
    require(
        (ROOT / "udt_g180_completed_pair_smooth_family_descent_2026-08-19/EXTERNAL_REVIEW_ADJUDICATION.md").is_file(),
        "G180 external adjudication missing",
    )
    require(
        (ROOT / "udt_g180_completed_pair_smooth_family_descent_2026-08-19/REVIEW_REPAIR_PREREGISTRATION.md").is_file(),
        "G180 repair preregistration missing",
    )
    require(
        (ROOT / "udt_g180_completed_pair_smooth_family_descent_2026-08-19/EXTERNAL_FOLLOWUP_REVIEW_RAW.md").read_text().strip()
        == "G180_REPAIR_ACCEPTED",
        "G180 repair-only external acceptance missing",
    )
    require(
        (ROOT / "udt_g180_completed_pair_smooth_family_descent_2026-08-19/FOLLOWUP_TRANSMISSION_RECORD.md").is_file(),
        "G180 follow-up transmission record missing",
    )
    require(
        by_id["G181"]["current_status"].startswith(
            "DERIVED_CONDITIONAL__EXTERNAL_REPAIR_ACCEPTED__"
            "PREREGISTERED_AT_A4DACEA9"
        ),
        "G181 endpoint-classification landing changed",
    )
    require(by_id["G181"]["epistemic_label"] == "MIXED", "G181 label changed")
    require(
        by_id["G181"]["active_use"]
        == "ACTIVE_BOUNDED_ONE_SIDED_ENDPOINT_CLASSIFICATION_ON_SUPPLIED_SMOOTH_REGULAR_INTERIOR_PAIR_FAMILIES_ONLY",
        "G181 active scope widened",
    )
    for open_item in (
        "physical observer event pair-germ and family selection",
        "two-sided branch and immersion carry",
        "null cut focal topology-changing and global completion strata",
        "non-scalar transport",
        "metric-space distance and numerical Xmax",
        "dynamics action source matter bootstrap radiative transfer observations and signalling",
    ):
        require(open_item in by_id["G181"]["open_scope"], f"G181 open boundary absent: {open_item}")
    for guard in (
        "G181 called canon unconditional singularity theorem global completion family selector or metric-space distance",
        "finite tape called physical distance",
        "integrable m called sufficient without completed coefficient limits",
        "m tending zero called universally regular or universally singular",
        "m tending infinity called infinite tape",
        "one-sided removable auxiliary stall called two-sided smooth immersion carry",
        "pair-metric normalization called branch gluing",
        "tape class called depth class",
        "zero radial speed called zero complete tangent",
        "angular turns called singular",
        "supplied family called selected physical history",
        "numerical Xmax fit observation action source matter bootstrap radiative transfer or signalling imported",
    ):
        require(guard in by_id["G181"]["forbidden_regression"], f"G181 guard absent: {guard}")
    g181 = ROOT / "udt_g181_completed_pair_singular_endpoint_classification_2026-08-19"
    require(
        by_id["G181"]["controlling_source"]
        == "udt_g181_completed_pair_singular_endpoint_classification_2026-08-19/AUDIT_REPORT.md",
        "G181 source changed",
    )
    require((g181 / "VERIFICATION_RESULT.json").is_file(), "G181 verification result missing")
    require((g181 / "EXTERNAL_REVIEW_ADJUDICATION.md").is_file(), "G181 adjudication missing")
    require((g181 / "REVIEW_REPAIR_PREREGISTRATION.md").is_file(), "G181 repair preregistration missing")
    require(
        (g181 / "EXTERNAL_REPAIR_FOLLOWUP_RAW.md").read_text().startswith("G181_REPAIR_ACCEPTED"),
        "G181 repair-only external acceptance missing",
    )
    require(
        '"external_followup": "G181_REPAIR_ACCEPTED"'
        in (g181 / "VERIFICATION_RESULT.json").read_text(),
        "G181 accepted verdict not recorded",
    )
    require((g181 / "TRANSMISSION_RECORD.md").is_file(), "G181 transmission record missing")

    require(
        by_id["G182"]["current_status"].startswith(
            "DERIVED_CONDITIONAL__EXTERNALLY_ACCEPTED_WITH_STATED_BOUNDS__"
            "PREREGISTERED_AT_0460674B"
        ),
        "G182 two-sided-carry landing changed",
    )
    require(by_id["G182"]["epistemic_label"] == "MIXED", "G182 label changed")
    require(
        by_id["G182"]["active_use"]
        == "ACTIVE_BOUNDED_TWO_SIDED_COMPLETED_PAIR_METRIC_AND_IMMERSION_MATCHING_CLASSIFICATION_ON_SUPPLIED_BRANCHES_AND_SUPPLIED_SEAM_CARRY_ONLY",
        "G182 active scope widened",
    )
    for open_item in (
        "physical observer event pair-germ branch and family selection",
        "unsupplied seam calibration carry",
        "null degenerate cut focal conjugate caustic branch crossing winding topology-changing and global completion strata",
        "non-scalar transport",
        "metric-space distance and numerical Xmax",
        "observations dynamics action source matter bootstrap radiative transfer and signalling",
    ):
        require(open_item in by_id["G182"]["open_scope"], f"G182 open boundary absent: {open_item}")
    for guard in (
        "G182 called canon unconditional branch selector global carry physical distance or singularity theorem",
        "supplied seam identification called metric-derived",
        "scalar Phi matching called shift metric or immersion carry",
        "completed metric matching called tangent direction or extrinsic jet matching",
        "Gram map called injective",
        "tangent magnitude called direction",
        "even stall called smooth or odd stall called cusp",
        "clock or shear erased as gauge while retaining the same query",
        "local theorem globalized",
        "Xmax observations dynamics action source matter bootstrap radiative transfer or signalling imported",
    ):
        require(guard in by_id["G182"]["forbidden_regression"], f"G182 guard absent: {guard}")
    g182 = ROOT / "udt_g182_completed_pair_two_sided_carry_classification_2026-08-19"
    require(
        by_id["G182"]["controlling_source"]
        == "udt_g182_completed_pair_two_sided_carry_classification_2026-08-19/AUDIT_REPORT.md",
        "G182 source changed",
    )
    require((g182 / "VERIFICATION_RESULT.json").is_file(), "G182 verification result missing")
    require((g182 / "EXTERNAL_REVIEW_ADJUDICATION.md").is_file(), "G182 adjudication missing")
    require((g182 / "TRANSMISSION_RECORD.md").is_file(), "G182 transmission record missing")
    require(
        "G182_ACCEPTED_WITH_STATED_BOUNDS"
        in (g182 / "EXTERNAL_ADVERSARIAL_REVIEW_RAW.md").read_text(),
        "G182 external acceptance missing",
    )
    require(
        '"external_review_accepted": true'
        in (g182 / "VERIFICATION_RESULT.json").read_text(),
        "G182 accepted verdict not recorded",
    )

    require(
        by_id["G183"]["current_status"].startswith(
            "DERIVED_CONDITIONAL__EXTERNAL_REPAIR_FOLLOWUP_ACCEPTED__"
            "PREREGISTERED_AT_65645E65"
        ),
        "G183 pair-strata landing changed",
    )
    require(by_id["G183"]["epistemic_label"] == "MIXED", "G183 label changed")
    require(
        by_id["G183"]["active_use"]
        == "ACTIVE_BOUNDED_LOCAL_PAIR_DOMAIN_AND_REGULAR_MULTIBRANCH_OUTPUT_TYPE_CLASSIFICATION_ON_SUPPLIED_QUERIES_ONLY",
        "G183 active scope widened",
    )
    for open_item in (
        "physical observer event pair-germ branch and family selection",
        "equivalence quotient among regular branches",
        "nontrivial holonomy and non-scalar transport",
        "topology-changing and global completion strata",
        "positive metric-space distance and numerical Xmax",
        "observations dynamics action source matter bootstrap radiative transfer and signalling",
    ):
        require(open_item in by_id["G183"]["open_scope"], f"G183 open boundary absent: {open_item}")
    for guard in (
        "G183 called canon unconditional branch selector physical distance singularity theorem or global completion",
        "null curve called pair-plane degeneracy",
        "null chosen clock called intrinsic plane degeneracy",
        "every zero Gram determinant called tangent rank loss outside the valid timelike-clock hypothesis",
        "spacelike plane admitted as observer pair",
        "conjugate direction outside the sampled variation called focal failure of the pair germ",
        "regular cut crossing or winding branches scalarized identified or selected by equal endpoints Phi or h",
        "branch label called holonomy",
        "local theorem globalized",
        "Xmax observations dynamics action source matter bootstrap radiative transfer or signalling imported",
    ):
        require(guard in by_id["G183"]["forbidden_regression"], f"G183 guard absent: {guard}")
    g183 = ROOT / "udt_g183_pair_degenerate_multibranch_strata_classification_2026-08-19"
    require(
        by_id["G183"]["controlling_source"]
        == "udt_g183_pair_degenerate_multibranch_strata_classification_2026-08-19/AUDIT_REPORT.md",
        "G183 source changed",
    )
    for name in (
        "VERIFICATION_RESULT.json",
        "EXTERNAL_REVIEW_ADJUDICATION.md",
        "REVIEW_REPAIR_PREREGISTRATION.md",
        "EXTERNAL_REPAIR_FOLLOWUP_ADJUDICATION.md",
        "TRANSMISSION_RECORD.md",
        "EXTERNAL_REPAIR_FOLLOWUP_TRANSCRIPT.txt.gz",
    ):
        require((g183 / name).is_file(), f"G183 evidence missing: {name}")
    require(
        "G183_REPAIR_ACCEPTED" in (g183 / "EXTERNAL_REPAIR_FOLLOWUP_RAW.md").read_text(),
        "G183 repair-only external acceptance missing",
    )
    g183_verification = (g183 / "VERIFICATION_RESULT.json").read_text()
    require('"external_review": "ACCEPTED"' in g183_verification, "G183 accepted review state absent")
    require('"external_review_accepted": true' in g183_verification, "G183 acceptance check absent")

    require(
        by_id["G184"]["current_status"].startswith(
            "DERIVED_CONDITIONAL__FRESH_EXTERNAL_REPAIR_FOLLOWUP_ACCEPTED__"
            "PREREGISTERED_AT_32D53AB9"
        ),
        "G184 realization-equivalence landing changed",
    )
    require(by_id["G184"]["epistemic_label"] == "MIXED", "G184 label changed")
    require(
        by_id["G184"]["active_use"]
        == "ACTIVE_BOUNDED_REGULAR_TYPED_REALIZATION_EQUIVALENCE_AND_COMPLETED_KERNEL_DESCENT_CLASSIFICATION_ON_SUPPLIED_QUERIES_ONLY",
        "G184 active scope widened",
    )
    for open_item in (
        "physical query symmetry group and branch population",
        "physical observer event pair-germ and family realization",
        "complete invariant or minimal sufficient descriptor for every possible requested channel",
        "nontrivial holonomy Jacobi connection and non-scalar transport",
        "degenerate topology-changing and global completion strata",
        "positive metric-space distance and numerical Xmax",
        "observations dynamics action source matter bootstrap radiative transfer and signalling",
    ):
        require(open_item in by_id["G184"]["open_scope"], f"G184 open boundary absent: {open_item}")
    for guard in (
        "G184 called canon unconditional physical branch quotient selector complete realization invariant or global completion",
        "strict and query-symmetry quotients silently conflated",
        "ambient reflection orientation reversal observer swap or screen flip admitted without query typing",
        "equal endpoints Phi tape pair metric or image called proof of realization equivalence",
        "completed scalar kernel weakened or reopened because it is many-to-one",
        "extrinsic curvature or covering degree scalarized into Phi",
        "winding label called holonomy",
        "physical branch selected",
        "local regular theorem globalized",
        "Xmax observations dynamics action source matter bootstrap radiative transfer or signalling imported",
    ):
        require(guard in by_id["G184"]["forbidden_regression"], f"G184 guard absent: {guard}")
    g184 = ROOT / "udt_g184_regular_branch_equivalence_classification_2026-08-19"
    require(
        by_id["G184"]["controlling_source"]
        == "udt_g184_regular_branch_equivalence_classification_2026-08-19/AUDIT_REPORT.md",
        "G184 source changed",
    )
    for name in (
        "VERIFICATION_RESULT.json",
        "EXTERNAL_REVIEW_ADJUDICATION.md",
        "REVIEW_REPAIR_PREREGISTRATION.md",
        "EXTERNAL_REPAIR_FOLLOWUP_ADJUDICATION.md",
        "TRANSMISSION_RECORD.md",
        "FOLLOWUP_TRANSMISSION_RECORD.md",
        "EXTERNAL_REPAIR_FOLLOWUP_TRANSCRIPT.txt.gz",
    ):
        require((g184 / name).is_file(), f"G184 evidence missing: {name}")
    require(
        "G184_REPAIR_ACCEPTED" in (g184 / "EXTERNAL_REPAIR_FOLLOWUP_RAW.md").read_text(),
        "G184 repair-only external acceptance missing",
    )
    g184_verification = (g184 / "VERIFICATION_RESULT.json").read_text()
    require('"external_review": "ACCEPTED"' in g184_verification, "G184 accepted review state absent")
    require('"external_review_accepted": true' in g184_verification, "G184 acceptance check absent")

    guard_rows = read_tsv(
        ROOT / "udt_foundational_semantic_regression_correction_2026-07-26/SEMANTIC_GUARD_UNIVERSE.tsv"
    )
    require(len(guard_rows) == 16, "guard universe must contain exactly 16 rows")
    guard_sources = {row["guard_id"]: row["controlling_source"] for row in guard_rows}
    for guard, source in guard_sources.items():
        if guard in {"G01", "G02", "G12", "G14"}:
            expected = {
                "G01": "udt_founding_phi_ownership_morphism_audit_2026-08-05/AUDIT_REPORT.md",
                "G02": "udt_founding_phi_ownership_morphism_audit_2026-08-05/EXACT_DERIVATION.md",
                "G12": "udt_complete_pair_phi_orchestra_audit_2026-08-05/AUDIT_REPORT.md",
                "G14": "udt_g163_xmax_dependency_reversal_audit_2026-08-18/AUDIT_REPORT.md",
            }[guard]
            require(
                by_id[guard]["controlling_source"] == expected,
                f"relational correction source priority changed: {guard}",
            )
        else:
            require(by_id[guard]["controlling_source"] == source, f"source priority changed: {guard}")

    expected_sources = {row["controlling_source"] for row in rows}
    for source in expected_sources:
        require((ROOT / source).is_file(), f"missing controlling source: {source}")

    validate_startup_surface(ROOT)

    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    for token in [
        "on **supplied ordered depth**",
        "presentation potential",
        "complete observer/event/path-to-depth assignment",
        "Angular, screen, and mixing data",
        "observed clock/ruler calibration scale",
        "CHALLENGED_OWNER_POSTULATE_NOT_DERIVED",
        "native scalar kernel ends at dimensionless `chi=tanh(phi_pair)`",
        "preferred center",
        "S^2` carrier is a `POSIT",
        "EH metric-only action is `CONDITIONAL",
        "Bootstrap/stable-matter is a working hypothesis",
        "Primary-kernel regression gate",
        "germ -> h=F^*g -> complete-pair Dual Reciprocity -> endpoint Phi values -> endpoint difference",
        "G142--G160 abstract carrier/carry/score architecture remains conditional historical control",
        "archive/scaffolded_kernel_controls_2026-08-19/README.md",
    ]:
        require(token in agents, f"AGENTS guard absent: {token}")

    scaffold_archive = ROOT / "archive/scaffolded_kernel_controls_2026-08-19/README.md"
    require(scaffold_archive.is_file(), "scaffolded-kernel quarantine pointer missing")
    scaffold_text = " ".join(scaffold_archive.read_text(encoding="utf-8").split())
    for token in (
        "quarantines a **use**, not the immutable evidence packages",
        "They are not the active derivation route",
        "complete pullback h=F^*g",
        "blocks regression from the metric pullback back to an independently scaffolded kernel",
    ):
        require(token in scaffold_text, f"scaffolded-kernel quarantine guard absent: {token}")

    xmax_controls = ("AGENTS.md", "LIVE.md", "CURRENT_SCIENTIFIC_PREMISES.md")
    xmax_source = "udt_g163_xmax_dependency_reversal_audit_2026-08-18/AUDIT_REPORT.md"
    for control in xmax_controls:
        text = (ROOT / control).read_text(encoding="utf-8")
        require("X_max" in text, f"control lacks Xmax guard: {control}")
        require("asymptot" in text.lower(), f"control lacks Xmax limiting meaning: {control}")
    require("udt_g163_xmax_dependency_reversal_audit_2026-08-18/" in
            (ROOT / "INDEX.md").read_text(encoding="utf-8"),
            "INDEX lacks controlling Xmax dependency-reversal route")
    require((ROOT / xmax_source).is_file(), "controlling Xmax correction source missing")

    adjudication = read_tsv(
        ROOT / "udt_foundational_semantic_regression_correction_2026-07-26/ACTIVE_SEMANTIC_ADJUDICATION.tsv"
    )
    require(len(adjudication) == 754, "semantic candidate adjudication must contain 754 rows")
    require(len({row["candidate_id"] for row in adjudication}) == 754, "duplicate semantic candidate id")
    require(len({row["path"] for row in adjudication}) == 754, "duplicate semantic candidate path")
    require(all(row["controlling_disposition"] for row in adjudication), "unadjudicated semantic candidate")

    dof = ROOT / "udt_global_functional_dof_constraint_rank_audit_2026-07-26"
    status = {row["id"]: row for row in read_tsv(dof / "STATUS_LEDGER.tsv")}
    presentation = {row["id"]: row for row in read_tsv(dof / "LOCAL_PRESENTATION_RANK.tsv")}
    require(status["S03"]["status"] == "CHOSE_COMPARISON_F4_7_TOTAL", "DOF independent phi still native")
    require(status["S04"]["status"] == "DERIVED_FOUNDED_PHI_ADDS_ZERO__COMPLETE_EXTENSION_OPEN", "DOF founded phi still conditional")
    require(presentation["P04"]["status"] == "CHOSE_COMPARISON_CONFIGURATION", "DOF comparison branch promotion")
    require(presentation["P05"]["status"] == "DERIVED_FOUNDED_SUBGROUP__FULL_EXTENSION_OPEN", "DOF founded branch regression")
    print(
        "PASS: G221-extended premise guards; PASS: 205-row premise "
        "registry, current bounded startup route, archive integrity, "
        "relational-depth/orchestra guards, X_max semantics, 754 historical dispositions, "
        "and corrected DOF semantics"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Bounded no-write provenance checks for the active G166--G196 kernel chain."""

from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CORE_PRODUCTION = (
    "udt_g166_primary_metric_ordered_pair_kernel_descent_2026-08-18/derive_primary_pair_kernel.py",
    "udt_g167_primary_metric_full_pair_pullback_orchestra_2026-08-18/derive_primary_metric_pair_pullback.py",
    "udt_g168_ordered_copresent_pair_plane_ownership_2026-08-18/derive_pair_plane_ownership.py",
    "udt_g170_endpoint_relative_bidirectional_pair_response_2026-08-19/derive_endpoint_relative_response.py",
    "udt_g171_primary_metric_multi_pair_response_2026-08-19/derive_multi_pair_response.py",
    "udt_g176_completed_pair_dual_reciprocity_consolidation_2026-08-19/derive_completed_pair_reciprocity.py",
    "udt_g179_complete_coframe_pair_pullback_extension_2026-08-19/derive_complete_coframe_extension.py",
    "udt_g180_completed_pair_smooth_family_descent_2026-08-19/derive_completed_pair_family.py",
    "udt_g188_complete_coframe_null_jacobi_extension_2026-08-20/derive_complete_coframe_null_jacobi.py",
    "udt_g190_completed_pair_timelive_frequency_screen_join_2026-08-20/derive_timelive_frequency_screen.py",
    "udt_g191_nonconformal_timelive_mixing_join_2026-08-20/derive_nonconformal_timelive_mixing.py",
    "udt_g192_smooth_timelive_mixing_family_classification_2026-08-20/derive_smooth_timelive_mixing.py",
    "udt_g193_noncommuting_transverse_mixing_extension_2026-08-20/derive_noncommuting_transverse_mixing.py",
    "udt_g194_general_symmetric_screen_mixing_closure_2026-08-20/derive_general_symmetric_screen_mixing.py",
    "udt_g195_antisymmetric_screen_rotation_boundary_2026-08-20/derive_antisymmetric_screen_rotation.py",
    "udt_g196_longitudinal_screen_mixing_descent_2026-08-20/derive_longitudinal_screen_mixing.py",
)

LIVE_FAMILY_PRODUCTION = CORE_PRODUCTION[-6:]
BANNED_EXECUTABLE_NAMES = {"P1", "G116", "G189", "Xmax", "X_max", "transfer", "luminosity"}


def parse(relative: str) -> tuple[str, ast.AST]:
    text = (ROOT / relative).read_text(encoding="utf-8")
    return text, ast.parse(text, filename=relative)


def imports(tree: ast.AST) -> list[str]:
    found: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            found.append(node.module or "")
    return found


def executable_names(tree: ast.AST) -> set[str]:
    return {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}


def main() -> None:
    missing = [relative for relative in CORE_PRODUCTION if not (ROOT / relative).is_file()]
    assert not missing, missing

    local_imports: dict[str, list[str]] = {}
    for relative in CORE_PRODUCTION:
        _, tree = parse(relative)
        suspect = [module for module in imports(tree) if module.startswith(("udt_", "G"))]
        if suspect:
            local_imports[relative] = suspect
    assert not local_imports, local_imports

    banned_names: dict[str, list[str]] = {}
    for relative in LIVE_FAMILY_PRODUCTION:
        _, tree = parse(relative)
        found = sorted(executable_names(tree) & BANNED_EXECUTABLE_NAMES)
        if found:
            banned_names[relative] = found
    assert not banned_names, banned_names

    g190_text, _ = parse(CORE_PRODUCTION[9])
    assert "# Post-result G116 algebraic regression only" in g190_text
    assert g190_text.index("def conformal_timelive_control") < g190_text.index(
        "# Post-result G116 algebraic regression only"
    )
    assert '"p1_used": False' in g190_text
    assert '"xmax_used": False' in g190_text
    assert '"radiative_transfer_derived": False' in g190_text

    g176 = (ROOT / "udt_g176_completed_pair_dual_reciprocity_consolidation_2026-08-19/AUDIT_REPORT.md").read_text(
        encoding="utf-8"
    )
    assert "WORKING_FOUNDATIONAL_CLARIFICATION" in g176
    assert "conditional on the adopted working clarification" in g176
    assert "does not select pair events or germs" in g176

    g196 = (ROOT / "udt_g196_longitudinal_screen_mixing_descent_2026-08-20/AUDIT_REPORT.md").read_text(
        encoding="utf-8"
    )
    assert "formula-level regression, not" in g196
    assert "CHOSE_MATHEMATICAL_FUNCTION_FAMILY" in g196
    assert "CHOSE_QUERY" in g196
    assert "P1/G116/G189, observations, transfer, source, `X_max` | `OMITTED`" in g196

    live = (ROOT / "LIVE.md").read_text(encoding="utf-8")
    handoff = (ROOT / "HANDOFF.md").read_text(encoding="utf-8")
    for text in (live, handoff):
        assert "`B,Q` are metric-fixed, `S=0`" in text
        assert "formula-level regression" in text
        assert "G116/G189" in text and "construction inputs" in text
    assert "local across turns or caustics" not in live

    result = {
        "status": "PASS",
        "production_files_parsed": len(CORE_PRODUCTION),
        "live_family_files_checked": len(LIVE_FAMILY_PRODUCTION),
        "repository_local_scientific_imports": 0,
        "banned_live_family_executable_names": 0,
        "g176_working_premise_guard": True,
        "g190_post_result_control_order": True,
        "g196_evidence_scope_guard": True,
        "startup_wording_guards": True,
        "landing": "NATIVE_CORE_RETAINED__PROVENANCE_REPAIRS_REQUIRED",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

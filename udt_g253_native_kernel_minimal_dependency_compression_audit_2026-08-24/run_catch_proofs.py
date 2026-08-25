#!/usr/bin/env python3
"""Hostile in-memory mutations for the G253 dependency contract."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ALLOWED = {
    "LOAD_BEARING_DERIVED",
    "LOAD_BEARING_DERIVED_CONDITIONAL",
    "LOAD_BEARING_WORKING_PREMISE",
    "LOAD_BEARING_SUPPLIED_QUERY_OR_HISTORY",
    "LOAD_BEARING_OBSERVED_ATTACHMENT",
}
FORBIDDEN = {"P1", "G116", "G189", "X_max", "FIT", "OUTCOME", "PROTECTED"}


def source_resolution_gate(record: dict[str, object]) -> None:
    existing = record["existing_layouts"]
    matching = record["matching_layouts"]
    assert isinstance(existing, set) and isinstance(matching, set)
    assert existing <= {"repository", "sealed"}
    assert matching <= existing
    assert existing
    assert matching == existing


def gate(record: dict[str, object]) -> None:
    assert record["classification"] in ALLOWED
    assert record["working_premise_status"] == "WORKING_FOUNDATIONAL_CLARIFICATION"
    assert record["metric_status"] == "SUPPLIED_OR_CONDITIONAL"
    assert record["germ_status"] == "QUERY_SUPPLIED"
    assert record["redshift_formula"] == "log(1+z)=Phi_source-Phi_observer"
    assert record["redshift_needs_angular"] is False
    assert record["angular_origin"] == "metric_connection_curvature_jacobi"
    assert record["angular_timing"] == "upstream_or_sibling_not_post_readout_patch"
    assert record["phi_alone_fixes_angular"] is False
    assert record["scale_changes_relative_depth"] is False
    assert record["scale_changes_normalized_shape"] is False
    assert record["scale_changes_absolute_area"] is True
    assert record["ce_role"] == "clock_ruler_unit_conversion"
    assert record["attachment_role"] == "downstream_same_object_unit_assignment"
    blob = " ".join(record["active_inputs"])
    assert not any(item in blob for item in FORBIDDEN)


BASE = {
    "classification": "LOAD_BEARING_DERIVED_CONDITIONAL",
    "working_premise_status": "WORKING_FOUNDATIONAL_CLARIFICATION",
    "metric_status": "SUPPLIED_OR_CONDITIONAL",
    "germ_status": "QUERY_SUPPLIED",
    "redshift_formula": "log(1+z)=Phi_source-Phi_observer",
    "redshift_needs_angular": False,
    "angular_origin": "metric_connection_curvature_jacobi",
    "angular_timing": "upstream_or_sibling_not_post_readout_patch",
    "phi_alone_fixes_angular": False,
    "scale_changes_relative_depth": False,
    "scale_changes_normalized_shape": False,
    "scale_changes_absolute_area": True,
    "ce_role": "clock_ruler_unit_conversion",
    "attachment_role": "downstream_same_object_unit_assignment",
    "active_inputs": ["metric", "pair_germ", "working_reciprocity"],
}

PKG = Path(__file__).resolve().parent


MUTATIONS = {
    "unsupported_edge": {"classification": "UNSUPPORTED_EDGE"},
    "canonize_working_premise": {"working_premise_status": "DERIVED_CANON"},
    "select_metric_history": {"metric_status": "DERIVED_PHYSICAL_HISTORY"},
    "select_pair_germ": {"germ_status": "METRIC_DERIVED"},
    "angular_redshift_patch": {"redshift_needs_angular": True},
    "post_readout_orchestra": {"angular_timing": "post_readout_patch"},
    "fitted_angular_origin": {"angular_origin": "fitted_template"},
    "phi_only_angular": {"phi_alone_fixes_angular": True},
    "scale_rewrites_depth": {"scale_changes_relative_depth": True},
    "scale_rewrites_shape": {"scale_changes_normalized_shape": True},
    "scale_erases_area": {"scale_changes_absolute_area": False},
    "ce_selects_length": {"ce_role": "absolute_length_selector"},
    "attachment_becomes_kernel": {"attachment_role": "kernel_profile_calibration"},
    "P1_dependency": {"active_inputs": ["metric", "P1"]},
    "G116_dependency": {"active_inputs": ["metric", "G116"]},
    "G189_dependency": {"active_inputs": ["metric", "G189"]},
    "Xmax_dependency": {"active_inputs": ["metric", "X_max"]},
    "fit_dependency": {"active_inputs": ["metric", "FIT"]},
    "outcome_dependency": {"active_inputs": ["metric", "OUTCOME"]},
    "protected_dependency": {"active_inputs": ["metric", "PROTECTED"]},
}

PATH_BASELINES = {
    "repository_layout": {
        "existing_layouts": {"repository"},
        "matching_layouts": {"repository"},
    },
    "sealed_layout": {
        "existing_layouts": {"sealed"},
        "matching_layouts": {"sealed"},
    },
}

PATH_MUTATIONS = {
    "missing_source": {"existing_layouts": set(), "matching_layouts": set()},
    "mismatched_source": {"existing_layouts": {"repository"}, "matching_layouts": set()},
    "conflicting_repository_and_sealed_sources": {
        "existing_layouts": {"repository", "sealed"},
        "matching_layouts": {"repository"},
    },
}


def main() -> None:
    gate(dict(BASE))
    caught = []
    for name, mutation in MUTATIONS.items():
        record = dict(BASE)
        record.update(mutation)
        try:
            gate(record)
        except AssertionError:
            caught.append(name)
        else:
            raise AssertionError(f"hostile mutation escaped: {name}")
    for record in PATH_BASELINES.values():
        source_resolution_gate(record)
    for name, record in PATH_MUTATIONS.items():
        try:
            source_resolution_gate(record)
        except AssertionError:
            caught.append(name)
        else:
            raise AssertionError(f"hostile path mutation escaped: {name}")
    result = {
        "baseline_pass": True,
        "path_resolution_positive_controls": len(PATH_BASELINES),
        "caught": caught,
        "caught_count": len(caught),
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if "--no-write" not in sys.argv[1:]:
        (PKG / "CATCH_PROOF_RESULT.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()

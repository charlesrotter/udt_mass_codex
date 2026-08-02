#!/usr/bin/env python3
"""Fail-closed semantic and provenance verifier for the FC07 response audit."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXPECTED_IDS = [f"W{index:02d}" for index in range(1, 9)]
MAXIMUM = (
    "FC07_FULL_SCREEN_CARTAN_AND_CURVATURE_DERIVED__ALL_NONCONSTANT_REGISTERED_INTERPOLATIONS_HAVE_"
    "NONZERO_BUNDLE_RELATIVE_PROJECTOR_RESPONSE__THREE_VARYING_UNIQUE_H1_CLASSES_HAVE_A_METRIC_"
    "INTRINSIC_GLOBAL_HARMONIC_RULER_CHANNEL__ONE_FORCED_HYPERBOLIC_INSTANCE__THREE_CONSTANT_"
    "SUBFAMILIES_HAVE_A_HOLONOMY_FIXED_RECIPROCAL_PLANE_WITHOUT_SELECTED_AXES__NO_UNIVERSAL_"
    "PROJECTOR_BOOTSTRAP_CLOSURE_XMAX_SELECTION_DYNAMICS_OR_MATTER"
)


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate(response, hodge, selection, holonomy, xmax, derivation, independent) -> None:
    assert [row["candidate_id"] for row in response] == EXPECTED_IDS
    assert [row["candidate_id"] for row in hodge] == EXPECTED_IDS
    assert len(selection) == 24 and all(sum(row["candidate_id"] == wid for row in selection) == 3 for wid in EXPECTED_IDS)
    assert [row["candidate_id"] for row in holonomy] == EXPECTED_IDS
    assert len(xmax) == 5
    assert all(row["orientation"] == "ORIENTABLE" for row in response[:6])
    assert all(row["orientation"] == "NONORIENTABLE" for row in response[6:])
    assert sum(row["screen_response"].startswith("NONZERO") for row in response) == 6
    assert sum(row["screen_response"] == "ZERO_CONSTANT_CONTROL" for row in response) == 2
    assert {row["monodromy_id"] for row in response if row["variation_scope"] == "FORCED_ALL_SPD"} == {"M_PARABOLIC", "M_HYPERBOLIC"}
    assert all(row["generic_midpoint_spatial_curvature_pattern"].startswith("ISOTROPIC_POSITIVE") for row in response[2:])
    assert all(row["generic_midpoint_spatial_curvature_pattern"] == "ZERO_FLAT" for row in response[:2])
    assert sum(row["unique_harmonic_line"] == "YES" for row in hodge) == 4
    assert {row["monodromy_id"] for row in hodge if row["unique_harmonic_line"] == "YES"} == {"M_MINUS_IDENTITY", "M_ORDER4_ROTATION", "M_ORDER6_ELLIPTIC", "M_HYPERBOLIC"}
    assert sum(row["channel_type"] == "NONIDENTITY_FOR_VARYING_h" and row["unique_harmonic_line"] == "YES" for row in hodge) == 3
    assert next(row for row in response if row["monodromy_id"] == "M_HYPERBOLIC")["variation_scope"] == "FORCED_ALL_SPD"
    assert next(row for row in response if row["monodromy_id"] == "M_HYPERBOLIC")["intrinsic_projector_class"] == "METRIC_INTRINSIC_GLOBAL_ON_REGISTERED_PRODUCT"
    assert next(row for row in response if row["monodromy_id"] == "M_PARABOLIC")["intrinsic_projector_class"] == "BUNDLE_RELATIVE_CONDITIONAL"
    assert all(row["physical_selection"] == "NONE" for row in response)
    assert {row["monodromy_id"] for row in holonomy if row["holonomy_ruling"] == "UNIQUE_HOLONOMY_FIXED_LORENTZIAN_RECIPROCAL_TWO_PLANE"} == {"M_MINUS_IDENTITY", "M_ORDER4_ROTATION", "M_ORDER6_ELLIPTIC"}
    assert all(row["axis_ruling"] == "NO_UNIQUE_CLOCK_RULER_AXES_OBSERVER_FRAME_FAMILY_RETAINED" for row in holonomy if row["holonomy_ruling"].startswith("UNIQUE_HOLONOMY"))
    assert all(row["relative_response"] == "ZERO_CONSTANT_SCREEN" and row["physical_observer_selection"] == "NONE" for row in holonomy)
    assert {row["classification"] for row in selection if row["object"] == "relative_projector_response"} <= {"NONZERO_SOMEWHERE_STRATIFIED", "ZERO_RESPONSE_CONTROL", "UNDEFINED_SELECTION_GATE_FAILED"}
    assert next(row for row in xmax if row["gate"] == "proper_base_scale")["ruling"] == "CHOSE_NOT_XMAX"
    assert next(row for row in xmax if row["gate"] == "observer_pair_dilation")["ruling"] == "XMAX_ENDPOINT_NOT_AVAILABLE_IN_THIS_BOUNDED_FAMILY"
    assert next(row for row in xmax if row["gate"] == "bootstrap")["ruling"] == "NO_NATIVE_EQUATION_FEEDBACK_OR_SAME_SOLUTION_CLOSURE"
    assert derivation["status"] == independent["status"] == "PASS"
    assert derivation["maximum_conclusion"] == MAXIMUM
    assert derivation["exact_checks"] == 69 and independent["check_count"] == 155
    assert derivation["generic_varying_controls"] == 6 and derivation["unique_H1_completions"] == 4
    assert derivation["varying_unique_H1_intrinsic_ruler_channels"] == 3
    assert derivation["constant_subfamily_unique_reciprocal_pair_planes"] == 3
    assert derivation["forced_varying_unique_H1_channels"] == ["M_HYPERBOLIC"]
    assert derivation["forced_varying_ambiguous_H1_channels"] == ["M_PARABOLIC"]
    assert derivation["universal_metric_ruler_projector"] is False
    assert derivation["native_bootstrap_return"] is False
    assert derivation["Xmax_derived"] is False
    assert derivation["physical_selection"] is False


def verify_sources() -> int:
    source_rows = rows("SOURCE_MANIFEST.tsv")
    assert len(source_rows) == 23 and len({row["path"] for row in source_rows}) == 23
    for row in source_rows:
        path = row["path"]
        base = row["base_commit"]
        blob = subprocess.run(["git", "ls-tree", base, "--", path], cwd=ROOT, text=True, capture_output=True, check=True).stdout.split()[2]
        payload = subprocess.run(["git", "show", f"{base}:{path}"], cwd=ROOT, capture_output=True, check=True).stdout
        assert blob == row["git_blob"]
        assert hashlib.sha256(payload).hexdigest() == row["sha256"]
        assert len(payload) == int(row["bytes"])
    return len(source_rows)


def verify_anchors() -> int:
    source_rows = {row["path"]: row for row in rows("SOURCE_MANIFEST.tsv")}
    anchors = rows("SOURCE_ANCHOR_LEDGER.tsv")
    assert len(anchors) == 15
    for row in anchors:
        source = source_rows[row["path"]]
        payload = subprocess.run(
            ["git", "show", f"{source['base_commit']}:{row['path']}"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        ).stdout
        assert row["exact_anchor"] in payload
    return len(anchors)


def main() -> int:
    response = rows("MONODROMY_CARTAN_RESPONSE_ATLAS.tsv")
    hodge = rows("HODGE_RETURN_CHANNEL.tsv")
    selection = rows("INTRINSIC_SELECTION_ATLAS.tsv")
    holonomy = rows("CONSTANT_SCREEN_HOLONOMY_ATLAS.tsv")
    xmax = rows("XMAX_AND_BOOTSTRAP_TYPE_GATE.tsv")
    derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    validate(response, hodge, selection, holonomy, xmax, derivation, independent)
    sources = verify_sources()
    anchors = verify_anchors()

    mutations = []
    for index in range(8):
        changed = deepcopy(response); changed[index]["candidate_id"] = "W99"
        mutations.append((changed, deepcopy(hodge), deepcopy(selection), deepcopy(holonomy), deepcopy(xmax), deepcopy(derivation), deepcopy(independent)))
    changed = deepcopy(response); changed[0]["screen_response"] = "NONZERO_EVERY_INTERIOR_POINT_GENERIC_CONTROL"
    mutations.append((changed, deepcopy(hodge), deepcopy(selection), deepcopy(holonomy), deepcopy(xmax), deepcopy(derivation), deepcopy(independent)))
    changed = deepcopy(response); next(row for row in changed if row["monodromy_id"] == "M_PARABOLIC")["intrinsic_projector_class"] = "METRIC_INTRINSIC_GLOBAL_ON_REGISTERED_PRODUCT"
    mutations.append((changed, deepcopy(hodge), deepcopy(selection), deepcopy(holonomy), deepcopy(xmax), deepcopy(derivation), deepcopy(independent)))
    changed = deepcopy(response); next(row for row in changed if row["monodromy_id"] == "M_HYPERBOLIC")["variation_scope"] = "OPTIONAL_FIXED_SUBFAMILY_EXISTS"
    mutations.append((changed, deepcopy(hodge), deepcopy(selection), deepcopy(holonomy), deepcopy(xmax), deepcopy(derivation), deepcopy(independent)))
    changed = deepcopy(response); changed[6]["orientation"] = "ORIENTABLE"
    mutations.append((changed, deepcopy(hodge), deepcopy(selection), deepcopy(holonomy), deepcopy(xmax), deepcopy(derivation), deepcopy(independent)))
    changed = deepcopy(response); changed[2]["generic_midpoint_spatial_curvature_pattern"] = "ANISOTROPIC"
    mutations.append((changed, deepcopy(hodge), deepcopy(selection), deepcopy(holonomy), deepcopy(xmax), deepcopy(derivation), deepcopy(independent)))
    changed = deepcopy(hodge); changed[0]["unique_harmonic_line"] = "YES"
    mutations.append((deepcopy(response), changed, deepcopy(selection), deepcopy(holonomy), deepcopy(xmax), deepcopy(derivation), deepcopy(independent)))
    changed = deepcopy(hodge); changed[5]["channel_type"] = "IDENTITY_CONSTANT_CONTROL"
    mutations.append((deepcopy(response), changed, deepcopy(selection), deepcopy(holonomy), deepcopy(xmax), deepcopy(derivation), deepcopy(independent)))
    changed = deepcopy(selection); next(row for row in changed if row["candidate_id"] == "W05" and row["object"] == "relative_projector_response")["classification"] = "NONZERO_GLOBAL_CHANNEL"
    mutations.append((deepcopy(response), deepcopy(hodge), changed, deepcopy(holonomy), deepcopy(xmax), deepcopy(derivation), deepcopy(independent)))
    changed = deepcopy(holonomy); changed[1]["axis_ruling"] = "UNIQUE_CLOCK_AXIS"
    mutations.append((deepcopy(response), deepcopy(hodge), deepcopy(selection), changed, deepcopy(xmax), deepcopy(derivation), deepcopy(independent)))
    changed = deepcopy(xmax); next(row for row in changed if row["gate"] == "proper_base_scale")["ruling"] = "DERIVED_XMAX"
    mutations.append((deepcopy(response), deepcopy(hodge), deepcopy(selection), deepcopy(holonomy), changed, deepcopy(derivation), deepcopy(independent)))
    changed = deepcopy(xmax); next(row for row in changed if row["gate"] == "bootstrap")["ruling"] = "BOOTSTRAP_CLOSED"
    mutations.append((deepcopy(response), deepcopy(hodge), deepcopy(selection), deepcopy(holonomy), changed, deepcopy(derivation), deepcopy(independent)))
    for field in ("universal_metric_ruler_projector", "native_bootstrap_return", "Xmax_derived", "physical_selection"):
        changed = deepcopy(derivation); changed[field] = True
        mutations.append((deepcopy(response), deepcopy(hodge), deepcopy(selection), deepcopy(holonomy), deepcopy(xmax), changed, deepcopy(independent)))
    changed = deepcopy(derivation); changed["maximum_conclusion"] = "BOOTSTRAP_AND_MASS_DERIVED"
    mutations.append((deepcopy(response), deepcopy(hodge), deepcopy(selection), deepcopy(holonomy), deepcopy(xmax), changed, deepcopy(independent)))
    changed = deepcopy(independent); changed["check_count"] = 0
    mutations.append((deepcopy(response), deepcopy(hodge), deepcopy(selection), deepcopy(holonomy), deepcopy(xmax), deepcopy(derivation), changed))

    caught = 0
    for mutation in mutations:
        try:
            validate(*mutation)
        except AssertionError:
            caught += 1
    assert caught == len(mutations)
    result = {
        "schema": "udt.fc07_cartan_response_return.verification.v1",
        "status": "PASS",
        "source_identities": sources,
        "source_anchors": anchors,
        "semantic_mutations": len(mutations),
        "semantic_mutations_caught": caught,
        "maximum_conclusion": MAXIMUM,
        "promotions_rejected": ["universal_projector", "bootstrap_closure", "Xmax_derivation", "physical_selection", "matter_or_mass"],
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

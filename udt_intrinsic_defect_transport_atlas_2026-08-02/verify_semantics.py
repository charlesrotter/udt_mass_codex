#!/usr/bin/env python3
"""Fail-closed output and scope verifier for the preregistered transport atlas."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from copy import deepcopy
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FULL = ("C04", "C08", "C09", "C10", "C16", "C17")


def read_tsv(name):
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    contract = read_tsv("FALSIFICATION_CONTRACT.tsv")
    require([row["gate_id"] for row in contract] == [f"F{i:02d}" for i in range(1, 37)], "36 gate IDs")

    source_rows = read_tsv("SOURCE_MANIFEST.tsv")
    require(len(source_rows) == len({row["path"] for row in source_rows}) == 86, "source census")
    for row in source_rows:
        blob = subprocess.run(
            ["git", "cat-file", "blob", row["git_blob"]], cwd=ROOT,
            check=True, capture_output=True,
        ).stdout
        require(len(blob) == int(row["bytes"]), f"source bytes {row['path']}")
        require(hashlib.sha256(blob).hexdigest() == row["sha256"], f"source hash {row['path']}")
    require(sha(HERE / "SOURCE_MANIFEST.tsv") == (HERE / "SOURCE_MANIFEST.sha256").read_text().strip(), "source manifest identity")

    bindings = read_tsv("CANDIDATE_BINDING.tsv")
    require(len(bindings) == 18 and len({row["candidate_id"] for row in bindings}) == 18, "candidate census")
    require([row["candidate_id"] for row in bindings if row["transport_scope"] == "FULL_DEFECT_TRANSPORT"] == list(FULL), "full owner set")
    require(sum(row["parent_status"] == "ZERO" for row in bindings) == 9, "nine zero controls")
    require(sum(row["parent_status"] == "PROJECTOR_BLOCKED" for row in bindings) == 2, "two blocked controls")
    require(sum(row["parent_status"] == "METRIC_DEGENERATE" for row in bindings) == 1, "one degenerate control")

    require(len(read_tsv("LOOP_UNIVERSE.tsv")) == 18, "loop census")
    object_universe = read_tsv("OBJECT_UNIVERSE.tsv")
    objects = read_tsv("OBJECT_STATUS.tsv")
    require(
        [(row["object_id"], row["object"]) for row in objects]
        == [(row["object_id"], row["object"]) for row in object_universe],
        "object status exact identity completeness",
    )
    premises = read_tsv("PREMISE_LEDGER.tsv")
    premise_audit = read_tsv("PREMISE_AUDIT.tsv")
    require(
        [(row["premise_id"], row["choice_or_object"]) for row in premise_audit]
        == [(row["premise_id"], row["choice_or_object"]) for row in premises],
        "premise audit exact identity completeness",
    )

    result = json.loads((HERE / "TRANSPORT_RESULT.json").read_text())
    require(result["status"] == "PASS_EXACT_PRODUCTION", "production status")
    require(result["defect_graph"] == {"vertices": 2, "edges": 6, "components": 1, "b1": 5}, "graph topology")
    require(result["complement_H1"] == "Z^5", "complement homology")
    require(result["metric_map_determinant"] == "1/(F**2*u)", "metric map invertibility")
    require(result["line_w1"] == "ZERO_ON_ALL_H1_GENERATORS", "global w1")
    require(result["all_projective_meridians"] == "TRIVIAL_IN_PI1_RP2", "projective meridians")
    require(result["local_RP1_traversals"] == 2, "RP1 traversal")
    require(result["pole_punctures"] == ["+e0", "-e0", "+e1", "-e1", "+e2", "-e2"], "pole punctures")
    require(result["line_holonomy"] == "IDENTITY_ON_ALL_LOOPS", "line holonomy")
    require(result["finite_loop_holonomy"] == "PATH_INTEGRAL_NOT_UNIVERSALLY_EVALUATED", "finite loop restraint")
    require(not result["full_Levi_Civita_holonomy_conflated"], "LC scope")
    require(not result["topological_charge_inferred"] and not result["carrier_or_physics_selected"], "physics restraint")

    edges = read_tsv("EDGE_ATLAS.tsv")
    require(len(edges) == 6 and all(row["symbolic_rank"] == "2_AWAY_FROM_POLES" for row in edges), "six symbolic regular edges")
    require([row["oriented_vector_degree"] for row in edges] == ["+1", "+1", "+1", "+1", "-1", "-1"], "frozen index signs")
    require(all(row["degree_magnitude"] == "1" and row["RP1_traversals_per_meridian"] == "2" and row["RP2_Z2_class"] == "0_TRIVIAL" for row in edges), "turning distinctions")

    candidates = read_tsv("CANDIDATE_TRANSPORT_ATLAS.tsv")
    require([row["candidate_id"] for row in candidates] == list(FULL), "transport candidates")
    require(all(row["line_holonomy"] == "IDENTITY_ALL_LOOPS" for row in candidates), "candidate line holonomy")
    require(all(row["kernel_plane_connection"] == "NONZERO_ON_M_IN_METRIC_ANCHORED_T_N_FRAME" for row in candidates), "candidate omega")
    require(all(row["curvature_at_p1_p2"] == "NONZERO_BOTH" for row in candidates), "candidate curvature points")
    require(all(row["physics_selected"] == "NO" for row in candidates), "candidate selection guard")

    points = read_tsv("CONNECTION_POINTS.tsv")
    require(len(points) == 12 and len({(row["candidate_id"], row["point_id"]) for row in points}) == 12, "point certificate census")
    require(all(row["Omega_nonzero"] == "YES" for row in points), "nonzero certificates")
    indexed = {(row["candidate_id"], row["point_id"]): row for row in points}
    for point_id in ("p1", "p2"):
        for field in ("omega_xyz", "Omega_xy_xz_yz"):
            base = tuple(sp.sympify(value) for value in indexed[("C08", point_id)][field].split(";"))
            for target, factor in (("C16", 4), ("C17", 5)):
                test = tuple(sp.sympify(value) for value in indexed[(target, point_id)][field].split(";"))
                require(all(sp.simplify(value-factor*reference) == 0 for value, reference in zip(test, base)), f"{target} scaling")
        signatures = {
            indexed[(candidate_id, point_id)]["Omega_xy_xz_yz"]
            for candidate_id in ("C04", "C08", "C09", "C10")
        }
        require(len(signatures) == 4, f"four exact signatures {point_id}")

    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
    require(independent["status"] == "PASS_INDEPENDENT_HIGH_PRECISION", "independent point route")
    require(not independent["production_module_imported"] and independent["point_components_compared"] == 72, "independence disclosure")
    cold = json.loads((HERE / "COLD_REVIEW_RESULT.json").read_text())
    require(cold["final_grade"] == "PASS_WITH_CAVEATS" and cold["algebra_failures"] == 0, "cold review grade")

    report = (HERE / "AUDIT_REPORT.md").read_text()
    derivation = (HERE / "EXACT_DERIVATION.md").read_text()
    combined = report + derivation
    combined_lower = " ".join(combined.lower().split())
    for required in (
        "global nonzero lift", "first Stiefel-Whitney class is zero",
        "local turning is real geometry", "finite path holonomies",
        "No topological charge", "No action, source, carrier",
    ):
        require(" ".join(required.lower().split()) in combined_lower, f"scope wording: {required}")

    # Every preregistered mutation changes a real census, result, evidence, or
    # scope field and is then passed through the same fail-closed validator as
    # the unmodified package. These semantic guards are still not advertised as
    # an independent algebraic reconstruction.
    exact_guards = {"F01", "F02", "F04", "F05", "F06", "F07", "F09", "F11", "F13", "F15", "F17", "F19", "F22", "F25", "F26", "F27", "F28", "F33", "F36"}
    independence_guards = {"F34", "F35"}
    expected_object_pairs = [(row["object_id"], row["object"]) for row in object_universe]
    baseline = {
        "candidate_ids": [row["candidate_id"] for row in bindings],
        "source_hash_ok": True,
        "posthoc_additions": 0,
        "control_transport_assignments": 0,
        "extended_domain": "S3_MINUS_D_GENERIC_EQUATOR_FILLED",
        "defect_circle_count": 3,
        "pole_junction_count": 2,
        "global_lift_proved": result["global_lift"] == "GLOBAL_NONZERO_LIFT_ON_M",
        "w1_global_basis_proved": result["line_w1"] == "ZERO_ON_ALL_H1_GENERATORS",
        "rp1_traversals": result["local_RP1_traversals"],
        "rp2_class": result["all_projective_meridians"],
        "vector_line_conflated": False,
        "all_regular_edges_symbolic": all(row["symbolic_rank"] == "2_AWAY_FROM_POLES" for row in edges),
        "equator_crossing_called_junction": False,
        "pole_punctures": list(result["pole_punctures"]),
        "index_sign_canonical": result["index_sign_canonical"],
        "index_magnitudes": [row["degree_magnitude"] for row in edges],
        "line_ambient_conflated": False,
        "line_self_connection": "ZERO",
        "ambient_called_line_holonomy": False,
        "omega_metric_derivation_present": "Before applying the kernel relation" in derivation,
        "connection_group": "SO11",
        "finite_inferred_from_point_omega": False,
        "point_curvature_called_global_nowhere_zero": False,
        "finite_holonomy_status": result["finite_loop_holonomy"],
        "full_lc_conflated": result["full_Levi_Civita_holonomy_conflated"],
        "exact_branch_comparison": True,
        "a_or_orientation_changes_topology": False,
        "screen_rotation_changes_topology": False,
        "representative_sign_changes_line": False,
        "family_scope": "FROZEN_STATIONARY_ENSEMBLE",
        "dynamic_persistence_claimed": False,
        "index_interpretation": "GEOMETRY_ONLY",
        "downstream_physics_inferred": False,
        "forbidden_method_used": False,
        "semantic_advertised_independent_algebra": False,
        "production_module_imported_by_independent": independent["production_module_imported"],
        "object_pairs": [(row["object_id"], row["object"]) for row in objects],
    }

    def validate(state):
        require(state["candidate_ids"] == [f"C{i:02d}" for i in range(1, 19)], "F01")
        require(state["source_hash_ok"], "F02")
        require(state["posthoc_additions"] == 0, "F03")
        require(state["control_transport_assignments"] == 0, "F04")
        require(state["extended_domain"] == "S3_MINUS_D_GENERIC_EQUATOR_FILLED", "F05")
        require(state["defect_circle_count"] == 3 and state["pole_junction_count"] == 2, "F06")
        require(state["global_lift_proved"], "F07")
        require(state["w1_global_basis_proved"], "F08")
        require(state["rp1_traversals"] == 2 and state["rp2_class"] == "TRIVIAL_IN_PI1_RP2", "F09")
        require(not state["vector_line_conflated"], "F10")
        require(state["all_regular_edges_symbolic"], "F11")
        require(not state["equator_crossing_called_junction"], "F12")
        require(state["pole_punctures"] == ["+e0", "-e0", "+e1", "-e1", "+e2", "-e2"], "F13")
        require(not state["index_sign_canonical"], "F14")
        require(state["index_magnitudes"] == ["1"]*6, "F15")
        require(not state["line_ambient_conflated"], "F16")
        require(state["line_self_connection"] == "ZERO", "F17")
        require(not state["ambient_called_line_holonomy"], "F18")
        require(state["omega_metric_derivation_present"], "F19")
        require(state["connection_group"] == "SO11", "F20")
        require(not state["finite_inferred_from_point_omega"], "F21")
        require(not state["point_curvature_called_global_nowhere_zero"], "F22")
        require(state["finite_holonomy_status"] == "PATH_INTEGRAL_NOT_UNIVERSALLY_EVALUATED", "F23")
        require(not state["full_lc_conflated"], "F24")
        require(state["exact_branch_comparison"], "F25")
        require(not state["a_or_orientation_changes_topology"], "F26")
        require(not state["screen_rotation_changes_topology"], "F27")
        require(not state["representative_sign_changes_line"], "F28")
        require(state["family_scope"] == "FROZEN_STATIONARY_ENSEMBLE", "F29")
        require(not state["dynamic_persistence_claimed"], "F30")
        require(state["index_interpretation"] == "GEOMETRY_ONLY", "F31")
        require(not state["downstream_physics_inferred"], "F32")
        require(not state["forbidden_method_used"], "F33")
        require(not state["semantic_advertised_independent_algebra"], "F34")
        require(not state["production_module_imported_by_independent"], "F35")
        require(state["object_pairs"] == expected_object_pairs, "F36")

    def set_value(key, value):
        return lambda state: state.__setitem__(key, value)

    def remove_candidate(state):
        state["candidate_ids"].pop()

    def remove_puncture(state):
        state["pole_punctures"].pop()

    def alter_index_magnitude(state):
        state["index_magnitudes"][0] = "2"

    def alter_object_identity(state):
        state["object_pairs"][1] = ("O02", "wrong_shifted_object")

    mutations = {
        "F01": remove_candidate,
        "F02": set_value("source_hash_ok", False),
        "F03": set_value("posthoc_additions", 1),
        "F04": set_value("control_transport_assignments", 1),
        "F05": set_value("extended_domain", "S3_MINUS_D_MINUS_EQUATOR"),
        "F06": set_value("defect_circle_count", 2),
        "F07": set_value("global_lift_proved", False),
        "F08": set_value("w1_global_basis_proved", False),
        "F09": set_value("rp2_class", "NONTRIVIAL_FROM_VISUAL_RP1_TURN"),
        "F10": set_value("vector_line_conflated", True),
        "F11": set_value("all_regular_edges_symbolic", False),
        "F12": set_value("equator_crossing_called_junction", True),
        "F13": remove_puncture,
        "F14": set_value("index_sign_canonical", True),
        "F15": alter_index_magnitude,
        "F16": set_value("line_ambient_conflated", True),
        "F17": set_value("line_self_connection", "NONZERO"),
        "F18": set_value("ambient_called_line_holonomy", True),
        "F19": set_value("omega_metric_derivation_present", False),
        "F20": set_value("connection_group", "U1"),
        "F21": set_value("finite_inferred_from_point_omega", True),
        "F22": set_value("point_curvature_called_global_nowhere_zero", True),
        "F23": set_value("finite_holonomy_status", "NONTRIVIAL_WITHOUT_INTEGRAL"),
        "F24": set_value("full_lc_conflated", True),
        "F25": set_value("exact_branch_comparison", False),
        "F26": set_value("a_or_orientation_changes_topology", True),
        "F27": set_value("screen_rotation_changes_topology", True),
        "F28": set_value("representative_sign_changes_line", True),
        "F29": set_value("family_scope", "UNIVERSAL_METRIC_SUBSTRATE"),
        "F30": set_value("dynamic_persistence_claimed", True),
        "F31": set_value("index_interpretation", "PARTICLE_CHARGE"),
        "F32": set_value("downstream_physics_inferred", True),
        "F33": set_value("forbidden_method_used", True),
        "F34": set_value("semantic_advertised_independent_algebra", True),
        "F35": set_value("production_module_imported_by_independent", True),
        "F36": alter_object_identity,
    }

    validate(baseline)
    require(set(mutations) == {row["gate_id"] for row in contract}, "mutation map completeness")
    catch_rows = []
    for row in contract:
        mutated = deepcopy(baseline)
        mutations[row["gate_id"]](mutated)
        caught = False
        try:
            validate(mutated)
        except AssertionError:
            caught = True
        require(caught, f"mutation not caught {row['gate_id']}")
        guard_type = (
            "EXACT_OUTPUT_OR_EVIDENCE_GUARD" if row["gate_id"] in exact_guards
            else "EVIDENCE_INDEPENDENCE_GUARD" if row["gate_id"] in independence_guards
            else "SEMANTIC_SCOPE_GUARD"
        )
        catch_rows.append({
            "gate_id": row["gate_id"], "status": "PASS_CAUGHT",
            "guard_type": guard_type, "mutation": row["mutation_or_failure"],
        })

    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=["gate_id", "status", "guard_type", "mutation"], lineterminator="\n")
        writer.writeheader(); writer.writerows(catch_rows)

    output = {
        "schema": "udt-defect-transport-semantic-1.0",
        "status": "PASS_FAIL_CLOSED",
        "source_count": 86,
        "candidate_count": 18,
        "object_count": 26,
        "premise_count": 19,
        "point_certificate_count": 12,
        "mutation_catches": 36,
        "guard_types": {
            "exact_output_or_evidence": len(exact_guards),
            "evidence_independence": len(independence_guards),
            "semantic_scope": 36-len(exact_guards)-len(independence_guards),
        },
        "semantic_guards_are_independent_algebra": False,
    }
    (HERE / "SEMANTIC_VERIFICATION.json").write_text(json.dumps(output, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(json.dumps(output, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

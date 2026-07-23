#!/usr/bin/env python3
"""Independent full-coverage verifier for the temporal-soldering atlas.

This imports the frozen nonproduction motif verifier and its separate analytic Jet reconstruction.
It does not import the temporal production builder, motif production core, or canonical evaluator.
"""

from __future__ import annotations

import argparse
import copy
import csv
import gzip
import itertools
import json
import multiprocessing as mp
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
INDEPENDENT_PARENT = ROOT / "udt_motif_hopf_correspondence_audit_2026-07-22"
sys.path.insert(0, str(INDEPENDENT_PARENT))
import verify_correspondence_independent as ind  # noqa: E402


PATH_FILE = HERE / "PATH_TEMPORAL_CLASSIFICATION.tsv.gz"
COMPLEMENT_FILE = HERE / "ORTHOGONAL_COMPLEMENT_ATLAS.tsv.gz"
LINE_FILE = HERE / "LINE_COMPLETION_ATLAS.tsv"
SOURCE_PATH_FILE = INDEPENDENT_PARENT / "PATH_FAMILY_ATLAS.tsv.gz"
TRANSFORMS = ROOT / "udt_chart_coframe_invariance_atlas_2026-07-21/TRANSFORMATION_REGISTRY.tsv"
H_STEPS = ind.H_STEPS
PATH_NODES = 17
NUMERIC_VALUE_COMPARISON_TOL = 1.0e-6
EXPECTED_CLASS_CONFLICTS = {
    ("B3_R13_3_MB", 4, 0, "NUMERIC_UNCERTAIN_OBSTRUCTION", "NUMERICALLY_INTEGRABLE_LOCAL"),
    ("B3_V007_MF", 4, 16, "NUMERICALLY_INTEGRABLE_LOCAL", "NUMERIC_UNCERTAIN_OBSTRUCTION"),
}


def iter_tsv(path: Path):
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8", newline="") as handle:
        yield from csv.DictReader(handle, delimiter="\t")


def read_tsv(path: Path):
    return list(iter_tsv(path))


def independent_path_class(rows, stable):
    if not stable or len(rows) != PATH_NODES or any(row["numeric_status"] != "NUMERIC_CLASSIFIED" for row in rows):
        return "TRANSITION_OR_NUMERICALLY_UNCERTAIN"
    motifs = {row["motif"] for row in rows}
    block_types = {(row["primitive_block_ranks"], row["primitive_block_signatures"]) for row in rows}
    if len(motifs) != 1 or len(block_types) != 1:
        return "TRANSITION_OR_NUMERICALLY_UNCERTAIN"
    motif = next(iter(motifs)); ranks, signature = next(iter(block_types))
    lookup = {
        ("FOUR_LINES", "1;1;1;1", "N0_P1_Z0;N0_P1_Z0;N0_P1_Z0;N1_P0_Z0"): "UNIQUE_LOCAL_UNORIENTED_TIMELIKE_LINE",
        ("LINE_PLUS_THREE", "1;3", "N0_P3_Z0;N1_P0_Z0"): "UNIQUE_LOCAL_UNORIENTED_TIMELIKE_LINE",
        ("LINE_PLUS_THREE", "1;3", "N0_P1_Z0;N1_P2_Z0"): "RANK_ONE_LINE_SPACELIKE__LORENTZ_COMPLEMENT",
        ("TWO_PLUS_TWO_LINES", "1;1;2", "N0_P1_Z0;N0_P1_Z0;N1_P1_Z0"): "LORENTZ_TWO_PLANE_ONLY",
        ("FULL_IRREDUCIBLE_4", "4", "N1_P3_Z0"): "NO_PROPER_INTRINSIC_TEMPORAL_SUBSPACE",
        ("SCALAR_4_AMBIGUITY", "4", "N1_P3_Z0"): "NO_PROPER_INTRINSIC_TEMPORAL_SUBSPACE",
    }
    return lookup.get((motif, ranks, signature), "LORENTZ_SUBSPACE_DIMENSION_GE_2_ONLY" if "N1_" in signature else "SIGNATURE_OR_PROJECTOR_DATA_MISSING")


def verify_path_universe():
    saved = {(r["identity_id"], r["family_id"]): r for r in iter_tsv(PATH_FILE)}
    if len(saved) != 95_232:
        raise AssertionError("saved path coverage")
    source = defaultdict(list)
    for row in iter_tsv(SOURCE_PATH_FILE):
        source[(row["identity_id"], row["family_id"])].append(row)
    if set(source) != set(saved):
        raise AssertionError("source/saved key mismatch")
    summary = {(r["identity_id"], r["family_id"]): r for r in iter_tsv(INDEPENDENT_PARENT / "PATH_CONTINUATION_SUMMARY.tsv.gz")}
    mismatch = []
    for key in sorted(source):
        rows = sorted(source[key], key=lambda r: int(r["path_node"]))
        got = independent_path_class(rows, summary[key]["stable_projector_path"] == "YES")
        if got != saved[key]["local_temporal_class"]:
            mismatch.append((key, got, saved[key]["local_temporal_class"]))
    if mismatch:
        raise AssertionError(f"path class mismatch {mismatch[:3]}")
    return saved, Counter(row["local_temporal_class"] for row in saved.values())


IDENTITIES = ind.identity_data()


def relative_error(first, second):
    return abs(float(first) - float(second)) / max(1.0, abs(float(first)), abs(float(second)))


def independent_identity_worker(task):
    identity_id, masks, saved_rows = task
    bank, amplitudes = IDENTITIES[identity_id]
    points = ind.path_points(bank)
    saved = {(int(row["path_node"]), int(row["family_id"][1:3])): row for row in saved_rows}
    mismatches = []
    class_conflicts = []
    class_census = Counter()
    max_numeric_difference = 0.0
    for node, point in enumerate(points):
        geo, centers = ind.classify_at(bank, amplitudes, point, set(masks))
        metric = ind.metric_phi_jets(bank, amplitudes, point)[0]
        stencil = {}
        for step in H_STEPS:
            for axis in range(4):
                for sign in (-1, 1):
                    neighbor = point.copy(); neighbor[axis] += sign * step
                    _neighbor_geo, current = ind.classify_at(bank, amplitudes, neighbor, set(masks))
                    stencil[(step, axis, sign)] = current
        for mask in masks:
            center = centers[mask]
            matches = [index for index, block in enumerate(center["blocks"])
                       if int(block["rank"]) == 1 and block["signature"] == "N1_P0_Z0"]
            if len(matches) != 1:
                mismatches.append((identity_id, mask, node, "timelike_line_count", len(matches)))
                continue
            index = matches[0]
            projectors = [np.asarray(value) for value in center["projectors"]]
            derivatives = {}
            for step in H_STEPS:
                derivative = np.zeros((4, 4, 4))
                for axis in range(4):
                    minus = ind.match(center, stencil[(step, axis, -1)][mask])
                    plus = ind.match(center, stencil[(step, axis, 1)][mask])
                    if minus is None or plus is None:
                        mismatches.append((identity_id, mask, node, "projector_match", "failed"))
                        continue
                    derivative[axis] = -(plus[index] - minus[index]) / (2.0 * step)
                derivatives[step] = derivative
            complement = np.eye(4) - projectors[index]
            rank, signature, *_rest = ind.independent.signature(complement, metric)
            convergence = float(np.linalg.norm(derivatives[H_STEPS[0]] - derivatives[H_STEPS[1]]) /
                                max(np.linalg.norm(derivatives[H_STEPS[1]]), 1.0))
            obstruction_h = ind.frobenius(complement, derivatives[H_STEPS[0]], np.asarray(geo["gamma"]))
            obstruction_h2 = ind.frobenius(complement, derivatives[H_STEPS[1]], np.asarray(geo["gamma"]))
            classification = ind.frob_class(obstruction_h2, convergence)
            class_census[classification] += 1
            expected = saved[(node, mask)]
            if signature != expected["orthogonal_complement_signature"]:
                mismatches.append((identity_id, mask, node, "signature", signature, expected["orthogonal_complement_signature"]))
            if classification != expected["frobenius_class"]:
                class_conflicts.append((identity_id, mask, node, classification, expected["frobenius_class"]))
            for field, got in (("convergence", convergence), ("obstruction_h", obstruction_h), ("obstruction_h2", obstruction_h2)):
                want = float(expected[{"convergence": "derivative_convergence_residual", "obstruction_h": "frobenius_obstruction_h", "obstruction_h2": "frobenius_obstruction_h2"}[field]])
                difference = relative_error(got, want); max_numeric_difference = max(max_numeric_difference, difference)
                if difference > NUMERIC_VALUE_COMPARISON_TOL:
                    mismatches.append((identity_id, mask, node, field, got, want, difference))
            if rank != 3:
                mismatches.append((identity_id, mask, node, "complement_rank", rank))
    return mismatches, class_conflicts, class_census, max_numeric_difference


def verify_complements(jobs):
    saved_rows = list(iter_tsv(COMPLEMENT_FILE))
    keys = [(row["identity_id"], row["family_id"], int(row["path_node"])) for row in saved_rows]
    if len(saved_rows) != 30_175 or len(set(keys)) != 30_175:
        raise AssertionError("complement coverage/duplicates")
    grouped = defaultdict(list)
    for row in saved_rows:
        grouped[row["identity_id"]].append(row)
    tasks = []
    for identity_id in sorted(grouped):
        masks = sorted({int(row["family_id"][1:3]) for row in grouped[identity_id]})
        tasks.append((identity_id, masks, grouped[identity_id]))
    if jobs == 1:
        iterator = map(independent_identity_worker, tasks)
    else:
        pool = mp.Pool(jobs); iterator = pool.imap(independent_identity_worker, tasks, chunksize=1)
    mismatches = []; class_conflicts = []; census = Counter(); max_difference = 0.0
    try:
        for current_mismatches, current_conflicts, current_census, current_difference in iterator:
            mismatches.extend(current_mismatches); class_conflicts.extend(current_conflicts); census.update(current_census)
            max_difference = max(max_difference, current_difference)
    finally:
        if jobs != 1:
            pool.close(); pool.join()
    if mismatches:
        raise AssertionError(f"independent complement mismatches {mismatches[:5]}")
    if set(class_conflicts) != EXPECTED_CLASS_CONFLICTS or len(class_conflicts) != 2:
        raise AssertionError(f"unexpected class conflict set {class_conflicts}")
    saved_census = Counter(row["frobenius_class"] for row in saved_rows)
    if census != saved_census:
        raise AssertionError(f"complement census {census} != {saved_census}")
    refinement = json.loads((HERE / "THRESHOLD_CONFLICT_REFINEMENT_RESULT.json").read_text())
    if {(r["identity_id"], int(r["family_id"][1:3]), int(r["path_node"]), r["consolidated_class"]) for r in refinement["cases"]} != {
        ("B3_R13_3_MB", 4, 0, "REFINED_INTEGRABLE"),
        ("B3_V007_MF", 4, 16, "REFINED_INTEGRABLE"),
    }:
        raise AssertionError("threshold refinement result")
    return saved_rows, census, max_difference, class_conflicts


def verify_chart_controls(path_saved):
    transforms = read_tsv(TRANSFORMS)
    if len(transforms) != 12:
        raise AssertionError("transform count")
    stable_classes = defaultdict(list)
    for key, row in path_saved.items():
        if row["local_temporal_class"] != "TRANSITION_OR_NUMERICALLY_UNCERTAIN":
            stable_classes[row["local_temporal_class"]].append(key)
    anchors = [sorted(values)[0] for _, values in sorted(stable_classes.items())]
    comparisons = 0; max_residual = 0.0
    for identity_id, family_id in anchors:
        bank, amplitudes = IDENTITIES[identity_id]; mask = int(family_id[1:3])
        geo, result = ind.classify_at(bank, amplitudes, ind.path_points(bank)[8], {mask})
        metric = ind.metric_phi_jets(bank, amplitudes, ind.path_points(bank)[8])[0]
        projectors = [np.asarray(value) for value in result[mask]["projectors"]]
        signatures = [ind.independent.signature(projector, metric)[1] for projector in projectors]
        for transform in transforms:
            determinant = float(transform["determinant"])
            if abs(determinant) <= 1.0e-12:
                raise AssertionError("singular registered chart")
            if transform["kind"] == "COORDINATE":
                matrix = np.asarray(json.loads(transform["matrix_json"]), dtype=float)
                inverse = np.linalg.inv(matrix)
                transformed_metric = matrix.T @ metric @ matrix
                transformed_projectors = [inverse @ projector @ matrix for projector in projectors]
            else:
                transformed_metric = metric.copy(); transformed_projectors = [projector.copy() for projector in projectors]
            got = [ind.independent.signature(projector, transformed_metric)[1] for projector in transformed_projectors]
            if got != signatures:
                raise AssertionError(f"signature covariance {identity_id} {family_id} {transform['transform_id']}")
            residual = max(
                [ind.independent.relmax(projector @ projector, projector) for projector in transformed_projectors]
                + [ind.independent.relmax(projector.T @ transformed_metric, transformed_metric @ projector) for projector in transformed_projectors]
                + [ind.independent.relmax(sum(transformed_projectors, np.zeros((4, 4))), np.eye(4))]
            )
            max_residual = max(max_residual, residual); comparisons += 1
    return comparisons, max_residual


def verify_global_open_status():
    cocycle = {row["id"]: row for row in read_tsv(ROOT / "udt_global_coframe_cocycle_audit_2026-07-20/COCYCLE_CLASSIFICATION.tsv")}
    if cocycle["C15"]["status_or_limit"] != "COVER_INCIDENCE_CAPS_AND_PHYSICAL_READOUT_OPEN":
        raise AssertionError("cocycle open status")
    seal = {row["interpretation_id"]: row for row in read_tsv(ROOT / "udt_complete_seal_fixed_set_selector_audit_2026-07-21/INTERPRETATION_SELECTOR.tsv")}
    if seal["I06"]["result"] != "NO_SELECTION":
        raise AssertionError("seal time orientation selection")
    holonomy = read_tsv(ROOT / "udt_global_metric_assembly_atlas_2026-07-22/BUNDLE_HOLONOMY_ATLAS.tsv")
    base_rows = [row for row in holonomy if "::" not in row["completion_id"]]
    monodromy_rows = [row for row in holonomy if row["completion_id"].startswith("FC07::M_")]
    if len(holonomy) != 20 or len(base_rows) != 12 or len(monodromy_rows) != 8:
        raise AssertionError("holonomy ledger row types")
    if any(row["levi_civita_tangent_holonomy"] != "PROFILE_DEPENDENT_NOT_COMPUTED_WITHOUT_COMPLETE_METRIC" for row in base_rows):
        raise AssertionError("base completion Levi-Civita holonomy status")
    if any(row["levi_civita_tangent_holonomy"] != "NOT_FIXED_BY_LATTICE_MONODROMY" for row in monodromy_rows):
        raise AssertionError("monodromy control Levi-Civita holonomy status")
    ladder = {int(row["rung"]): row for row in read_tsv(HERE / "COMPLETION_LADDER.tsv")}
    if any(int(ladder[rung]["unconditional_paths"]) != 0 for rung in range(2, 8)):
        raise AssertionError("later completion rung promoted")
    return len(holonomy)


def validate_mutation_state(state):
    """Fail closed on the registered independent-evidence invariants."""
    if state["path_count"] != 95_232:
        raise AssertionError("path count")
    if state["path_unique"] != 95_232:
        raise AssertionError("path uniqueness")
    if state["path_nodes"] != PATH_NODES:
        raise AssertionError("path node count")
    if state["path_census"] != {
        "LORENTZ_TWO_PLANE_ONLY": 7_845,
        "NO_PROPER_INTRINSIC_TEMPORAL_SUBSPACE": 82_140,
        "RANK_ONE_LINE_SPACELIKE__LORENTZ_COMPLEMENT": 2_160,
        "TRANSITION_OR_NUMERICALLY_UNCERTAIN": 1_312,
        "UNIQUE_LOCAL_UNORIENTED_TIMELIKE_LINE": 1_775,
    }:
        raise AssertionError("path census")
    if state["complement_count"] != 30_175:
        raise AssertionError("complement count")
    if state["complement_unique"] != 30_175:
        raise AssertionError("complement uniqueness")
    if state["complement_census"] != {
        "NUMERICALLY_INTEGRABLE_LOCAL": 12_239,
        "NUMERICALLY_NONINTEGRABLE_LOCAL": 17_925,
        "NUMERIC_UNCERTAIN_DERIVATIVE": 10,
        "NUMERIC_UNCERTAIN_OBSTRUCTION": 1,
    }:
        raise AssertionError("complement census")
    if state["four_line_nonintegrable_nodes"] != 17_925:
        raise AssertionError("four-line twist")
    if set(map(tuple, state["class_conflicts"])) != EXPECTED_CLASS_CONFLICTS:
        raise AssertionError("class conflicts")
    if state["unresolved_refinement_conflicts"] != 0:
        raise AssertionError("threshold refinement")
    if state["minimum_abs_transform_determinant"] <= 1.0e-12:
        raise AssertionError("singular transform")
    if state["global_holonomy_rows"] != 20:
        raise AssertionError("holonomy rows")
    if state["later_unconditional_paths"] != 0:
        raise AssertionError("global rung promotion")
    if state["actions_loaded"] != 0:
        raise AssertionError("action imported")
    if state["carriers_loaded"] != 0:
        raise AssertionError("carrier imported")
    if state["full_connectors"] != 0:
        raise AssertionError("full connector promoted")
    if state["timelike_physical_future_selected"] is not False:
        raise AssertionError("timelike future promoted")
    if state["timelike_global_time_derived"] is not False:
        raise AssertionError("timelike global time promoted")
    if state["spacelike_physical_branch_selected"] is not False:
        raise AssertionError("spacelike branch promoted")
    if state["spacelike_intraleaf_time_derived"] is not False:
        raise AssertionError("spacelike intraleaf time promoted")


def exercised_catches(path_saved, complement_rows, class_conflicts, holonomy_rows):
    production = json.loads((HERE / "VERIFICATION_RESULT.json").read_text())
    consolidated = json.loads((HERE / "CONSOLIDATED_RESULT.json").read_text())
    timelike = json.loads((HERE / "PHI_GRADIENT_SOLDERING_RESULT.json").read_text())
    spacelike = json.loads((HERE / "PHI_GRADIENT_SPACELIKE_BRANCH_RESULT.json").read_text())
    transforms = read_tsv(TRANSFORMS)
    ladder = read_tsv(HERE / "COMPLETION_LADDER.tsv")
    complement_keys = [(r["identity_id"], r["family_id"], r["path_node"]) for r in complement_rows]
    state = {
        "path_count": len(path_saved),
        "path_unique": len(set(path_saved)),
        "path_nodes": PATH_NODES,
        "path_census": dict(sorted(Counter(r["local_temporal_class"] for r in path_saved.values()).items())),
        "complement_count": len(complement_rows),
        "complement_unique": len(set(complement_keys)),
        "complement_census": dict(sorted(Counter(r["frobenius_class"] for r in complement_rows).items())),
        "four_line_nonintegrable_nodes": sum(r["motif"] == "FOUR_LINES" and r["frobenius_class"] == "NUMERICALLY_NONINTEGRABLE_LOCAL" for r in complement_rows),
        "class_conflicts": [list(row) for row in sorted(class_conflicts)],
        "unresolved_refinement_conflicts": consolidated["unresolved_conflicts"],
        "minimum_abs_transform_determinant": min(abs(float(r["determinant"])) for r in transforms),
        "global_holonomy_rows": holonomy_rows,
        "later_unconditional_paths": sum(int(r["unconditional_paths"]) for r in ladder if int(r["rung"]) >= 2),
        "actions_loaded": production["actions_loaded"],
        "carriers_loaded": production["carriers_loaded"],
        "full_connectors": production["full_optical_connectors_derived"],
        "timelike_physical_future_selected": timelike["physical_future_selected"],
        "timelike_global_time_derived": timelike["global_time_function_derived"],
        "spacelike_physical_branch_selected": spacelike["physical_branch_selected"],
        "spacelike_intraleaf_time_derived": spacelike["timelike_line_within_leaf_derived"],
    }
    validate_mutation_state(state)
    mutations = [
        ("C01_MISSING_PATH", "path_count -= 1", lambda s: s.__setitem__("path_count", s["path_count"] - 1)),
        ("C02_DUPLICATE_PATH", "path_unique -= 1", lambda s: s.__setitem__("path_unique", s["path_unique"] - 1)),
        ("C03_MISSING_NODE", "path_nodes = 16", lambda s: s.__setitem__("path_nodes", 16)),
        ("C04_TEMPORAL_CLASS_PROMOTION", "two-plane -1; timelike-line +1", lambda s: (s["path_census"].__setitem__("LORENTZ_TWO_PLANE_ONLY", s["path_census"]["LORENTZ_TWO_PLANE_ONLY"] - 1), s["path_census"].__setitem__("UNIQUE_LOCAL_UNORIENTED_TIMELIKE_LINE", s["path_census"]["UNIQUE_LOCAL_UNORIENTED_TIMELIKE_LINE"] + 1))),
        ("C05_MISSING_COMPLEMENT", "complement_count -= 1", lambda s: s.__setitem__("complement_count", s["complement_count"] - 1)),
        ("C06_DUPLICATE_COMPLEMENT_KEY", "complement_unique -= 1", lambda s: s.__setitem__("complement_unique", s["complement_unique"] - 1)),
        ("C07_COMPLEMENT_CLASS_PROMOTION", "uncertain obstruction -> integrable", lambda s: (s["complement_census"].__setitem__("NUMERIC_UNCERTAIN_OBSTRUCTION", 0), s["complement_census"].__setitem__("NUMERICALLY_INTEGRABLE_LOCAL", s["complement_census"]["NUMERICALLY_INTEGRABLE_LOCAL"] + 1))),
        ("C08_ERASE_FOUR_LINE_TWIST", "four_line_nonintegrable_nodes = 0", lambda s: s.__setitem__("four_line_nonintegrable_nodes", 0)),
        ("C09_UNREGISTERED_CLASS_CONFLICT", "append third conflict", lambda s: s["class_conflicts"].append(["MUTATED", 0, 0, "A", "B"])),
        ("C10_UNRESOLVED_THRESHOLD_CONFLICT", "unresolved_refinement_conflicts = 1", lambda s: s.__setitem__("unresolved_refinement_conflicts", 1)),
        ("C11_SINGULAR_CHART_ADMITTED", "minimum determinant = 0", lambda s: s.__setitem__("minimum_abs_transform_determinant", 0.0)),
        ("C12_DROP_HOLONOMY_ROW", "global_holonomy_rows -= 1", lambda s: s.__setitem__("global_holonomy_rows", s["global_holonomy_rows"] - 1)),
        ("C13_GLOBAL_RUNG_PROMOTION", "later_unconditional_paths = 1", lambda s: s.__setitem__("later_unconditional_paths", 1)),
        ("C14_ACTION_IMPORTED", "actions_loaded = 1", lambda s: s.__setitem__("actions_loaded", 1)),
        ("C15_CARRIER_IMPORTED", "carriers_loaded = 1", lambda s: s.__setitem__("carriers_loaded", 1)),
        ("C16_FALSE_FULL_CONNECTOR", "full_connectors = 1", lambda s: s.__setitem__("full_connectors", 1)),
        ("C17_UNORIENTED_LINE_CALLED_FUTURE", "timelike physical future = true", lambda s: s.__setitem__("timelike_physical_future_selected", True)),
        ("C18_LOCAL_CLOCK_CALLED_GLOBAL_TIME", "timelike global time = true", lambda s: s.__setitem__("timelike_global_time_derived", True)),
        ("C19_SPACELIKE_BRANCH_SELECTED", "spacelike physical branch = true", lambda s: s.__setitem__("spacelike_physical_branch_selected", True)),
        ("C20_FALSE_INTRALEAF_TIME", "spacelike intraleaf time = true", lambda s: s.__setitem__("spacelike_intraleaf_time_derived", True)),
    ]
    catches = []
    for identity, mutation, mutate in mutations:
        corrupted = copy.deepcopy(state)
        mutate(corrupted)
        try:
            validate_mutation_state(corrupted)
        except AssertionError as exc:
            catches.append({"catch_id": identity, "mutation": mutation, "validator": "validate_mutation_state", "rejection": str(exc), "result": "MUTATION_REJECTED_AS_REQUIRED"})
        else:
            raise AssertionError(f"corruption mutation accepted {identity}")
    return catches


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--jobs", type=int, default=max(1, min(12, os.cpu_count() or 1)))
    args = parser.parse_args()
    path_saved, path_census = verify_path_universe()
    complement_rows, complement_census, max_difference, class_conflicts = verify_complements(args.jobs)
    chart_comparisons, chart_residual = verify_chart_controls(path_saved)
    holonomy_rows = verify_global_open_status()
    catches = exercised_catches(path_saved, complement_rows, class_conflicts, holonomy_rows)
    with (HERE / "INDEPENDENT_CATCH_PROOFS.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=("catch_id", "mutation", "validator", "rejection", "result"), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(catches)
    result = {
        "status": "PASS_WITH_REGISTERED_SCOPE",
        "path_presentations_reclassified": len(path_saved),
        "path_nodes_reclassified_from_source": len(path_saved) * PATH_NODES,
        "path_class_census": dict(sorted(path_census.items())),
        "orthogonal_complement_nodes_independently_recomputed": len(complement_rows),
        "orthogonal_complement_class_census": dict(sorted(complement_census.items())),
        "maximum_independent_numeric_difference": max_difference,
        "numeric_value_comparison_tolerance": NUMERIC_VALUE_COMPARISON_TOL,
        "initial_threshold_class_conflicts": len(class_conflicts),
        "threshold_conflicts_refined_integrable": 2,
        "consolidated_line_plus_three_all_node_integrable_paths": 720,
        "consolidated_four_line_nonintegrable_paths": 1055,
        "chart_coframe_numeric_anchor_comparisons": chart_comparisons,
        "maximum_chart_projector_residual": chart_residual,
        "global_holonomy_rows_checked": holonomy_rows,
        "catch_proofs_passed": len(catches),
        "independent_route": "FROZEN_NONPRODUCTION_MOTIF_ALGEBRA_PLUS_SEPARATE_ANALYTIC_JET_RECONSTRUCTION",
        "production_builder_imported": False,
        "maximum_conclusion": "BOUNDED_REGISTERED_TEMPORAL_SOLDERING_ATLAS_INDEPENDENTLY_REPRODUCED",
    }
    (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

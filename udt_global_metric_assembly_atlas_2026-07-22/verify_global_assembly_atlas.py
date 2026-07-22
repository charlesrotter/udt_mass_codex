#!/usr/bin/env python3
"""Independent fail-closed verifier for the UDT global metric-assembly atlas."""

from __future__ import annotations

import csv
import gzip
import hashlib
import itertools
import json
import math
import sys
from collections import Counter, defaultdict
from copy import deepcopy
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PRIOR_DIR = ROOT / "udt_motif_hopf_correspondence_audit_2026-07-22"
sys.path.insert(0, str(PRIOR_DIR))

import build_correspondence_atlas as frozen  # noqa: E402
from motif_core import projector_set_distance  # noqa: E402


TRANSPORT_PASS = 2.0e-7
REFINEMENT_PASS = 5.0e-6
DERIVATIVE_STEP = 1.0e-5


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def rows(path: Path):
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def relmax(first, second):
    left = np.asarray(first, dtype=float)
    right = np.asarray(second, dtype=float)
    return float(np.max(np.abs(left - right)) / max(1.0, float(np.max(np.abs(left))), float(np.max(np.abs(right)))))


def require(condition: bool, message: str):
    if not condition:
        raise AssertionError(message)


def source_checks():
    lineage = rows(HERE / "SOURCE_LINEAGE.tsv")
    require(len(lineage) == 8, "source lineage count")
    for row in lineage:
        require(digest(ROOT / row["path"]) == row["sha256"], f"source hash {row['path']}")
    return lineage


def independent_candidate_set():
    grouped = defaultdict(list)
    for row in rows(PRIOR_DIR / "DISTRIBUTION_ATLAS.tsv.gz"):
        if row["motif"] == "TWO_PLUS_TWO_LINES" and row["distribution_kind"] == "COMPLEMENTARY_RANK2":
            grouped[(row["identity_id"], row["family_id"])].append(row["frobenius_class"])
    return {
        key for key, values in grouped.items()
        if len(values) == 2 and all(value == "NUMERICALLY_INTEGRABLE_LOCAL" for value in values)
    }


def path_and_anchor_checks():
    frozen_summary = rows(PRIOR_DIR / "PATH_CONTINUATION_SUMMARY.tsv.gz")
    census = rows(HERE / "PATH_ASSEMBLY_CENSUS.tsv.gz")
    require(len(frozen_summary) == 95_232 and len(census) == 95_232, "path count")
    frozen_keys = {(row["identity_id"], row["family_id"]) for row in frozen_summary}
    census_keys = {(row["identity_id"], row["family_id"]) for row in census}
    require(len(frozen_keys) == 95_232 and census_keys == frozen_keys, "path identity coverage")
    motif_census = Counter(row["distinct_motifs"] for row in frozen_summary if row["stable_projector_path"] == "YES")
    require(motif_census == Counter({
        "FULL_IRREDUCIBLE_4": 70_812,
        "SCALAR_4_AMBIGUITY": 11_328,
        "TWO_PLUS_TWO_LINES": 7_845,
        "LINE_PLUS_THREE": 2_880,
        "FOUR_LINES": 1_055,
    }), "stable motif census")
    strata = defaultdict(list)
    for row in frozen_summary:
        if row["stable_projector_path"] == "YES":
            strata[(row["distinct_motifs"], row["family_id"])].append((row["identity_id"], row["family_id"], row["distinct_motifs"]))
    expected = {
        min(values, key=lambda item: hashlib.sha256(f"{item[0]}\t{item[1]}".encode()).hexdigest())
        for values in strata.values()
    }
    transport = rows(HERE / "DENSE_TRANSPORT_ATLAS.tsv")
    observed = {(row["identity_id"], row["family_id"], row["motif"]) for row in transport}
    require(len(strata) == 83 and len(transport) == 83 and observed == expected, "dense anchor selection")
    statuses = Counter()
    for row in transport:
        values = [
            float(row["intertwining_residual_129"]),
            float(row["metric_isometry_residual_129"]),
            float(row["kato_metric_skew_residual_129"]),
            float(row["kato_commutator_residual_129"]),
        ]
        expected_status = (
            "DENSE_TRANSPORT_PASS"
            if max(values) <= TRANSPORT_PASS and float(row["refinement_65_129"]) <= REFINEMENT_PASS
            else "DENSE_TRANSPORT_NUMERIC_MARGIN_RETAINED"
        )
        require(row["transport_status"] == expected_status, "transport classification")
        require(row["error"] == "-", "transport execution error")
        statuses[expected_status] += 1
    return motif_census, statuses, transport


def candidate_follow_checks():
    expected = independent_candidate_set()
    require(len(expected) == 1_536, "independent candidate count")
    summaries = rows(HERE / "FINITE_CELL_DISTRIBUTION_SUMMARY.tsv")
    observed = {(row["identity_id"], row["family_id"]) for row in summaries}
    require(len(summaries) == 1_536 and observed == expected, "candidate set identity")
    follow = rows(HERE / "FINITE_CELL_DISTRIBUTION_FOLLOW.tsv.gz")
    require(len(follow) == 1_536 * 9, "candidate node count")
    node_map = defaultdict(set)
    for row in follow:
        node_map[(row["identity_id"], row["family_id"])].add(int(row["path_node"]))
        require(row["node_status"] == "BOTH_SIDES_SAMPLED_INTEGRABLE", "candidate node status")
    require(all(values == set(range(9)) for values in node_map.values()), "candidate node coverage")
    require(all(row["path_status"] == "SAMPLED_ALL_9_NODES_INTEGRABLE_CANDIDATE" for row in summaries), "candidate path status")
    require({identity.rsplit("_", 1)[-1] for identity, _family in observed} == {"M8"}, "candidate mask provenance")
    require(len({identity for identity, _family in observed}) == 192, "candidate unique identity count")
    provenance = rows(HERE / "CANDIDATE_PROVENANCE_CENSUS.tsv")
    require(len(provenance) == 8, "candidate provenance family rows")
    require(all(row["structural_mask"] == "M8" and row["selected_ensembles"] == "PHI_FIELD" for row in provenance), "candidate phi-only disclosure")
    return summaries, follow, provenance


def gcd_pair(text: str):
    a, b = (int(value) for value in text.strip("()").split(","))
    return a, b


def completion_and_holonomy_checks():
    completions = rows(HERE / "COMPLETION_CLASS_REGISTRY.tsv")
    require(len(completions) == 12 and len({row["completion_id"] for row in completions}) == 12, "completion registry")
    assembly = rows(HERE / "MOTIF_COMPLETION_ATLAS.tsv")
    require(len(assembly) == 7 * 12, "motif completion cross")
    require({int(row["frozen_stable_path_count"]) for row in assembly if row["motif"] == "TRANSITION_OR_UNCERTAIN"} == {1_312}, "transition count in cross")
    require(all(row["global_selection"] == "NOT_SELECTED_BY_LOCAL_MOTIF" for row in assembly), "local selection promotion")

    caps = rows(HERE / "CAP_PAIR_WITNESSES.tsv")
    require(len(caps) == 256, "cap witness count")
    cap_classes = Counter()
    for row in caps:
        first = gcd_pair(row["v_minus"])
        second = gcd_pair(row["v_plus"])
        require(math.gcd(abs(first[0]), abs(first[1])) == 1, "first cap primitive")
        require(math.gcd(abs(second[0]), abs(second[1])) == 1, "second cap primitive")
        signed = first[0] * second[1] - first[1] * second[0]
        require(int(row["signed_determinant"]) == signed, "cap determinant")
        require(int(row["p_abs_determinant"]) == abs(signed), "cap p")
        require(row["coverage_status"] == "BOUNDED_ARITHMETIC_WITNESS_NOT_INFINITE_FAMILY_EXHAUSTION", "cap exhaustiveness guard")
        cap_classes[row["topology_class"]] += 1
    require(cap_classes == Counter({"LENS_L_P_Q_CONVENTION": 182, "S3_DETERMINANT_ONE": 58, "P0_DEPENDENT_CYCLES": 16}), "cap class census")

    monodromies = rows(HERE / "TORUS_MONODROMY_REGISTRY.tsv")
    require(len(monodromies) == 8, "monodromy witnesses")
    for row in monodromies:
        matrix = np.asarray(json.loads(row["matrix"]), dtype=int)
        require(int(row["determinant"]) == int(round(np.linalg.det(matrix))), "monodromy determinant")
        require(abs(int(row["determinant"])) == 1, "monodromy GL2Z")
        require(int(row["trace"]) == int(np.trace(matrix)), "monodromy trace")

    holonomy = rows(HERE / "BUNDLE_HOLONOMY_ATLAS.tsv")
    require(len(holonomy) == 20, "holonomy row count")
    require(all(row["conflation_guard"] == "FOUR_NOTIONS_DISTINCT" for row in holonomy), "holonomy conflation guard")
    require(any(row["completion_id"] == "FC12_RECIPROCAL_TORIC_DIAGONAL" and "Q_FINITE" in row["principal_circle_characteristic_data"] for row in holonomy), "finite endpoint Q retained")
    return completions, assembly, caps, monodromies, holonomy


def selector_and_stage_checks(completions):
    selectors = rows(HERE / "SELECTOR_MATRIX.tsv")
    require(len(selectors) == 7 * len(completions), "selector matrix cross")
    require(all(row["selection_power"] == "NONSELECTING_IN_CURRENT_REGISTRY" for row in selectors), "selector power")
    require({row["selector_id"] for row in selectors} == {"RECIPROCITY", "CSN", "FINITE_CELL", "STATIC_SEAL", "BOOTSTRAP", "SCALE_MATTER_INVENTORY", "DENSITY_BOOTSTRAP"}, "selector identities")
    density = rows(HERE / "DENSITY_BOOTSTRAP_CIRCULARITY_LEDGER.tsv")
    require(len(density) == 5, "density routes")
    desired = next(row for row in density if row["route_id"] == "D03_NATIVE_SIMULTANEOUS_FIXED_POINT")
    require(desired["mass_status"] == "OPEN_NATIVE_OBJECT_REQUIRED", "density fixed point mass gate")
    require(desired["selection_authority"] == "POTENTIAL_FUTURE_EIGENVALUE_OR_BRANCH_SELECTOR", "density fixed point status")
    stages = rows(HERE / "STAGE_GATE_LEDGER.tsv")
    require(len(stages) == 7, "stage count")
    stage6 = next(row for row in stages if row["stage"].startswith("6_"))
    stage7 = next(row for row in stages if row["stage"].startswith("7_"))
    require(stage6["status"] == "NOT_ACTIVATED__GLOBAL_QUOTIENT_NOT_SELECTED", "stage 6 gate")
    require(stage7["status"] == "NOT_ACTIVATED__NATIVE_DYNAMICS_UNDEFINED", "stage 7 gate")
    result = json.loads((HERE / "ATLAS_RESULT.json").read_text(encoding="utf-8"))
    require(result["selected_global_quotient_classes"] == [], "selected quotient list")
    require(result["cpu_time_live_runs"] == 0 and result["gpu_runs"] == 0, "time/GPU gate")
    require(result["midpoint_integrable_unique_analytic_identities"] == 192, "result unique candidate identities")
    require(result["midpoint_integrable_structural_mask_census"] == {"M8": 1536}, "result mask census")
    return selectors, density, stages, result


def classify_independent(identity, family, point):
    analytic = frozen.volume.previous.regular_family(int(identity["bank"]), np.asarray(identity["amplitudes"], dtype=float), np.asarray(point, dtype=float))
    geometry = frozen.evaluate_metric_jets(analytic["metric_jets"])
    phi = analytic["phi"]
    objects = frozen.intrinsic_objects(geometry, np.asarray(phi.first), np.asarray(phi.second))
    scalar = {key: objects[key] for key in ("R", "H", "D")}
    result = frozen.classify_motif_family(
        frozen.family_operators(objects, tuple(family["keys"])), objects["gradient"], objects["metric"], scalar, tuple(family["keys"])
    )
    return geometry, result


def independent_generator(identity, family, t):
    start = np.asarray(identity["start_point"], dtype=float)
    end = np.asarray(identity["end_point"], dtype=float)
    tangent = end - start
    point = (1.0 - t) * start + t * end
    geometry, center = classify_independent(identity, family, point)
    projectors = [np.asarray(value, dtype=float) for value in center["projectors"]]
    eps = DERIVATIVE_STEP
    if t <= eps:
        sample_results = [classify_independent(identity, family, (1.0 - (t + offset)) * start + (t + offset) * end)[1] for offset in (eps, 2 * eps)]
        samples = [frozen.matched_projectors(center, result)[0] for result in sample_results]
        partials = [(-3 * projectors[index] + 4 * samples[0][index] - samples[1][index]) / (2 * eps) for index in range(len(projectors))]
    elif t >= 1.0 - eps:
        sample_results = [classify_independent(identity, family, (1.0 - (t - offset)) * start + (t - offset) * end)[1] for offset in (eps, 2 * eps)]
        samples = [frozen.matched_projectors(center, result)[0] for result in sample_results]
        partials = [(3 * projectors[index] - 4 * samples[0][index] + samples[1][index]) / (2 * eps) for index in range(len(projectors))]
    else:
        minus = classify_independent(identity, family, (1.0 - (t - eps)) * start + (t - eps) * end)[1]
        plus = classify_independent(identity, family, (1.0 - (t + eps)) * start + (t + eps) * end)[1]
        left = frozen.matched_projectors(center, minus)[0]
        right = frozen.matched_projectors(center, plus)[0]
        partials = [(right[index] - left[index]) / (2 * eps) for index in range(len(projectors))]
    gamma_t = np.einsum("r,mrn->mn", tangent, np.asarray(geometry.christoffel, dtype=float))
    covariant = [partial + gamma_t @ projector - projector @ gamma_t for partial, projector in zip(partials, projectors)]
    kato = sum((derivative @ projector for derivative, projector in zip(covariant, projectors)), np.zeros((4, 4)))
    return kato - gamma_t, np.asarray(geometry.metric, dtype=float), projectors


def independent_transport_anchors(transport_rows):
    identity_map = {row["identity_id"]: row for row in frozen.identities()}
    family_map = {row["family_id"]: row for row in frozen.FAMILIES}
    selected = []
    for motif in ("FOUR_LINES", "LINE_PLUS_THREE", "TWO_PLUS_TWO_LINES"):
        candidates = [row for row in transport_rows if row["motif"] == motif]
        selected.append(min(candidates, key=lambda row: row["selection_sha256"]))
    results = []
    for row in selected:
        identity = identity_map[row["identity_id"]]
        family = family_map[row["family_id"]]

        def rhs(t, flat):
            generator = independent_generator(identity, family, float(t))[0]
            return (generator @ flat.reshape(4, 4)).reshape(-1)

        solution = solve_ivp(rhs, (0.0, 1.0), np.eye(4).reshape(-1), method="DOP853", rtol=2e-9, atol=2e-11)
        require(solution.success, "independent transport integrator")
        matrix = solution.y[:, -1].reshape(4, 4)
        _m0, metric0, projectors0 = independent_generator(identity, family, 0.0)
        _m1, metric1, projectors1 = independent_generator(identity, family, 1.0)
        inverse = np.linalg.inv(matrix)
        transported = [matrix @ projector @ inverse for projector in projectors0]
        intertwining = projector_set_distance(transported, projectors1)
        isometry = relmax(matrix.T @ metric1 @ matrix, metric0)
        require(intertwining <= 2e-5 and isometry <= 2e-5, "independent transport endpoint")
        results.append({
            "identity_id": row["identity_id"],
            "family_id": row["family_id"],
            "motif": row["motif"],
            "method": "SCIPY_DOP853_INDEPENDENT_ORCHESTRATION",
            "function_evaluations": int(solution.nfev),
            "intertwining_residual": intertwining,
            "metric_isometry_residual": isometry,
        })
    require(Counter(item["motif"] for item in results) == Counter({
        "FOUR_LINES": 1,
        "LINE_PLUS_THREE": 1,
        "TWO_PLUS_TWO_LINES": 1,
    }), "independent anchor motif labels")
    return results


def exact_connection_control():
    eta = np.diag([-1.0, 1.0, 1.0, 1.0])
    generator = np.asarray([
        [0.0, 0.37, 0.0, 0.0],
        [0.37, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, -0.23],
        [0.0, 0.0, 0.23, 0.0],
    ])
    require(relmax(generator.T @ eta + eta @ generator, np.zeros((4, 4))) <= 1e-15, "independent metric-skew generator")
    # At s=0, rank-one coordinate projectors give sum [A,P_i]P_i=A when A has zero diagonal.
    projectors = []
    for index in range(4):
        value = np.zeros((4, 4))
        value[index, index] = 1.0
        projectors.append(value)
    derivatives = [generator @ value - value @ generator for value in projectors]
    kato = sum((derivative @ projector for derivative, projector in zip(derivatives, projectors)), np.zeros((4, 4)))
    require(relmax(kato, generator) <= 1e-15, "independent Kato reconstruction")
    require(max(relmax(kato @ p - p @ kato, d) for p, d in zip(projectors, derivatives)) <= 1e-15, "independent commutator identity")
    return {"metric_skew_residual": relmax(kato.T @ eta + eta @ kato, np.zeros((4, 4))), "kato_generator_residual": relmax(kato, generator)}


def run_catches(path_census, transport, summaries, follow, provenance, completions, assembly, caps, holonomy, selectors, density, stages):
    catches = []

    def exercise(catch_id, description, mutator, validator):
        mutated = mutator()
        caught = False
        try:
            validator(mutated)
        except AssertionError:
            caught = True
        require(caught, f"catch did not fire {catch_id}")
        catches.append({"catch_id": catch_id, "mutation": description, "result": "PASS_MUTATION_REJECTED"})

    exercise("C01", "remove one path", lambda: path_census[:-1], lambda value: require(len(value) == 95_232, "missing path"))
    exercise("C02", "duplicate one path identity", lambda: path_census + [path_census[0]], lambda value: require(len({(r['identity_id'],r['family_id']) for r in value}) == len(value), "duplicate path"))
    exercise("C03", "remove one dense stratum anchor", lambda: transport[:-1], lambda value: require(len(value) == 83, "missing anchor"))
    exercise("C04", "promote a numeric-margin transport row", lambda: [{**r, "transport_status": "DENSE_TRANSPORT_PASS"} if r["transport_status"].endswith("RETAINED") else r for r in transport], lambda value: require(all(not (r["transport_status"] == "DENSE_TRANSPORT_PASS" and max(float(r[k]) for k in ("intertwining_residual_129","metric_isometry_residual_129","kato_metric_skew_residual_129","kato_commutator_residual_129")) > TRANSPORT_PASS) for r in value), "margin promotion"))
    exercise("C05", "remove one 1536-set identity", lambda: summaries[:-1], lambda value: require(len(value) == 1_536, "candidate missing"))
    exercise("C06", "drop one candidate path node", lambda: follow[:-1], lambda value: require(len(value) == 1_536 * 9, "node missing"))
    exercise("C07", "promote midpoint-only evidence to all-node", lambda: [{**summaries[0], "nodes_recorded": "1"}] + summaries[1:], lambda value: require(all(int(r["nodes_recorded"]) == 9 for r in value), "midpoint promotion"))
    exercise("C08", "erase phi-only candidate provenance", lambda: [{**r, "selected_ensembles": "FULL_ORCHESTRA"} for r in provenance], lambda value: require(all(r["selected_ensembles"] == "PHI_FIELD" for r in value), "provenance loss"))
    exercise("C09", "claim bounded cap witnesses exhaust the family", lambda: [{**r, "coverage_status": "EXHAUSTIVE"} for r in caps], lambda value: require(all("NOT_INFINITE_FAMILY_EXHAUSTION" in r["coverage_status"] for r in value), "false exhaustion"))
    exercise("C10", "call open interval transport closed holonomy", lambda: [{**r, "projector_kato_transport": "CLOSED_HOLONOMY"} if r["completion_id"] == "FC01_BOUNDARY_BOUNDARY" else r for r in holonomy], lambda value: require(all(r["projector_kato_transport"] != "CLOSED_HOLONOMY" for r in value), "open holonomy"))
    exercise("C11", "conflate holonomy notions", lambda: [{**r, "conflation_guard": "MERGED"} for r in holonomy], lambda value: require(all(r["conflation_guard"] == "FOUR_NOTIONS_DISTINCT" for r in value), "holonomy conflation"))
    exercise("C12", "select a local motif completion", lambda: [{**r, "global_selection": "SELECTED"} if r is assembly[0] else r for r in assembly], lambda value: require(all(r["global_selection"] == "NOT_SELECTED_BY_LOCAL_MOTIF" for r in value), "local selection"))
    exercise("C13", "grant one selector unique power", lambda: [{**r, "selection_power": "SELECTS"} if r is selectors[0] else r for r in selectors], lambda value: require(all(r["selection_power"] == "NONSELECTING_IN_CURRENT_REGISTRY" for r in value), "selector promotion"))
    exercise("C14", "activate deformation before quotient selection", lambda: [{**r, "status": "ACTIVATED"} if r["stage"].startswith("6_") else r for r in stages], lambda value: require(next(r for r in value if r["stage"].startswith("6_"))["status"].startswith("NOT_ACTIVATED"), "stage6"))
    exercise("C15", "activate time-live before native dynamics", lambda: [{**r, "status": "ACTIVATED"} if r["stage"].startswith("7_") else r for r in stages], lambda value: require(next(r for r in value if r["stage"].startswith("7_"))["status"].startswith("NOT_ACTIVATED"), "stage7"))
    exercise("C16", "promote supplied density to native selector", lambda: [{**r, "selection_authority": "NATIVE_SELECTOR"} if r["route_id"] == "D01_OBSERVED_DENSITY_INPUT" else r for r in density], lambda value: require(next(r for r in value if r["route_id"] == "D01_OBSERVED_DENSITY_INPUT")["selection_authority"] == "COMPARISON_OR_CALIBRATION_ONLY", "density input promotion"))
    exercise("C17", "mark native fixed point closed without mass", lambda: [{**r, "mass_status": "DERIVED"} if r["route_id"] == "D03_NATIVE_SIMULTANEOUS_FIXED_POINT" else r for r in density], lambda value: require(next(r for r in value if r["route_id"] == "D03_NATIVE_SIMULTANEOUS_FIXED_POINT")["mass_status"] == "OPEN_NATIVE_OBJECT_REQUIRED", "mass chicken egg"))
    exercise("C18", "filter singular completion from registry", lambda: [r for r in completions if r["completion_id"] != "FC06_NONPRIMITIVE_CAP"], lambda value: require(len(value) == 12, "merit filtering"))
    return catches


def main():
    lineage = source_checks()
    motif_census, transport_census, transport = path_and_anchor_checks()
    summaries, follow, provenance = candidate_follow_checks()
    completions, assembly, caps, monodromies, holonomy = completion_and_holonomy_checks()
    selectors, density, stages, result = selector_and_stage_checks(completions)
    independent_exact = exact_connection_control()
    independent_anchors = independent_transport_anchors(transport)
    path_census = rows(HERE / "PATH_ASSEMBLY_CENSUS.tsv.gz")
    catches = run_catches(path_census, transport, summaries, follow, provenance, completions, assembly, caps, holonomy, selectors, density, stages)
    with (HERE / "CATCH_PROOFS.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(catches[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(catches)
    verification = {
        "schema": "udt-global-metric-assembly-verification-1.0",
        "status": "PASS_WITH_REGISTERED_NUMERIC_MARGINS",
        "source_hashes": "PASS",
        "path_identities": len(path_census),
        "stable_motif_census": dict(sorted(motif_census.items())),
        "dense_transport_status_census": dict(sorted(transport_census.items())),
        "independent_transport_anchors": independent_anchors,
        "independent_exact_connection_control": independent_exact,
        "candidate_paths": len(summaries),
        "candidate_nodes": len(follow),
        "candidate_unique_analytic_identities": len({row["identity_id"] for row in summaries}),
        "candidate_structural_masks": sorted({row["identity_id"].rsplit("_", 1)[-1] for row in summaries}),
        "completion_classes": len(completions),
        "cap_witnesses": len(caps),
        "monodromy_witnesses": len(monodromies),
        "selector_rows": len(selectors),
        "density_bootstrap_routes": len(density),
        "catch_proofs": len(catches),
        "stage_6_status": next(row["status"] for row in stages if row["stage"].startswith("6_")),
        "stage_7_status": next(row["status"] for row in stages if row["stage"].startswith("7_")),
        "maximum_conclusion": result["maximum_conclusion"],
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(verification, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(verification, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Preregistered two-node cross-implementation Frobenius refinement."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "udt_motif_hopf_correspondence_audit_2026-07-22"))
import build_temporal_soldering_atlas as production  # noqa: E402
import verify_correspondence_independent as independent  # noqa: E402


STEPS = (1.0e-4, 5.0e-5, 2.5e-5, 1.25e-5)
CASES = (
    ("B3_R13_3_MB", "M04_D", 0),
    ("B3_V007_MF", "M04_D", 16),
)
DERIVATIVE_GATE = 5.0e-3
INTEGRABLE_GATE = 1.0e-7
NONINTEGRABLE_GATE = 1.0e-5


def production_route(identity_id, family_id, node):
    identity = production.IDENTITY_BY_ID[identity_id]
    family = production.FAMILY_BY_ID[family_id]
    start = np.asarray(identity["start_point"]); end = np.asarray(identity["end_point"])
    point = (1.0 - node / 16.0) * start + (node / 16.0) * end
    geometry, centers = production.classify_selected(identity, [family], point)
    center = centers[family_id]; index = production.line_index(center)
    projectors = [np.asarray(value) for value in center["projectors"]]
    complement = np.eye(4) - projectors[index]
    derivatives = {}
    for step in STEPS:
        derivative = np.zeros((4, 4, 4))
        for axis in range(4):
            values = []
            for sign in (-1, 1):
                neighbor = point.copy(); neighbor[axis] += sign * step
                _geo, result = production.classify_selected(identity, [family], neighbor)
                matched, _permutation, _distance = production.prior.matched_projectors(center, result[family_id])
                if matched is None:
                    raise AssertionError("production projector match")
                values.append(matched[index])
            derivative[axis] = -(values[1] - values[0]) / (2.0 * step)
        derivatives[step] = derivative
    return complement, np.asarray(geometry.christoffel), derivatives, "PRODUCTION_CANONICAL_EVALUATOR"


def independent_route(identity_id, family_id, node):
    bank, amplitudes = independent.identity_data()[identity_id]
    mask = int(family_id[1:3]); point = independent.path_points(bank)[node]
    geo, centers = independent.classify_at(bank, amplitudes, point, {mask})
    center = centers[mask]
    matches = [index for index, block in enumerate(center["blocks"])
               if int(block["rank"]) == 1 and block["signature"] == "N1_P0_Z0"]
    if len(matches) != 1:
        raise AssertionError("independent timelike line")
    index = matches[0]; projectors = [np.asarray(value) for value in center["projectors"]]
    complement = np.eye(4) - projectors[index]
    derivatives = {}
    for step in STEPS:
        derivative = np.zeros((4, 4, 4))
        for axis in range(4):
            values = []
            for sign in (-1, 1):
                neighbor = point.copy(); neighbor[axis] += sign * step
                _neighbor_geo, result = independent.classify_at(bank, amplitudes, neighbor, {mask})
                matched = independent.match(center, result[mask])
                if matched is None:
                    raise AssertionError("independent projector match")
                values.append(matched[index])
            derivative[axis] = -(values[1] - values[0]) / (2.0 * step)
        derivatives[step] = derivative
    return complement, np.asarray(geo["gamma"]), derivatives, "INDEPENDENT_ANALYTIC_JET"


def route_rows(identity_id, family_id, node, route_function):
    projector, gamma, derivatives, route = route_function(identity_id, family_id, node)
    obstructions = {step: independent.frobenius(projector, derivatives[step], gamma) for step in STEPS}
    rows = []
    for index, step in enumerate(STEPS):
        if index + 1 < len(STEPS):
            next_step = STEPS[index + 1]
            convergence = float(np.linalg.norm(derivatives[step] - derivatives[next_step]) /
                                max(np.linalg.norm(derivatives[next_step]), 1.0))
        else:
            convergence = float("nan")
        rows.append({
            "identity_id": identity_id, "family_id": family_id, "path_node": node, "route": route,
            "h": f"{step:.17g}", "frobenius_obstruction": f"{obstructions[step]:.17g}",
            "derivative_convergence_to_next_h": f"{convergence:.17g}",
        })
    return rows, obstructions, derivatives


def classify_case(route_payloads):
    all_last = []; all_convergence = []
    for _rows, obstruction, derivatives in route_payloads:
        all_last.extend((obstruction[STEPS[-2]], obstruction[STEPS[-1]]))
        all_convergence.append(float(np.linalg.norm(derivatives[STEPS[-2]] - derivatives[STEPS[-1]]) /
                                     max(np.linalg.norm(derivatives[STEPS[-1]]), 1.0)))
    if max(all_convergence) <= DERIVATIVE_GATE and all(value <= INTEGRABLE_GATE for value in all_last):
        return "REFINED_INTEGRABLE"
    if max(all_convergence) <= DERIVATIVE_GATE and all(value >= NONINTEGRABLE_GATE for value in all_last):
        return "REFINED_NONINTEGRABLE"
    return "CROSS_IMPLEMENTATION_NUMERIC_UNCERTAIN_OBSTRUCTION"


def main():
    rows = []; results = []
    for identity_id, family_id, node in CASES:
        payloads = [
            route_rows(identity_id, family_id, node, production_route),
            route_rows(identity_id, family_id, node, independent_route),
        ]
        for current_rows, _obstructions, _derivatives in payloads:
            rows.extend(current_rows)
        results.append({
            "identity_id": identity_id, "family_id": family_id, "path_node": node,
            "consolidated_class": classify_case(payloads),
        })
    with (HERE / "THRESHOLD_CONFLICT_REFINEMENT.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=(
            "identity_id", "family_id", "path_node", "route", "h", "frobenius_obstruction",
            "derivative_convergence_to_next_h",
        ), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)
    result = {
        "cases": results,
        "steps": list(STEPS),
        "derivative_gate": DERIVATIVE_GATE,
        "integrable_gate": INTEGRABLE_GATE,
        "nonintegrable_gate": NONINTEGRABLE_GATE,
        "candidate_rows": len(CASES),
        "routes": 2,
        "retuning_outside_frozen_candidates": 0,
    }
    (HERE / "THRESHOLD_CONFLICT_REFINEMENT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

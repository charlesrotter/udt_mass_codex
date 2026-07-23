#!/usr/bin/env python3
"""Verify the preregistered exact phi-gradient local soldering join."""

from __future__ import annotations

import csv
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


TOL = 1.0e-9
IDENTITIES = ind.identity_data()
FAMILY_KEYS = {family_id: keys for family_id, _mask, keys in ind.FAMILIES}


def rows(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def worker(task):
    identity_id, family_ids = task
    bank, amplitudes = IDENTITIES[identity_id]
    output = []
    for node, point in enumerate(ind.path_points(bank)):
        g, dg, ddg, dphi, ddphi = ind.metric_phi_jets(bank, amplitudes, point)
        objects, _geo = ind.independent.objects(g, dg, ddg, dphi, ddphi)
        inverse = np.linalg.inv(g); gradient = inverse @ dphi
        s = float(dphi @ gradient); dyad = np.outer(gradient, dphi)
        if not s < 0.0:
            raise AssertionError(f"non-timelike phi gradient {identity_id} node {node}: {s}")
        p_phi = dyad / s; q_phi = np.eye(4) - p_phi
        q_rank, q_signature, *_ = ind.independent.signature(q_phi, g)
        for family_id in family_ids:
            mask = int(family_id[1:3]); keys = FAMILY_KEYS[family_id]
            result = ind.independent.classify(
                ind.independent.operators(objects, keys), objects["gradient"], g,
                {key: objects[key] for key in ("R", "H", "D")}, keys,
            )
            matches = [index for index, block in enumerate(result["blocks"])
                       if int(block["rank"]) == 1 and block["signature"] == "N1_P0_Z0"]
            if len(matches) != 1:
                raise AssertionError(f"line count {identity_id} {family_id} {node}")
            projector = np.asarray(result["projectors"][matches[0]])
            residuals = {
                "dyad_minimal_polynomial": ind.independent.relmax(dyad @ dyad, s * dyad),
                "projector_idempotence": ind.independent.relmax(p_phi @ p_phi, p_phi),
                "metric_self_adjoint": ind.independent.relmax(p_phi.T @ g, g @ p_phi),
                "gradient_annihilation": ind.independent.relmax(q_phi @ gradient, np.zeros(4)),
                "covector_annihilation": ind.independent.relmax(dphi @ q_phi, np.zeros(4)),
                "projector_join": ind.independent.relmax(projector, p_phi),
            }
            if max(residuals.values()) > TOL or q_rank != 3 or q_signature != "N0_P3_Z0":
                raise AssertionError(f"phi join {identity_id} {family_id} {node} {residuals} {q_rank} {q_signature}")
            output.append({
                "identity_id": identity_id, "family_id": family_id, "path_node": node,
                "s": s, "lapse_phi": 1.0 / np.sqrt(-s), "q_signature": q_signature,
                **residuals,
            })
    return output


def main():
    line_rows = [row for row in rows(HERE / "CROSS_IMPLEMENTATION_LINE_COMPLETION.tsv")
                 if row["motif"] == "LINE_PLUS_THREE"]
    if len(line_rows) != 720 or any("D" not in FAMILY_KEYS[row["family_id"]] for row in line_rows):
        raise AssertionError("frozen D-family candidate set")
    grouped = defaultdict(list)
    for row in line_rows:
        grouped[row["identity_id"]].append(row["family_id"])
    tasks = [(identity_id, sorted(families)) for identity_id, families in sorted(grouped.items())]
    jobs = max(1, min(12, os.cpu_count() or 1)); all_rows = []
    with mp.Pool(jobs) as pool:
        for current in pool.imap(worker, tasks, chunksize=1):
            all_rows.extend(current)
    all_rows.sort(key=lambda r: (r["identity_id"], r["family_id"], r["path_node"]))
    if len(all_rows) != 12_240:
        raise AssertionError("node coverage")
    residual_fields = (
        "dyad_minimal_polynomial", "projector_idempotence", "metric_self_adjoint",
        "gradient_annihilation", "covector_annihilation", "projector_join",
    )
    family_census = Counter(row["family_id"] for row in line_rows)
    result = {
        "status": "PASS_WITH_REGISTERED_SCOPE",
        "path_presentations": len(line_rows),
        "unique_analytic_identities": len(grouped),
        "node_presentations": len(all_rows),
        "all_families_contain_D": True,
        "all_nodes_s_negative": True,
        "s_closest_to_zero": max(row["s"] for row in all_rows),
        "s_most_negative": min(row["s"] for row in all_rows),
        "lapse_phi_min": min(row["lapse_phi"] for row in all_rows),
        "lapse_phi_max": max(row["lapse_phi"] for row in all_rows),
        "max_residuals": {field: max(row[field] for row in all_rows) for field in residual_fields},
        "family_presentation_census": dict(sorted(family_census.items())),
        "exact_local_theorem": {
            "dyad": "D=grad(phi) tensor dphi",
            "minimal_polynomial": "D^2=sD",
            "timelike_projector": "P_phi=D/s for s=g_inverse(dphi,dphi)<0",
            "spatial_projector": "Q_phi=I-P_phi projects onto ker(dphi)",
            "frobenius": "ker(dphi) integrable because d(dphi)=0",
            "adapted_lapse": "N_phi=1/sqrt(-s) for tau=phi",
            "adapted_shift": "zero only for the chosen normal-flow congruence",
        },
        "physical_future_selected": False,
        "continuous_sign_between_17_nodes_certified": False,
        "global_time_function_derived": False,
        "physical_clock_scale_derived": False,
        "maximum_conclusion": "EXACT_LOCAL_CONDITIONAL_PHI_GRADIENT_SOLDERING_THEOREM_ON_TIMELIKE_DPHI_BRANCH",
    }
    (HERE / "PHI_GRADIENT_SOLDERING_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

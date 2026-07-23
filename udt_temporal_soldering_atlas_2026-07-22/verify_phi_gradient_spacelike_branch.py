#!/usr/bin/env python3
"""Verify the preregistered exact spacelike phi-gradient branch."""

from __future__ import annotations

import csv
import gzip
import json
import multiprocessing as mp
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "udt_motif_hopf_correspondence_audit_2026-07-22"))
import verify_correspondence_independent as ind  # noqa: E402


TOL = 1.0e-9
IDENTITIES = ind.identity_data()
FAMILY_KEYS = {family_id: keys for family_id, _mask, keys in ind.FAMILIES}


def path_rows():
    with gzip.open(HERE / "PATH_TEMPORAL_CLASSIFICATION.tsv.gz", "rt", encoding="utf-8", newline="") as handle:
        return [row for row in csv.DictReader(handle, delimiter="\t")
                if row["local_temporal_class"] == "RANK_ONE_LINE_SPACELIKE__LORENTZ_COMPLEMENT"]


def worker(task):
    identity_id, family_ids = task; bank, amplitudes = IDENTITIES[identity_id]; output = []
    for node, point in enumerate(ind.path_points(bank)):
        g, dg, ddg, dphi, ddphi = ind.metric_phi_jets(bank, amplitudes, point)
        objects, _geo = ind.independent.objects(g, dg, ddg, dphi, ddphi)
        gradient = np.linalg.inv(g) @ dphi; s = float(dphi @ gradient); dyad = np.outer(gradient, dphi)
        if not s > 0.0:
            raise AssertionError(f"non-spacelike phi gradient {identity_id} {node}: {s}")
        p_phi = dyad / s; q_phi = np.eye(4) - p_phi
        q_rank, q_signature, *_ = ind.independent.signature(q_phi, g)
        for family_id in family_ids:
            keys = FAMILY_KEYS[family_id]
            result = ind.independent.classify(
                ind.independent.operators(objects, keys), objects["gradient"], g,
                {key: objects[key] for key in ("R", "H", "D")}, keys,
            )
            matches = [index for index, block in enumerate(result["blocks"])
                       if int(block["rank"]) == 1 and block["signature"] == "N0_P1_Z0"]
            if len(matches) != 1:
                raise AssertionError(f"spacelike line count {identity_id} {family_id} {node}")
            projector = np.asarray(result["projectors"][matches[0]])
            residuals = {
                "dyad_minimal_polynomial": ind.independent.relmax(dyad @ dyad, s * dyad),
                "projector_idempotence": ind.independent.relmax(p_phi @ p_phi, p_phi),
                "metric_self_adjoint": ind.independent.relmax(p_phi.T @ g, g @ p_phi),
                "gradient_annihilation": ind.independent.relmax(q_phi @ gradient, np.zeros(4)),
                "covector_annihilation": ind.independent.relmax(dphi @ q_phi, np.zeros(4)),
                "projector_join": ind.independent.relmax(projector, p_phi),
            }
            if max(residuals.values()) > TOL or q_rank != 3 or q_signature != "N1_P2_Z0":
                raise AssertionError(f"spacelike phi join {identity_id} {family_id} {node} {residuals} {q_rank} {q_signature}")
            output.append({"s": s, **residuals})
    return output


def main():
    candidates = path_rows()
    if len(candidates) != 2_160 or any("D" not in FAMILY_KEYS[row["family_id"]] for row in candidates):
        raise AssertionError("frozen spacelike D-family candidate set")
    grouped = defaultdict(list)
    for row in candidates:
        grouped[row["identity_id"]].append(row["family_id"])
    tasks = [(identity_id, sorted(families)) for identity_id, families in sorted(grouped.items())]
    all_rows = []
    with mp.Pool(max(1, min(12, os.cpu_count() or 1))) as pool:
        for current in pool.imap(worker, tasks, chunksize=1): all_rows.extend(current)
    if len(all_rows) != 36_720:
        raise AssertionError("spacelike node coverage")
    residual_fields = (
        "dyad_minimal_polynomial", "projector_idempotence", "metric_self_adjoint",
        "gradient_annihilation", "covector_annihilation", "projector_join",
    )
    result = {
        "status": "PASS_WITH_REGISTERED_SCOPE",
        "path_presentations": len(candidates), "unique_analytic_identities": len(grouped),
        "node_presentations": len(all_rows), "all_families_contain_D": True,
        "all_nodes_s_positive": True, "s_closest_to_zero": min(row["s"] for row in all_rows),
        "s_largest": max(row["s"] for row in all_rows),
        "max_residuals": {field: max(row[field] for row in all_rows) for field in residual_fields},
        "family_presentation_census": dict(sorted(Counter(row["family_id"] for row in candidates).items())),
        "exact_local_theorem": {
            "spatial_projector": "P_phi=D/s for s>0",
            "lorentzian_leaf_projector": "Q_phi=I-P_phi projects onto ker(dphi)",
            "frobenius": "ker(dphi) integrable because d(dphi)=0",
            "remaining_time_problem": "Q_phi has signature N1_P2_Z0 and contains no selected timelike line",
        },
        "physical_branch_selected": False, "timelike_line_within_leaf_derived": False,
        "global_time_orientation_derived": False, "lapse_shift_derived": False,
        "maximum_conclusion": "EXACT_LOCAL_CONDITIONAL_PHI_DEPTH_FOLIATION_ON_SPACELIKE_DPHI_BRANCH__INTRALEAF_TIME_OPEN",
    }
    (HERE / "PHI_GRADIENT_SPACELIKE_BRANCH_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

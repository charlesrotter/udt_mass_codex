#!/usr/bin/env python3
"""Build the preregistered chart/coframe/supplied-split invariance atlas."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PARENT = ROOT / "udt_structural_ensemble_metric_atlas_2026-07-21"
EVALUATOR = ROOT / "udt_canonical_geometry_evaluator_p01_2026-07-21"
sys.path.insert(0, str(EVALUATOR))

from canonical_geometry_evaluator import metric_jets_from_split  # noqa: E402


SCHEMA = "udt-chart-coframe-invariance-atlas-1.0"
CLASSIFICATION = "BOUNDED_CHART_COFRAME_AND_SUPPLIED_SPLIT_ORBITS_OBSERVED"
MAXIMUM = "BOUNDED_CHART_COFRAME_AND_SUPPLIED_SPLIT_INVARIANCE_ATLAS_CHARACTERIZED"
ETA = np.diag((-1.0, 1.0, 1.0, 1.0))
TOL = 1.0e-10
ACTIVE_TOL = 1.0e-9
MARGIN_LOW = ACTIVE_TOL / 100.0
MARGIN_HIGH = ACTIVE_TOL * 100.0
PAYLOADS = (
    "metric_twojet", "riemann", "weyl", "ricci", "scalar", "cartan_curvature",
    "phi_twojet", "split_slot_twojet", "split_shear", "split_twist",
)
SPLIT_PAYLOADS = {"split_slot_twojet", "split_shear", "split_twist"}
SOURCE_HASHES = {
    "udt_structural_ensemble_metric_atlas_2026-07-21/SHA256SUMS.txt":
        "3d569ed31506f5f7ce44beac30e8419571f734b3973dcc34d6c474bf78636757",
    "udt_canonical_geometry_evaluator_p01_2026-07-21/SHA256SUMS.txt":
        "b7d8917cb27627c7ad7767fcffbd5b5d7a9dc6da2171b2d8fba329d04014ffad",
    "udt_complete_metric_solution_space_map_2026-07-21/SHA256SUMS.txt":
        "1778e4dcfcf9ac0bd3574fb3ff5248f2990265fa40d0822ff964ac67c434ae38",
}
PREREG_HASHES = {
    "PREREGISTRATION.md": "9f1d1efa85f1f534db25aeeccb1d51e4ca2033f76f1261b402d41df3b5e265ff",
    "PREREGISTRATION_CORRECTION.md": "TO_BE_REPLACED",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def write_tsv(name: str, fields: list[str], rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def relmax(actual: np.ndarray | float, expected: np.ndarray | float) -> float:
    a = np.asarray(actual, dtype=float)
    b = np.asarray(expected, dtype=float)
    return float(np.max(np.abs(a - b)) / max(1.0, float(np.max(np.abs(b)))))


def flatten_twojet(value: np.ndarray, first: np.ndarray, second: np.ndarray) -> np.ndarray:
    return np.concatenate((np.asarray(value).reshape(-1), np.asarray(first).reshape(-1), np.asarray(second).reshape(-1)))


def coordinate_matrices() -> list[dict[str, object]]:
    block = np.array([
        [1.0, .2, 0.0, 0.0], [.1, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, -.15], [0.0, 0.0, .25, 1.0],
    ])
    cross = np.array([
        [1.0, 0.0, .12, 0.0], [0.0, 1.0, 0.0, -.18],
        [.07, 0.0, 1.0, 0.0], [0.0, .09, 0.0, 1.0],
    ])
    swap12 = np.eye(4)
    swap12[[1, 2]] = swap12[[2, 1]]
    swap02 = np.eye(4)
    swap02[[0, 2]] = swap02[[2, 0]]
    return [
        {"id": "C00_IDENTITY", "kind": "COORDINATE", "matrix": np.eye(4), "distribution": "ORIGINAL", "inverse_pair": "C00_IDENTITY"},
        {"id": "C01_BLOCK_GENERAL", "kind": "COORDINATE", "matrix": block, "distribution": "BLOCK_PRESERVING", "inverse_pair": "C02_BLOCK_GENERAL_INVERSE"},
        {"id": "C02_BLOCK_GENERAL_INVERSE", "kind": "COORDINATE", "matrix": np.linalg.inv(block), "distribution": "BLOCK_PRESERVING", "inverse_pair": "C01_BLOCK_GENERAL"},
        {"id": "C03_CROSS_GENERAL", "kind": "COORDINATE", "matrix": cross, "distribution": "CROSS_RESEATED", "inverse_pair": "C04_CROSS_GENERAL_INVERSE"},
        {"id": "C04_CROSS_GENERAL_INVERSE", "kind": "COORDINATE", "matrix": np.linalg.inv(cross), "distribution": "CROSS_RESEATED", "inverse_pair": "C03_CROSS_GENERAL"},
        {"id": "C05_SWAP_DEPTH_SCREEN", "kind": "COORDINATE", "matrix": swap12, "distribution": "PERMUTED_RESEATED", "inverse_pair": "C05_SWAP_DEPTH_SCREEN"},
        {"id": "C06_SWAP_TIME_SCREEN", "kind": "COORDINATE", "matrix": swap02, "distribution": "PERMUTED_RESEATED", "inverse_pair": "C06_SWAP_TIME_SCREEN"},
    ]


def generator(kind: str) -> np.ndarray:
    result = np.zeros((4, 4))
    if kind == "K01":
        result[0, 1] = result[1, 0] = 1.0
    elif kind == "K02":
        result[0, 2] = result[2, 0] = 1.0
    elif kind == "K23":
        result[2, 3], result[3, 2] = -1.0, 1.0
    else:
        raise ValueError(kind)
    return result


def lorentz_matrix(kind: str, theta: float) -> np.ndarray:
    result = np.eye(4)
    if kind in {"K01", "K02"}:
        a = int(kind[-1])
        result[0, 0] = result[a, a] = math.cosh(theta)
        result[0, a] = result[a, 0] = math.sinh(theta)
    else:
        c, s = math.cos(theta), math.sin(theta)
        result[2, 2], result[2, 3] = c, -s
        result[3, 2], result[3, 3] = s, c
    return result


def coframe_transforms() -> list[dict[str, object]]:
    zero1, zero2 = np.zeros(4), np.zeros((4, 4))
    rows = [
        ("F01_CONSTANT_BASE_BOOST", "K01", .31, zero1, zero2),
        ("F02_LOCAL_BASE_BOOST", "K01", .31, np.array([.07, -.04, .03, .05]), np.array([
            [.02, .01, 0, -.005], [.01, -.015, .004, 0],
            [0, .004, .01, .006], [-.005, 0, .006, -.012],
        ])),
        ("F03_CONSTANT_CROSS_BOOST", "K02", .27, zero1, zero2),
        ("F04_LOCAL_CROSS_BOOST", "K02", -.22, np.array([-.03, .06, .02, -.05]), np.array([
            [.011, -.004, .003, 0], [-.004, .018, 0, -.006],
            [.003, 0, -.009, .005], [0, -.006, .005, .014],
        ])),
        ("F05_LOCAL_SCREEN_ROTATION", "K23", .37, np.array([.04, .02, -.06, .03]), np.array([
            [-.008, .003, 0, .004], [.003, .012, -.005, 0],
            [0, -.005, .016, .002], [.004, 0, .002, -.011],
        ])),
    ]
    result = []
    for identity, gen_name, theta, first, second in rows:
        k = generator(gen_name)
        lam = lorentz_matrix(gen_name, theta)
        dlam = np.array([first[a] * k @ lam for a in range(4)])
        ddlam = np.array([
            [second[a, b] * k @ lam + first[a] * first[b] * k @ k @ lam for b in range(4)]
            for a in range(4)
        ])
        result.append({
            "id": identity, "kind": "COFRAME", "matrix": lam, "distribution": "COORDINATE_SPLIT_UNCHANGED",
            "inverse_pair": "POINTWISE_INVERSE", "generator": gen_name, "parameter": theta,
            "parameter_first": first, "parameter_second": second,
            "matrix_first": dlam, "matrix_second": ddlam,
            "local": bool(np.max(np.abs(first)) or np.max(np.abs(second))),
        })
    return result


def transform_coframe_coordinate(e, de, dde, j):
    return (
        e @ j,
        np.einsum("kb,kim,ma->bia", j, de, j),
        np.einsum("kb,lc,klim,ma->bcia", j, j, dde, j),
    )


def transform_coframe_internal(e, de, dde, item):
    lam, dlam, ddlam = item["matrix"], item["matrix_first"], item["matrix_second"]
    et = lam @ e
    det = np.array([dlam[a] @ e + lam @ de[a] for a in range(4)])
    ddet = np.array([
        [ddlam[a, b] @ e + dlam[a] @ de[b] + dlam[b] @ de[a] + lam @ dde[a, b] for b in range(4)]
        for a in range(4)
    ])
    return et, det, ddet


def metric_from_coframe(e, de, dde):
    g = e.T @ ETA @ e
    dg = np.array([de[a].T @ ETA @ e + e.T @ ETA @ de[a] for a in range(4)])
    ddg = np.array([
        [
            dde[a, b].T @ ETA @ e + de[a].T @ ETA @ de[b]
            + de[b].T @ ETA @ de[a] + e.T @ ETA @ dde[a, b]
            for b in range(4)
        ] for a in range(4)
    ])
    return g, dg, ddg


def transform_metric_coordinate(g, dg, ddg, j):
    return (
        np.einsum("ma,mn,nb->ab", j, g, j),
        np.einsum("ka,mb,nc,kmn->abc", j, j, j, dg),
        np.einsum("ka,lb,mc,nd,klmn->abcd", j, j, j, j, ddg),
    )


def transform_covariant4(value, j):
    return np.einsum("ra,sb,uc,vd,rsuv->abcd", j, j, j, j, value)


def transform_covariant2(value, j):
    return np.einsum("ra,sb,rs->ab", j, j, value)


def transform_phi(phi, j):
    value = np.array([float(phi["value"])])
    first = np.einsum("ka,k->a", j, np.asarray(phi["first"], dtype=float))
    second = np.einsum("ka,lb,kl->ab", j, j, np.asarray(phi["second"], dtype=float))
    return value, first, second


def cartan_curvature(e, g, riemann):
    inverse = np.linalg.inv(g)
    up = np.einsum("ra,asuv->rsuv", inverse, riemann)
    return np.einsum("ir,rsuv,sj->ijuv", e, up, np.linalg.inv(e))


def matmul_jet(a, da, dda, b, db, ddb):
    value = a @ b
    first = np.array([da[k] @ b + a @ db[k] for k in range(4)])
    second = np.array([
        [dda[k, ell] @ b + da[k] @ db[ell] + da[ell] @ db[k] + a @ ddb[k, ell] for ell in range(4)]
        for k in range(4)
    ])
    return value, first, second


def transpose_jet(value, first, second):
    return value.T, np.swapaxes(first, 1, 2), np.swapaxes(second, 2, 3)


def split_from_metric_jets(g, dg, ddg):
    q, dq, ddq = g[2:, 2:], dg[:, 2:, 2:], ddg[:, :, 2:, 2:]
    gbb, dgbb, ddgbb = g[:2, :2], dg[:, :2, :2], ddg[:, :, :2, :2]
    b, db, ddb = g[:2, 2:].T, np.swapaxes(dg[:, :2, 2:], 1, 2), np.swapaxes(ddg[:, :, :2, 2:], 2, 3)
    q_eigs = np.linalg.eigvalsh(q)
    if np.min(np.abs(q_eigs)) <= ACTIVE_TOL:
        return {"status": "MARGINAL", "q_eigs": q_eigs, "h_eigs": np.array([np.nan, np.nan])}
    qinv = np.linalg.inv(q)
    dqinv = np.array([-qinv @ dq[k] @ qinv for k in range(4)])
    ddqinv = np.array([
        [qinv @ dq[ell] @ qinv @ dq[k] @ qinv + qinv @ dq[k] @ qinv @ dq[ell] @ qinv - qinv @ ddq[k, ell] @ qinv for ell in range(4)]
        for k in range(4)
    ])
    bt, dbt, ddbt = transpose_jet(b, db, ddb)
    temp = matmul_jet(bt, dbt, ddbt, qinv, dqinv, ddqinv)
    correction = matmul_jet(*temp, b, db, ddb)
    h, dh, ddh = gbb - correction[0], dgbb - correction[1], ddgbb - correction[2]
    h_eigs = np.linalg.eigvalsh(h)
    if np.min(np.abs(h_eigs)) <= ACTIVE_TOL:
        return {"status": "MARGINAL", "q_eigs": q_eigs, "h_eigs": h_eigs}
    if not (np.all(q_eigs > ACTIVE_TOL) and h_eigs[0] < -ACTIVE_TOL and h_eigs[1] > ACTIVE_TOL):
        return {"status": "INVALID_SIGNATURE", "q_eigs": q_eigs, "h_eigs": h_eigs}
    a = matmul_jet(qinv, dqinv, ddqinv, b, db, ddb)
    av, ad, add = a
    values = np.array([h[0, 0], h[0, 1], h[1, 1], q[0, 0], q[0, 1], q[1, 1], av[0, 0], av[1, 0], av[0, 1], av[1, 1]])
    first = np.array([[dh[k, 0, 0], dh[k, 0, 1], dh[k, 1, 1], dq[k, 0, 0], dq[k, 0, 1], dq[k, 1, 1], ad[k, 0, 0], ad[k, 1, 0], ad[k, 0, 1], ad[k, 1, 1]] for k in range(4)])
    second = np.array([[[ddh[k, ell, 0, 0], ddh[k, ell, 0, 1], ddh[k, ell, 1, 1], ddq[k, ell, 0, 0], ddq[k, ell, 0, 1], ddq[k, ell, 1, 1], add[k, ell, 0, 0], add[k, ell, 1, 0], add[k, ell, 0, 1], add[k, ell, 1, 1]] for ell in range(4)] for k in range(4)])
    rebuilt = metric_jets_from_split(values, first, second)
    forward = max(relmax(rebuilt.metric, g), relmax(rebuilt.first, dg), relmax(rebuilt.second, ddg))
    shear, twist = split_kinematics(values, first)
    return {
        "status": "DEFINED", "q_eigs": q_eigs, "h_eigs": h_eigs, "values": values,
        "first": first, "second": second, "forward_residual": forward,
        "shear": shear, "twist": twist,
    }


def split_kinematics(values, first):
    q = np.array([[values[3], values[4]], [values[4], values[5]]])
    shifts = np.array([[values[6], values[8]], [values[7], values[9]]])
    dq = [np.array([[first[k, 3], first[k, 4]], [first[k, 4], first[k, 5]]]) for k in range(4)]
    da = [np.array([[first[k, 6], first[k, 8]], [first[k, 7], first[k, 9]]]) for k in range(4)]
    inverse = np.linalg.inv(q)
    twist = np.zeros(2)
    for vertical in range(2):
        twist[vertical] = da[0][vertical, 1] - da[1][vertical, 0] - sum(shifts[other, 0] * da[2 + other][vertical, 1] for other in range(2)) + sum(shifts[other, 1] * da[2 + other][vertical, 0] for other in range(2))
    shears = []
    for base in range(2):
        horizontal = dq[base] - sum(shifts[vertical, base] * dq[2 + vertical] for vertical in range(2))
        vertical_derivative = np.array([[da[2 + derivative][output, base] for output in range(2)] for derivative in range(2)])
        deformation = .5 * (horizontal - vertical_derivative @ q - q @ vertical_derivative.T)
        expansion = float(np.trace(inverse @ deformation))
        shear = deformation - .5 * expansion * q
        shears.append((shear[0, 0], shear[0, 1], shear[1, 1]))
    return np.asarray(shears), twist


def baseline_payload(raw):
    g = np.asarray(raw["metric"], dtype=float)
    e = np.asarray(raw["coframe"], dtype=float)
    riemann = np.asarray(raw["riemann_down"], dtype=float)
    phi = raw["phi"]
    return {
        "metric_twojet": flatten_twojet(g, np.asarray(raw["metric_first"]), np.asarray(raw["metric_second"])),
        "riemann": riemann.reshape(-1),
        "weyl": np.asarray(raw["weyl_down"], dtype=float).reshape(-1),
        "ricci": np.asarray(raw["ricci"], dtype=float).reshape(-1),
        "scalar": np.array([float(raw["observables"]["scalar_curvature"])]),
        "cartan_curvature": cartan_curvature(e, g, riemann).reshape(-1),
        "phi_twojet": flatten_twojet(np.array([phi["value"]]), np.asarray(phi["first"]), np.asarray(phi["second"])),
        "split_slot_twojet": flatten_twojet(np.asarray(raw["slot_values"]), np.asarray(raw["slot_first"]), np.asarray(raw["slot_second"])),
        "split_shear": np.asarray(raw["shear_vector"], dtype=float).reshape(-1),
        "split_twist": np.asarray(raw["twist_vector"], dtype=float).reshape(-1),
    }


def transform_record(raw, item):
    e, de, dde = (np.asarray(raw[name], dtype=float) for name in ("coframe", "coframe_first", "coframe_second"))
    g, dg, ddg = (np.asarray(raw[name], dtype=float) for name in ("metric", "metric_first", "metric_second"))
    riemann, weyl, ricci = (np.asarray(raw[name], dtype=float) for name in ("riemann_down", "weyl_down", "ricci"))
    scalar = float(raw["observables"]["scalar_curvature"])
    base_cartan = cartan_curvature(e, g, riemann)
    if item["kind"] == "COORDINATE":
        j = item["matrix"]
        et, det, ddet = transform_coframe_coordinate(e, de, dde, j)
        gt, dgt, ddgt = transform_metric_coordinate(g, dg, ddg, j)
        rt, wt, rit = transform_covariant4(riemann, j), transform_covariant4(weyl, j), transform_covariant2(ricci, j)
        phiv, phid, phidd = transform_phi(raw["phi"], j)
        predicted_cartan = np.einsum("ua,vb,ijuv->ijab", j, j, base_cartan)
        roundtrip = transform_metric_coordinate(gt, dgt, ddgt, np.linalg.inv(j))
        roundtrip_residual = max(relmax(roundtrip[0], g), relmax(roundtrip[1], dg), relmax(roundtrip[2], ddg))
        determinant_expected = np.linalg.det(j) ** 2 * np.linalg.det(g)
    else:
        et, det, ddet = transform_coframe_internal(e, de, dde, item)
        gt, dgt, ddgt = g.copy(), dg.copy(), ddg.copy()
        rt, wt, rit = riemann.copy(), weyl.copy(), ricci.copy()
        phiv, phid, phidd = transform_phi(raw["phi"], np.eye(4))
        lam = item["matrix"]
        predicted_cartan = np.einsum("ia,abuv,bj->ijuv", lam, base_cartan, np.linalg.inv(lam))
        roundtrip_residual = 0.0
        determinant_expected = np.linalg.det(g)
    metric_from_frame = metric_from_coframe(et, det, ddet)
    metric_residual = max(relmax(metric_from_frame[0], gt), relmax(metric_from_frame[1], dgt), relmax(metric_from_frame[2], ddgt))
    ct = cartan_curvature(et, gt, rt)
    cartan_residual = relmax(ct, predicted_cartan)
    inverse = np.linalg.inv(gt)
    up = np.einsum("ra,asuv->rsuv", inverse, rt)
    ricci_from_riemann = np.einsum("rsrn->sn", up)
    scalar_from_ricci = float(np.einsum("ab,ab", inverse, rit))
    split = split_from_metric_jets(gt, dgt, ddgt)
    payload = {
        "metric_twojet": flatten_twojet(gt, dgt, ddgt), "riemann": rt.reshape(-1),
        "weyl": wt.reshape(-1), "ricci": rit.reshape(-1), "scalar": np.array([scalar]),
        "cartan_curvature": ct.reshape(-1), "phi_twojet": flatten_twojet(phiv, phid, phidd),
        "split_slot_twojet": None, "split_shear": None, "split_twist": None,
    }
    if split["status"] == "DEFINED":
        payload.update({
            "split_slot_twojet": flatten_twojet(split["values"], split["first"], split["second"]),
            "split_shear": split["shear"].reshape(-1), "split_twist": split["twist"].reshape(-1),
        })
    determinant_residual = abs(float(np.linalg.det(gt)) - determinant_expected) / max(1.0, abs(determinant_expected))
    ricci_residual = relmax(ricci_from_riemann, rit)
    scalar_residual = abs(scalar_from_ricci - scalar) / max(1.0, abs(scalar))
    weyl_trace = float(np.max(np.abs(np.einsum("ac,abcd->bd", inverse, wt))))
    failures = max(metric_residual, cartan_residual, determinant_residual, ricci_residual, scalar_residual, roundtrip_residual)
    if failures > TOL:
        primary = "NUMERIC_COVARIANCE_FAILURE"
    elif item["kind"] == "COFRAME":
        primary = "METRIC_INVARIANT_COFRAME_GAUGE"
    elif split["status"] == "INVALID_SIGNATURE":
        primary = "SUPPLIED_SPLIT_UNDEFINED_SIGNATURE"
    elif split["status"] == "MARGINAL":
        primary = "SUPPLIED_SPLIT_MARGINAL"
    elif item["distribution"] in {"CROSS_RESEATED", "PERMUTED_RESEATED"}:
        primary = "SUPPLIED_SPLIT_RESEATED_DEFINED"
    else:
        primary = "TENSOR_COVARIANT_COMPONENT_CHANGE"
    return payload, split, {
        "primary_status": primary, "metric_twojet_residual": metric_residual,
        "cartan_covariance_residual": cartan_residual, "determinant_weight_residual": determinant_residual,
        "ricci_contraction_residual": ricci_residual, "scalar_contraction_residual": scalar_residual,
        "weyl_trace_max_abs": weyl_trace, "inverse_roundtrip_residual": roundtrip_residual,
        "metric_determinant": float(np.linalg.det(gt)),
        "metric_inertia": ",".join(map(str, inertia(gt))),
    }


def inertia(matrix):
    eigs = np.linalg.eigvalsh(matrix)
    return int(np.count_nonzero(eigs < -ACTIVE_TOL)), int(np.count_nonzero(eigs > ACTIVE_TOL)), int(np.count_nonzero(np.abs(eigs) <= ACTIVE_TOL))


def represent_payload(name: str, vector: np.ndarray, item):
    if item["kind"] == "COFRAME":
        if name == "cartan_curvature":
            c = vector.reshape(4, 4, 4, 4)
            lam = item["matrix"]
            return np.einsum("ia,abuv,bj->ijuv", lam, c, np.linalg.inv(lam)).reshape(-1)
        return vector.copy()
    j = item["matrix"]
    if name == "metric_twojet":
        g, dg, ddg = vector[:16].reshape(4, 4), vector[16:80].reshape(4, 4, 4), vector[80:].reshape(4, 4, 4, 4)
        return flatten_twojet(*transform_metric_coordinate(g, dg, ddg, j))
    if name in {"riemann", "weyl"}:
        return transform_covariant4(vector.reshape(4, 4, 4, 4), j).reshape(-1)
    if name == "ricci":
        return transform_covariant2(vector.reshape(4, 4), j).reshape(-1)
    if name == "scalar":
        return vector.copy()
    if name == "cartan_curvature":
        return np.einsum("ua,vb,ijuv->ijab", j, j, vector.reshape(4, 4, 4, 4)).reshape(-1)
    if name == "phi_twojet":
        return flatten_twojet(np.array([vector[0]]), np.einsum("ka,k->a", j, vector[1:5]), np.einsum("ka,lb,kl->ab", j, j, vector[5:].reshape(4, 4)))
    if item["id"] == "C00_IDENTITY":
        return vector.copy()
    return None


def interaction_fields() -> list[str]:
    fields = ["transform_id", "interaction_id", "carrier_id", "bank", "point_id", "target_mask", "target_integer", "ensemble_order", "subsets_used"]
    for name in PAYLOADS:
        fields.extend([f"{name}_domain", f"{name}_l2", f"{name}_max_abs", f"{name}_active", f"{name}_baseline_active", f"{name}_covariance_residual"])
    return fields


def main() -> None:
    checks = []

    def check(name, condition):
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    PREREG_HASHES["PREREGISTRATION_CORRECTION.md"] = "c3ee82ce5603a8bfeabc653e56ab8664b17f1c7597ddfa9ec0a3fa69cc948454"
    for path, expected in SOURCE_HASHES.items():
        check(f"source_{path}", digest(ROOT / path) == expected)
    for path, expected in PREREG_HASHES.items():
        check(f"prereg_{path}", digest(HERE / path) == expected)
    source_rows = [{"path": path, "sha256": value, "role": "IMMUTABLE_SOURCE"} for path, value in SOURCE_HASHES.items()]
    source_rows += [{"path": path, "sha256": value, "role": "PREREGISTRATION"} for path, value in PREREG_HASHES.items()]
    write_tsv("SOURCE_LINEAGE.tsv", ["path", "sha256", "role"], source_rows)

    transforms = coordinate_matrices() + coframe_transforms()
    check("transformation_count", len(transforms) == 12 and len({x["id"] for x in transforms}) == 12)
    transform_rows = []
    for item in transforms:
        matrix = item["matrix"]
        lorentz_residual = relmax(matrix.T @ ETA @ matrix, ETA) if item["kind"] == "COFRAME" else ""
        check(f"invertible_{item['id']}", abs(np.linalg.det(matrix)) > 1e-12)
        if item["kind"] == "COFRAME":
            check(f"lorentz_{item['id']}", float(lorentz_residual) <= TOL)
        transform_rows.append({
            "transform_id": item["id"], "kind": item["kind"], "distribution_relation": item["distribution"],
            "inverse_pair": item["inverse_pair"], "determinant": float(np.linalg.det(matrix)),
            "matrix_json": json.dumps(matrix.tolist(), separators=(",", ":")),
            "local": "YES" if item.get("local", False) else "NO",
            "generator": item.get("generator", ""), "parameter": item.get("parameter", ""),
            "parameter_first_json": json.dumps(np.asarray(item.get("parameter_first", [])).tolist(), separators=(",", ":")),
            "parameter_second_json": json.dumps(np.asarray(item.get("parameter_second", [])).tolist(), separators=(",", ":")),
            "lorentz_residual": lorentz_residual,
        })
    write_tsv("TRANSFORMATION_REGISTRY.tsv", list(transform_rows[0]), transform_rows)

    parent_config = read_tsv(PARENT / "CONFIGURATION_OBSERVATIONS.tsv")
    parent_interactions = read_tsv(PARENT / "MOBIUS_INTERACTIONS.tsv")
    check("parent_configurations", len(parent_config) == 6144 and len({r["configuration_id"] for r in parent_config}) == 6144)
    check("parent_interactions", len(parent_interactions) == 5760 and len({r["interaction_id"] for r in parent_interactions}) == 5760)
    shard_registry = read_tsv(PARENT / "RAW_SHARD_REGISTRY.tsv")
    check("parent_raw_shards", len(shard_registry) == 8 and sum(int(r["records"]) for r in shard_registry) == 6144)

    config_fields = [
        "transform_id", "configuration_id", "carrier_id", "mask_id", "mask_integer", "bank", "point_id",
        "primary_status", "split_status", "q_eigenvalues", "h_eigenvalues", "split_forward_residual",
        "shear_rank", "twist_rank", "shear_max_abs", "twist_max_abs", "metric_twojet_residual",
        "cartan_covariance_residual", "determinant_weight_residual", "ricci_contraction_residual",
        "scalar_contraction_residual", "weyl_trace_max_abs", "inverse_roundtrip_residual",
        "metric_determinant", "metric_inertia", "retained", "physical_merit",
    ]
    interaction_header = interaction_fields()
    config_handles, config_writers, interaction_handles, interaction_writers = {}, {}, {}, {}
    config_shards, interaction_shards = [], []
    for item in transforms:
        identity = item["id"]
        cp = HERE / f"CONFIGURATION_ORBITS_{identity}.tsv"
        mp = HERE / f"MOBIUS_ORBITS_{identity}.tsv"
        config_handles[identity] = cp.open("w", encoding="utf-8", newline="")
        interaction_handles[identity] = mp.open("w", encoding="utf-8", newline="")
        config_writers[identity] = csv.DictWriter(config_handles[identity], fieldnames=config_fields, delimiter="\t", lineterminator="\n")
        interaction_writers[identity] = csv.DictWriter(interaction_handles[identity], fieldnames=interaction_header, delimiter="\t", lineterminator="\n")
        config_writers[identity].writeheader()
        interaction_writers[identity].writeheader()

    config_status = defaultdict(Counter)
    split_status = defaultdict(Counter)
    order_stats = defaultdict(lambda: Counter())
    margins = defaultdict(list)
    span_vectors = defaultdict(list)
    max_residuals = defaultdict(float)
    config_counts = Counter()
    interaction_counts = Counter()

    for shard in shard_registry:
        with (PARENT / shard["path"]).open(encoding="utf-8") as handle:
            raw_rows = [json.loads(line) for line in handle]
        check(f"raw_shard_{shard['path']}", len(raw_rows) == int(shard["records"]) and digest(PARENT / shard["path"]) == shard["sha256"])
        transformed_context = {item["id"]: {} for item in transforms}
        baseline_context = {}
        for raw in raw_rows:
            key = (raw["carrier_id"], int(raw["mask_integer"]))
            baseline_context[key] = baseline_payload(raw)
            for item in transforms:
                identity = item["id"]
                payload, split, diagnostics = transform_record(raw, item)
                transformed_context[identity][key] = payload
                q_eigs, h_eigs = split["q_eigs"], split["h_eigs"]
                row = {
                    "transform_id": identity, "configuration_id": raw["configuration_id"], "carrier_id": raw["carrier_id"],
                    "mask_id": raw["mask_id"], "mask_integer": raw["mask_integer"], "bank": raw["bank"], "point_id": raw["point_id"],
                    **diagnostics, "split_status": split["status"],
                    "q_eigenvalues": ";".join(f"{x:.17g}" for x in q_eigs),
                    "h_eigenvalues": ";".join("nan" if not np.isfinite(x) else f"{x:.17g}" for x in h_eigs),
                    "split_forward_residual": split.get("forward_residual", ""),
                    "shear_rank": int(np.linalg.matrix_rank(split["shear"], tol=ACTIVE_TOL)) if split["status"] == "DEFINED" else "",
                    "twist_rank": int(np.linalg.matrix_rank(split["twist"].reshape(2, 1), tol=ACTIVE_TOL)) if split["status"] == "DEFINED" else "",
                    "shear_max_abs": float(np.max(np.abs(split["shear"]))) if split["status"] == "DEFINED" else "",
                    "twist_max_abs": float(np.max(np.abs(split["twist"]))) if split["status"] == "DEFINED" else "",
                    "retained": "YES", "physical_merit": "NOT_EVALUATED",
                }
                config_writers[identity].writerow(row)
                config_counts[identity] += 1
                config_status[identity][diagnostics["primary_status"]] += 1
                split_status[identity][split["status"]] += 1
                for field in ("metric_twojet_residual", "cartan_covariance_residual", "determinant_weight_residual", "ricci_contraction_residual", "scalar_contraction_residual", "inverse_roundtrip_residual"):
                    max_residuals[(identity, field)] = max(max_residuals[(identity, field)], float(diagnostics[field]))

        carrier_ids = sorted({r["carrier_id"] for r in raw_rows})
        bank, point_id = raw_rows[0]["bank"], raw_rows[0]["point_id"]
        for item in transforms:
            identity = item["id"]
            for carrier in carrier_ids:
                for target in range(1, 16):
                    subsets = [subset for subset in range(16) if subset & ~target == 0]
                    interaction_id = f"{carrier}_T{target:X}_{bank}_{point_id}"
                    row = {
                        "transform_id": identity, "interaction_id": interaction_id, "carrier_id": carrier,
                        "bank": bank, "point_id": point_id, "target_mask": f"M{target:X}", "target_integer": target,
                        "ensemble_order": target.bit_count(), "subsets_used": ";".join(f"M{x:X}" for x in subsets),
                    }
                    for name in PAYLOADS:
                        base = sum(((-1) ** (target.bit_count() - subset.bit_count())) * baseline_context[(carrier, subset)][name] for subset in subsets)
                        vertices = [transformed_context[identity][(carrier, subset)][name] for subset in subsets]
                        base_active = "YES" if float(np.max(np.abs(base))) > ACTIVE_TOL else "NO"
                        if any(value is None for value in vertices):
                            row.update({f"{name}_domain": "UNDEFINED_SPLIT_DOMAIN", f"{name}_l2": "", f"{name}_max_abs": "", f"{name}_active": "", f"{name}_baseline_active": base_active, f"{name}_covariance_residual": ""})
                            order_stats[(identity, target.bit_count(), name)]["undefined"] += 1
                            continue
                        vector = sum(((-1) ** (target.bit_count() - subset.bit_count())) * vertices[index] for index, subset in enumerate(subsets))
                        maximum = float(np.max(np.abs(vector)))
                        active = "YES" if maximum > ACTIVE_TOL else "NO"
                        expected = represent_payload(name, base, item)
                        covariance = relmax(vector, expected) if expected is not None else ""
                        domain = "DEFINED_COVARIANCE_CHECKED" if expected is not None else "DEFINED_NO_LINEAR_CONTRACT"
                        row.update({f"{name}_domain": domain, f"{name}_l2": float(np.linalg.norm(vector)), f"{name}_max_abs": maximum, f"{name}_active": active, f"{name}_baseline_active": base_active, f"{name}_covariance_residual": covariance})
                        span_vectors[(identity, target, name)].append(vector)
                        margins[(identity, name)].append(maximum)
                        order_stats[(identity, target.bit_count(), name)]["defined"] += 1
                        order_stats[(identity, target.bit_count(), name)]["active" if active == "YES" else "inactive"] += 1
                        order_stats[(identity, target.bit_count(), name)]["discordant" if active != base_active else "concordant"] += 1
                        if covariance != "":
                            max_residuals[(identity, f"mobius_{name}")] = max(max_residuals[(identity, f"mobius_{name}")], float(covariance))
                    interaction_writers[identity].writerow(row)
                    interaction_counts[identity] += 1

    for handle in list(config_handles.values()) + list(interaction_handles.values()):
        handle.close()
    for item in transforms:
        identity = item["id"]
        cp, mp = HERE / f"CONFIGURATION_ORBITS_{identity}.tsv", HERE / f"MOBIUS_ORBITS_{identity}.tsv"
        config_shards.append({"transform_id": identity, "path": cp.name, "rows": config_counts[identity], "bytes": cp.stat().st_size, "sha256": digest(cp)})
        interaction_shards.append({"transform_id": identity, "path": mp.name, "rows": interaction_counts[identity], "bytes": mp.stat().st_size, "sha256": digest(mp)})
    check("configuration_orbit_count", sum(config_counts.values()) == 73728 and all(value == 6144 for value in config_counts.values()))
    check("interaction_orbit_count", sum(interaction_counts.values()) == 69120 and all(value == 5760 for value in interaction_counts.values()))
    check("no_numeric_covariance_failures", sum(c["NUMERIC_COVARIANCE_FAILURE"] for c in config_status.values()) == 0)
    check("full_tensor_mobius_covariance", all(value <= TOL for (identity, field), value in max_residuals.items() if field.startswith("mobius_") and field.replace("mobius_", "") not in SPLIT_PAYLOADS))
    check("all_retained", sum(config_counts.values()) == 73728)
    write_tsv("CONFIGURATION_ORBIT_SHARDS.tsv", list(config_shards[0]), config_shards)
    write_tsv("MOBIUS_ORBIT_SHARDS.tsv", list(interaction_shards[0]), interaction_shards)

    census_rows = []
    split_rows = []
    for item in transforms:
        identity = item["id"]
        for status, count in sorted(config_status[identity].items()):
            census_rows.append({"transform_id": identity, "kind": item["kind"], "primary_status": status, "configurations": count})
        for status, count in sorted(split_status[identity].items()):
            split_rows.append({"transform_id": identity, "distribution_relation": item["distribution"], "split_status": status, "configurations": count, "retained": "YES"})
    write_tsv("INVARIANCE_CENSUS.tsv", list(census_rows[0]), census_rows)
    write_tsv("SPLIT_DOMAIN_CENSUS.tsv", list(split_rows[0]), split_rows)

    order_rows = []
    for (identity, order, name), counter in sorted(order_stats.items()):
        order_rows.append({"transform_id": identity, "ensemble_order": order, "payload": name, "defined_rows": counter["defined"], "undefined_rows": counter["undefined"], "active_rows": counter["active"], "inactive_rows": counter["inactive"], "activity_concordant": counter["concordant"], "activity_discordant": counter["discordant"]})
    write_tsv("INTERACTION_ORDER_CENSUS.tsv", list(order_rows[0]), order_rows)

    span_rows = []
    for item in transforms:
        identity = item["id"]
        for target in range(1, 16):
            for name in PAYLOADS:
                vectors = span_vectors[(identity, target, name)]
                if vectors:
                    matrix = np.stack(vectors)
                    singular = np.linalg.svd(matrix, compute_uv=False)
                    rank = int(np.count_nonzero(singular > ACTIVE_TOL))
                    retained = singular[singular > ACTIVE_TOL]
                    discarded = singular[singular <= ACTIVE_TOL]
                    row = {"vectors_defined": len(vectors), "components": matrix.shape[1], "span_rank": rank, "largest_singular": float(singular[0]), "min_retained_singular": float(np.min(retained)) if retained.size else 0.0, "max_discarded_singular": float(np.max(discarded)) if discarded.size else 0.0}
                else:
                    row = {"vectors_defined": 0, "components": "", "span_rank": "", "largest_singular": "", "min_retained_singular": "", "max_discarded_singular": ""}
                span_rows.append({"transform_id": identity, "target_mask": f"M{target:X}", "target_integer": target, "ensemble_order": target.bit_count(), "payload": name, **row, "rank_threshold": ACTIVE_TOL, "physical_dof_claimed": "NO"})
    check("span_rows", len(span_rows) == 1800)
    write_tsv("TRANSFORMED_SPAN_RANKS.tsv", list(span_rows[0]), span_rows)
    rank_margin_rows = []
    for row in span_rows:
        if row["span_rank"] == "":
            status = "UNDEFINED_SPLIT_DOMAIN"
        else:
            retained_value = float(row["min_retained_singular"])
            discarded_value = float(row["max_discarded_singular"])
            retained_near = retained_value > 0.0 and MARGIN_LOW <= retained_value <= MARGIN_HIGH
            discarded_near = discarded_value > 0.0 and MARGIN_LOW <= discarded_value <= MARGIN_HIGH
            status = "NUMERIC_UNCERTAIN" if retained_near or discarded_near else "NUMERIC_CLASSIFIED"
        rank_margin_rows.append({
            "transform_id": row["transform_id"], "target_mask": row["target_mask"],
            "target_integer": row["target_integer"], "payload": row["payload"],
            "span_rank": row["span_rank"], "min_retained_singular": row["min_retained_singular"],
            "max_discarded_singular": row["max_discarded_singular"], "rank_threshold": ACTIVE_TOL,
            "caution_low": MARGIN_LOW, "caution_high": MARGIN_HIGH, "rank_margin_status": status,
        })
    check("rank_margin_rows", len(rank_margin_rows) == 1800)
    write_tsv("RANK_THRESHOLD_MARGIN_LEDGER.tsv", list(rank_margin_rows[0]), rank_margin_rows)

    margin_rows = []
    for item in transforms:
        identity = item["id"]
        for name in PAYLOADS:
            values = margins[(identity, name)]
            active = [v for v in values if v > ACTIVE_TOL]
            inactive = [v for v in values if v <= ACTIVE_TOL]
            margin_rows.append({"transform_id": identity, "payload": name, "defined_rows": len(values), "active_rows": len(active), "inactive_rows": len(inactive), "uncertain_rows": sum(MARGIN_LOW <= v <= MARGIN_HIGH for v in values), "min_active_max_abs": min(active) if active else 0.0, "max_inactive_max_abs": max(inactive) if inactive else 0.0, "max_observed_abs": max(values) if values else "", "activity_threshold": ACTIVE_TOL})
    write_tsv("NUMERIC_MARGIN_LEDGER.tsv", list(margin_rows[0]), margin_rows)

    residual_rows = [{"transform_id": identity, "quantity": field, "max_relative_residual": value, "tolerance": TOL, "pass": "YES" if value <= TOL else "NO"} for (identity, field), value in sorted(max_residuals.items())]
    write_tsv("COVARIANCE_RESIDUAL_CENSUS.tsv", list(residual_rows[0]), residual_rows)

    coverage = [
        ("C01", "parent configurations", 6144, 6144), ("C02", "parent interactions", 5760, 5760),
        ("C03", "registered transformations", 12, 12), ("C04", "configuration orbit rows", sum(config_counts.values()), 73728),
        ("C05", "interaction orbit rows", sum(interaction_counts.values()), 69120), ("C06", "configuration shards", len(config_shards), 12),
        ("C07", "interaction shards", len(interaction_shards), 12), ("C08", "span rows", len(span_rows), 1800),
        ("C09", "discarded configurations", 0, 0), ("C10", "solutions/actions loaded", 0, 0),
    ]
    write_tsv("COVERAGE_LEDGER.tsv", ["id", "object", "observed", "required", "pass"], [{"id": a, "object": b, "observed": c, "required": d, "pass": "YES" if c == d else "NO"} for a, b, c, d in coverage])
    premise_rows = [
        ("P01", "4D conformal-Lorentzian coframe metric", "CONDITIONAL", "parent realization"),
        ("P02", "twelve exact transformations", "FREE_AND_EXPLORED", "finite registered probes"),
        ("P03", "constant coordinate charts", "BOUNDED", "nonlinear charts open"),
        ("P04", "local Lorentz coframes", "GAUGE_TEST", "registered values and two-jets"),
        ("P05", "first-two last-two split", "CHOSE", "reseated and audited, not selected"),
        ("P06", "ensemble mask histories", "CHOSE", "fixed before transformations"),
        ("P07", "component activity threshold", "PINNED_BY_HABIT", "1e-9 with margins"),
        ("P08", "action source carrier boundary scale", "OPEN", "not loaded"),
    ]
    write_tsv("PREMISE_STATUS_LEDGER.tsv", ["id", "premise", "status", "scope"], [{"id": a, "premise": b, "status": c, "scope": d} for a, b, c, d in premise_rows])
    anti = [
        "chart component change called new geometry", "coframe gauge called physical sector", "reseated split called selected",
        "invalid split discarded", "undefined split imputed", "component rank called physical degrees of freedom",
        "ensemble mask re-fit after transform", "finite probes called full group proof", "action or source inferred",
        "unexpected pattern filtered", "coordinate reseating called evolution", "physical merit ranking",
    ]
    write_tsv("ANTI_IMPOSITION_AUDIT.tsv", ["id", "failure_mode", "present"], [{"id": f"A{i:02d}", "failure_mode": text, "present": "ABSENT"} for i, text in enumerate(anti, 1)])

    result = {
        "schema": SCHEMA, "status": "PASS", "classification": CLASSIFICATION, "maximum_conclusion": MAXIMUM,
        "checks": len(checks), "checks_passed": checks, "transformations": len(transforms),
        "configuration_records": 6144, "interaction_records": 5760,
        "configuration_orbit_records": sum(config_counts.values()), "interaction_orbit_records": sum(interaction_counts.values()),
        "configuration_shards": len(config_shards), "interaction_shards": len(interaction_shards), "span_rows": len(span_rows),
        "numeric_uncertain_span_rows": sum(row["rank_margin_status"] == "NUMERIC_UNCERTAIN" for row in rank_margin_rows),
        "split_domain_counts": {identity: dict(counter) for identity, counter in sorted(split_status.items())},
        "primary_status_counts": {identity: dict(counter) for identity, counter in sorted(config_status.items())},
        "max_certification_residual": max(max_residuals.values()),
        "numeric_covariance_failures": sum(c["NUMERIC_COVARIANCE_FAILURE"] for c in config_status.values()),
        "discarded_records": 0, "physical_merit_filter": False, "action_loaded": False, "solutions_run": 0,
        "full_group_exhaustiveness_claim": False, "split_selected_claim": False, "gpu_used": False,
        "evidence_grade": "OBSERVED_PENDING_INDEPENDENT_VERIFICATION",
    }
    (HERE / "ATLAS_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    transcript = [
        "UDT_CHART_COFRAME_INVARIANCE_ATLAS=PASS",
        f"checks={len(checks)} transformations=12 configurations=6144 interactions=5760",
        f"configuration_orbits={result['configuration_orbit_records']} interaction_orbits={result['interaction_orbit_records']}",
        f"split_domain_counts={result['split_domain_counts']}",
        f"primary_status_counts={result['primary_status_counts']}",
        f"max_certification_residual={result['max_certification_residual']:.17g} numeric_covariance_failures=0",
        "discarded=0 merit_filter=NO action=NO solutions=0 full_group_claim=NO split_selected=NO gpu=NO",
        f"maximum_conclusion={MAXIMUM}",
    ]
    (HERE / "ATLAS_TRANSCRIPT.txt").write_text("\n".join(transcript) + "\n", encoding="utf-8")
    print("\n".join(transcript))


if __name__ == "__main__":
    main()

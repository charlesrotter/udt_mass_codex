#!/usr/bin/env python3
"""Independent fail-closed verifier for the chart/coframe invariance atlas.

This file deliberately does not import build_invariance_atlas.py.
"""

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
sys.path.insert(0, str(ROOT / "udt_canonical_geometry_evaluator_p01_2026-07-21"))

from canonical_geometry_evaluator import MetricJets, evaluate_coframe_jets, evaluate_metric_jets, metric_jets_from_split  # noqa: E402


ETA = np.diag((-1.0, 1.0, 1.0, 1.0))
TOL = 1.0e-10
ACTIVE_TOL = 1.0e-9
MAXIMUM = "BOUNDED_CHART_COFRAME_AND_SUPPLIED_SPLIT_INVARIANCE_ATLAS_CHARACTERIZED"
FULL_TENSORS = ("metric_twojet", "riemann", "weyl", "ricci", "scalar", "cartan_curvature", "phi_twojet")
SPLIT_PAYLOADS = ("split_slot_twojet", "split_shear", "split_twist")
SOURCE_HASHES = {
    "udt_structural_ensemble_metric_atlas_2026-07-21/SHA256SUMS.txt": "3d569ed31506f5f7ce44beac30e8419571f734b3973dcc34d6c474bf78636757",
    "udt_canonical_geometry_evaluator_p01_2026-07-21/SHA256SUMS.txt": "b7d8917cb27627c7ad7767fcffbd5b5d7a9dc6da2171b2d8fba329d04014ffad",
    "udt_complete_metric_solution_space_map_2026-07-21/SHA256SUMS.txt": "1778e4dcfcf9ac0bd3574fb3ff5248f2990265fa40d0822ff964ac67c434ae38",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(name: str, fields: list[str], content: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(content)


def relmax(actual, expected) -> float:
    a, b = np.asarray(actual, dtype=float), np.asarray(expected, dtype=float)
    return float(np.max(np.abs(a - b)) / max(1.0, float(np.max(np.abs(b)))))


def transform_metric(g, dg, ddg, j):
    return (
        np.einsum("ma,mn,nb->ab", j, g, j),
        np.einsum("ka,mb,nc,kmn->abc", j, j, j, dg),
        np.einsum("ka,lb,mc,nd,klmn->abcd", j, j, j, j, ddg),
    )


def transform_four(value, j):
    return np.einsum("ra,sb,uc,vd,rsuv->abcd", j, j, j, j, value)


def generator(name: str) -> np.ndarray:
    k = np.zeros((4, 4))
    if name == "K01":
        k[0, 1] = k[1, 0] = 1.0
    elif name == "K02":
        k[0, 2] = k[2, 0] = 1.0
    elif name == "K23":
        k[2, 3], k[3, 2] = -1.0, 1.0
    else:
        raise ValueError(name)
    return k


def coframe_metric(e, de, dde):
    g = e.T @ ETA @ e
    dg = np.array([de[k].T @ ETA @ e + e.T @ ETA @ de[k] for k in range(4)])
    ddg = np.array([[dde[k, l].T @ ETA @ e + de[k].T @ ETA @ de[l] + de[l].T @ ETA @ de[k] + e.T @ ETA @ dde[k, l] for l in range(4)] for k in range(4)])
    return g, dg, ddg


class D2:
    """Independent scalar second-jet algebra used for the split check."""

    def __init__(self, value, first=None, second=None):
        self.v = float(value)
        self.d = np.zeros(4) if first is None else np.asarray(first, dtype=float)
        self.dd = np.zeros((4, 4)) if second is None else np.asarray(second, dtype=float)

    def __add__(self, other):
        b = other if isinstance(other, D2) else D2(other)
        return D2(self.v + b.v, self.d + b.d, self.dd + b.dd)

    __radd__ = __add__

    def __neg__(self):
        return D2(-self.v, -self.d, -self.dd)

    def __sub__(self, other):
        return self + (-other if isinstance(other, D2) else -other)

    def __rsub__(self, other):
        return (-self) + other

    def __mul__(self, other):
        b = other if isinstance(other, D2) else D2(other)
        return D2(self.v * b.v, self.d * b.v + self.v * b.d, self.dd * b.v + self.v * b.dd + np.outer(self.d, b.d) + np.outer(b.d, self.d))

    __rmul__ = __mul__

    def reciprocal(self):
        return D2(1.0 / self.v, -self.d / self.v**2, 2.0 * np.outer(self.d, self.d) / self.v**3 - self.dd / self.v**2)

    def __truediv__(self, other):
        b = other if isinstance(other, D2) else D2(other)
        return self * b.reciprocal()


def dmat(g, dg, ddg, row_slice, col_slice):
    rs, cs = list(range(4))[row_slice], list(range(4))[col_slice]
    return [[D2(g[i, j], dg[:, i, j], ddg[:, :, i, j]) for j in cs] for i in rs]


def mmul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), D2(0.0)) for j in range(len(b[0]))] for i in range(len(a))]


def trans(a):
    return [list(x) for x in zip(*a)]


def independent_split(g, dg, ddg):
    q = dmat(g, dg, ddg, slice(2, 4), slice(2, 4))
    b = trans(dmat(g, dg, ddg, slice(0, 2), slice(2, 4)))
    q_values = np.array([[q[i][j].v for j in range(2)] for i in range(2)])
    qe = np.linalg.eigvalsh(q_values)
    if np.min(np.abs(qe)) <= ACTIVE_TOL:
        return {"status": "MARGINAL"}
    determinant = q[0][0] * q[1][1] - q[0][1] * q[1][0]
    qinv = [[q[1][1] / determinant, -q[0][1] / determinant], [-q[1][0] / determinant, q[0][0] / determinant]]
    a = mmul(qinv, b)
    correction = mmul(mmul(trans(b), qinv), b)
    gbb = dmat(g, dg, ddg, slice(0, 2), slice(0, 2))
    h = [[gbb[i][j] - correction[i][j] for j in range(2)] for i in range(2)]
    h_values = np.array([[h[i][j].v for j in range(2)] for i in range(2)])
    he = np.linalg.eigvalsh(h_values)
    if np.min(np.abs(he)) <= ACTIVE_TOL:
        return {"status": "MARGINAL"}
    if not (np.all(qe > ACTIVE_TOL) and he[0] < -ACTIVE_TOL and he[1] > ACTIVE_TOL):
        return {"status": "INVALID_SIGNATURE"}
    jets = [h[0][0], h[0][1], h[1][1], q[0][0], q[0][1], q[1][1], a[0][0], a[1][0], a[0][1], a[1][1]]
    values = np.array([x.v for x in jets])
    first = np.array([x.d for x in jets]).T
    second = np.transpose(np.array([x.dd for x in jets]), (1, 2, 0))
    rebuilt = metric_jets_from_split(values, first, second)
    forward = max(relmax(rebuilt.metric, g), relmax(rebuilt.first, dg), relmax(rebuilt.second, ddg))
    shear, twist = independent_kinematics(values, first)
    return {"status": "DEFINED", "values": values, "first": first, "second": second, "shear": shear, "twist": twist, "forward": forward}


def independent_kinematics(values, first):
    q = np.array([[values[3], values[4]], [values[4], values[5]]])
    a = np.array([[values[6], values[8]], [values[7], values[9]]])
    dq = np.array([[[first[k, 3], first[k, 4]], [first[k, 4], first[k, 5]]] for k in range(4)])
    da = np.array([[[first[k, 6], first[k, 8]], [first[k, 7], first[k, 9]]] for k in range(4)])
    twist = np.array([da[0, v, 1] - da[1, v, 0] - sum(a[o, 0] * da[2 + o, v, 1] for o in range(2)) + sum(a[o, 1] * da[2 + o, v, 0] for o in range(2)) for v in range(2)])
    inverse = np.linalg.inv(q)
    shears = []
    for i in range(2):
        horizontal = dq[i] - sum(a[v, i] * dq[2 + v] for v in range(2))
        vertical = np.array([[da[2 + derivative, output, i] for output in range(2)] for derivative in range(2)])
        deformation = 0.5 * (horizontal - vertical @ q - q @ vertical.T)
        shear = deformation - 0.5 * np.trace(inverse @ deformation) * q
        shears.append([shear[0, 0], shear[0, 1], shear[1, 1]])
    return np.asarray(shears), twist


def split_payload(split, name):
    if split["status"] != "DEFINED":
        return None
    if name == "split_slot_twojet":
        return np.concatenate((split["values"], split["first"].reshape(-1), split["second"].reshape(-1)))
    if name == "split_shear":
        return split["shear"].reshape(-1)
    return split["twist"].reshape(-1)


def must_fail(name, predicate, catch_rows):
    failed = False
    try:
        failed = not bool(predicate())
    except Exception:
        failed = True
    if not failed:
        raise AssertionError(f"catch proof did not reject: {name}")
    catch_rows.append({"catch_id": name, "result": "REJECTED_AS_REQUIRED"})


def main() -> None:
    check_count = 0
    check_categories = Counter()
    check_digest = hashlib.sha256()

    def check(name, condition):
        nonlocal check_count
        if not condition:
            raise AssertionError(name)
        check_count += 1
        check_categories[name.split("_", 1)[0]] += 1
        check_digest.update((name + "\n").encode())

    for path, expected in SOURCE_HASHES.items():
        check(f"source_{path}", digest(ROOT / path) == expected)
    check("preregistration", digest(HERE / "PREREGISTRATION.md") == "9f1d1efa85f1f534db25aeeccb1d51e4ca2033f76f1261b402d41df3b5e265ff")
    check("preregistration_correction", digest(HERE / "PREREGISTRATION_CORRECTION.md") == "c3ee82ce5603a8bfeabc653e56ab8664b17f1c7597ddfa9ec0a3fa69cc948454")

    registry = rows(HERE / "TRANSFORMATION_REGISTRY.tsv")
    check("transform_count", len(registry) == 12 and len({r["transform_id"] for r in registry}) == 12)
    transforms = {}
    for row in registry:
        matrix = np.asarray(json.loads(row["matrix_json"]), dtype=float)
        check(f"invertible_{row['transform_id']}", abs(np.linalg.det(matrix)) > 1e-12)
        if row["kind"] == "COFRAME":
            check(f"lorentz_{row['transform_id']}", relmax(matrix.T @ ETA @ matrix, ETA) <= TOL)
        transforms[row["transform_id"]] = {**row, "matrix": matrix}
    check("inverse_block", relmax(transforms["C01_BLOCK_GENERAL"]["matrix"] @ transforms["C02_BLOCK_GENERAL_INVERSE"]["matrix"], np.eye(4)) <= TOL)
    check("inverse_cross", relmax(transforms["C03_CROSS_GENERAL"]["matrix"] @ transforms["C04_CROSS_GENERAL_INVERSE"]["matrix"], np.eye(4)) <= TOL)

    config_shards, mobius_shards = rows(HERE / "CONFIGURATION_ORBIT_SHARDS.tsv"), rows(HERE / "MOBIUS_ORBIT_SHARDS.tsv")
    check("configuration_shards", len(config_shards) == 12 and sum(int(r["rows"]) for r in config_shards) == 73728)
    check("mobius_shards", len(mobius_shards) == 12 and sum(int(r["rows"]) for r in mobius_shards) == 69120)
    for shard in config_shards + mobius_shards:
        check(f"shard_hash_{shard['transform_id']}_{shard['path']}", digest(HERE / shard["path"]) == shard["sha256"])

    config_lookup, status_counts, split_counts = {}, defaultdict(Counter), defaultdict(Counter)
    for shard in config_shards:
        content = rows(HERE / shard["path"])
        check(f"config_rows_{shard['transform_id']}", len(content) == 6144)
        for row in content:
            key = (row["transform_id"], row["configuration_id"])
            check(f"config_unique_{len(config_lookup)}", key not in config_lookup)
            config_lookup[key] = row
            status_counts[row["transform_id"]][row["primary_status"]] += 1
            split_counts[row["transform_id"]][row["split_status"]] += 1
            check(f"retained_{len(config_lookup)}", row["retained"] == "YES")
            for field in ("metric_twojet_residual", "cartan_covariance_residual", "determinant_weight_residual", "ricci_contraction_residual", "scalar_contraction_residual", "inverse_roundtrip_residual"):
                check(f"residual_{len(config_lookup)}_{field}", float(row[field]) <= TOL)
    check("config_unique_total", len(config_lookup) == 73728)
    check("c06_invalid", split_counts["C06_SWAP_TIME_SCREEN"] == Counter({"INVALID_SIGNATURE": 6144}))
    check("other_splits_defined", all(split_counts[t] == Counter({"DEFINED": 6144}) for t in transforms if t != "C06_SWAP_TIME_SCREEN"))
    check("no_numeric_failures", sum(c["NUMERIC_COVARIANCE_FAILURE"] for c in status_counts.values()) == 0)

    interaction_lookup = {}
    for shard in mobius_shards:
        content = rows(HERE / shard["path"])
        check(f"mobius_rows_{shard['transform_id']}", len(content) == 5760)
        for row in content:
            key = (row["transform_id"], row["interaction_id"])
            check(f"mobius_unique_{len(interaction_lookup)}", key not in interaction_lookup)
            interaction_lookup[key] = row
            target = int(row["target_integer"])
            check(f"mobius_subsets_{len(interaction_lookup)}", len(row["subsets_used"].split(";")) == 2 ** target.bit_count())
            for name in FULL_TENSORS:
                check(f"tensor_defined_{len(interaction_lookup)}_{name}", row[f"{name}_domain"] == "DEFINED_COVARIANCE_CHECKED" and float(row[f"{name}_covariance_residual"]) <= TOL)
            for name in SPLIT_PAYLOADS:
                if row["transform_id"] == "C06_SWAP_TIME_SCREEN":
                    check(f"split_undefined_{len(interaction_lookup)}_{name}", row[f"{name}_domain"] == "UNDEFINED_SPLIT_DOMAIN" and row[f"{name}_l2"] == "")
                else:
                    check(f"split_defined_{len(interaction_lookup)}_{name}", row[f"{name}_domain"].startswith("DEFINED") and row[f"{name}_l2"] != "")
    check("mobius_unique_total", len(interaction_lookup) == 69120)

    ranks = rows(HERE / "TRANSFORMED_SPAN_RANKS.tsv")
    check("span_rows", len(ranks) == 1800)
    rank_lookup = {(r["transform_id"], int(r["target_integer"]), r["payload"]): r for r in ranks}
    for target in range(1, 16):
        for name in FULL_TENSORS:
            baseline = rank_lookup[("C00_IDENTITY", target, name)]["span_rank"]
            check(f"tensor_rank_invariant_{target}_{name}", all(rank_lookup[(t, target, name)]["span_rank"] == baseline for t in transforms))
        for name in SPLIT_PAYLOADS:
            baseline = rank_lookup[("C00_IDENTITY", target, name)]["span_rank"]
            check(f"coframe_split_rank_invariant_{target}_{name}", all(rank_lookup[(t, target, name)]["span_rank"] == baseline for t in transforms if t.startswith("F")))
            check(f"c06_split_rank_undefined_{target}_{name}", rank_lookup[("C06_SWAP_TIME_SCREEN", target, name)]["vectors_defined"] == "0" and rank_lookup[("C06_SWAP_TIME_SCREEN", target, name)]["span_rank"] == "")

    # Independent raw checks. Local Lorentz metric jets: every carrier/context at empty/full masks.
    raw_shards = rows(PARENT / "RAW_SHARD_REGISTRY.tsv")
    selected_for_split = {"R00_1", "V001"}
    selected_raw = {}
    coordinate_curvature_residual = 0.0
    local_metric_residual = 0.0
    independent_cartan_residual = 0.0
    independent_spin_residual = 0.0
    split_forward_residual = 0.0
    curvature_anchor_count = 0
    local_anchor_count = 0
    cartan_anchor_count = 0
    split_source_count = 0
    mutation_anchor = None
    for shard in raw_shards:
        with (PARENT / shard["path"]).open(encoding="utf-8") as handle:
            shard_raw = [json.loads(line) for line in handle]
        for raw in shard_raw:
            mask = int(raw["mask_integer"])
            g, dg, ddg = (np.asarray(raw[x], dtype=float) for x in ("metric", "metric_first", "metric_second"))
            e, de, dde = (np.asarray(raw[x], dtype=float) for x in ("coframe", "coframe_first", "coframe_second"))
            if mask in {0, 15}:
                base_coframe = evaluate_coframe_jets(e, de, dde)
                if mutation_anchor is None and raw["carrier_id"] == "R00_1" and mask == 15:
                    mutation_anchor = (raw, base_coframe)
                for identity, item in transforms.items():
                    if item["kind"] == "COFRAME":
                        lam = item["matrix"]
                        first = np.asarray(json.loads(item["parameter_first_json"]), dtype=float)
                        second = np.asarray(json.loads(item["parameter_second_json"]), dtype=float)
                        k = generator(item["generator"])
                        dlam = np.array([first[a] * k @ lam for a in range(4)])
                        ddlam = np.array([[second[a, b] * k @ lam + first[a] * first[b] * k @ k @ lam for b in range(4)] for a in range(4)])
                        et = lam @ e
                        det = np.array([dlam[a] @ e + lam @ de[a] for a in range(4)])
                        ddet = np.array([[ddlam[a, b] @ e + dlam[a] @ de[b] + dlam[b] @ de[a] + lam @ dde[a, b] for b in range(4)] for a in range(4)])
                        rebuilt = coframe_metric(et, det, ddet)
                        local_metric_residual = max(local_metric_residual, relmax(rebuilt[0], g), relmax(rebuilt[1], dg), relmax(rebuilt[2], ddg))
                        evaluated_coframe = evaluate_coframe_jets(et, det, ddet)
                        expected_cartan = np.einsum("ia,abuv,bj->ijuv", lam, base_coframe.cartan_curvature, np.linalg.inv(lam))
                        independent_cartan_residual = max(independent_cartan_residual, relmax(evaluated_coframe.cartan_curvature, expected_cartan))
                        expected_spin = np.array([lam @ base_coframe.spin_connection[mu] @ np.linalg.inv(lam) - dlam[mu] @ np.linalg.inv(lam) for mu in range(4)])
                        independent_spin_residual = max(independent_spin_residual, relmax(evaluated_coframe.spin_connection, expected_spin))
                        local_anchor_count += 1
                        cartan_anchor_count += 1
                if raw["carrier_id"] == "R00_1":
                    for identity, item in transforms.items():
                        if item["kind"] != "COORDINATE":
                            continue
                        j = item["matrix"]
                        gt, dgt, ddgt = transform_metric(g, dg, ddg, j)
                        evaluated = evaluate_metric_jets(MetricJets(gt, dgt, ddgt))
                        expected_r = transform_four(np.asarray(raw["riemann_down"]), j)
                        coordinate_curvature_residual = max(coordinate_curvature_residual, relmax(evaluated.riemann_down, expected_r))
                        et = e @ j
                        det = np.einsum("kb,kim,ma->bia", j, de, j)
                        ddet = np.einsum("kb,lc,klim,ma->bcia", j, j, dde, j)
                        coordinate_coframe = evaluate_coframe_jets(et, det, ddet)
                        expected_cartan = np.einsum("ua,vb,ijuv->ijab", j, j, base_coframe.cartan_curvature)
                        independent_cartan_residual = max(independent_cartan_residual, relmax(coordinate_coframe.cartan_curvature, expected_cartan))
                        independent = independent_split(gt, dgt, ddgt)
                        split_forward_residual = max(split_forward_residual, independent.get("forward", 0.0))
                        saved = config_lookup[(identity, raw["configuration_id"])]
                        check(f"anchor_split_status_{curvature_anchor_count}", saved["split_status"] == independent["status"])
                        curvature_anchor_count += 1
                        cartan_anchor_count += 1
            if raw["carrier_id"] in selected_for_split:
                key = (raw["bank"], raw["point_id"], raw["carrier_id"], mask)
                selected_raw[key] = (g, dg, ddg)
                split_source_count += 1
    check("local_anchor_count", local_anchor_count == 48 * 8 * 2 * 5)
    check("local_metric_invariance", local_metric_residual <= TOL)
    check("independent_spin_connection", independent_spin_residual <= TOL)
    check("coordinate_curvature_anchor_count", curvature_anchor_count == 1 * 8 * 2 * 7)
    check("coordinate_curvature_covariance", coordinate_curvature_residual <= TOL)
    check("independent_cartan_anchor_count", cartan_anchor_count == 48 * 8 * 2 * 5 + 1 * 8 * 2 * 7)
    check("independent_cartan_covariance", independent_cartan_residual <= TOL)
    check("independent_split_forward", split_forward_residual <= TOL)
    check("split_sources", split_source_count == 2 * 8 * 16)

    # Independently recompute the cross/reseated split interactions for all 192 registered anchors.
    split_interaction_checks = 0
    split_interaction_residual = 0.0
    for identity in ("C03_CROSS_GENERAL", "C04_CROSS_GENERAL_INVERSE", "C05_SWAP_DEPTH_SCREEN", "C06_SWAP_TIME_SCREEN"):
        j = transforms[identity]["matrix"]
        for bank, point in sorted({(key[0], key[1]) for key in selected_raw}):
            for carrier in sorted(selected_for_split):
                transformed = {}
                for mask in range(16):
                    g, dg, ddg = selected_raw[(bank, point, carrier, mask)]
                    transformed[mask] = independent_split(*transform_metric(g, dg, ddg, j))
                for target in (3, 5, 6, 7):
                    subsets = [s for s in range(16) if not s & ~target]
                    interaction_id = f"{carrier}_T{target:X}_{bank}_{point}"
                    saved = interaction_lookup[(identity, interaction_id)]
                    for name in SPLIT_PAYLOADS:
                        vertices = [split_payload(transformed[s], name) for s in subsets]
                        if any(v is None for v in vertices):
                            check(f"independent_split_undefined_{split_interaction_checks}", saved[f"{name}_domain"] == "UNDEFINED_SPLIT_DOMAIN")
                        else:
                            vector = sum(((-1) ** (target.bit_count() - s.bit_count())) * vertices[index] for index, s in enumerate(subsets))
                            split_interaction_residual = max(split_interaction_residual, abs(float(saved[f"{name}_l2"]) - float(np.linalg.norm(vector))) / max(1.0, float(np.linalg.norm(vector))), abs(float(saved[f"{name}_max_abs"]) - float(np.max(np.abs(vector)))) / max(1.0, float(np.max(np.abs(vector)))))
                        split_interaction_checks += 1
    check("split_interaction_check_count", split_interaction_checks == 4 * 8 * 2 * 4 * 3)
    check("split_interactions_independent", split_interaction_residual <= TOL)

    result = json.loads((HERE / "ATLAS_RESULT.json").read_text())
    check("maximum_conclusion", result["maximum_conclusion"] == MAXIMUM)
    check("result_counts", result["configuration_orbit_records"] == 73728 and result["interaction_orbit_records"] == 69120)
    check("result_no_failures", result["numeric_covariance_failures"] == 0 and result["discarded_records"] == 0)
    check("no_claim_escalation", not result["action_loaded"] and not result["full_group_exhaustiveness_claim"] and not result["split_selected_claim"])
    check("margin_ledger_complete", len(rows(HERE / "NUMERIC_MARGIN_LEDGER.tsv")) == 120)
    rank_margins = rows(HERE / "RANK_THRESHOLD_MARGIN_LEDGER.tsv")
    uncertain_rank_rows = [row for row in rank_margins if row["rank_margin_status"] == "NUMERIC_UNCERTAIN"]
    check("rank_margin_ledger_complete", len(rank_margins) == 1800)
    check("rank_margin_exact_uncertain_set", len(uncertain_rank_rows) == 1 and uncertain_rank_rows[0]["transform_id"] == "C05_SWAP_DEPTH_SCREEN" and uncertain_rank_rows[0]["target_mask"] == "M4" and uncertain_rank_rows[0]["payload"] == "split_slot_twojet" and uncertain_rank_rows[0]["span_rank"] == "130")

    catch_rows = []
    registry_gate = lambda data: len(data) == 12 and len({r["transform_id"] for r in data}) == 12
    must_fail("K01_MISSING_TRANSFORMATION", lambda: registry_gate(registry[:-1]), catch_rows)
    must_fail("K02_DUPLICATE_TRANSFORMATION", lambda: registry_gate(registry + [registry[0]]), catch_rows)
    singular = np.zeros((4, 4))
    must_fail("K03_SINGULAR_CHART", lambda: abs(np.linalg.det(singular)) > 1e-12, catch_rows)
    bad_lorentz = transforms["F01_CONSTANT_BASE_BOOST"]["matrix"].copy(); bad_lorentz[0, 0] += .01
    must_fail("K04_NON_LORENTZ_COFRAME", lambda: relmax(bad_lorentz.T @ ETA @ bad_lorentz, ETA) <= TOL, catch_rows)
    must_fail("K05_WRONG_INVERSE_PAIR", lambda: relmax(transforms["C01_BLOCK_GENERAL"]["matrix"] @ transforms["C04_CROSS_GENERAL_INVERSE"]["matrix"], np.eye(4)) <= TOL, catch_rows)
    raw_anchor, base_anchor = mutation_anchor
    e0, de0, dde0 = (np.asarray(raw_anchor[x], dtype=float) for x in ("coframe", "coframe_first", "coframe_second"))
    local_item = transforms["F02_LOCAL_BASE_BOOST"]
    local_lam = local_item["matrix"]
    mutated_constant = evaluate_coframe_jets(local_lam @ e0, np.array([local_lam @ de0[k] for k in range(4)]), np.array([[local_lam @ dde0[k, l] for l in range(4)] for k in range(4)]))
    local_first = np.asarray(json.loads(local_item["parameter_first_json"]), dtype=float)
    local_k = generator(local_item["generator"])
    local_dlam = np.array([local_first[a] * local_k @ local_lam for a in range(4)])
    correct_spin = np.array([local_lam @ base_anchor.spin_connection[mu] @ np.linalg.inv(local_lam) - local_dlam[mu] @ np.linalg.inv(local_lam) for mu in range(4)])
    must_fail("K06_OMITTED_LOCAL_DERIVATIVE", lambda: relmax(mutated_constant.spin_connection, correct_spin) <= TOL, catch_rows)
    anchor_g, anchor_dg, anchor_ddg = (np.asarray(raw_anchor[x], dtype=float) for x in ("metric", "metric_first", "metric_second"))
    anchor_r = np.asarray(raw_anchor["riemann_down"], dtype=float)
    anchor_j = transforms["C03_CROSS_GENERAL"]["matrix"]
    transformed_anchor = transform_metric(anchor_g, anchor_dg, anchor_ddg, anchor_j)
    actual_anchor_r = evaluate_metric_jets(MetricJets(*transformed_anchor)).riemann_down
    wrong_index_r = np.swapaxes(transform_four(anchor_r, anchor_j), 0, 1)
    must_fail("K07_TENSOR_INDEX_PERMUTATION", lambda: relmax(actual_anchor_r, wrong_index_r) <= TOL, catch_rows)
    c06_key = next(k for k in config_lookup if k[0] == "C06_SWAP_TIME_SCREEN")
    mutated_c06 = dict(config_lookup[c06_key]); mutated_c06["split_status"] = "DEFINED"
    must_fail("K08_INVALID_SPLIT_ACCEPTED", lambda: mutated_c06["split_status"] == "INVALID_SIGNATURE", catch_rows)
    c06_example = next(r for (t, _), r in interaction_lookup.items() if t == "C06_SWAP_TIME_SCREEN")
    imputed_c06 = dict(c06_example); imputed_c06["split_slot_twojet_l2"] = "0.0"
    must_fail("K09_UNDEFINED_SPLIT_IMPUTED", lambda: imputed_c06["split_slot_twojet_domain"] == "UNDEFINED_SPLIT_DOMAIN" and imputed_c06["split_slot_twojet_l2"] == "", catch_rows)
    parent_manifest = (ROOT / "udt_structural_ensemble_metric_atlas_2026-07-21/SHA256SUMS.txt").read_bytes()
    mutated_manifest = bytearray(parent_manifest); mutated_manifest[0] ^= 1
    source_gate = lambda data: hashlib.sha256(data).hexdigest() == SOURCE_HASHES["udt_structural_ensemble_metric_atlas_2026-07-21/SHA256SUMS.txt"]
    must_fail("K10_MUTATED_PARENT_INPUT", lambda: source_gate(bytes(mutated_manifest)), catch_rows)
    example = next(iter(interaction_lookup.values()))
    subset_gate = lambda row: row["target_mask"] == f"M{int(row['target_integer']):X}" and len(row["subsets_used"].split(";")) == 2 ** int(row["target_integer"]).bit_count()
    altered_mask = dict(example); altered_mask["target_integer"] = str((int(example["target_integer"]) % 15) + 1)
    must_fail("K11_ALTERED_ENSEMBLE_MASK", lambda: subset_gate(altered_mask), catch_rows)
    omitted_cube = dict(example); omitted_cube["subsets_used"] = ";".join(example["subsets_used"].split(";")[:-1])
    must_fail("K12_MOBIUS_CUBE_OMISSION", lambda: subset_gate(omitted_cube), catch_rows)
    rank_margin_gate = lambda data: len(data) == 1800 and sum(row["rank_margin_status"] == "NUMERIC_UNCERTAIN" for row in data) == 1
    must_fail("K13_THRESHOLD_MARGIN_OMISSION", lambda: rank_margin_gate([row for row in rank_margins if row is not uncertain_rank_rows[0]]), catch_rows)
    escalated = dict(result); escalated["maximum_conclusion"] = "FULL_GROUP_AND_PHYSICAL_SPLIT_SELECTED"
    must_fail("K14_CLAIM_ESCALATION", lambda: escalated["maximum_conclusion"] == MAXIMUM, catch_rows)
    write_tsv("CATCH_PROOFS.tsv", ["catch_id", "result"], catch_rows)

    verification = {
        "status": "PASS", "checks": check_count, "check_name_sha256": check_digest.hexdigest(),
        "check_category_counts": dict(sorted(check_categories.items())), "catch_proofs": len(catch_rows),
        "configuration_orbits": len(config_lookup), "interaction_orbits": len(interaction_lookup),
        "local_lorentz_anchor_checks": local_anchor_count, "coordinate_curvature_anchor_checks": curvature_anchor_count,
        "independent_split_interaction_checks": split_interaction_checks,
        "max_local_metric_residual": local_metric_residual, "max_coordinate_curvature_residual": coordinate_curvature_residual,
        "independent_cartan_anchor_checks": cartan_anchor_count,
        "max_independent_cartan_residual": independent_cartan_residual,
        "max_independent_spin_connection_residual": independent_spin_residual,
        "max_independent_split_forward_residual": split_forward_residual, "max_independent_split_interaction_residual": split_interaction_residual,
        "maximum_conclusion": MAXIMUM,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(verification, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    transcript = [
        "UDT_CHART_COFRAME_INVARIANCE_ATLAS_VERIFICATION=PASS",
        f"checks={check_count} catch_proofs={len(catch_rows)}",
        f"configuration_orbits={len(config_lookup)} interaction_orbits={len(interaction_lookup)}",
        f"local_lorentz_anchors={local_anchor_count} max_metric_residual={local_metric_residual:.17g}",
        f"coordinate_curvature_anchors={curvature_anchor_count} max_curvature_residual={coordinate_curvature_residual:.17g}",
        f"independent_cartan_anchors={cartan_anchor_count} max_cartan_residual={independent_cartan_residual:.17g} max_spin_residual={independent_spin_residual:.17g}",
        f"independent_split_interactions={split_interaction_checks} max_residual={split_interaction_residual:.17g}",
        f"maximum_conclusion={MAXIMUM}",
    ]
    (HERE / "VERIFICATION_TRANSCRIPT.txt").write_text("\n".join(transcript) + "\n", encoding="utf-8")
    print("\n".join(transcript))


if __name__ == "__main__":
    main()

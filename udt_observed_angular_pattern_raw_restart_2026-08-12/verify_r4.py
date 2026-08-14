#!/usr/bin/env python3
"""Independent full replay of the preregistered R4 empirical relation atlas."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy import linalg, signal


NBIN = 119
LANES = ("W0_UNIT", "W1_SPECTRO", "W2_IMAGING", "W3_OFFICIAL_OBS")
RATIOS = (5, 10, 20)
NSIDES = (4, 8, 16)
EXPECTED_COUNTS = {
    "RANDOM_DENSITY": 1552,
    "WEIGHT_LANE": 1746,
    "CAP": 1164,
    "ADJACENT_SHELL": 2184,
    "COARSE_FINE_CONTAINMENT": 2640,
}
REL_METRICS = (
    "raw_rms_difference", "raw_max_abs_difference", "raw_relative_l2",
    "centered_rms_difference", "centered_relative_l2", "centered_cosine",
    "difference_rms_difference", "difference_relative_l2", "difference_cosine",
)
CAP_METRICS = (
    "rank", "positive_condition", "difference_rms", "covariance_rms_scale",
    "difference_to_covariance_rms", "range_fraction", "unresolved_fraction",
    "range_quadratic_per_rank", "diagonal_standardized_rms",
)
QUANTILES = np.array([0.0, 0.25, 0.5, 0.75, 0.9, 0.95, 1.0], dtype=np.float64)
Q_NAMES = ("min", "q25", "median", "q75", "q90", "q95", "max")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_tsv(path: Path) -> list[dict]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def parse_endpoint(text: str) -> tuple:
    sample, cap, factor, group, lane, ratio = text.split("|")
    return sample, cap, int(factor), int(group), lane, int(ratio)


def load_parent_curves(path: Path):
    grouped = defaultdict(list)
    with path.open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            key = (
                row["sample"], row["cap"], int(row["factor"]), int(row["group"]),
                row["lane"], int(row["ratio"]),
            )
            grouped[key].append(row)
    assert len(grouped) == 2328
    curves = {}
    meta = {}
    edges0 = None
    for key, rows in grouped.items():
        ordered = sorted(rows, key=lambda row: float(row["theta_lo_deg"]))
        assert len(ordered) == NBIN
        edges = tuple((float(row["theta_lo_deg"]), float(row["theta_hi_deg"])) for row in ordered)
        if edges0 is None:
            edges0 = edges
        else:
            assert edges == edges0
        curve = np.fromiter((float(row["w_theta"]) for row in ordered), dtype=np.float64, count=NBIN)
        assert np.isfinite(curve).all()
        curves[key] = curve
        first = ordered[0]
        meta[key] = (float(first["z_lo"]), float(first["z_hi"]))
    return curves, meta, np.asarray(edges0, dtype=np.float64)


def enumerate_relations(curves: dict, meta: dict) -> list[tuple[str, tuple, tuple]]:
    selections = sorted({key[:4] for key in curves})
    selection_set = set(selections)
    out = []
    for sel in selections:
        for lane in LANES:
            out.extend([
                ("RANDOM_DENSITY", sel + (lane, 5), sel + (lane, 20)),
                ("RANDOM_DENSITY", sel + (lane, 10), sel + (lane, 20)),
            ])
    for sel in selections:
        for ratio in RATIOS:
            for lane in LANES[1:]:
                out.append(("WEIGHT_LANE", sel + (LANES[0], ratio), sel + (lane, ratio)))
    for sample, factor, group in sorted({(s, f, g) for s, _, f, g in selections}):
        n = (sample, "North", factor, group)
        s = (sample, "South", factor, group)
        if n in selection_set and s in selection_set:
            for lane in LANES:
                for ratio in RATIOS:
                    out.append(("CAP", n + (lane, ratio), s + (lane, ratio)))
    adjacency = defaultdict(list)
    for sample, cap, factor, group in selections:
        adjacency[(sample, cap, factor)].append(group)
    for (sample, cap, factor), groups in sorted(adjacency.items()):
        groups = sorted(groups)
        for left, right in zip(groups[:-1], groups[1:]):
            for lane in LANES:
                for ratio in RATIOS:
                    out.append((
                        "ADJACENT_SHELL",
                        (sample, cap, factor, left, lane, ratio),
                        (sample, cap, factor, right, lane, ratio),
                    ))
    base = {key[:4]: value for key, value in meta.items() if key[4:] == (LANES[0], 20)}
    links = []
    for parent, (plo, phi) in sorted(base.items()):
        if parent[2] not in (2, 4):
            continue
        for child, (clo, chi) in sorted(base.items()):
            if child[:2] == parent[:2] and child[2] == 1 and clo >= plo - 1e-12 and chi <= phi + 1e-12:
                links.append((child, parent))
    assert len(links) == 220
    for child, parent in links:
        for lane in LANES:
            for ratio in RATIOS:
                out.append(("COARSE_FINE_CONTAINMENT", child + (lane, ratio), parent + (lane, ratio)))
    assert Counter(kind for kind, _, _ in out) == Counter(EXPECTED_COUNTS)
    assert len(out) == 9286
    return out


def relation_values(a: np.ndarray, b: np.ndarray):
    delta = b - a
    ac = a - a.sum(dtype=np.float64) / a.size
    bc = b - b.sum(dtype=np.float64) / b.size
    da = a[1:] - a[:-1]
    db = b[1:] - b[:-1]
    dac = da - da.sum(dtype=np.float64) / da.size
    dbc = db - db.sum(dtype=np.float64) / db.size

    def rel_and_cos(x, y):
        nx2 = float(x @ x); ny2 = float(y @ y)
        rel_denom = math.sqrt(nx2 + ny2)
        cos_denom = math.sqrt(nx2 * ny2)
        rel = math.sqrt(float((y - x) @ (y - x))) / rel_denom if rel_denom else 0.0
        cosine = float(x @ y) / cos_denom if cos_denom else 0.0
        return rel, cosine

    raw_rel, _ = rel_and_cos(a, b)
    centered_rel, centered_cos = rel_and_cos(ac, bc)
    diff_rel, diff_cos = rel_and_cos(da, db)
    values = {
        "raw_rms_difference": math.sqrt(float(delta @ delta) / delta.size),
        "raw_max_abs_difference": float(np.abs(delta).max()),
        "raw_relative_l2": raw_rel,
        "centered_rms_difference": math.sqrt(float((bc - ac) @ (bc - ac)) / ac.size),
        "centered_relative_l2": centered_rel,
        "centered_cosine": centered_cos,
        "difference_rms_difference": math.sqrt(float((db - da) @ (db - da)) / da.size),
        "difference_relative_l2": diff_rel,
        "difference_cosine": diff_cos,
    }
    return values, ac, bc, dac, dbc


def cell_path(root: Path, key: str) -> Path:
    candidates = [root / f"{key}.npz", root / f"R3_{key}.npz"]
    found = [path for path in candidates if path.is_file()]
    assert len(found) == 1, (key, found)
    return found[0]


def selection_name(sample: str, cap: str, factor: int, group: int) -> str:
    return f"{sample}_{cap}_f{factor}_g{group:02d}"


def independent_cap_values(nc, sc, lane_index: int, nside: int, d: np.ndarray):
    cn = np.asarray(nc[f"covariance_n{nside}"][lane_index], dtype=np.float64)
    cs = np.asarray(sc[f"covariance_n{nside}"][lane_index], dtype=np.float64)
    matrix = (cn + cs + cn.T + cs.T) / 2.0
    eig, vec = linalg.eigh(matrix, driver="evr", check_finite=True)
    tau = NBIN * np.finfo(np.float64).eps * float(eig[-1])
    assert float(eig[0]) >= -100.0 * tau
    mask = eig > tau
    rank = int(mask.sum())
    coeff = vec[:, mask].T @ d
    d2 = float(d @ d)
    r2 = float(coeff @ coeff)
    rf = float(np.clip(r2 / d2 if d2 else 1.0, 0.0, 1.0))
    q = float(np.sum((coeff * coeff) / eig[mask]))
    diag = np.diag(matrix)
    dm = diag > tau
    cov_rms = math.sqrt(float(diag.sum()) / NBIN)
    diff_rms = math.sqrt(d2 / NBIN)
    return {
        "rank": rank,
        "rank_tau": tau,
        "positive_condition": float(eig[-1] / eig[mask][0]),
        "difference_rms": diff_rms,
        "covariance_rms_scale": cov_rms,
        "difference_to_covariance_rms": diff_rms / cov_rms,
        "range_fraction": rf,
        "unresolved_fraction": 1.0 - rf,
        "range_quadratic_per_rank": q / rank,
        "diagonal_standardized_rms": math.sqrt(float(np.sum((d[dm] ** 2) / diag[dm])) / int(dm.sum())),
        "resolved_diagonal_bins": int(dm.sum()),
        "eigen_min": float(eig[0]),
        "eigen_max": float(eig[-1]),
    }


def assert_close(actual: float, expected: float, label: str, atol=2e-12, rtol=2e-10):
    if not math.isclose(actual, expected, abs_tol=atol, rel_tol=rtol):
        raise AssertionError(f"{label}: {actual} != {expected}")


def verify_manifest(package: Path):
    rows = read_tsv(package / "R4_OUTPUT_MANIFEST.tsv")
    assert len(rows) == 5
    for row in rows:
        path = package / row["artifact"]
        assert path.stat().st_size == int(row["bytes"])
        assert sha256(path) == row["sha256"]


def verify_summaries(package: Path, relation_rows: list[dict], cap_rows: list[dict]):
    saved = read_tsv(package / "R4_SUMMARY.tsv")
    expected = {}
    rel_groups = defaultdict(list)
    for row in relation_rows:
        rel_groups[("relation_type", row["relation_type"])].append(row)
        rel_groups[("relation_type_sample_factor", f"{row['relation_type']}|{row['sample']}|{row['factor_pair']}")].append(row)
    for (grouping, key), rows in rel_groups.items():
        for metric in REL_METRICS:
            expected[("RELATION", grouping, key, metric)] = np.quantile(
                np.array([float(row[metric]) for row in rows]), QUANTILES
            )
    cap_groups = defaultdict(list)
    for row in cap_rows:
        cap_groups[("nside", f"n{row['nside']}")].append(row)
        cap_groups[("nside_sample_factor_lane", f"n{row['nside']}|{row['sample']}|f{row['factor']}|{row['lane']}")].append(row)
    for (grouping, key), rows in cap_groups.items():
        for metric in CAP_METRICS:
            expected[("CAP_COVARIANCE", grouping, key, metric)] = np.quantile(
                np.array([float(row[metric]) for row in rows]), QUANTILES
            )
    assert len(saved) == len(expected)
    for row in saved:
        key = (row["surface"], row["grouping"], row["group_key"], row["metric"])
        q = expected.pop(key)
        for name, value in zip(Q_NAMES, q):
            assert_close(float(row[name]), float(value), f"summary {key}/{name}", atol=2e-13, rtol=2e-12)
    assert not expected


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-dir", type=Path, default=here)
    parser.add_argument(
        "--r3-cells", type=Path,
        default=Path("/media/udt-admin/ScratchDisk/Data/UDT_BOSS_R3_2026-08-14/R3_COVARIANCE_CELLS"),
    )
    parser.add_argument("--output", type=Path, default=here / "R4_VERIFICATION_RESULT.json")
    args = parser.parse_args()
    package = args.package_dir.resolve()
    cells = args.r3_cells.resolve()

    verify_manifest(package)
    curves, meta, theta_edges = load_parent_curves(package / "R2_CURVE_ATLAS.tsv")
    expected_relations = enumerate_relations(curves, meta)
    relation_rows = read_tsv(package / "R4_RELATION_ATLAS.tsv")
    assert len(relation_rows) == len(expected_relations)
    lag = np.load(package / "R4_CROSS_LAG_ATLAS.npz", allow_pickle=False)
    assert lag["raw_centered_cross_correlation"].shape == (9286, 237)
    assert lag["difference_centered_cross_correlation"].shape == (9286, 235)
    assert np.array_equal(lag["relation_id"], np.arange(9286, dtype=np.int32))
    assert np.array_equal(lag["raw_lag_bins"], np.arange(-118, 119, dtype=np.int16))
    assert np.array_equal(lag["difference_lag_bins"], np.arange(-117, 118, dtype=np.int16))
    assert np.array_equal(lag["theta_edges_deg"], theta_edges)

    max_relation_abs = 0.0
    max_lag_abs = 0.0
    raw_a = np.empty((9286, NBIN), dtype=np.float64)
    raw_b = np.empty((9286, NBIN), dtype=np.float64)
    diff_a = np.empty((9286, NBIN - 1), dtype=np.float64)
    diff_b = np.empty((9286, NBIN - 1), dtype=np.float64)
    for index, (row, expected) in enumerate(zip(relation_rows, expected_relations)):
        kind, akey, bkey = expected
        assert int(row["relation_id"]) == index
        assert row["relation_type"] == kind
        assert parse_endpoint(row["curve_a"]) == akey
        assert parse_endpoint(row["curve_b"]) == bkey
        values, ac, bc, dac, dbc = relation_values(curves[akey], curves[bkey])
        raw_a[index] = ac; raw_b[index] = bc
        diff_a[index] = dac; diff_b[index] = dbc
        for metric, expected_value in values.items():
            saved = float(row[metric])
            max_relation_abs = max(max_relation_abs, abs(saved - expected_value))
            assert_close(saved, expected_value, f"relation {index}/{metric}", atol=3e-14, rtol=3e-13)
    raw_conv = signal.fftconvolve(raw_a, raw_b[:, ::-1], mode="full", axes=1)
    diff_conv = signal.fftconvolve(diff_a, diff_b[:, ::-1], mode="full", axes=1)
    raw_denom = np.linalg.norm(raw_a, axis=1) * np.linalg.norm(raw_b, axis=1)
    diff_denom = np.linalg.norm(diff_a, axis=1) * np.linalg.norm(diff_b, axis=1)
    raw_replay = np.divide(raw_conv, raw_denom[:, None], out=np.zeros_like(raw_conv),
                           where=raw_denom[:, None] > 0)
    diff_replay = np.divide(diff_conv, diff_denom[:, None], out=np.zeros_like(diff_conv),
                            where=diff_denom[:, None] > 0)
    raw_saved = lag["raw_centered_cross_correlation"]
    diff_saved = lag["difference_centered_cross_correlation"]
    max_lag_abs = max(float(np.max(np.abs(raw_saved - raw_replay))),
                      float(np.max(np.abs(diff_saved - diff_replay))))
    if not np.allclose(raw_saved, raw_replay, rtol=2e-12, atol=2e-13):
        raise AssertionError("raw cross-lag replay mismatch")
    if not np.allclose(diff_saved, diff_replay, rtol=2e-12, atol=2e-13):
        raise AssertionError("difference cross-lag replay mismatch")
    lag.close()

    cap_rows = read_tsv(package / "R4_CAP_COVARIANCE_ATLAS.tsv")
    assert len(cap_rows) == 1164
    seen = set()
    max_cap_abs = 0.0
    max_projector_abs_difference = 0.0
    max_projector_tolerance_bound = 0.0
    max_projector_abs_by_field = {
        "range_fraction": 0.0,
        "unresolved_fraction": 0.0,
        "range_quadratic_per_rank": 0.0,
    }
    max_projector_tolerance_by_field = {
        "range_fraction": 0.0,
        "unresolved_fraction": 0.0,
        "range_quadratic_per_rank": 0.0,
    }
    max_positive_condition_abs_difference = 0.0
    cap_by_selection = defaultdict(list)
    for row in cap_rows:
        cap_by_selection[(row["sample"], int(row["factor"]), int(row["group"]))].append(row)
    assert len(cap_by_selection) == 97
    for (sample, factor, group), selection_rows in sorted(cap_by_selection.items()):
        nsel = selection_name(sample, "North", factor, group)
        ssel = selection_name(sample, "South", factor, group)
        assert len(selection_rows) == 12
        with np.load(cell_path(cells, nsel), allow_pickle=False) as nc, np.load(cell_path(cells, ssel), allow_pickle=False) as sc:
            assert json.loads(str(nc["metadata"].item()))["selection_key"] == nsel
            assert json.loads(str(sc["metadata"].item()))["selection_key"] == ssel
            for row in selection_rows:
                lane = row["lane"]; nside = int(row["nside"]); lane_index = LANES.index(lane)
                key = (sample, factor, group, lane, nside)
                assert key not in seen
                seen.add(key)
                assert row["north_selection"] == nsel and row["south_selection"] == ssel
                nkey = (sample, "North", factor, group, lane, 20)
                skey = (sample, "South", factor, group, lane, 20)
                values = independent_cap_values(nc, sc, lane_index, nside, curves[nkey] - curves[skey])
                for metric, expected_value in values.items():
                    saved = float(row[metric])
                    max_cap_abs = max(max_cap_abs, abs(saved - float(expected_value)))
                    if metric in {"range_fraction", "unresolved_fraction", "range_quadratic_per_rank"}:
                        projector_bound = max(
                            3e-10,
                            2048.0 * np.finfo(np.float64).eps * values["positive_condition"],
                        )
                        max_projector_abs_difference = max(
                            max_projector_abs_difference, abs(saved - float(expected_value))
                        )
                        max_projector_abs_by_field[metric] = max(
                            max_projector_abs_by_field[metric], abs(saved - float(expected_value))
                        )
                        max_projector_tolerance_bound = max(
                            max_projector_tolerance_bound, projector_bound
                        )
                        max_projector_tolerance_by_field[metric] = max(
                            max_projector_tolerance_by_field[metric], projector_bound
                        )
                        projector_atol = projector_bound if metric != "range_quadratic_per_rank" else 3e-12
                        assert_close(saved, float(expected_value), f"cap {key}/{metric}",
                                     atol=projector_atol, rtol=projector_bound)
                    elif metric == "positive_condition":
                        condition_bound = max(
                            3e-10,
                            2048.0 * np.finfo(np.float64).eps * values["positive_condition"],
                        )
                        max_positive_condition_abs_difference = max(
                            max_positive_condition_abs_difference, abs(saved - float(expected_value))
                        )
                        assert_close(saved, float(expected_value), f"cap {key}/{metric}",
                                     atol=3e-12, rtol=condition_bound)
                    else:
                        assert_close(saved, float(expected_value), f"cap {key}/{metric}",
                                     atol=3e-12, rtol=3e-10)
    assert len(seen) == 1164
    verify_summaries(package, relation_rows, cap_rows)

    result = json.loads((package / "R4_RESULT.json").read_text())
    assert result["status"] == "ASSEMBLED__INDEPENDENT_VERIFICATION_PENDING"
    assert result["relation_count"] == 9286 and result["cap_covariance_record_count"] == 1164
    payload = {
        "status": "PASS",
        "verifier": "independent scipy-FFT/scipy-eigh full replay",
        "relation_count": 9286,
        "cap_covariance_record_count": 1164,
        "summary_record_count": len(read_tsv(package / "R4_SUMMARY.tsv")),
        "max_relation_descriptor_abs_difference": max_relation_abs,
        "max_cross_lag_abs_difference": max_lag_abs,
        "max_cap_descriptor_abs_difference": max_cap_abs,
        "max_range_projector_abs_difference": max_projector_abs_difference,
        "max_condition_aware_projector_tolerance_bound": max_projector_tolerance_bound,
        "max_range_projector_abs_difference_by_field": max_projector_abs_by_field,
        "max_condition_aware_projector_tolerance_bound_by_field": max_projector_tolerance_by_field,
        "max_positive_condition_abs_difference": max_positive_condition_abs_difference,
        "scope": "bounded R4 data-only relation/covariance atlas; no physical interpretation",
    }
    if args.output.exists():
        raise FileExistsError(args.output)
    tmp = args.output.with_suffix(args.output.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(tmp, args.output)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

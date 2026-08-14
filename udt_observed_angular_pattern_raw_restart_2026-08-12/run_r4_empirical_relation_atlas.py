#!/usr/bin/env python3
"""Assemble the preregistered R4 data-only empirical relation atlas."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np


NBIN = 119
LANES = ("W0_UNIT", "W1_SPECTRO", "W2_IMAGING", "W3_OFFICIAL_OBS")
RATIOS = (5, 10, 20)
NSIDES = (4, 8, 16)
RELATION_COUNTS = {
    "RANDOM_DENSITY": 1552,
    "WEIGHT_LANE": 1746,
    "CAP": 1164,
    "ADJACENT_SHELL": 2184,
    "COARSE_FINE_CONTAINMENT": 2640,
}
EXPECTED_PARENT_HASHES = {
    "R2_CURVE_ATLAS.tsv": "32b592a85cbadbc080391353be6d0ee73a2d0d8a37c10aead28e041a7810f603",
    "R2_OUTPUT_MANIFEST.tsv": "6eb143be6c41d4047eab1714de322ce15b8530646456cb6bc0ed43f237333031",
    "R3_OUTPUT_MANIFEST.tsv": "3a38784ac248997bd987598308b98edbf60566759e4fdc35d54d98b161a11cfa",
    "R3_FINAL_EVIDENCE_MANIFEST.tsv": "7c609d70b1d55122885c58705dcef9eeb81ca6ded17ec0d550985bd5ecc1913e",
}
OUTPUTS = (
    "R4_RELATION_ATLAS.tsv",
    "R4_CROSS_LAG_ATLAS.npz",
    "R4_CAP_COVARIANCE_ATLAS.tsv",
    "R4_SUMMARY.tsv",
    "R4_RESULT.json",
    "R4_OUTPUT_MANIFEST.tsv",
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def atomic_tsv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    if path.exists():
        raise FileExistsError(path)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    os.replace(tmp, path)


def atomic_json(path: Path, payload: dict) -> None:
    if path.exists():
        raise FileExistsError(path)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(tmp, path)


def atomic_npz(path: Path, **arrays) -> None:
    if path.exists():
        raise FileExistsError(path)
    with tempfile.NamedTemporaryFile(dir=path.parent, suffix=".npz", delete=False) as handle:
        tmp = Path(handle.name)
    try:
        np.savez_compressed(tmp, **arrays)
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()


def finite_float(value: float) -> float:
    out = float(value)
    if not math.isfinite(out):
        raise ArithmeticError(f"nonfinite descriptor {out}")
    return out


def curve_key(row: dict) -> tuple:
    return (
        row["sample"], row["cap"], int(row["factor"]), int(row["group"]),
        row["lane"], int(row["ratio"]),
    )


def selection_key(key: tuple) -> str:
    sample, cap, factor, group, _, _ = key
    return f"{sample}_{cap}_f{factor}_g{group:02d}"


def load_curves(path: Path):
    buckets: dict[tuple, list[dict]] = defaultdict(list)
    with path.open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            buckets[curve_key(row)].append(row)
    if len(buckets) != 2328:
        raise ArithmeticError(f"expected 2328 curves, found {len(buckets)}")

    curves: dict[tuple, np.ndarray] = {}
    meta: dict[tuple, dict] = {}
    reference_edges = None
    for key, rows in buckets.items():
        rows.sort(key=lambda r: float(r["theta_lo_deg"]))
        if len(rows) != NBIN:
            raise ArithmeticError(f"{key}: expected {NBIN} bins, found {len(rows)}")
        edges = tuple((float(r["theta_lo_deg"]), float(r["theta_hi_deg"])) for r in rows)
        if reference_edges is None:
            reference_edges = edges
        elif edges != reference_edges:
            raise ArithmeticError(f"angular-bin mismatch for {key}")
        values = np.array([float(r["w_theta"]) for r in rows], dtype=np.float64)
        if not np.all(np.isfinite(values)):
            raise ArithmeticError(f"nonfinite curve {key}")
        curves[key] = values
        first = rows[0]
        meta[key] = {
            "sample": first["sample"], "cap": first["cap"],
            "factor": int(first["factor"]), "group": int(first["group"]),
            "z_lo": float(first["z_lo"]), "z_hi": float(first["z_hi"]),
            "lane": first["lane"], "ratio": int(first["ratio"]),
        }
    return curves, meta, np.asarray(reference_edges, dtype=np.float64)


def build_relations(curves: dict, meta: dict) -> list[tuple[str, tuple, tuple]]:
    relations: list[tuple[str, tuple, tuple]] = []
    selection_axes = sorted({key[:4] for key in curves})

    for sel in selection_axes:
        for lane in LANES:
            relations.append(("RANDOM_DENSITY", sel + (lane, 5), sel + (lane, 20)))
            relations.append(("RANDOM_DENSITY", sel + (lane, 10), sel + (lane, 20)))

    for sel in selection_axes:
        for ratio in RATIOS:
            for lane in LANES[1:]:
                relations.append(("WEIGHT_LANE", sel + (LANES[0], ratio), sel + (lane, ratio)))

    cap_axes = sorted({(s, f, g) for s, _, f, g in selection_axes})
    selection_set = set(selection_axes)
    for sample, factor, group in cap_axes:
        north = (sample, "North", factor, group)
        south = (sample, "South", factor, group)
        if north not in selection_set or south not in selection_set:
            continue
        for lane in LANES:
            for ratio in RATIOS:
                relations.append(("CAP", north + (lane, ratio), south + (lane, ratio)))

    grouped: dict[tuple, list[int]] = defaultdict(list)
    for sample, cap, factor, group in selection_axes:
        grouped[(sample, cap, factor)].append(group)
    for (sample, cap, factor), groups in sorted(grouped.items()):
        ordered = sorted(groups)
        for g_a, g_b in zip(ordered[:-1], ordered[1:]):
            for lane in LANES:
                for ratio in RATIOS:
                    relations.append((
                        "ADJACENT_SHELL",
                        (sample, cap, factor, g_a, lane, ratio),
                        (sample, cap, factor, g_b, lane, ratio),
                    ))

    coarse_links = []
    base_meta = {key[:4]: value for key, value in meta.items() if key[4:] == (LANES[0], 20)}
    for coarse, cm in sorted(base_meta.items()):
        if coarse[2] == 1:
            continue
        for fine, fm in sorted(base_meta.items()):
            if fine[:2] != coarse[:2] or fine[2] != 1:
                continue
            if fm["z_lo"] >= cm["z_lo"] - 1e-12 and fm["z_hi"] <= cm["z_hi"] + 1e-12:
                coarse_links.append((fine, coarse))
    if len(coarse_links) != 220:
        raise ArithmeticError(f"expected 220 coarse/fine links, found {len(coarse_links)}")
    for fine, coarse in coarse_links:
        for lane in LANES:
            for ratio in RATIOS:
                relations.append((
                    "COARSE_FINE_CONTAINMENT",
                    fine + (lane, ratio), coarse + (lane, ratio),
                ))

    counts = Counter(kind for kind, _, _ in relations)
    if counts != Counter(RELATION_COUNTS) or len(relations) != 9286:
        raise ArithmeticError(f"relation census mismatch: {counts}, total={len(relations)}")
    for _, a, b in relations:
        if a not in curves or b not in curves:
            raise KeyError(f"missing relation endpoint {a} -> {b}")
    return relations


def norm_descriptors(a: np.ndarray, b: np.ndarray) -> tuple[dict, np.ndarray, np.ndarray, int, int]:
    delta = b - a
    ac = a - np.mean(a)
    bc = b - np.mean(b)
    da = np.diff(a)
    db = np.diff(b)
    dac = da - np.mean(da)
    dbc = db - np.mean(db)

    def relation(x, y):
        nx = float(np.linalg.norm(x)); ny = float(np.linalg.norm(y))
        denom_rel = math.sqrt(nx * nx + ny * ny)
        denom_cos = nx * ny
        rel = float(np.linalg.norm(y - x) / denom_rel) if denom_rel > 0 else 0.0
        cos = float(np.dot(x, y) / denom_cos) if denom_cos > 0 else 0.0
        return rel, cos, int(denom_cos == 0)

    raw_rel, _, raw_deg = relation(a, b)
    centered_rel, centered_cos, centered_deg = relation(ac, bc)
    diff_rel, diff_cos, diff_deg = relation(da, db)
    values = {
        "raw_rms_difference": float(np.sqrt(np.mean(delta * delta))),
        "raw_max_abs_difference": float(np.max(np.abs(delta))),
        "raw_relative_l2": raw_rel,
        "centered_rms_difference": float(np.sqrt(np.mean((bc - ac) ** 2))),
        "centered_relative_l2": centered_rel,
        "centered_cosine": centered_cos,
        "difference_rms_difference": float(np.sqrt(np.mean((db - da) ** 2))),
        "difference_relative_l2": diff_rel,
        "difference_cosine": diff_cos,
        "raw_rms_a": float(np.sqrt(np.mean(a * a))),
        "raw_rms_b": float(np.sqrt(np.mean(b * b))),
        "centered_rms_a": float(np.sqrt(np.mean(ac * ac))),
        "centered_rms_b": float(np.sqrt(np.mean(bc * bc))),
        "raw_degenerate": raw_deg,
        "centered_degenerate": centered_deg,
        "difference_degenerate": diff_deg,
    }
    for key, value in values.items():
        if not key.endswith("degenerate"):
            finite_float(value)

    raw_norm = float(np.linalg.norm(ac) * np.linalg.norm(bc))
    diff_norm = float(np.linalg.norm(dac) * np.linalg.norm(dbc))
    raw_xcorr = np.correlate(ac, bc, mode="full") / raw_norm if raw_norm > 0 else np.zeros(237)
    diff_xcorr = np.correlate(dac, dbc, mode="full") / diff_norm if diff_norm > 0 else np.zeros(235)
    if raw_xcorr.shape != (237,) or diff_xcorr.shape != (235,):
        raise ArithmeticError("cross-lag shape failure")
    if not np.all(np.isfinite(raw_xcorr)) or not np.all(np.isfinite(diff_xcorr)):
        raise ArithmeticError("nonfinite cross-lag array")
    return values, raw_xcorr, diff_xcorr, int(raw_norm == 0), int(diff_norm == 0)


def relation_factor_pair(kind: str, ma: dict, mb: dict) -> str:
    return f"{ma['factor']}->{mb['factor']}" if ma["factor"] != mb["factor"] else str(ma["factor"])


def assemble_relations(curves, meta, relations):
    rows = []
    raw_lags = np.empty((len(relations), 237), dtype=np.float64)
    diff_lags = np.empty((len(relations), 235), dtype=np.float64)
    for index, (kind, akey, bkey) in enumerate(relations):
        ma, mb = meta[akey], meta[bkey]
        values, rx, dx, raw_lag_deg, diff_lag_deg = norm_descriptors(curves[akey], curves[bkey])
        raw_lags[index] = rx
        diff_lags[index] = dx
        row = {
            "relation_id": index,
            "relation_type": kind,
            "curve_a": "|".join(map(str, akey)),
            "curve_b": "|".join(map(str, bkey)),
            "sample": ma["sample"],
            "cap_a": ma["cap"], "cap_b": mb["cap"],
            "factor_a": ma["factor"], "group_a": ma["group"],
            "factor_b": mb["factor"], "group_b": mb["group"],
            "factor_pair": relation_factor_pair(kind, ma, mb),
            "z_lo_a": format(ma["z_lo"], ".17g"), "z_hi_a": format(ma["z_hi"], ".17g"),
            "z_lo_b": format(mb["z_lo"], ".17g"), "z_hi_b": format(mb["z_hi"], ".17g"),
            "lane_a": ma["lane"], "lane_b": mb["lane"],
            "ratio_a": ma["ratio"], "ratio_b": mb["ratio"],
            **{key: (format(value, ".17g") if isinstance(value, float) else value)
               for key, value in values.items()},
            "raw_lag_degenerate": raw_lag_deg,
            "difference_lag_degenerate": diff_lag_deg,
        }
        rows.append(row)
    return rows, raw_lags, diff_lags


def cell_path(root: Path, sel_key: str) -> Path:
    candidates = (root / f"{sel_key}.npz", root / f"R3_{sel_key}.npz")
    found = [path for path in candidates if path.is_file()]
    if len(found) != 1:
        raise FileNotFoundError(f"expected one R3 cell for {sel_key}, found {found}")
    return found[0]


def load_cell(root: Path, sel_key: str):
    path = cell_path(root, sel_key)
    handle = np.load(path, allow_pickle=False)
    metadata = json.loads(str(handle["metadata"].item()))
    if metadata.get("selection_key") != sel_key:
        handle.close()
        raise ArithmeticError(f"cell ownership mismatch {path}: {metadata.get('selection_key')}")
    return handle


def assemble_cap_covariance(curves: dict, meta: dict, cell_root: Path):
    base = sorted({(k[0], k[2], k[3]) for k in curves if k[1] == "North" and k[4:] == (LANES[0], 20)})
    rows = []
    eps = np.finfo(np.float64).eps
    for sample, factor, group in base:
        nkey0 = (sample, "North", factor, group, LANES[0], 20)
        skey0 = (sample, "South", factor, group, LANES[0], 20)
        if nkey0 not in curves or skey0 not in curves:
            continue
        nsel = selection_key(nkey0); ssel = selection_key(skey0)
        with load_cell(cell_root, nsel) as nc, load_cell(cell_root, ssel) as sc:
            for lane_index, lane in enumerate(LANES):
                nkey = (sample, "North", factor, group, lane, 20)
                skey = (sample, "South", factor, group, lane, 20)
                d = curves[nkey] - curves[skey]
                dnorm2 = float(np.dot(d, d))
                for nside in NSIDES:
                    cn = np.asarray(nc[f"covariance_n{nside}"][lane_index], dtype=np.float64)
                    cs = np.asarray(sc[f"covariance_n{nside}"][lane_index], dtype=np.float64)
                    csum = 0.5 * ((cn + cs) + (cn + cs).T)
                    if not np.all(np.isfinite(csum)):
                        raise ArithmeticError(f"nonfinite C_sum {nsel}/{lane}/n{nside}")
                    eig, vec = np.linalg.eigh(csum)
                    lam_max = float(eig[-1])
                    tau = NBIN * eps * lam_max
                    if float(eig[0]) < -100.0 * tau:
                        raise ArithmeticError(f"C_sum PSD failure {nsel}/{lane}/n{nside}")
                    mask = eig > tau
                    rank = int(np.count_nonzero(mask))
                    if rank == 0:
                        raise ArithmeticError(f"zero-rank C_sum {nsel}/{lane}/n{nside}")
                    coeff = vec[:, mask].T @ d
                    range_norm2 = float(np.dot(coeff, coeff))
                    range_fraction = range_norm2 / dnorm2 if dnorm2 > 0 else 1.0
                    range_fraction = float(np.clip(range_fraction, 0.0, 1.0))
                    q_range = float(np.sum(coeff * coeff / eig[mask]))
                    diag = np.diag(csum)
                    diag_mask = diag > tau
                    if not np.any(diag_mask):
                        raise ArithmeticError(f"no resolved diagonal {nsel}/{lane}/n{nside}")
                    diag_std_rms = float(np.sqrt(np.mean((d[diag_mask] ** 2) / diag[diag_mask])))
                    cov_rms = float(np.sqrt(np.mean(diag)))
                    diff_rms = float(np.sqrt(np.mean(d * d)))
                    row = {
                        "sample": sample, "factor": factor, "group": group,
                        "z_lo": format(meta[nkey]["z_lo"], ".17g"),
                        "z_hi": format(meta[nkey]["z_hi"], ".17g"),
                        "lane": lane, "nside": nside,
                        "north_selection": nsel, "south_selection": ssel,
                        "rank": rank, "rank_tau": format(tau, ".17g"),
                        "positive_condition": format(lam_max / float(eig[mask][0]), ".17g"),
                        "difference_rms": format(diff_rms, ".17g"),
                        "covariance_rms_scale": format(cov_rms, ".17g"),
                        "difference_to_covariance_rms": format(diff_rms / cov_rms, ".17g"),
                        "range_fraction": format(range_fraction, ".17g"),
                        "unresolved_fraction": format(1.0 - range_fraction, ".17g"),
                        "range_quadratic_per_rank": format(q_range / rank, ".17g"),
                        "diagonal_standardized_rms": format(diag_std_rms, ".17g"),
                        "resolved_diagonal_bins": int(np.count_nonzero(diag_mask)),
                        "eigen_min": format(float(eig[0]), ".17g"),
                        "eigen_max": format(lam_max, ".17g"),
                    }
                    for value in row.values():
                        if isinstance(value, float):
                            finite_float(value)
                    rows.append(row)
    if len(rows) != 1164:
        raise ArithmeticError(f"expected 1164 cap covariance rows, found {len(rows)}")
    return rows


QUANTILES = (0.0, 0.25, 0.5, 0.75, 0.9, 0.95, 1.0)
Q_NAMES = ("min", "q25", "median", "q75", "q90", "q95", "max")
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


def summary_record(surface: str, grouping: str, group_key: str, metric: str, values: list[float]) -> dict:
    arr = np.asarray(values, dtype=np.float64)
    if arr.size == 0 or not np.all(np.isfinite(arr)):
        raise ArithmeticError(f"invalid summary {surface}/{group_key}/{metric}")
    q = np.quantile(arr, QUANTILES)
    row = {"surface": surface, "grouping": grouping, "group_key": group_key,
           "metric": metric, "count": int(arr.size)}
    row.update({name: format(float(value), ".17g") for name, value in zip(Q_NAMES, q)})
    return row


def build_summaries(relation_rows: list[dict], cap_rows: list[dict]) -> list[dict]:
    out = []
    relation_groups = defaultdict(list)
    for row in relation_rows:
        relation_groups[("relation_type", row["relation_type"])].append(row)
        key = f"{row['relation_type']}|{row['sample']}|{row['factor_pair']}"
        relation_groups[("relation_type_sample_factor", key)].append(row)
    for (grouping, key), rows in sorted(relation_groups.items()):
        for metric in REL_METRICS:
            out.append(summary_record("RELATION", grouping, key, metric,
                                      [float(row[metric]) for row in rows]))

    cap_groups = defaultdict(list)
    for row in cap_rows:
        cap_groups[("nside", f"n{row['nside']}")].append(row)
        key = f"n{row['nside']}|{row['sample']}|f{row['factor']}|{row['lane']}"
        cap_groups[("nside_sample_factor_lane", key)].append(row)
    for (grouping, key), rows in sorted(cap_groups.items()):
        for metric in CAP_METRICS:
            out.append(summary_record("CAP_COVARIANCE", grouping, key, metric,
                                      [float(row[metric]) for row in rows]))
    return out


def write_manifest(output_dir: Path, artifacts: list[str]) -> None:
    rows = []
    for name in artifacts:
        path = output_dir / name
        rows.append({"artifact": name, "bytes": path.stat().st_size, "sha256": sha256(path)})
    atomic_tsv(output_dir / "R4_OUTPUT_MANIFEST.tsv", ["artifact", "bytes", "sha256"], rows)


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-dir", type=Path, default=here)
    parser.add_argument(
        "--r3-cells", type=Path,
        default=Path("/media/udt-admin/ScratchDisk/Data/UDT_BOSS_R3_2026-08-14/R3_COVARIANCE_CELLS"),
    )
    args = parser.parse_args()
    package = args.package_dir.resolve()
    cell_root = args.r3_cells.resolve()
    for name in OUTPUTS:
        if (package / name).exists():
            raise FileExistsError(f"refusing to overwrite {package / name}")
    for name, expected in EXPECTED_PARENT_HASHES.items():
        actual = sha256(package / name)
        if actual != expected:
            raise ArithmeticError(f"parent hash mismatch {name}: {actual} != {expected}")

    curves, meta, theta_edges = load_curves(package / "R2_CURVE_ATLAS.tsv")
    relations = build_relations(curves, meta)
    relation_rows, raw_lags, diff_lags = assemble_relations(curves, meta, relations)
    cap_rows = assemble_cap_covariance(curves, meta, cell_root)
    summary_rows = build_summaries(relation_rows, cap_rows)

    atomic_tsv(package / "R4_RELATION_ATLAS.tsv", list(relation_rows[0]), relation_rows)
    atomic_npz(
        package / "R4_CROSS_LAG_ATLAS.npz",
        relation_id=np.arange(len(relations), dtype=np.int32),
        raw_lag_bins=np.arange(-118, 119, dtype=np.int16),
        difference_lag_bins=np.arange(-117, 118, dtype=np.int16),
        raw_centered_cross_correlation=raw_lags,
        difference_centered_cross_correlation=diff_lags,
        theta_edges_deg=theta_edges,
    )
    atomic_tsv(package / "R4_CAP_COVARIANCE_ATLAS.tsv", list(cap_rows[0]), cap_rows)
    atomic_tsv(package / "R4_SUMMARY.tsv", list(summary_rows[0]), summary_rows)
    result = {
        "status": "ASSEMBLED__INDEPENDENT_VERIFICATION_PENDING",
        "parent_curve_count": len(curves),
        "angular_bin_count": NBIN,
        "relation_count": len(relations),
        "relation_counts": dict(Counter(kind for kind, _, _ in relations)),
        "cap_covariance_record_count": len(cap_rows),
        "nside_values": list(NSIDES),
        "lane_values": list(LANES),
        "random_ratios": list(RATIOS),
        "raw_cross_lag_count": raw_lags.shape[1],
        "difference_cross_lag_count": diff_lags.shape[1],
        "maximum_conclusion": (
            "OBSERVED bounded complete relation and all-grid covariance-dependence atlas only; "
            "no preferred feature, significance, physical scale, BAO interpretation, cosmology, "
            "UDT comparison, CMB relation, or X_max"
        ),
    }
    atomic_json(package / "R4_RESULT.json", result)
    write_manifest(package, list(OUTPUTS[:-1]))
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

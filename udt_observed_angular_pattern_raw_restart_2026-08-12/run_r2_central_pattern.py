#!/usr/bin/env python3
"""Complete R2 BOSS observer-coordinate central-pattern atlas.

Requires Corrfunc 2.5.3 on PYTHONPATH. See R2_PREREGISTRATION.md.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import resource
import shutil
import sys
import time
from pathlib import Path

import numpy as np
from scipy.fft import dct

try:
    import Corrfunc
    from Corrfunc.mocks.DDtheta_mocks import DDtheta_mocks
except ImportError as exc:  # pragma: no cover - operational guard
    raise SystemExit(
        "Corrfunc 2.5.3 is required. Install the wheel pinned in R2_ENGINE_PROVENANCE.tsv "
        "and put its target directory on PYTHONPATH."
    ) from exc

import run_r1_ingestion_nulls as r1


ROOT = Path(__file__).resolve().parent
EDGES_DEG = np.arange(0.25, 30.0001, 0.25, dtype=np.float64)
CENTERS_DEG = (EDGES_DEG[:-1] + EDGES_DEG[1:]) / 2.0
RATIOS = (5, 10, 20)
LANES = ("W0_UNIT", "W1_SPECTRO", "W2_IMAGING", "W3_OFFICIAL_OBS")
RSS_STOP_GIB = 16.0
THREADS = 8
FINAL_NAMES = (
    "R2_PAIR_COMPONENT_ATLAS.tsv",
    "R2_CURVE_ATLAS.tsv",
    "R2_DESCRIPTOR_ATLAS.tsv",
    "R2_EXTREMA_CROSSING_ATLAS.tsv",
    "R2_DCT_ATLAS.tsv",
    "R2_LAG_ATLAS.tsv",
    "R2_CONSISTENCY_SUMMARY.tsv",
    "R2_RESOURCE_OBSERVED.tsv",
    "R2_RESULT.json",
    "R2_RUN.log",
    "R2_OUTPUT_MANIFEST.tsv",
)


def rss_gib() -> float:
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024.0**2)


def check_rss() -> None:
    if rss_gib() > RSS_STOP_GIB:
        raise MemoryError(f"RSS stop exceeded: {rss_gib():.3f} GiB > {RSS_STOP_GIB:.3f} GiB")


def logger(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = path.open("a")

    def emit(message: str) -> None:
        stamp = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        line = f"[{stamp}] {message}"
        print(line, flush=True)
        handle.write(line + "\n")
        handle.flush()

    return handle, emit


def groups(sample: str):
    ids = r1.sample_shell_ids(sample).astype(int)
    for factor in (1, 2, 4):
        for number, start in enumerate(range(0, len(ids), factor)):
            members = ids[start : start + factor]
            z_lo, _ = r1.shell_bounds(int(members[0]))
            _, z_hi = r1.shell_bounds(int(members[-1]))
            yield {
                "factor": factor,
                "group": number,
                "members": members,
                "z_lo": z_lo,
                "z_hi": z_hi,
                "actual_width": z_hi - z_lo,
            }


def all_units():
    for sample in ("CMASS", "LOWZ"):
        for cap in ("North", "South"):
            for group in groups(sample):
                yield sample, cap, group


def unit_key(sample: str, cap: str, group: dict) -> str:
    return f"{sample}_{cap}_f{group['factor']}_g{group['group']:02d}"


def component_path(checkpoints: Path, key: str, component: str, ratio, lane: str) -> Path:
    return checkpoints / f"{key}__{component}__r{ratio}__{lane}.npz"


def resource_path(checkpoints: Path, key: str) -> Path:
    return checkpoints / f"{key}__resource.json"


def atomic_npz(path: Path, **arrays) -> None:
    temp = path.with_suffix(path.suffix + ".tmp")
    with temp.open("wb") as handle:
        np.savez_compressed(handle, **arrays)
    temp.replace(path)


def read_component(path: Path, expected: dict | None = None):
    with np.load(path, allow_pickle=False) as bundle:
        meta = json.loads(str(bundle["metadata"].item()))
        counts = bundle["counts"].astype(np.int64)
        weighted = bundle["weighted"].astype(np.float64)
    if expected is not None:
        for key, value in expected.items():
            if meta.get(key) != value:
                raise ValueError(f"checkpoint mismatch {path}: {key}={meta.get(key)!r} != {value!r}")
    if counts.shape != (119,) or weighted.shape != (119,):
        raise ValueError(f"checkpoint shape failure: {path}")
    return meta, counts, weighted


def pair_count(ra1, dec1, weights1, ra2=None, dec2=None, weights2=None):
    auto = ra2 is None
    result = DDtheta_mocks(
        1 if auto else 0,
        THREADS,
        EDGES_DEG,
        np.asarray(ra1, dtype=np.float64),
        np.asarray(dec1, dtype=np.float64),
        weights1=None if weights1 is None else np.asarray(weights1, dtype=np.float64),
        RA2=None if auto else np.asarray(ra2, dtype=np.float64),
        DEC2=None if auto else np.asarray(dec2, dtype=np.float64),
        weights2=None if weights2 is None else np.asarray(weights2, dtype=np.float64),
        link_in_dec=True,
        link_in_ra=True,
        verbose=False,
        output_thetaavg=False,
        fast_acos=False,
        copy_particles=True,
        enable_min_sep_opt=True,
        isa="fastest",
        weight_type=None if weights1 is None else "pair_product",
    )
    ordered_factor = 2 if auto else 1
    raw_ordered = result["npairs"].astype(np.int64)
    if auto and np.any(raw_ordered % 2):
        raise ArithmeticError("Corrfunc returned odd ordered auto-pair count")
    counts = raw_ordered // ordered_factor
    if weights1 is None:
        weighted = counts.astype(np.float64)
    else:
        weighted = raw_ordered.astype(np.float64) * result["weightavg"] / ordered_factor
    return counts, weighted


def write_component(path: Path, meta: dict, counts: np.ndarray, weighted: np.ndarray) -> None:
    if np.any(counts < 0) or not np.all(np.isfinite(weighted)):
        raise ArithmeticError(f"invalid pair output: {path}")
    atomic_npz(path, metadata=np.asarray(json.dumps(meta, sort_keys=True)), counts=counts, weighted=weighted)


def execute_components(checkpoints: Path, runlog: Path) -> None:
    checkpoints.mkdir(parents=True, exist_ok=True)
    handle, log = logger(runlog)
    try:
        log(
            f"R2 components start Corrfunc={Corrfunc.__version__} NumPy={np.__version__} "
            f"threads={THREADS}; galaxy pattern opens only into frozen checkpoints"
        )
        entries = r1.read_manifest()
        data_entries = {(e.sample, e.cap): e for e in entries if e.kind == "data"}
        random_entries = {(e.sample, e.cap): e for e in entries if e.kind == "random"}
        for sample in ("CMASS", "LOWZ"):
            for cap in ("North", "South"):
                data_entry = data_entries[(sample, cap)]
                random_entry = random_entries[(sample, cap)]
                data = r1.read_numeric_columns(
                    data_entry.path, ["RA", "DEC", "Z"] + r1.WEIGHT_FIELDS, data_entry.rows
                )
                random = r1.read_numeric_columns(random_entry.path, ["RA", "DEC", "Z"], random_entry.rows)
                weights = r1.weight_arrays(data)
                if not all(np.all(np.isfinite(data[x])) for x in data):
                    raise ValueError(f"nonfinite data field: {sample}/{cap}")
                if not all(np.all(np.isfinite(random[x])) for x in random):
                    raise ValueError(f"nonfinite random field: {sample}/{cap}")
                if not all(np.all(x > 0.0) for x in weights.values()):
                    raise ValueError(f"nonpositive data weight: {sample}/{cap}")
                data_sid = r1.assign_shells(data["Z"], sample)
                random_sid = r1.assign_shells(random["Z"], sample)
                hashes = r1.splitmix64(
                    np.arange(random_entry.rows, dtype=np.uint64), int(random_entry.sha256[:16], 16)
                )
                for group in groups(sample):
                    started = time.monotonic()
                    key = unit_key(sample, cap, group)
                    dlo, dhi = int(group["members"][0]), int(group["members"][-1])
                    di = np.flatnonzero((data_sid >= dlo) & (data_sid <= dhi))
                    ri_all = np.flatnonzero((random_sid >= dlo) & (random_sid <= dhi))
                    nd = int(di.size)
                    needed = 20 * nd
                    if nd < 2 or ri_all.size < needed:
                        raise ValueError(f"insufficient population {key}: ND={nd}, random={ri_all.size}, need={needed}")
                    hlocal = hashes[ri_all]
                    chosen_local = np.argpartition(hlocal, needed - 1)[:needed]
                    chosen_local = chosen_local[
                        np.lexsort((ri_all[chosen_local], hlocal[chosen_local]))
                    ]
                    ri20 = ri_all[chosen_local]
                    common = {
                        "sample": sample,
                        "cap": cap,
                        "factor": int(group["factor"]),
                        "group": int(group["group"]),
                        "z_lo": group["z_lo"],
                        "z_hi": group["z_hi"],
                        "n_data": nd,
                        "n_random_available": int(ri_all.size),
                        "corrfunc": Corrfunc.__version__,
                        "threads": THREADS,
                    }

                    for lane in LANES:
                        path = component_path(checkpoints, key, "DD", "NA", lane)
                        expected = dict(common, component="DD", ratio="NA", lane=lane)
                        if path.exists():
                            read_component(path, expected)
                        else:
                            w = weights[lane][di]
                            counts, weighted = pair_count(data["RA"][di], data["DEC"][di], w)
                            meta = dict(
                                expected,
                                sumw=float(np.sum(w, dtype=np.float64)),
                                sumw2=float(np.sum(w * w, dtype=np.float64)),
                                normalization=float(
                                    (np.sum(w, dtype=np.float64) ** 2 - np.sum(w * w, dtype=np.float64)) / 2.0
                                ),
                            )
                            if meta["normalization"] <= 0.0:
                                raise ArithmeticError(f"nonpositive DD normalization: {key}/{lane}")
                            write_component(path, meta, counts, weighted)
                            log(f"R2 checkpoint {key} DD {lane}")
                            check_rss()

                    for ratio in RATIOS:
                        ri = ri20[: ratio * nd]
                        rr_path = component_path(checkpoints, key, "RR", ratio, "RANDOM_UNIT")
                        rr_expected = dict(common, component="RR", ratio=ratio, lane="RANDOM_UNIT")
                        if rr_path.exists():
                            read_component(rr_path, rr_expected)
                        else:
                            counts, weighted = pair_count(random["RA"][ri], random["DEC"][ri], None)
                            nr = int(ri.size)
                            meta = dict(
                                rr_expected,
                                n_random=nr,
                                sumw=float(nr),
                                sumw2=float(nr),
                                normalization=float(nr * (nr - 1) / 2.0),
                            )
                            write_component(rr_path, meta, counts, weighted)
                            log(f"R2 checkpoint {key} RR ratio={ratio}")
                            check_rss()
                        for lane in LANES:
                            dr_path = component_path(checkpoints, key, "DR", ratio, lane)
                            dr_expected = dict(common, component="DR", ratio=ratio, lane=lane)
                            if dr_path.exists():
                                read_component(dr_path, dr_expected)
                            else:
                                w = weights[lane][di]
                                counts, weighted = pair_count(
                                    data["RA"][di], data["DEC"][di], w,
                                    random["RA"][ri], random["DEC"][ri], np.ones(ri.size, dtype=np.float64),
                                )
                                sumw = float(np.sum(w, dtype=np.float64))
                                meta = dict(
                                    dr_expected,
                                    n_random=int(ri.size),
                                    sumw=sumw,
                                    sumw2=float(np.sum(w * w, dtype=np.float64)),
                                    normalization=float(sumw * ri.size),
                                )
                                write_component(dr_path, meta, counts, weighted)
                                log(f"R2 checkpoint {key} DR ratio={ratio} {lane}")
                                check_rss()
                    log(
                        f"R2 selection complete {key} ND={nd} NRavail={ri_all.size} "
                        f"wall={time.monotonic()-started:.3f}s RSS={rss_gib():.3f}GiB"
                    )
                    rp = resource_path(checkpoints, key)
                    rt = rp.with_suffix(".json.tmp")
                    rt.write_text(json.dumps({
                        "sample": sample, "cap": cap, "factor": int(group["factor"]),
                        "group": int(group["group"]), "wall_seconds": time.monotonic() - started,
                        "max_rss_gib": rss_gib(), "threads": THREADS,
                    }, sort_keys=True) + "\n")
                    rt.replace(rp)
                    del di, ri_all, hlocal, chosen_local, ri20
                del data, random, weights, data_sid, random_sid, hashes
                check_rss()
        log("R2 all pair components complete")
    finally:
        handle.close()


def atomic_writer(path: Path, fields):
    temp = path.with_suffix(path.suffix + ".tmp")
    handle = temp.open("w", newline="")
    writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    return temp, handle, writer


def finalize_writer(path: Path, temp: Path, handle) -> None:
    handle.flush()
    os.fsync(handle.fileno())
    handle.close()
    temp.replace(path)


def curve_id(sample, cap, factor, group, lane, ratio):
    return f"{sample}_{cap}_f{factor}_g{group:02d}_{lane}_r{ratio}"


def extrema_crossings(w):
    rows = []
    for i in range(1, len(w) - 1):
        if w[i] > w[i - 1] and w[i] > w[i + 1]:
            rows.append(("STRICT_MAX", i, i, CENTERS_DEG[i], w[i]))
        if w[i] < w[i - 1] and w[i] < w[i + 1]:
            rows.append(("STRICT_MIN", i, i, CENTERS_DEG[i], w[i]))
    i = 0
    while i < len(w) - 1:
        if w[i + 1] == w[i]:
            j = i + 1
            while j + 1 < len(w) and w[j + 1] == w[i]:
                j += 1
            rows.append(("EXACT_PLATEAU", i, j, (CENTERS_DEG[i] + CENTERS_DEG[j]) / 2.0, w[i]))
            i = j
        i += 1
    for i in range(len(w) - 1):
        if w[i] == 0.0:
            rows.append(("EXACT_ZERO", i, i, CENTERS_DEG[i], 0.0))
        elif w[i] * w[i + 1] < 0.0:
            theta = CENTERS_DEG[i] - w[i] * (CENTERS_DEG[i + 1] - CENTERS_DEG[i]) / (w[i + 1] - w[i])
            rows.append(("LINEAR_SIGN_CROSSING", i, i + 1, theta, 0.0))
    if w[-1] == 0.0:
        rows.append(("EXACT_ZERO", len(w) - 1, len(w) - 1, CENTERS_DEG[-1], 0.0))
    return rows


def lag_values(values):
    centered = values - np.mean(values)
    energy = float(np.dot(centered, centered))
    if energy == 0.0:
        return np.r_[1.0, np.zeros(len(values) - 1)], 1
    return np.asarray([np.dot(centered[: len(values) - lag], centered[lag:]) / energy for lag in range(len(values))]), 0


def assemble(checkpoints: Path, output: Path, checkpoint_log: Path) -> None:
    existing = [name for name in FINAL_NAMES if (output / name).exists()]
    if existing:
        raise FileExistsError(f"R2 final outputs already exist: {existing}")
    output.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()

    component_fields = [
        "sample", "cap", "factor", "group", "z_lo", "z_hi", "actual_width", "component", "ratio",
        "lane", "theta_lo_deg", "theta_hi_deg", "raw_npairs", "raw_weighted_sum", "normalization",
    ]
    curve_fields = [
        "curve_id", "sample", "cap", "factor", "group", "z_lo", "z_hi", "actual_width", "lane", "ratio",
        "n_data", "n_random", "theta_lo_deg", "theta_hi_deg", "dd_raw", "dr_raw", "rr_raw",
        "dd_weighted", "dr_weighted", "rr_weighted", "dd_norm", "dr_norm", "rr_norm", "w_theta",
    ]
    descriptor_fields = [
        "curve_id", "sample", "cap", "factor", "group", "lane", "ratio", "mean", "rms",
        "total_variation", "first_difference_rms", "second_difference_rms", "strict_max_count",
        "strict_min_count", "plateau_count", "zero_crossing_count", "raw_lag_degenerate",
        "difference_lag_degenerate",
    ]
    feature_fields = ["curve_id", "kind", "bin_start", "bin_end", "theta_deg", "value"]
    dct_fields = ["curve_id", "coefficient", "value"]
    lag_fields = ["curve_id", "series", "lag_bins", "lag_degrees", "value", "degenerate"]
    consistency_fields = [
        "comparison", "sample", "cap_or_pair", "factor", "group", "lane_or_pair", "ratio_or_pair",
        "max_abs_difference", "rms_difference",
    ]

    writers = {}
    for name, fields in [
        ("R2_PAIR_COMPONENT_ATLAS.tsv", component_fields),
        ("R2_CURVE_ATLAS.tsv", curve_fields),
        ("R2_DESCRIPTOR_ATLAS.tsv", descriptor_fields),
        ("R2_EXTREMA_CROSSING_ATLAS.tsv", feature_fields),
        ("R2_DCT_ATLAS.tsv", dct_fields),
        ("R2_LAG_ATLAS.tsv", lag_fields),
        ("R2_CONSISTENCY_SUMMARY.tsv", consistency_fields),
    ]:
        writers[name] = (*atomic_writer(output / name, fields), fields)

    curves = {}
    selection_count = 0
    component_rows = curve_rows = feature_rows = dct_rows = lag_rows = 0
    try:
        for sample, cap, group in all_units():
            selection_count += 1
            key = unit_key(sample, cap, group)
            loaded = {}
            for lane in LANES:
                path = component_path(checkpoints, key, "DD", "NA", lane)
                loaded[("DD", "NA", lane)] = read_component(path)
            for ratio in RATIOS:
                loaded[("RR", ratio, "RANDOM_UNIT")] = read_component(
                    component_path(checkpoints, key, "RR", ratio, "RANDOM_UNIT")
                )
                for lane in LANES:
                    loaded[("DR", ratio, lane)] = read_component(
                        component_path(checkpoints, key, "DR", ratio, lane)
                    )

            _, _, component_writer, _ = writers["R2_PAIR_COMPONENT_ATLAS.tsv"]
            for (component, ratio, lane), (meta, counts, weighted) in loaded.items():
                for b in range(119):
                    component_writer.writerow({
                        "sample": sample, "cap": cap, "factor": group["factor"], "group": group["group"],
                        "z_lo": f"{group['z_lo']:.2f}", "z_hi": f"{group['z_hi']:.2f}",
                        "actual_width": f"{group['actual_width']:.2f}", "component": component,
                        "ratio": ratio, "lane": lane, "theta_lo_deg": f"{EDGES_DEG[b]:.2f}",
                        "theta_hi_deg": f"{EDGES_DEG[b+1]:.2f}", "raw_npairs": int(counts[b]),
                        "raw_weighted_sum": f"{weighted[b]:.17g}",
                        "normalization": f"{float(meta['normalization']):.17g}",
                    })
                    component_rows += 1

            _, _, curve_writer, _ = writers["R2_CURVE_ATLAS.tsv"]
            _, _, descriptor_writer, _ = writers["R2_DESCRIPTOR_ATLAS.tsv"]
            _, _, feature_writer, _ = writers["R2_EXTREMA_CROSSING_ATLAS.tsv"]
            _, _, dct_writer, _ = writers["R2_DCT_ATLAS.tsv"]
            _, _, lag_writer, _ = writers["R2_LAG_ATLAS.tsv"]
            for ratio in RATIOS:
                rr_meta, rr_counts, rr_weighted = loaded[("RR", ratio, "RANDOM_UNIT")]
                if np.any(rr_counts <= 0):
                    raise ArithmeticError(f"nonpositive RR bin: {key}/r{ratio}")
                rr_norm = rr_weighted / float(rr_meta["normalization"])
                for lane in LANES:
                    dd_meta, dd_counts, dd_weighted = loaded[("DD", "NA", lane)]
                    dr_meta, dr_counts, dr_weighted = loaded[("DR", ratio, lane)]
                    dd_norm = dd_weighted / float(dd_meta["normalization"])
                    dr_norm = dr_weighted / float(dr_meta["normalization"])
                    w = (dd_norm - 2.0 * dr_norm + rr_norm) / rr_norm
                    if not np.all(np.isfinite(w)):
                        raise ArithmeticError(f"nonfinite R2 curve: {key}/{lane}/r{ratio}")
                    cid = curve_id(sample, cap, group["factor"], group["group"], lane, ratio)
                    curves[(sample, cap, group["factor"], group["group"], lane, ratio)] = w.copy()
                    for b in range(119):
                        curve_writer.writerow({
                            "curve_id": cid, "sample": sample, "cap": cap, "factor": group["factor"],
                            "group": group["group"], "z_lo": f"{group['z_lo']:.2f}",
                            "z_hi": f"{group['z_hi']:.2f}", "actual_width": f"{group['actual_width']:.2f}",
                            "lane": lane, "ratio": ratio, "n_data": dd_meta["n_data"],
                            "n_random": rr_meta["n_random"], "theta_lo_deg": f"{EDGES_DEG[b]:.2f}",
                            "theta_hi_deg": f"{EDGES_DEG[b+1]:.2f}", "dd_raw": int(dd_counts[b]),
                            "dr_raw": int(dr_counts[b]), "rr_raw": int(rr_counts[b]),
                            "dd_weighted": f"{dd_weighted[b]:.17g}",
                            "dr_weighted": f"{dr_weighted[b]:.17g}",
                            "rr_weighted": f"{rr_weighted[b]:.17g}",
                            "dd_norm": f"{dd_norm[b]:.17g}", "dr_norm": f"{dr_norm[b]:.17g}",
                            "rr_norm": f"{rr_norm[b]:.17g}", "w_theta": f"{w[b]:.17g}",
                        })
                        curve_rows += 1
                    features = extrema_crossings(w)
                    for kind, bs, be, theta, value in features:
                        feature_writer.writerow({
                            "curve_id": cid, "kind": kind, "bin_start": bs, "bin_end": be,
                            "theta_deg": f"{theta:.17g}", "value": f"{value:.17g}",
                        })
                        feature_rows += 1
                    coeffs = dct(w, type=2, norm="ortho")
                    for index, value in enumerate(coeffs):
                        dct_writer.writerow({"curve_id": cid, "coefficient": index, "value": f"{value:.17g}"})
                        dct_rows += 1
                    raw_lag, raw_deg = lag_values(w)
                    diff_lag, diff_deg = lag_values(np.diff(w))
                    for series, values, degenerate in (
                        ("MEAN_CENTERED_RAW", raw_lag, raw_deg),
                        ("MEAN_CENTERED_FIRST_DIFFERENCE", diff_lag, diff_deg),
                    ):
                        for lag, value in enumerate(values):
                            lag_writer.writerow({
                                "curve_id": cid, "series": series, "lag_bins": lag,
                                "lag_degrees": f"{0.25*lag:.2f}", "value": f"{value:.17g}",
                                "degenerate": degenerate,
                            })
                            lag_rows += 1
                    kinds = [x[0] for x in features]
                    descriptor_writer.writerow({
                        "curve_id": cid, "sample": sample, "cap": cap, "factor": group["factor"],
                        "group": group["group"], "lane": lane, "ratio": ratio,
                        "mean": f"{np.mean(w):.17g}", "rms": f"{np.sqrt(np.mean(w*w)):.17g}",
                        "total_variation": f"{np.sum(np.abs(np.diff(w))):.17g}",
                        "first_difference_rms": f"{np.sqrt(np.mean(np.diff(w)**2)):.17g}",
                        "second_difference_rms": f"{np.sqrt(np.mean(np.diff(w, n=2)**2)):.17g}",
                        "strict_max_count": kinds.count("STRICT_MAX"),
                        "strict_min_count": kinds.count("STRICT_MIN"),
                        "plateau_count": kinds.count("EXACT_PLATEAU"),
                        "zero_crossing_count": kinds.count("LINEAR_SIGN_CROSSING") + kinds.count("EXACT_ZERO"),
                        "raw_lag_degenerate": raw_deg, "difference_lag_degenerate": diff_deg,
                    })
        if selection_count != 194 or len(curves) != 2328:
            raise AssertionError(f"R2 census mismatch: selections={selection_count}, curves={len(curves)}")

        _, _, consistency_writer, _ = writers["R2_CONSISTENCY_SUMMARY.tsv"]
        for sample, cap, group in all_units():
            for lane in LANES:
                base = curves[(sample, cap, group["factor"], group["group"], lane, 20)]
                for ratio in (5, 10):
                    delta = curves[(sample, cap, group["factor"], group["group"], lane, ratio)] - base
                    consistency_writer.writerow({
                        "comparison": "RANDOM_DENSITY", "sample": sample, "cap_or_pair": cap,
                        "factor": group["factor"], "group": group["group"], "lane_or_pair": lane,
                        "ratio_or_pair": f"{ratio}-20", "max_abs_difference": f"{np.max(np.abs(delta)):.17g}",
                        "rms_difference": f"{np.sqrt(np.mean(delta*delta)):.17g}",
                    })
            for ratio in RATIOS:
                base = curves[(sample, cap, group["factor"], group["group"], "W0_UNIT", ratio)]
                for lane in LANES[1:]:
                    delta = curves[(sample, cap, group["factor"], group["group"], lane, ratio)] - base
                    consistency_writer.writerow({
                        "comparison": "WEIGHT_LANE", "sample": sample, "cap_or_pair": cap,
                        "factor": group["factor"], "group": group["group"],
                        "lane_or_pair": f"{lane}-W0_UNIT", "ratio_or_pair": ratio,
                        "max_abs_difference": f"{np.max(np.abs(delta)):.17g}",
                        "rms_difference": f"{np.sqrt(np.mean(delta*delta)):.17g}",
                    })
        for sample in ("CMASS", "LOWZ"):
            for group in groups(sample):
                for lane in LANES:
                    for ratio in RATIOS:
                        north = curves[(sample, "North", group["factor"], group["group"], lane, ratio)]
                        south = curves[(sample, "South", group["factor"], group["group"], lane, ratio)]
                        delta = north - south
                        consistency_writer.writerow({
                            "comparison": "CAP", "sample": sample, "cap_or_pair": "North-South",
                            "factor": group["factor"], "group": group["group"], "lane_or_pair": lane,
                            "ratio_or_pair": ratio, "max_abs_difference": f"{np.max(np.abs(delta)):.17g}",
                            "rms_difference": f"{np.sqrt(np.mean(delta*delta)):.17g}",
                        })
    except Exception:
        for name, (temp, handle, _, _) in writers.items():
            handle.close()
            temp.unlink(missing_ok=True)
        raise
    else:
        for name, (temp, handle, _, _) in writers.items():
            finalize_writer(output / name, temp, handle)

    resources = output / "R2_RESOURCE_OBSERVED.tsv"
    with resources.open("x", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["phase", "sample", "cap", "factor", "group", "wall_seconds", "max_rss_gib", "threads"])
        for sample, cap, group in all_units():
            record = json.loads(resource_path(checkpoints, unit_key(sample, cap, group)).read_text())
            writer.writerow([
                "components", sample, cap, group["factor"], group["group"],
                f"{float(record['wall_seconds']):.6f}", f"{float(record['max_rss_gib']):.6f}",
                int(record["threads"]),
            ])
        writer.writerow([
            "assembly", "ALL", "ALL", "ALL", "ALL", f"{time.monotonic()-started:.6f}",
            f"{rss_gib():.6f}", THREADS,
        ])

    result = {
        "status": "OBSERVED__R2_CENTRAL_PATTERN_ATLAS_ASSEMBLED__VERIFICATION_PENDING",
        "selection_count": selection_count,
        "curve_count": len(curves),
        "angular_bin_count": 119,
        "component_rows": component_rows,
        "curve_rows": curve_rows,
        "feature_rows": feature_rows,
        "dct_rows": dct_rows,
        "lag_rows": lag_rows,
        "corrfunc": Corrfunc.__version__,
        "threads": THREADS,
        "max_rss_gib": rss_gib(),
        "assembly_wall_seconds": time.monotonic() - started,
    }
    temp = (output / "R2_RESULT.json").with_suffix(".json.tmp")
    temp.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temp.replace(output / "R2_RESULT.json")
    shutil.copyfile(checkpoint_log, output / "R2_RUN.log")

    manifest_path = output / "R2_OUTPUT_MANIFEST.tsv"
    manifest_temp = manifest_path.with_suffix(".tsv.tmp")
    manifest_names = [name for name in FINAL_NAMES if name != "R2_OUTPUT_MANIFEST.tsv"]
    with manifest_temp.open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["artifact", "bytes", "sha256"])
        for name in manifest_names:
            path = output / name
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            writer.writerow([name, path.stat().st_size, digest])
    manifest_temp.replace(manifest_path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("components", "assemble", "all"), default="all")
    parser.add_argument("--checkpoint-dir", type=Path, default=Path("/tmp/udt_boss_r2_checkpoints"))
    parser.add_argument("--output-dir", type=Path, default=ROOT)
    args = parser.parse_args()
    checkpoints = args.checkpoint_dir.resolve()
    output = args.output_dir.resolve()
    checkpoint_log = checkpoints / "R2_RUN.log"
    if Corrfunc.__version__ != "2.5.3":
        raise RuntimeError(f"Corrfunc version mismatch: {Corrfunc.__version__}")
    if args.phase in ("components", "all"):
        execute_components(checkpoints, checkpoint_log)
    if args.phase in ("assemble", "all"):
        assemble(checkpoints, output, checkpoint_log)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

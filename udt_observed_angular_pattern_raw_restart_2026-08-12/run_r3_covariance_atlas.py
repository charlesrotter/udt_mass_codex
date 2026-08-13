#!/usr/bin/env python3
"""Execute the preregistered R3 data-only spatial covariance atlas."""

from __future__ import annotations

import argparse
import csv
import gc
import hashlib
import json
import math
import os
import resource
import shutil
import sys
import time
from collections import defaultdict
from pathlib import Path

import healpy as hp
import numpy as np
import treecorr

import run_r1_ingestion_nulls as r1
import run_r2_central_pattern as r2


ROOT = Path(__file__).resolve().parent
SCRIPT = Path(__file__).resolve()
LANES = tuple(r1.WEIGHT_LANES)
NSIDES = (4, 8, 16)
EDGES = np.arange(0.25, 30.0001, 0.25, dtype=np.float64)
NBIN = len(EDGES) - 1
TREE_NBIN = NBIN + 1
TREE_MAX_SEP = float(EDGES[-1] + (EDGES[1] - EDGES[0]))
THREADS = 8
RSS_STOP_GIB = 16.0
RATIO = 20
COMPONENTS = ("DD", "DR", "RR")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_npz(path: Path, **arrays) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    with temp.open("wb") as handle:
        np.savez_compressed(handle, **arrays)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temp, path)


def atomic_text(path: Path, content: str) -> None:
    temp = path.with_name(path.name + ".tmp")
    with temp.open("x") as handle:
        handle.write(content)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temp, path)


def check_rss() -> float:
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0**2
    if rss > RSS_STOP_GIB:
        raise MemoryError(f"R3 RSS {rss:.3f} GiB exceeds {RSS_STOP_GIB:.1f} GiB stop")
    return rss


def logger(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = path.open("a", buffering=1)

    def write(message: str) -> None:
        stamp = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        line = f"[{stamp}] {message}"
        print(line, flush=True)
        handle.write(line + "\n")

    return handle, write


def pixel_ids(ra, dec, nside=16):
    return hp.ang2pix(
        nside,
        np.deg2rad(90.0 - np.asarray(dec, dtype=np.float64)),
        np.deg2rad(np.mod(np.asarray(ra, dtype=np.float64), 360.0)),
        nest=True,
    )


def load_block_pixels():
    out = defaultdict(list)
    with (ROOT / "R3_BLOCK_ATLAS.tsv").open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            out[(row["sample"], row["cap"], int(row["nside"]))].append(int(row["nested_pixel"]))
    answer = {}
    for key, values in out.items():
        array = np.asarray(values, dtype=np.int64)
        assert np.all(np.diff(array) > 0)
        answer[key] = array
    assert len(answer) == 12
    return answer


def load_r2_components():
    build = defaultdict(lambda: {"count": [], "weight": [], "normalization": None})
    with (ROOT / "R2_PAIR_COMPONENT_ATLAS.tsv").open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            component, ratio, lane = row["component"], row["ratio"], row["lane"]
            keep = (
                (component == "DD" and ratio == "NA" and lane in LANES)
                or (component == "DR" and ratio == str(RATIO) and lane in LANES)
                or (component == "RR" and ratio == str(RATIO) and lane == "RANDOM_UNIT")
            )
            if not keep:
                continue
            key = (
                row["sample"], row["cap"], int(row["factor"]), int(row["group"]),
                component, lane,
            )
            item = build[key]
            item["count"].append(int(row["raw_npairs"]))
            item["weight"].append(float(row["raw_weighted_sum"]))
            norm = float(row["normalization"])
            if item["normalization"] is None:
                item["normalization"] = norm
            else:
                assert item["normalization"] == norm
    expected = 194 * 9
    assert len(build) == expected
    for item in build.values():
        assert len(item["count"]) == len(item["weight"]) == NBIN
        item["count"] = np.asarray(item["count"], dtype=np.int64)
        item["weight"] = np.asarray(item["weight"], dtype=np.float64)
    return dict(build)


def patch_labels(ra, dec, fine_pixels):
    pix = pixel_ids(ra, dec, 16)
    label = np.searchsorted(fine_pixels, pix)
    if np.any(label == len(fine_pixels)) or np.any(fine_pixels[label] != pix):
        raise ValueError("object lies outside random-owned NSIDE=16 footprint")
    return label.astype(np.int32)


def parent_maps(sample, cap, block_pixels):
    fine = block_pixels[(sample, cap, 16)]
    maps = {}
    for nside in NSIDES:
        divisor = (16 // nside) ** 2
        parent = fine // divisor
        expected = block_pixels[(sample, cap, nside)]
        index = np.searchsorted(expected, parent)
        assert np.all(index < len(expected)) and np.all(expected[index] == parent)
        maps[nside] = index.astype(np.int32)
    return fine, maps


def tree_count(catalog1, catalog2=None):
    config = dict(
        min_sep=0.25,
        # One discarded outer guard bin prevents TreeCorr's patch-level
        # _trivially_zero prefilter from dropping patch relations containing
        # valid pairs just inside the 30-degree analysis boundary.
        max_sep=TREE_MAX_SEP,
        nbins=TREE_NBIN,
        sep_units="degrees",
        bin_type="Linear",
        bin_slop=0.0,
        angle_slop=0.0,
        brute=False,
    )
    corr = treecorr.NNCorrelation(**config)
    if catalog2 is None:
        corr.process(catalog1, metric="Arc", num_threads=THREADS, corr_only=False)
    else:
        corr.process(catalog1, catalog2, metric="Arc", num_threads=THREADS, corr_only=False)
    return corr


def correlation_arrays(corr):
    full_counts = np.asarray(corr.npairs, dtype=np.float64)
    full_weights = np.asarray(corr.weight, dtype=np.float64)
    if full_counts.shape != (TREE_NBIN,) or full_weights.shape != (TREE_NBIN,):
        raise ArithmeticError("invalid TreeCorr guarded component shape")
    counts_float = full_counts[:NBIN]
    counts = np.rint(counts_float).astype(np.int64)
    if not np.array_equal(counts_float, counts.astype(np.float64)):
        raise ArithmeticError("TreeCorr returned noninteger pair counts")
    weights = full_weights[:NBIN]
    if counts.shape != (NBIN,) or weights.shape != (NBIN,) or np.any(counts < 0) or not np.all(np.isfinite(weights)):
        raise ArithmeticError("invalid TreeCorr central component")
    return counts, weights


def aggregate_removals(corr, fine_to_parent, parent_sizes, chunk_size=4096):
    removals = {
        nside: {
            "count": np.zeros((parent_sizes[nside], NBIN), dtype=np.int64),
            "weight": np.zeros((parent_sizes[nside], NBIN), dtype=np.float64),
        }
        for nside in NSIDES
    }
    sum_count = np.zeros(NBIN, dtype=np.int64)
    sum_weight = np.zeros(NBIN, dtype=np.float64)
    items = list(corr.results.items())
    for start in range(0, len(items), chunk_size):
        chunk = items[start : start + chunk_size]
        left = np.fromiter((key[0] for key, _ in chunk), dtype=np.int32, count=len(chunk))
        right = np.fromiter((key[1] for key, _ in chunk), dtype=np.int32, count=len(chunk))
        counts_float = np.stack([
            np.asarray(value.npairs, dtype=np.float64)[:NBIN] for _, value in chunk
        ])
        counts = np.rint(counts_float).astype(np.int64)
        if not np.array_equal(counts_float, counts.astype(np.float64)):
            raise ArithmeticError("noninteger patch pair count")
        weights = np.stack([
            np.asarray(value.weight, dtype=np.float64)[:NBIN] for _, value in chunk
        ])
        sum_count += np.sum(counts, axis=0, dtype=np.int64)
        sum_weight += np.sum(weights, axis=0, dtype=np.float64)
        for nside in NSIDES:
            a = fine_to_parent[nside][left]
            b = fine_to_parent[nside][right]
            np.add.at(removals[nside]["count"], a, counts)
            np.add.at(removals[nside]["weight"], a, weights)
            different = b != a
            if np.any(different):
                np.add.at(removals[nside]["count"], b[different], counts[different])
                np.add.at(removals[nside]["weight"], b[different], weights[different])
    central_count, central_weight = correlation_arrays(corr)
    if not np.array_equal(sum_count, central_count):
        raise ArithmeticError("patch integer sums do not reproduce central component")
    if not np.allclose(sum_weight, central_weight, rtol=5e-12, atol=1e-8):
        raise ArithmeticError("patch weighted sums do not reproduce central component")
    return removals


def component_comparison(observed_count, observed_weight, expected, label):
    exact = bool(np.array_equal(observed_count, expected["count"]))
    absdiff = float(np.max(np.abs(observed_weight - expected["weight"])))
    reldiff = float(
        np.max(np.abs(observed_weight - expected["weight"]) / np.maximum(np.abs(expected["weight"]), 1.0))
    )
    if not exact or not (reldiff <= 5e-9 or absdiff <= 1e-7):
        raise ArithmeticError(f"R2 central mismatch {label}: exact={exact} abs={absdiff} rel={reldiff}")
    return {"label": label, "integer_counts_exact": exact, "max_weight_abs_difference": absdiff, "max_weight_relative_difference": reldiff}


def occupancy(labels, size, values=None):
    if values is None:
        return np.bincount(labels, minlength=size).astype(np.float64)
    return np.bincount(labels, weights=np.asarray(values, dtype=np.float64), minlength=size).astype(np.float64)


def covariance_record(leaveout):
    k = leaveout.shape[0]
    if k < 2 or leaveout.shape[1] != NBIN or not np.all(np.isfinite(leaveout)):
        raise ArithmeticError("invalid leave-one array")
    mean = np.mean(leaveout, axis=0, dtype=np.float64)
    centered = leaveout - mean
    covariance = ((k - 1.0) / k) * (centered.T @ centered)
    covariance = (covariance + covariance.T) / 2.0
    eig = np.linalg.eigvalsh(covariance)
    largest = float(eig[-1])
    tau = float(NBIN * np.finfo(np.float64).eps * largest) if largest > 0.0 else 0.0
    if eig[0] < -100.0 * max(tau, np.finfo(np.float64).tiny):
        raise ArithmeticError(f"covariance PSD failure: min={eig[0]} tau={tau}")
    rank = int(np.count_nonzero(eig > tau))
    if rank > min(NBIN, k - 1):
        raise ArithmeticError("covariance rank bound failure")
    return mean, covariance, eig, tau, rank


def selection_key(sample, cap, group):
    return f"{sample}_{cap}_f{int(group['factor'])}_g{int(group['group']):02d}"


def checkpoint_path(directory: Path, sample, cap, group):
    return directory / f"R3_{selection_key(sample, cap, group)}.npz"


def cell_contract():
    return {
        "script_sha256": sha256(SCRIPT),
        "preregistration_sha256": sha256(ROOT / "R3_PREREGISTRATION.md"),
        "block_atlas_sha256": sha256(ROOT / "R3_BLOCK_ATLAS.tsv"),
        "r2_output_manifest_sha256": sha256(ROOT / "R2_OUTPUT_MANIFEST.tsv"),
        "treecorr": treecorr.__version__,
        "healpy": hp.__version__,
        "numpy": np.__version__,
        "lanes": list(LANES),
        "nsides": list(NSIDES),
        "ratio": RATIO,
        "nbin": NBIN,
        "tree_nbin_with_discarded_outer_guard": TREE_NBIN,
        "tree_max_sep_with_discarded_outer_guard_deg": TREE_MAX_SEP,
        "threads": THREADS,
    }


def read_cell(path: Path, expected=None):
    with np.load(path, allow_pickle=False) as bundle:
        meta = json.loads(str(bundle["metadata"].item()))
        arrays = {name: bundle[name] for name in bundle.files if name != "metadata"}
    if expected is not None:
        for key, value in expected.items():
            if meta.get(key) != value:
                raise ValueError(f"checkpoint mismatch {path}: {key}")
    return meta, arrays


def execute_selection(sample, cap, group, data, random, data_sid, random_sid, hashes, weights, block_pixels, r2_components, outpath, log):
    start = time.monotonic()
    key = selection_key(sample, cap, group)
    lo, hi = int(group["members"][0]), int(group["members"][-1])
    di = np.flatnonzero((data_sid >= lo) & (data_sid <= hi))
    candidates = np.flatnonzero((random_sid >= lo) & (random_sid <= hi))
    need = RATIO * len(di)
    if len(di) < 2 or len(candidates) < need:
        raise ValueError(f"insufficient selection population {key}")
    local = np.argpartition(hashes[candidates], need - 1)[:need]
    local = local[np.lexsort((candidates[local], hashes[candidates][local]))]
    ri = candidates[local]

    fine_pixels, fine_to_parent = parent_maps(sample, cap, block_pixels)
    parent_sizes = {nside: len(block_pixels[(sample, cap, nside)]) for nside in NSIDES}
    data_patch = patch_labels(data["RA"][di], data["DEC"][di], fine_pixels)
    random_patch = patch_labels(random["RA"][ri], random["DEC"][ri], fine_pixels)
    data_parent = {nside: fine_to_parent[nside][data_patch] for nside in NSIDES}
    random_parent = {nside: fine_to_parent[nside][random_patch] for nside in NSIDES}

    random_catalog = treecorr.Catalog(
        ra=random["RA"][ri], dec=random["DEC"][ri], ra_units="degrees", dec_units="degrees",
        w=np.ones(len(ri), dtype=np.float64), patch=random_patch, npatch=len(fine_pixels),
    )
    rr_corr = tree_count(random_catalog)
    rr_count, rr_weight = correlation_arrays(rr_corr)
    rr_expected = r2_components[(sample, cap, int(group["factor"]), int(group["group"]), "RR", "RANDOM_UNIT")]
    comparisons = [component_comparison(rr_count, rr_weight, rr_expected, f"{key}/RR/RANDOM_UNIT")]
    rr_remove = aggregate_removals(rr_corr, fine_to_parent, parent_sizes)

    arrays = {
        "central_rr_count": rr_count,
        "central_rr_weight": rr_weight,
        "central_dd_count": np.empty((len(LANES), NBIN), dtype=np.int64),
        "central_dd_weight": np.empty((len(LANES), NBIN), dtype=np.float64),
        "central_dr_count": np.empty((len(LANES), NBIN), dtype=np.int64),
        "central_dr_weight": np.empty((len(LANES), NBIN), dtype=np.float64),
        "central_curve": np.empty((len(LANES), NBIN), dtype=np.float64),
    }
    summaries = []
    anchor = int(group["factor"]) == 1 and int(group["group"]) == 0

    # Geometry-owned block populations are shared across weight lanes.
    geometry = {}
    for nside in NSIDES:
        size = parent_sizes[nside]
        nr_all = occupancy(random_parent[nside], size).astype(np.int64)
        nd_all = occupancy(data_parent[nside], size).astype(np.int64)
        # A literal spatial subcatalog is the union of selected data and random support.
        # A full-footprint block can legitimately contain selected galaxies but zero rows
        # from the finite deterministic 20x random subset. Deleting that block then removes
        # data-incident DD/DR pairs while its RR removal is exactly zero.
        active = (nr_all > 0) | (nd_all > 0)
        active_index = np.flatnonzero(active)
        if len(active_index) < 2:
            raise ValueError(f"too few active blocks {key}/nside{nside}")
        parent_pix = block_pixels[(sample, cap, nside)]
        geometry[nside] = (active_index, nd_all[active], nr_all[active])
        arrays[f"active_pixel_n{nside}"] = parent_pix[active]
        arrays[f"data_count_n{nside}"] = nd_all[active]
        arrays[f"random_count_n{nside}"] = nr_all[active]

    for lane_index, lane in enumerate(LANES):
        w = np.asarray(weights[lane][di], dtype=np.float64)
        data_catalog = treecorr.Catalog(
            ra=data["RA"][di], dec=data["DEC"][di], ra_units="degrees", dec_units="degrees",
            w=w, patch=data_patch, npatch=len(fine_pixels),
        )
        dd_corr = tree_count(data_catalog)
        dr_corr = tree_count(data_catalog, random_catalog)
        dd_count, dd_weight = correlation_arrays(dd_corr)
        dr_count, dr_weight = correlation_arrays(dr_corr)
        dd_expected = r2_components[(sample, cap, int(group["factor"]), int(group["group"]), "DD", lane)]
        dr_expected = r2_components[(sample, cap, int(group["factor"]), int(group["group"]), "DR", lane)]
        comparisons.append(component_comparison(dd_count, dd_weight, dd_expected, f"{key}/DD/{lane}"))
        comparisons.append(component_comparison(dr_count, dr_weight, dr_expected, f"{key}/DR/{lane}"))
        dd_remove = aggregate_removals(dd_corr, fine_to_parent, parent_sizes)
        dr_remove = aggregate_removals(dr_corr, fine_to_parent, parent_sizes)

        arrays["central_dd_count"][lane_index] = dd_count
        arrays["central_dd_weight"][lane_index] = dd_weight
        arrays["central_dr_count"][lane_index] = dr_count
        arrays["central_dr_weight"][lane_index] = dr_weight
        arrays["central_curve"][lane_index] = (
            dd_weight / dd_expected["normalization"]
            - 2.0 * dr_weight / dr_expected["normalization"]
            + rr_weight / rr_expected["normalization"]
        ) / (rr_weight / rr_expected["normalization"])

        for nside in NSIDES:
            active_index, nd, nr = geometry[nside]
            size = parent_sizes[nside]
            sumw_block = occupancy(data_parent[nside], size, w)[active_index]
            sumw2_block = occupancy(data_parent[nside], size, w * w)[active_index]
            arrays.setdefault(f"data_sumw_n{nside}", np.empty((len(LANES), len(active_index)), dtype=np.float64))[lane_index] = sumw_block
            arrays.setdefault(f"data_sumw2_n{nside}", np.empty((len(LANES), len(active_index)), dtype=np.float64))[lane_index] = sumw2_block

            total_sumw = float(np.sum(w, dtype=np.float64))
            total_sumw2 = float(np.sum(w * w, dtype=np.float64))
            retained_sumw = total_sumw - sumw_block
            retained_sumw2 = total_sumw2 - sumw2_block
            retained_nr = len(ri) - nr
            dd_norm = (retained_sumw**2 - retained_sumw2) / 2.0
            dr_norm = retained_sumw * retained_nr
            rr_norm = retained_nr * (retained_nr - 1.0) / 2.0
            if np.any(dd_norm <= 0.0) or np.any(dr_norm <= 0.0) or np.any(rr_norm <= 0.0):
                raise ArithmeticError(f"nonpositive leave-one normalization {key}/{lane}/nside{nside}")

            ddw = dd_weight[None, :] - dd_remove[nside]["weight"][active_index]
            drw = dr_weight[None, :] - dr_remove[nside]["weight"][active_index]
            rrw = rr_weight[None, :] - rr_remove[nside]["weight"][active_index]
            ddc = dd_count[None, :] - dd_remove[nside]["count"][active_index]
            drc = dr_count[None, :] - dr_remove[nside]["count"][active_index]
            rrc = rr_count[None, :] - rr_remove[nside]["count"][active_index]
            if np.any(ddc < 0) or np.any(drc < 0) or np.any(rrc <= 0) or np.any(rrw <= 0.0):
                raise ArithmeticError(f"invalid retained component {key}/{lane}/nside{nside}")
            rrn = rrw / rr_norm[:, None]
            leaveout = (ddw / dd_norm[:, None] - 2.0 * drw / dr_norm[:, None] + rrn) / rrn
            mean, covariance, eig, tau, rank = covariance_record(leaveout)
            arrays.setdefault(f"jk_mean_n{nside}", np.empty((len(LANES), NBIN), dtype=np.float64))[lane_index] = mean
            arrays.setdefault(f"covariance_n{nside}", np.empty((len(LANES), NBIN, NBIN), dtype=np.float64))[lane_index] = covariance
            arrays.setdefault(f"eigenvalues_n{nside}", np.empty((len(LANES), NBIN), dtype=np.float64))[lane_index] = eig
            arrays.setdefault(f"rank_n{nside}", np.empty(len(LANES), dtype=np.int16))[lane_index] = rank
            arrays.setdefault(f"rank_tau_n{nside}", np.empty(len(LANES), dtype=np.float64))[lane_index] = tau
            if anchor and lane == "W3_OFFICIAL_OBS" and nside in (4, 16):
                arrays[f"anchor_leaveout_n{nside}"] = leaveout

            diag = np.diag(covariance)
            positive = eig[eig > tau]
            summaries.append({
                "lane": lane,
                "nside": nside,
                "active_blocks": len(active_index),
                "data_block_min": int(np.min(nd)),
                "data_block_median": float(np.median(nd)),
                "data_block_max": int(np.max(nd)),
                "data_block_cv": float(np.std(nd) / np.mean(nd)),
                "random_block_min": int(np.min(nr)),
                "random_block_median": float(np.median(nr)),
                "random_block_max": int(np.max(nr)),
                "random_block_cv": float(np.std(nr) / np.mean(nr)),
                "rank": rank,
                "rank_bound": min(NBIN, len(active_index) - 1),
                "rank_tau": tau,
                "eigen_min": float(eig[0]),
                "eigen_max": float(eig[-1]),
                "positive_condition": float(eig[-1] / positive[0]) if len(positive) else math.inf,
                "diag_min": float(np.min(diag)),
                "diag_median": float(np.median(diag)),
                "diag_max": float(np.max(diag)),
                "symmetry_max_abs": float(np.max(np.abs(covariance - covariance.T))),
            })
        del dd_corr, dr_corr, data_catalog, dd_remove, dr_remove
        gc.collect()
        check_rss()

    elapsed = time.monotonic() - start
    metadata = {
        **cell_contract(),
        "sample": sample,
        "cap": cap,
        "factor": int(group["factor"]),
        "group": int(group["group"]),
        "z_lo": float(group["z_lo"]),
        "z_hi": float(group["z_hi"]),
        "n_data": len(di),
        "n_random": len(ri),
        "selection_key": key,
        "anchor": anchor,
        "comparisons": comparisons,
        "summaries": summaries,
        "wall_seconds": elapsed,
        "max_rss_gib": check_rss(),
    }
    atomic_npz(outpath, metadata=np.asarray(json.dumps(metadata, sort_keys=True)), **arrays)
    log(f"R3 selection complete {key} ND={len(di)} NR={len(ri)} wall={elapsed:.3f}s RSS={metadata['max_rss_gib']:.3f}GiB")
    del rr_corr, random_catalog, rr_remove, arrays
    gc.collect()


def execute(checkpoints: Path, runlog: Path):
    checkpoints.mkdir(parents=True, exist_ok=True)
    handle, log = logger(runlog)
    try:
        log(f"R3 start TreeCorr={treecorr.__version__} healpy={hp.__version__} NumPy={np.__version__} threads={THREADS}")
        blocks = load_block_pixels()
        r2_components = load_r2_components()
        entries = r1.read_manifest()
        data_entries = {(e.sample, e.cap): e for e in entries if e.kind == "data"}
        random_entries = {(e.sample, e.cap): e for e in entries if e.kind == "random"}
        contract = cell_contract()
        for sample in ("CMASS", "LOWZ"):
            for cap in ("North", "South"):
                de, re = data_entries[(sample, cap)], random_entries[(sample, cap)]
                data = r1.read_numeric_columns(de.path, ["RA", "DEC", "Z"] + r1.WEIGHT_FIELDS, de.rows)
                random = r1.read_numeric_columns(re.path, ["RA", "DEC", "Z"], re.rows)
                weights = r1.weight_arrays(data)
                if not all(np.all(np.isfinite(data[field])) for field in data):
                    raise ValueError(f"nonfinite data {sample}/{cap}")
                if not all(np.all(np.isfinite(random[field])) for field in random):
                    raise ValueError(f"nonfinite random {sample}/{cap}")
                if not all(np.all(value > 0.0) for value in weights.values()):
                    raise ValueError(f"nonpositive weights {sample}/{cap}")
                data_sid = r1.assign_shells(data["Z"], sample)
                random_sid = r1.assign_shells(random["Z"], sample)
                hashes = r1.splitmix64(np.arange(re.rows, dtype=np.uint64), int(re.sha256[:16], 16))
                for group in r2.groups(sample):
                    path = checkpoint_path(checkpoints, sample, cap, group)
                    expected = {
                        **contract,
                        "sample": sample,
                        "cap": cap,
                        "factor": int(group["factor"]),
                        "group": int(group["group"]),
                        "selection_key": selection_key(sample, cap, group),
                    }
                    if path.exists():
                        read_cell(path, expected)
                        log(f"R3 checkpoint reused {expected['selection_key']}")
                    else:
                        execute_selection(
                            sample, cap, group, data, random, data_sid, random_sid, hashes, weights,
                            blocks, r2_components, path, log,
                        )
        log("R3 all covariance cells complete")
    finally:
        handle.close()


def assemble(checkpoints: Path, runlog: Path):
    final_dir = ROOT / "R3_COVARIANCE_CELLS"
    final_files = (
        ROOT / "R3_COVARIANCE_SUMMARY.tsv",
        ROOT / "R3_CENTRAL_ENGINE_COMPARISON.tsv",
        ROOT / "R3_RESOURCE_OBSERVED.tsv",
        ROOT / "R3_RESULT.json",
        ROOT / "R3_RUN.log",
        ROOT / "R3_OUTPUT_MANIFEST.tsv",
    )
    if final_dir.exists() or any(path.exists() for path in final_files):
        raise FileExistsError("R3 final outputs already exist")
    groups = [(sample, cap, group) for sample in ("CMASS", "LOWZ") for cap in ("North", "South") for group in r2.groups(sample)]
    if len(groups) != 194:
        raise AssertionError(len(groups))
    contract = cell_contract()
    summary_rows, comparison_rows, resource_rows = [], [], []
    cells = []
    for sample, cap, group in groups:
        path = checkpoint_path(checkpoints, sample, cap, group)
        expected = {
            **contract,
            "sample": sample,
            "cap": cap,
            "factor": int(group["factor"]),
            "group": int(group["group"]),
            "selection_key": selection_key(sample, cap, group),
        }
        meta, arrays = read_cell(path, expected)
        for item in meta["summaries"]:
            summary_rows.append({
                "selection_key": meta["selection_key"], "sample": sample, "cap": cap,
                "factor": meta["factor"], "group": meta["group"], "z_lo": meta["z_lo"], "z_hi": meta["z_hi"],
                **item,
            })
        for item in meta["comparisons"]:
            comparison_rows.append({"selection_key": meta["selection_key"], **item})
        resource_rows.append({
            "selection_key": meta["selection_key"], "n_data": meta["n_data"], "n_random": meta["n_random"],
            "wall_seconds": meta["wall_seconds"], "max_rss_gib": meta["max_rss_gib"],
        })
        cells.append((path, meta["selection_key"] + ".npz"))

    def write_tsv(path, rows):
        fields = list(rows[0])
        temp = path.with_name(path.name + ".tmp")
        with temp.open("x", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
            writer.writeheader(); writer.writerows(rows)
        os.replace(temp, path)

    write_tsv(ROOT / "R3_COVARIANCE_SUMMARY.tsv", summary_rows)
    write_tsv(ROOT / "R3_CENTRAL_ENGINE_COMPARISON.tsv", comparison_rows)
    write_tsv(ROOT / "R3_RESOURCE_OBSERVED.tsv", resource_rows)
    final_dir.mkdir()
    for source, name in cells:
        shutil.copyfile(source, final_dir / name)
    shutil.copyfile(runlog, ROOT / "R3_RUN.log")

    result = {
        "status": "OBSERVED__R3_COVARIANCE_ATLAS_ASSEMBLED__VERIFICATION_PENDING",
        "selection_count": 194,
        "lane_count": len(LANES),
        "nside_count": len(NSIDES),
        "angular_bin_count": NBIN,
        "covariance_count": len(summary_rows),
        "central_component_comparison_count": len(comparison_rows),
        "treecorr": treecorr.__version__,
        "healpy": hp.__version__,
        "max_rss_gib": max(float(row["max_rss_gib"]) for row in resource_rows),
        "total_selection_wall_seconds": sum(float(row["wall_seconds"]) for row in resource_rows),
    }
    atomic_text(ROOT / "R3_RESULT.json", json.dumps(result, indent=2, sort_keys=True) + "\n")

    artifacts = [
        ROOT / "R3_BLOCK_ATLAS.tsv", ROOT / "R3_BLOCK_RESULT.json",
        ROOT / "R3_COVARIANCE_SUMMARY.tsv", ROOT / "R3_CENTRAL_ENGINE_COMPARISON.tsv",
        ROOT / "R3_RESOURCE_OBSERVED.tsv", ROOT / "R3_RESULT.json", ROOT / "R3_RUN.log",
    ] + [final_dir / name for _, name in cells]
    manifest = ROOT / "R3_OUTPUT_MANIFEST.tsv"
    lines = ["artifact\tbytes\tsha256"]
    for path in artifacts:
        lines.append(f"{path.relative_to(ROOT)}\t{path.stat().st_size}\t{sha256(path)}")
    atomic_text(manifest, "\n".join(lines) + "\n")
    print(f"PASS: assembled R3 ({len(cells)} cells, {len(summary_rows)} covariances)")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("components", "assemble", "all"), default="all")
    parser.add_argument("--checkpoint-dir", type=Path, required=True)
    args = parser.parse_args()
    runlog = args.checkpoint_dir / "R3_RUN.log"
    if args.phase in ("components", "all"):
        execute(args.checkpoint_dir, runlog)
    if args.phase in ("assemble", "all"):
        assemble(args.checkpoint_dir, runlog)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

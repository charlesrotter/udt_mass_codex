#!/usr/bin/env python3
"""R1 BOSS ingestion and random-only Landy--Szalay controls.

This program is outcome-blind with respect to the galaxy angular pattern. Galaxy coordinates are
never sent to a pair counter. See R1_EXECUTION_CONTRACT.md.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import math
import os
import re
import resource
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import scipy
from scipy.spatial import cKDTree


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "DATA_MANIFEST.tsv"
EDGES_DEG = np.arange(0.25, 30.0001, 0.25, dtype=np.float64)
EDGES_CHORD = 2.0 * np.sin(np.deg2rad(EDGES_DEG) / 2.0)
RANDOM_RATIO = 5
REPLICATES = 2
RSS_STOP_GIB = 12.0
CHUNK_ROWS = 131_072

FINAL_NAMES = [
    "R1_FILE_INGESTION_SUMMARY.tsv",
    "R1_INGESTION_ATLAS.tsv",
    "R1_RANDOM_NULL_ATLAS.tsv",
    "R1_RANDOM_NULL_SUMMARY.tsv",
    "R1_ENGINE_ANCHOR_INPUTS.npz",
    "R1_ENGINE_ANCHOR.tsv",
    "R1_RESOURCE_OBSERVED.tsv",
    "R1_RESULT.json",
    "R1_RUN.log",
]

WEIGHT_FIELDS = ["WEIGHT_CP", "WEIGHT_NOZ", "WEIGHT_SYSTOT"]
WEIGHT_LANES = ["W0_UNIT", "W1_SPECTRO", "W2_IMAGING", "W3_OFFICIAL_OBS"]


@dataclass(frozen=True)
class Entry:
    sample: str
    cap: str
    kind: str
    path: Path
    nbytes: int
    rows: int
    sha256: str


def log(message: str, handle=None) -> None:
    stamp = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    line = f"[{stamp}] {message}"
    print(line, flush=True)
    if handle is not None:
        handle.write(line + "\n")
        handle.flush()


def current_rss_gib() -> float:
    # Linux ru_maxrss is KiB.
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024.0**2)


def enforce_rss() -> None:
    rss = current_rss_gib()
    if rss > RSS_STOP_GIB:
        raise MemoryError(f"registered RSS stop exceeded: {rss:.3f} GiB > {RSS_STOP_GIB:.3f} GiB")


def read_manifest() -> list[Entry]:
    out: list[Entry] = []
    with MANIFEST.open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            out.append(
                Entry(
                    row["sample"],
                    row["cap"],
                    row["kind"],
                    Path(row["path"]),
                    int(row["bytes"]),
                    int(row["rows"]),
                    row["sha256"],
                )
            )
    return out


def _parse_value(card: bytes):
    text = card.decode("ascii")
    if text[8:10] != "= ":
        return None
    raw = text[10:80].split("/", 1)[0].strip()
    if raw.startswith("'"):
        return raw.strip().strip("'").rstrip()
    if raw in {"T", "F"}:
        return raw == "T"
    try:
        return int(raw)
    except ValueError:
        try:
            return float(raw.replace("D", "E"))
        except ValueError:
            return raw


def _read_header(handle) -> dict[str, object]:
    cards: list[bytes] = []
    while True:
        block = handle.read(2880)
        if len(block) != 2880:
            raise EOFError("truncated FITS header")
        cards.extend(block[i : i + 80] for i in range(0, 2880, 80))
        if any(card[:8].decode("ascii").strip() == "END" for card in cards[-36:]):
            break
    header: dict[str, object] = {}
    for card in cards:
        key = card[:8].decode("ascii").strip()
        if key == "END":
            break
        if key:
            value = _parse_value(card)
            if value is not None:
                header[key] = value
    return header


def _data_size(header: dict[str, object]) -> int:
    naxis = int(header.get("NAXIS", 0))
    if naxis == 0:
        return 0
    count = 1
    for axis in range(1, naxis + 1):
        count *= int(header[f"NAXIS{axis}"])
    bitpix = abs(int(header.get("BITPIX", 8)))
    return count * bitpix // 8 + int(header.get("PCOUNT", 0))


def _skip_padded(handle, size: int) -> None:
    padded = ((size + 2879) // 2880) * 2880
    remaining = padded
    while remaining:
        block = handle.read(min(8 * 1024 * 1024, remaining))
        if not block:
            raise EOFError("truncated FITS data")
        remaining -= len(block)


def _field_width(tform: str) -> tuple[int, str, int]:
    match = re.fullmatch(r"\s*(\d*)([A-Z])(?:\([^)]*\))?\s*", tform)
    if not match:
        raise ValueError(f"unsupported TFORM={tform!r}")
    repeat = int(match.group(1) or 1)
    code = match.group(2)
    unit = {"L": 1, "X": 0, "B": 1, "I": 2, "J": 4, "K": 8,
            "A": 1, "E": 4, "D": 8, "C": 8, "M": 16, "P": 8, "Q": 16}[code]
    width = (repeat + 7) // 8 if code == "X" else repeat * unit
    return width, code, repeat


def _open_table(path: Path):
    handle = gzip.open(path, "rb") if path.suffix == ".gz" else path.open("rb")
    primary = _read_header(handle)
    _skip_padded(handle, _data_size(primary))
    table = _read_header(handle)
    if str(table.get("XTENSION", "")).strip() != "BINTABLE":
        handle.close()
        raise ValueError(f"first FITS extension is not BINTABLE: {path}")
    rowbytes = int(table["NAXIS1"])
    nrows = int(table["NAXIS2"])
    nfields = int(table["TFIELDS"])
    offset = 0
    fields = {}
    for number in range(1, nfields + 1):
        name = str(table[f"TTYPE{number}"]).strip()
        tform = str(table[f"TFORM{number}"]).strip()
        width, code, repeat = _field_width(tform)
        fields[name] = (offset, code, repeat, width)
        offset += width
    if offset != rowbytes:
        handle.close()
        raise ValueError(f"FITS row-width mismatch: parsed {offset}, header {rowbytes}")
    return handle, nrows, rowbytes, fields


def read_numeric_columns(path: Path, names: list[str], expected_rows: int) -> dict[str, np.ndarray]:
    handle, nrows, rowbytes, fields = _open_table(path)
    if nrows != expected_rows:
        handle.close()
        raise ValueError(f"row mismatch for {path}: {nrows} != {expected_rows}")
    missing = sorted(set(names) - set(fields))
    if missing:
        handle.close()
        raise ValueError(f"missing columns in {path}: {missing}")
    outputs = {name: np.empty(nrows, dtype=np.float64) for name in names}
    dtype_for = {"B": ">u1", "I": ">i2", "J": ">i4", "K": ">i8", "E": ">f4", "D": ">f8"}
    start = 0
    try:
        while start < nrows:
            take = min(CHUNK_ROWS, nrows - start)
            need = take * rowbytes
            payload = handle.read(need)
            while len(payload) < need:
                more = handle.read(need - len(payload))
                if not more:
                    raise EOFError(f"truncated FITS table in {path}")
                payload += more
            for name in names:
                offset, code, repeat, _ = fields[name]
                if repeat != 1 or code not in dtype_for:
                    raise ValueError(f"selected field {name} is not a scalar numeric field")
                view = np.ndarray(
                    shape=(take,), dtype=np.dtype(dtype_for[code]), buffer=payload,
                    offset=offset, strides=(rowbytes,),
                )
                outputs[name][start : start + take] = view
            start += take
    finally:
        handle.close()
    return outputs


def sample_shell_ids(sample: str) -> np.ndarray:
    return np.arange(0, 28, dtype=np.int16) if sample == "LOWZ" else np.arange(28, 55, dtype=np.int16)


def assign_shells(z: np.ndarray, sample: str) -> np.ndarray:
    out = np.full(z.size, -1, dtype=np.int16)
    finite = np.isfinite(z)
    if sample == "LOWZ":
        valid = finite & (z >= 0.15) & (z < 0.43)
    elif sample == "CMASS":
        valid = finite & (z >= 0.43) & (z <= 0.70)
    else:
        raise ValueError(sample)
    ids = np.floor((z[valid] - 0.15) / 0.01 + 1e-11).astype(np.int16)
    if sample == "CMASS":
        ids = np.minimum(ids, 54)  # include an exactly represented Z=0.70 in [0.69,0.70]
    out[valid] = ids
    return out


def shell_bounds(shell_id: int) -> tuple[float, float]:
    return 0.15 + 0.01 * shell_id, 0.15 + 0.01 * (shell_id + 1)


def weight_arrays(cols: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    one = np.ones_like(cols["Z"], dtype=np.float64)
    spectro = cols["WEIGHT_CP"] + cols["WEIGHT_NOZ"] - 1.0
    imaging = cols["WEIGHT_SYSTOT"]
    return {
        "W0_UNIT": one,
        "W1_SPECTRO": spectro,
        "W2_IMAGING": imaging,
        "W3_OFFICIAL_OBS": spectro * imaging,
    }


def splitmix64(indices: np.ndarray, seed: int) -> np.ndarray:
    with np.errstate(over="ignore"):
        z = indices.astype(np.uint64, copy=False) + np.uint64(seed) + np.uint64(0x9E3779B97F4A7C15)
        z = (z ^ (z >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)
        z = (z ^ (z >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)
        return z ^ (z >> np.uint64(31))


def unit_vectors(ra_deg: np.ndarray, dec_deg: np.ndarray) -> np.ndarray:
    ra = np.deg2rad(ra_deg)
    dec = np.deg2rad(dec_deg)
    cosd = np.cos(dec)
    return np.column_stack((cosd * np.cos(ra), cosd * np.sin(ra), np.sin(dec)))


def pair_bins(points_a: np.ndarray, points_b: np.ndarray | None = None) -> np.ndarray:
    tree_a = cKDTree(points_a)
    if points_b is None:
        ordered = tree_a.count_neighbors(tree_a, EDGES_CHORD, cumulative=False).astype(np.int64)
        bins = ordered[1:]
        if np.any(bins % 2):
            raise ArithmeticError("auto pair bin returned an odd ordered-pair count")
        return bins // 2
    tree_b = cKDTree(points_b)
    return tree_a.count_neighbors(tree_b, EDGES_CHORD, cumulative=False)[1:].astype(np.int64)


def brute_pair_bins(points_a: np.ndarray, points_b: np.ndarray | None = None) -> np.ndarray:
    if points_b is None:
        delta = points_a[:, None, :] - points_a[None, :, :]
        dist = np.sqrt(np.sum(delta * delta, axis=2))
        dist = dist[np.triu_indices(points_a.shape[0], k=1)]
    else:
        delta = points_a[:, None, :] - points_b[None, :, :]
        dist = np.sqrt(np.sum(delta * delta, axis=2)).ravel()
    return np.histogram(dist, bins=EDGES_CHORD)[0].astype(np.int64)


def engine_self_test() -> None:
    rng = np.random.default_rng(20260812)
    def directions(n):
        ra = rng.uniform(0.0, 360.0, n)
        dec = np.rad2deg(np.arcsin(rng.uniform(-1.0, 1.0, n)))
        return unit_vectors(ra, dec)
    a, b = directions(257), directions(521)
    if not np.array_equal(pair_bins(a), brute_pair_bins(a)):
        raise AssertionError("synthetic auto pair-count anchor failed")
    if not np.array_equal(pair_bins(a, b), brute_pair_bins(a, b)):
        raise AssertionError("synthetic cross pair-count anchor failed")


def atomic_tsv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    temp = path.with_suffix(path.suffix + ".tmp")
    with temp.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    temp.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=ROOT)
    args = parser.parse_args()
    outdir = args.output_dir.resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    existing = [name for name in FINAL_NAMES if (outdir / name).exists()]
    if existing:
        raise FileExistsError(f"registered final outputs already exist: {existing}")

    log_path = outdir / "R1_RUN.log"
    with log_path.open("x") as runlog:
        started = time.monotonic()
        log(f"R1 start Python={sys.version.split()[0]} NumPy={np.__version__} SciPy={scipy.__version__}", runlog)
        log("galaxy angular pair counters are disabled by construction", runlog)
        engine_self_test()
        log("synthetic cKDTree/brute-force pair-count anchor PASS", runlog)

        entries = read_manifest()
        data_entries = {(e.sample, e.cap): e for e in entries if e.kind == "data"}
        random_entries = {(e.sample, e.cap): e for e in entries if e.kind == "random"}
        if set(data_entries) != set(random_entries) or len(data_entries) != 4:
            raise ValueError("manifest does not contain four matched data/random sample-cap pairs")

        file_rows: list[dict] = []
        shell_state: dict[tuple[str, str, int], dict] = {}
        data_counts: dict[tuple[str, str, int], int] = {}
        resources: list[dict] = []

        # Data ingestion only: never pass galaxy coordinates to pair_bins.
        for key in sorted(data_entries):
            entry = data_entries[key]
            tick = time.monotonic()
            cols = read_numeric_columns(entry.path, ["RA", "DEC", "Z"] + WEIGHT_FIELDS, entry.rows)
            if not all(np.all(np.isfinite(cols[name])) for name in cols):
                raise ValueError(f"nonfinite allowed data field in {entry.path}")
            weights = weight_arrays(cols)
            if not all(np.all(np.isfinite(value)) and np.all(value > 0.0) for value in weights.values()):
                raise ValueError(f"nonpositive/nonfinite registered weight in {entry.path}")
            sid = assign_shells(cols["Z"], entry.sample)
            selected = sid >= 0
            file_rows.append({
                "sample": entry.sample, "cap": entry.cap, "kind": entry.kind,
                "rows_manifest": entry.rows, "rows_read": cols["Z"].size,
                "rows_in_scope": int(np.count_nonzero(selected)),
                "rows_outside_scope": int(np.count_nonzero(~selected)),
                "ra_min": f"{np.min(cols['RA']):.17g}", "ra_max": f"{np.max(cols['RA']):.17g}",
                "dec_min": f"{np.min(cols['DEC']):.17g}", "dec_max": f"{np.max(cols['DEC']):.17g}",
                "z_min": f"{np.min(cols['Z']):.17g}", "z_max": f"{np.max(cols['Z']):.17g}",
                "all_allowed_finite": 1, "all_registered_weights_positive": 1,
            })
            for shell_id in sample_shell_ids(entry.sample):
                mask = sid == shell_id
                n = int(np.count_nonzero(mask))
                state = {"data_count": n}
                data_counts[(entry.sample, entry.cap, int(shell_id))] = n
                for lane, values in weights.items():
                    state[f"{lane}_sumw"] = float(np.sum(values[mask], dtype=np.float64))
                    state[f"{lane}_sumw2"] = float(np.sum(values[mask] ** 2, dtype=np.float64))
                shell_state[(entry.sample, entry.cap, int(shell_id))] = state
            resources.append({
                "sample": entry.sample, "cap": entry.cap, "phase": "data_ingest",
                "wall_seconds": f"{time.monotonic()-tick:.6f}", "max_rss_gib": f"{current_rss_gib():.6f}",
            })
            enforce_rss()
            log(f"data ingest {entry.sample}/{entry.cap} complete; no galaxy pairs computed", runlog)
            del cols, weights, sid

        null_rows: list[dict] = []
        null_summaries: list[dict] = []
        anchor_rows: list[dict] = []
        anchor_arrays: dict[str, np.ndarray] = {}

        for key in sorted(random_entries):
            entry = random_entries[key]
            tick_file = time.monotonic()
            cols = read_numeric_columns(entry.path, ["RA", "DEC", "Z"], entry.rows)
            if not all(np.all(np.isfinite(cols[name])) for name in cols):
                raise ValueError(f"nonfinite allowed random field in {entry.path}")
            sid = assign_shells(cols["Z"], entry.sample)
            selected = sid >= 0
            file_rows.append({
                "sample": entry.sample, "cap": entry.cap, "kind": entry.kind,
                "rows_manifest": entry.rows, "rows_read": cols["Z"].size,
                "rows_in_scope": int(np.count_nonzero(selected)),
                "rows_outside_scope": int(np.count_nonzero(~selected)),
                "ra_min": f"{np.min(cols['RA']):.17g}", "ra_max": f"{np.max(cols['RA']):.17g}",
                "dec_min": f"{np.min(cols['DEC']):.17g}", "dec_max": f"{np.max(cols['DEC']):.17g}",
                "z_min": f"{np.min(cols['Z']):.17g}", "z_max": f"{np.max(cols['Z']):.17g}",
                "all_allowed_finite": 1, "all_registered_weights_positive": "NA",
            })
            seed = int(entry.sha256[:16], 16)
            hashes = splitmix64(np.arange(entry.rows, dtype=np.uint64), seed)

            for shell_id in sample_shell_ids(entry.sample):
                tick_shell = time.monotonic()
                shell_id = int(shell_id)
                state = shell_state[(entry.sample, entry.cap, shell_id)]
                candidates = np.flatnonzero(sid == shell_id)
                n_random = int(candidates.size)
                n_data = data_counts[(entry.sample, entry.cap, shell_id)]
                state["random_count"] = n_random
                if n_data == 0:
                    state["r1_status"] = "UNSAMPLED_DATA"
                    continue
                needed = REPLICATES * (1 + RANDOM_RATIO) * n_data
                if n_random < needed:
                    state["r1_status"] = "INSUFFICIENT_RANDOM_FOR_FROZEN_PARTITIONS"
                    raise ValueError(
                        f"{entry.sample}/{entry.cap}/shell{shell_id}: random {n_random} < required {needed}"
                    )
                h_shell = hashes[candidates]
                chosen_local = np.argpartition(h_shell, needed - 1)[:needed]
                chosen_local = chosen_local[np.argsort(h_shell[chosen_local], kind="stable")]
                chosen = candidates[chosen_local]
                state["r1_status"] = "SAMPLED"
                rep_records = []
                for replicate in range(REPLICATES):
                    block = (1 + RANDOM_RATIO) * n_data
                    lo = replicate * block
                    data_index = chosen[lo : lo + n_data]
                    random_index = chosen[lo + n_data : lo + block]
                    p_data = unit_vectors(cols["RA"][data_index], cols["DEC"][data_index])
                    p_random = unit_vectors(cols["RA"][random_index], cols["DEC"][random_index])
                    dd = pair_bins(p_data)
                    dr = pair_bins(p_data, p_random)
                    rr = pair_bins(p_random)
                    if np.any(rr <= 0):
                        raise ArithmeticError(
                            f"nonpositive RR in {entry.sample}/{entry.cap}/shell{shell_id}/rep{replicate}"
                        )
                    dd_total = n_data * (n_data - 1) / 2.0
                    dr_total = n_data * (RANDOM_RATIO * n_data)
                    nr = RANDOM_RATIO * n_data
                    rr_total = nr * (nr - 1) / 2.0
                    ddn, drn, rrn = dd / dd_total, dr / dr_total, rr / rr_total
                    w = (ddn - 2.0 * drn + rrn) / rrn
                    sigma = np.sqrt(1.0 / np.maximum(dd, 1) + 4.0 / np.maximum(dr, 1) + 1.0 / rr)
                    zproxy = w / sigma
                    rep_records.append((w, sigma))
                    z_lo, z_hi = shell_bounds(shell_id)
                    for bin_id in range(w.size):
                        null_rows.append({
                            "sample": entry.sample, "cap": entry.cap, "shell_id": shell_id,
                            "z_lo": f"{z_lo:.2f}", "z_hi": f"{z_hi:.2f}",
                            "replicate": replicate, "random_ratio": RANDOM_RATIO,
                            "theta_lo_deg": f"{EDGES_DEG[bin_id]:.2f}",
                            "theta_hi_deg": f"{EDGES_DEG[bin_id+1]:.2f}",
                            "dd_raw": int(dd[bin_id]), "dr_raw": int(dr[bin_id]), "rr_raw": int(rr[bin_id]),
                            "dd_norm": f"{ddn[bin_id]:.17g}", "dr_norm": f"{drn[bin_id]:.17g}",
                            "rr_norm": f"{rrn[bin_id]:.17g}", "w_null": f"{w[bin_id]:.17g}",
                            "sigma_proxy": f"{sigma[bin_id]:.17g}", "z_proxy": f"{zproxy[bin_id]:.17g}",
                        })
                    null_summaries.append({
                        "sample": entry.sample, "cap": entry.cap, "shell_id": shell_id,
                        "replicate": replicate, "n_pseudo_data": n_data,
                        "n_pseudo_random": nr, "max_abs_w": f"{np.max(np.abs(w)):.17g}",
                        "rms_w": f"{np.sqrt(np.mean(w*w)):.17g}",
                        "max_abs_z_proxy": f"{np.max(np.abs(zproxy)):.17g}",
                        "rms_z_proxy": f"{np.sqrt(np.mean(zproxy*zproxy)):.17g}",
                        "min_rr_raw": int(np.min(rr)),
                        "within_registered_guard": int(
                            np.max(np.abs(zproxy)) <= 12.0 and np.sqrt(np.mean(zproxy*zproxy)) <= 3.0
                        ),
                    })

                    if shell_id == int(sample_shell_ids(entry.sample)[0]) and replicate == 0:
                        ad = p_data[: min(128, p_data.shape[0])].copy()
                        ar = p_random[: min(256, p_random.shape[0])].copy()
                        label = f"{entry.sample}_{entry.cap}"
                        anchor_arrays[f"{label}_data"] = ad
                        anchor_arrays[f"{label}_random"] = ar
                        for family, fast, exact in [
                            ("DD", pair_bins(ad), brute_pair_bins(ad)),
                            ("DR", pair_bins(ad, ar), brute_pair_bins(ad, ar)),
                            ("RR", pair_bins(ar), brute_pair_bins(ar)),
                        ]:
                            anchor_rows.append({
                                "sample": entry.sample, "cap": entry.cap, "family": family,
                                "n_a": ad.shape[0] if family != "RR" else ar.shape[0],
                                "n_b": "NA" if family != "DR" else ar.shape[0],
                                "fast_counts_csv": ",".join(str(int(x)) for x in fast),
                                "brute_counts_csv": ",".join(str(int(x)) for x in exact),
                                "max_abs_count_difference": int(np.max(np.abs(fast - exact))),
                                "all_bins_exact": int(np.array_equal(fast, exact)),
                            })

                w0, s0 = rep_records[0]
                w1, s1 = rep_records[1]
                dz = (w0 - w1) / np.sqrt(s0 * s0 + s1 * s1)
                null_summaries.append({
                    "sample": entry.sample, "cap": entry.cap, "shell_id": shell_id,
                    "replicate": "DIFFERENCE_0_MINUS_1", "n_pseudo_data": n_data,
                    "n_pseudo_random": RANDOM_RATIO * n_data,
                    "max_abs_w": f"{np.max(np.abs(w0-w1)):.17g}",
                    "rms_w": f"{np.sqrt(np.mean((w0-w1)**2)):.17g}",
                    "max_abs_z_proxy": f"{np.max(np.abs(dz)):.17g}",
                    "rms_z_proxy": f"{np.sqrt(np.mean(dz*dz)):.17g}",
                    "min_rr_raw": "NA",
                    "within_registered_guard": int(
                        np.max(np.abs(dz)) <= 12.0 and np.sqrt(np.mean(dz*dz)) <= 3.0
                    ),
                })
                resources.append({
                    "sample": entry.sample, "cap": entry.cap, "phase": f"random_null_shell_{shell_id:02d}",
                    "wall_seconds": f"{time.monotonic()-tick_shell:.6f}",
                    "max_rss_gib": f"{current_rss_gib():.6f}",
                })
                enforce_rss()
                log(
                    f"random null {entry.sample}/{entry.cap} shell={shell_id:02d} "
                    f"N_D={n_data} N_R={n_random} complete",
                    runlog,
                )
                del candidates, h_shell, chosen_local, chosen

            resources.append({
                "sample": entry.sample, "cap": entry.cap, "phase": "random_file_total",
                "wall_seconds": f"{time.monotonic()-tick_file:.6f}", "max_rss_gib": f"{current_rss_gib():.6f}",
            })
            del cols, sid, hashes
            enforce_rss()

        ingestion_rows: list[dict] = []
        for sample, cap, shell_id in sorted(shell_state):
            z_lo, z_hi = shell_bounds(shell_id)
            state = shell_state[(sample, cap, shell_id)]
            row = {
                "sample": sample, "cap": cap, "shell_id": shell_id,
                "z_lo": f"{z_lo:.2f}", "z_hi": f"{z_hi:.2f}",
                "data_count": state["data_count"], "random_count": state.get("random_count", "NA"),
                "r1_status": state.get("r1_status", "NOT_RUN"),
            }
            for lane in WEIGHT_LANES:
                row[f"{lane}_sumw"] = f"{state[f'{lane}_sumw']:.17g}"
                row[f"{lane}_sumw2"] = f"{state[f'{lane}_sumw2']:.17g}"
            ingestion_rows.append(row)

        file_fields = [
            "sample", "cap", "kind", "rows_manifest", "rows_read", "rows_in_scope", "rows_outside_scope",
            "ra_min", "ra_max", "dec_min", "dec_max", "z_min", "z_max",
            "all_allowed_finite", "all_registered_weights_positive",
        ]
        ingestion_fields = [
            "sample", "cap", "shell_id", "z_lo", "z_hi", "data_count", "random_count", "r1_status",
        ] + [f"{lane}_{stat}" for lane in WEIGHT_LANES for stat in ("sumw", "sumw2")]
        null_fields = [
            "sample", "cap", "shell_id", "z_lo", "z_hi", "replicate", "random_ratio",
            "theta_lo_deg", "theta_hi_deg", "dd_raw", "dr_raw", "rr_raw", "dd_norm", "dr_norm",
            "rr_norm", "w_null", "sigma_proxy", "z_proxy",
        ]
        summary_fields = [
            "sample", "cap", "shell_id", "replicate", "n_pseudo_data", "n_pseudo_random",
            "max_abs_w", "rms_w", "max_abs_z_proxy", "rms_z_proxy", "min_rr_raw",
            "within_registered_guard",
        ]
        anchor_fields = [
            "sample", "cap", "family", "n_a", "n_b", "fast_counts_csv", "brute_counts_csv",
            "max_abs_count_difference", "all_bins_exact",
        ]
        resource_fields = ["sample", "cap", "phase", "wall_seconds", "max_rss_gib"]

        atomic_tsv(outdir / "R1_FILE_INGESTION_SUMMARY.tsv", file_fields, file_rows)
        atomic_tsv(outdir / "R1_INGESTION_ATLAS.tsv", ingestion_fields, ingestion_rows)
        atomic_tsv(outdir / "R1_RANDOM_NULL_ATLAS.tsv", null_fields, null_rows)
        atomic_tsv(outdir / "R1_RANDOM_NULL_SUMMARY.tsv", summary_fields, null_summaries)
        atomic_tsv(outdir / "R1_ENGINE_ANCHOR.tsv", anchor_fields, anchor_rows)
        atomic_tsv(outdir / "R1_RESOURCE_OBSERVED.tsv", resource_fields, resources)
        np.savez_compressed(outdir / "R1_ENGINE_ANCHOR_INPUTS.npz", **anchor_arrays)

        guards_pass = all(int(row["within_registered_guard"]) == 1 for row in null_summaries)
        anchors_pass = all(int(row["all_bins_exact"]) == 1 for row in anchor_rows)
        result = {
            "status": (
                "OBSERVED__R1_RANDOM_NULL_CONTROLS_PASS" if guards_pass and anchors_pass
                else "OBSERVED__R1_RANDOM_OR_ESTIMATOR_CONTAMINATION_TO_AUDIT"
            ),
            "galaxy_pair_counts_computed": False,
            "fine_shells": len(ingestion_rows),
            "sampled_shells": sum(row["r1_status"] == "SAMPLED" for row in ingestion_rows),
            "null_curve_count": sum(str(row["replicate"]).isdigit() for row in null_summaries),
            "null_bin_rows": len(null_rows),
            "registered_guards_pass": guards_pass,
            "independent_actual_catalog_pair_anchors_pass": anchors_pass,
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "angular_bin_count": len(EDGES_DEG) - 1,
            "random_ratio": RANDOM_RATIO,
            "replicates": REPLICATES,
            "max_rss_gib": current_rss_gib(),
            "wall_seconds": time.monotonic() - started,
        }
        result_path = outdir / "R1_RESULT.json"
        temp = result_path.with_suffix(".json.tmp")
        temp.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        temp.replace(result_path)
        log(f"R1 finished: {result['status']}", runlog)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Independent full-output and pair-engine verification for R2."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np
import treecorr

import run_r1_ingestion_nulls as r1


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "R2_VERIFICATION_RESULT.json"
EDGES = np.arange(0.25, 30.0001, 0.25, dtype=np.float64)
CENTERS = (EDGES[:-1] + EDGES[1:]) / 2.0
LANES = ("W0_UNIT", "W1_SPECTRO", "W2_IMAGING", "W3_OFFICIAL_OBS")
RATIOS = (5, 10, 20)


def read_tsv(name):
    with (ROOT / name).open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def close(a, b, rtol=2e-12, atol=1e-15):
    return np.allclose(a, b, rtol=rtol, atol=atol)


def own_extrema(w):
    out = []
    for i in range(1, len(w) - 1):
        if w[i] > w[i - 1] and w[i] > w[i + 1]:
            out.append(("STRICT_MAX", i, i, CENTERS[i], w[i]))
        if w[i] < w[i - 1] and w[i] < w[i + 1]:
            out.append(("STRICT_MIN", i, i, CENTERS[i], w[i]))
    i = 0
    while i < len(w) - 1:
        if w[i + 1] == w[i]:
            j = i + 1
            while j + 1 < len(w) and w[j + 1] == w[i]:
                j += 1
            out.append(("EXACT_PLATEAU", i, j, (CENTERS[i] + CENTERS[j]) / 2.0, w[i]))
            i = j
        i += 1
    for i in range(len(w) - 1):
        if w[i] == 0.0:
            out.append(("EXACT_ZERO", i, i, CENTERS[i], 0.0))
        elif w[i] * w[i + 1] < 0.0:
            theta = CENTERS[i] - w[i] * (CENTERS[i + 1] - CENTERS[i]) / (w[i + 1] - w[i])
            out.append(("LINEAR_SIGN_CROSSING", i, i + 1, theta, 0.0))
    if w[-1] == 0.0:
        out.append(("EXACT_ZERO", len(w) - 1, len(w) - 1, CENTERS[-1], 0.0))
    return out


def own_lag(values):
    x = values - np.sum(values) / len(values)
    energy = float(np.sum(x * x))
    if energy == 0.0:
        return np.r_[1.0, np.zeros(len(values) - 1)], 1
    return np.asarray([np.sum(x[: len(x) - k] * x[k:]) / energy for k in range(len(x))]), 0


def dct_matrix(n=119):
    j = np.arange(n)[None, :]
    k = np.arange(n)[:, None]
    matrix = np.cos(np.pi * (j + 0.5) * k / n) * math.sqrt(2.0 / n)
    matrix[0, :] = 1.0 / math.sqrt(n)
    return matrix


def own_shell_ids(z, sample):
    out = np.full(len(z), -1, dtype=np.int16)
    if sample == "LOWZ":
        valid = np.isfinite(z) & (z >= 0.15) & (z < 0.43)
    else:
        valid = np.isfinite(z) & (z >= 0.43) & (z <= 0.70)
    ids = np.floor((z[valid] - 0.15) / 0.01 + 1e-11).astype(np.int16)
    if sample == "CMASS":
        ids = np.minimum(ids, 54)
    out[valid] = ids
    return out


def own_splitmix(indices, seed):
    with np.errstate(over="ignore"):
        x = indices.astype(np.uint64) + np.uint64(seed) + np.uint64(0x9E3779B97F4A7C15)
        x = (x ^ (x >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)
        x = (x ^ (x >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)
        return x ^ (x >> np.uint64(31))


def tc_count(auto, ra1, dec1, w1, ra2=None, dec2=None, w2=None):
    cfg = dict(
        min_sep=0.25, max_sep=30.0, nbins=119, sep_units="degrees", bin_type="Linear",
        bin_slop=0.0, angle_slop=0.0, brute=False,
    )
    c1 = treecorr.Catalog(ra=ra1, dec=dec1, ra_units="degrees", dec_units="degrees", w=w1)
    nn = treecorr.NNCorrelation(**cfg)
    if auto:
        nn.process(c1, metric="Arc", num_threads=8, corr_only=False)
    else:
        c2 = treecorr.Catalog(ra=ra2, dec=dec2, ra_units="degrees", dec_units="degrees", w=w2)
        nn.process(c1, c2, metric="Arc", num_threads=8, corr_only=False)
    return nn.npairs.astype(np.int64), nn.weight.astype(np.float64)


def direct_count(auto, ra1, dec1, w1, ra2=None, dec2=None, w2=None):
    rb, db, wb = (ra1, dec1, w1) if auto else (ra2, dec2, w2)
    dot = (
        np.sin(np.deg2rad(dec1))[:, None] * np.sin(np.deg2rad(db))[None, :]
        + np.cos(np.deg2rad(dec1))[:, None] * np.cos(np.deg2rad(db))[None, :]
        * np.cos(np.deg2rad(ra1)[:, None] - np.deg2rad(rb)[None, :])
    )
    theta = np.rad2deg(np.arccos(np.clip(dot, -1.0, 1.0)))
    weights = w1[:, None] * wb[None, :]
    if auto:
        upper = np.triu_indices(len(ra1), 1)
        theta, weights = theta[upper], weights[upper]
    else:
        theta, weights = theta.ravel(), weights.ravel()
    return np.histogram(theta, bins=EDGES)[0], np.histogram(theta, bins=EDGES, weights=weights)[0]


def load_components():
    components = defaultdict(lambda: {"count": [], "weight": [], "norm": None})
    with (ROOT / "R2_PAIR_COMPONENT_ATLAS.tsv").open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            ratio = row["ratio"] if row["ratio"] == "NA" else int(row["ratio"])
            key = (
                row["sample"], row["cap"], int(row["factor"]), int(row["group"]),
                row["component"], ratio, row["lane"],
            )
            item = components[key]
            item["count"].append(int(row["raw_npairs"]))
            item["weight"].append(float(row["raw_weighted_sum"]))
            norm = float(row["normalization"])
            if item["norm"] is None:
                item["norm"] = norm
            else:
                assert item["norm"] == norm
    assert len(components) == 194 * 19
    for item in components.values():
        assert len(item["count"]) == len(item["weight"]) == 119
        item["count"] = np.asarray(item["count"], dtype=np.int64)
        item["weight"] = np.asarray(item["weight"], dtype=np.float64)
        assert item["norm"] > 0.0
    return components


def load_and_verify_curves(components):
    curves = defaultdict(list)
    metadata = {}
    with (ROOT / "R2_CURVE_ATLAS.tsv").open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            cid = row["curve_id"]
            key = (row["sample"], row["cap"], int(row["factor"]), int(row["group"]))
            lane, ratio = row["lane"], int(row["ratio"])
            dd = components[key + ("DD", "NA", lane)]
            dr = components[key + ("DR", ratio, lane)]
            rr = components[key + ("RR", ratio, "RANDOM_UNIT")]
            b = len(curves[cid])
            assert b < 119
            assert int(row["dd_raw"]) == dd["count"][b]
            assert int(row["dr_raw"]) == dr["count"][b]
            assert int(row["rr_raw"]) == rr["count"][b] and rr["count"][b] > 0
            assert close(float(row["dd_weighted"]), dd["weight"][b])
            assert close(float(row["dr_weighted"]), dr["weight"][b])
            assert close(float(row["rr_weighted"]), rr["weight"][b])
            ddn, drn, rrn = dd["weight"][b] / dd["norm"], dr["weight"][b] / dr["norm"], rr["weight"][b] / rr["norm"]
            w = (ddn - 2.0 * drn + rrn) / rrn
            assert close(float(row["dd_norm"]), ddn)
            assert close(float(row["dr_norm"]), drn)
            assert close(float(row["rr_norm"]), rrn)
            assert close(float(row["w_theta"]), w)
            curves[cid].append(w)
            metadata[cid] = (row["sample"], row["cap"], int(row["factor"]), int(row["group"]), lane, ratio)
    assert len(curves) == 2328
    for cid in list(curves):
        assert len(curves[cid]) == 119
        curves[cid] = np.asarray(curves[cid], dtype=np.float64)
    return curves, metadata


def verify_descriptors(curves):
    rows = read_tsv("R2_DESCRIPTOR_ATLAS.tsv")
    assert len(rows) == 2328
    for row in rows:
        w = curves[row["curve_id"]]
        features = own_extrema(w)
        kinds = [x[0] for x in features]
        expected = {
            "mean": np.mean(w), "rms": np.sqrt(np.mean(w * w)),
            "total_variation": np.sum(np.abs(np.diff(w))),
            "first_difference_rms": np.sqrt(np.mean(np.diff(w) ** 2)),
            "second_difference_rms": np.sqrt(np.mean(np.diff(w, n=2) ** 2)),
        }
        for field, value in expected.items():
            assert close(float(row[field]), value)
        assert int(row["strict_max_count"]) == kinds.count("STRICT_MAX")
        assert int(row["strict_min_count"]) == kinds.count("STRICT_MIN")
        assert int(row["plateau_count"]) == kinds.count("EXACT_PLATEAU")
        assert int(row["zero_crossing_count"]) == kinds.count("LINEAR_SIGN_CROSSING") + kinds.count("EXACT_ZERO")

    actual_features = defaultdict(list)
    for row in read_tsv("R2_EXTREMA_CROSSING_ATLAS.tsv"):
        actual_features[row["curve_id"]].append((
            row["kind"], int(row["bin_start"]), int(row["bin_end"]), float(row["theta_deg"]), float(row["value"])
        ))
    for cid, w in curves.items():
        expected = own_extrema(w)
        actual = actual_features[cid]
        assert len(actual) == len(expected)
        for got, want in zip(actual, expected):
            assert got[:3] == want[:3] and close(got[3], want[3]) and close(got[4], want[4])

    matrix = dct_matrix()
    actual_dct = defaultdict(list)
    for row in read_tsv("R2_DCT_ATLAS.tsv"):
        actual_dct[row["curve_id"]].append((int(row["coefficient"]), float(row["value"])))
    for cid, w in curves.items():
        values = sorted(actual_dct[cid])
        assert [x[0] for x in values] == list(range(119))
        assert close(np.asarray([x[1] for x in values]), matrix @ w, rtol=2e-11, atol=2e-14)

    actual_lag = defaultdict(list)
    for row in read_tsv("R2_LAG_ATLAS.tsv"):
        actual_lag[(row["curve_id"], row["series"])].append(
            (int(row["lag_bins"]), float(row["value"]), int(row["degenerate"]))
        )
    for cid, w in curves.items():
        for series, values in (("MEAN_CENTERED_RAW", w), ("MEAN_CENTERED_FIRST_DIFFERENCE", np.diff(w))):
            expected, degenerate = own_lag(values)
            actual = sorted(actual_lag[(cid, series)])
            assert [x[0] for x in actual] == list(range(len(expected)))
            assert all(x[2] == degenerate for x in actual)
            assert close(np.asarray([x[1] for x in actual]), expected)


def verify_consistency(curves, metadata):
    by_query = {value: curves[cid] for cid, value in metadata.items()}
    rows = read_tsv("R2_CONSISTENCY_SUMMARY.tsv")
    assert len(rows) == 4462
    for row in rows:
        sample, factor, group = row["sample"], int(row["factor"]), int(row["group"])
        if row["comparison"] == "RANDOM_DENSITY":
            cap, lane = row["cap_or_pair"], row["lane_or_pair"]
            low, high = (int(x) for x in row["ratio_or_pair"].split("-"))
            delta = by_query[(sample, cap, factor, group, lane, low)] - by_query[(sample, cap, factor, group, lane, high)]
        elif row["comparison"] == "WEIGHT_LANE":
            cap = row["cap_or_pair"]
            lane, _ = row["lane_or_pair"].split("-", 1)
            ratio = int(row["ratio_or_pair"])
            delta = by_query[(sample, cap, factor, group, lane, ratio)] - by_query[(sample, cap, factor, group, "W0_UNIT", ratio)]
        else:
            lane, ratio = row["lane_or_pair"], int(row["ratio_or_pair"])
            delta = by_query[(sample, "North", factor, group, lane, ratio)] - by_query[(sample, "South", factor, group, lane, ratio)]
        assert close(float(row["max_abs_difference"]), np.max(np.abs(delta)))
        assert close(float(row["rms_difference"]), np.sqrt(np.mean(delta * delta)))


def anchor_indices(sample, cap, factor, group_number, ratio):
    entries = r1.read_manifest()
    de = next(e for e in entries if e.sample == sample and e.cap == cap and e.kind == "data")
    re = next(e for e in entries if e.sample == sample and e.cap == cap and e.kind == "random")
    data = r1.read_numeric_columns(de.path, ["RA", "DEC", "Z"] + r1.WEIGHT_FIELDS, de.rows)
    random = r1.read_numeric_columns(re.path, ["RA", "DEC", "Z"], re.rows)
    ids = np.arange(0, 28) if sample == "LOWZ" else np.arange(28, 55)
    members = ids[group_number * factor : (group_number + 1) * factor]
    ds, rs = own_shell_ids(data["Z"], sample), own_shell_ids(random["Z"], sample)
    di = np.flatnonzero((ds >= members[0]) & (ds <= members[-1]))
    candidates = np.flatnonzero((rs >= members[0]) & (rs <= members[-1]))
    hashes = own_splitmix(np.arange(re.rows, dtype=np.uint64), int(re.sha256[:16], 16))
    need = 20 * len(di)
    local = np.argpartition(hashes[candidates], need - 1)[:need]
    local = local[np.lexsort((candidates[local], hashes[candidates][local]))]
    ri = candidates[local[: ratio * len(di)]]
    spectro = data["WEIGHT_CP"] + data["WEIGHT_NOZ"] - 1.0
    weights = {
        "W0_UNIT": np.ones(len(data["Z"])), "W1_SPECTRO": spectro,
        "W2_IMAGING": data["WEIGHT_SYSTOT"], "W3_OFFICIAL_OBS": spectro * data["WEIGHT_SYSTOT"],
    }
    return data, random, di, ri, weights


def verify_pair_anchors(components):
    anchors = (
        ("LOWZ", "South", 1, 0, "W3_OFFICIAL_OBS", 5),
        ("CMASS", "North", 1, 7, "W3_OFFICIAL_OBS", 20),
        ("CMASS", "South", 4, 0, "W1_SPECTRO", 10),
    )
    records = []
    for sample, cap, factor, group, lane, ratio in anchors:
        data, random, di, ri, weights = anchor_indices(sample, cap, factor, group, ratio)
        w = weights[lane][di]
        cases = (
            ("DD", True, data["RA"][di], data["DEC"][di], w, None, None, None,
             components[(sample, cap, factor, group, "DD", "NA", lane)]),
            ("DR", False, data["RA"][di], data["DEC"][di], w, random["RA"][ri], random["DEC"][ri], np.ones(len(ri)),
             components[(sample, cap, factor, group, "DR", ratio, lane)]),
            ("RR", True, random["RA"][ri], random["DEC"][ri], np.ones(len(ri)), None, None, None,
             components[(sample, cap, factor, group, "RR", ratio, "RANDOM_UNIT")]),
        )
        for component, auto, ra1, dec1, w1, ra2, dec2, w2, primary in cases:
            count, weighted = tc_count(auto, ra1, dec1, w1, ra2, dec2, w2)
            exact = bool(np.array_equal(count, primary["count"]))
            absdiff = float(np.max(np.abs(weighted - primary["weight"])))
            reldiff = float(np.max(np.abs(weighted - primary["weight"]) / np.maximum(np.abs(primary["weight"]), 1.0)))
            assert exact and (reldiff <= 5e-9 or absdiff <= 1e-7)
            records.append({
                "sample": sample, "cap": cap, "factor": factor, "group": group, "lane": lane,
                "ratio": ratio, "component": component, "integer_counts_exact": exact,
                "max_weight_abs_difference": absdiff, "max_weight_relative_difference": reldiff,
            })
    return records


def verify_brute_anchors(components):
    records = []
    for sample in ("CMASS", "LOWZ"):
        for cap in ("North", "South"):
            data, random, di, ri, weights = anchor_indices(sample, cap, 1, 0, 5)
            di, ri = di[:128], ri[:256]
            w = weights["W3_OFFICIAL_OBS"][di]
            for component, auto, ra1, dec1, w1, ra2, dec2, w2 in (
                ("DD", True, data["RA"][di], data["DEC"][di], w, None, None, None),
                ("DR", False, data["RA"][di], data["DEC"][di], w, random["RA"][ri], random["DEC"][ri], np.ones(len(ri))),
                ("RR", True, random["RA"][ri], random["DEC"][ri], np.ones(len(ri)), None, None, None),
            ):
                dc, dw = direct_count(auto, ra1, dec1, w1, ra2, dec2, w2)
                tc, tw = tc_count(auto, ra1, dec1, w1, ra2, dec2, w2)
                exact = bool(np.array_equal(dc, tc))
                absdiff = float(np.max(np.abs(dw - tw)))
                reldiff = float(np.max(np.abs(dw - tw) / np.maximum(np.abs(dw), 1.0)))
                assert exact and (reldiff <= 5e-12 or absdiff <= 1e-10)
                records.append({
                    "sample": sample, "cap": cap, "component": component,
                    "integer_counts_exact": exact, "max_weight_abs_difference": absdiff,
                    "max_weight_relative_difference": reldiff,
                })
    return records


def main() -> int:
    if OUTPUT.exists():
        raise FileExistsError(OUTPUT)
    with (ROOT / "R2_OUTPUT_MANIFEST.tsv").open(newline="") as handle:
        manifest = list(csv.DictReader(handle, delimiter="\t"))
    for row in manifest:
        path = ROOT / row["artifact"]
        assert path.stat().st_size == int(row["bytes"])
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"]

    result = json.loads((ROOT / "R2_RESULT.json").read_text())
    assert result["selection_count"] == 194 and result["curve_count"] == 2328
    assert result["curve_rows"] == 2328 * 119 and result["component_rows"] == 194 * 19 * 119

    components = load_components()
    curves, metadata = load_and_verify_curves(components)
    verify_descriptors(curves)
    verify_consistency(curves, metadata)
    treecorr_records = verify_pair_anchors(components)
    brute_records = verify_brute_anchors(components)

    verification = {
        "status": "PASS",
        "primary_manifest_sha256": hashlib.sha256((ROOT / "R2_OUTPUT_MANIFEST.tsv").read_bytes()).hexdigest(),
        "component_family_count": len(components), "curve_count": len(curves),
        "all_curve_and_descriptor_rows_recomputed": True,
        "treecorr_anchor_records": treecorr_records,
        "direct_brute_anchor_records": brute_records,
        "treecorr": treecorr.__version__,
    }
    OUTPUT.write_text(json.dumps(verification, indent=2, sort_keys=True) + "\n")
    print(
        "PASS: R2 independent verification "
        f"({len(components)} components, {len(curves)} curves, "
        f"{len(treecorr_records)} TreeCorr anchors, {len(brute_records)} direct anchors)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

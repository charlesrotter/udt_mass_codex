#!/usr/bin/env python3
"""Independent post-run verification of the R3 covariance atlas."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

import healpy as hp
import numpy as np
import treecorr

import run_r1_ingestion_nulls as r1
import run_r2_central_pattern as r2
import verify_r2 as v2


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "R3_VERIFICATION_RESULT.json"
LANES = ("W0_UNIT", "W1_SPECTRO", "W2_IMAGING", "W3_OFFICIAL_OBS")
NSIDES = (4, 8, 16)
NBIN = 119


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_cell(path):
    with np.load(path, allow_pickle=False) as bundle:
        meta = json.loads(str(bundle["metadata"].item()))
        arrays = {name: bundle[name] for name in bundle.files if name != "metadata"}
    return meta, arrays


def close(a, b, rtol=2e-12, atol=2e-14):
    return np.allclose(a, b, rtol=rtol, atol=atol)


def component_matches(observed_count, observed_weight, expected):
    """Apply the exact preregistered R3 central-component gate."""
    exact = np.array_equal(observed_count, expected["count"])
    absolute = np.abs(observed_weight - expected["weight"])
    absdiff = float(np.max(absolute))
    reldiff = float(np.max(absolute / np.maximum(np.abs(expected["weight"]), 1.0)))
    weighted = reldiff <= 5e-9 or absdiff <= 1e-7
    return bool(exact and weighted)


def central_curve_from_weights(dd_weight, dr_weight, rr_weight, dd_norm, dr_norm, rr_norm):
    """Reconstruct the frozen Landy--Szalay readout from supplied components."""
    return (
        dd_weight / dd_norm - 2.0 * dr_weight / dr_norm + rr_weight / rr_norm
    ) / (rr_weight / rr_norm)


def guarded_tree_count(auto, ra1, dec1, w1, ra2=None, dec2=None, w2=None):
    """Independent unpatched TreeCorr replay with the verified outer guard."""
    config = dict(
        min_sep=0.25, max_sep=30.25, nbins=120, sep_units="degrees", bin_type="Linear",
        bin_slop=0.0, angle_slop=0.0, brute=False,
    )
    catalog1 = treecorr.Catalog(
        ra=ra1, dec=dec1, w=w1, ra_units="degrees", dec_units="degrees"
    )
    correlation = treecorr.NNCorrelation(**config)
    if auto:
        correlation.process(catalog1, metric="Arc", num_threads=8, corr_only=False)
    else:
        catalog2 = treecorr.Catalog(
            ra=ra2, dec=dec2, w=w2, ra_units="degrees", dec_units="degrees"
        )
        correlation.process(catalog1, catalog2, metric="Arc", num_threads=8, corr_only=False)
    counts_float = np.asarray(correlation.npairs, dtype=np.float64)[:NBIN]
    counts = np.rint(counts_float).astype(np.int64)
    assert np.array_equal(counts_float, counts.astype(np.float64))
    weights = np.asarray(correlation.weight, dtype=np.float64)[:NBIN]
    assert counts.shape == weights.shape == (NBIN,) and np.all(np.isfinite(weights))
    return counts, weights


def component_residual(observed_weight, expected_weight):
    absolute = np.abs(observed_weight - expected_weight)
    return {
        "max_weight_abs_difference": float(np.max(absolute)),
        "max_weight_relative_difference": float(
            np.max(absolute / np.maximum(np.abs(expected_weight), 1.0))
        ),
    }


def own_covariance_checks(covariance, k):
    assert covariance.shape == (NBIN, NBIN) and np.all(np.isfinite(covariance))
    assert np.array_equal(covariance, covariance.T)
    eig = np.linalg.eigvalsh(covariance)
    largest = float(eig[-1])
    tau = NBIN * np.finfo(np.float64).eps * largest if largest > 0.0 else 0.0
    assert eig[0] >= -100.0 * max(tau, np.finfo(np.float64).tiny)
    rank = int(sum(value > tau for value in eig.tolist()))
    assert rank <= min(NBIN, k - 1)
    return eig, tau, rank


def block_pixels():
    out = {}
    grouped = {}
    with (ROOT / "R3_BLOCK_ATLAS.tsv").open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            grouped.setdefault((row["sample"], row["cap"], int(row["nside"])), []).append(int(row["nested_pixel"]))
    for key, values in grouped.items():
        out[key] = np.asarray(values, dtype=np.int64)
    return out


def pixel(ra, dec, nside):
    return hp.ang2pix(nside, np.deg2rad(90.0 - dec), np.deg2rad(np.mod(ra, 360.0)), nest=True)


def anchor_replays(cells):
    entries = r1.read_manifest()
    de = {(e.sample, e.cap): e for e in entries if e.kind == "data"}
    re = {(e.sample, e.cap): e for e in entries if e.kind == "random"}
    blocks = block_pixels()
    records = []
    for sample in ("CMASS", "LOWZ"):
        for cap in ("North", "South"):
            data_entry, random_entry = de[(sample, cap)], re[(sample, cap)]
            data = r1.read_numeric_columns(data_entry.path, ["RA", "DEC", "Z"] + r1.WEIGHT_FIELDS, data_entry.rows)
            random = r1.read_numeric_columns(random_entry.path, ["RA", "DEC", "Z"], random_entry.rows)
            ds, rs = r1.assign_shells(data["Z"], sample), r1.assign_shells(random["Z"], sample)
            ids = np.arange(0, 28) if sample == "LOWZ" else np.arange(28, 55)
            shell = int(ids[0])
            di = np.flatnonzero(ds == shell)
            candidates = np.flatnonzero(rs == shell)
            hashes = r1.splitmix64(np.arange(random_entry.rows, dtype=np.uint64), int(random_entry.sha256[:16], 16))
            need = 20 * len(di)
            local = np.argpartition(hashes[candidates], need - 1)[:need]
            local = local[np.lexsort((candidates[local], hashes[candidates][local]))]
            ri = candidates[local]
            weights = r1.weight_arrays(data)["W3_OFFICIAL_OBS"][di]
            key = f"{sample}_{cap}_f1_g00"
            _, arrays = cells[key]
            for nside in (4, 16):
                active_pixels = arrays[f"active_pixel_n{nside}"]
                target = int(active_pixels[0])
                keep_d = pixel(data["RA"][di], data["DEC"][di], nside) != target
                keep_r = pixel(random["RA"][ri], random["DEC"][ri], nside) != target
                ddc, ddw = r2.pair_count(data["RA"][di][keep_d], data["DEC"][di][keep_d], weights[keep_d])
                drc, drw = r2.pair_count(
                    data["RA"][di][keep_d], data["DEC"][di][keep_d], weights[keep_d],
                    random["RA"][ri][keep_r], random["DEC"][ri][keep_r], np.ones(np.count_nonzero(keep_r)),
                )
                rrc, rrw = r2.pair_count(random["RA"][ri][keep_r], random["DEC"][ri][keep_r], None)
                sumw = float(np.sum(weights[keep_d], dtype=np.float64))
                sumw2 = float(np.sum(weights[keep_d] ** 2, dtype=np.float64))
                nr = int(np.count_nonzero(keep_r))
                ddn = (sumw**2 - sumw2) / 2.0
                drn = sumw * nr
                rrn = nr * (nr - 1.0) / 2.0
                tddc, tddw = guarded_tree_count(
                    True, data["RA"][di][keep_d], data["DEC"][di][keep_d], weights[keep_d]
                )
                tdrc, tdrw = guarded_tree_count(
                    False, data["RA"][di][keep_d], data["DEC"][di][keep_d], weights[keep_d],
                    random["RA"][ri][keep_r], random["DEC"][ri][keep_r], np.ones(np.count_nonzero(keep_r)),
                )
                trrc, trrw = guarded_tree_count(
                    True, random["RA"][ri][keep_r], random["DEC"][ri][keep_r],
                    np.ones(np.count_nonzero(keep_r)),
                )
                assert component_matches(tddc, tddw, {"count": ddc, "weight": ddw})
                assert component_matches(tdrc, tdrw, {"count": drc, "weight": drw})
                assert component_matches(trrc, trrw, {"count": rrc, "weight": rrw})
                corrfunc_curve = central_curve_from_weights(ddw, drw, rrw, ddn, drn, rrn)
                treecorr_curve = central_curve_from_weights(tddw, tdrw, trrw, ddn, drn, rrn)
                expected = arrays[f"anchor_leaveout_n{nside}"][0]
                assert close(treecorr_curve, expected)
                records.append({
                    "sample": sample, "cap": cap, "nside": nside, "nested_pixel": target,
                    "corrfunc_saved_curve_max_abs_difference": float(np.max(np.abs(corrfunc_curve - expected))),
                    "treecorr_saved_curve_max_abs_difference": float(np.max(np.abs(treecorr_curve - expected))),
                    "dd_pair_count": int(np.sum(ddc)), "dr_pair_count": int(np.sum(drc)), "rr_pair_count": int(np.sum(rrc)),
                    "dd_engine_residual": component_residual(tddw, ddw),
                    "dr_engine_residual": component_residual(tdrw, drw),
                    "rr_engine_residual": component_residual(trrw, rrw),
                })
    return records


def support_replays(cells):
    """Independently reconstruct every stored data/random active-block union."""
    entries = r1.read_manifest()
    de = {(e.sample, e.cap): e for e in entries if e.kind == "data"}
    re = {(e.sample, e.cap): e for e in entries if e.kind == "random"}
    blocks = block_pixels()
    records = 0
    data_only_records = 0
    data_only_blocks = 0
    for sample in ("CMASS", "LOWZ"):
        for cap in ("North", "South"):
            data_entry, random_entry = de[(sample, cap)], re[(sample, cap)]
            data = r1.read_numeric_columns(data_entry.path, ["RA", "DEC", "Z"] + r1.WEIGHT_FIELDS, data_entry.rows)
            random = r1.read_numeric_columns(random_entry.path, ["RA", "DEC", "Z"], random_entry.rows)
            ds, rs = r1.assign_shells(data["Z"], sample), r1.assign_shells(random["Z"], sample)
            hashes = r1.splitmix64(
                np.arange(random_entry.rows, dtype=np.uint64), int(random_entry.sha256[:16], 16)
            )
            all_weights = r1.weight_arrays(data)
            for group in r2.groups(sample):
                lo, hi = int(group["members"][0]), int(group["members"][-1])
                di = np.flatnonzero((ds >= lo) & (ds <= hi))
                candidates = np.flatnonzero((rs >= lo) & (rs <= hi))
                need = 20 * len(di)
                local = np.argpartition(hashes[candidates], need - 1)[:need]
                local = local[np.lexsort((candidates[local], hashes[candidates][local]))]
                ri = candidates[local]
                key = f"{sample}_{cap}_f{int(group['factor'])}_g{int(group['group']):02d}"
                _, arrays = cells[key]
                for nside in NSIDES:
                    footprint = blocks[(sample, cap, nside)]
                    dpix = pixel(data["RA"][di], data["DEC"][di], nside)
                    rpix = pixel(random["RA"][ri], random["DEC"][ri], nside)
                    dlabel = np.searchsorted(footprint, dpix)
                    rlabel = np.searchsorted(footprint, rpix)
                    assert np.all(dlabel < len(footprint)) and np.all(footprint[dlabel] == dpix)
                    assert np.all(rlabel < len(footprint)) and np.all(footprint[rlabel] == rpix)
                    nd = np.bincount(dlabel, minlength=len(footprint)).astype(np.int64)
                    nr = np.bincount(rlabel, minlength=len(footprint)).astype(np.int64)
                    active = (nd > 0) | (nr > 0)
                    assert np.array_equal(arrays[f"active_pixel_n{nside}"], footprint[active])
                    assert np.array_equal(arrays[f"data_count_n{nside}"], nd[active])
                    assert np.array_equal(arrays[f"random_count_n{nside}"], nr[active])
                    for lane_index, lane in enumerate(LANES):
                        w = all_weights[lane][di]
                        sumw = np.bincount(dlabel, weights=w, minlength=len(footprint))[active]
                        sumw2 = np.bincount(dlabel, weights=w * w, minlength=len(footprint))[active]
                        assert close(arrays[f"data_sumw_n{nside}"][lane_index], sumw)
                        assert close(arrays[f"data_sumw2_n{nside}"][lane_index], sumw2)
                    missing = (nd > 0) & (nr == 0)
                    if np.any(missing):
                        data_only_records += 1
                        data_only_blocks += int(np.count_nonzero(missing))
                    records += 1
    assert records == 194 * 3
    assert data_only_records == 17 and data_only_blocks == 17
    return {
        "selection_resolution_records": records,
        "data_only_selection_resolution_records": data_only_records,
        "data_only_blocks": data_only_blocks,
    }


def main() -> int:
    if OUTPUT.exists():
        raise FileExistsError(OUTPUT)
    with (ROOT / "R3_OUTPUT_MANIFEST.tsv").open(newline="") as handle:
        manifest = list(csv.DictReader(handle, delimiter="\t"))
    for row in manifest:
        path = ROOT / row["artifact"]
        assert path.stat().st_size == int(row["bytes"])
        assert digest(path) == row["sha256"]
    result = json.loads((ROOT / "R3_RESULT.json").read_text())
    assert result["selection_count"] == 194 and result["covariance_count"] == 194 * 4 * 3
    assert result["central_component_comparison_count"] == 194 * 9

    r2_components = v2.load_components()
    summary = {}
    with (ROOT / "R3_COVARIANCE_SUMMARY.tsv").open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            summary[(row["selection_key"], row["lane"], int(row["nside"]))] = row
    assert len(summary) == 194 * 4 * 3

    cells = {}
    full_rank_counts = {str(nside): 0 for nside in NSIDES}
    anchor_covariance_replays = 0
    central_curve_max_abs_difference_from_r2 = 0.0
    central_curve_records_exceeding_removed_gate = 0
    central_curve_bins_exceeding_removed_gate = 0
    for path in sorted((ROOT / "R3_COVARIANCE_CELLS").glob("*.npz")):
        meta, arrays = read_cell(path)
        key = meta["selection_key"]
        cells[key] = (meta, arrays)
        sample, cap, factor, group = meta["sample"], meta["cap"], int(meta["factor"]), int(meta["group"])
        rr = r2_components[(sample, cap, factor, group, "RR", 20, "RANDOM_UNIT")]
        assert component_matches(arrays["central_rr_count"], arrays["central_rr_weight"], rr)
        for lane_index, lane in enumerate(LANES):
            dd = r2_components[(sample, cap, factor, group, "DD", "NA", lane)]
            dr = r2_components[(sample, cap, factor, group, "DR", 20, lane)]
            assert component_matches(
                arrays["central_dd_count"][lane_index], arrays["central_dd_weight"][lane_index], dd
            )
            assert component_matches(
                arrays["central_dr_count"][lane_index], arrays["central_dr_weight"][lane_index], dr
            )
            stored_curve = arrays["central_curve"][lane_index]
            reconstructed_curve = central_curve_from_weights(
                arrays["central_dd_weight"][lane_index],
                arrays["central_dr_weight"][lane_index],
                arrays["central_rr_weight"],
                dd["norm"], dr["norm"], rr["norm"],
            )
            assert np.array_equal(stored_curve, reconstructed_curve)
            r2_curve = central_curve_from_weights(
                dd["weight"], dr["weight"], rr["weight"], dd["norm"], dr["norm"], rr["norm"]
            )
            difference = np.abs(stored_curve - r2_curve)
            central_curve_max_abs_difference_from_r2 = max(
                central_curve_max_abs_difference_from_r2, float(np.max(difference))
            )
            removed_tolerance = 2e-10 + 5e-9 * np.abs(r2_curve)
            removed_failures = difference > removed_tolerance
            if np.any(removed_failures):
                central_curve_records_exceeding_removed_gate += 1
                central_curve_bins_exceeding_removed_gate += int(np.count_nonzero(removed_failures))
            for nside in NSIDES:
                k = len(arrays[f"active_pixel_n{nside}"])
                covariance = arrays[f"covariance_n{nside}"][lane_index]
                eig, tau, rank = own_covariance_checks(covariance, k)
                assert close(eig, arrays[f"eigenvalues_n{nside}"][lane_index], rtol=5e-10, atol=2e-14)
                assert close(tau, arrays[f"rank_tau_n{nside}"][lane_index])
                assert rank == int(arrays[f"rank_n{nside}"][lane_index])
                row = summary[(key, lane, nside)]
                assert rank == int(row["rank"]) and k == int(row["active_blocks"])
                if rank == NBIN:
                    full_rank_counts[str(nside)] += 1
                if meta["anchor"] and lane == "W3_OFFICIAL_OBS" and nside in (4, 16):
                    leaveout = arrays[f"anchor_leaveout_n{nside}"]
                    mean = np.mean(leaveout, axis=0)
                    centered = leaveout - mean
                    cov2 = ((len(leaveout) - 1.0) / len(leaveout)) * (centered.T @ centered)
                    cov2 = (cov2 + cov2.T) / 2.0
                    assert close(mean, arrays[f"jk_mean_n{nside}"][lane_index])
                    assert close(cov2, covariance, rtol=5e-11, atol=2e-14)
                    anchor_covariance_replays += 1
    assert len(cells) == 194 and anchor_covariance_replays == 8
    support = support_replays(cells)
    corrfunc_records = anchor_replays(cells)
    assert len(corrfunc_records) == 8

    verification = {
        "status": "PASS",
        "manifest_sha256": digest(ROOT / "R3_OUTPUT_MANIFEST.tsv"),
        "cell_count": len(cells),
        "covariance_count": len(summary),
        "all_central_components_replayed_against_R2": True,
        "all_central_curves_exactly_reconstructed_from_saved_components": True,
        "central_curve_r2_reconciliation": {
            "maximum_absolute_difference": central_curve_max_abs_difference_from_r2,
            "records_exceeding_removed_unpreregistered_gate": central_curve_records_exceeding_removed_gate,
            "bins_exceeding_removed_unpreregistered_gate": central_curve_bins_exceeding_removed_gate,
        },
        "anchor_covariance_replay_count": anchor_covariance_replays,
        "corrfunc_leave_one_anchor_records": corrfunc_records,
        "active_union_independent_replay": support,
        "full_rank_counts_by_nside": full_rank_counts,
    }
    OUTPUT.write_text(json.dumps(verification, indent=2, sort_keys=True) + "\n")
    print(f"PASS: R3 independent verification ({len(cells)} cells, {len(summary)} covariances, 8 leave-one anchors)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Structural verification for the preregistered R3 patch-cardinality repair."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import treecorr

import run_r3_covariance_atlas as r3


GUARDED = Path("/tmp/udt_boss_r3_checkpoints_guarded")
EXPECTED_TREECORR = "5.1.3"
EXPECTED_PRODUCTION_SHA256 = "a09d287b24ce662ced9e986d0480ffc94caf54962c3205ea81ba2a1e8b2f7840"
EXPECTED_LEGACY_PRODUCTION_SHA256 = "7806327137fc2351693855dd9a71bfe1a3541e7b67c11478f450f6c859bcbb88"


def plain_catalog(ra, dec, weights):
    return treecorr.Catalog(
        ra=np.asarray(ra, dtype=np.float64),
        dec=np.asarray(dec, dtype=np.float64),
        ra_units="degrees",
        dec_units="degrees",
        w=np.asarray(weights, dtype=np.float64),
    )


def arrays(corr):
    return r3.correlation_arrays(corr)


def same_component(left, right):
    lc, lw = arrays(left)
    rc, rw = arrays(right)
    absdiff = float(np.max(np.abs(lw - rw)))
    reldiff = float(np.max(np.abs(lw - rw) / np.maximum(np.abs(rw), 1.0)))
    if not np.array_equal(lc, rc):
        raise AssertionError("central integer component mismatch")
    if not np.allclose(lw, rw, rtol=5e-13, atol=1e-12):
        raise AssertionError(f"central weighted component mismatch: abs={absdiff} rel={reldiff}")
    return absdiff, reldiff


def check_children(parts, ra, dec, weights, patch, npatch):
    occupied = np.unique(patch)
    if [int(part.patch) for part in parts] != occupied.tolist():
        raise AssertionError("single-patch child IDs do not preserve occupied global labels")
    if {part.npatch for part in parts} != {npatch}:
        raise AssertionError("explicit child catalog lost global patch cardinality")
    covered = np.zeros(len(ra), dtype=np.int8)
    for part, patch_id in zip(parts, occupied):
        use = patch == patch_id
        covered[use] += 1
        if len(part.ra) != int(np.count_nonzero(use)):
            raise AssertionError("single-patch child row count mismatch")
        if not np.allclose(np.rad2deg(part.ra), ra[use], rtol=0.0, atol=1e-13):
            raise AssertionError("single-patch child RA membership mismatch")
        if not np.allclose(np.rad2deg(part.dec), dec[use], rtol=0.0, atol=1e-13):
            raise AssertionError("single-patch child DEC membership mismatch")
        if not np.array_equal(part.w, weights[use]):
            raise AssertionError("single-patch child weight membership mismatch")
    if not np.array_equal(covered, np.ones(len(ra), dtype=np.int8)):
        raise AssertionError("single-patch children do not cover source rows exactly once")
    return occupied.tolist()


def synthetic_check():
    data_ra = np.array([0.1, 0.8, 2.1, 2.9, 4.2, 4.8])
    data_dec = np.array([0.0, 0.2, -0.1, 0.15, -0.2, 0.05])
    data_w = np.array([1.0, 1.25, 0.75, 1.5, 0.5, 2.0])
    data_patch = np.array([0, 0, 2, 2, 7, 7], dtype=np.int32)
    random_ra = np.array([0.3, 1.2, 2.4, 3.4, 4.5, 5.2, 6.0])
    random_dec = np.array([0.1, -0.2, 0.05, 0.2, -0.15, 0.0, 0.12])
    random_w = np.ones(len(random_ra))
    random_patch = np.array([0, 0, 2, 2, 5, 5, 5], dtype=np.int32)
    npatch = 9

    legacy_data = treecorr.Catalog(
        ra=data_ra, dec=data_dec, ra_units="degrees", dec_units="degrees",
        w=data_w, patch=data_patch, npatch=npatch,
    )
    legacy_random = treecorr.Catalog(
        ra=random_ra, dec=random_dec, ra_units="degrees", dec_units="degrees",
        w=random_w, patch=random_patch, npatch=npatch,
    )
    legacy_error = None
    try:
        r3.tree_count(legacy_data, legacy_random)
    except RuntimeError as exc:
        legacy_error = str(exc)
    expected_error = "Cross correlation requires both catalogs use the same patches."
    if legacy_error != expected_error:
        raise AssertionError(f"legacy failure was not reproduced: {legacy_error!r}")

    data_parts = r3.tree_patch_catalogs(data_ra, data_dec, data_w, data_patch, npatch)
    random_parts = r3.tree_patch_catalogs(random_ra, random_dec, random_w, random_patch, npatch)
    data_ids = check_children(data_parts, data_ra, data_dec, data_w, data_patch, npatch)
    random_ids = check_children(random_parts, random_ra, random_dec, random_w, random_patch, npatch)

    corrected_dr = r3.tree_count(data_parts, random_parts)
    direct_dr = r3.tree_count(
        plain_catalog(data_ra, data_dec, data_w),
        plain_catalog(random_ra, random_dec, random_w),
    )
    corrected_dd = r3.tree_count(data_parts)
    direct_dd = r3.tree_count(plain_catalog(data_ra, data_dec, data_w))
    corrected_rr = r3.tree_count(random_parts)
    direct_rr = r3.tree_count(plain_catalog(random_ra, random_dec, random_w))
    central_residuals = [
        same_component(corrected_dr, direct_dr),
        same_component(corrected_dd, direct_dd),
        same_component(corrected_rr, direct_rr),
    ]

    identity = np.arange(npatch, dtype=np.int32)
    maps = {nside: identity for nside in r3.NSIDES}
    sizes = {nside: npatch for nside in r3.NSIDES}
    correlations = {"DD": corrected_dd, "DR": corrected_dr, "RR": corrected_rr}
    removals = {name: r3.aggregate_removals(corr, maps, sizes) for name, corr in correlations.items()}
    deletion_checks = 0
    deletion_absdiff = 0.0
    deletion_reldiff = 0.0
    for patch_id in sorted(set(data_ids) | set(random_ids)):
        keep_d = data_patch != patch_id
        keep_r = random_patch != patch_id
        direct = {
            "DD": r3.tree_count(plain_catalog(data_ra[keep_d], data_dec[keep_d], data_w[keep_d])),
            "DR": r3.tree_count(
                plain_catalog(data_ra[keep_d], data_dec[keep_d], data_w[keep_d]),
                plain_catalog(random_ra[keep_r], random_dec[keep_r], random_w[keep_r]),
            ),
            "RR": r3.tree_count(plain_catalog(random_ra[keep_r], random_dec[keep_r], random_w[keep_r])),
        }
        for name in r3.COMPONENTS:
            central_count, central_weight = arrays(correlations[name])
            count, weight = arrays(direct[name])
            expected_count = central_count - removals[name][16]["count"][patch_id]
            expected_weight = central_weight - removals[name][16]["weight"][patch_id]
            if not np.array_equal(count, expected_count):
                raise AssertionError(f"literal {name} deletion count mismatch for patch {patch_id}")
            absdiff = float(np.max(np.abs(weight - expected_weight)))
            reldiff = float(np.max(np.abs(weight - expected_weight) / np.maximum(np.abs(weight), 1.0)))
            if not np.allclose(weight, expected_weight, rtol=5e-13, atol=1e-12):
                raise AssertionError(
                    f"literal {name} deletion weight mismatch for patch {patch_id}: "
                    f"abs={absdiff} rel={reldiff}"
                )
            deletion_absdiff = max(deletion_absdiff, absdiff)
            deletion_reldiff = max(deletion_reldiff, reldiff)
            deletion_checks += 1

    return {
        "legacy_failure_reproduced": True,
        "data_occupied_patch_ids": data_ids,
        "random_occupied_patch_ids": random_ids,
        "data_only_patch_ids": sorted(set(data_ids) - set(random_ids)),
        "random_only_patch_ids": sorted(set(random_ids) - set(data_ids)),
        "central_integer_counts_exact": True,
        "central_weight_max_abs_difference": max(item[0] for item in central_residuals),
        "central_weight_max_relative_difference": max(item[1] for item in central_residuals),
        "literal_deletion_checks": deletion_checks,
        "literal_deletion_weight_max_abs_difference": deletion_absdiff,
        "literal_deletion_weight_max_relative_difference": deletion_reldiff,
        "global_npatch": npatch,
    }


def load_inputs(sample, cap):
    entries = r3.r1.read_manifest()
    data_entry = next(e for e in entries if e.kind == "data" and e.sample == sample and e.cap == cap)
    random_entry = next(e for e in entries if e.kind == "random" and e.sample == sample and e.cap == cap)
    data = r3.r1.read_numeric_columns(
        data_entry.path, ["RA", "DEC", "Z"] + r3.r1.WEIGHT_FIELDS, data_entry.rows,
    )
    random = r3.r1.read_numeric_columns(random_entry.path, ["RA", "DEC", "Z"], random_entry.rows)
    weights = r3.r1.weight_arrays(data)
    data_sid = r3.r1.assign_shells(data["Z"], sample)
    random_sid = r3.r1.assign_shells(random["Z"], sample)
    hashes = r3.r1.splitmix64(
        np.arange(random_entry.rows, dtype=np.uint64), int(random_entry.sha256[:16], 16),
    )
    group = next(iter(r3.r2.groups(sample)))
    return data, random, data_sid, random_sid, hashes, weights, group


def run_real_cell(sample, cap):
    data, random, data_sid, random_sid, hashes, weights, group = load_inputs(sample, cap)
    blocks = r3.load_block_pixels()
    components = r3.load_r2_components()
    with tempfile.TemporaryDirectory(prefix=f"udt_r3_{sample}_{cap}_repair_") as directory:
        outpath = Path(directory) / f"R3_{sample}_{cap}_f1_g00.npz"
        r3.execute_selection(
            sample, cap, group, data, random, data_sid, random_sid, hashes, weights,
            blocks, components, outpath, lambda message: None,
        )
        expected = {
            **r3.cell_contract(),
            "sample": sample,
            "cap": cap,
            "factor": int(group["factor"]),
            "group": int(group["group"]),
            "selection_key": r3.selection_key(sample, cap, group),
        }
        meta, cell_arrays = r3.read_cell(outpath, expected)
    if len(meta["comparisons"]) != 9 or len(meta["summaries"]) != 12:
        raise AssertionError("real trigger structural record count mismatch")
    if not all(item["integer_counts_exact"] for item in meta["comparisons"]):
        raise AssertionError("real trigger central integer comparison failed")
    max_abs = max(float(item["max_weight_abs_difference"]) for item in meta["comparisons"])
    max_rel = max(float(item["max_weight_relative_difference"]) for item in meta["comparisons"])
    return meta, cell_arrays, {"max_weight_abs_difference": max_abs, "max_weight_relative_difference": max_rel}


def real_checks():
    south_meta, _, south = run_real_cell("CMASS", "South")
    north_meta, north_arrays, north = run_real_cell("CMASS", "North")
    old_path = GUARDED / "R3_CMASS_North_f1_g00.npz"
    old_meta, old_arrays = r3.read_cell(old_path)
    central_names = (
        "central_rr_count", "central_rr_weight", "central_dd_count", "central_dd_weight",
        "central_dr_count", "central_dr_weight", "central_curve",
    )
    for name in central_names:
        if np.issubdtype(north_arrays[name].dtype, np.integer):
            equal = np.array_equal(north_arrays[name], old_arrays[name])
        else:
            equal = np.allclose(north_arrays[name], old_arrays[name], rtol=5e-12, atol=1e-8)
        if not equal:
            raise AssertionError(f"North checkpoint regression mismatch: {name}")

    current_contract = r3.cell_contract()
    expected_mismatches = [
        "patch_cardinality_correction_preregistration_sha256",
        "script_sha256",
        "treecorr_patch_representation",
    ]
    checkpoint_paths = sorted(GUARDED.glob("R3_*.npz"))
    if len(checkpoint_paths) != 48:
        raise AssertionError(f"expected 48 guarded legacy checkpoints, found {len(checkpoint_paths)}")
    mismatch_census = {}
    for path in checkpoint_paths:
        meta, _ = r3.read_cell(path)
        if path.name != f"R3_{meta.get('selection_key')}.npz":
            raise AssertionError(f"legacy checkpoint filename/metadata mismatch: {path.name}")
        if meta.get("script_sha256") != EXPECTED_LEGACY_PRODUCTION_SHA256:
            raise AssertionError(f"unexpected legacy script hash: {path.name}")
        if meta.get("patch_cardinality_correction_preregistration_sha256") is not None:
            raise AssertionError(f"legacy checkpoint unexpectedly owns correction preregistration: {path.name}")
        if meta.get("treecorr_patch_representation") is not None:
            raise AssertionError(f"legacy checkpoint unexpectedly owns corrected representation: {path.name}")
        mismatches = sorted(key for key, value in current_contract.items() if meta.get(key) != value)
        if mismatches != expected_mismatches:
            raise AssertionError(f"unexpected checkpoint contract changes for {path.name}: {mismatches}")
        mismatch_census[tuple(mismatches)] = mismatch_census.get(tuple(mismatches), 0) + 1
    return {
        "south_trigger": {
            "selection_key": south_meta["selection_key"],
            "comparison_count": len(south_meta["comparisons"]),
            **south,
        },
        "north_regression": {
            "selection_key": north_meta["selection_key"],
            "central_array_count": len(central_names),
            **north,
        },
        "legacy_checkpoint_count": len(checkpoint_paths),
        "legacy_checkpoint_contract_mismatches": expected_mismatches,
        "legacy_checkpoint_mismatch_census": {
            ",".join(key): value for key, value in mismatch_census.items()
        },
        "legacy_checkpoints_reusable": False,
    }


def operational_gates(run_repository_tests):
    wrapper = r3.ROOT / "run_r3_guarded_service.sh"
    exit_test = subprocess.run([str(wrapper), "--self-test-exit"], check=False, capture_output=True, text=True)
    if exit_test.returncode != 7:
        raise AssertionError(f"service wrapper masked failure: {exit_test.returncode}")
    result = {"service_wrapper_failure_exit": exit_test.returncode}
    if run_repository_tests:
        completed = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/"],
            cwd=r3.ROOT.parent,
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0 or "103 passed, 1 xfailed" not in completed.stdout:
            raise AssertionError(
                f"repository gate failed: code={completed.returncode}\n{completed.stdout}\n{completed.stderr}"
            )
        result["repository_tests"] = "103 passed, 1 xfailed"
    else:
        result["repository_tests"] = "NOT_REQUESTED"
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--real", action="store_true")
    parser.add_argument("--repository-gates", action="store_true")
    args = parser.parse_args()
    if args.real and not args.repository_gates:
        parser.error("--real requires --repository-gates for a fail-closed full verification")
    if treecorr.__version__ != EXPECTED_TREECORR:
        raise AssertionError(f"unexpected TreeCorr version {treecorr.__version__}")
    script_sha256 = r3.sha256(r3.SCRIPT)
    if script_sha256 != EXPECTED_PRODUCTION_SHA256:
        raise AssertionError(f"unexpected post-repair production hash {script_sha256}")
    result = {
        "treecorr": treecorr.__version__,
        "production_script_sha256": script_sha256,
        "synthetic": synthetic_check(),
        "operational": operational_gates(args.repository_gates),
    }
    if args.real:
        result["real"] = real_checks()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

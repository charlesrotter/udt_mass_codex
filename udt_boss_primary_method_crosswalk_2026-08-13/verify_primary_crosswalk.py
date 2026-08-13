#!/usr/bin/env python3
"""Independent finite checks for the preregistered BOSS method crosswalk.

This verifier deliberately does not import the R0--R3 production modules.  It uses
Astropy for an independent FITS read, checks the official DR12 SAS file sizes and
catalog schemas, audits the literal redshift-boundary convention, and verifies the
weighted finite-sample pair normalizations by direct enumeration.

It does not open R3 outputs or compute a galaxy correlation function.
"""

from __future__ import annotations

import csv
import json
import platform
from pathlib import Path

import numpy as np
import astropy
from astropy.io import fits


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA_MANIFEST = ROOT / "udt_observed_angular_pattern_raw_restart_2026-08-12" / "DATA_MANIFEST.tsv"
OUTPUT = HERE / "INDEPENDENT_VERIFICATION.json"

# Bytes listed by the official SDSS DR12 BOSS LSS SAS directory on 2026-08-13.
OFFICIAL_BYTES = {
    "galaxy_DR12v5_CMASS_North.fits.gz": 138_873_951,
    "galaxy_DR12v5_CMASS_South.fits.gz": 51_580_500,
    "galaxy_DR12v5_LOWZ_North.fits.gz": 73_432_436,
    "galaxy_DR12v5_LOWZ_South.fits.gz": 32_341_613,
    "random0_DR12v5_CMASS_North.fits.gz": 3_239_878_693,
    "random0_DR12v5_CMASS_South.fits.gz": 1_172_229_517,
    "random0_DR12v5_LOWZ_North.fits.gz": 1_578_615_321,
    "random0_DR12v5_LOWZ_South.fits.gz": 713_300_258,
}

DATA_REQUIRED = {
    "RA",
    "DEC",
    "Z",
    "WEIGHT_CP",
    "WEIGHT_NOZ",
    "WEIGHT_STAR",
    "WEIGHT_SEEING",
    "WEIGHT_SYSTOT",
    "WEIGHT_FKP",
    "NZ",
}
RANDOM_REQUIRED = {"RA", "DEC", "Z", "ZINDX", "WEIGHT_FKP", "NZ"}


def read_manifest() -> list[dict[str, str]]:
    with DATA_MANIFEST.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def direct_pair_normalization_check() -> dict[str, float | bool]:
    data_weights = np.asarray([1.25, 0.75, 2.0, 1.5], dtype=np.float64)
    random_weights = np.ones(7, dtype=np.float64)

    dd_direct = sum(
        data_weights[i] * data_weights[j]
        for i in range(data_weights.size)
        for j in range(i + 1, data_weights.size)
    )
    dd_formula = ((data_weights.sum() ** 2) - np.square(data_weights).sum()) / 2.0
    dr_direct = sum(wd * wr for wd in data_weights for wr in random_weights)
    dr_formula = data_weights.sum() * random_weights.sum()
    rr_direct = sum(
        random_weights[i] * random_weights[j]
        for i in range(random_weights.size)
        for j in range(i + 1, random_weights.size)
    )
    rr_formula = random_weights.size * (random_weights.size - 1) / 2.0

    return {
        "dd_direct": float(dd_direct),
        "dd_formula": float(dd_formula),
        "dd_exact": bool(dd_direct == dd_formula),
        "dr_direct": float(dr_direct),
        "dr_formula": float(dr_formula),
        "dr_exact": bool(dr_direct == dr_formula),
        "rr_direct": float(rr_direct),
        "rr_formula": float(rr_formula),
        "rr_exact": bool(rr_direct == rr_formula),
    }


def main() -> None:
    rows = read_manifest()
    file_checks: list[dict[str, object]] = []
    boundary_checks: list[dict[str, object]] = []

    for row in rows:
        path = Path(row["path"])
        name = path.name
        if name not in OFFICIAL_BYTES:
            raise AssertionError(f"no preregistered official-size entry for {name}")
        actual_bytes = path.stat().st_size
        manifest_bytes = int(row["bytes"])
        if actual_bytes != manifest_bytes or actual_bytes != OFFICIAL_BYTES[name]:
            raise AssertionError(f"file-size mismatch for {name}")

        with fits.open(path, memmap=False, lazy_load_hdus=True) as hdul:
            table_hdu = hdul[1]
            nrows = int(table_hdu.header["NAXIS2"])
            columns = set(table_hdu.columns.names)
        required = DATA_REQUIRED if row["kind"] == "data" else RANDOM_REQUIRED
        missing = sorted(required - columns)
        if missing:
            raise AssertionError(f"missing required columns in {name}: {missing}")
        if nrows != int(row["rows"]):
            raise AssertionError(f"row-count mismatch for {name}")

        file_checks.append(
            {
                "name": name,
                "kind": row["kind"],
                "official_bytes": OFFICIAL_BYTES[name],
                "manifest_bytes": manifest_bytes,
                "actual_bytes": actual_bytes,
                "rows": nrows,
                "required_columns_present": True,
            }
        )

        # The publication-vs-local boundary audit needs the measured catalogs only.
        # Official random redshifts are draws from these measured redshifts.
        if row["kind"] != "data":
            continue

        with fits.open(path, memmap=False, lazy_load_hdus=False) as hdul:
            data = hdul[1].data
            z = np.asarray(data["Z"], dtype=np.float64)
            w_star = np.asarray(data["WEIGHT_STAR"], dtype=np.float64)
            w_seeing = np.asarray(data["WEIGHT_SEEING"], dtype=np.float64)
            w_systot = np.asarray(data["WEIGHT_SYSTOT"], dtype=np.float64)
            w_cp = np.asarray(data["WEIGHT_CP"], dtype=np.float64)
            w_noz = np.asarray(data["WEIGHT_NOZ"], dtype=np.float64)

        if row["sample"] == "LOWZ":
            local_mask = (z >= 0.15) & (z < 0.43)
            publication_mask = (z > 0.15) & (z < 0.43)
        else:
            local_mask = (z >= 0.43) & (z <= 0.70)
            publication_mask = (z > 0.43) & (z < 0.70)

        w3 = w_systot * (w_cp + w_noz - 1.0)
        if not np.all(np.isfinite(w3)) or not np.all(w3 > 0.0):
            raise AssertionError(f"nonpositive or nonfinite W3 in {name}")

        product = w_star * w_seeing
        max_product_error = float(np.max(np.abs(w_systot - product)))
        max_product_relative_error = float(
            np.max(np.abs(w_systot - product) / np.maximum(np.abs(w_systot), np.finfo(float).tiny))
        )

        boundary_checks.append(
            {
                "name": name,
                "sample": row["sample"],
                "cap": row["cap"],
                "rows_local_scope": int(np.count_nonzero(local_mask)),
                "rows_publication_notation_scope": int(np.count_nonzero(publication_mask)),
                "symmetric_mask_difference": int(np.count_nonzero(local_mask ^ publication_mask)),
                "literal_equal_0p15": int(np.count_nonzero(z == 0.15)),
                "literal_equal_0p43": int(np.count_nonzero(z == 0.43)),
                "literal_equal_0p70": int(np.count_nonzero(z == 0.70)),
                "stored_float32_equal_0p15": int(np.count_nonzero(z == float(np.float32(0.15)))),
                "stored_float32_equal_0p43": int(np.count_nonzero(z == float(np.float32(0.43)))),
                "stored_float32_equal_0p70": int(np.count_nonzero(z == float(np.float32(0.70)))),
                "w_systot_product_max_abs_error": max_product_error,
                "w_systot_product_max_relative_error": max_product_relative_error,
                "w3_min": float(np.min(w3)),
                "w3_max": float(np.max(w3)),
            }
        )

    pair_check = direct_pair_normalization_check()
    if not all(pair_check[key] for key in ("dd_exact", "dr_exact", "rr_exact")):
        raise AssertionError("finite-sample pair normalization failure")

    if any(item["symmetric_mask_difference"] != 0 for item in boundary_checks):
        boundary_status = "MISMATCH_RECORDED"
    else:
        boundary_status = "NO_REALIZED_ROW_DIFFERENCE"

    if any(item["w_systot_product_max_relative_error"] > 2.0e-7 for item in boundary_checks):
        raise AssertionError("WEIGHT_SYSTOT product relation exceeds float32 rounding allowance")

    result = {
        "status": "PASS",
        "implementation_independence": "ASTROPY_AND_DIRECT_ENUMERATION__NO_R0_R3_MODULE_IMPORT",
        "versions": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "astropy": astropy.__version__,
        },
        "official_file_listing_match": True,
        "catalog_schema_match": True,
        "boundary_status": boundary_status,
        "file_checks": file_checks,
        "boundary_checks": boundary_checks,
        "pair_normalization_check": pair_check,
        "r3_scientific_content_opened": False,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Outcome-blind G277 anchor ownership and identifiability audit."""

from __future__ import annotations

import csv
import argparse
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np

from sealed_source_paths import source_path


PKG = Path(__file__).resolve().parent
ROOT = PKG.parent
MANIFEST = PKG / "SOURCE_MANIFEST.tsv"
OUT_JSON = PKG / "DERIVATION_RESULT.json"
OUT_TSV = PKG / "ANCHOR_CLASSIFICATION.tsv"
SCHEMA_TSV = PKG / "DATA_SCHEMA_AUDIT.tsv"
COVARIANCE_TSV = PKG / "COVARIANCE_RANK_AUDIT.tsv"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def resolve_source(path_text: str) -> Path:
    return source_path(path_text, ROOT)


def exact_rank(matrix: list[list[int]]) -> int:
    work = [[Fraction(value) for value in row] for row in matrix]
    if not work:
        return 0
    rows = len(work)
    cols = len(work[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next((row for row in range(pivot_row, rows) if work[row][col]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][col]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][col]:
                continue
            factor = work[row][col]
            work[row] = [
                work[row][index] - factor * work[pivot_row][index]
                for index in range(cols)
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def read_manifest() -> dict[str, str]:
    verified: dict[str, str] = {}
    with MANIFEST.open(newline="") as stream:
        for row in csv.DictReader(stream, delimiter="\t"):
            path = resolve_source(row["path"])
            actual = sha256(path)
            assert actual == row["sha256"], (row["path"], actual, row["sha256"])
            verified[row["path"]] = actual
    return verified


def pantheon_schema() -> dict[str, object]:
    path = source_path("Data/Pantheon+SH0ES.dat", ROOT)
    with path.open(newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter=" ", skipinitialspace=True))
    required = {
        "CID",
        "zHD",
        "zCMB",
        "zHEL",
        "m_b_corr",
        "MU_SH0ES",
        "CEPH_DIST",
        "IS_CALIBRATOR",
    }
    assert rows and required.issubset(rows[0])
    calibrators = [row for row in rows if row["IS_CALIBRATOR"] == "1"]
    noncalibrators = [row for row in rows if row["IS_CALIBRATOR"] == "0"]
    assert len(calibrators) + len(noncalibrators) == len(rows)
    cepheid_values = [float(row["CEPH_DIST"]) for row in calibrators]
    noncal_values = {float(row["CEPH_DIST"]) for row in noncalibrators}
    assert all(math.isfinite(value) and value > 0 for value in cepheid_values)
    assert noncal_values == {-9.0}
    covariance_path = source_path("Data/Pantheon+SH0ES_STAT+SYS.cov", ROOT)
    with covariance_path.open() as stream:
        dimension = int(stream.readline().strip())
        payload_lines = sum(1 for _ in stream)
    assert dimension == len(rows)
    assert payload_lines == dimension * dimension
    return {
        "rows": len(rows),
        "calibrator_rows": len(calibrators),
        "unique_calibrator_cids": len({row["CID"] for row in calibrators}),
        "calibrator_ceph_dist_min": min(cepheid_values),
        "calibrator_ceph_dist_max": max(cepheid_values),
        "noncalibrator_ceph_dist_sentinel": -9.0,
        "covariance_dimension": dimension,
        "covariance_payload_entries": payload_lines,
    }


def sealed_primary_source_checks() -> dict[str, bool]:
    readme = source_path(
        f"{PKG.name}/sources/PantheonPlus_4_DISTANCES_AND_COVAR_README.txt", ROOT
    ).read_text()
    likelihood = source_path(
        f"{PKG.name}/sources/PantheonPlus_SH0ES_cosmosis_likelihood.py", ROOT
    ).read_text()
    checks = {
        "ceph_dist_semantics": "CEPH_DIST - cepheid calculated absolute distance to host" in readme,
        "calibrator_flag_semantics": (
            "IS_CALIBRATOR - binary to designate if this SN is in a host that has an associated cepheid distance"
            in readme
        ),
        "cepheid_covariance_semantics": "also Cepheid host covariance" in readme,
        "official_mask": "(data['zHD']>0.01) | (np.array(data['IS_CALIBRATOR'],dtype=bool))" in likelihood,
        "calibrator_uses_ceph_dist": "self.cepheid_distance = data['CEPH_DIST'][self.ww]" in likelihood,
        "calibrator_theory_assignment": (
            "theory_ynew[np.array(self.is_calibrator,dtype='bool')] = self.cepheid_distance"
            in likelihood
        ),
        "calibrates_absolute_magnitude": "what calibrates M" in likelihood,
    }
    assert all(checks.values())
    return checks


def actual_covariance_rank_audit() -> dict[str, object]:
    table_path = source_path("Data/Pantheon+SH0ES.dat", ROOT)
    with table_path.open(newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter=" ", skipinitialspace=True))
    zhd = np.array([float(row["zHD"]) for row in rows], dtype=np.float64)
    is_cal = np.array([row["IS_CALIBRATOR"] == "1" for row in rows], dtype=bool)
    mask = (zhd > 0.01) | is_cal
    selected_cal = is_cal[mask]
    design = np.column_stack((~selected_cal, np.ones(selected_cal.size, dtype=np.float64)))
    payload = np.loadtxt(source_path("Data/Pantheon+SH0ES_STAT+SYS.cov", ROOT), skiprows=1)
    covariance = payload.reshape(len(rows), len(rows))[np.ix_(mask, mask)]
    assert np.isfinite(covariance).all()
    raw_symmetry_defect = float(np.max(np.abs(covariance - covariance.T)))
    raw_symmetry_gate_pass = raw_symmetry_defect <= 1e-12
    assert not raw_symmetry_gate_pass
    routes = {
        "mean": (covariance + covariance.T) / 2.0,
        "lower": np.tril(covariance) + np.tril(covariance, -1).T,
        "upper": np.triu(covariance) + np.triu(covariance, 1).T,
    }
    route_rows: list[dict[str, str]] = []
    route_values: dict[str, dict[str, object]] = {}
    for name, matrix in routes.items():
        np.linalg.cholesky(matrix)
        fisher = design.T @ np.linalg.solve(matrix, design)
        eigenvalues = np.linalg.eigvalsh(fisher)
        ratio = float(eigenvalues[0] / eigenvalues[-1])
        rank = int(np.linalg.matrix_rank(fisher))
        assert rank == 2
        assert ratio > 1e-12
        route_values[name] = {
            "fisher": fisher,
            "eigenvalues": eigenvalues,
            "condition_ratio": ratio,
            "rank": rank,
        }
    reference_fisher = route_values["mean"]["fisher"]
    reference_eigenvalues = route_values["mean"]["eigenvalues"]
    max_fisher_relative_difference = 0.0
    max_eigen_relative_difference = 0.0
    for name, values in route_values.items():
        fisher = values["fisher"]
        eigenvalues = values["eigenvalues"]
        fisher_rel = float(
            np.max(np.abs(fisher - reference_fisher) / np.maximum(1.0, np.abs(reference_fisher)))
        )
        eigen_rel = float(
            np.max(
                np.abs(eigenvalues - reference_eigenvalues)
                / np.maximum(1.0, np.abs(reference_eigenvalues))
            )
        )
        max_fisher_relative_difference = max(max_fisher_relative_difference, fisher_rel)
        max_eigen_relative_difference = max(max_eigen_relative_difference, eigen_rel)
        route_rows.append(
            {
                "route": name,
                "rows": str(selected_cal.size),
                "calibrators": str(int(selected_cal.sum())),
                "flow": str(int((~selected_cal).sum())),
                "design_rank": str(int(np.linalg.matrix_rank(design))),
                "weighted_rank": str(values["rank"]),
                "eigen_min": repr(float(eigenvalues[0])),
                "eigen_max": repr(float(eigenvalues[-1])),
                "eigen_ratio": repr(values["condition_ratio"]),
                "fisher_relative_to_mean": repr(fisher_rel),
                "eigen_relative_to_mean": repr(eigen_rel),
            }
        )
    assert max_fisher_relative_difference < 1e-4
    assert max_eigen_relative_difference < 1e-4
    return {
        "rows": int(selected_cal.size),
        "calibrators": int(selected_cal.sum()),
        "flow": int((~selected_cal).sum()),
        "actual_design_rank": int(np.linalg.matrix_rank(design)),
        "raw_symmetry_defect": raw_symmetry_defect,
        "raw_symmetry_threshold": 1e-12,
        "raw_symmetry_gate_pass": raw_symmetry_gate_pass,
        "symmetric_routes": {
            name: {
                "weighted_rank": values["rank"],
                "condition_ratio": values["condition_ratio"],
            }
            for name, values in route_values.items()
        },
        "max_fisher_relative_difference": max_fisher_relative_difference,
        "max_eigen_relative_difference": max_eigen_relative_difference,
        "route_rows": route_rows,
    }


def des_schema() -> dict[str, object]:
    readme = source_path(
        "/media/udt-admin/ScratchDisk/Data/UDT_DES_SN5YR_DOVEKIE_2026-08-15/"
        "4_DISTANCES_COVMAT/README.md",
        ROOT,
    ).read_text()
    assert "MU` - SN distances (assuming H0 of 70)" in readme
    assert "global parameters are determined from the likelihood analysis" in readme
    assert "biasCor_mu" in readme
    lines = source_path(
        "/media/udt-admin/ScratchDisk/Data/UDT_DES_SN5YR_DOVEKIE_2026-08-15/"
        "4_DISTANCES_COVMAT/DES-Dovekie_HD.csv",
        ROOT,
    ).read_text().splitlines()
    varnames = next(line for line in lines if line.startswith("VARNAMES:"))
    rows = [line for line in lines if line.startswith("SN:")]
    assert "MU" in varnames.split()
    return {
        "rows": len(rows),
        "varnames": varnames.removeprefix("VARNAMES: "),
        "release_h0_normalization": 70,
        "global_nuisance_from_likelihood": True,
        "bias_correction_present": True,
    }


def cmb_typing() -> dict[str, object]:
    type_path = source_path(
        "udt_cmb_G79_same_geometry_dimensional_sne_query_2026-08-11/TYPE_LEDGER.tsv", ROOT
    )
    thermal_path = source_path(
        "udt_cmb_G79_same_geometry_dimensional_sne_query_2026-08-11/THERMAL_READOUT_LEDGER.tsv",
        ROOT,
    )
    with type_path.open(newline="") as stream:
        rows = {row["object"]: row for row in csv.DictReader(stream, delimiter="\t")}
    with thermal_path.open(newline="") as stream:
        thermal = {row["stage"]: row for row in csv.DictReader(stream, delimiter="\t")}
    assert rows["cmb_temp"]["status"] == "OPEN_NO_OWNER"
    assert "source" in rows["cmb_temp"]["open_scope"].lower()
    assert thermal["thermal_parameter"]["status"] == "CONDITIONAL_READOUT_ONLY"
    assert thermal["temperature_sky"]["status"] == "CONDITIONAL_FUTURE_MAP"
    return {
        "cmb_temp_status": rows["cmb_temp"]["status"],
        "thermal_parameter_status": thermal["thermal_parameter"]["status"],
        "temperature_sky_status": thermal["temperature_sky"]["status"],
    }


def identifiability_checks() -> dict[str, object]:
    # Columns are additive log-scale followed by release/absolute-magnitude offsets.
    one_relative = [[1, 1], [1, 1], [1, 1]]
    two_relative_offsets = [[1, 1, 0], [1, 1, 0], [1, 0, 1], [1, 0, 1]]
    two_relative_shared_offset = [[1, 1], [1, 1], [1, 1], [1, 1]]
    calibrator_plus_flow = [[0, 1], [0, 1], [1, 1], [1, 1]]
    cmb_unknown_source = [[0, 1], [0, 1]]
    checks = {
        "one_relative_rank": exact_rank(one_relative),
        "one_relative_columns": 2,
        "two_relative_offsets_rank": exact_rank(two_relative_offsets),
        "two_relative_offsets_columns": 3,
        "two_relative_shared_offset_rank": exact_rank(two_relative_shared_offset),
        "two_relative_shared_offset_columns": 2,
        "calibrator_plus_flow_rank": exact_rank(calibrator_plus_flow),
        "calibrator_plus_flow_columns": 2,
        "cmb_unknown_source_rank": exact_rank(cmb_unknown_source),
        "cmb_unknown_source_columns": 2,
    }
    assert checks["one_relative_rank"] < checks["one_relative_columns"]
    assert checks["two_relative_offsets_rank"] < checks["two_relative_offsets_columns"]
    assert checks["two_relative_shared_offset_rank"] < checks["two_relative_shared_offset_columns"]
    assert checks["calibrator_plus_flow_rank"] == checks["calibrator_plus_flow_columns"]
    assert checks["cmb_unknown_source_rank"] < checks["cmb_unknown_source_columns"]
    return checks


def classifications() -> list[dict[str, str]]:
    return [
        {
            "candidate": "PantheonPlus_CEPH_DIST_calibrators",
            "classification": "CONDITIONAL_TRANSFER_OR_DISTANCE_ANCHOR",
            "homothety_weight": "+1_after_distance_attachment",
            "independent_datum": "yes_processed_distance_ladder",
            "remaining_bridge": "Cepheid_distance_modulus_to_same_UDT_metric_distance;_radiative_transfer_if_used_through_SNe",
            "reason": "calibrator_rows_break_scale_vs_SN_absolute_magnitude_rank_only_after_the_published_distance_ladder_and_operational_distance_bridge_are_supplied",
        },
        {
            "candidate": "PantheonPlus_noncalibrators_only",
            "classification": "RELATIVE_ONLY",
            "homothety_weight": "degenerate_with_magnitude_offset",
            "independent_datum": "no_absolute_zero_point",
            "remaining_bridge": "absolute_magnitude_or_independent_distance",
            "reason": "G236_G237_marginalize_one_release_offset_and_the_exact_design_is_rank_deficient",
        },
        {
            "candidate": "DES_Dovekie_alone",
            "classification": "RELATIVE_ONLY",
            "homothety_weight": "degenerate_with_release_normalization",
            "independent_datum": "no_without_importing_H0_70",
            "remaining_bridge": "independent_absolute_zero_point",
            "reason": "release_MU_assumes_H0_70_and_global_nuisance_parameters_come_from_the_release_likelihood",
        },
        {
            "candidate": "PantheonPlus_relative_plus_DES_relative",
            "classification": "RELATIVE_ONLY",
            "homothety_weight": "common_scale_column_in_offset_span",
            "independent_datum": "no",
            "remaining_bridge": "one_nonzero_weight_absolute_anchor",
            "reason": "combining_relative_catalogs_does_not_raise_the_exact_design_to_full_column_rank",
        },
        {
            "candidate": "PantheonPlus_calibrators_plus_Hubble_flow",
            "classification": "CONDITIONAL_TRANSFER_OR_DISTANCE_ANCHOR",
            "homothety_weight": "+1_after_metric_distance_attachment",
            "independent_datum": "yes_processed_distance_ladder",
            "remaining_bridge": "common_SN_standardization_and_declared_luminosity_or_area_transfer",
            "reason": "calibrator_and_flow_rows_make_scale_and_shared_absolute_magnitude_columns_independent",
        },
        {
            "candidate": "cmb_temp",
            "classification": "NOT_CURRENTLY_SCALE_TYPED",
            "homothety_weight": "zero_or_undefined_under_current_query",
            "independent_datum": "observed_temperature_but_source_state_unowned",
            "remaining_bridge": "source_temperature_thermalization_detector_and_metric_distance_depth_attachment",
            "reason": "current_G79_typing_is_OPEN_NO_OWNER_and_temperature_ratio_constrains_depth_not_constant_homothety_scale",
        },
        {
            "candidate": "G276_same_segment_proper_clock",
            "classification": "DIRECT_NONZERO_WEIGHT_ANCHOR",
            "homothety_weight": "+1",
            "independent_datum": "yes_when_supplied",
            "remaining_bridge": "physical_record_and_exact_segment_identity_only",
            "reason": "ell_equals_cE_tau_star_over_C_bar_is_already_derived_conditionally",
        },
        {
            "candidate": "G250_direct_geometric_record",
            "classification": "DIRECT_NONZERO_WEIGHT_ANCHOR",
            "homothety_weight": "known_nonzero_when_exact_object_is_supplied",
            "independent_datum": "yes_when_supplied",
            "remaining_bridge": "physical_record_and_same_object_identity_only",
            "reason": "one_matched_nonzero_weight_record_fixes_the_single_positive_homothety",
        },
    ]


def write_tsv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            delimiter="\t",
            fieldnames=list(rows[0]),
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def main(no_write: bool = False) -> None:
    sources = read_manifest()
    pantheon = pantheon_schema()
    primary_sources = sealed_primary_source_checks()
    des = des_schema()
    cmb = cmb_typing()
    ranks = identifiability_checks()
    covariance_rank = actual_covariance_rank_audit()
    classes = classifications()
    if not no_write:
        write_tsv(OUT_TSV, classes)
    schema_rows = [
        {"source": "PantheonPlus", "field": key, "value": str(value)}
        for key, value in pantheon.items()
    ] + [
        {"source": "DES_Dovekie", "field": key, "value": str(value)}
        for key, value in des.items()
    ] + [
        {"source": "cmb_typing", "field": key, "value": str(value)}
        for key, value in cmb.items()
    ]
    if not no_write:
        write_tsv(SCHEMA_TSV, schema_rows)
        write_tsv(COVARIANCE_TSV, covariance_rank["route_rows"])
    result = {
        "status": "PASS",
        "landing": (
            "PANTHEONPLUS_CEPHEID_HOST_ROUTE_IS_A_CONDITIONAL_ABSOLUTE_SCALE_ATTACHMENT"
            "__NOT_A_NATIVE_G276_CLOCK_ANCHOR__PANTHEONPLUS_NONCALIBRATORS_DES_AND_THEIR_RELATIVE_"
            "COMBINATION_REMAIN_SCALE_DEGENERATE__CMB_TEMP_IS_NOT_CURRENTLY_SCALE_TYPED__NO_FIT_"
            "SCALE_HISTORY_KERNEL_OR_XMAX_SELECTED"
        ),
        "source_hashes_verified": len(sources),
        "pantheon_schema": pantheon,
        "sealed_primary_source_checks": primary_sources,
        "des_schema": des,
        "cmb_typing": cmb,
        "identifiability": ranks,
        "actual_covariance_weighted_rank": {
            key: value for key, value in covariance_rank.items() if key != "route_rows"
        },
        "classification_count": len(classes),
        "observational_fit_performed": False,
        "numerical_scale_computed": False,
        "metric_or_kernel_changed": False,
        "xmax_selected": False,
    }
    if not no_write:
        OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    main(no_write=parser.parse_args().no_write)

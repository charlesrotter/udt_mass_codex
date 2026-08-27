#!/usr/bin/env python3
"""Implementation-distinct G277 verifier; does not import production or read its outputs."""

from __future__ import annotations

import hashlib
import argparse
import json
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "INDEPENDENT_VERIFICATION.json"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(131071)
            if not chunk:
                return h.hexdigest()
            h.update(chunk)


def rank_by_minors(rows: list[list[int]], columns: int) -> int:
    if columns == 1:
        return int(any(row[0] != 0 for row in rows))
    if columns == 2:
        for i, first in enumerate(rows):
            for second in rows[i + 1 :]:
                if first[0] * second[1] - first[1] * second[0] != 0:
                    return 2
        return int(any(any(value != 0 for value in row) for row in rows))
    if columns == 3:
        for i, a in enumerate(rows):
            for j, b in enumerate(rows[i + 1 :], i + 1):
                for c in rows[j + 1 :]:
                    determinant = (
                        a[0] * (b[1] * c[2] - b[2] * c[1])
                        - a[1] * (b[0] * c[2] - b[2] * c[0])
                        + a[2] * (b[0] * c[1] - b[1] * c[0])
                    )
                    if determinant:
                        return 3
        projected = [[row[0], row[1]] for row in rows]
        if rank_by_minors(projected, 2) == 2:
            return 2
        projected = [[row[0], row[2]] for row in rows]
        if rank_by_minors(projected, 2) == 2:
            return 2
        projected = [[row[1], row[2]] for row in rows]
        return rank_by_minors(projected, 2)
    raise ValueError(columns)


def parse_pantheon_without_csv() -> dict[str, int | float]:
    lines = (ROOT / "Data/Pantheon+SH0ES.dat").read_text().splitlines()
    names = lines[0].split()
    index = {name: position for position, name in enumerate(names)}
    required = ["CID", "CEPH_DIST", "IS_CALIBRATOR", "m_b_corr", "MU_SH0ES"]
    assert all(name in index for name in required)
    rows = [line.split() for line in lines[1:] if line.strip()]
    calibrators = [row for row in rows if row[index["IS_CALIBRATOR"]] == "1"]
    noncalibrators = [row for row in rows if row[index["IS_CALIBRATOR"]] == "0"]
    values = [float(row[index["CEPH_DIST"]]) for row in calibrators]
    assert values and min(values) > 0
    assert {float(row[index["CEPH_DIST"]]) for row in noncalibrators} == {-9.0}
    return {
        "rows": len(rows),
        "calibrator_rows": len(calibrators),
        "unique_calibrator_cids": len({row[index["CID"]] for row in calibrators}),
        "ceph_min": min(values),
        "ceph_max": max(values),
    }


def classify_from_facts(
    *,
    independent: bool,
    nonzero_weight: bool,
    zero_point_closed: bool,
    same_object: bool,
    bridge_owned: bool,
    source_owned: bool,
) -> str:
    if not source_owned or not nonzero_weight:
        return "NOT_CURRENTLY_SCALE_TYPED"
    if not zero_point_closed:
        return "RELATIVE_ONLY"
    if independent and same_object and bridge_owned:
        return "DIRECT_NONZERO_WEIGHT_ANCHOR"
    return "CONDITIONAL_TRANSFER_OR_DISTANCE_ANCHOR"


def sealed_semantics() -> dict[str, bool]:
    readme = (HERE / "sources/PantheonPlus_4_DISTANCES_AND_COVAR_README.txt").read_text()
    likelihood = (HERE / "sources/PantheonPlus_SH0ES_cosmosis_likelihood.py").read_text()
    thermal = (
        ROOT
        / "udt_cmb_G79_same_geometry_dimensional_sne_query_2026-08-11/THERMAL_READOUT_LEDGER.tsv"
    ).read_text()
    checks = {
        "ceph_distance": "CEPH_DIST - cepheid calculated absolute distance to host" in readme,
        "calibrator_flag": "associated cepheid distance" in readme,
        "cepheid_covariance": "also Cepheid host covariance" in readme,
        "calibrator_theory": "Here we use the Cepheid host distances as the \"theory\"" in likelihood,
        "calibrates_M": "what calibrates M" in likelihood,
        "thermal_conditional": "thermal_parameter\tsupplied one-parameter thermal spectrum" in thermal,
        "temperature_future": "temperature_sky\tsupplied T_src" in thermal,
    }
    assert all(checks.values())
    return checks


def covariance_weighted_independence() -> dict[str, object]:
    lines = (ROOT / "Data/Pantheon+SH0ES.dat").read_text().splitlines()
    names = lines[0].split()
    idx = {name: position for position, name in enumerate(names)}
    rows = [line.split() for line in lines[1:] if line.strip()]
    zhd = np.array([float(row[idx["zHD"]]) for row in rows], dtype=np.float64)
    is_cal = np.array([row[idx["IS_CALIBRATOR"]] == "1" for row in rows], dtype=bool)
    mask = (zhd > 0.01) | is_cal
    selected = is_cal[mask]
    design = np.column_stack((~selected, np.ones(selected.size)))
    with (ROOT / "Data/Pantheon+SH0ES_STAT+SYS.cov").open() as stream:
        dimension = int(stream.readline())
        payload = np.fromiter((float(line) for line in stream), dtype=np.float64)
    raw = payload.reshape(dimension, dimension)[np.ix_(mask, mask)]
    symmetry_defect = float(np.max(np.abs(raw - raw.T)))
    assert symmetry_defect > 1e-12
    routes = {
        "mean": (raw + raw.T) / 2.0,
        "lower": np.tril(raw) + np.tril(raw, -1).T,
        "upper": np.triu(raw) + np.triu(raw, 1).T,
    }
    results: dict[str, dict[str, float | int]] = {}
    for name, matrix in routes.items():
        lower = np.linalg.cholesky(matrix)
        whitened = np.linalg.solve(lower, design)
        gram = whitened.T @ whitened
        determinant = float(gram[0, 0] * gram[1, 1] - gram[0, 1] * gram[1, 0])
        eigenvalues = np.linalg.eigvalsh(gram)
        ratio = float(eigenvalues[0] / eigenvalues[-1])
        assert determinant > 0
        assert ratio > 1e-12
        results[name] = {
            "determinant": determinant,
            "condition_ratio": ratio,
            "rank": 2,
        }
    reference = results["mean"]
    for name in ("lower", "upper"):
        assert abs(results[name]["determinant"] - reference["determinant"]) / reference["determinant"] < 1e-4
        assert abs(results[name]["condition_ratio"] - reference["condition_ratio"]) / reference["condition_ratio"] < 1e-4
    return {
        "rows": int(selected.size),
        "calibrators": int(selected.sum()),
        "flow": int((~selected).sum()),
        "raw_symmetry_defect": symmetry_defect,
        "raw_symmetry_gate_pass": False,
        "routes": results,
    }


def source_derived_classification_facts(
    source_checks: dict[str, bool],
    covariance_rank: dict[str, object],
    exact_ranks: dict[str, int],
) -> dict[str, dict[str, bool]]:
    g236 = (ROOT / "udt_g236_dual_sne_relational_state_reconstruction_2026-08-23/AUDIT_REPORT.md").read_text()
    g258 = (ROOT / "udt_g258_redshift_area_inverse_metric_reconstruction_2026-08-25/AUDIT_REPORT.md").read_text()
    g275 = (
        ROOT / "udt_g275_projective_position_scale_attachment_xmax_separation_2026-08-26/AUDIT_REPORT.md"
    ).read_text()
    g276 = (
        ROOT / "udt_g276_proper_clock_ce_scale_anchor_reconciliation_2026-08-26/AUDIT_REPORT.md"
    ).read_text()
    cmb_types = (
        ROOT / "udt_cmb_G79_same_geometry_dimensional_sne_query_2026-08-11/TYPE_LEDGER.tsv"
    ).read_text()
    des_root = Path(
        "/media/udt-admin/ScratchDisk/Data/"
        "UDT_DES_SN5YR_DOVEKIE_2026-08-15/4_DISTANCES_COVMAT"
    )
    des_readme = (des_root / "README.md").read_text()
    des_table = (des_root / "DES-Dovekie_HD.csv").read_text()
    pantheon_observed = covariance_rank["rows"] > 0 and (
        covariance_rank["calibrators"] + covariance_rank["flow"] == covariance_rank["rows"]
    )
    des_observed = (
        "VARNAMES: CID IDSURVEY zHD zHEL MU MUERR" in des_table
        and des_table.count("\nSN:") > 0
    )
    relative_offset_open = (
        "+B_c" in g236.replace(" ", "")
        and "relative state" in g236
    )
    des_normalization_open = (
        "assuming H0 of 70" in des_readme
        and "global parameters are determined from the likelihood analysis" in des_readme
    )
    transfer_imported = "transparent transfer is imported and conditional" in g258
    projective_not_operational_distance = "not automatically" in g275 and "operational" in g275
    calibrator_rank_closed = all(
        route["rank"] == 2 and route["condition_ratio"] > 1e-12
        for route in covariance_rank["routes"].values()
    )
    calibrator_source_owned = (
        source_checks["ceph_distance"]
        and source_checks["calibrator_theory"]
        and source_checks["calibrates_M"]
        and source_checks["cepheid_covariance"]
    )
    clock_direct = (
        "independently calibrated positive proper-clock record" in g276
        and "homothety weight" in g276
        and "exact modeled timelike segment" in g276
    )
    cmb_source_open = "cmb_temp\tobserved temperature field on sky\tunowned source field" in cmb_types
    assertions = {
        "relative_offset_open": relative_offset_open,
        "transfer_imported": transfer_imported,
        "projective_not_operational_distance": projective_not_operational_distance,
        "calibrator_rank_closed": calibrator_rank_closed,
        "calibrator_source_owned": calibrator_source_owned,
        "clock_direct": clock_direct,
        "cmb_source_open": cmb_source_open,
        "pantheon_observed": pantheon_observed,
        "des_observed": des_observed,
        "des_normalization_open": des_normalization_open,
        "one_relative_rank_deficient": exact_ranks["relative_one"] < 2,
        "two_relative_rank_deficient": exact_ranks["relative_two_offsets"] < 3,
    }
    assert all(assertions.values())
    return {
        "PantheonPlus_CEPH_DIST": {
            "independent": calibrator_source_owned,
            "nonzero_weight": source_checks["ceph_distance"] and calibrator_rank_closed,
            "zero_point_closed": source_checks["calibrates_M"] and calibrator_rank_closed,
            "same_object": not projective_not_operational_distance,
            "bridge_owned": not transfer_imported,
            "source_owned": calibrator_source_owned,
        },
        "PantheonPlus_relative": {
            "independent": pantheon_observed,
            "nonzero_weight": pantheon_observed,
            "zero_point_closed": not relative_offset_open,
            "same_object": not projective_not_operational_distance,
            "bridge_owned": not transfer_imported,
            "source_owned": pantheon_observed,
        },
        "DES_Dovekie": {
            "independent": des_observed,
            "nonzero_weight": des_observed,
            "zero_point_closed": not des_normalization_open,
            "same_object": not projective_not_operational_distance,
            "bridge_owned": not transfer_imported,
            "source_owned": des_observed,
        },
        "two_relative_releases": {
            "independent": pantheon_observed and des_observed,
            "nonzero_weight": exact_ranks["relative_two_offsets"] > 0,
            "zero_point_closed": not assertions["two_relative_rank_deficient"],
            "same_object": not projective_not_operational_distance,
            "bridge_owned": not transfer_imported,
            "source_owned": pantheon_observed and des_observed,
        },
        "cmb_temp": {
            "independent": "observed temperature field on sky" in cmb_types,
            "nonzero_weight": not cmb_source_open,
            "zero_point_closed": not cmb_source_open,
            "same_object": not cmb_source_open,
            "bridge_owned": not cmb_source_open,
            "source_owned": not cmb_source_open,
        },
        "G276_clock_control": {
            "independent": clock_direct,
            "nonzero_weight": clock_direct,
            "zero_point_closed": clock_direct,
            "same_object": clock_direct,
            "bridge_owned": clock_direct,
            "source_owned": clock_direct,
        },
    }


def main(no_write: bool = False) -> None:
    expected = {
        "Data/Pantheon+SH0ES.dat": "1cb0fc379ef066afdc2ffd1857681cc478024570d8a3eba284fb645775198cf8",
        "Data/Pantheon+SH0ES_STAT+SYS.cov": "abf806d966485e64afdb359c87bffc0ecc00d05eff0a31ced66f247385df0fdc",
        "/media/udt-admin/ScratchDisk/Data/UDT_DES_SN5YR_DOVEKIE_2026-08-15/4_DISTANCES_COVMAT/README.md": "7afa1b4c11f465d90eeb0352eb4ca0721f2baa856f545e16ac24af9aa067cf7e",
        "/media/udt-admin/ScratchDisk/Data/UDT_DES_SN5YR_DOVEKIE_2026-08-15/4_DISTANCES_COVMAT/DES-Dovekie_HD.csv": "2f57019d783eaa976df80a41b0054171a2d994ee9808d715ce850c2df5720aaf",
    }
    for name, wanted in expected.items():
        path = Path(name)
        if not path.is_absolute():
            path = ROOT / path
        assert digest(path) == wanted
    sealed_expected = {
        "sources/PantheonPlus_4_DISTANCES_AND_COVAR_README.txt": "e2b0d262757f01c1794a938c78d32600a21e289b2a0320e5c660c4c6fc9aa87e",
        "sources/PantheonPlus_SH0ES_cosmosis_likelihood.py": "345fac3781a5cb930b95e91c1c07eb17dcf99b441703bb5e449477519240a59d",
    }
    for name, wanted in sealed_expected.items():
        assert digest(HERE / name) == wanted
    pantheon = parse_pantheon_without_csv()
    assert pantheon == {
        "rows": 1701,
        "calibrator_rows": 77,
        "unique_calibrator_cids": 43,
        "ceph_min": 29.177,
        "ceph_max": 34.526,
    }
    des_root = Path(
        "/media/udt-admin/ScratchDisk/Data/"
        "UDT_DES_SN5YR_DOVEKIE_2026-08-15/4_DISTANCES_COVMAT"
    )
    readme = (des_root / "README.md").read_text()
    assert "assuming H0 of 70" in readme
    assert "global parameters are determined from the likelihood analysis" in readme
    cmb_types = (
        ROOT / "udt_cmb_G79_same_geometry_dimensional_sne_query_2026-08-11/TYPE_LEDGER.tsv"
    ).read_text()
    assert "cmb_temp\tobserved temperature field on sky\tunowned source field" in cmb_types
    assert "\tOPEN_NO_OWNER\t" in cmb_types
    source_semantics = sealed_semantics()
    covariance_rank = covariance_weighted_independence()

    ranks = {
        "relative_one": rank_by_minors([[1, 1], [1, 1]], 2),
        "relative_two_offsets": rank_by_minors([[1, 1, 0], [1, 0, 1]], 3),
        "calibrator_plus_flow": rank_by_minors([[0, 1], [1, 1]], 2),
        "cmb_unknown_source": rank_by_minors([[0, 1], [0, 1]], 2),
    }
    assert ranks == {
        "relative_one": 1,
        "relative_two_offsets": 2,
        "calibrator_plus_flow": 2,
        "cmb_unknown_source": 1,
    }

    facts = source_derived_classification_facts(source_semantics, covariance_rank, ranks)
    derived_classes = {name: classify_from_facts(**values) for name, values in facts.items()}
    assert derived_classes == {
        "PantheonPlus_CEPH_DIST": "CONDITIONAL_TRANSFER_OR_DISTANCE_ANCHOR",
        "PantheonPlus_relative": "RELATIVE_ONLY",
        "DES_Dovekie": "RELATIVE_ONLY",
        "two_relative_releases": "RELATIVE_ONLY",
        "cmb_temp": "NOT_CURRENTLY_SCALE_TYPED",
        "G276_clock_control": "DIRECT_NONZERO_WEIGHT_ANCHOR",
    }
    result = {
        "status": "VERIFIED_WITH_CAVEATS",
        "implementation_independent": True,
        "reads_production_output": False,
        "imports_production": False,
        "pantheon_schema": pantheon,
        "sealed_primary_source_checks": source_semantics,
        "actual_covariance_weighted_rank": covariance_rank,
        "exact_design_ranks": ranks,
        "classification": derived_classes,
        "classification_derived_from_explicit_predicate": True,
        "classification_facts_derived_from_sources_and_computation": True,
        "caveat": (
            "PantheonPlus_identifiability_requires_the_published_distance_ladder_and_a_declared_"
            "UDT_operational_distance_or_radiative_transfer_bridge;_it_is_not_a_native_G276_clock_record"
        ),
        "fit_performed": False,
        "scale_computed": False,
    }
    if not no_write:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    main(no_write=parser.parse_args().no_write)

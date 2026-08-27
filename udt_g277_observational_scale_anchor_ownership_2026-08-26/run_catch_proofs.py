#!/usr/bin/env python3
"""Nonvacuous hostile overclaim controls for G277."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "CATCH_PROOF_RESULT.json"


def direct_anchor_allowed(facts: dict[str, object]) -> tuple[bool, str]:
    required = (
        "independent",
        "nonzero_weight",
        "zero_point_closed",
        "same_object",
        "bridge_owned",
        "source_owned",
    )
    for criterion in required:
        if not bool(facts[criterion]):
            return False, criterion
    return True, "accepted"


def pure_length_dimension(exponents: tuple[int, int]) -> bool:
    length, time = exponents
    return length == 1 and time == 0


def xmax_allowed(*, populated_boundary: bool, global_completion: bool) -> tuple[bool, str]:
    if not populated_boundary:
        return False, "populated_boundary"
    if not global_completion:
        return False, "global_completion"
    return True, "accepted"


def source_semantics() -> dict[str, bool]:
    readme = (HERE / "sources/PantheonPlus_4_DISTANCES_AND_COVAR_README.txt").read_text()
    likelihood = (HERE / "sources/PantheonPlus_SH0ES_cosmosis_likelihood.py").read_text()
    des = Path(
        "/media/udt-admin/ScratchDisk/Data/"
        "UDT_DES_SN5YR_DOVEKIE_2026-08-15/4_DISTANCES_COVMAT/README.md"
    ).read_text()
    cmb = (
        ROOT / "udt_cmb_G79_same_geometry_dimensional_sne_query_2026-08-11/TYPE_LEDGER.tsv"
    ).read_text()
    checks = {
        "pantheon_is_distance_not_clock": (
            "CEPH_DIST - cepheid calculated absolute distance to host" in readme
            and "Cepheid host distances as the \"theory\"" in likelihood
        ),
        "des_conventional_normalization": "assuming H0 of 70" in des,
        "cmb_source_unowned": "cmb_temp\tobserved temperature field on sky\tunowned source field" in cmb,
    }
    assert all(checks.values())
    return checks


def main(no_write: bool = False) -> None:
    semantics = source_semantics()
    cases = {
        "metric_self_record_called_independent": dict(
            independent=False,
            nonzero_weight=True,
            zero_point_closed=True,
            same_object=True,
            bridge_owned=True,
            source_owned=True,
        ),
        "zero_weight_normalized_state_called_direct": dict(
            independent=True,
            nonzero_weight=False,
            zero_point_closed=True,
            same_object=True,
            bridge_owned=True,
            source_owned=True,
        ),
        "relative_catalog_called_direct": dict(
            independent=True,
            nonzero_weight=True,
            zero_point_closed=False,
            same_object=True,
            bridge_owned=True,
            source_owned=True,
        ),
        "two_relative_catalogs_called_direct": dict(
            independent=True,
            nonzero_weight=True,
            zero_point_closed=False,
            same_object=False,
            bridge_owned=False,
            source_owned=True,
        ),
        "DES_H0_70_called_UDT_direct": dict(
            independent=True,
            nonzero_weight=True,
            zero_point_closed=not semantics["des_conventional_normalization"],
            same_object=True,
            bridge_owned=True,
            source_owned=True,
        ),
        "Pantheon_CEPH_DIST_called_native_clock": dict(
            independent=True,
            nonzero_weight=True,
            zero_point_closed=True,
            same_object=not semantics["pantheon_is_distance_not_clock"],
            bridge_owned=True,
            source_owned=True,
        ),
        "imported_transfer_called_owned": dict(
            independent=True,
            nonzero_weight=True,
            zero_point_closed=True,
            same_object=True,
            bridge_owned=False,
            source_owned=True,
        ),
        "cmb_temp_called_direct_without_source": dict(
            independent=True,
            nonzero_weight=True,
            zero_point_closed=True,
            same_object=True,
            bridge_owned=True,
            source_owned=not semantics["cmb_source_unowned"],
        ),
    }
    rejected: dict[str, str] = {}
    for name, facts in cases.items():
        accepted, failed_criterion = direct_anchor_allowed(facts)
        assert not accepted
        rejected[name] = failed_criterion

    assert not pure_length_dimension((1, -1))
    rejected["c_E_alone_called_length"] = "dimensional_type"
    accepted_xmax, failed_xmax = xmax_allowed(populated_boundary=False, global_completion=True)
    assert not accepted_xmax and failed_xmax == "populated_boundary"
    rejected["ell_called_Xmax_without_populated_boundary"] = failed_xmax
    accepted_xmax, failed_xmax = xmax_allowed(populated_boundary=True, global_completion=False)
    assert not accepted_xmax and failed_xmax == "global_completion"
    rejected["ell_called_Xmax_without_global_completion"] = failed_xmax
    required_criteria = {
        "independent",
        "nonzero_weight",
        "zero_point_closed",
        "same_object",
        "bridge_owned",
        "source_owned",
        "dimensional_type",
        "populated_boundary",
        "global_completion",
    }
    assert len(rejected) == 11
    assert required_criteria.issubset(set(rejected.values()))
    assert all(reason != "accepted" for reason in rejected.values())
    result = {
        "status": "PASS",
        "rejected_overclaims": len(rejected),
        "failed_criterion_by_overclaim": rejected,
        "required_criteria_covered": sorted(required_criteria),
        "unconditional_true_controls": 0,
        "phrase_anywhere_controls": 0,
        "literal_missing_column_semantic_controls": 0,
    }
    if not no_write:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    main(no_write=parser.parse_args().no_write)

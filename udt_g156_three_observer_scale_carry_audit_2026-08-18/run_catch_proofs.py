#!/usr/bin/env python3
"""Mutation catches for the G156 category and conclusion boundaries."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent
QUALIFIED_LANDING = (
    "PAIR_METRIC_CANONICALLY_SUPPLIES_POSITIVE_HALF_DENSITY_SECTION__"
    "ANY_SUPPLIED_TYPED_CARRY_INDUCES_GAUGE_INVARIANT_LOG_DETERMINANT_CHARACTER__"
    "FULL_CLOSURE_IMPLIES_BUT_IS_NOT_IMPLIED_BY_SCALE_CLOSURE__"
    "OWNED_CHART_OVERLAP_AND_LEVI_CIVITA_CARRIES_ARE_SCALE_FLAT__"
    "ARBITRARY_SUPPLIED_NONISOMETRIC_CARRIES_NEED_NOT_BE_FLAT__"
    "NO_METRIC_OWNED_CROSS_QUERY_CARRY_OR_KAPPA_HISTORY"
)


BASE = {
    "half_density_carrier": "DERIVED",
    "scalar_carry": "CONDITIONAL_ON_TYPED_CARRY",
    "single_query_scale": "FLAT_ENDPOINT_EXACT",
    "genuine_overlap_scale": "ZERO",
    "levi_civita_scale": "ZERO",
    "scale_closure_implies_full_closure": False,
    "metric_owned_cross_query_nonisometric_carry": False,
    "metric_owned_kappa_history": False,
    "landing": QUALIFIED_LANDING,
    "source_count": 19,
}


def validate(item):
    assert item["half_density_carrier"] == "DERIVED"
    assert item["scalar_carry"] == "CONDITIONAL_ON_TYPED_CARRY"
    assert item["single_query_scale"] == "FLAT_ENDPOINT_EXACT"
    assert item["genuine_overlap_scale"] == "ZERO"
    assert item["levi_civita_scale"] == "ZERO"
    assert item["scale_closure_implies_full_closure"] is False
    assert item["metric_owned_cross_query_nonisometric_carry"] is False
    assert item["metric_owned_kappa_history"] is False
    assert item["landing"] == QUALIFIED_LANDING
    assert item["source_count"] == 19


def catch(name, key, value):
    sample = deepcopy(BASE)
    sample[key] = value
    try:
        validate(sample)
    except AssertionError:
        return {"name": name, "caught": True}
    return {"name": name, "caught": False}


def main():
    validate(BASE)
    catches = [
        catch("treat_kappa_coefficient_as_coordinate_scalar", "half_density_carrier", "SCALAR_KAPPA"),
        catch("promote_conditional_determinant_carry_to_metric_selector", "scalar_carry", "METRIC_SELECTED"),
        catch("infer_full_matrix_closure_from_scale_closure", "scale_closure_implies_full_closure", True),
        catch("assign_nonzero_levi_civita_scale_holonomy", "levi_civita_scale", "NONZERO"),
        catch("invent_cross_query_carry_from_shared_endpoints", "metric_owned_cross_query_nonisometric_carry", True),
        catch("promote_scale_carry_to_kappa_evolution", "metric_owned_kappa_history", True),
        catch("change_registered_landing", "landing", "METRIC_OWNED_NONTRIVIAL_SCALE_CONNECTION"),
        catch("omit_frozen_source", "source_count", 18),
    ]
    assert all(item["caught"] for item in catches)
    result = {"status": "PASS", "catch_count": len(catches), "caught": catches}
    (HERE / "CATCH_PROOF_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

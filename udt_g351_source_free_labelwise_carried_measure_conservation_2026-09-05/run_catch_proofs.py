#!/usr/bin/env python3
"""Hostile mathematical and semantic catch proofs for G351."""

from fractions import Fraction as F
import json


def validate(claim):
    failures = []
    p = claim["observer_weight"]
    a = claim["frequency_exponent"]
    q = claim["area_exponent"]
    if (a - p) * F(1) != 0:
        failures.append("frequency exponent violates conservation witness")
    if (q + 1) * F(1) != 0:
        failures.append("area exponent violates conservation witness")
    if claim["p_selected"]:
        failures.append("conservation does not select observer weight")
    if claim["zero_creates_content"]:
        failures.append("conservation cannot create source content")
    if claim["finite_density_at_all_caustics"]:
        failures.append("inverse-area density need not remain finite at caustics")
    if claim["full_measure_has_ordinary_density"]:
        failures.append("an arbitrary finite measure may have a singular part with no ordinary density")
    if claim["uses_zero_density_ratio"]:
        failures.append("zero density requires division-free equality rather than a ratio")
    if claim["union_area_replaces_label_measure"]:
        failures.append("geometric union drops label multiplicity")
    if claim["cross_label_physics_selected"]:
        failures.append("measure additivity does not select physical aggregation")
    if claim["premise_status"] != "OWNER_ADOPTED_PROVISIONAL_PREMISE":
        failures.append("conservation premise ownership changed")
    if claim["imports_light_physics"]:
        failures.append("light or energy physics imported")
    if claim["changes_metric_kernel_history_scale_xmax_canon"]:
        failures.append("bounded ceiling violated")
    return failures


def main():
    baseline = {
        "observer_weight": F(3, 2),
        "frequency_exponent": F(3, 2),
        "area_exponent": F(-1),
        "p_selected": False,
        "zero_creates_content": False,
        "finite_density_at_all_caustics": False,
        "full_measure_has_ordinary_density": False,
        "uses_zero_density_ratio": False,
        "union_area_replaces_label_measure": False,
        "cross_label_physics_selected": False,
        "premise_status": "OWNER_ADOPTED_PROVISIONAL_PREMISE",
        "imports_light_physics": False,
        "changes_metric_kernel_history_scale_xmax_canon": False,
    }
    mutations = {
        "wrong_q": {"area_exponent": F(0)},
        "wrong_frequency_weight": {"frequency_exponent": F(5, 2)},
        "select_p": {"p_selected": True},
        "create_from_zero": {"zero_creates_content": True},
        "finite_caustic_density": {"finite_density_at_all_caustics": True},
        "promote_full_measure_to_density": {"full_measure_has_ordinary_density": True},
        "divide_zero_density": {"uses_zero_density_ratio": True},
        "replace_measure_by_union": {"union_area_replaces_label_measure": True},
        "select_cross_label_physics": {"cross_label_physics_selected": True},
        "promote_premise_to_derived": {"premise_status": "DERIVED"},
        "import_light_physics": {"imports_light_physics": True},
        "change_bounded_science": {"changes_metric_kernel_history_scale_xmax_canon": True},
    }
    baseline_failures = validate(baseline)
    caught = {}
    diagnostics = {}
    for name, changes in mutations.items():
        candidate = dict(baseline)
        candidate.update(changes)
        errors = validate(candidate)
        caught[name] = bool(errors)
        diagnostics[name] = errors
    result = {
        "all_passed": not baseline_failures and all(caught.values()),
        "baseline_failures": baseline_failures,
        "caught": caught,
        "diagnostics": diagnostics,
        "mutations_caught": sum(caught.values()),
        "mutations_total": len(caught),
        "classification": "MATHEMATICAL_WITNESS_AND_SEMANTIC_REGRESSION_GUARD",
    }
    print(json.dumps(result, indent=2, sort_keys=True) + "\n", end="")
    if not result["all_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import copy
import csv
import json
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
F = Fraction
EXPECTED_STAMPS = {
    "COPRESENCE": "WORKING_INTERPRETIVE_FRAME",
    "METRIC_CAUSAL_STRUCTURE": "DERIVED_CONDITIONAL",
    "INSTANTANEOUS_OPERATIONAL_ACCESS": "NOT_DERIVED",
    "COMPLETE_WHOLE_SOLUTION_LAW": "OPEN",
}
EXPECTED_AXIS = {
    "phi": "f/50",
    "a": "1/64",
    "R": "1",
    "event": "north_stereographic",
    "invariants": ["scalar_curvature", "Ricci_squared", "Kretschmann"],
}


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def trim(poly: list[F]) -> list[F]:
    result = list(poly)
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def derivative(poly: list[F]) -> list[F]:
    return trim([F(index) * value for index, value in enumerate(poly)][1:] or [F(0)])


def divide(dividend: list[F], divisor: list[F]) -> tuple[list[F], list[F]]:
    dividend = trim(dividend)
    divisor = trim(divisor)
    assert divisor != [F(0)]
    if len(dividend) < len(divisor):
        return [F(0)], dividend
    quotient = [F(0)] * (len(dividend) - len(divisor) + 1)
    remainder = list(dividend)
    while remainder != [F(0)] and len(remainder) >= len(divisor):
        power = len(remainder) - len(divisor)
        factor = remainder[-1] / divisor[-1]
        quotient[power] = factor
        for index, value in enumerate(divisor):
            remainder[index + power] -= factor * value
        remainder = trim(remainder)
    return trim(quotient), trim(remainder)


def gcd(left: list[F], right: list[F]) -> list[F]:
    left, right = trim(left), trim(right)
    while right != [F(0)]:
        _, remainder = divide(left, right)
        left, right = right, remainder
    return [value / left[-1] for value in left]


def evaluate(poly: list[F], value: F) -> F:
    result = F(0)
    for coefficient in reversed(poly):
        result = result * value + coefficient
    return result


def sturm_sequence(poly: list[F]) -> list[list[F]]:
    squarefree_divisor = gcd(poly, derivative(poly))
    squarefree, remainder = divide(poly, squarefree_divisor)
    assert remainder == [F(0)]
    sequence = [trim(squarefree), derivative(squarefree)]
    while sequence[-1] != [F(0)]:
        _, remainder = divide(sequence[-2], sequence[-1])
        if remainder == [F(0)]:
            break
        sequence.append([-value for value in remainder])
    return sequence


def variations(signs: list[int]) -> int:
    nonzero = [sign for sign in signs if sign]
    return sum(left != right for left, right in zip(nonzero, nonzero[1:]))


def finite_variations(sequence: list[list[F]], value: F) -> int:
    signs = []
    for poly in sequence:
        result = evaluate(poly, value)
        signs.append(1 if result > 0 else -1 if result < 0 else 0)
    return variations(signs)


def infinite_variations(sequence: list[list[F]], positive: bool) -> int:
    signs = []
    for poly in sequence:
        sign = 1 if poly[-1] > 0 else -1
        if not positive and (len(poly) - 1) % 2:
            sign *= -1
        signs.append(sign)
    return variations(signs)


def validation_errors(state: dict[str, object]) -> list[str]:
    result = state["result"]
    assert isinstance(result, dict)
    errors: list[str] = []
    if result.get("premise_stamps") != EXPECTED_STAMPS:
        errors.append("stamps")
    if result.get("frozen_axis") != EXPECTED_AXIS:
        errors.append("frozen_axis")
    if result.get("degree_bound") != 9 or int(result.get("actual_degree", -1)) > 9:
        errors.append("degree")
    nodes = state["nodes"]
    if (
        not isinstance(nodes, list)
        or [row.get("node_id") for row in nodes] != [f"N{i:02d}" for i in range(1, 11)]
        or [row.get("lambda") for row in nodes] != [str(value) for value in range(-4, 6)]
    ):
        errors.append("nodes")
    if result.get("production_nodes_reproduced_exactly") is not True:
        errors.append("interpolation")
    holdouts = state["holdouts"]
    if not isinstance(holdouts, list) or len(holdouts) != 7 or any(row.get("exact_match") != "YES" for row in holdouts):
        errors.append("holdouts")
    coefficients = state["coefficients"]
    if not isinstance(coefficients, list) or len(coefficients) != int(result.get("actual_degree", -1)) + 1 or coefficients[-1].get("nonzero") != "YES":
        errors.append("leading_degree")
    roots = state["roots"]
    if not isinstance(roots, list) or len(roots) != result.get("distinct_real_roots"):
        errors.append("roots")
    if isinstance(roots, list) and any(row.get("multiplicity") != "1" for row in roots):
        errors.append("multiplicity")
    intervals = state["intervals"]
    if not isinstance(intervals, list) or len(intervals) != result.get("certificate_intervals"):
        errors.append("intervals")
    centers = state["centers"]
    if not isinstance(centers, list) or [row.get("candidate_id") for row in centers] != [f"C0{i}" for i in range(1, 7)]:
        errors.append("centers")
    if result.get("other_gates_lambda_independent") is not True:
        errors.append("other_gates")
    if result.get("torch_tolerance") != "2e-9*max(1,abs(D_exact))":
        errors.append("torch_tolerance")
    for flag in ["D_zero_proves_clock_absent", "D_zero_proves_extra_symmetry", "D_zero_proves_metric_singular", "full_configuration_component_claim", "lambda_selected", "physical_phase_claim", "instantaneous_access_claim", "physics_inferences"]:
        if result.get(flag) is not False:
            errors.append(flag)
    if result.get("preregistration_correction_commit") != "2ec7a4b":
        errors.append("preregistration_correction")
    return errors


def main() -> int:
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    coefficients_rows = rows("POLYNOMIAL_COEFFICIENTS.tsv")
    coefficients = [F(row["coefficient"]) for row in coefficients_rows]
    assert len(coefficients) == 8 and coefficients[-1] != 0
    common = gcd(coefficients, derivative(coefficients))
    assert len(common) == 1  # Every root is simple.
    sequence = sturm_sequence(coefficients)
    distinct_real_roots = infinite_variations(sequence, False) - infinite_variations(sequence, True)
    assert distinct_real_roots == 7

    root_rows = rows("REAL_ROOTS.tsv")
    assert len(root_rows) == distinct_real_roots
    for row in root_rows:
        left, right = F(row["left_bound"]), F(row["right_bound"])
        assert left < right
        assert evaluate(coefficients, left) != 0 and evaluate(coefficients, right) != 0
        assert finite_variations(sequence, left) - finite_variations(sequence, right) == 1
        assert row["multiplicity"] == "1"

    interval_rows = rows("LAMBDA_INTERVALS.tsv")
    assert len(interval_rows) == distinct_real_roots + 1
    for row in interval_rows:
        value = evaluate(coefficients, F(row["exact_sample"]))
        observed = "POSITIVE" if value > 0 else "NEGATIVE"
        assert observed == row["determinant_sign"]

    state = {
        "result": result,
        "nodes": rows("PRODUCTION_NODE_OUTCOMES.tsv"),
        "holdouts": rows("EXACT_HOLDOUT_OUTCOMES.tsv"),
        "coefficients": coefficients_rows,
        "roots": root_rows,
        "intervals": interval_rows,
        "centers": rows("CENTER_ASSIGNMENTS.tsv"),
    }
    assert not validation_errors(state), validation_errors(state)

    catches: list[tuple[str, bool, str]] = []

    def mutate(identifier: str, change, label: str) -> None:
        mutant = copy.deepcopy(state)
        change(mutant)
        catches.append((identifier, bool(validation_errors(mutant)), label))

    mutate("F01", lambda x: x["result"].__setitem__("instantaneous_access_claim", True), "instant_access_rejected")
    mutate("F02", lambda x: x["result"]["premise_stamps"].pop("COPRESENCE"), "stamp_loss_rejected")
    mutate("F03", lambda x: x["result"]["frozen_axis"].__setitem__("a", "1/32"), "axis_retake_rejected")
    mutate("F04", lambda x: x["result"].__setitem__("degree_bound", 10), "degree_change_rejected")
    mutate("F05", lambda x: x["nodes"].pop(), "missing_node_rejected")
    mutate("F06", lambda x: x["result"].__setitem__("production_nodes_reproduced_exactly", False), "float_interpolation_rejected")
    mutate("F07", lambda x: x["holdouts"][0].__setitem__("exact_match", "NO"), "holdout_mismatch_rejected")
    mutate("F08", lambda x: x["coefficients"][-1].__setitem__("nonzero", "NO"), "false_degree_rejected")
    mutate("F09", lambda x: x["roots"].pop(), "missing_root_rejected")
    mutate("F10", lambda x: x["roots"][0].__setitem__("multiplicity", "2"), "multiplicity_change_rejected")
    mutate("F11", lambda x: x["intervals"].pop(), "missing_interval_rejected")
    mutate("F12", lambda x: x["centers"].pop(), "missing_center_rejected")
    mutate("F13", lambda x: x["result"].__setitem__("other_gates_lambda_independent", False), "other_gate_claim_rejected")
    mutate("F14", lambda x: x["result"].__setitem__("torch_tolerance", "1e-2"), "loose_tolerance_rejected")
    mutate("F15", lambda x: x["result"].__setitem__("D_zero_proves_clock_absent", True), "clock_loss_rejected")
    mutate("F16", lambda x: x["result"].__setitem__("D_zero_proves_extra_symmetry", True), "symmetry_overclaim_rejected")
    mutate("F17", lambda x: x["result"].__setitem__("D_zero_proves_metric_singular", True), "singularity_overclaim_rejected")
    mutate("F18", lambda x: x["result"].__setitem__("full_configuration_component_claim", True), "full_component_overclaim_rejected")
    mutate("F19", lambda x: x["result"].__setitem__("lambda_selected", True), "lambda_selection_rejected")
    mutate("F20", lambda x: x["result"].__setitem__("instantaneous_access_claim", True), "semantic_selection_rejected")
    mutate("F21", lambda x: x["result"].__setitem__("physics_inferences", True), "physics_inference_rejected")
    mutate("F22", lambda x: x["nodes"][0].__setitem__("lambda", "-5"), "node_retune_rejected")
    assert len(catches) == 22 and all(passed for _, passed, _ in catches)
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["catch_id", "result", "exercise"])
        writer.writerows((identifier, "PASS" if passed else "FAIL", label)
                         for identifier, passed, label in catches)

    independent = {
        "method": "STANDARD_LIBRARY_FRACTION_STURM_NO_SYMPY_IMPORT",
        "actual_degree": len(coefficients) - 1,
        "polynomial_squarefree": True,
        "distinct_real_roots": distinct_real_roots,
        "root_brackets_one_each": len(root_rows),
        "interval_signs_reproduced": len(interval_rows),
        "catch_proofs_passed": len(catches),
        "catch_proofs_total": len(catches),
    }
    (HERE / "STURM_RESULT.json").write_text(
        json.dumps(independent, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("PASS stdlib_sturm_distinct_real_roots 7")
    print("PASS simple_root_brackets 7/7")
    print("PASS interval_signs 8/8")
    print("PASS center_assignments 6/6")
    print("PASS catch_proofs 22/22")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

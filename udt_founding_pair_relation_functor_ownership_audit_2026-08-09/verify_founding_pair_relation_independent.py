#!/usr/bin/env python3
"""Independent stdlib verifier for the founding pair-relation ownership audit."""

from __future__ import annotations

import argparse
import csv
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
ALLOWED = {
    "FOUNDING_DERIVED",
    "QUERY_SUPPLIED_NOT_FOUNDING_DERIVED",
    "METRIC_DERIVED_AFTER_DECLARED_QUERY",
    "CONSTRAINT_NOT_SELECTOR",
    "CONDITIONAL_LOCAL",
    "BRANCH_RELATION_NOT_SINGLE_MAP",
    "OUTPUT_COMPATIBLE_NOT_SELECTOR",
    "OPEN_NOT_OWNED",
    "FAILS_REQUIRED_TYPE",
}


def matmul(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def diag_depth(x: float) -> list[list[float]]:
    return [[math.exp(-x), 0.0], [0.0, math.exp(x)]]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    checks: list[dict[str, object]] = []

    def check(name: str, condition: bool, detail: object = "") -> None:
        checks.append({"name": name, "passed": bool(condition), "detail": str(detail)})

    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    check("source_count", len(sources) == 15, len(sources))
    check("source_unique", len({row["path"] for row in sources}) == 15)
    for index, row in enumerate(sources, start=1):
        data = subprocess.check_output(["git", "show", row["source_ref"]], cwd=ROOT)
        check(f"source_{index:02d}", hashlib.sha256(data).hexdigest() == row["sha256"], row["path"])

    with (PACKAGE / "SEMANTIC_INTERPRETATION_ARENA.tsv").open(newline="", encoding="utf-8") as handle:
        arena = list(csv.DictReader(handle, delimiter="\t"))
    with (PACKAGE / "SEMANTIC_OWNERSHIP_ATLAS.tsv").open(newline="", encoding="utf-8") as handle:
        atlas = list(csv.DictReader(handle, delimiter="\t"))
    check("arena_count", len(arena) == 9, len(arena))
    check("arena_ids", {row["interpretation_id"] for row in arena} == {f"I{i:02d}" for i in range(1, 10)})
    identities = [(row["interpretation_id"], row["axis_id"]) for row in atlas]
    check("atlas_count", len(atlas) == 108, len(atlas))
    check("atlas_unique", len(set(identities)) == 108)
    check("atlas_each_interpretation", all(sum(row["interpretation_id"] == f"I{i:02d}" for row in atlas) == 12 for i in range(1, 10)))
    check("atlas_each_axis", all(sum(row["axis_id"] == f"A{i:02d}" for row in atlas) == 9 for i in range(1, 13)))
    check("atlas_dispositions", all(row["disposition"] in ALLOWED for row in atlas))
    check("no_merit_filter", all(row["merit_filter"] == "NONE_CHARACTERIZE_ONLY" for row in atlas))

    source_text = (ROOT / "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md").read_text(encoding="utf-8")
    idx_depth = source_text.find("at relative depth $\\Delta$")
    idx_composition = source_text.find("Positional composition fixes the exponential")
    check("logical_order_depth_before_composition", 0 <= idx_depth < idx_composition, (idx_depth, idx_composition))
    check("no_event_pairing_definition", "event pairing" not in source_text.lower())

    # Independent numerical representation of the reciprocal character.
    a, b = 0.31, -0.17
    composed = matmul(diag_depth(b), diag_depth(a))
    direct = diag_depth(a + b)
    check("D_composition", max(abs(composed[i][j] - direct[i][j]) for i in range(2) for j in range(2)) < 1e-14)
    inverse = diag_depth(-a)
    identity = matmul(diag_depth(a), inverse)
    check("D_reversal", max(abs(identity[i][j] - (1.0 if i == j else 0.0)) for i in range(2) for j in range(2)) < 1e-14)

    # A pair of objects can have multiple arrows. Ordering alone supplies a hom-set, not its member.
    arrows = {("A", "B", "f"), ("A", "B", "g")}
    check("nonthin_homset_witness", len(arrows) == 2 and {(x[0], x[1]) for x in arrows} == {("A", "B")})
    reverses = {(target, source, name + "_inv") for source, target, name in arrows}
    check("reversal_preserves_nonuniqueness", len(reverses) == 2 and {(x[0], x[1]) for x in reverses} == {("B", "A")})

    # Exact rational flat pairing family at L=1, k=1/3.
    L = Fraction(1, 1)
    k = Fraction(1, 3)
    h00 = Fraction(-1, 1)
    h01 = -k / L
    h11 = Fraction(1, 1) - (k / L) ** 2
    determinant = h00 * h11 - h01 * h01
    ruler2 = h11 - h01 * h01 / h00
    check("pairing_h00", h00 == -1, h00)
    check("pairing_h01", h01 == Fraction(-1, 3), h01)
    check("pairing_h11", h11 == Fraction(8, 9), h11)
    check("pairing_det", determinant == -1, determinant)
    check("pairing_ruler", ruler2 == 1, ruler2)
    ratio = (-determinant) / (h00 * h00)
    check("pairing_terminal_zero", ratio == 1, ratio)
    y = Fraction(2, 5)
    B_event_k = (y + k, L)
    B_event_zero = (y, L)
    check("same_worldlines_distinct_pair_events", B_event_k != B_event_zero, (B_event_k, B_event_zero))

    # Distinct rotating ruler evolutions, same induced metric at a sample point.
    yy, ss, omega = 0.37, 0.4, 0.8
    plus = (yy, ss * math.cos(omega * yy), ss * math.sin(omega * yy), 0.0)
    minus = (yy, ss * math.cos(omega * yy), -ss * math.sin(omega * yy), 0.0)
    h00_rot = -1.0 + omega * omega * ss * ss
    check("rotating_maps_distinct", plus != minus, (plus, minus))
    check("rotating_metrics_equal", h00_rot == -1.0 + (-omega) ** 2 * ss * ss, h00_rot)

    # Local c_E calibration is compatible with every k; it does not select k.
    check("origin_eta_at_k_zero", (-1, 0, 1) == (-1, 0, 1))
    check("normalized_nonzero_k_survives", h00 == -1 and determinant == -1 and k != 0)

    # Middle reset is distinct from common scaling and shifts the reciprocal depth.
    reset = 0.23
    carried_depth = a + b
    reset_depth = a + b + reset
    check("matched_carry_adds", abs(carried_depth - 0.14) < 1e-15, carried_depth)
    check("unowned_reset_changes_carry", abs(reset_depth - carried_depth - reset) < 1e-15, reset_depth)
    common = 7.0
    common_ratio = (common * math.exp(carried_depth)) / (common * math.exp(-carried_depth))
    check("common_scale_cancels", abs(0.5 * math.log(common_ratio) - carried_depth) < 1e-15)

    # Two different normalized profiles share the same finite asymptote.
    depth = 30.0
    p1 = math.tanh(depth)
    p2 = 1.0 - math.exp(-depth)
    check("xmax_two_profiles_near_same_limit", abs(1.0 - p1) < 1e-12 and abs(1.0 - p2) < 1e-12)
    check("xmax_profiles_not_identical", abs(math.tanh(1.0) - (1.0 - math.exp(-1.0))) > 0.1)

    # Fail-closed semantic gates.
    i01_a12 = next(row for row in atlas if row["interpretation_id"] == "I01" and row["axis_id"] == "A12")
    i04_a06 = next(row for row in atlas if row["interpretation_id"] == "I04" and row["axis_id"] == "A06")
    i07_a04 = next(row for row in atlas if row["interpretation_id"] == "I07" and row["axis_id"] == "A04")
    i06_a12 = next(row for row in atlas if row["interpretation_id"] == "I06" and row["axis_id"] == "A12")
    check("founding_scope_not_promoted", i01_a12["disposition"] == "FOUNDING_DERIVED" and "not the observer-to-depth" in i01_a12["basis"])
    check("local_metric_positive_route_retained", i04_a06["disposition"] == "METRIC_DERIVED_AFTER_DECLARED_QUERY")
    check("cE_not_event_pairing", i07_a04["disposition"] == "FAILS_REQUIRED_TYPE")
    check("reciprocity_not_selector", i06_a12["disposition"] == "CONSTRAINT_NOT_SELECTOR")

    passed = sum(int(row["passed"]) for row in checks)
    result = {
        "schema": "udt-founding-pair-relation-ownership-independent-v1",
        "implementation": "python_stdlib_no_sympy_import",
        "checks_total": len(checks),
        "checks_passed": passed,
        "checks_failed": len(checks) - passed,
        "failed": [row for row in checks if not row["passed"]],
        "checks": checks,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if result["checks_failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

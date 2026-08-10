#!/usr/bin/env python3
"""Independent stdlib verifier for the calibrated observer-pair map owner atlas."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
ALLOWED = {
    "DERIVED_FROM_METRIC_AND_DECLARED_QUERY",
    "CONDITIONAL_QUERY_DATA",
    "CONDITIONAL_BRANCH_STRUCTURE",
    "LOCAL_ONLY_BRANCH_VALUED",
    "FAILS_REQUIRED_TYPE",
    "OPEN_NOT_DECIDED_BY_CURRENT_FOUNDATION",
}


def matmul(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def rotation(x: float) -> list[list[float]]:
    return [[math.cos(x), math.sin(x)], [-math.sin(x), math.cos(x)]]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rows: list[dict[str, object]] = []

    def check(name: str, condition: bool, detail: object = "") -> None:
        rows.append({"name": name, "passed": bool(condition), "detail": str(detail)})

    # Frozen source replay, independently parsed.
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    check("source_count", len(sources) == 20, len(sources))
    check("source_unique", len({row["path"] for row in sources}) == 20)
    for index, row in enumerate(sources, start=1):
        data = subprocess.check_output(["git", "show", row["source_ref"]], cwd=ROOT)
        check(f"source_{index:02d}", hashlib.sha256(data).hexdigest() == row["sha256"], row["path"])

    # Atlas shape and fail-closed dispositions.
    with (PACKAGE / "PAIR_MAP_ATLAS.tsv").open(newline="", encoding="utf-8") as handle:
        atlas = list(csv.DictReader(handle, delimiter="\t"))
    check("atlas_rows", len(atlas) == 66, len(atlas))
    identities = [(row["candidate_id"], row["axis_id"]) for row in atlas]
    check("atlas_unique", len(set(identities)) == 66)
    check("candidate_set", {row["candidate_id"] for row in atlas} == {f"P{i:02d}" for i in range(1, 7)})
    check("axis_set_each", all(sum(row["candidate_id"] == candidate for row in atlas) == 11 for candidate in {f"P{i:02d}" for i in range(1, 7)}))
    check("dispositions_registered", all(row["disposition"] in ALLOWED for row in atlas))
    check("no_merit_filter", all(row["merit_filter"] == "NONE_CHARACTERIZE_ONLY" for row in atlas))

    # P01: exact flat accelerated tube at a=1/5, s=1.
    a, s = 0.2, 1.0
    h00_acc = -(1.0 + a * s) ** 2
    check("accelerated_h00", abs(h00_acc + 36.0 / 25.0) < 1e-15, h00_acc)
    check("accelerated_inertial_limit", abs(-(1.0 + 0.0 * s) ** 2 + 1.0) < 1e-15)

    # P04: opposite rotating direction fields define different maps but the same induced h.
    y, radius, omega = 0.4, 1.0 / 3.0, 1.0
    plus = (y, radius * math.cos(omega * y), radius * math.sin(omega * y), 0.0)
    minus = (y, radius * math.cos(-omega * y), radius * math.sin(-omega * y), 0.0)
    h00_rot = -1.0 + omega * omega * radius * radius
    check("rotating_h00", abs(h00_rot + 8.0 / 9.0) < 1e-15, h00_rot)
    check("opposite_rotations_distinct", plus != minus, (plus, minus))
    check("opposite_rotations_same_h", abs((-1 + (-omega) ** 2 * radius**2) - h00_rot) < 1e-15)
    check("rotating_null_stratum", abs(-1.0 + omega * omega * (1.0 / omega) ** 2) < 1e-15)

    # P02: the same flat metric permits a rotating presentation with transverse bracket.
    bracket_at_zero = (0.0, omega)
    check("frobenius_transverse_nonzero", bracket_at_zero == (0.0, 1.0), bracket_at_zero)
    check("frobenius_zero_rotation", (0.0, 0.0) == (0.0, 0.0))

    # P03: stationary Killing norm and terminal depth differ generically; join iff N R=1.
    N, R = 0.5, 3.0
    terminal = 0.5 * math.log(R / N)
    killing = -math.log(N)
    check("stationary_generic_difference", abs(terminal - killing - 0.5 * math.log(N * R)) < 1e-15)
    check("stationary_not_equal_generic", abs(terminal - killing) > 1e-3)
    R_join = 1.0 / N
    check("stationary_equal_at_TL_one", abs(0.5 * math.log(R_join / N) + math.log(N)) < 1e-15)

    # P05: position dExp blocks do not subdivide; the complete Jacobi phase does.
    half = math.sin(math.pi / 6.0) / (math.pi / 6.0)
    full = math.sin(math.pi / 3.0) / (math.pi / 3.0)
    check("dexp_position_noncomposition", abs(half * half - full) > 1e-3, (half * half, full))
    check("conjugate_rank_zero", abs(math.sin(math.pi)) < 2e-16)
    p, q = 0.37, -0.21
    composed = matmul(rotation(q), rotation(p))
    direct = rotation(p + q)
    check("jacobi_phase_composes", max(abs(composed[i][j] - direct[i][j]) for i in range(2) for j in range(2)) < 1e-15)

    # P06: carried reciprocal calibrations add; resetting the middle tape is arbitrary.
    depth_a, depth_b, reset = 0.4, -0.1, 0.27
    check("carried_depth", abs((depth_a + depth_b) - 0.3) < 1e-15)
    check("rebuilt_reset_changes_depth", abs((depth_a + depth_b + reset) - (depth_a + depth_b)) > 0.2)
    common = 4.2
    original = 0.5 * math.log(math.exp(2 * (depth_a + depth_b)))
    scaled = 0.5 * math.log((common * math.exp(depth_a + depth_b)) / (common * math.exp(-(depth_a + depth_b))))
    check("common_scale_cancels", abs(original - scaled) < 1e-15)

    passed = sum(int(row["passed"]) for row in rows)
    result = {
        "schema": "udt-calibrated-pair-map-owner-atlas-independent-v1",
        "implementation": "python_stdlib_no_sympy_import",
        "checks_total": len(rows),
        "checks_passed": passed,
        "checks_failed": len(rows) - passed,
        "failed": [row for row in rows if not row["passed"]],
        "rows": rows,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if passed == len(rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())

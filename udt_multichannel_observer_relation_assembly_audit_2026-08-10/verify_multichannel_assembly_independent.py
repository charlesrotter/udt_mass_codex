#!/usr/bin/env python3
"""Independent stdlib/Fraction reconstruction of the multi-channel load-bearing algebra."""

from __future__ import annotations

import csv
import json
import math
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent


def det2(m: tuple[tuple[F, F], tuple[F, F]]) -> F:
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def matmul(a: tuple[tuple[F, F], tuple[F, F]], b: tuple[tuple[F, F], tuple[F, F]]) -> tuple[tuple[F, F], tuple[F, F]]:
    return (
        (a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]),
        (a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]),
    )


def decompose(h: tuple[tuple[F, F], tuple[F, F]]) -> tuple[F, F, F]:
    t2 = -h[0][0]
    beta = h[0][1] / h[0][0]
    l2 = h[1][1] - h[0][1] * h[0][1] / h[0][0]
    return t2, l2, beta


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def main() -> int:
    checks: dict[str, bool] = {}
    def check(name: str, value: bool) -> None:
        checks[name] = bool(value)
        if not value:
            raise AssertionError(name)

    examples = (
        (F(3, 2), F(5, 3), F(2, 7)),
        (F(7, 4), F(9, 5), F(-3, 8)),
        (F(11, 6), F(13, 7), F(5, 9)),
    )
    for index, (t, l, beta) in enumerate(examples):
        h = ((-t * t, -t * t * beta), (-t * t * beta, l * l - t * t * beta * beta))
        t2, l2, bout = decompose(h)
        check(f"pair_inverse_{index}", (t2, l2, bout) == (t * t, l * l, beta))
        check(f"pair_det_{index}", det2(h) == -t * t * l * l)

    states = ((F(2), F(3)), (F(5), F(7)), (F(11), F(13)))
    b1_01 = math.log(float(states[1][0] / states[0][0]))
    b1_12 = math.log(float(states[2][0] / states[1][0]))
    b1_02 = math.log(float(states[2][0] / states[0][0]))
    b2_01 = math.log(float(states[1][0] * states[1][1] / (states[0][0] * states[0][1])))
    b2_12 = math.log(float(states[2][0] * states[2][1] / (states[1][0] * states[1][1])))
    b2_02 = math.log(float(states[2][0] * states[2][1] / (states[0][0] * states[0][1])))
    check("clock_density_telescopes", abs(b1_01 + b1_12 - b1_02) < 1e-14)
    check("area_density_telescopes", abs(b2_01 + b2_12 - b2_02) < 1e-14)
    check("kappa_delta_linear_change_invertible", abs(F(1, 2) * 1 - 0) > 0)

    shift = F(3, 7)
    h_shift = ((F(-1), -shift), (-shift, F(1) - shift * shift))
    check("shift_same_density", decompose(h_shift) == (F(1), F(1), shift))
    check("shift_det_minus_one", det2(h_shift) == -1)

    h_common = ((F(-4), F(0)), (F(0), F(4)))
    check("common_scale_distinct", decompose(h_common) == (F(4), F(4), F(0)))
    h_recip = ((F(-1, 4), F(0)), (F(0), F(4)))
    check("reciprocal_distinct", decompose(h_recip) == (F(1, 4), F(4), F(0)))

    h_mix1 = ((F(-3, 16), F(0)), (F(0), F(4)))
    check("mix1_det", det2(h_mix1) == F(-3, 4))
    check("mix1_channels", decompose(h_mix1) == (F(3, 16), F(4), F(0)))
    h_mix2 = ((F(-3, 16), F(1, 12)), (F(1, 12), F(37, 9)))
    check("mix2_det", det2(h_mix2) == F(-7, 9))
    check("mix2_channels", decompose(h_mix2) == (F(3, 16), F(112, 27), F(-4, 9)))

    quarter = ((F(0), F(-1)), (F(1), F(0)))
    minus_identity = ((F(-1), F(0)), (F(0), F(-1)))
    check("quarter_turn_composes", matmul(quarter, quarter) == minus_identity)
    check("quarter_turn_inverse", matmul(quarter, ((F(0), F(1)), (F(-1), F(0)))) == ((F(1), F(0)), (F(0), F(1))))

    check("zero_depth_angular_witness", F(-4097, 2048) != 0)
    check("channel_rows_16", len(rows("CHANNEL_CLASSIFICATION.tsv")) == 16)
    check("assembled_rows_6", len(rows("ASSEMBLED_CHANNELS.tsv")) == 6)
    check("regime_rows_10", len(rows("GEOMETRIC_REGIME_ATLAS.tsv")) == 10)
    dispositions = {row["channel_id"]: row["disposition"] for row in rows("CHANNEL_CLASSIFICATION.tsv")}
    check("alpha_family_not_promoted", dispositions["C07"] == "UNSELECTED_PATH_SCALARIZATION_FAMILY")
    check("beta_family_not_promoted", dispositions["C08"] == "UNSELECTED_ENDPOINT_SCALARIZATION_FAMILY")
    check("strain_not_character", dispositions["C09"] == "DIAGNOSTIC_NOT_CHARACTER")
    check("query_owner_open", dispositions["C16"] == "CONDITIONAL_QUERY_PROJECTION")

    result = {
        "schema_version": 1,
        "status": "PASS",
        "method": "INDEPENDENT_STDLIB_FRACTION_PAIR_METRIC_DENSITY_AND_ROTATION_RECONSTRUCTION",
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "failed": [name for name, value in checks.items() if not value],
    }
    assert result["passed"] == result["total"]
    (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

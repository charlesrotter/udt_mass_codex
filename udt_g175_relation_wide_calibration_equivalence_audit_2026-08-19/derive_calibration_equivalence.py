#!/usr/bin/env python3
"""Exact symbolic derivation for G175."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
landing = (
    "A_LOCAL_CALIBRATION_DOES_NOT_OWN_RELATION_WIDE_CARRY"
    "__ONE_SUPPLIED_CALIBRATED_PAIR_MAP_DOES"
    "__ALL_ENDPOINT_DEPTHS_FIX_EXACTLY_ONE_CONSTANT_UNIT_CLASS"
    "__POINTWISE_METRIC_UNIT_IS_A_DIFFERENT_CALIBRATION_NOT_THE_FOUNDED_CARRIED_TAPE"
)

A, H, m, f, c, v = sp.symbols("A H m f c v", positive=True)
Ap, Aq, Hp, Hq, mp, mq, fp, fq = sp.symbols(
    "Ap Aq Hp Hq mp mq fp fq", positive=True
)

checks: list[tuple[str, bool]] = []


def check(name: str, expression: sp.Expr) -> None:
    checks.append((name, sp.simplify(expression) == 0))


K = A * H / m**2
Kn = A * H / (f * m) ** 2
check("point_recalibration", Kn - K / f**2)
check("log_shift", sp.log(Kn) / 4 - sp.log(K) / 4 + sp.log(f) / 2)

Kp = Ap * Hp / mp**2
Kq = Aq * Hq / mq**2
Knp = Ap * Hp / (fp * mp) ** 2
Knq = Aq * Hq / (fq * mq) ** 2
Rm = Kq / Kp
Rn = Knq / Knp
check("endpoint_ratio_transition", Rn / Rm - (fp / fq) ** 2)
check("same_pair_reversal", Rm * (Kp / Kq) - 1)
check("constant_unit_cancellation", Rn.subs({fp: c, fq: c}) - Rm)

Kr = sp.symbols("Kr", positive=True)
check("matched_telescope", (Kq / Kp) * (Kr / Kq) - Kr / Kp)
check("metric_unit_normalization", (A * H / H) - A)
check("determinant_one_normalization", A * H / (H / A) - A**2)
check("founded_radial_normalization", A * (A * v**2) / v**2 - A**2)
check("metric_unit_differs_from_founded", (A**2) / A - A)

# Exact A-anchored endpoint witness: f_A=1, f_B=4.
check("anchored_witness_transition", (Rn / Rm).subs({fp: 1, fq: 4}) - sp.Rational(1, 16))
check("positive_regular_recalibration", (f * m) ** 2 - f**2 * m**2)

if not all(ok for _, ok in checks):
    raise SystemExit([name for name, ok in checks if not ok])

atlas = [
    ("G175-W01", "n=fm", "K_n/K_m", "1/f^2", "exact recalibration"),
    ("G175-W02", "f_p=f_q=c", "R_n/R_m", "1", "constant unit class"),
    ("G175-W03", "f_A=1,f_B=4", "R_n/R_m", "1/16", "A-anchored nonselection"),
    ("G175-W04", "m^2=H", "K", "A", "pointwise metric unit"),
    ("G175-W05", "m^2=H/A", "K", "A^2", "determinant-one candidate"),
    ("G175-W06", "H=A v^2,m^2=v^2", "K", "A^2", "founded radial recovery"),
]
with (HERE / "CALIBRATION_EQUIVALENCE_ATLAS.tsv").open("w", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(("id", "condition", "quantity", "exact_value", "classification"))
    writer.writerows(atlas)

result = {
    "landing": landing,
    "checks_total": len(checks),
    "checks_passed": sum(ok for _, ok in checks),
    "checks": {name: ok for name, ok in checks},
    "atlas_rows": len(atlas),
}
(HERE / "DERIVATION_RESULT.json").write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps(result, sort_keys=True))

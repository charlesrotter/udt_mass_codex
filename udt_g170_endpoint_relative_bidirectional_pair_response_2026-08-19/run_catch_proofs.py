#!/usr/bin/env python3
"""Mutation catches for the G170 endpoint-relative theorem."""

from __future__ import annotations

from fractions import Fraction as F
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
catches: list[dict[str, object]] = []


def catch(name: str, detected: bool, detail: object) -> None:
    catches.append({"name": name, "caught": bool(detected), "detail": str(detail)})
    if not detected:
        raise AssertionError(f"mutation escaped: {name}: {detail}")


def metric(T: F, L: F, beta: F) -> tuple[tuple[F, F], tuple[F, F]]:
    return ((-T * T, -T * T * beta), (-T * T * beta, L * L - T * T * beta * beta))


def det(h: tuple[tuple[F, F], tuple[F, F]]) -> F:
    return h[0][0] * h[1][1] - h[0][1] * h[1][0]


def q2(h: tuple[tuple[F, F], tuple[F, F]]) -> F:
    return h[0][0] * h[0][0] / (-det(h))


T_A, L_A, beta_A = F(2), F(3), F(1, 2)
T_B, L_B, beta_B = F(3), F(5), F(-1, 3)
h_A = metric(T_A, L_A, beta_A)
h_B = metric(T_B, L_B, beta_B)
exp2_AB = (L_B / T_B) / (L_A / T_A)
exp2_BA = 1 / exp2_AB

# 1. The old G169 category error: a nonzero endpoint density is not the arrow depth.
surface_endpoint_exp2 = F(2)
surface_relative_exp2 = surface_endpoint_exp2 / surface_endpoint_exp2
catch("single_endpoint_as_arrow_depth", surface_endpoint_exp2 != surface_relative_exp2, surface_relative_exp2)

# 2. Wrong endpoint order changes the directed response.
wrong_order = (L_A / T_A) / (L_B / T_B)
catch("wrong_endpoint_order", wrong_order != exp2_AB, (wrong_order, exp2_AB))

# 3. Copying the forward response instead of swapping endpoints breaks reversal.
catch("same_sign_reverse", exp2_AB * exp2_AB != 1, exp2_AB * exp2_AB)

# 4. Reading the diagonal spatial entry ignores the live shift.
naive_q2_A = (-h_A[0][0]) / h_A[1][1]
catch("diagonal_readout_freezes_shift", naive_q2_A != q2(h_A), (naive_q2_A, q2(h_A)))

# 5. The G167 angular Gram cannot be discarded.
h_full = ((F(-391, 100), F(9, 50)), (F(9, 50), F(2)))
h_base = ((F(-4), F(0)), (F(0), F(1)))
catch("base_only_freezes_angular_gram", q2(h_full) != q2(h_base), (q2(h_full), q2(h_base)))

# 6. A trace correction bolted onto the base readout is not the full determinant readout.
angular_trace = F(109, 100)
post_readout = q2(h_base) + angular_trace
catch("post_readout_angular_correction", post_readout != q2(h_full), (post_readout, q2(h_full)))

# 7. A common scale must cancel; a volume-like substitute does not.
omega = F(7, 3)
scaled_h_A = tuple(tuple(omega * omega * value for value in row) for row in h_A)
bad_volume_readout = -det(scaled_h_A)
catch("common_scale_contamination", bad_volume_readout != -det(h_A), (bad_volume_readout, -det(h_A)))
catch("correct_common_scale_control", q2(scaled_h_A) == q2(h_A), q2(scaled_h_A))

# 8. Matched middle state telescopes; two independent B calibrations do not.
R_A, R_B, R_C = F(3, 2), F(5, 3), F(7, 4)
matched = (R_B / R_A) * (R_C / R_B)
catch("broken_matched_telescoping", matched == R_C / R_A, matched)
R_B_left, R_B_right = F(5, 3), F(11, 6)
unmatched = (R_B_left / R_A) * (R_C / R_B_right)
catch("unmatched_middle_forced_closed", unmatched != R_C / R_A, (unmatched, R_C / R_A))

# 9. Absolute value cannot carry directed reversal.
signed_marker = F(2, 5)
catch("absolute_depth_erases_orientation", abs(signed_marker) == abs(-signed_marker) and signed_marker != -signed_marker, signed_marker)

# 10. Independent reciprocal recalibration is not a shared-origin gauge shift.
endpoint_A, endpoint_B = F(2), F(5)
shift_A, shift_B = F(1, 3), F(2, 3)
original_difference = endpoint_B - endpoint_A
independently_recalibrated = (endpoint_B + shift_B) - (endpoint_A + shift_A)
catch(
    "independent_recalibration_called_gauge",
    independently_recalibrated != original_difference,
    independently_recalibrated - original_difference,
)

# 11. The actual reverse uses the same endpoint data and is exact.
catch("correct_reversal_control", exp2_AB * exp2_BA == 1, exp2_AB * exp2_BA)

result = {
    "status": "PASS",
    "catches_passed": sum(int(row["caught"]) for row in catches),
    "catches_total": len(catches),
    "catches": catches,
    "no_site": bool(sys.flags.no_site),
}
(HERE / "CATCH_PROOF_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": result["status"], "passed": result["catches_passed"], "total": len(catches)}, sort_keys=True))

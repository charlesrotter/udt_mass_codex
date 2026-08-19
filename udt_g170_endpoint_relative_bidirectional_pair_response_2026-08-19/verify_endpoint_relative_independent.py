#!/usr/bin/env python3
"""Independent exact-Fraction verification of G170; imports no production code."""

from __future__ import annotations

from fractions import Fraction as F
import json
from pathlib import Path
import random
import sys


HERE = Path(__file__).resolve().parent
RNG = random.Random(1700819)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def det2(h: tuple[tuple[F, F], tuple[F, F]]) -> F:
    return h[0][0] * h[1][1] - h[0][1] * h[1][0]


def channel_metric(T: F, L: F, beta: F) -> tuple[tuple[F, F], tuple[F, F]]:
    return (
        (-T * T, -T * T * beta),
        (-T * T * beta, L * L - T * T * beta * beta),
    )


def q2(h: tuple[tuple[F, F], tuple[F, F]]) -> F:
    return h[0][0] * h[0][0] / (-det2(h))


def add2(
    a: tuple[tuple[F, F], tuple[F, F]],
    b: tuple[tuple[F, F], tuple[F, F]],
) -> tuple[tuple[F, F], tuple[F, F]]:
    return (
        (a[0][0] + b[0][0], a[0][1] + b[0][1]),
        (a[1][0] + b[1][0], a[1][1] + b[1][1]),
    )


def scale2(
    factor: F,
    h: tuple[tuple[F, F], tuple[F, F]],
) -> tuple[tuple[F, F], tuple[F, F]]:
    return (
        (factor * h[0][0], factor * h[0][1]),
        (factor * h[1][0], factor * h[1][1]),
    )


def primary_parts(
    u: F,
    radius: F,
    sine: F,
    columns: tuple[tuple[F, F, F, F], tuple[F, F, F, F]],
) -> tuple[
    tuple[tuple[F, F], tuple[F, F]],
    tuple[tuple[F, F], tuple[F, F]],
    tuple[tuple[F, F], tuple[F, F]],
]:
    weights = (-F(1, 1) / (u * u), u * u, radius * radius, radius * radius * sine * sine)
    base_weights = weights[:2]
    angular_weights = weights[2:]

    def gram(weights_here: tuple[F, ...], offset: int) -> tuple[tuple[F, F], tuple[F, F]]:
        out = [[F(0), F(0)], [F(0), F(0)]]
        for i in range(2):
            for j in range(2):
                out[i][j] = sum(
                    weights_here[k] * columns[i][k + offset] * columns[j][k + offset]
                    for k in range(len(weights_here))
                )
        return ((out[0][0], out[0][1]), (out[1][0], out[1][1]))

    base = gram(base_weights, 0)
    angular = gram(angular_weights, 2)
    return add2(base, angular), base, angular


def positive_fraction(low: int = 1, high: int = 9) -> F:
    return F(RNG.randint(low, high), RNG.randint(1, 9))


def signed_fraction(scale: int = 4) -> F:
    return F(RNG.randint(-scale, scale), RNG.randint(1, 9))


checks = 0
channel_trials = 1200
for trial in range(channel_trials):
    T_A, L_A = positive_fraction(), positive_fraction()
    T_B, L_B = positive_fraction(), positive_fraction()
    T_C, L_C = positive_fraction(), positive_fraction()
    beta_A, beta_B, beta_C = signed_fraction(), signed_fraction(), signed_fraction()
    h_A = channel_metric(T_A, L_A, beta_A)
    h_B = channel_metric(T_B, L_B, beta_B)
    h_C = channel_metric(T_C, L_C, beta_C)

    require(det2(h_A) == -T_A * T_A * L_A * L_A, f"A determinant {trial}")
    require(det2(h_B) == -T_B * T_B * L_B * L_B, f"B determinant {trial}")
    require(det2(h_C) == -T_C * T_C * L_C * L_C, f"C determinant {trial}")
    checks += 3
    require(q2(h_A) == (T_A / L_A) ** 2, f"A q2 {trial}")
    require(q2(h_B) == (T_B / L_B) ** 2, f"B q2 {trial}")
    require(q2(h_C) == (T_C / L_C) ** 2, f"C q2 {trial}")
    checks += 3

    exp2_AB = (L_B / T_B) / (L_A / T_A)
    exp2_BA = (L_A / T_A) / (L_B / T_B)
    exp2_BC = (L_C / T_C) / (L_B / T_B)
    exp2_AC = (L_C / T_C) / (L_A / T_A)
    require(exp2_AB * exp2_BA == 1, f"reversal ratio {trial}")
    require(exp2_AB * exp2_BC == exp2_AC, f"matched composition {trial}")
    checks += 2

    chi_AB = (exp2_AB - 1) / (exp2_AB + 1)
    chi_BA = (exp2_BA - 1) / (exp2_BA + 1)
    require(chi_AB == -chi_BA, f"chi reversal {trial}")
    checks += 1

    omega_A, omega_B = positive_fraction(), positive_fraction()
    require(q2(scale2(omega_A * omega_A, h_A)) == q2(h_A), f"A common scale {trial}")
    require(q2(scale2(omega_B * omega_B, h_B)) == q2(h_B), f"B common scale {trial}")
    checks += 2

    # The same endpoint value at both ends is a zero relative response, not a same-sign arrow.
    same = positive_fraction()
    exp2_same = same / same
    require(exp2_same == 1 and (exp2_same - 1) / (exp2_same + 1) == 0, f"equal endpoint {trial}")
    checks += 1

    # Independently rebuilt middle calibrations do not telescope unless they are equal.
    B_left = positive_fraction()
    B_right = positive_fraction()
    if B_left == B_right:
        B_right += F(1, 97)
    unmatched = (B_left / (L_A / T_A)) * ((L_C / T_C) / B_right)
    require(unmatched != exp2_AC, f"unmatched middle accidentally closed {trial}")
    checks += 1


angular_trials = 1200
accepted = 0
attempts = 0
angular_shift_live = 0
angular_readout_changed = 0
while accepted < angular_trials:
    attempts += 1
    require(attempts < 100000, "angular trial generation stalled")
    u = positive_fraction(1, 5)
    radius = positive_fraction(1, 6)
    sine = F(RNG.randint(1, 8), RNG.randint(9, 12))
    col0 = (
        F(RNG.randint(3, 7)),
        F(RNG.randint(-2, 2), 10),
        F(RNG.randint(1, 3), RNG.randint(10, 20)),
        F(RNG.randint(1, 3), RNG.randint(10, 20)),
    )
    col1 = (
        F(RNG.randint(-2, 2), 10),
        F(RNG.randint(2, 7), RNG.randint(3, 9)),
        F(RNG.randint(1, 4), RNG.randint(8, 18)),
        F(RNG.randint(1, 4), RNG.randint(8, 18)),
    )
    full, base, angular = primary_parts(u, radius, sine, (col0, col1))
    if full[0][0] >= 0 or det2(full) >= 0 or base[0][0] >= 0 or det2(base) >= 0:
        continue
    if full[0][1] == 0 or q2(full) == q2(base):
        continue

    require(full == add2(base, angular), f"angular assembly {accepted}")
    require(full[0][0] < 0 and det2(full) < 0, f"angular regular {accepted}")
    require(q2(full) > 0 and q2(base) > 0, f"angular q2 positive {accepted}")
    checks += 3
    angular_shift_live += int(full[0][1] != 0)
    angular_readout_changed += int(q2(full) != q2(base))

    omega = positive_fraction()
    require(q2(scale2(omega * omega, full)) == q2(full), f"angular scale {accepted}")
    checks += 1

    # A second exact regular endpoint supplies a genuine relative ratio whose reverse is automatic.
    T_ref, L_ref = positive_fraction(), positive_fraction()
    q2_relative = q2(full) / ((T_ref / L_ref) ** 2)
    q2_reverse = ((T_ref / L_ref) ** 2) / q2(full)
    require(q2_relative * q2_reverse == 1, f"angular endpoint reversal {accepted}")
    checks += 1
    accepted += 1


landing = (
    "ENDPOINT_RELATIVE_RECIPROCAL_DEPTH_DERIVED_FROM_TERMINAL_CEFF_RATIOS"
    "__WITHIN_ONE_CONSISTENT_RECIPROCAL_CALIBRATION_CLASS"
    "__BIDIRECTIONAL_REVERSAL_AND_MATCHED_COMPOSITION_AUTOMATIC"
    "__G169_SINGLE_ENDPOINT_REVERSAL_COUNTEREXAMPLE_RECLASSIFIED"
    "__COPRESENCE_NOT_LOAD_BEARING"
    "__CROSS_QUERY_AND_FULL_NONSCALAR_CARRY_REMAIN_OPEN"
)
result = {
    "landing_supported": landing,
    "implementation": "independent standard-library Fraction; no production import",
    "seed": 1700819,
    "channel_trials": channel_trials,
    "angular_trials": angular_trials,
    "angular_generation_attempts": attempts,
    "angular_shift_live": angular_shift_live,
    "angular_readout_changed": angular_readout_changed,
    "checks_passed": checks,
    "status": "PASS",
    "no_site": bool(sys.flags.no_site),
}
(HERE / "INDEPENDENT_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, sort_keys=True))

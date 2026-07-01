"""Warn against overfitting residuals with native-looking small quantities.

Small residuals can often be matched by combining a few plausible-looking
native quantities. This script searches low-order signed combinations to show
that numerical closeness alone is weak evidence.
"""

from __future__ import annotations

import itertools
import math

from native_angular_ms_subtraction import finite_part


ETA = 1.0 / 18.0
GAMMA = 3.0 * math.exp(-ETA / 2.0)
ELECTRON_MEV = 0.51099895
E1_RATIO = 2.10394 / 1.1343262
TARGET_MU = 105.6583755
TARGET_TAU = 1776.86


def residuals() -> dict[str, float]:
    pred_mu = ELECTRON_MEV * GAMMA**5
    pred_tau = ELECTRON_MEV * E1_RATIO * GAMMA**7
    return {
        "mu": math.log(TARGET_MU / pred_mu),
        "tau": math.log(TARGET_TAU / pred_tau),
    }


def candidate_terms() -> list[tuple[str, float]]:
    det_ordinary_m1 = finite_part("ordinary-mono1", 10000, 1.0)
    det_m2_m1 = finite_part("mono2-mono1", 10000, 1.0)
    return [
        ("eta/2", ETA / 2.0),
        ("eta/3", ETA / 3.0),
        ("eta/4", ETA / 4.0),
        ("eta^2", ETA * ETA),
        ("E1_core", 0.0167668973),
        ("E1_shell", 0.0009437632),
        ("M1_core", 0.0001659681),
        ("M1_shell", 0.0001465535),
        ("eta*MS_ordinary_M1", ETA * det_ordinary_m1),
        ("eta*MS_M2_M1", ETA * det_m2_m1),
    ]


def signed_combos(terms: list[tuple[str, float]], max_terms: int = 3):
    for count in range(1, max_terms + 1):
        for combo in itertools.combinations(terms, count):
            for signs in itertools.product([-1.0, 1.0], repeat=count):
                label = " ".join(
                    f"{'+' if sign > 0 else '-'}{name}" for sign, (name, _value) in zip(signs, combo)
                )
                value = sum(sign * value for sign, (_name, value) in zip(signs, combo))
                yield label, value


def main() -> None:
    res = residuals()
    terms = candidate_terms()
    print("Residual combo warning")
    print("Searches signed combinations of up to 3 native-looking small quantities.")
    print()
    for branch, target in res.items():
        rows = []
        for label, value in signed_combos(terms, 3):
            rows.append((abs(value - target), label, value))
        print(f"{branch} residual target={target:+.10f}")
        for error, label, value in sorted(rows)[:8]:
            print(f"  value={value:+.10f} error={error:.3g} combo={label}")
        print()
    print("verdict:")
    print("  many small combinations can imitate the residuals")
    print("  residual matching is not evidence without an independent derivation")


if __name__ == "__main__":
    main()

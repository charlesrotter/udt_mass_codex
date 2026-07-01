"""Residual budget for the current mass-ladder candidate.

After the combined native candidate, the remaining errors are small:

    mu-like:  predicted high by about 2.28%
    tau-like: predicted low by about 3.96%

This script expresses those residuals as logarithmic correction budgets and
compares them with native small quantities already present in the rebuild.
The goal is not to fit them, but to prevent accidental tuning.
"""

from __future__ import annotations

import math

from native_angular_ms_subtraction import finite_part


N = 3
ETA = 1.0 / 18.0
GAMMA = N * math.exp(-ETA / 2.0)
ELECTRON_MEV = 0.51099895
E1_RATIO = 2.10394 / 1.1343262
TARGET_MU = 105.6583755
TARGET_TAU = 1776.86


def main() -> None:
    pred_mu = ELECTRON_MEV * GAMMA**5
    pred_tau = ELECTRON_MEV * E1_RATIO * GAMMA**7
    log_mu = math.log(TARGET_MU / pred_mu)
    log_tau = math.log(TARGET_TAU / pred_tau)

    print("Residual budget audit")
    print(f"eta={ETA:.12g}")
    print(f"gamma={GAMMA:.12g}")
    print()
    print("current residual log corrections needed")
    print(f"  mu-like:  log(target/pred)={log_mu:+.10f} = {log_mu / ETA:+.6f} eta")
    print(f"  tau-like: log(target/pred)={log_tau:+.10f} = {log_tau / ETA:+.6f} eta")
    print()

    det_ordinary_m1 = finite_part("ordinary-mono1", 10000, 1.0)
    det_m2_m1 = finite_part("mono2-mono1", 10000, 1.0)
    candidates = [
        ("eta/2", ETA / 2.0),
        ("eta/3", ETA / 3.0),
        ("eta^2", ETA * ETA),
        ("E1 core action", 0.0167668973),
        ("E1 shell pressure", 0.0009437632),
        ("M1 core action", 0.0001659681),
        ("M1 shell pressure", 0.0001465535),
        ("eta * MS(ordinary-M1)", ETA * det_ordinary_m1),
        ("-eta * MS(ordinary-M1)", -ETA * det_ordinary_m1),
        ("eta * MS(M2-M1)", ETA * det_m2_m1),
    ]
    print("native small quantities for scale comparison")
    for label, value in candidates:
        print(f"  {label:26s} {value:+.10f}")
    print()
    print("diagnostic:")
    print("  mu residual is about -0.406 eta")
    print("  tau residual is about +0.726 eta")
    print("  signs differ, so a single common correction cannot fix both")
    print("  residual closure probably needs branch-specific native effects or better derivation of gamma/depth")
    print()
    print("verdict:")
    print("  treat the residual as a multi-component audit target, not as a free fit parameter")


if __name__ == "__main__":
    main()

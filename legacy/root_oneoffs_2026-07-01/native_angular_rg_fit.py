"""Renormalized finite-part fits for angular determinant differences.

The raw angular determinant sums are cutoff dependent. This script asks whether
simple asymptotic subtractions leave a stable finite remainder.

For a determinant difference D(L), fit

    D(L) = divergent_terms(L) + finite_constant + residual

over large cutoffs. If the finite_constant is stable under fit window and basis,
there may be a meaningful angular boundary/RG datum. If not, the determinant
needs a UDT-native renormalization prescription before it can be used.
"""

from __future__ import annotations

import argparse
import math

import numpy as np


def logdet_monopole(n: int, cutoff: int, mu2: float) -> float:
    spin = abs(n) / 2.0
    total = 0.0
    for k in range(cutoff + 1):
        j = spin + k
        lam = j * (j + 1.0) - spin * spin
        deg = int(round(2.0 * j + 1.0))
        total += deg * math.log(lam + mu2)
    return total


def logdet_ordinary(cutoff: int, mu2: float) -> float:
    total = 0.0
    for ell in range(cutoff + 1):
        lam = ell * (ell + 1.0)
        deg = 2 * ell + 1
        total += deg * math.log(lam + mu2)
    return total


def basis_matrix(cutoffs: np.ndarray, basis_name: str) -> np.ndarray:
    L = cutoffs.astype(float)
    logL = np.log(L)
    columns = []
    if basis_name == "minimal":
        columns = [L * logL, L, logL, np.ones_like(L)]
    elif basis_name == "extended":
        columns = [L * logL, L, logL, np.ones_like(L), 1.0 / L]
    elif basis_name == "polylog":
        columns = [
            L * L * logL,
            L * L,
            L * logL,
            L,
            logL,
            np.ones_like(L),
            1.0 / L,
        ]
    else:
        raise ValueError(f"unknown basis {basis_name}")
    return np.vstack(columns).T


def fit_constant(cutoffs: np.ndarray, values: np.ndarray, basis_name: str):
    A = basis_matrix(cutoffs, basis_name)
    coeffs, *_ = np.linalg.lstsq(A, values, rcond=None)
    fitted = A @ coeffs
    residual = values - fitted
    constant = coeffs[-2] if basis_name in {"extended", "polylog"} else coeffs[-1]
    rms = float(np.sqrt(np.mean(residual * residual)))
    return constant, rms, coeffs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mu2", type=float, default=1.0)
    parser.add_argument("--max-cutoff", type=int, default=2000)
    parser.add_argument("--step", type=int, default=20)
    args = parser.parse_args()

    cutoffs = np.arange(args.step, args.max_cutoff + 1, args.step)
    mono1 = np.array([logdet_monopole(1, int(L), args.mu2) for L in cutoffs])
    mono2 = np.array([logdet_monopole(2, int(L), args.mu2) for L in cutoffs])
    ordinary = np.array([logdet_ordinary(int(L), args.mu2) for L in cutoffs])

    diffs = {
        "mono2-mono1": mono2 - mono1,
        "ordinary-mono1": ordinary - mono1,
    }

    print("Angular determinant finite-part fit")
    print(f"mu2={args.mu2:g} max_cutoff={args.max_cutoff} step={args.step}")
    print("finite constants are basis/window diagnostics, not predictions")
    print()

    windows = [
        (0.25, 1.0),
        (0.50, 1.0),
        (0.75, 1.0),
    ]
    for name, values in diffs.items():
        print(name)
        for basis in ["minimal", "extended", "polylog"]:
            for lo_frac, hi_frac in windows:
                lo = int(args.max_cutoff * lo_frac)
                hi = int(args.max_cutoff * hi_frac)
                mask = (cutoffs >= lo) & (cutoffs <= hi)
                constant, rms, _coeffs = fit_constant(cutoffs[mask], values[mask], basis)
                print(
                    f"  basis={basis:8s} window={lo:5d}-{hi:5d} "
                    f"const={constant:14.8g} rms={rms:12.4g}"
                )
        print()

    print("verdict:")
    print("  if constants vary strongly across basis/window, angular determinant")
    print("  finite parts are scheme dependent and need a native subtraction rule")


if __name__ == "__main__":
    main()


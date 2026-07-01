"""Basis-label transport model for the epsilon sector.

The epsilon volume form selects an oriented 3-basis up to SL(3)-like changes.
The current gamma, however, needs a trace over three transported basis labels:

    gamma = exp(-eta/2) sum_i <e_i^outer | e_i^core>.

This is a stronger condition than preserving the volume form. It requires an
orthonormal/metric structure on the boundary angular space that makes basis
labels meaningful.
"""

from __future__ import annotations

import math

import numpy as np


N = 3
ETA = 1.0 / 18.0
PENALTY = math.exp(-ETA / 2.0)


def gram_trace(overlap: np.ndarray) -> float:
    return float(np.trace(overlap))


def normalized_trace(overlap: np.ndarray) -> float:
    # Polar/SVD style normalization: compare only orientation after removing
    # singular values. This is diagnostic, not a full polar decomposition.
    _u, singular, _vh = np.linalg.svd(overlap)
    return float(sum(1.0 for _ in singular))


def main() -> None:
    cases = [
        ("identity orthonormal frame", np.eye(N)),
        ("permuted frame", np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]], dtype=float)),
        ("rotated frame pi/3", np.array([[0.5, -math.sqrt(3) / 2, 0], [math.sqrt(3) / 2, 0.5, 0], [0, 0, 1]], dtype=float)),
        ("non-orthonormal volume preserving", np.diag([2.0, 0.5, 1.0])),
    ]

    print("Epsilon basis-label transport audit")
    print(f"penalty=exp(-eta/2)={PENALTY:.12g}")
    print()
    for label, overlap in cases:
        det = float(np.linalg.det(overlap))
        tr = gram_trace(overlap)
        print(label)
        print(f"  det={det:.12g}")
        print(f"  trace_overlap={tr:.12g}")
        print(f"  gamma_trace={PENALTY * tr:.12g}")
        print()
    print("verdict:")
    print("  gamma=N exp(-eta/2) requires identity overlap of transported basis labels")
    print("  epsilon volume preservation alone does not fix this overlap")
    print("  a boundary metric/orthonormal frame rule is required")


if __name__ == "__main__":
    main()

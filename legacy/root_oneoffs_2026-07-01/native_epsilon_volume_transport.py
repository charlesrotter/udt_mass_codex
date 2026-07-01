"""Epsilon volume-form transport audit.

For a 3-dimensional angular boundary space V, the epsilon object is the volume
form in Lambda^3 V. A boundary frame map A: V_core -> V_outer transports the
volume form by det(A).

This script separates two notions:

    vector transfer trace:  tr(A)
    volume-form transfer:  det(A)

The current mass-ladder gamma uses vector-space trace N, while epsilon
singlet preservation naturally speaks about det(A)=1. This is a possible
category mismatch unless the transported labels are basis orientations, not
only the single volume form.
"""

from __future__ import annotations

import math

import numpy as np


N = 3
ETA = 1.0 / 18.0
PENALTY = math.exp(-ETA / 2.0)


def rotation_z(theta: float) -> np.ndarray:
    return np.array(
        [
            [math.cos(theta), -math.sin(theta), 0.0],
            [math.sin(theta), math.cos(theta), 0.0],
            [0.0, 0.0, 1.0],
        ]
    )


def scale_diag(values: tuple[float, float, float]) -> np.ndarray:
    return np.diag(values)


def main() -> None:
    cases = [
        ("identity", np.eye(3)),
        ("rotation theta=eta", rotation_z(ETA)),
        ("rotation theta=pi/3", rotation_z(math.pi / 3.0)),
        ("volume-preserving anisotropic", scale_diag((2.0, 0.5, 1.0))),
        ("uniform scale 0.9", scale_diag((0.9, 0.9, 0.9))),
        ("orientation reversal", scale_diag((-1.0, 1.0, 1.0))),
    ]

    print("Epsilon volume-form transport audit")
    print(f"penalty=exp(-eta/2)={PENALTY:.12g}")
    print()
    for label, matrix in cases:
        tr = float(np.trace(matrix))
        det = float(np.linalg.det(matrix))
        gamma_trace = PENALTY * tr
        gamma_det = PENALTY * det
        print(label)
        print(f"  tr(A)={tr:.12g}")
        print(f"  det(A)={det:.12g}")
        print(f"  penalty*tr(A)={gamma_trace:.12g}")
        print(f"  penalty*det(A)={gamma_det:.12g}")
        print()
    print("verdict:")
    print("  epsilon volume-form preservation gives det(A)=1, not tr(A)=N")
    print("  current gamma needs transported basis labels or diagonal vector transfer")
    print("  volume-form transport alone is insufficient")


if __name__ == "__main__":
    main()

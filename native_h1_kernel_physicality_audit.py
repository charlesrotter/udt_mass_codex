import math
import random

import numpy as np


def random_rotation(seed: int = 7) -> np.ndarray:
    rng = random.Random(seed)
    a = np.array([[rng.uniform(-1.0, 1.0) for _ in range(3)] for _ in range(3)])
    q, r = np.linalg.qr(a)
    if np.linalg.det(q) < 0:
        q[:, 0] *= -1.0
    return q


def main() -> None:
    eta = 1.0 / 18.0
    h1_kernel = eta * np.eye(3)
    rotation = random_rotation()
    rotated_kernel = rotation.T @ h1_kernel @ rotation

    print("H1 kernel physicality audit")
    print("=" * 29)
    print("Boundary H1 data can be represented as a vector q_a in the ell=1 space.")
    print("The isotropic metric projection gives the quadratic kernel:")
    print("  S = eta q_a q_a")
    print("  K_ab = eta delta_ab")
    print()
    print("Under a global S2 rotation R:")
    print("  q -> R q")
    print("  K -> R^T K R")
    print("For K=eta I, the kernel is unchanged up to basis conjugation.")
    print()
    print("Kernel invariants:")
    print(f"  trace(K)={np.trace(h1_kernel):.12g}")
    print(f"  trace(R^T K R)={np.trace(rotated_kernel):.12g}")
    print(f"  determinant(K)={np.linalg.det(h1_kernel):.12g}")
    print(f"  determinant(R^T K R)={np.linalg.det(rotated_kernel):.12g}")
    print(f"  transfer trace Tr exp(-K/2)={3.0 * math.exp(-eta / 2.0):.12g}")
    print()
    print("Interpretation:")
    print("  - Rotation changes the H1 basis but preserves the three-dimensional rank.")
    print("  - The rank is removed only if a singlet-only constraint projects out H1.")
    print("  - Ordinary rotational symmetry gives degeneracy; it is not automatically")
    print("    a gauge redundancy to divide out.")
    print()
    print("Audit verdict:")
    print("  Treating the H1 rank as physical is consistent if non-scalar boundary")
    print("  shapes are allowed as sector data.")
    print("  The ladder fails if elementary closure requires S2-rotation singlets at")
    print("  each boundary constraint.")


if __name__ == "__main__":
    main()

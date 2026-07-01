import math
import random

import numpy as np


def orthonormal_relative_basis() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    common = np.array([1.0, 1.0, 1.0])
    common = common / np.linalg.norm(common)
    e1 = np.array([1.0, -1.0, 0.0])
    e1 = e1 / np.linalg.norm(e1)
    e2 = np.cross(common, e1)
    e2 = e2 / np.linalg.norm(e2)
    return common, e1, e2


def random_unit_2d(rng: random.Random) -> tuple[float, float]:
    angle = rng.random() * 2.0 * math.pi
    return math.cos(angle), math.sin(angle)


def main() -> None:
    common, e1, e2 = orthonormal_relative_basis()
    gram = np.array(
        [
            [float(np.dot(common, common)), float(np.dot(common, e1)), float(np.dot(common, e2))],
            [float(np.dot(e1, common)), float(np.dot(e1, e1)), float(np.dot(e1, e2))],
            [float(np.dot(e2, common)), float(np.dot(e2, e1)), float(np.dot(e2, e2))],
        ]
    )

    rng = random.Random(11)
    moment = np.zeros((2, 2))
    samples = 200000
    for _ in range(samples):
        x, y = random_unit_2d(rng)
        v = x * e1 + y * e2
        coords = np.array([float(np.dot(v, e1)), float(np.dot(v, e2))])
        moment += np.outer(coords, coords)
    moment /= samples

    print("E1 relative-shape measure audit")
    print("=" * 35)
    print("For an ordinary three-component H1 branch, remove the common")
    print("amplitude direction (1,1,1)/sqrt(3).")
    print("The relative-shape space is the two-dimensional orthogonal plane.")
    print()
    print("Basis Gram matrix [common, rel1, rel2]:")
    for row in gram:
        print("  " + " ".join(f"{value: .12f}" for value in row))
    print()
    print("Uniform relative-angle second moment in the relative plane:")
    for row in moment:
        print("  " + " ".join(f"{value: .12f}" for value in row))
    print()
    print("Analytic expectation:")
    print("  <u_i u_j>_relative_circle = delta_ij / 2")
    print()
    print("Measure verdict:")
    print("  - E1 relative shape after removing common amplitude is a clean")
    print("    two-dimensional isotropic plane.")
    print("  - Its bare shape measure is isotropic in that plane.")
    print("  - This supports the two E1 shape nodes per boundary but does not")
    print("    by itself supply branch-specific residual corrections.")
    print("  - Any E1-specific correction must come from boundary action weighting,")
    print("    nonlinear q-flow, determinant factors, or coefficient normalization.")


if __name__ == "__main__":
    main()

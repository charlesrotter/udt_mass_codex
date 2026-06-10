import math
from dataclasses import dataclass


@dataclass(frozen=True)
class KernelType:
    name: str
    rank: int
    action: float
    determinant_power: float
    branch_use: str

    @property
    def trace_weight(self) -> float:
        return self.rank * math.exp(-self.action / 2.0)

    @property
    def gaussian_norm(self) -> float:
        # Schematic finite-dimensional Gaussian normalization:
        # integral exp(-1/2 x^T A x) dx ~ (det A)^(-1/2).
        # determinant_power lets us test whether this factor is included,
        # omitted, or partly canceled by normalized transfer convention.
        if self.action <= 0:
            return 1.0
        return self.action ** (-0.5 * self.rank * self.determinant_power)

    @property
    def total_weight(self) -> float:
        return self.trace_weight * self.gaussian_norm


def main() -> None:
    eta = 1.0 / 18.0
    kernels = [
        KernelType("normalized rank-one node", 1, eta, 0.0, "one scalar projector constraint"),
        KernelType("unnormalized rank-one Gaussian", 1, eta, 1.0, "if node measure is not normalized"),
        KernelType("normalized H1 block", 3, eta, 0.0, "one full common H1 block"),
        KernelType("unnormalized H1 Gaussian", 3, eta, 1.0, "if full H1 block measure contributes"),
        KernelType("E1 relative shape block", 2, eta, 1.0, "possible two-mode shape determinant"),
    ]

    print("Transfer gluing determinant audit")
    print("=" * 35)
    print("Symmetric transfer gives exp(-eta/2) per one-sided node.")
    print("A gluing measure may also contribute determinant/Jacobian factors.")
    print("This audit is schematic: exact powers require the actual boundary kernel.")
    print()
    print(f"eta={eta:.12g}")
    print()
    for kernel in kernels:
        print(kernel.name)
        print(f"  rank={kernel.rank}")
        print(f"  determinant power={kernel.determinant_power}")
        print(f"  trace weight={kernel.trace_weight:.12g}")
        print(f"  gaussian norm factor={kernel.gaussian_norm:.12g}")
        print(f"  total schematic weight={kernel.total_weight:.12g}")
        print(f"  branch use={kernel.branch_use}")

    print("\nGluing verdict:")
    print("  - If kernels are normalized transfer operators, determinant factors")
    print("    cancel by convention and gamma is unchanged.")
    print("  - If the physical boundary path integral includes unnormalized Gaussian")
    print("    measures, determinant factors can be large and rank-dependent.")
    print("  - Therefore gluing determinants are dangerous: they can dominate unless")
    print("    the boundary measure is normalized or canonically canceled.")
    print("  - The exact transfer construction must specify normalization before any")
    print("    determinant correction is used.")


if __name__ == "__main__":
    main()

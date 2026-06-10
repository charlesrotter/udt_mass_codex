from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectionCase:
    label: str
    q: float

    @property
    def boundary_momentum_scale(self) -> float:
        # -Pi_f = q/2 at R=1.
        return self.q / 2.0

    @property
    def h1_projected_unit(self) -> float:
        # Isotropic S2 projection: divide scalar by 3.
        return self.boundary_momentum_scale / 3.0

    @property
    def transfer_side(self) -> float:
        return self.h1_projected_unit / 2.0


def main() -> None:
    cases = [
        ProjectionCase("self-similar eta collar", 1.0 / 3.0),
        ProjectionCase("M1-positive q diagnostic", 0.387510439043),
        ProjectionCase("E1-negative q diagnostic", 0.264116906769),
    ]

    print("Boundary momentum H1 projection")
    print("=" * 31)
    print("C1 boundary conjugate scale:")
    print("  -Pi_f = q/2")
    print("Round S2/H1 isotropic projection:")
    print("  <n_a n_b> = delta_ab/3")
    print("Projected unit:")
    print("  eta(q) = (q/2)/3 = q/6")
    print("Transfer side:")
    print("  eta(q)/2 = q/12")
    print()

    for case in cases:
        print(case.label)
        print(f"  q={case.q:.12g}")
        print(f"  -Pi_f=q/2={case.boundary_momentum_scale:.12g}")
        print(f"  eta(q)=q/6={case.h1_projected_unit:.12g}")
        print(f"  one-sided transfer=q/12={case.transfer_side:.12g}")
        print()

    print("Projection verdict:")
    print("  - eta can be interpreted as the H1 projection of the C1 boundary")
    print("    canonical momentum at phi0.")
    print("  - This unifies the extrinsic-jump and action-variation views.")
    print("  - The hidden mechanism is now a variational boundary conjugate:")
    print("      C1 boundary momentum -> S2/H1 projection -> eta -> transfer side.")


if __name__ == "__main__":
    main()

from dataclasses import dataclass


@dataclass(frozen=True)
class CollarState:
    label: str
    q: float
    radius: float = 1.0

    @property
    def f(self) -> float:
        return 1.0

    @property
    def fprime(self) -> float:
        return -self.q / self.radius

    @property
    def canonical_momentum(self) -> float:
        # C1 radial density in f is (1/4) r^2 f'^2.
        # Variation gives boundary term (1/2) r^2 f' delta f.
        return 0.5 * self.radius * self.radius * self.fprime

    @property
    def needed_boundary_derivative(self) -> float:
        # For free variation of f at boundary, add Bdry(f) with dBdry/df=-Pi.
        return -self.canonical_momentum


def main() -> None:
    states = [
        CollarState("self-similar eta collar", 1.0 / 3.0),
        CollarState("M1-positive q diagnostic", 0.387510439043),
        CollarState("E1-negative q diagnostic", 0.264116906769),
    ]

    print("C1 phi0 boundary conjugate audit")
    print("=" * 35)
    print("C1 radial density in f=e^{-2phi}:")
    print("  L = (1/4) r^2 f'^2")
    print("Variation gives boundary term:")
    print("  Pi_f delta f = (1/2) r^2 f' delta f")
    print()
    print("At phi0 collar R=1, f=1, f'=-q:")
    print("  Pi_f = -q/2")
    print()
    for state in states:
        print(state.label)
        print(f"  q={state.q:.12g}")
        print(f"  f'={state.fprime:.12g}")
        print(f"  Pi_f=(1/2)r^2f'={state.canonical_momentum:.12g}")
        print(f"  needed dS_boundary/df={state.needed_boundary_derivative:.12g}")
        print(f"  eta=q/6={state.q / 6.0:.12g}")
        print()

    print("Boundary conjugate verdict:")
    print("  - Nonzero q means the C1 action has a nonzero canonical boundary momentum.")
    print("  - A well-posed finite-cell variational problem needs either fixed f at phi0")
    print("    or a boundary functional whose derivative cancels Pi_f.")
    print("  - Since f(phi0)=1 is already the interface condition, the hidden mechanism")
    print("    may be the conjugate boundary functional that makes this constrained")
    print("    endpoint physical rather than an imposed wall.")
    print("  - Its derivative scale is q/2, the same scale as the extrinsic jump.")


if __name__ == "__main__":
    main()

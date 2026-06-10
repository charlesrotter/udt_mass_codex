from dataclasses import dataclass


@dataclass(frozen=True)
class AngularSpace:
    ell: int

    @property
    def dimension(self) -> int:
        return 2 * self.ell + 1

    @property
    def has_unique_three_epsilon(self) -> bool:
        return self.dimension == 3


def main() -> None:
    print("Frame-count origin audit")
    print("=" * 24)
    print("Round S2 scalar harmonics have dimension:")
    print("  dim H_ell = 2 ell + 1")
    print()

    for ell in range(0, 5):
        space = AngularSpace(ell)
        print(f"ell={ell}")
        print(f"  dimension={space.dimension}")
        print(f"  unique 3-index epsilon available={space.has_unique_three_epsilon}")

    print("\nMetric-native facts:")
    print("  - ell=0 is the scalar/common mode.")
    print("  - ell=1 is the lowest non-scalar angular space.")
    print("  - dim H_1=3 on the round S2.")
    print("  - A three-dimensional oriented label space carries epsilon_abc.")
    print()
    print("Conditional universal-use step:")
    print("  - M1 compact/primitive branches and E1 ordinary branches both close")
    print("    through the same phi=0 scalar/interface frame.")
    print("  - If true, every surviving branch inherits N_frame=3.")
    print("  - If false, M1 and E1 could carry different frame counts and the")
    print("    current shared gamma/depth structure would not be universal.")
    print()
    print("Audit verdict:")
    print("  N_frame=3 is metric-native for the lowest non-scalar S2 space.")
    print("  Its universal use across surviving branches remains a boundary-closure")
    print("  condition, not a completed derivation.")


if __name__ == "__main__":
    main()

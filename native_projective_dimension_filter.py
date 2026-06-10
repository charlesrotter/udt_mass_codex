from dataclasses import dataclass


@dataclass(frozen=True)
class CompactSector:
    flux: int

    @property
    def degeneracy(self) -> int:
        return abs(self.flux) + 1

    @property
    def projective_real_dimension(self) -> int:
        # CP^(d-1) has real dimension 2(d-1).
        return 2 * (self.degeneracy - 1)

    @property
    def matches_s2(self) -> bool:
        return self.projective_real_dimension == 2

    @property
    def primitive_nonzero(self) -> bool:
        return abs(self.flux) == 1


def main() -> None:
    print("Projective dimension filter")
    print("=" * 27)
    print("For compact U(1) flux n, the lowest compact sector has degeneracy:")
    print("  d = |n| + 1")
    print("After quotienting common compact phase:")
    print("  projective space = CP^(d-1)")
    print("  real dimension = 2(d-1)")
    print("The common interface frame is S2, real dimension 2.")
    print()

    for flux in range(0, 6):
        sector = CompactSector(flux)
        if flux == 0:
            status = "trivial compact sector"
        elif sector.matches_s2 and sector.primitive_nonzero:
            status = "unique primitive compact sector matching S2"
        elif sector.matches_s2:
            status = "S2 match but check primitivity"
        else:
            status = "projective space larger than S2"
        print(f"n={flux}")
        print(f"  degeneracy d={sector.degeneracy}")
        print(f"  CP^(d-1) real dimension={sector.projective_real_dimension}")
        print(f"  matches S2 interface dimension={sector.matches_s2}")
        print(f"  status={status}")

    print("\nFilter verdict:")
    print("  - The primitive nonzero compact sector |n|=1 is uniquely CP1=S2.")
    print("  - This gives a topological reason M1 can meet the H1 interface frame.")
    print("  - Higher compact flux sectors do not map to the elementary S2 interface")
    print("    without extra projection data, so they are non-elementary in this frame.")


if __name__ == "__main__":
    main()

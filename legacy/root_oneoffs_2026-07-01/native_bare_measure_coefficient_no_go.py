from dataclasses import dataclass


@dataclass(frozen=True)
class MeasureFact:
    name: str
    exact_fact: str
    coefficient_consequence: str


FACTS = [
    MeasureFact(
        "CP1/Hopf M1 measure",
        "Fubini-Study measure on CP1 pushes forward to the round S2 measure",
        "no anisotropic M1 correction from bare projective geometry",
    ),
    MeasureFact(
        "H1/S2 second moment",
        "<n_a n_b>=delta_ab/3",
        "gives eta projection, not a branch coefficient",
    ),
    MeasureFact(
        "E1 relative plane",
        "after removing common amplitude, the relative-shape plane is isotropic",
        "no E1 coefficient boost from bare relative-angle measure",
    ),
    MeasureFact(
        "volume normalization",
        "total measure can be normalized to one on each branch space",
        "absolute volume ratios are not invariant unless the boundary measure specifies them",
    ),
]


def main() -> None:
    print("bare measure coefficient no-go")
    print("=" * 32)
    for fact in FACTS:
        print(fact.name)
        print(f"  exact fact:              {fact.exact_fact}")
        print(f"  coefficient consequence: {fact.coefficient_consequence}")
        print()

    print("No-go verdict:")
    print("  Bare geometry measures support isotropy and projection identities.")
    print("  They do not supply C_M1, C_M2, or C_E1 without a derived boundary")
    print("  action or measure density.")


if __name__ == "__main__":
    main()

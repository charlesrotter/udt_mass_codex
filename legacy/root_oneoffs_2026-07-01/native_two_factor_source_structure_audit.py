from dataclasses import dataclass
from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


@dataclass(frozen=True)
class Structure:
    name: str
    value: Fraction
    status: str
    condition: str


STRUCTURES = [
    Structure(
        name="same-axis fourth moment",
        value=Fraction(1, 5),
        status="rejected for s=1/9",
        condition="this is <n_i^4>, not <n_i^2>^2",
    ),
    Structure(
        name="single H1/S2 projection",
        value=Fraction(1, 3),
        status="rejected for s=1/9",
        condition="one projection gives s=1/3",
    ),
    Structure(
        name="independent input/output H1 projections",
        value=Fraction(1, 9),
        status="viable target",
        condition="requires two independently normalized edge projections",
    ),
    Structure(
        name="curvature-share times H1 projection",
        value=Fraction(1, 9),
        status="viable only after curvature-share closure",
        condition="requires q=1/3 from an independent closure, otherwise circular",
    ),
    Structure(
        name="rank-one normalized kernel trace",
        value=Fraction(1, 9),
        status="viable target",
        condition="requires an exact separable kernel with two trace-normalized H1 legs",
    ),
]


def main() -> None:
    print("two-factor source-structure audit")
    print("=" * 39)
    for structure in STRUCTURES:
        print(structure.name)
        print(f"  value:     {fmt(structure.value)}")
        print(f"  status:    {structure.status}")
        print(f"  condition: {structure.condition}")
        print()

    print("No-invention verdict:")
    print("  The strongest non-circular path is an exact edge kernel with two")
    print("  independently normalized H1/S2 projection legs. Without that kernel,")
    print("  s=1/9 remains the minimal phi0 postulate, not a derivation.")


if __name__ == "__main__":
    main()

from dataclasses import dataclass
from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


@dataclass(frozen=True)
class Ingredient:
    name: str
    status: str
    supplies: str
    does_not_supply: str


ETA = Fraction(1, 18)


INGREDIENTS = [
    Ingredient(
        "edge scalar eta",
        "available after banked P_phi0 plus H1/S2 projection",
        "eta=1/18",
        "an angular operator",
    ),
    Ingredient(
        "normalized ell=1 angular operator",
        "metric-derived",
        "L1=(-R^2 Delta_S2)/2=I3 on H1",
        "the coefficient eta",
    ),
    Ingredient(
        "trace-preserving scalar lift",
        "plausible but still a boundary-measure rule",
        "one scalar boundary budget distributed over the H1 identity",
        "the transfer/gluing interpretation",
    ),
    Ingredient(
        "full value action",
        "not derived",
        "would be S0_full=eta <a,L1 a>",
        "cannot be claimed from eta and L1 separately",
    ),
]


def main() -> None:
    print("S0 full-action gate")
    print("=" * 19)
    print(f"eta={fmt(ETA)}")
    print()
    for ingredient in INGREDIENTS:
        print(ingredient.name)
        print(f"  status:          {ingredient.status}")
        print(f"  supplies:        {ingredient.supplies}")
        print(f"  does not supply: {ingredient.does_not_supply}")
        print()

    print("Gate verdict:")
    print("  The metric supplies eta and L1 as separate objects.")
    print("  The missing S0_full gate is the native boundary rule that forms")
    print("  the product eta L1 as the angular value action.")


if __name__ == "__main__":
    main()

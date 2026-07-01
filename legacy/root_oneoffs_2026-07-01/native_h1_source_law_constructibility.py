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
    role: str


INGREDIENTS = [
    Ingredient(
        name="spatial curvature fraction",
        status="exact metric geometry",
        role="R3(phi0)/R2(phi0)=q",
    ),
    Ingredient(
        name="H1/S2 projection factor",
        status="exact after H1 selection",
        role="one H1 share gives factor 1/3",
    ),
    Ingredient(
        name="source law product",
        status="not automatic",
        role="s(q)=q/3 requires a variational rule coupling the two ingredients",
    ),
]


def main() -> None:
    print("H1 source-law constructibility audit")
    print("=" * 41)
    for ingredient in INGREDIENTS:
        print(ingredient.name)
        print(f"  status: {ingredient.status}")
        print(f"  role:   {ingredient.role}")
        print()

    print("If the source law is native:")
    print("  s(q) = q/3")
    print("then the exact q-flow is:")
    print("  dq/dt = q^2 - q + 2q/3")
    print("        = q(q - 1/3)")
    print()
    print("Fixed branches:")
    print("  q = 0")
    print("  q = 1/3")
    print()
    q = Fraction(1, 3)
    print("At the nontrivial branch:")
    print(f"  s(q) = {fmt(q / 3)}")
    print("  the source is constant through the collar")
    print("  finite C1 action keeps the q=1/3 branch")
    print("  delta_h = 0")
    print()
    print("Constructibility verdict:")
    print("  The metric supplies q and the H1 projection factor separately.")
    print("  The source law s(q)=q/3 is derived only if the UDT boundary/collar")
    print("  variational principle forms their product as the active H1 source.")
    print("  Until then, s(q)=q/3 is the cleanest narrowed postulate, not a")
    print("  completed derivation.")


if __name__ == "__main__":
    main()

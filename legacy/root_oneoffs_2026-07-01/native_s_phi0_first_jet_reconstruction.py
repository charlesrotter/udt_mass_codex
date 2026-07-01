from dataclasses import dataclass
from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


@dataclass(frozen=True)
class FirstJetPiece:
    name: str
    fixed_by: str
    first_variation_content: str


Q = Fraction(1, 3)
BOUNDARY = Q / 2
ETA = Q / 6


PIECES = [
    FirstJetPiece(
        "value closure",
        "finite closed cell requirement",
        "delta S contains multiplier term enforcing a_tail=0",
    ),
    FirstJetPiece(
        "C1 conjugate momentum",
        "banked P_phi0",
        "dS/df at phi0 must cancel Pi_f and carry q/2=1/6",
    ),
    FirstJetPiece(
        "H1 projection",
        "round-S2 second moment",
        "projected first variation is eta=(q/2)/3=1/18",
    ),
    FirstJetPiece(
        "one-sided split",
        "banked P_transfer gluing rule if accepted",
        "each side carries eta/2=1/36",
    ),
]


def main() -> None:
    print("S_phi0 first-jet reconstruction")
    print("=" * 35)
    print("Known active-lane scalars:")
    print(f"  q = {fmt(Q)}")
    print(f"  q/2 = {fmt(BOUNDARY)}")
    print(f"  eta = {fmt(ETA)}")
    print()
    for piece in PIECES:
        print(piece.name)
        print(f"  fixed by:                 {piece.fixed_by}")
        print(f"  first-variation content:  {piece.first_variation_content}")
        print()

    print("First-jet verdict:")
    print("  The active lane can specify the first variation of S_phi0 at the")
    print("  boundary point. This is enough to carry eta.")
    print("  It is not enough to determine coefficient weights.")


if __name__ == "__main__":
    main()

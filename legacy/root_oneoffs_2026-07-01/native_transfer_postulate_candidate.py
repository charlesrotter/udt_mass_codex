from fractions import Fraction
import math


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("transfer postulate candidate audit")
    print("=" * 38)
    eta = Fraction(1, 18)
    one_sided = eta / 2
    gamma = 3.0 * math.exp(-float(one_sided))
    print("Given banked P_phi0:")
    print(f"  eta = {fmt(eta)}")
    print()
    print("Candidate transfer rule:")
    print("  P_transfer: each independent edge node contributes")
    print("    gamma = N exp(-eta/2)")
    print("  with N=3 from H1/S2 channel multiplicity.")
    print()
    print("For eta=1/18:")
    print(f"  eta/2 = {fmt(one_sided)}")
    print(f"  gamma = 3 exp(-1/36) = {gamma:.12g}")
    print()
    print("What must be derived to upgrade P_transfer:")
    print("  1. N=3 acts as multiplicity in the transfer, not only representation count.")
    print("  2. eta/2 is the correct one-sided boundary action per independent node.")
    print("  3. node contributions multiply rather than add.")
    print("  4. typed nodes are independent after shared H1 frame merging.")
    print()
    print("No-invention verdict:")
    print("  P_transfer is a second possible compact postulate, but it is not")
    print("  resolved by P_phi0. Keep it separate.")


if __name__ == "__main__":
    main()

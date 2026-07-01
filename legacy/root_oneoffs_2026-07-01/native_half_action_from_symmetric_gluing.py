from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("half-action from symmetric gluing")
    print("=" * 36)
    eta = Fraction(1, 18)
    print("Let the full shared phi0 edge action be:")
    print(f"  B = eta = {fmt(eta)}")
    print()
    print("Let a one-sided transfer kernel carry side weight w.")
    print()
    print("Composable gluing condition:")
    print("  left side + right side = one full shared boundary action")
    print("  w + w = B")
    print()
    print("Reflection symmetry of the two sides gives:")
    print("  w_left = w_right = w")
    print()
    print("Therefore:")
    print(f"  w = B/2 = eta/2 = {fmt(eta / 2)}")
    print()
    print("No-approximation verdict:")
    print("  eta/2 is exact if the transfer kernel is one side of a symmetric")
    print("  composable phi0 boundary action. The remaining burden is proving")
    print("  that the physical transfer object is such a one-sided kernel.")


if __name__ == "__main__":
    main()

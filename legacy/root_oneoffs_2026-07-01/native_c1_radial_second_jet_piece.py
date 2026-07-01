from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def action(q: Fraction) -> Fraction:
    return q * q / (4 * (1 - 2 * q))


def first_derivative(q: Fraction) -> Fraction:
    # derivative of q^2/[4(1-2q)]
    return q * (1 - q) / (2 * (1 - 2 * q) ** 2)


def second_derivative(q: Fraction) -> Fraction:
    # derivative of q(1-q)/[2(1-2q)^2]
    return Fraction(1, 2) / (1 - 2 * q) + 2 * q * (1 - q) / ((1 - 2 * q) ** 3)


def main() -> None:
    print("C1 radial second-jet piece")
    print("=" * 28)
    q = Fraction(1, 3)
    a0 = action(q)
    a1 = first_derivative(q)
    a2 = second_derivative(q)
    print("For A(q)=S_C1/R=q^2/[4(1-2q)]:")
    print(f"  A(1/3)       = {fmt(a0)}")
    print(f"  A'(1/3)      = {fmt(a1)}")
    print(f"  A''(1/3)     = {fmt(a2)}")
    print(f"  H1-projected A''/3 = {fmt(a2 / 3)}")
    print()
    print("Interpretation:")
    print("  The C1 metric supplies an exact scalar radial stiffness at the")
    print("  q=1/3 branch. This is a second-jet piece in the q/radial")
    print("  direction, not the full typed Hessian for M1/E1 coefficients.")
    print()
    print("Pattern verdict:")
    print("  Tier D should not start from free coefficient fitting. It should")
    print("  first ask whether each typed Hessian block descends from exact")
    print("  C1/HJ second variations like this radial piece.")


if __name__ == "__main__":
    main()

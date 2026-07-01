from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def action(q: Fraction) -> Fraction:
    return q * q / (4 * (1 - 2 * q))


def first_derivative(q: Fraction) -> Fraction:
    return q * (1 - q) / (2 * (1 - 2 * q) ** 2)


def second_derivative(q: Fraction) -> Fraction:
    return Fraction(1, 2) / (1 - 2 * q) + 2 * q * (1 - q) / ((1 - 2 * q) ** 3)


def main() -> None:
    print("exact q-variation Taylor expansion")
    print("=" * 40)
    print("A(q)=S_C1/R=q^2/[4(1-2q)]")
    print("q0=1/3, u=q-q0")
    print()
    q0 = Fraction(1, 3)
    a0 = action(q0)
    a1 = first_derivative(q0)
    a2 = second_derivative(q0)
    print(f"  A(q0)  = {fmt(a0)}")
    print(f"  A'(q0) = {fmt(a1)}")
    print(f"  A''(q0)= {fmt(a2)}")
    print()
    print("Taylor through second order:")
    print(f"  A(q0+u) = {fmt(a0)} + {fmt(a1)} u + {fmt(a2 / 2)} u^2 + O(u^3)")
    print()
    print("H1-projected Taylor through second order:")
    print(
        f"  A_H1(q0+u) = {fmt(a0 / 3)} + {fmt(a1 / 3)} u"
        f" + {fmt(a2 / 6)} u^2 + O(u^3)"
    )
    print()
    print("Variation verdict:")
    print("  The radial q direction has a nonzero first variation at q=1/3.")
    print("  Therefore q=1/3 is not a stationary point of the bare C1 action.")
    print("  Its role is a self-similar/action-value balance unless another")
    print("  boundary condition or constraint supplies the stationarity equation.")


if __name__ == "__main__":
    main()

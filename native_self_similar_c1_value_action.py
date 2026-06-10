from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def c1_action_over_radius(q: Fraction) -> Fraction:
    return q * q / (4 * (1 - 2 * q))


def main() -> None:
    print("self-similar C1 value action")
    print("=" * 31)
    print("For a self-similar finite cell:")
    print("  f(r) = (R/r)^q")
    print("  f(R) = 1")
    print("  f' = -q R^q r^(-q-1)")
    print()
    print("Radial C1 action:")
    print("  S_C1 = (1/4) integral_0^R r^2 f'^2 dr")
    print("       = q^2 R / [4(1-2q)]")
    print()
    print("Scale-normalized action:")
    print("  S_C1/R = q^2/[4(1-2q)]")
    print()

    q = Fraction(1, 3)
    action = c1_action_over_radius(q)
    projected = action / 3
    eta = q / 6
    side = eta / 2
    print("For q=1/3:")
    print(f"  S_C1/R = {fmt(action)}")
    print(f"  H1 projection of action = (S_C1/R)/3 = {fmt(projected)}")
    print(f"  eta = q/6 = {fmt(eta)}")
    print(f"  eta/2 = {fmt(side)}")
    print()
    print("Exact equality:")
    print("  (S_C1/R)/3 = eta/2 = 1/36")
    print()
    print("No-approximation verdict:")
    print("  For the self-similar q=1/3 cell, the metric C1 action value")
    print("  itself supplies the one-sided H1 action unit after projection.")
    print("  This is stronger than reading eta/2 only from symmetric gluing.")


if __name__ == "__main__":
    main()

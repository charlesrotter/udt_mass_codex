from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def c1_action_over_radius(q: Fraction) -> Fraction:
    return q * q / (4 * (1 - 2 * q))


def main() -> None:
    print("C1 value-momentum pair")
    print("=" * 27)
    print("For the self-similar finite cell:")
    print("  f(r) = (R/r)^q")
    print("  S_C1/R = q^2/[4(1-2q)]")
    print("  -Pi_f/R = q/2 at phi0")
    print()

    q = Fraction(1, 3)
    action = c1_action_over_radius(q)
    projected_action = action / 3
    projected_momentum = (q / 2) / 3
    eta = q / 6

    print("At q=1/3:")
    print(f"  S_C1/R = {fmt(action)}")
    print(f"  H1 projected action = {fmt(projected_action)}")
    print(f"  H1 projected momentum = {fmt(projected_momentum)}")
    print(f"  eta = q/6 = {fmt(eta)}")
    print(f"  eta/2 = {fmt(eta / 2)}")
    print()
    print("Exact pair:")
    print(f"  projected momentum = eta = {fmt(eta)}")
    print(f"  projected action   = eta/2 = {fmt(eta / 2)}")
    print()
    print("Jigsaw verdict:")
    print("  The same C1 metric functional supplies both the eta momentum")
    print("  and the eta/2 action value on the self-similar H1-projected branch.")
    print("  This fills the value-action numerical hole, while the boundary")
    print("  transfer interpretation remains a separate operation-level gate.")


if __name__ == "__main__":
    main()

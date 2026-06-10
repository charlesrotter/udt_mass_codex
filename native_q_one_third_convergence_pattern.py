from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def c1_action_over_radius(q: Fraction) -> Fraction:
    return q * q / (4 * (1 - 2 * q))


def main() -> None:
    print("q=1/3 convergence pattern")
    print("=" * 29)
    q = Fraction(1, 3)
    action = c1_action_over_radius(q)
    momentum = q / 2
    action_exponent = 1 - 2 * q

    print("Exact balances at q=1/3:")
    print(f"  profile exponent q                 = {fmt(q)}")
    print(f"  finite-action remainder 1-2q       = {fmt(action_exponent)}")
    print(f"  unprojected C1 action S_C1/R       = {fmt(action)}")
    print(f"  unprojected boundary momentum q/2  = {fmt(momentum)}")
    print(f"  action / momentum                  = {fmt(action / momentum)}")
    print()
    print("Equivalent nontrivial conditions:")
    print("  1 - 2q = q                 -> q=1/3")
    print("  q^2/[4(1-2q)] = q/4        -> q=1/3")
    print("  [S_C1/R]/3 = (q/6)/2       -> q=1/3")
    print()
    print("Pattern verdict:")
    print("  q=1/3 is the point where profile scaling, finite-action scaling,")
    print("  C1 action value, and projected side-action normalization lock")
    print("  together. This is convergence evidence, not a standalone variational")
    print("  selection theorem.")


if __name__ == "__main__":
    main()

from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("C1 value-action q condition")
    print("=" * 29)
    print("Demand that the projected C1 value action equal the side action:")
    print("  [q^2/(4(1-2q))]/3 = eta/2")
    print()
    print("With eta=q/6:")
    print("  q^2/[12(1-2q)] = q/12")
    print()
    print("For q != 0, multiply by 12/q:")
    print("  q/(1-2q) = 1")
    print("  q = 1 - 2q")
    print("  3q = 1")
    print("  q = 1/3")
    print()
    print("Branches:")
    print("  q=0 trivial")
    print("  q=1/3 nontrivial self-similar value-action branch")
    print()
    q = Fraction(1, 3)
    print("At q=1/3:")
    print(f"  finite-action condition q<1/2 holds: {q < Fraction(1, 2)}")
    print(f"  action exponent 1-2q = {fmt(1 - 2 * q)}")
    print(f"  profile exponent q = {fmt(q)}")
    print()
    print("Condition verdict:")
    print("  The same q=1/3 condition appears as equality between profile scaling,")
    print("  action-remainder scaling, and projected side-action normalization.")
    print("  This does not alone derive P_phi0, but it upgrades q=1/3 from a")
    print("  banked slope to a metric value-action fixed point candidate.")


if __name__ == "__main__":
    main()

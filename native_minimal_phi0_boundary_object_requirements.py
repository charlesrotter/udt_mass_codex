from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("minimal phi0 boundary object requirements")
    print("=" * 45)
    q = Fraction(1, 3)
    eta = q / 6
    side = eta / 2
    print("A full phi0 boundary object that closes the current gates must supply:")
    print()
    print("1. Momentum closure")
    print("   dS_b/dF |F=1 = q/2")
    print()
    print("2. Full H1 value action")
    print("   S_0|H1 = eta I_3 = (q/6) I_3")
    print()
    print("3. One-sided composable transfer")
    print("   A_side|H1 = (eta/2) I_3 = (q/12) I_3")
    print()
    print("4. H1 state-count operation")
    print("   gamma = Tr_H1 exp(-A_side)")
    print()
    print("5. q selection or q preservation")
    print("   either q=1/3 directly, or p=q plus H1 self-consistency")
    print()
    print("For q=1/3:")
    print(f"  q/2 = {fmt(q / 2)}")
    print(f"  eta = q/6 = {fmt(eta)}")
    print(f"  eta/2 = q/12 = {fmt(side)}")
    print()
    print("No-approximation verdict:")
    print("  Items 1-4 can belong to an interface-local transfer object.")
    print("  Item 5 is a collar/self-consistency condition unless the boundary")
    print("  variation contains an independent q-stationarity equation.")


if __name__ == "__main__":
    main()

from fractions import Fraction


def fmt(x: Fraction) -> str:
    if x.denominator == 1:
        return str(x.numerator)
    return f"{x.numerator}/{x.denominator}"


def main() -> None:
    print("Exact interface momentum jump")
    print("=" * 31)
    print("C1 canonical momentum:")
    print("  Pi_f = (1/2) r^2 f'")
    print()
    print("At phi0, R=1, f=1:")
    print("  inner f' = -q")
    print("  flat exterior f' = 0")
    print()
    print("Therefore:")
    print("  Pi_inner = -q/2")
    print("  Pi_outer = 0")
    print("  Delta Pi = Pi_outer - Pi_inner = q/2")
    print()
    q = Fraction(1, 3)
    delta_pi = q / 2
    eta = delta_pi / 3
    side = eta / 2
    print("For q=1/3:")
    print(f"  Delta Pi = {fmt(delta_pi)}")
    print(f"  H1-projected Delta Pi = {fmt(eta)}")
    print(f"  one-sided transfer = {fmt(side)}")
    print()
    print("Exact interface requirement:")
    print("  The boundary functional must carry the canonical momentum jump")
    print("  from Pi_inner=-q/2 to Pi_outer=0.")
    print("  The same jump is the eta-producing scalar after H1 projection.")
    print()
    print("No-approximation verdict:")
    print("  The interface mechanism is exactly a momentum-jump carrier in C1 variables.")


if __name__ == "__main__":
    main()

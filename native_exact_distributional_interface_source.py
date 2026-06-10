from fractions import Fraction


def fmt(x: Fraction) -> str:
    if x.denominator == 1:
        return str(x.numerator)
    return f"{x.numerator}/{x.denominator}"


def main() -> None:
    print("Exact distributional interface source")
    print("=" * 39)
    print("C1 radial field equation in f:")
    print("  (r^2 f')' = J(r)")
    print()
    print("Integrate across a thin phi0 interface at R:")
    print("  [r^2 f']_out-in = integral J(r) dr")
    print()
    print("In canonical momentum Pi_f=(1/2)r^2 f':")
    print("  Delta Pi_f = Pi_out - Pi_in = (1/2) integral J(r) dr")
    print()
    print("For flat exterior and inner f'=-q/R at R=1:")
    print("  Pi_in = -q/2")
    print("  Pi_out = 0")
    print("  Delta Pi_f = q/2")
    print("  integral J dr = q")
    print()
    q = Fraction(1, 3)
    delta_pi = q / 2
    source_integral = q
    eta = delta_pi / 3
    print("Self-similar q=1/3:")
    print(f"  Delta Pi_f = {fmt(delta_pi)}")
    print(f"  interface source integral = {fmt(source_integral)}")
    print(f"  H1-projected Delta Pi_f = {fmt(eta)}")
    print()
    print("Exact conclusion:")
    print("  Any phi0 boundary functional that creates the eta-producing jump is")
    print("  equivalent, in the radial C1 equation, to a distributional interface")
    print("  source with integrated strength q.")
    print("  The H1/S2 projection acts on Delta Pi_f=q/2, not directly on J=q.")
    print()
    print("No-approximation verdict:")
    print("  The interface source strength is exactly q for the stated collar data.")


if __name__ == "__main__":
    main()

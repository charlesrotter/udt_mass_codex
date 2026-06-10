from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("tail-cancel / H1-survive gluing identity")
    print("=" * 44)
    print("Source-free radial C1 identity:")
    print("  (r^2 f')' = 0")
    print("  f = A + B/r")
    print("  Pi_f = (1/2)r^2 f' = -B/2")
    print()
    print("Exterior flatness:")
    print("  B_out = 0")
    print("  Pi_out = 0")
    print("  exterior radial tail cancels")
    print()
    print("Interior first jet at phi=0:")
    print("  f(R)=1")
    print("  q = -R f'_in/f(R)")
    print("  Pi_in = -qR/2")
    print()
    print("Two-sided gluing with an interface source:")
    print("  Pi_out - Pi_in = Delta Pi")
    print("  Delta Pi = qR/2")
    print()
    print("Thus the exterior tail can be zero while the interior first jet")
    print("survives as a localized interface momentum jump.")
    print()
    q = Fraction(1, 3)
    r = Fraction(1)
    delta_pi = q * r / 2
    eta = delta_pi / 3
    side = eta / 2
    print("At the nontrivial H1-compatible branch:")
    print(f"  q = {fmt(q)}")
    print(f"  Delta Pi/R = {fmt(delta_pi / r)}")
    print(f"  H1 projection eta = (Delta Pi/R)/3 = {fmt(eta)}")
    print(f"  one-side bridge action = eta/2 = {fmt(side)}")
    print()
    print("H1 survival condition:")
    print("  The radial tail is scalar/monopole data and is killed outside.")
    print("  The surviving imprint is the H1-projected interface jump:")
    print("    P_H1(Delta Pi/R) = eta I3")
    print()
    print("Gluing verdict:")
    print("  The desired operation is not smooth matching.")
    print("  It is internalized-asymptotic gluing:")
    print("    value f=1 is shared,")
    print("    exterior tail B_out is zero,")
    print("    interior first jet q survives as Delta Pi,")
    print("    H1 projection carries the macro-accessible imprint.")
    print()
    print("Remaining proof:")
    print("  Derive why the elementary bridge selects q=1/3 / H1 rather")
    print("  than merely allowing an arbitrary interface jump.")


if __name__ == "__main__":
    main()

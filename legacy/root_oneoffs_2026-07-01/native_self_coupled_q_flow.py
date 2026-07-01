from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("self-coupled q-flow")
    print("=" * 20)
    print("Start with exact q-flow:")
    print("  dq/dt = q^2 - q + 2s(q)")
    print()
    print("Self-coupled curvature-share source:")
    print("  s(q) = q/3")
    print()
    print("Then:")
    print("  dq/dt = q^2 - q + 2q/3")
    print("        = q^2 - q/3")
    print("        = q(q - 1/3)")
    print()
    print("Fixed branches:")
    print("  q = 0")
    print("  q = 1/3")
    print()
    q = Fraction(1, 3)
    print("On the nontrivial branch:")
    print(f"  q = {fmt(q)}")
    print(f"  s(q) = {fmt(q / 3)}")
    print("  dq/dt = 0")
    print("  delta_h = 0")
    print()
    print("No-approximation verdict:")
    print("  s(q)=q/3 is not a constant-source assumption off shell.")
    print("  It becomes constant on the selected fixed branch q=1/3.")
    print("  This can derive P_phi0 if the source law itself is native.")


if __name__ == "__main__":
    main()

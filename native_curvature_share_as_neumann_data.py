from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("curvature-share closure as Neumann boundary data")
    print("=" * 53)
    print("At phi0:")
    print("  K_rad = q/(2R^2)")
    print("  K_S2 = 1/R^2")
    print("  Pi_f = -qR/2")
    print()
    print("Therefore:")
    print("  K_rad / K_S2 = q/2")
    print("  -Pi_f / R = q/2")
    print()
    print("Minimal curvature-share closure:")
    print("  K_rad / K_S2 = 1/6")
    print()
    print("Equivalent momentum boundary condition:")
    print("  -Pi_f / R = 1/6")
    print("  Pi_f = -R/6")
    print()
    q = Fraction(1, 3)
    print("This gives:")
    print(f"  q = {fmt(q)}")
    print(f"  eta = q/6 = {fmt(q / 6)}")
    print(f"  one-sided transfer = q/12 = {fmt(q / 12)}")
    print()
    print("Variational interpretation:")
    print("  This is Neumann/edge momentum data for the C1 radial action.")
    print("  It is not ordinary C1 bulk stress and not a potential B(f) alone.")
    print()
    print("No-invention verdict:")
    print("  If accepted as a postulate, the smallest honest form is:")
    print("    the phi0 edge fixes the dimensionless C1 momentum -Pi_f/R to one")
    print("    radial-angular curvature share, 1/6.")
    print("  To upgrade it from postulate to derivation, the boundary variation")
    print("  must produce this Neumann value.")


if __name__ == "__main__":
    main()

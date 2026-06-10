from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("Spatial curvature fraction at phi0")
    print("=" * 37)
    print("Spatial metric on a static slice:")
    print("  dl^2 = f^{-1} dr^2 + r^2 dOmega^2")
    print()
    print("Exact 3D scalar curvature:")
    print("  R3 = 2(1 - f - r f')/r^2")
    print()
    print("Intrinsic scalar curvature of the round S2 collar:")
    print("  R2 = 2/r^2")
    print()
    print("At phi0:")
    print("  f(R)=1")
    print("  f'(R)=-q/R")
    print("  R3(phi0) = 2q/R^2")
    print("  R2(phi0) = 2/R^2")
    print()
    print("Therefore:")
    print("  R3(phi0) / R2(phi0) = q")
    print()
    q = Fraction(1, 3)
    print("For q=1/3:")
    print(f"  R3 = {fmt(q)} R2")
    print("  the spatial curvature at the collar is one third of the")
    print("  intrinsic S2 collar curvature.")
    print()
    print("No-invention verdict:")
    print("  q is not merely a slope parameter.")
    print("  At phi0 it is exactly the fraction of S2 intrinsic curvature")
    print("  appearing as spatial-slice scalar curvature.")
    print("  This does not derive q=1/3, but it makes the target geometric:")
    print("  derive why the native closure selects the one-third curvature fraction.")


if __name__ == "__main__":
    main()

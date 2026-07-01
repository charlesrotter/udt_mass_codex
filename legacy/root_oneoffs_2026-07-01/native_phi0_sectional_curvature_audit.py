from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("phi0 sectional-curvature audit")
    print("=" * 37)
    print("Spatial metric:")
    print("  dl^2 = f^{-1} dr^2 + r^2 dOmega^2")
    print()
    print("Use proper radial distance rho with:")
    print("  d rho = dr / sqrt(f)")
    print("  dr/d rho = sqrt(f)")
    print()
    print("Exact sectional curvatures:")
    print("  K_radial-angular = -f'/(2r)")
    print("  K_tangent-sphere = (1-f)/r^2")
    print()
    print("3D scalar curvature:")
    print("  R3 = 4 K_radial-angular + 2 K_tangent-sphere")
    print("     = 2(1-f-rf')/r^2")
    print()
    print("At phi0:")
    print("  f(R)=1")
    print("  f'(R)=-q/R")
    print("  K_radial-angular = q/(2R^2)")
    print("  K_tangent-sphere = 0")
    print("  R3 = 2q/R^2")
    print()
    print("Intrinsic S2 collar curvature:")
    print("  K_S2 = 1/R^2")
    print("  R2 = 2/R^2")
    print()
    print("Ratios:")
    print("  K_radial-angular / K_S2 = q/2")
    print("  (two radial-angular planes summed) / K_S2 = q")
    print("  R3 / R2 = q")
    print()
    q = Fraction(1, 3)
    print("For q=1/3:")
    print(f"  K_radial-angular / K_S2 = {fmt(q / 2)}")
    print(f"  R3 / R2 = {fmt(q)}")
    print()
    print("No-invention verdict:")
    print("  q=1/3 is not ordinary isotropic 3D curvature.")
    print("  At phi0, the ambient tangential sectional curvature is zero.")
    print("  The q data lives in the two radial-angular sectional planes.")
    print("  The eta unit q/2 is exactly the ratio of each radial-angular")
    print("  sectional curvature to the intrinsic S2 curvature.")


if __name__ == "__main__":
    main()

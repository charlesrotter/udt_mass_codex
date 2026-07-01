from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("phi0 DtN potential shift")
    print("=" * 29)
    print("After Liouville transform v=r a, each angular mode sees:")
    print("  H_l = -d_rho^2 + V_l")
    print("  V_l = r''/r + l(l+1)/r^2")
    print()
    print("UDT positional-dilation term:")
    print("  r'' = f'/2")
    print()
    print("At phi0:")
    print("  f=1")
    print("  f'=-q/R")
    print("  r''/r = -q/(2R^2)")
    print()
    print("Therefore:")
    print("  V_l(phi0) = [l(l+1) - q/2]/R^2")
    print()
    q = Fraction(1, 3)
    print("If P_phi0 is banked:")
    print(f"  q = {fmt(q)}")
    print("  V_l(phi0) = [l(l+1) - 1/6]/R^2")
    print()
    print("For ell=1:")
    v1 = Fraction(2, 1) - q / 2
    print(f"  V_1(phi0) = {fmt(v1)}/R^2")
    print()
    print("Compare product normalized angular kernel:")
    print("  L1 = I3")
    print("  product collar potential would be 1/R^2 after normalization")
    print()
    print("No-overclaim verdict:")
    print("  Positional dilation shifts the boundary-normal DtN operator.")
    print("  The naive product kernel L1=I3 is exact as a boundary angular operator,")
    print("  but not as the full bulk DtN normal operator through the warped collar.")


if __name__ == "__main__":
    main()

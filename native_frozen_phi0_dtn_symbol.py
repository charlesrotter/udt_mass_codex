from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("frozen phi0 DtN symbol diagnostic")
    print("=" * 38)
    print("Refactored Liouville normal operator:")
    print("  H_l = -d_rho^2 + V_l")
    print("  V_l = [l(l+1) - q/2]/R^2 at phi0")
    print()
    print("Frozen-coefficient DtN eigenvalue:")
    print("  lambda_l^frozen = sqrt(V_l)")
    print("                  = sqrt(l(l+1)-q/2)/R")
    print()
    print("Product-cylinder comparison:")
    print("  lambda_l^product = sqrt(l(l+1))/R")
    print()
    q = Fraction(1, 3)
    l = 1
    shifted = Fraction(l * (l + 1), 1) - q / 2
    product = Fraction(l * (l + 1), 1)
    ratio_sq = shifted / product
    print("For P_phi0 q=1/3 and ell=1:")
    print(f"  shifted V coefficient = {fmt(shifted)}")
    print(f"  product V coefficient = {fmt(product)}")
    print(f"  squared DtN ratio = {fmt(ratio_sq)}")
    print("  DtN ratio = sqrt(11/12)")
    print()
    print("Diagnostic verdict:")
    print("  The frozen local DtN symbol is shifted by positional dilation.")
    print("  Therefore the simple product kernel is not the local bulk DtN symbol")
    print("  unless an abstract boundary action or exact reduction removes this")
    print("  warping contribution.")


if __name__ == "__main__":
    main()

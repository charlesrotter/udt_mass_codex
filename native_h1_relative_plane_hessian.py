from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("H1 relative-plane Hessian")
    print("=" * 27)
    print("Start with an H1 identity Hessian:")
    print("  K_H1 = k I3")
    print()
    print("Choose an orthonormal split:")
    print("  e0 = common-amplitude direction")
    print("  e1,e2 = relative-shape plane")
    print()
    print("Because K_H1 is proportional to I3:")
    print("  O^T K_H1 O = k I3")
    print()
    print("After fixing or removing the common amplitude e0:")
    print("  K_relative = k I2")
    print()
    eta = Fraction(1, 18)
    side = eta / 2
    print("For the intrinsic side-action branch:")
    print(f"  k = eta/2 = {fmt(side)}")
    print(f"  K_relative = {fmt(side)} I2")
    print()
    print("For the warped-DtN branch:")
    print("  k = fixed normalization * D_1")
    print("  K_relative = same k on both relative coordinates")
    print()
    print("Variation verdict:")
    print("  The E1 two-dimensional relative plane does not require a new")
    print("  anisotropic coefficient if it is the common-amplitude quotient")
    print("  of the H1 identity block. The open question is whether the typed")
    print("  E1 relative plane is exactly this quotient.")


if __name__ == "__main__":
    main()

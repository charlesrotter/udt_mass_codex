from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("shell stress as S0 coupling audit")
    print("=" * 36)
    q = Fraction(1, 3)
    angular_stress = q / 2
    eta = angular_stress / 3
    print("For a flat exterior and inner slope f'_in=-q/R:")
    print("  [K^a_b] = diag(q/2R, 0, 0)")
    print("  [K] = q/2R")
    print("  [K^a_b] - delta^a_b[K] = (0, -q/2R, -q/2R)")
    print()
    print("Thus the jump has angular-only isotropic stress scale:")
    print(f"  q/2 = {fmt(angular_stress)}")
    print()
    print("H1/S2 projection gives:")
    print(f"  eta = (q/2)/3 = {fmt(eta)}")
    print()
    print("What this supports:")
    print("  radial slope momentum couples to angular surface geometry at phi0")
    print()
    print("What it does not yet supply:")
    print("  the constant-blind Laplacian operator L1")
    print()
    print("Reason:")
    print("  isotropic angular stress couples first to angular metric/area variation,")
    print("  while L1 requires a shape-gradient or nonconstant-mode boundary action.")
    print()
    print("No-approximation verdict:")
    print("  The shell stress partially closes scalar-to-angular coupling.")
    print("  It supplies the angular surface scale q/2, but not yet the L1 operator.")


if __name__ == "__main__":
    main()

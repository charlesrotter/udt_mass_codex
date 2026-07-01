from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("Minimal curvature-share closure candidate")
    print("=" * 43)
    print("Native phi0 quantities:")
    print("  K_S2 = 1/R^2")
    print("  K_radial-angular = q/(2R^2)")
    print("  two radial-angular planes sum to q/R^2")
    print()
    print("H1/S2 isotropic share:")
    print("  <n_a n_b> = delta_ab/3")
    print("  one isotropic frame share of K_S2 is K_S2/3")
    print()
    print("Minimal closure condition:")
    print("  total radial-angular curvature share = one H1 isotropic share")
    print("  q K_S2 = K_S2/3")
    print("  q = 1/3")
    print()
    q = Fraction(1, 3)
    print("Consequences:")
    print(f"  per radial-angular plane: q/2 = {fmt(q / 2)}")
    print(f"  H1/S2 projected eta: (q/2)/3 = {fmt(q / 6)}")
    print(f"  one-sided transfer: eta/2 = {fmt(q / 12)}")
    print()
    print("Status:")
    print("  This is a minimal native closure postulate, not a derivation.")
    print("  It does not import Standard Model machinery or Einstein dynamics.")
    print("  It postulates the curvature-share allocation at the phi0 edge.")
    print()
    print("Test:")
    print("  Derive or reject this closure from the C1/angular boundary variation.")


if __name__ == "__main__":
    main()

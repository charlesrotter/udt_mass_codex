from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("phi0 edge-embedding resolution candidate")
    print("=" * 48)
    print("Minimal optional postulate:")
    print("  P_phi0: the phi0 edge fixes the dimensionless C1 boundary momentum")
    print("          to one radial-angular curvature share.")
    print()
    print("Equivalent forms:")
    print("  -Pi_f/R = 1/6")
    print("  K_rad/K_S2 = 1/6")
    print("  q/2 = 1/6")
    print("  q = 1/3")
    print()
    q = Fraction(1, 3)
    s = q * (1 - q) / 2
    print("Exact consequences:")
    print(f"  q = {fmt(q)}")
    print(f"  s = q(1-q)/2 = {fmt(s)}")
    print(f"  eta = q/6 = {fmt(q / 6)}")
    print(f"  one-sided transfer = eta/2 = {fmt(q / 12)}")
    print()
    print("Interpretation:")
    print("  mass emergence starts as a phi/angular edge condition:")
    print("    C1 boundary momentum")
    print("    radial-angular embedding curvature")
    print("    H1/S2 projection")
    print()
    print("What this resolves:")
    print("  - why intrinsic angular algebra survives")
    print("  - where q/2 lives geometrically")
    print("  - why eta=1/18 follows from a single small closure")
    print("  - why ordinary C1 bulk stress and Maxwell are not the eta mechanism")
    print()
    print("What this does not resolve:")
    print("  - derivation of P_phi0 from a boundary kernel")
    print("  - cascade depth rule")
    print("  - gamma transfer normalization beyond eta")
    print("  - branch coefficient ratios")


if __name__ == "__main__":
    main()

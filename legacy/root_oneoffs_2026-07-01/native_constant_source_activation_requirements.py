from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("constant source activation requirements")
    print("=" * 41)
    print("Radial source equation:")
    print("  f'' + 2f'/r + 2s f/r^2 = 0")
    print()
    print("Intrinsic S2 scalar curvature:")
    print("  R2 = 2/r^2")
    print()
    print("Therefore:")
    print("  2s f/r^2 = s R2 f")
    print()
    print("A constant source follows if:")
    print("  1. the active source is a fixed fraction of R2,")
    print("  2. the fraction is built from normalized H1/S2 data,")
    print("  3. no radial amplitude/window multiplies the source.")
    print()
    s = Fraction(1, 9)
    print(f"For s={fmt(s)}:")
    print("  source = (1/9) R2 f")
    print()
    print("No-approximation verdict:")
    print("  Constant s is native if activation is a fixed curvature-share.")
    print("  Any radial amplitude, window, or branch-dependent normalization")
    print("  makes s(t) run and reopens delta_h.")


if __name__ == "__main__":
    main()

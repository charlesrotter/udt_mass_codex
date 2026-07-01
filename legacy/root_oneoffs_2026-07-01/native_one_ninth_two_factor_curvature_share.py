from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("one-ninth two-factor curvature share")
    print("=" * 41)
    print("Target:")
    print("  s = 1/9")
    print("  source = s R2 f")
    print()
    print("Single S2/H1 isotropic projection:")
    print("  <n_a n_b> = delta_ab/3")
    print("  trace share per H1 component = 1/3")
    print("  this gives 1/3, not 1/9")
    print()
    print("Non-circular two-factor route:")
    print("  source fraction = curvature-share factor x H1 projection factor")
    print("                  = (1/3) x (1/3)")
    print("                  = 1/9")
    print()
    print("Required independence:")
    print("  the first 1/3 must be a curvature/source share,")
    print("  the second 1/3 must be an H1/S2 projection share,")
    print("  and they must not be the same projection counted twice.")
    print()
    value = Fraction(1, 3) * Fraction(1, 3)
    print(f"Exact product: {fmt(value)}")
    print()
    print("No-approximation verdict:")
    print("  s=1/9 is derivable only if the metric supplies two independent")
    print("  one-third factors. A single isotropic projection is insufficient.")


if __name__ == "__main__":
    main()

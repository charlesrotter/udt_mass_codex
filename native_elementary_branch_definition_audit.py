from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("elementary branch definition audit")
    print("=" * 34)
    print("Pre-spectrum elementary branch means:")
    print("  no typed excitation/depth structure yet")
    print("  no additional scalar source residual")
    print("  no positive relative scalar boundary-layer mode")
    print("  keep only metric-forced harmonic carrier data")
    print()
    print("Metric-forced carrier data at phi0:")
    print("  value normalization f=1")
    print("  absolute harmonic H1 area carrier")
    print("  first jet q through C1 momentum")
    print()
    print("Excluded from elementary ground branch:")
    print("  relative scalar h residual with E[y]>0")
    print("  because it is an excitation/dressing of the collar domain")
    print()
    print("Therefore in the elementary branch:")
    print("  h=1")
    print("  delta_h=0")
    print("  p=q")
    print()

    q = Fraction(1, 3)
    print("Then H1 one-graph compatibility gives:")
    print(f"  q=p={fmt(q)}")
    print(f"  s={fmt(q * (1 - q) / 2)}")
    print(f"  eta={fmt(q / 6)}")
    print(f"  eta/2={fmt(q / 12)}")
    print()
    print("Verdict:")
    print("  P_domain is equivalent to defining the pre-spectrum elementary")
    print("  branch as the least-action harmonic carrier branch.")
    print("  Nonzero h is not forbidden absolutely; it is classified as a")
    print("  higher relative scalar boundary-layer excitation outside the")
    print("  elementary branch.")


if __name__ == "__main__":
    main()

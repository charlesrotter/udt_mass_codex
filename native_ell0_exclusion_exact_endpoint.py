from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("ell=0 exclusion from exact endpoint equation")
    print("=" * 50)
    print("Endpoint source equation:")
    print("  p(1-p)/2 = eta lambda")
    print()
    print("For the constant angular sector:")
    print("  ell = 0")
    print("  lambda = ell(ell+1) = 0")
    print()
    print("Therefore:")
    print("  p(1-p)/2 = 0")
    print("  p = 0 or p = 1")
    print()
    print("Finite-action endpoint filter:")
    print("  finite C1 endpoint branch requires p < 1/2")
    print("  so p = 1 is rejected")
    print()
    print("Remaining branch:")
    p = Fraction(0, 1)
    print(f"  p = {fmt(p)}")
    print()
    print("No-approximation verdict:")
    print("  ell=0 carries no angular source and gives the trivial finite branch.")
    print("  It is background/scalar collar data, not a negative-phi matter endpoint.")
    print("  The first nonconstant finite angular bridge is ell=1.")


if __name__ == "__main__":
    main()

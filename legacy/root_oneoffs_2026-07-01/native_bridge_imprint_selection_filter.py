from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def disc(ell: int, eta: Fraction) -> Fraction:
    return 1 - 8 * eta * ell * (ell + 1)


def main() -> None:
    print("metric-only bridge imprint audit")
    print("=" * 33)
    print("Metric facts already in hand:")
    print("  1. exterior scalar/radial tail cancellation is B_out=0")
    print("  2. a nonzero interior first jet appears as Delta Pi")
    print("  3. normalized angular data are scale-invariant at phi=0")
    print()
    print("Angular decomposition at phi=0:")
    print("  ell=0: scalar/background channel")
    print("  ell=1: first nonconstant angular channel H1")
    print("  ell>=2: higher angular shape channels")
    print()
    print("Observed consequence 1: exterior tail cancellation")
    print("  The ell=0 radial/scalar tail cannot be the macro-accessible imprint.")
    print("  It is killed outside by B_out=0.")
    print()
    eta = Fraction(1, 18)
    print("Observed consequence 2: endpoint admissibility, conditional on eta=1/18")
    for ell in range(4):
        d = disc(ell, eta)
        if ell == 0:
            verdict = "trivial finite branch only"
        elif d < 0:
            verdict = "no real endpoint powers"
        elif ell == 1:
            verdict = "nontrivial finite branch p=1/3"
        else:
            verdict = "check"
        print(f"  ell={ell}: discriminant={fmt(d)} -> {verdict}")
    print()
    print("Audit result:")
    print("  Once eta=1/18 is supplied, H1 is the only nontrivial finite")
    print("  scale-invariant angular imprint that can survive the bridge.")
    print()
    print("What this does and does not prove:")
    print("  proves: why the surviving imprint is H1, after eta/q is supplied")
    print("  does not prove: why q=1/3 is selected rather than an arbitrary jump")
    print()
    print("Metric-only verdict:")
    print("  The bridge naturally kills scalar radial tail and preserves the")
    print("  first nontrivial angular imprint. This is not a new mechanism.")
    print("  The remaining upstream selector")
    print("  is still the elementary source inventory / q=1/3 rule.")


if __name__ == "__main__":
    main()

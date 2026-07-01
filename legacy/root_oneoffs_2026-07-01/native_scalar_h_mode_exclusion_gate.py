from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("scalar h-mode exclusion gate")
    print("=" * 29)
    print("Write the finite-cell interior as:")
    print("  f(r) = (R/r)^p h(r)")
    print("  h(R) = 1")
    print()
    print("Then the phi0 slope is:")
    print("  q = -R f'(R)/f(R)")
    print("    = p - d ln h / d ln r |R")
    print("    = p + delta_h")
    print()
    print("Exact interpretation:")
    print("  delta_h is the independent scalar radial boundary-layer Cauchy datum.")
    print("  It is not part of the H1 area-form carrier.")
    print()

    print("Elementary H1 bridge reading:")
    print("  scalar-tail cancellation removes the scalar/radial imprint channel.")
    print("  Lambda^3 H1 supplies the angular area-form carrier.")
    print("  If the elementary phi0 projector admits only this H1 carrier plus")
    print("  the value normalization f=1, then delta_h=0.")
    print()

    p = Fraction(1, 3)
    q = p
    print("If delta_h=0:")
    print(f"  q=p={fmt(q)}")
    print(f"  Delta Pi/R=q/2={fmt(q / 2)}")
    print(f"  eta=q/6={fmt(q / 6)}")
    print(f"  eta/2={fmt(q / 12)}")
    print()

    print("If delta_h is allowed:")
    print("  q=p+delta_h")
    print("  the angular endpoint equation gives only a compatibility range")
    print("  and q is not selected.")
    print()

    print("Gate verdict:")
    print("  p=q is equivalent to excluding the scalar h boundary-layer mode.")
    print("  The H1 area-form result gives a concrete reason to try this:")
    print("    the elementary bridge has a canonical angular carrier but no")
    print("    canonical independent scalar h carrier.")
    print("  This is the current best no-new-mechanism route to the one-graph")
    print("  Calderon condition.")


if __name__ == "__main__":
    main()

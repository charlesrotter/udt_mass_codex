from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("collar Hodge carrier audit")
    print("=" * 27)
    print("Topological collar:")
    print("  M = I x S2")
    print()
    print("De Rham carrier inventory:")
    print("  H^0(M) = R")
    print("  H^1(M) = 0")
    print("  H^2(M) = R [omega_S2]")
    print("  H^3(M) = 0  for the interval collar with boundary")
    print()
    print("Metric angular carrier:")
    print("  Lambda^3 H1 pulls back to omega_S2.")
    print("  This is the unique harmonic/cohomological angular 2-form carrier.")
    print()
    print("Radial transgression:")
    print("  d ln f wedge omega_S2 = d(ln f omega_S2)")
    print("  It is exact on the collar and contributes through boundaries.")
    print()
    print("Split f into endpoint profile and h-mode:")
    print("  ln f = p ln(R/r) + ln h")
    print("  h(R)=1")
    print()
    print("Then:")
    print("  d ln f wedge omega")
    print("    = -p d ln r wedge omega + d ln h wedge omega")
    print("    = d[p ln(R/r) omega] + d[ln h omega]")
    print()
    print("At phi0:")
    print("  ln h(R)=0")
    print("  so the h transgression has no phi0 value contribution.")
    print("  Its effect is a derivative/Cauchy residual, not a new harmonic")
    print("  angular carrier.")
    print()

    q = Fraction(1, 3)
    print("If the elementary projector keeps only:")
    print("  value normalization f=1")
    print("  the H1 harmonic area-form carrier")
    print("  no extra exact scalar boundary residual")
    print("then:")
    print("  h is quotiented/excluded")
    print(f"  q=p={fmt(q)}")
    print()

    print("No-overclaim verdict:")
    print("  Hodge inventory supports excluding h from the elementary carrier")
    print("  space, because h is an exact scalar boundary residual.")
    print("  It does not by itself prove the Calderon projector performs that")
    print("  quotient. The remaining proof is a boundary-domain statement.")


if __name__ == "__main__":
    main()

from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("harmonic domain projection audit")
    print("=" * 34)
    print("Hodge-Morrey style carrier split on I x S2:")
    print("  harmonic carrier: omega_S2")
    print("  exact residual:   d(y omega_S2)")
    print("  y = ln h")
    print()
    print("Boundary values:")
    print("  y(phi0)=0 because h(phi0)=1")
    print("  if the endpoint profile normalization absorbs h at the inner end,")
    print("  the elementary residual has y(endpoint)=0 as well")
    print()
    print("Then:")
    print("  integral_{I x S2} d(y omega_S2)")
    print("    = 4 pi [y]_{endpoint}^{phi0}")
    print("    = 0")
    print()
    print("So a two-boundary relative exact h residual carries:")
    print("  no harmonic/cohomological charge")
    print("  no phi0 value trace")
    print("  only derivative/Cauchy data")
    print()
    print("A harmonic representative projector would therefore:")
    print("  keep omega_S2")
    print("  kill d(y omega_S2)")
    print()

    q = Fraction(1, 3)
    print("If the elementary phi0 domain is this harmonic representative domain:")
    print("  delta_h=0")
    print(f"  q=p={fmt(q)}")
    print(f"  eta=q/6={fmt(q / 6)}")
    print()
    print("If the domain is larger:")
    print("  exact relative h residuals are allowed")
    print("  q is not fixed by the H1 carrier alone")
    print()
    print("Projection verdict:")
    print("  The harmonic-domain projection is a natural current-facts candidate")
    print("  for the elementary phi0 projector.")
    print("  It is not a bulk mechanism and not an SM import.")
    print("  Remaining derivation: show UDT mass emergence uses the harmonic")
    print("  representative domain rather than the full relative Cauchy domain.")


if __name__ == "__main__":
    main()

from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("postulate ledger after mixed Hodge")
    print("=" * 36)
    print("No longer independent:")
    print("  eta/2")
    print("    derived as H1-projected on-shell C1 action at q=1/3")
    print("  endpoint self-similarity")
    print("    derived from H1 endpoint compatibility plus p=q")
    print("  rank-one angular carrier")
    print("    supplied by Lambda^3 H1 -> dOmega_S2")
    print("  h exclusion within elementary harmonic sector")
    print("    follows from relative harmonic 0-form energy identity")
    print()
    print("Remaining minimal domain premise:")
    print("  P_domain:")
    print("    elementary phi0 mass emergence uses the mixed Hodge harmonic")
    print("    representative projector on I x S2")
    print()
    print("What P_domain means:")
    print("  keep absolute harmonic H1 angular area carrier")
    print("  kill relative exact scalar h residuals")
    print()

    q = Fraction(1, 3)
    print("If P_domain holds:")
    print(f"  h=1")
    print(f"  delta_h=0")
    print(f"  q=p={fmt(q)}")
    print(f"  s={fmt(q * (1 - q) / 2)}")
    print(f"  Delta Pi/R={fmt(q / 2)}")
    print(f"  eta={fmt(q / 6)}")
    print(f"  eta/2={fmt(q / 12)}")
    print()
    print("Still outside this pre-spectrum closure:")
    print("  electron mass scale anchor")
    print("  full spectrum/depth/typed coefficient construction")
    print()
    print("Verdict:")
    print("  The remaining pre-spectrum postulate has been compressed to one")
    print("  boundary-domain identification, P_domain.")
    print("  Everything else in the elementary branch follows from metric/H1/C1")
    print("  identities once P_domain is accepted or derived.")


if __name__ == "__main__":
    main()

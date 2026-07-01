from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("endpoint self-similarity after H1 domain")
    print("=" * 43)
    print("Use current facts:")
    print("  H1 area-form carrier gives N=3")
    print("  H1 eigenvalue lambda=2")
    print("  H1 projected boundary scale eta=(q/2)/N")
    print("  harmonic-domain projector kills h, so p=q")
    print()

    n = Fraction(3)
    lam = Fraction(2)
    print("Endpoint compatibility:")
    print("  p(1-p)/2 = eta lambda")
    print("  eta=(q/2)/N")
    print(f"  lambda={fmt(lam)}")
    print("so:")
    print("  p(1-p)/2 = q/N")
    print()
    print("One-graph condition:")
    print("  p=q")
    print()
    print("Nontrivial branch:")
    print("  p(1-p)/2 = p/N")
    print("  (1-p)/2 = 1/N")
    print("  p = 1 - 2/N")
    p = Fraction(1) - Fraction(2, 1) / n
    print(f"  with N={fmt(n)}: p={fmt(p)}")
    print()

    rem = 1 - 2 * p
    eta = (p / 2) / n
    c1_projected = (p * p / (4 * (1 - 2 * p))) / n
    print("Consequences:")
    print(f"  q=p={fmt(p)}")
    print(f"  finite-action remainder exponent 1-2p={fmt(rem)}")
    print(f"  endpoint profile exponent p={fmt(p)}")
    print(f"  endpoint self-similarity 1-2p=p: {rem == p}")
    print(f"  eta=(q/2)/N={fmt(eta)}")
    print(f"  projected C1 action={fmt(c1_projected)}")
    print(f"  eta/2={fmt(eta / 2)}")
    print()
    print("Verdict:")
    print("  Endpoint self-similarity is not an independent postulate if the")
    print("  harmonic H1 domain projector is accepted or derived.")
    print("  It follows from H1 endpoint compatibility plus the one-graph")
    print("  condition p=q.")
    print("  If the harmonic-domain projector is not accepted, endpoint")
    print("  self-similarity can remain a fallback closure principle.")


if __name__ == "__main__":
    main()

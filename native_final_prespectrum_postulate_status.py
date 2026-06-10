from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("final pre-spectrum postulate status")
    print("=" * 36)
    print("Derived in the current frame:")
    print("  H1 area-form carrier: Lambda^3 H1 -> dOmega_S2")
    print("  rank-one angular carrier: H1, N=3")
    print("  h exclusion inside elementary branch: Dirichlet principle")
    print("  p=q: because delta_h=0 in least-action branch")
    print("  p=q=1/3: H1 one-graph compatibility")
    print("  eta=1/18: H1-projected C1 momentum")
    print("  eta/2=1/36: H1-projected on-shell C1 action")
    print("  endpoint self-similarity: consequence of N=3 one-graph branch")
    print()
    print("Remaining domain statement:")
    print("  The pre-spectrum elementary branch is the least-action mixed-Hodge")
    print("  harmonic carrier branch on I x S2.")
    print()
    print("This means:")
    print("  keep absolute harmonic H1 area carrier")
    print("  quotient/omit positive relative scalar h excitations")
    print()
    print("Not claimed:")
    print("  h modes cannot exist")
    print("  all spectrum/depth coefficients are derived")
    print("  the electron mass scale is derived")
    print()

    q = Fraction(1, 3)
    print("Elementary branch output:")
    print(f"  q={fmt(q)}")
    print(f"  s={fmt(q * (1 - q) / 2)}")
    print(f"  Delta Pi/R={fmt(q / 2)}")
    print(f"  eta={fmt(q / 6)}")
    print(f"  eta/2={fmt(q / 12)}")
    print()
    print("Verdict:")
    print("  For the pre-spectrum elementary branch, the old q/eta/eta-half")
    print("  postulates have collapsed into one boundary-domain definition.")
    print("  The next stage is spectrum construction, where positive relative")
    print("  scalar/typed modes may re-enter as excitations rather than as the")
    print("  elementary ground branch.")


if __name__ == "__main__":
    main()

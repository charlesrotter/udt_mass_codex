from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("H1 Cauchy graph merge gate")
    print("=" * 29)
    print("Newly derived angular carrier:")
    print("  Lambda^3 H1 pulls back to the S2 area form.")
    print("  Therefore H1 supplies the canonical rank-one angular projector.")
    print("  For H1, N=3 and lambda=2.")
    print()

    print("Cauchy graph variable at phi0:")
    print("  kappa[u] = -R u'(R)/u(R)")
    print("  endpoint/collar graph value for angular profile: p")
    print("  C1 collar graph value for f: q")
    print()

    n = Fraction(3, 1)
    lam = Fraction(2, 1)
    print("H1 projected boundary scale:")
    print("  eta = (q/2)/N")
    print(f"  with N={fmt(n)}: eta = q/6")
    print()

    print("Angular endpoint compatibility:")
    print("  p(1-p)/2 = eta lambda")
    print("  eta=(q/2)/N, lambda=2")
    print("  p(1-p)/2 = q/N")
    print()

    print("Alternative A: one self-similar Cauchy graph")
    print("  p=q")
    print("  q(1-q)/2 = q/N")
    print("  q=0 or q=1-2/N")
    q = Fraction(1, 1) - Fraction(2, 1) / n
    eta = q / (2 * n)
    print(f"  for N=3: q={fmt(q)}")
    print(f"  eta={fmt(eta)}")
    print(f"  eta/2={fmt(eta / 2)}")
    print()

    print("Alternative B: split boundary-layer graph")
    print("  p and q are independent Cauchy eigenvalues")
    print("  p(1-p)/2 = q/N")
    print("  q is not selected without another boundary condition")
    print()

    print("Merge verdict:")
    print("  The H1 area-form result solves the angular-projector side.")
    print("  It does not by itself prove the one-graph condition p=q.")
    print("  The remaining proof is exactly the Calderon uniqueness problem:")
    print("    phi0 must admit one self-similar Cauchy graph for elementary")
    print("    mass emergence, excluding an independent h/boundary-layer mode.")


if __name__ == "__main__":
    main()

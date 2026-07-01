from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def finite_action(q: Fraction) -> bool:
    return Fraction(0, 1) < q < Fraction(1, 2)


def main() -> None:
    print("projector-rank activation audit")
    print("=" * 33)
    print("A trace-normalized angular projector gives:")
    print("  normalized share = rank(P)/N = m/N")
    print()
    print("If the collar source is radial share times projected angular share:")
    print("  s(q,N,m) = q m/N")
    print()
    print("Then:")
    print("  dq/dt = q^2 - q + 2q m/N")
    print("        = q(q - (1 - 2m/N))")
    print()
    print("Nonzero branch:")
    print("  q_(N,m) = 1 - 2m/N = (N - 2m)/N")
    print()

    print("Odd S2 dimensions with admissible projector ranks:")
    for ell in range(1, 6):
        n = 2 * ell + 1
        print(f"  ell={ell}, N={n}")
        for m in range(1, n + 1):
            q = Fraction(n - 2 * m, n)
            if q <= 0:
                continue
            status = "finite" if finite_action(q) else "not finite"
            marker = "rank-one law" if m == 1 else "higher-rank law"
            print(f"    m={m}: q={fmt(q)}, {status}, {marker}")

    print()
    print("Rank-one consequence:")
    print("  m=1 gives q=(N-2)/N.")
    print("  finite C1 action then allows only N=3 on the non-scalar S2 ladder.")
    print()
    print("Higher-rank warning:")
    print("  if m is freely selectable, additional finite branches appear.")
    print("  example: N=5, m=2 gives q=1/5.")
    print()
    print("Gate verdict:")
    print("  The source law s(q,N)=q/N is equivalent to a rank-one angular")
    print("  activation law, not merely to angular projection in general.")
    print("  Therefore the missing metric statement is sharper:")
    print("    the phi0 collar activates a canonical rank-one angular projector.")
    print("  The N=3 Lambda^3 uniqueness is a candidate reason for that rank-one")
    print("  activation, but arbitrary higher-rank activation must be excluded.")


if __name__ == "__main__":
    main()

from fractions import Fraction


def matmul(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def fmt_matrix(matrix: list[list[Fraction]]) -> str:
    return "[" + "; ".join(", ".join(fmt(x) for x in row) for row in matrix) + "]"


def main() -> None:
    print("elementary phi0 projector candidate")
    print("=" * 37)
    print("Use current post-H1 carrier basis:")
    print("  e0 = value normalization f(phi0)=1")
    print("  e1 = self-similar endpoint/Cauchy exponent p")
    print("  e2 = exact scalar boundary residual delta_h")
    print("  e3 = H1 harmonic area-form carrier")
    print()
    print("Candidate elementary projector:")
    print("  keep e0")
    print("  keep e1")
    print("  kill e2")
    print("  keep e3")
    print()

    projector = [
        [Fraction(1), Fraction(0), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(0), Fraction(1)],
    ]
    squared = matmul(projector, projector)
    print(f"  P      = {fmt_matrix(projector)}")
    print(f"  P^2    = {fmt_matrix(squared)}")
    print(f"  P^2=P  = {squared == projector}")
    print()

    n = Fraction(3)
    print("Under this projector:")
    print("  delta_h=0")
    print("  q=p")
    print("  eta=(q/2)/N")
    print(f"  N={fmt(n)} from H1 area-form carrier")
    print()

    q = Fraction(1, 3)
    print("H1 compatibility on the one graph:")
    print("  q(1-q)/2 = q/N")
    print("  q=0 or q=1-2/N")
    print(f"  nontrivial q={fmt(q)}")
    print(f"  eta={fmt(q / (2 * n))}")
    print(f"  eta/2={fmt(q / (4 * n))}")
    print()

    print("No-overclaim verdict:")
    print("  This is an exact idempotent candidate for the elementary phi0")
    print("  projector after the H1 area-form discovery.")
    print("  It is a proof only if the UDT boundary domain is shown to use")
    print("  this harmonic-carrier quotient, killing the exact scalar residual.")


if __name__ == "__main__":
    main()

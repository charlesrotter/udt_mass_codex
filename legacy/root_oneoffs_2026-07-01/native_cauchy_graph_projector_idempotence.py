from fractions import Fraction


def matmul(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    rows = len(a)
    cols = len(b[0])
    inner = len(b)
    return [
        [sum(a[i][k] * b[k][j] for k in range(inner)) for j in range(cols)]
        for i in range(rows)
    ]


def fmt_matrix(m: list[list[Fraction]]) -> str:
    def fmt(x: Fraction) -> str:
        if x.denominator == 1:
            return str(x.numerator)
        return f"{x.numerator}/{x.denominator}"

    return "[" + "; ".join(", ".join(fmt(x) for x in row) for row in m) + "]"


def main() -> None:
    print("Cauchy graph projector idempotence")
    print("=" * 36)
    lam = Fraction(1, 36)
    print("For a one-mode boundary graph p = lambda u, use the Dirichlet-fiber")
    print("projection from arbitrary Cauchy data (u,p) to admissible data:")
    print("  P_lambda(u,p) = (u, lambda u)")
    print()
    p = [[Fraction(1), Fraction(0)], [lam, Fraction(0)]]
    p2 = matmul(p, p)
    print(f"  lambda = {lam}")
    print(f"  P      = {fmt_matrix(p)}")
    print(f"  P^2    = {fmt_matrix(p2)}")
    print(f"  P^2=P  = {p2 == p}")
    print()
    print("For H1, lambda acts as lambda I3, so this graph projector is copied")
    print("on each of the three H1 boundary labels.")
    print()
    print("Projector verdict:")
    print("  A Cauchy projector is not mysterious at the block level: it is the")
    print("  graph of the metric's DtN/action relation. The unresolved issue is")
    print("  which lambda is physical: intrinsic eta/2, warped DtN dressing, or")
    print("  a constrained two-sided combination.")


if __name__ == "__main__":
    main()

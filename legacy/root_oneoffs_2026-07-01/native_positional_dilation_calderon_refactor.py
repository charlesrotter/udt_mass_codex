from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def graph_projector(kappa: Fraction) -> list[list[Fraction]]:
    return [[Fraction(1), Fraction(0)], [kappa, Fraction(0)]]


def matmul(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def fmt_matrix(matrix: list[list[Fraction]]) -> str:
    return "[" + "; ".join(", ".join(fmt(x) for x in row) for row in matrix) + "]"


def main() -> None:
    print("positional-dilation Calderon refactor")
    print("=" * 41)
    print("GR/PDE atlas object:")
    print("  Calderon projector = projection onto Cauchy data that are traces")
    print("  of valid bulk solutions.")
    print()
    print("UDT boundary variable at phi0:")
    print("  f = exp(-2 phi)")
    print("  f(phi0) = 1")
    print("  spatial normal derivative: d/d rho = sqrt(f) d/dr")
    print("  at phi0: d/d rho = d/dr")
    print()
    print("Scale-normalized Cauchy eigenvalue:")
    print("  kappa[u] = -R (d u/d rho) / u")
    print("  at phi0: kappa[u] = -R u'(R)/u(R)")
    print()
    print("For a homogeneous collar trace u=(R/r)^p:")
    print("  kappa[u] = p")
    print()
    print("For the C1 collar field f with f(R)=1:")
    print("  q = -R f'(R)/f(R)")
    print("  therefore kappa[f] = q")
    print()
    print("Graph projector for one scale eigenvalue kappa:")
    print("  P_kappa(u, m) = (u, kappa u)")
    kappa = Fraction(1, 3)
    p = graph_projector(kappa)
    p2 = matmul(p, p)
    print(f"  P_1/3 = {fmt_matrix(p)}")
    print(f"  P_1/3^2 = {fmt_matrix(p2)}")
    print(f"  idempotent = {p2 == p}")
    print()
    print("Projector-identification condition:")
    print("  If phi0 is one shared self-similar Cauchy graph, then")
    print("  angular endpoint kappa = p and C1 collar kappa = q are the same")
    print("  graph eigenvalue.")
    print("  Hence p=q.")
    print()
    print("H1 compatibility then gives:")
    print("  p(1-p)/2 = eta*2")
    print("  eta = q/6")
    print("  p=q")
    print("  q(1-q)/2 = q/3")
    print("  q = 0 or q = 1/3")
    print()
    q = Fraction(1, 3)
    eta = q / 6
    print("Nontrivial branch:")
    print(f"  q = {fmt(q)}")
    print(f"  eta = {fmt(eta)}")
    print(f"  side action eta/2 = {fmt(eta / 2)}")
    print()
    print("Proof-status verdict:")
    print("  The GR Calderon machinery, after positional-dilation refactor,")
    print("  explains exactly what must be proven: phi0 must be a single")
    print("  self-similar Cauchy graph. If that is true, p=q is not an extra")
    print("  postulate; it is the graph identity of the transformed projector.")
    print("  The remaining hard proof is excluding a non-self-similar phi0")
    print("  boundary layer with independent p and q.")


if __name__ == "__main__":
    main()

from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("phi0 variation variable ledger")
    print("=" * 32)
    print("Boundary variables:")
    print("  F = f(phi0)")
    print("  q = -R f'(R)/F")
    print("  n_a = H1/projective unit direction on S2")
    print("  P_H1 = projector onto the ell=1 triplet")
    print()
    print("C1 boundary momentum:")
    print("  Pi_F = (1/2) R^2 f'(R)")
    print("  scale-normalized at F=1: -Pi_F/R = q/2")
    print()
    print("A local boundary functional near F=1 has:")
    print("  S_b(F,n) = S_0[n] + S_1[n](F-1) + O((F-1)^2)")
    print()
    print("Momentum closure fixes:")
    print("  S_1 = q/2")
    print("or with H1 direction resolution:")
    print("  S_1,ab = (q/2) n_a n_b")
    print()
    print("Round-S2 averaging gives:")
    print("  <S_1,ab> = (q/6) delta_ab")
    print()
    q = Fraction(1, 3)
    print("For q=1/3:")
    print(f"  q/2 = {fmt(q / 2)}")
    print(f"  q/6 = {fmt(q / 6)}")
    print()
    print("What this ledger fixes:")
    print("  the scalar edge momentum scale")
    print("  the H1/S2 isotropic projection scale")
    print()
    print("What it does not fix:")
    print("  S_0[n], the value/action term")
    print("  whether q is forced to 1/3")
    print("  whether delta_h=0")
    print("  whether the transfer operation is a trace, average, or determinant")


if __name__ == "__main__":
    main()

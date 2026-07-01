from fractions import Fraction


def fmt(value: Fraction | None) -> str:
    if value is None:
        return "none"
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def discriminant(ell: int, eta: Fraction) -> Fraction:
    lam = ell * (ell + 1)
    # p(1-p)/2 = eta lambda -> p^2 - p + 2 eta lambda = 0
    return 1 - 8 * eta * lam


def roots(ell: int, eta: Fraction) -> tuple[Fraction, Fraction] | None:
    disc = discriminant(ell, eta)
    if disc < 0:
        return None
    # For eta=1/18 and low ell, the discriminants are perfect rational squares.
    if disc == 1:
        root = Fraction(1)
    elif disc == Fraction(1, 9):
        root = Fraction(1, 3)
    elif disc == Fraction(0):
        root = Fraction(0)
    else:
        return None
    return ((1 - root) / 2, (1 + root) / 2)


def main() -> None:
    print("H1 projector admissibility spectrum")
    print("=" * 38)
    eta = Fraction(1, 18)
    print("Endpoint equation:")
    print("  p(1-p)/2 = eta ell(ell+1)")
    print(f"  eta = {fmt(eta)}")
    print()
    print("Real endpoint powers require:")
    print("  1 - 8 eta ell(ell+1) >= 0")
    print("  ell(ell+1) <= 1/(8 eta) = 9/4")
    print()
    print("ell  lambda  discriminant  roots        finite nontrivial?")
    for ell in range(0, 6):
        lam = ell * (ell + 1)
        disc = discriminant(ell, eta)
        rs = roots(ell, eta)
        if rs is None:
            root_text = "none"
            finite = "no"
        else:
            root_text = f"{fmt(rs[0])}, {fmt(rs[1])}"
            finite_roots = [r for r in rs if 0 < r < Fraction(1, 2)]
            finite = "yes" if finite_roots else "no"
        print(f"{ell:>3}  {lam:>6}  {fmt(disc):>12}  {root_text:<12} {finite}")
    print()
    print("Selector verdict:")
    print("  ell=0 gives only the trivial finite root p=0.")
    print("  ell=1 gives the only nontrivial finite root p=1/3.")
    print("  ell>=2 has no real endpoint power at eta=1/18.")
    print("  Therefore the admissible nontrivial angular Cauchy projector is P_H1.")


if __name__ == "__main__":
    main()

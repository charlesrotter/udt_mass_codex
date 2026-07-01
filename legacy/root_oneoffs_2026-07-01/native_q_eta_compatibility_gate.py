from fractions import Fraction


def fmt(value: Fraction | tuple[Fraction, Fraction] | None) -> str:
    if value is None:
        return "none"
    if isinstance(value, tuple):
        return f"{fmt(value[0])}, {fmt(value[1])}"
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def c1_action_h1(q: Fraction) -> Fraction:
    return q * q / (12 * (1 - 2 * q))


def eta_from_q(q: Fraction) -> Fraction:
    return q / 6


def h1_endpoint_roots(q: Fraction) -> tuple[Fraction, Fraction] | None:
    eta = eta_from_q(q)
    # H1 has lambda=2, so p(1-p)/2 = 2 eta = q/3.
    disc = 1 - Fraction(8, 3) * q
    if disc < 0:
        return None
    if disc == Fraction(1, 9):
        sqrt_disc = Fraction(1, 3)
    elif disc == 1:
        sqrt_disc = Fraction(1)
    elif disc == 0:
        sqrt_disc = Fraction(0)
    else:
        return None
    return ((1 - sqrt_disc) / 2, (1 + sqrt_disc) / 2)


def main() -> None:
    print("q/eta compatibility gate")
    print("=" * 26)
    print("Metric inputs:")
    print("  eta = q/6 from C1 boundary momentum plus H1/S2 projection")
    print("  H1 endpoint equation: p(1-p)/2 = eta * 2 = q/3")
    print("  H1 projected C1 action: A_H1(q) = q^2/[12(1-2q)]")
    print()
    print("H1-only admissibility window as a function of q:")
    print("  ell=1 real: 1 - (8/3)q >= 0 -> q <= 3/8")
    print("  ell=2 rejected: 1 - 8q < 0 -> q > 1/8")
    print("  nontrivial H1-only window: 1/8 < q <= 3/8")
    print()
    print("Compatibility equation 1: self-similar endpoint Cauchy datum")
    print("  p = q")
    print("  q(1-q)/2 = q/3")
    print("  q = 0 or q = 1/3")
    print()
    print("Compatibility equation 2: projected C1 action equals side action")
    print("  A_H1(q) = eta/2")
    print("  q^2/[12(1-2q)] = q/12")
    print("  q = 0 or q = 1/3")
    print()
    q = Fraction(1, 3)
    eta = eta_from_q(q)
    roots = h1_endpoint_roots(q)
    print("Nontrivial branch:")
    print(f"  q = {fmt(q)}")
    print(f"  eta = {fmt(eta)}")
    print(f"  H1 endpoint roots = {fmt(roots)}")
    print(f"  finite root p = {fmt(roots[0] if roots else None)}")
    print(f"  A_H1(q) = {fmt(c1_action_h1(q))}")
    print(f"  eta/2 = {fmt(eta / 2)}")
    print(f"  q is inside H1-only window: {Fraction(1, 8) < q <= Fraction(3, 8)}")
    print()
    print("Gate verdict:")
    print("  If the phi0 Cauchy projector identifies endpoint exponent,")
    print("  collar slope, and projected C1 side action as one self-similar")
    print("  boundary datum, then q=1/3 and eta=1/18 are forced.")
    print("  Without that exact projector identification, this remains a")
    print("  conditional compatibility theorem, not a variational derivation.")


if __name__ == "__main__":
    main()

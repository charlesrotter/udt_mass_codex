from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def admissibility_window_for_h1_only() -> tuple[Fraction, Fraction]:
    # H1 real endpoint: ell=1, lambda=2, eta=q/6.
    # discriminant = 1 - 8 eta lambda = 1 - 8(q/6)2 = 1 - 8q/3 >= 0.
    # ell=2 rejected: discriminant = 1 - 8(q/6)6 = 1 - 8q < 0.
    return Fraction(1, 8), Fraction(3, 8)


def main() -> None:
    print("projection-intersection q-constraint audit")
    print("=" * 43)
    print("Projection intersection imposes:")
    print("  f=1")
    print("  B_out=0 -> Pi_out=0")
    print("  Delta Pi/R = q/2")
    print("  angular imprint must be scale-invariant")
    print()
    print("By itself this allows any q with a corresponding interface jump:")
    for q in [Fraction(1, 6), Fraction(1, 4), Fraction(1, 3), Fraction(3, 8)]:
        print(f"  q={fmt(q)} -> Delta Pi/R={fmt(q / 2)}")
    print()
    lo, hi = admissibility_window_for_h1_only()
    print("If eta=q/6 and H1-only endpoint admissibility is imposed:")
    print(f"  ell=2 rejected requires q > {fmt(lo)}")
    print(f"  ell=1 real requires q <= {fmt(hi)}")
    print(f"  H1-only window: {fmt(lo)} < q <= {fmt(hi)}")
    print()
    print("Therefore:")
    print("  projection intersection + H1-only admissibility narrows q")
    print("  to an interval, not a point.")
    print()
    print("The point q=1/3 requires an additional exact condition:")
    print("  p=q self-similar Cauchy graph, or")
    print("  s(q)=q/3 fixed source law, or")
    print("  projected C1 side-action compatibility.")
    print()
    print("Audit verdict:")
    print("  Tail cancellation and angular imprint survival are selection")
    print("  filters, but not the q selector. The selector must be the")
    print("  elementary source inventory / self-similar Cauchy graph condition.")


if __name__ == "__main__":
    main()

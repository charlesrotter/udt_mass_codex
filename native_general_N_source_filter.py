from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def finite_action(q: Fraction) -> bool:
    return Fraction(0, 1) < q < Fraction(1, 2)


def main() -> None:
    print("general N source-filter audit")
    print("=" * 29)
    print("Test the metric-product source law:")
    print("  s(q,N) = q/N")
    print()
    print("This is not asserted as derived here.")
    print("It is the exact form obtained if the active collar source is:")
    print("  radial curvature share q times angular projection share 1/N.")
    print()
    print("q-flow:")
    print("  dq/dt = q^2 - q + 2s")
    print("        = q^2 - q + 2q/N")
    print("        = q(q - (1 - 2/N))")
    print()
    print("Nonzero branch:")
    print("  q_N = 1 - 2/N = (N-2)/N")
    print()

    print("S2 angular ladder:")
    for ell in range(0, 6):
        n = 2 * ell + 1
        q = Fraction(n - 2, n)
        s = q / n
        role = "scalar tail" if ell == 0 else "angular"
        action = "finite" if finite_action(q) else "not finite"
        matter = "eligible" if finite_action(q) and ell > 0 else "excluded"
        print(f"  ell={ell}, N={n}, role={role}")
        print(f"    q_N={fmt(q)}")
        print(f"    s=q/N={fmt(s)}")
        print(f"    C1 action: {action}")
        print(f"    matter-cell status: {matter}")

    print()
    print("Exact filter result:")
    print("  ell=0 has N=1 and q=-1: scalar/tail channel, not matter endpoint.")
    print("  ell=1 has N=3 and q=1/3: non-scalar and finite-action.")
    print("  ell>=2 has N>=5 and q>=3/5: violates p<1/2 finite-action bound.")
    print()
    print("Gate verdict:")
    print("  If s(q,N)=q/N is derived from the boundary/collar variation,")
    print("  the metric-product law selects N=3 and q=1/3 together.")
    print("  Then the remaining 3 is not inserted; it is the only S2 angular")
    print("  dimension surviving scalar-tail cancellation plus finite C1 action.")


if __name__ == "__main__":
    main()

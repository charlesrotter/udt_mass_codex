from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("current proof stack after H1")
    print("=" * 28)
    print("Derived/current facts:")
    print("  1. phi0 fixes value: f=1")
    print("  2. exterior scalar tail is killed: B_out=0")
    print("  3. interior first jet survives as Delta Pi/R=q/2")
    print("  4. ell=0 is scalar/tail, not the angular matter carrier")
    print("  5. first nonconstant S2 carrier is H1 with N=3")
    print("  6. Lambda^3 H1 pulls back to dOmega_S2")
    print("  7. H1 gives eta=(q/2)/3=q/6")
    print("  8. exact q-flow is dq/dt=q^2-q+2s(t)")
    print("  9. h residual means q=p+delta_h")
    print(" 10. nonzero delta_h is a scalar residual/split graph")
    print()

    print("Minimal boundary-domain assumption still open:")
    print("  elementary phi0 mass emergence uses the harmonic H1 carrier domain")
    print("  and quotients relative exact scalar h residuals.")
    print()

    q = Fraction(1, 3)
    print("If that domain statement holds:")
    print(f"  delta_h=0")
    print(f"  q=p={fmt(q)}")
    print(f"  s={fmt(q * (1 - q) / 2)}")
    print(f"  Delta Pi/R={fmt(q / 2)}")
    print(f"  eta={fmt(q / 6)}")
    print(f"  eta/2={fmt(q / 12)}")
    print()

    print("If that domain statement fails:")
    print("  relative scalar h modes are admitted")
    print("  q remains branch/profile dependent")
    print("  q=1/3 is conditional, not derived")
    print()

    print("Status verdict:")
    print("  The route is not merely fitting now.")
    print("  The metric has supplied a coherent harmonic-carrier branch.")
    print("  The remaining issue is the boundary domain of elementary phi0 data.")


if __name__ == "__main__":
    main()

from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("post-H1 area-form rebaseline")
    print("=" * 30)
    print("Use only current facts:")
    print()
    print("1. phi0 value normalization")
    print("   f(phi0)=1")
    print()
    print("2. exterior scalar-tail cancellation")
    print("   B_out=0, Pi_out=0")
    print()
    print("3. interior first-jet datum")
    print("   q=-R f'(R)/f(R)")
    print("   Delta Pi/R=q/2")
    print()
    print("4. H1 area-form identity")
    print("   Lambda^3 H1 pulls back to dOmega_S2")
    print("   H1 supplies the canonical rank-one angular carrier")
    print()
    print("5. H1 trace share")
    print("   N=3")
    print("   eta=(q/2)/3=q/6")
    print()
    print("6. exact q-flow")
    print("   dq/dt=q^2-q+2s(t)")
    print()
    print("7. h-mode meaning")
    print("   q=p+delta_h")
    print("   nonzero delta_h requires a scalar source residual or split graph")
    print()

    q = Fraction(1, 3)
    print("Conditional elementary closure:")
    print("  If the elementary bridge has no additional scalar source residual")
    print("  beyond the canonical H1 area-form carrier, then delta_h=0.")
    print(f"  q=p={fmt(q)}")
    print(f"  s=q(1-q)/2={fmt(q * (1 - q) / 2)}")
    print(f"  Delta Pi/R={fmt(q / 2)}")
    print(f"  eta={fmt(q / 6)}")
    print(f"  eta/2={fmt(q / 12)}")
    print()

    print("Do not use as premises without re-deriving under current facts:")
    print("  old no-extra-scale arguments")
    print("  old Dirac/Form-T spinor imports")
    print("  old bulk-potential source attempts")
    print("  old Standard Model analog labels")
    print()
    print("Current live proof obligation:")
    print("  prove the elementary phi0 bridge source inventory has no scalar")
    print("  residual beyond the H1 area-form carrier, or keep q=1/3 conditional.")


if __name__ == "__main__":
    main()

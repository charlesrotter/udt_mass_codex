from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("H1 transgression boundary audit")
    print("=" * 35)
    print("Canonical H1 collar form:")
    print("  Xi_H1 = d ln f wedge omega_H1")
    print()
    print("Since omega_H1 is the S2 area form and is closed on the collar:")
    print("  Xi_H1 = d(ln f omega_H1)")
    print()
    print("Therefore on I x S2:")
    print("  integral Xi_H1 = 4 pi [ln f]_{inner}^{phi0}")
    print()
    print("At phi0:")
    print("  f(phi0)=1")
    print("  ln f(phi0)=0")
    print()
    print("No-overclaim result:")
    print("  the pure H1 transgression is an endpoint/Cauchy object.")
    print("  It does not create an ordinary bulk Euler-Lagrange source.")
    print("  It can carry boundary Cauchy data and angular normalization.")
    print()

    q = Fraction(1, 3)
    print("If an independent Cauchy graph supplies q:")
    print(f"  q = {fmt(q)}")
    print(f"  C1 momentum scale q/2 = {fmt(q / 2)}")
    print(f"  H1 trace-normalized share q/6 = {fmt(q / 6)}")
    print()
    print("But the transgression alone does not select q.")
    print()
    print("Proof consequence:")
    print("  The H1 area-form result should be used to build the phi0")
    print("  Calderon/Cauchy boundary projector, not as a standalone bulk")
    print("  source derivation.")
    print()
    print("Remaining exact gate:")
    print("  show that the Cauchy projector graph has rank-one H1 scalar")
    print("  boundary data and fixed slope q=1/3, or keep q=1/3 conditional.")


if __name__ == "__main__":
    main()

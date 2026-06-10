from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("induced S2 measure H1 trace")
    print("=" * 31)
    print("On the phi0 boundary, the induced angular measure is the round S2 measure:")
    print("  dmu = dOmega")
    print()
    print("For the ell subspace, the projector diagonal obeys the addition theorem:")
    print("  P_ell(Omega,Omega) = sum_m |Y_ell,m(Omega)|^2")
    print("                      = (2 ell + 1)/(4 pi)")
    print()
    print("Therefore:")
    print("  Tr P_ell = integral_S2 P_ell(Omega,Omega) dOmega")
    print("          = 2 ell + 1")
    print()
    ell = 1
    trace = 2 * ell + 1
    eta = Fraction(1, 18)
    side = eta / 2
    print("For H1 / ell=1:")
    print(f"  Tr P_H1 = {trace}")
    print(f"  side action a = eta/2 = {fmt(side)}")
    print("  Tr_H1 exp(-a I3) = exp(-a) Tr P_H1")
    print("                    = 3 exp(-1/36)")
    print()
    print("Plain-sight verdict:")
    print("  The factor 3 is not an imported state count if the boundary operation")
    print("  is the induced-measure trace over the H1 projector. It is the round-S2")
    print("  boundary measure reading the ell=1 degeneracy.")


if __name__ == "__main__":
    main()

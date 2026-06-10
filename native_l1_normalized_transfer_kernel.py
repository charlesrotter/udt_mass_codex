from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("normalized ell=1 transfer-kernel candidate")
    print("=" * 47)
    eta = Fraction(1, 18)
    side = eta / 2
    coeff = eta / 4
    print("Round S2 Laplacian:")
    print("  -R^2 Delta_S2 |_{ell=1} = 2 I_3")
    print()
    print("Normalize by the ell=1 eigenvalue:")
    print("  L_1 = (-R^2 Delta_S2)/2 restricted to ell=1")
    print("  L_1 = I_3")
    print()
    print("Given banked P_phi0:")
    print(f"  eta = {fmt(eta)}")
    print()
    print("Candidate side action:")
    print("  A_side = (eta/2) L_1")
    print("         = (eta/2) I_3")
    print()
    print("Equivalently in unnormalized Laplacian form:")
    print("  A_side = (eta/4)(-R^2 Delta_S2)|_{ell=1}")
    print(f"  eta/4 = {fmt(coeff)}")
    print()
    print("Trace:")
    print("  Tr exp(-A_side) = 3 exp(-eta/2)")
    print()
    print("What this derives:")
    print("  the I_3 channel identity from the metric angular Laplacian")
    print()
    print("What remains postulated or to derive:")
    print("  the side-action coupling A_side=(eta/2)L_1")
    print("  why the transfer uses the ell=1 normalized kernel")
    print("  why independent edge nodes multiply")


if __name__ == "__main__":
    main()

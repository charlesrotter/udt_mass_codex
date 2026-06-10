from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("H1 restricted operator equivalence")
    print("=" * 38)
    eta = Fraction(1, 18)
    print("Let P_H1 project onto the ell=1 triplet.")
    print()
    print("Two different full-S2 operators become identical after H1 restriction:")
    print("  P_H1 I P_H1 = I_3")
    print("  P_H1 [(-R^2 Delta_S2)/2] P_H1 = I_3")
    print()
    print("Therefore, on the transfer space H1:")
    print("  isotropic angular surface stress and normalized L1 both act as I_3")
    print()
    print("If the H1 transfer space is independently selected, then:")
    print(f"  A_side = (eta/2) I_3 = {fmt(eta / 2)} I_3")
    print("can be supplied by an isotropic angular coupling restricted to H1.")
    print()
    print("No-approximation verdict:")
    print("  The trace over H1 cannot distinguish an intrinsic identity kernel")
    print("  from normalized L1. The real selection question moves to why the")
    print("  transfer space is exactly H1.")


if __name__ == "__main__":
    main()

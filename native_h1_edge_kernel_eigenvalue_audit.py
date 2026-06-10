from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("H1 edge-kernel eigenvalue audit")
    print("=" * 36)
    eta = Fraction(1, 18)
    print(f"Use eta = {fmt(eta)}.")
    print()
    print("Candidate A: scalar identity action")
    print("  A = (eta/2) I_3")
    print("  eigenvalues: eta/2, eta/2, eta/2")
    print("  trace exp(-A) = 3 exp(-eta/2)")
    print("  status: gives P_transfer exactly")
    print()
    print("Candidate B: rank-one direction action")
    print("  A = (eta/2) n n^T")
    print("  eigenvalues: eta/2, 0, 0")
    print("  trace exp(-A) = exp(-eta/2) + 2")
    print("  status: not P_transfer")
    print()
    print("Candidate C: normalized isotropic projector")
    print("  <n_a n_b> = delta_ab/3")
    print("  A = (eta/2) (I_3/3)")
    print("  eigenvalues: eta/6, eta/6, eta/6")
    print("  trace exp(-A) = 3 exp(-eta/6)")
    print("  status: not P_transfer")
    print()
    print("Candidate D: scalar after projection, then channel trace")
    print("  projection produces scalar eta")
    print("  independent transfer postulate assigns eta/2 to each of 3 channels")
    print("  trace exp(-A) = 3 exp(-eta/2)")
    print("  status: P_transfer, but requires a separate channel-trace rule")
    print()
    print("No-invention verdict:")
    print("  The exact H1/S2 projection alone does not derive P_transfer.")
    print("  P_transfer requires the metric edge to turn the projected scalar eta")
    print("  into an equal one-sided action on three channel states.")


if __name__ == "__main__":
    main()

from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("exact transfer identity conditions")
    print("=" * 38)
    eta = Fraction(1, 18)
    half = eta / 2
    print("Given banked P_phi0:")
    print(f"  eta = {fmt(eta)}")
    print()
    print("Exact conditional transfer identity:")
    print("  If an edge transfer node has:")
    print("    1. three exactly degenerate H1/S2 channel states, and")
    print("    2. scalar one-sided action eta/2 on each state,")
    print("  then its trace is:")
    print("    gamma = Tr_H1 exp(-eta/2 I_3)")
    print("          = 3 exp(-eta/2)")
    print()
    print("For eta=1/18:")
    print(f"  eta/2 = {fmt(half)}")
    print("  gamma = 3 exp(-1/36)")
    print()
    print("What is exact here:")
    print("  the trace identity")
    print("  the no-double-counting half-boundary bookkeeping if the transfer")
    print("  kernel is one side of a glued boundary")
    print()
    print("What is not exact from P_phi0 alone:")
    print("  existence of the transfer kernel")
    print("  threefold degeneracy as transfer multiplicity")
    print("  scalar action eta/2 on all three channels")
    print("  multiplication over independent typed nodes")
    print()
    print("No-invention verdict:")
    print("  P_transfer is an exact conditional identity, not a derived UDT result.")
    print("  To derive it, the metric must supply the three-channel scalar")
    print("  one-sided edge kernel.")


if __name__ == "__main__":
    main()

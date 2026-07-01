from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("ell=1 heat-kernel semigroup audit")
    print("=" * 39)
    eta = Fraction(1, 18)
    half = eta / 2
    print("Metric angular fact:")
    print("  L1 = (-R^2 Delta_S2)/2 |_{ell=1} = I3")
    print()
    print("Define the spectral boundary kernel:")
    print("  U(t) = exp(-t L1)")
    print()
    print("Since L1=I3:")
    print("  U(t) = exp(-t) I3")
    print("  Tr U(t) = 3 exp(-t)")
    print()
    print("Exact semigroup law:")
    print("  U(t1) U(t2) = U(t1+t2)")
    print()
    print("For a two-sided split of the edge quantum:")
    print(f"  eta = {fmt(eta)}")
    print(f"  side time = eta/2 = {fmt(half)}")
    print("  U(eta/2) U(eta/2) = U(eta)")
    print()
    print("One-side trace:")
    print("  Tr U(eta/2) = 3 exp(-eta/2)")
    print()
    print("Full glued trace:")
    print("  Tr U(eta) = 3 exp(-eta)")
    print()
    print("Exact result:")
    print("  Spectral kernel math supplies the exponential, the trace, and the")
    print("  two-sided composition law once L1 and the time parameter are given.")
    print()
    print("Remaining UDT condition:")
    print("  Identify the phi0 edge action time with eta, or side time with eta/2.")


if __name__ == "__main__":
    main()

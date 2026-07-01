from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("P_phi0 from H1 self-consistency")
    print("=" * 38)
    print("Endpoint equation:")
    print("  p(1-p)/2 = eta lambda")
    print()
    print("H1 bridge:")
    print("  ell = 1")
    print("  lambda = ell(ell+1) = 2")
    print()
    print("H1/S2 projected collar scale:")
    print("  eta = q/6")
    print()
    print("Self-similar edge closure:")
    print("  p = q")
    print()
    print("Substitute:")
    print("  q(1-q)/2 = (q/6) * 2")
    print("  q(1-q)/2 = q/3")
    print()
    print("Solutions:")
    print("  q = 0")
    print("  q = 1/3")
    print()
    print("Endpoint filter:")
    print("  q=0 is the trivial scalar/background branch")
    print("  q=1/3 is the first nontrivial H1 self-consistent branch")
    print()
    q = Fraction(1, 3)
    eta = q / 6
    print("Consequences:")
    print(f"  q = {fmt(q)}")
    print(f"  eta = q/6 = {fmt(eta)}")
    print()
    print("No-approximation verdict:")
    print("  P_phi0 is derived if p=q self-similar edge closure is derived.")
    print("  Otherwise this is a conditional derivation, not a replacement")
    print("  for the banked postulate.")


if __name__ == "__main__":
    main()

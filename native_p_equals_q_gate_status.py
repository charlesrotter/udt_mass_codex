from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("p=q gate status")
    print("=" * 17)
    print("Write the finite-cell interior as:")
    print("  f(r) = (R/r)^p h(r)")
    print("  h(R) = 1")
    print()
    print("Then the phi0 collar slope is:")
    print("  q_phi0 = p - d ln h / d ln r |R")
    print("         = p + delta_h")
    print()
    print("So:")
    print("  p=q_phi0 iff delta_h=0")
    print()
    print("Constant H1 source support:")
    s = Fraction(1, 9)
    print(f"  if s={fmt(s)}, radial branches are q=1/3 and q=2/3")
    print("  finite C1 action rejects q=2/3")
    print("  remaining branch has q=1/3 at every radius")
    print("  therefore delta_h=0")
    print()
    print("No-approximation verdict:")
    print("  p=q is supported if the H1 source is constant through the collar.")
    print("  The open gate is whether the native phi0 boundary layer enforces")
    print("  delta_h=0 or allows source running.")


if __name__ == "__main__":
    main()

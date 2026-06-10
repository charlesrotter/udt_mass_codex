from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def action_finite(p: Fraction) -> bool:
    return p < Fraction(1, 2)


def main() -> None:
    print("constant H1 source mode-filter audit")
    print("=" * 42)
    print("Constant-source radial equation:")
    print("  f'' + 2 f'/r + 2s f/r^2 = 0")
    print()
    print("For a power branch f ~ r^-q:")
    print("  s = q(1-q)/2")
    print()
    s = Fraction(1, 9)
    q1 = Fraction(1, 3)
    q2 = Fraction(2, 3)
    print(f"For s={fmt(s)}:")
    print(f"  q branches: {fmt(q1)}, {fmt(q2)}")
    print()
    print("General local solution:")
    print("  f(r) = A r^(-1/3) + B r^(-2/3)")
    print()
    print("C1 finite-action condition near the endpoint:")
    print("  f ~ r^-p is finite-action only if p < 1/2")
    print(f"  p=1/3 finite? {action_finite(q1)}")
    print(f"  p=2/3 finite? {action_finite(q2)}")
    print()
    print("Therefore finite C1 action sets:")
    print("  B = 0")
    print()
    print("Then:")
    print("  f(r) = A r^(-1/3)")
    print("  q(r) = -d ln f/d ln r = 1/3 at every radius")
    print("  delta_h = 0")
    print()
    print("At phi0:")
    print(f"  q_phi0 = {fmt(q1)}")
    print(f"  -Pi_f/R = q/2 = {fmt(q1 / 2)}")
    print(f"  eta = q/6 = {fmt(q1 / 6)}")
    print()
    print("No-invention verdict:")
    print("  If the phi0 collar is governed by the constant H1 source s=1/9,")
    print("  then finite C1 action removes the 2/3 companion branch and enforces")
    print("  q_phi0=p=1/3. The remaining open derivation is s=1/9 as the native")
    print("  H1 edge source.")


if __name__ == "__main__":
    main()

from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("delta_h integral gate")
    print("=" * 21)
    print("For the radial equation:")
    print("  f'' + 2 f'/r + 2 s(r) f/r^2 = 0")
    print()
    print("Use t = ln r and q(t) = -d ln f/dt.")
    print("The exact q-flow is:")
    print("  dq/dt = q^2 - q + 2 s(t)")
    print()
    print("If p is the endpoint exponent and q_phi0 is the collar slope:")
    print("  delta_h = q_phi0 - p")
    print()
    print("Therefore:")
    print("  delta_h = integral_endpoint^phi0 [q^2 - q + 2s(t)] dt")
    print()
    q = Fraction(1, 3)
    s = q * (1 - q) / 2
    print("For constant self-consistent H1 branch:")
    print(f"  q = {fmt(q)}")
    print(f"  s = q(1-q)/2 = {fmt(s)}")
    print("  dq/dt = 0")
    print("  delta_h = 0")
    print()
    print("No-approximation verdict:")
    print("  No collar renormalization is an exact integral condition on q-flow.")
    print("  A hidden metric mechanism could enforce it by making the H1 source")
    print("  constant, by cancellation in the integral, or by a boundary condition.")


if __name__ == "__main__":
    main()

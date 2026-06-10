from fractions import Fraction


def fmt(x: Fraction) -> str:
    if x.denominator == 1:
        return str(x.numerator)
    return f"{x.numerator}/{x.denominator}"


def main() -> None:
    print("Exact scale-normalized boundary momentum")
    print("=" * 42)
    print("At a collar of radius R with f(R)=1:")
    print("  q = -R f'(R)/f(R)")
    print("  f'(R) = -q/R")
    print()
    print("C1 boundary momentum:")
    print("  Pi_f = (1/2) R^2 f'(R)")
    print("       = -q R / 2")
    print()
    print("Thus Pi_f is scale-covariant, not dimensionless.")
    print("The dimensionless momentum density per collar radius is:")
    print("  pi_hat = -Pi_f / R = q/2")
    print()
    print("H1 projection uses the dimensionless collar quantity:")
    print("  eta(q) = pi_hat / 3 = q/6")
    print()
    q = Fraction(1, 3)
    pi_hat = q / 2
    eta = pi_hat / 3
    side = eta / 2
    print("For q=1/3:")
    print(f"  pi_hat = {fmt(pi_hat)}")
    print(f"  eta = {fmt(eta)}")
    print(f"  one-sided transfer = {fmt(side)}")
    print()
    print("Exact scale verdict:")
    print("  Setting R=1 is a dimensionless cell normalization.")
    print("  The invariant transfer unit is built from -Pi_f/R=q/2, not from")
    print("  the raw dimensionful/covariant Pi_f.")
    print("  This preserves scale covariance of the mass-ratio ladder.")


if __name__ == "__main__":
    main()

from fractions import Fraction
import math


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("banked P_phi0 working chain")
    print("=" * 32)
    print("Working choice:")
    print("  Bank P_phi0 as a minimal native edge postulate.")
    print()
    print("P_phi0:")
    print("  -Pi_f/R = 1/6")
    print("  equivalently K_rad/K_S2 = 1/6")
    print()

    q = Fraction(1, 3)
    s = q * (1 - q) / 2
    eta = q / 6
    one_sided = eta / 2
    gamma = 3.0 * math.exp(-float(one_sided))

    print("Exact consequences of P_phi0 plus H1/S2 projection:")
    print(f"  q = {fmt(q)}")
    print(f"  s = q(1-q)/2 = {fmt(s)}")
    print(f"  eta = q/6 = {fmt(eta)}")
    print(f"  one-sided transfer exponent = eta/2 = {fmt(one_sided)}")
    print()
    print("Transfer diagnostic, not yet derived:")
    print(f"  gamma = 3 exp(-eta/2) = {gamma:.12g}")
    print()
    print("Status ledger:")
    print("  P_phi0: banked minimal postulate")
    print("  H1/S2 projection: derived geometry")
    print("  finite-action branch filter: derived once s=1/9 is present")
    print("  gamma transfer form: diagnostic / candidate")
    print("  typed depth rule: diagnostic / candidate")
    print("  branch coefficients: diagnostic / candidate")


if __name__ == "__main__":
    main()

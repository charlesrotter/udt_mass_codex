import math
from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("H1 internal trace from gluing")
    print("=" * 32)
    dim_h1 = 3
    action = Fraction(1, 36)
    print("Let the one-side H1 transfer kernel be:")
    print("  K_ij = exp(-a) delta_ij")
    print(f"  a = eta/2 = {fmt(action)}")
    print()
    print("If an external H1 label is fixed:")
    print("  K_ii = exp(-a)")
    print()
    print("If the H1 label is internal after gluing and unobserved:")
    print("  sum_i K_ii = Tr_H1 K = 3 exp(-a)")
    print()
    print("This is an index contraction, not an average.")
    print("  normalized average would give exp(-a)")
    print("  determinant would give exp(-3a)")
    print("  trace gives 3 exp(-a)")
    print()
    trace_value = dim_h1 * math.exp(-float(action))
    print("Numerical check:")
    print(f"  Tr_H1 K = {trace_value:.12g}")
    print()
    print("Jigsaw verdict:")
    print("  Once the metric gives an identity kernel on H1 and the H1 label is")
    print("  an internal glued boundary label, trace is the natural invariant")
    print("  contraction. The remaining physics gate is whether the particle")
    print("  transfer really leaves the H1 label internal/unobserved.")


if __name__ == "__main__":
    main()

import math
from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("trace/product merge pattern")
    print("=" * 29)
    a = Fraction(1, 36)
    n = 3
    gamma = n * math.exp(-float(a))

    print("One internal H1 boundary label:")
    print("  K = exp(-a) I3")
    print(f"  a = {fmt(a)}")
    print("  Tr K = 3 exp(-a)")
    print()
    print("Two independent internal labels:")
    print("  K_total = K_1 tensor K_2")
    print("  Tr K_total = Tr(K_1) Tr(K_2)")
    print("             = gamma^2")
    print()
    print("This means trace and product are not separate mechanisms once")
    print("independent local boundary labels are established.")
    print()
    print("Checks:")
    print(f"  gamma   = {gamma:.12g}")
    print(f"  gamma^2 = {gamma ** 2:.12g}")
    print()
    print("Pattern verdict:")
    print("  The operation-level jigsaw piece is internal-label contraction.")
    print("  A single internal label gives a trace; independent local internal")
    print("  labels give tensor-product traces and therefore gamma powers.")


if __name__ == "__main__":
    main()

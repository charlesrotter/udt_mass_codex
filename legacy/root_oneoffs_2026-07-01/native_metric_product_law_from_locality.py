import math
from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("metric product law from locality")
    print("=" * 32)
    dim_h1 = 3
    action = Fraction(1, 36)
    gamma = dim_h1 * math.exp(-float(action))

    print("For one independent H1 transfer slot:")
    print("  K = exp(-a) I3")
    print(f"  a = {fmt(action)}")
    print("  Tr K = 3 exp(-a) = gamma")
    print()
    print("For n independent local slots:")
    print("  K_total = K_1 tensor K_2 tensor ... tensor K_n")
    print("  Tr K_total = product_i Tr K_i")
    print("             = gamma^n")
    print()
    for n in (5, 7):
        print(f"n={n}: gamma^n = {gamma ** n:.12g}")
    print()
    print("Jigsaw verdict:")
    print("  The metric/local-action side supplies the product law if the boundary")
    print("  slots are independent local transfer factors. It does not by itself")
    print("  derive the M1=5 or E1=7 slot counts.")


if __name__ == "__main__":
    main()

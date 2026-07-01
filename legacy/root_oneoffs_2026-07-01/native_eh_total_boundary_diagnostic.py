from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("Einstein-Hilbert total-boundary diagnostic")
    print("=" * 45)
    print("For ds^2 = -f dt^2 + f^{-1} dr^2 + r^2 dOmega^2:")
    print("  sqrt(-g) = r^2 sin(theta)")
    print("  R = -f'' - 4 f'/r + 2(1-f)/r^2")
    print()
    print("Suppressing the angular/time factors, the radial EH density is:")
    print("  L_EH = r^2 R")
    print("       = -r^2 f'' - 4 r f' + 2(1-f)")
    print()
    print("Exact total derivative identity:")
    print("  L_EH = d/dr [2 r (1-f) - r^2 f']")
    print()
    print("At phi0 with f(R)=1:")
    print("  B_EH(phi0) = -R^2 f'(R)")
    print("             = q R")
    print()
    print("Compare C1:")
    print("  Pi_f = (1/2) R^2 f'(R)")
    print("  -2 Pi_f = -R^2 f'(R) = q R")
    print("  Delta Pi_f for flat exterior = q R/2")
    print()
    q = Fraction(1, 3)
    print("For q=1/3:")
    print(f"  B_EH(phi0) = {fmt(q)} R")
    print(f"  -Pi_f = {fmt(q / 2)} R")
    print(f"  -Pi_f/R = {fmt(q / 2)}")
    print()
    print("No-invention verdict:")
    print("  In this metric sector, GR's scalar-curvature action is boundary-only.")
    print("  It identifies the same collar quantity as C1, with B_EH = -2 Pi_f.")
    print("  This is a strong map toward a missing UDT boundary/joint term, but")
    print("  not by itself permission to import the Einstein-Hilbert action.")


if __name__ == "__main__":
    main()

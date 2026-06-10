from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("phi0 Cauchy graph uniqueness gate")
    print("=" * 38)
    print("Two exact alternatives:")
    print()
    print("A. Single self-similar Cauchy graph")
    print("  angular endpoint eigenvalue p and C1 collar eigenvalue q")
    print("  are the same graph eigenvalue.")
    print("  condition: p=q")
    print("  H1 equation with eta=q/6:")
    print("    q(1-q)/2 = q/3")
    print("  branches:")
    print("    q=0")
    print("    q=1/3")
    print("  nontrivial result:")
    print("    q=1/3, eta=1/18, P_adm=P_H1")
    print()
    print("B. Split boundary-layer graph")
    print("  angular endpoint eigenvalue p and C1 collar eigenvalue q")
    print("  are independent boundary-layer data.")
    print("  H1 endpoint equation:")
    print("    p(1-p)/2 = q/3")
    print("  H1-only admissibility:")
    print("    1/8 < q <= 3/8")
    print("  result:")
    print("    q is not selected by this gate")
    print()
    print("Exact comparison at the target branch:")
    q = Fraction(1, 3)
    eta = q / 6
    print(f"  q = {fmt(q)}")
    print(f"  eta = {fmt(eta)}")
    print(f"  finite H1 root p = {fmt(q)}")
    print(f"  projected side action = {fmt(eta / 2)}")
    print()
    print("Uniqueness proof requirement:")
    print("  Show from the UDT positional-dilation boundary operator that phi0")
    print("  admits alternative A and excludes alternative B for the elementary")
    print("  mass-emergence bridge.")
    print()
    print("What would count as proof:")
    print("  1. a derived two-sided Calderon projector with one graph eigenvalue;")
    print("  2. a boundary/joint term whose stationarity enforces p=q; or")
    print("  3. a no-extra-scale theorem excluding independent boundary-layer data.")


if __name__ == "__main__":
    main()

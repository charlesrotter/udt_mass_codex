from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("ell=1 Poisson semigroup / DtN audit")
    print("=" * 43)
    print("Exact product-collar boundary model:")
    print("  P = -d_x^2 + L")
    print("  x >= 0 is normal distance from the boundary")
    print()
    print("For boundary data u(0)=u0 and decaying extension:")
    print("  u(x) = exp(-x sqrt(L)) u0")
    print()
    print("Dirichlet-to-Neumann map:")
    print("  -u'(0) = sqrt(L) u0")
    print()
    print("For the normalized ell=1 angular operator:")
    print("  L = L1 = I3")
    print("  sqrt(L1) = I3")
    print("  u(x) = exp(-x) u0")
    print("  Tr exp(-x sqrt(L1)) = 3 exp(-x)")
    print()
    eta = Fraction(1, 18)
    side = eta / 2
    print("If the phi0 side-length/action parameter is eta/2:")
    print(f"  x = eta/2 = {fmt(side)}")
    print("  one-side trace = 3 exp(-eta/2)")
    print()
    print("Exact theorem status:")
    print("  This is exact for the product-collar operator -d_x^2+L1.")
    print()
    print("UDT status:")
    print("  UDT must still show that the two-sided phi0 bridge is governed by")
    print("  this product-collar Poisson kernel and that x=eta/2.")


if __name__ == "__main__":
    main()

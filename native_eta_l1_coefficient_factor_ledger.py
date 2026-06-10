from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("eta-L1 coefficient factor ledger")
    print("=" * 36)
    q = Fraction(1, 3)
    boundary_momentum = q / 2
    h1_projection = boundary_momentum / 3
    one_side = h1_projection / 2
    laplacian_coeff = one_side / 2
    print("Start with banked P_phi0:")
    print(f"  q = {fmt(q)}")
    print()
    print("C1 boundary momentum unit:")
    print(f"  q/2 = {fmt(boundary_momentum)}")
    print()
    print("H1/S2 isotropic projection:")
    print(f"  eta = (q/2)/3 = q/6 = {fmt(h1_projection)}")
    print()
    print("One-sided interface split:")
    print(f"  eta/2 = q/12 = {fmt(one_side)}")
    print()
    print("Unnormalized Laplacian coefficient for L1=(-R^2 Delta)/2:")
    print(f"  eta/4 = q/24 = {fmt(laplacian_coeff)}")
    print()
    print("Thus:")
    print("  A_side = (eta/2) L1")
    print("         = (eta/4)(-R^2 Delta_S2)|_{ell=1}")
    print()
    print("No-approximation verdict:")
    print("  The desired coefficient has an exact factor ledger:")
    print("  boundary momentum x isotropic projection x side split x L1 normalization.")
    print("  The ledger is coherent, but the side split and coupling still need")
    print("  a native action argument.")


if __name__ == "__main__":
    main()

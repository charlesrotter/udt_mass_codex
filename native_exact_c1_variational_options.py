from fractions import Fraction


def fmt(x: Fraction) -> str:
    if x.denominator == 1:
        return str(x.numerator)
    return f"{x.numerator}/{x.denominator}"


def main() -> None:
    print("Exact C1 variational options at phi0")
    print("=" * 39)
    print("C1 radial action in f=e^{-2phi}:")
    print("  S_C1 = (1/4) integral r^2 f'^2 dr")
    print()
    print("Exact variation:")
    print("  delta S_C1 = bulk term + [Pi_f delta f]_boundary")
    print("  Pi_f = (1/2) r^2 f'")
    print()
    print("At phi0 with R=1, f=1, f'=-q:")
    print("  Pi_f = -q/2")
    print()
    print("Existing C1 variational choices:")
    print("  1. Dirichlet boundary:")
    print("       delta f = 0 at phi0")
    print("       nonzero Pi_f is allowed")
    print("       but f=1 is imposed as a boundary condition, not derived")
    print()
    print("  2. Natural/free boundary:")
    print("       delta f is free at phi0")
    print("       stationarity requires Pi_f = 0")
    print("       hence q = 0")
    print()
    print("  3. Added boundary functional S_b(f, ...):")
    print("       stationarity requires Pi_f + dS_b/df = 0")
    print("       nonzero q possible if dS_b/df = q/2")
    print("       but S_b is not present in bare C1 unless derived elsewhere")
    print()
    q = Fraction(1, 3)
    print("For q=1/3:")
    print(f"  Pi_f = {fmt(-q / 2)}")
    print(f"  required dS_b/df = {fmt(q / 2)}")
    print()
    print("No-invention verdict:")
    print("  Bare C1 alone gives either:")
    print("    - imposed Dirichlet phi0 boundary with nonzero momentum, or")
    print("    - natural Neumann boundary with q=0.")
    print("  It does not derive a nonzero-q phi0 closure with flat exterior.")
    print("  Therefore the phi0 boundary functional remains an open requirement")
    print("  unless found in another already-native metric/interface term.")


if __name__ == "__main__":
    main()

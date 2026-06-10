from fractions import Fraction


def fmt(x: Fraction) -> str:
    if x.denominator == 1:
        return str(x.numerator)
    return f"{x.numerator}/{x.denominator}"


def main() -> None:
    print("Exact exterior Hamilton-Jacobi no-go")
    print("=" * 39)
    print("Source-free exterior C1 problem on r in [R, infinity):")
    print("  S_ext = (1/4) integral_R^infty r^2 f'^2 dr")
    print("with boundary conditions:")
    print("  f(R)=F")
    print("  f(infinity)=1")
    print()
    print("Exact solution:")
    print("  f(r) = 1 + B/r")
    print("  B = R(F-1)")
    print()
    print("Exact on-shell action:")
    print("  S_ext(F;R) = B^2/(4R)")
    print("             = R(F-1)^2/4")
    print()
    print("Exterior boundary derivative:")
    print("  dS_ext/dF = R(F-1)/2 = B/2")
    print()
    print("Exterior canonical momentum at R:")
    print("  Pi_out = (1/2)R^2 f'(R) = -B/2")
    print("  dS_ext/dF = -Pi_out")
    print()

    r = Fraction(1, 1)
    f_flat = Fraction(1, 1)
    b_flat = r * (f_flat - 1)
    s_ext_flat = b_flat * b_flat / (4 * r)
    derivative_flat = r * (f_flat - 1) / 2
    q = Fraction(1, 3)
    needed = q / 2
    print("Flat exterior at the collar:")
    print(f"  F = {fmt(f_flat)}")
    print(f"  B = {fmt(b_flat)}")
    print(f"  S_ext = {fmt(s_ext_flat)}")
    print(f"  dS_ext/dF = {fmt(derivative_flat)}")
    print()
    print("Needed to cancel inner self-similar C1 momentum:")
    print(f"  q = {fmt(q)}")
    print(f"  -Pi_inner = q/2 = {fmt(needed)}")
    print()
    print("Exact conclusion:")
    print("  The flat exterior Hamilton-Jacobi functional has zero derivative at F=1.")
    print("  It cannot cancel a nonzero inner momentum q/2.")
    print("  Therefore the eta-producing phi0 momentum jump is not hidden in the")
    print("  smooth exterior HJ term. It requires an additional interface functional")
    print("  or an exactly derived replacement for flat exterior closure.")


if __name__ == "__main__":
    main()

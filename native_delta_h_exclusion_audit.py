from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("delta_h exclusion audit")
    print("=" * 23)
    print("General finite-cell collar factorization:")
    print("  f(r) = (R/r)^p h(r)")
    print("  h(R) = 1")
    print()
    print("phi0 slope:")
    print("  q = -d ln f / d ln r |R")
    print("    = p - d ln h / d ln r |R")
    print("    = p + delta_h")
    print()
    print("So p=q iff:")
    print("  delta_h = 0")
    print()
    print("No-extra-scale test:")
    print("  h(r) = exp[-a(r/R - 1)]")
    print("  h(R) = 1")
    print("  -d ln h / d ln r |R = a")
    print("  q = p + a")
    print()
    print("This deformation uses only the dimensionless coordinate r/R and")
    print("a dimensionless amplitude a. It introduces no new length scale.")
    print()
    print("Therefore:")
    print("  no-extra-scale alone does not prove p=q.")
    print()
    print("What must be excluded instead:")
    print("  an independent boundary-layer shape variable h with nonzero")
    print("  logarithmic derivative at phi0.")
    print()
    print("Exact ways to exclude it:")
    print("  1. derive a one-graph Calderon projector whose Cauchy data have")
    print("     no independent h direction;")
    print("  2. derive a phi0 joint/boundary stationarity equation setting")
    print("     delta_h=0;")
    print("  3. derive a constant H1 source law through the collar, making")
    print("     the finite-action branch globally self-similar.")
    print()
    p = Fraction(1, 3)
    a = Fraction(1, 20)
    print("Example split-graph branch:")
    print(f"  p = {fmt(p)}")
    print(f"  a = delta_h = {fmt(a)}")
    print(f"  q = p + a = {fmt(p + a)}")
    print("  This preserves f(R)=1 but breaks p=q.")
    print()
    print("Audit verdict:")
    print("  The next proof cannot rely on scale language alone.")
    print("  It must remove the independent h direction from the phi0")
    print("  Cauchy data, or show the native boundary variation kills it.")


if __name__ == "__main__":
    main()

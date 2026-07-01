from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("phi0 quasilocal slope-density identity")
    print("=" * 41)
    print("Metric:")
    print("  ds^2 = -f dt^2 + f^{-1} dr^2 + r^2 dOmega^2")
    print()
    print("GR atlas object for this metric form:")
    print("  m_MS(r) = r(1-f)/2")
    print()
    print("Exact derivative:")
    print("  m_MS'(r) = (1 - f - r f')/2")
    print()
    print("Spatial scalar curvature identity:")
    print("  R3 = 2(1 - f - r f')/r^2")
    print("  therefore R3 = 4 m_MS'/r^2")
    print()
    print("At a phi0 collar:")
    print("  f(R)=1")
    print("  q=-R f'(R)/f(R)=-R f'(R)")
    print("  m_MS(R)=0")
    print("  m_MS'(R)=q/2")
    print("  R3/R2=q, where R2=2/R^2")
    print()
    print("Interpretation:")
    print("  phi0 can have zero quasilocal mass value while carrying a nonzero")
    print("  quasilocal slope-density. The same q appears as spatial curvature")
    print("  fraction, C1 boundary momentum density, and Brown-York angular stress.")
    print()
    q = Fraction(1, 3)
    print("For q=1/3:")
    print(f"  m_MS'(R) = {fmt(q / 2)}")
    print(f"  R3/R2 = {fmt(q)}")
    print(f"  H1-projected boundary unit = (q/2)/3 = {fmt(q / 6)}")
    print()
    print("No-invention verdict:")
    print("  This is not a mass mechanism import.")
    print("  It is an exact metric identity showing that the collar can hide")
    print("  the value channel while exposing the slope-density channel.")


if __name__ == "__main__":
    main()

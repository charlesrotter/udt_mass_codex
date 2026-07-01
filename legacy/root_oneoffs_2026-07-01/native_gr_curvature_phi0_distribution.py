from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("GR curvature diagnostic for a phi0 slope jump")
    print("=" * 47)
    print("Metric:")
    print("  ds^2 = -f dt^2 + f^{-1} dr^2 + r^2 dOmega^2")
    print()
    print("Exact curvature identities for this metric form:")
    print("  G^t_t = G^r_r = (r f' + f - 1)/r^2")
    print("  G^theta_theta = G^phi_phi = f''/2 + f'/r")
    print("  R = -f'' - 4 f'/r + 2(1-f)/r^2")
    print()
    print("At a phi0 collar:")
    print("  f(R) = 1")
    print("  f'_in = -q/R")
    print("  f'_out = 0")
    print("  Delta f' = f'_out - f'_in = q/R")
    print()
    print("Distributional consequence:")
    print("  f'' contains (q/R) delta(r-R)")
    print("  R_singular contains -(q/R) delta(r-R)")
    print("  G^theta_theta_singular contains (q/(2R)) delta(r-R)")
    print()
    print("Compare to exact C1 interface source:")
    print("  (r^2 f')' = J")
    print("  integral J dr = R^2 Delta f' = q R")
    print("  Delta Pi_f = (1/2) integral J dr = q R/2")
    print()
    print("Curvature measure comparison:")
    print("  integral r^2 R_singular dr = -q R")
    print("  This is the same magnitude as the C1 source integral, with sign set")
    print("  by curvature and normal conventions.")
    print()
    q = Fraction(1, 3)
    print("For q=1/3:")
    print(f"  integral J dr = {fmt(q)} R")
    print(f"  Delta Pi_f = {fmt(q / 2)} R")
    print(f"  scale-normalized Delta Pi_f/R = {fmt(q / 2)}")
    print()
    print("No-invention verdict:")
    print("  GR curvature math points to the slope jump itself as a native")
    print("  distributional boundary object. This does not import Einstein sourcing,")
    print("  but it does identify an exact joint/curvature candidate that must be")
    print("  checked against the UDT action and angular projection.")


if __name__ == "__main__":
    main()

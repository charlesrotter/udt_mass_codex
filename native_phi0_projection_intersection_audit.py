from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("phi=0 projection intersection audit")
    print("=" * 37)
    print("Metric-given subconditions:")
    print()
    print("1. Value normalization:")
    print("   f(phi=0) = 1")
    print()
    print("2. Exterior tail kernel:")
    print("   source-free exterior f_out = 1 + B_out/r")
    print("   flat macro/scalar exterior imposes B_out = 0")
    print("   since Pi_out = -B_out/2, this also gives Pi_out = 0")
    print()
    print("3. Interior first-jet image:")
    print("   q = -R f'_in/f(R)")
    print("   Pi_in = -qR/2")
    print("   Delta Pi = Pi_out - Pi_in = qR/2")
    print()
    print("4. Scale-invariant angular carrier:")
    print("   normalized angular data are decomposed by -R^2 Delta_S2")
    print("   H1 is ell=1, the first nonconstant sector")
    print()
    print("Projection-intersection form:")
    print("   admissible macro-visible imprint")
    print("     = ker(B_out)")
    print("       intersect image(Delta Pi)")
    print("       restricted to scale-invariant angular boundary data")
    print()
    q = Fraction(1, 3)
    delta_pi_over_r = q / 2
    eta = delta_pi_over_r / 3
    side = eta / 2
    print("If the upstream selector supplies q=1/3:")
    print(f"   Delta Pi/R = {fmt(delta_pi_over_r)}")
    print(f"   H1 projection eta = {fmt(eta)}")
    print(f"   side value eta/2 = {fmt(side)}")
    print()
    print("What is exact without selecting q:")
    print("   tail cancellation forces Pi_out=0")
    print("   any nonzero interior q survives only as an interface jump")
    print("   angular scale-invariant data are the only non-radial bridge labels")
    print()
    print("What remains open:")
    print("   why the elementary bridge source inventory selects q=1/3")
    print("   instead of an arbitrary Delta Pi/R=q/2")
    print()
    print("Metric-only verdict:")
    print("   The metric is exposing a projection intersection, not a force:")
    print("     value normalization, radial-tail kernel, first-jet image,")
    print("     and angular scale-invariant restriction.")


if __name__ == "__main__":
    main()

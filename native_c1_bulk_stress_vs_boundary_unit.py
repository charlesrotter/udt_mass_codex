from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("C1 bulk stress vs phi0 boundary unit")
    print("=" * 41)
    print("C1 scalar Lagrangian form, suppressing the overall coupling:")
    print("  L = -1/2 e^{-2phi} (partial phi)^2")
    print("  f = e^{-2phi}")
    print("  phi' = -f'/(2f)")
    print()
    print("For a static radial field:")
    print("  e^{-2phi} g^rr phi'^2 = f * f * phi'^2 = f'^2/4")
    print()
    print("Mixed stress components, up to the common coupling:")
    print("  T^t_t = -f'^2/8")
    print("  T^r_r = +f'^2/8")
    print("  T^theta_theta = T^phi_phi = -f'^2/8")
    print()
    print("At phi0:")
    print("  f=1")
    print("  f'=-q/R")
    print("  T^theta_theta = -q^2/(8R^2)")
    print()
    print("Compare boundary unit:")
    print("  C1 boundary momentum: -Pi_f/R = q/2")
    print("  Brown-York atlas angular unit: R tau^A_A -> q/2")
    print()
    q = Fraction(1, 3)
    print("For q=1/3:")
    print(f"  C1 angular bulk stress magnitude = {fmt(q * q / 8)} / R^2")
    print(f"  boundary unit = {fmt(q / 2)}")
    print()
    print("No-invention verdict:")
    print("  The C1 bulk stress is quadratic in q.")
    print("  The eta-producing unit is linear in q.")
    print("  Therefore ordinary C1 bulk stress is not the missing eta mechanism.")
    print("  The linear object is the C1 boundary momentum / edge stress.")


if __name__ == "__main__":
    main()

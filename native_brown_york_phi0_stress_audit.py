from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("Brown-York phi0 boundary-stress audit")
    print("=" * 43)
    print("Metric:")
    print("  ds^2 = -f dt^2 + f^{-1} dr^2 + r^2 dOmega^2")
    print()
    print("For the timelike r=R boundary:")
    print("  K^t_t = f'/(2 sqrt(f))")
    print("  K^theta_theta = K^phi_phi = sqrt(f)/R")
    print("  K = f'/(2 sqrt(f)) + 2 sqrt(f)/R")
    print()
    print("Trace-reversed boundary curvature:")
    print("  K^a_b - K delta^a_b")
    print("    t component      = -2 sqrt(f)/R")
    print("    angular component = -f'/(2 sqrt(f)) - sqrt(f)/R")
    print()
    print("Flat reference subtraction:")
    print("  reference t component      = -2/R")
    print("  reference angular component = -1/R")
    print()
    print("Subtracted Brown-York-type stress structure:")
    print("  tau^t_t        proportional to 2(1 - sqrt(f))/R")
    print("  tau^A_A        proportional to -f'/(2 sqrt(f)) + (1 - sqrt(f))/R")
    print()
    print("At phi0:")
    print("  f=1")
    print("  f'=-q/R")
    print("  tau^t_t = 0")
    print("  tau^A_A proportional to q/(2R)")
    print()
    print("Dimensionless angular stress unit:")
    print("  R tau^A_A -> q/2")
    print()
    q = Fraction(1, 3)
    print("For q=1/3:")
    print(f"  R tau^A_A -> {fmt(q / 2)}")
    print(f"  H1/S2 projected eta = (q/2)/3 = {fmt(q / 6)}")
    print()
    print("No-invention verdict:")
    print("  Brown-York stress separates value from variation.")
    print("  The phi0 boundary can have zero subtracted quasilocal energy at f=1")
    print("  while retaining an angular boundary stress proportional to q/2.")
    print("  This matches the already found angular-only shell signature.")
    print()
    print("Guardrail:")
    print("  This is a GR boundary-stress map, not a UDT derivation yet.")
    print("  The native task is to derive the same angular boundary stress from")
    print("  the UDT C1/angular variational structure.")


if __name__ == "__main__":
    main()

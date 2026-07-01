from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("relative residual spectrum audit")
    print("=" * 32)
    print("Let y=ln h be a scalar residual on a finite collar interval.")
    print("For the elementary normalization:")
    print("  y(endpoint)=0")
    print("  y(phi0)=0")
    print()
    print("The scalar relative/Dirichlet interval spectrum has modes:")
    print("  y_n(t) = sin(n pi t/L), n=1,2,...")
    print("with eigenvalues:")
    print("  (n pi/L)^2 > 0")
    print()
    print("Therefore:")
    print("  there is no nonzero scalar harmonic residual y with zero endpoint")
    print("  values on the interval.")
    print()
    print("By contrast:")
    print("  omega_H1=dOmega_S2 is the harmonic angular carrier.")
    print()
    print("Elementary zero-carrier domain:")
    print("  keeps the harmonic H1 carrier")
    print("  kills positive relative scalar residual modes")
    print()

    q = Fraction(1, 3)
    print("If elementary mass emergence is the zero/harmonic carrier sector:")
    print("  y=0")
    print("  delta_h=0")
    print(f"  q=p={fmt(q)}")
    print()
    print("If positive relative scalar modes are admitted:")
    print("  h is an excitation or boundary-layer dressing")
    print("  q is branch/profile dependent")
    print()
    print("Spectrum verdict:")
    print("  h is not part of the elementary harmonic carrier space.")
    print("  It can exist only as a larger-domain relative scalar excitation.")
    print("  This supports, but does not independently prove, the elementary")
    print("  phi0 projector that kills h.")


if __name__ == "__main__":
    main()

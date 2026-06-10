from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("h-residual energy identity")
    print("=" * 26)
    print("Let y=ln h be the scalar relative residual on the collar interval.")
    print("Elementary relative boundary values:")
    print("  y(endpoint)=0")
    print("  y(phi0)=0")
    print()
    print("If y is source-free/harmonic on the elementary scalar residual")
    print("sector, then:")
    print("  y''=0")
    print()
    print("Energy identity:")
    print("  integral (y')^2 dt = [y y']_endpoint^phi0 - integral y y'' dt")
    print()
    print("With y=0 at both ends and y''=0:")
    print("  integral (y')^2 dt = 0")
    print("so:")
    print("  y'=0")
    print("  y=constant")
    print("  boundary values force y=0")
    print()
    print("Therefore:")
    print("  h=1")
    print("  delta_h=0")
    print()

    q = Fraction(1, 3)
    print("Then on the H1 one-graph branch:")
    print(f"  q=p={fmt(q)}")
    print(f"  eta={fmt(q / 6)}")
    print(f"  eta/2={fmt(q / 12)}")
    print()
    print("If y is nonzero:")
    print("  it is not a source-free harmonic residual.")
    print("  It must be a positive relative scalar excitation or be driven by")
    print("  an additional scalar source/boundary-layer condition.")
    print()
    print("Proof-status verdict:")
    print("  The elementary projector kills h if the scalar residual sector is")
    print("  source-free and harmonic/zero-mode.")
    print("  The remaining domain statement is whether elementary mass emergence")
    print("  is precisely this source-free harmonic carrier sector.")


if __name__ == "__main__":
    main()

from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("source coefficient as S2 curvature fraction")
    print("=" * 46)
    print("Radial angular-source equation:")
    print("  f'' + 2 f'/r + 2s f/r^2 = 0")
    print()
    print("Round S2 scalar curvature:")
    print("  R2 = 2/r^2")
    print()
    print("Therefore the source term is:")
    print("  (2s/r^2) f = s R2 f")
    print()
    print("So s is exactly:")
    print("  the fraction of intrinsic S2 scalar curvature coupled into the")
    print("  radial f equation.")
    print()
    s = Fraction(1, 9)
    print(f"For s={fmt(s)}:")
    print("  source = (1/9) R2 f")
    print()
    print("Projection checks:")
    print("  one isotropic S2/H1 share = R2/3 -> s=1/3")
    print("  two independent one-third shares = R2/9 -> s=1/9")
    print()
    print("No-invention verdict:")
    print("  The open derivation is not an arbitrary source constant.")
    print("  It is specifically whether the native edge couples one ninth of")
    print("  the S2 scalar curvature into the radial f equation.")


if __name__ == "__main__":
    main()

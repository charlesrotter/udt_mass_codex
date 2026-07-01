from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("relative h-residual domain audit")
    print("=" * 32)
    print("Post-H1 carrier split on the collar I x S2:")
    print("  harmonic angular carrier: omega_H1 = dOmega_S2")
    print("  scalar boundary residual: y = ln h")
    print()
    print("Boundary normalization at phi0:")
    print("  h(phi0)=1")
    print("  y(phi0)=0")
    print()
    print("So h has no value trace at phi0.")
    print("It can enter phi0 Cauchy data only through:")
    print("  dy/dn at phi0")
    print("or equivalently:")
    print("  delta_h = -d ln h / d ln r |phi0")
    print()
    print("Exact carrier classification:")
    print("  omega_H1 is the harmonic angular carrier.")
    print("  d y wedge omega_H1 = d(y omega_H1) is exact.")
    print("  Because y(phi0)=0, its phi0 value trace vanishes.")
    print("  Nonzero delta_h is therefore a relative exact Cauchy residual.")
    print()

    p = Fraction(1, 3)
    s0 = p * (1 - p) / 2
    print("If the elementary bridge source inventory is exhausted by H1:")
    print(f"  p={fmt(p)}")
    print(f"  s0=p(1-p)/2={fmt(s0)}")
    print("  q=p+delta")
    print("  delta' = delta^2 - delta/3")
    print()
    print("With endpoint/self-similar boundary datum delta=0 at one end:")
    print("  uniqueness of the first-order flow gives delta=0 everywhere.")
    print()
    print("If a relative exact scalar residual is admitted:")
    print("  delta_h may be nonzero")
    print("  q=p+delta_h")
    print("  the elementary branch is no longer selected by H1 alone")
    print()
    print("Domain verdict:")
    print("  The remaining question is not algebraic.")
    print("  It is the boundary domain of the elementary phi0 projector:")
    print("    harmonic angular carrier only -> h killed -> q=p")
    print("    harmonic carrier plus relative exact scalar residual -> q free")
    print()
    print("Minimal current postulate, if needed:")
    print("  Elementary mass emergence uses the harmonic H1 carrier domain")
    print("  and quotients relative exact scalar Cauchy residues.")


if __name__ == "__main__":
    main()

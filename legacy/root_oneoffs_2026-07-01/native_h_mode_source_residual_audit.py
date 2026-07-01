from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("h-mode source residual audit")
    print("=" * 28)
    print("Use t=ln r and q=-d ln f/dt.")
    print("The exact q-flow is:")
    print("  dq/dt = q^2 - q + 2s(t)")
    print("so:")
    print("  s(t) = (q' - q^2 + q)/2")
    print()

    p = Fraction(1, 3)
    s0 = p * (1 - p) / 2
    print("For the self-similar H1 endpoint:")
    print(f"  p = {fmt(p)}")
    print(f"  s0 = p(1-p)/2 = {fmt(s0)}")
    print()

    print("Write:")
    print("  q(t) = p + delta(t)")
    print()
    print("Then the exact source residual is:")
    print("  Delta s = s - s0")
    print("          = [delta' + delta(1-2p) - delta^2]/2")
    print()
    print("For p=1/3:")
    print("  Delta s = [delta' + delta/3 - delta^2]/2")
    print()

    print("Therefore:")
    print("  delta=0 gives Delta s=0.")
    print("  nonzero delta is not free; it requires a source residual,")
    print("  unless it obeys the special running equation for the same s0.")
    print()

    print("If the collar source is exactly the canonical H1 area-form source")
    print("with no additional scalar source:")
    print("  s(t)=s0=1/9")
    print("then:")
    print("  delta' = delta^2 - delta/3")
    print()
    print("With endpoint boundary condition delta(endpoint)=0, uniqueness of")
    print("the first-order q-flow gives:")
    print("  delta(t)=0 through the elementary collar.")
    print()

    a = Fraction(1, 20)
    residual_at_phi0 = (a + a / 3 - a * a) / 2
    print("Counterexample h(r)=exp[-a(r/R-1)] at phi0:")
    print(f"  a=delta_h={fmt(a)}")
    print(f"  Delta s(phi0)={fmt(residual_at_phi0)}")
    print()

    print("Gate verdict:")
    print("  Allowing h is equivalent to allowing an additional scalar source")
    print("  residual or an independent boundary-layer flow.")
    print("  If the elementary bridge source inventory is exhausted by the")
    print("  canonical H1 area-form carrier, h is excluded and p=q.")


if __name__ == "__main__":
    main()

from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("one-third equivalence triangle")
    print("=" * 34)
    print("Definitions:")
    print("  p = endpoint profile exponent for f ~ r^-p")
    print("  q = collar log-slope, q = -d ln f / d ln r")
    print("  s = constant H1 source in q-flow")
    print()
    print("Bridge assumption to test:")
    print("  q_phi0 = p")
    print("  This holds for a globally self-similar power-law collar,")
    print("  but is not guaranteed for a finite cell with a boundary layer.")
    print()
    print("Endpoint self-similarity:")
    print("  1 - 2p = p")
    p = Fraction(1, 3)
    print(f"  p = {fmt(p)}")
    print()
    print("If q=p:")
    q = p
    print(f"  q = {fmt(q)}")
    print(f"  curvature-share R3/R2 = q = {fmt(q)}")
    print()
    print("Fixed-source q-flow:")
    print("  fixed point condition: s = q(1-q)/2")
    s = q * (1 - q) / 2
    print(f"  s = {fmt(s)}")
    print()
    print("Downstream transfer:")
    print(f"  q/2 = {fmt(q / 2)}")
    print(f"  eta = q/6 = {fmt(q / 6)}")
    print(f"  eta/2 = q/12 = {fmt(q / 12)}")
    print()
    print("No-invention verdict:")
    print("  The three one-third routes are algebraically the same if q_phi0=p.")
    print("  Therefore the decisive native question is:")
    print("    does the phi0 boundary layer preserve the self-similar log-slope?")
    print("  If yes, q=1/3 follows from endpoint self-similarity.")
    print("  If no, q is determined by the boundary layer/source running instead.")


if __name__ == "__main__":
    main()

from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("GR atlas: Robin / joint audit for phi0")
    print("=" * 41)
    print("Native C1 radial action in f=e^{-2phi}:")
    print("  S_C1 = (1/4) integral r^2 f'^2 dr")
    print()
    print("Exact boundary variation:")
    print("  delta S_C1 = bulk + [Pi_f delta f]")
    print("  Pi_f = (1/2) R^2 f'(R)")
    print()
    print("At phi0:")
    print("  f(R)=1")
    print("  q = -R f'(R)/f(R)")
    print("  Pi_f = -q R/2")
    print("  dimensionless conjugate = -Pi_f/R = q/2")
    print()
    print("Robin/mixed-boundary classification:")
    print("  A nonzero q with free delta f requires a boundary functional B.")
    print("  Stationarity gives:")
    print("    Pi_f + partial B/partial f = 0")
    print("  Therefore:")
    print("    partial B/partial f = q R/2")
    print()
    q = Fraction(1, 3)
    print("For the current H1 target q=1/3:")
    print(f"  -Pi_f/R = {fmt(q / 2)}")
    print(f"  eta = (q/2)/3 = {fmt(q / 6)}")
    print(f"  one-sided transfer = eta/2 = {fmt(q / 12)}")
    print()
    print("Joint/corner target:")
    print("  A native phi0 joint term would be localized at the collar where")
    print("  the radial negative-phi region and the angular S2 data meet.")
    print("  It must produce the derivative q R/2 without creating an exterior 1/r tail.")
    print()
    print("No-invention verdict:")
    print("  Robin language identifies the exact missing mathematical role.")
    print("  It does not derive B or q. The strongest next search is for a")
    print("  native UDT joint/edge term whose variation supplies this boundary momentum.")


if __name__ == "__main__":
    main()

from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("self-coupled curvature-share source")
    print("=" * 38)
    print("At phi0:")
    print("  R3/R2 = q")
    print()
    print("If H1 activation uses:")
    print("  curvature-share factor q")
    print("  times independent H1/S2 projection 1/3")
    print("then:")
    print("  s(q) = q/3")
    print()
    print("Endpoint/collar self-consistency requires:")
    print("  q(1-q)/2 = s(q)")
    print("  q(1-q)/2 = q/3")
    print()
    print("Solutions:")
    print("  q = 0")
    print("  q = 1/3")
    print()
    q = Fraction(1, 3)
    print("Nontrivial branch:")
    print(f"  q = {fmt(q)}")
    print(f"  s = q/3 = {fmt(q / 3)}")
    print(f"  eta = q/6 = {fmt(q / 6)}")
    print()
    print("No-approximation verdict:")
    print("  This route does not assume the curvature share is already 1/3.")
    print("  It assumes the source law s(q)=q/3, then self-consistency selects")
    print("  the nontrivial q=1/3 branch.")


if __name__ == "__main__":
    main()

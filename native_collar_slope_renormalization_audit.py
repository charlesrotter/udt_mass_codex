from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("collar slope renormalization audit")
    print("=" * 40)
    print("Write a finite-cell interior as:")
    print("  f(r) = (R/r)^p h(r)")
    print("with:")
    print("  h(R) = 1")
    print()
    print("The collar log-slope is:")
    print("  q_phi0 = -d ln f / d ln r at R")
    print("         = p - d ln h / d ln r at R")
    print()
    print("Define boundary-layer renormalization:")
    print("  delta_h = - d ln h / d ln r at R")
    print("  q_phi0 = p + delta_h")
    print()
    print("Therefore:")
    print("  q_phi0 = p only if delta_h = 0")
    print()
    p = Fraction(1, 3)
    print("For endpoint self-similarity p=1/3:")
    print(f"  q_phi0 = {fmt(p)} + delta_h")
    print(f"  eta = q_phi0/6 = {fmt(p / 6)} + delta_h/6")
    print()
    print("Flat exterior condition:")
    print("  f_out=1 and f'_out=0")
    print("  This does not force delta_h=0.")
    print("  It only tells us the interface jump equals the inner q_phi0.")
    print()
    print("No-invention verdict:")
    print("  The endpoint p=1/3 route derives q=1/3 only if the phi0")
    print("  boundary layer does not renormalize the log-slope.")
    print("  The next native test is whether C1/angular closure enforces delta_h=0,")
    print("  or instead predicts a branch-dependent delta_h.")


if __name__ == "__main__":
    main()

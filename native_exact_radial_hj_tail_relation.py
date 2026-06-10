from fractions import Fraction


def fmt(x: Fraction) -> str:
    if x.denominator == 1:
        return str(x.numerator)
    return f"{x.numerator}/{x.denominator}"


def main() -> None:
    print("Exact radial C1 Hamilton-Jacobi / tail relation")
    print("=" * 52)
    print("For source-free radial C1 in f=e^{-2phi}:")
    print("  S = (1/4) integral r^2 f'^2 dr")
    print("Euler-Lagrange equation:")
    print("  (r^2 f')' = 0")
    print("Exact solution:")
    print("  f(r) = A + B/r")
    print()
    print("Canonical momentum:")
    print("  Pi_f = (1/2) r^2 f' = -B/2")
    print("Thus:")
    print("  B = -2 Pi_f")
    print()
    print("At a collar R with f(R)=1 and q=-R f'(R)/f(R):")
    print("  f'(R) = -q/R")
    print("  B = q R")
    print("  Pi_f = -q R / 2")
    print()
    q = Fraction(1, 3)
    r = Fraction(1, 1)
    b = q * r
    pi = -b / 2
    eta = (-pi) / 3
    print("Exact self-similar collar R=1, q=1/3:")
    print(f"  B = {fmt(b)}")
    print(f"  Pi_f = {fmt(pi)}")
    print(f"  H1 projection (-Pi_f)/3 = {fmt(eta)}")
    print()
    print("Asymptotically flat exterior requires:")
    print("  f_out(r) = 1 + a/r")
    print("and a flat exterior has:")
    print("  a = 0")
    print("  Pi_f,out = 0")
    print()
    print("Exact conclusion:")
    print("  A nonzero inner q corresponds to a nonzero vacuum-tail coefficient")
    print("  on the source-free side of the C1 equation.")
    print("  Therefore q!=0 and a_out=0 cannot be joined by a smooth source-free")
    print("  continuation. A boundary/interface contribution is required.")
    print()
    print("No-approximation verdict:")
    print("  The phi0 layer is not optional if eta is nonzero and the exterior is flat.")


if __name__ == "__main__":
    main()

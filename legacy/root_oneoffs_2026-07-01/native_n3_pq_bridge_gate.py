from fractions import Fraction
from math import comb


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def lambda3_count(n: int) -> int:
    if n < 3:
        return 0
    return comb(n, 3)


def main() -> None:
    print("N=3 to p=q bridge gate")
    print("=" * 27)
    print("Metric-visible pieces:")
    print("  scalar tail cancellation removes ell=0, N=1 as matter imprint")
    print("  first nonconstant S2 angular carrier is ell=1, N=3")
    print("  N=3 has Lambda^3 count=1")
    print()

    for ell in range(0, 5):
        n = 2 * ell + 1
        role = "scalar tail" if ell == 0 else "angular carrier"
        print(
            f"  ell={ell}: N={n}, role={role}, "
            f"Lambda^3 count={lambda3_count(n)}"
        )

    print()
    print("Endpoint C1 self-similarity:")
    print("  finite action remainder exponent = 1 - 2p")
    print("  self-similar endpoint condition: 1 - 2p = p")
    p = Fraction(1, 3)
    print(f"  p = {fmt(p)}")
    print()

    n = 3
    p_from_dimension = Fraction(1, n)
    print("Angular-dimension reading:")
    print("  if endpoint exponent is inverse surviving angular dimension,")
    print("  p = 1/N")
    print(f"  with N={n}: p = {fmt(p_from_dimension)}")
    print(f"  agreement with C1 self-similarity: {p_from_dimension == p}")
    print()

    print("Collar bridge:")
    print("  write f(r)=(R/r)^p h(r), h(R)=1")
    print("  q_phi0 = p - d ln h/d ln r |R")
    print("         = p + delta_h")
    print("  q_phi0=p iff delta_h=0")
    print()

    q = p
    delta_pi_over_r = q / 2
    eta = q / 6
    one_side = eta / 2
    source = q * (1 - q) / 2
    print("If the one-graph/no-running bridge delta_h=0 holds:")
    print(f"  q = {fmt(q)}")
    print(f"  Delta Pi/R = q/2 = {fmt(delta_pi_over_r)}")
    print(f"  eta = q/6 = {fmt(eta)}")
    print(f"  eta/2 = {fmt(one_side)}")
    print(f"  fixed q-flow source s=q(1-q)/2 = {fmt(source)}")
    print()

    print("Gate verdict:")
    print("  N=3 is now pinned by angular survival, not by a Dirac import.")
    print("  p=1/3 is independently pinned by exact C1 endpoint self-similarity.")
    print("  Their equality p=1/N is therefore an intersection of metric pieces.")
    print("  The remaining nontrivial gate is q_phi0=p, equivalently delta_h=0.")
    print("  If that gate is derived, q=1/3 follows without fitting.")


if __name__ == "__main__":
    main()

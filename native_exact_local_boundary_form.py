from fractions import Fraction


def fmt(x: Fraction) -> str:
    if x.denominator == 1:
        return str(x.numerator)
    return f"{x.numerator}/{x.denominator}"


def main() -> None:
    print("Exact local phi0 boundary form")
    print("=" * 31)
    print("Let F be the boundary value f(phi0).")
    print("A differentiable boundary functional S_b(F, nodes) that cancels")
    print("the C1 inner momentum must satisfy at F=1:")
    print("  dS_b/dF = q/2")
    print()
    print("Therefore its exact first variation at the collar is:")
    print("  delta S_b = (q/2) delta F")
    print()
    print("Equivalently, every acceptable S_b has local form:")
    print("  S_b(F, nodes) = S_b(1, nodes) + (q/2)(F-1) + terms with")
    print("                  zero first F-derivative at F=1")
    print()
    q = Fraction(1, 3)
    derivative = q / 2
    eta = derivative / 3
    print("For q=1/3:")
    print(f"  dS_b/dF = {fmt(derivative)}")
    print(f"  H1-projected derivative = {fmt(eta)}")
    print()
    print("If the H1/projective unit vector n_a carries the boundary observable,")
    print("the exact first variation can be resolved as:")
    print("  delta S_b,ab = (q/2) n_a n_b delta F")
    print("and round-S2 averaging gives:")
    print("  <delta S_b,ab> = (q/6) delta_ab delta F")
    print()
    print("Exact conclusion:")
    print("  The local momentum-carrying part of the phi0 functional is fixed")
    print("  by its first derivative. This does not determine the value condition")
    print("  S_b(1,nodes), which is where a_tail=0 must enter.")
    print()
    print("No-approximation verdict:")
    print("  Local momentum closure and global tail closure are exactly distinct")
    print("  pieces of the boundary functional.")


if __name__ == "__main__":
    main()

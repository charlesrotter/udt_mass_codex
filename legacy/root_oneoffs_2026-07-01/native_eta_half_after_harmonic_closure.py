from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def c1_action_over_radius(q: Fraction) -> Fraction:
    return q * q / (4 * (1 - 2 * q))


def main() -> None:
    print("eta/2 after harmonic closure")
    print("=" * 31)
    print("Use only the current post-H1 facts:")
    print("  harmonic H1 carrier gives N=3")
    print("  elementary harmonic-domain closure gives delta_h=0")
    print("  endpoint self-similarity gives q=p=1/3")
    print()

    q = Fraction(1, 3)
    n = Fraction(3)
    eta = (q / 2) / n
    c1 = c1_action_over_radius(q)
    projected_c1 = c1 / n
    print("C1 action for a self-similar finite cell:")
    print("  f(r)=(R/r)^q")
    print("  S_C1/R = q^2/[4(1-2q)]")
    print()
    print(f"At q={fmt(q)}:")
    print(f"  S_C1/R = {fmt(c1)}")
    print(f"  H1 projected C1 action = (S_C1/R)/N = {fmt(projected_c1)}")
    print(f"  eta = (q/2)/N = {fmt(eta)}")
    print(f"  eta/2 = {fmt(eta / 2)}")
    print()
    print("Exact identity:")
    print("  H1 projected C1 action = eta/2")
    print(f"  {fmt(projected_c1)} = {fmt(eta / 2)}")
    print()

    print("Equivalently, before setting q:")
    print("  demand projected C1 action equals eta/2")
    print("  [q^2/(4(1-2q))]/N = [(q/2)/N]/2")
    print("  q^2/[4(1-2q)] = q/4")
    print("  nontrivial branch: q=1/3")
    print()

    print("Verdict:")
    print("  eta/2 is not an extra postulate once the elementary harmonic")
    print("  closure supplies q=1/3.")
    print("  It is the exact H1-projected on-shell C1 action value of the")
    print("  self-similar finite cell.")
    print("  Symmetric gluing can still explain why two sides compose to eta,")
    print("  but it is no longer needed to manufacture the number 1/36.")


if __name__ == "__main__":
    main()

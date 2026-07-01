from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def nonzero_fixed_for_s_equals_cq(c: Fraction) -> Fraction:
    # q(1-q)/2 = c q gives q=0 or 1-2c.
    return 1 - 2 * c


def main() -> None:
    print("activation law alternative scan")
    print("=" * 34)
    print("For source law s(q)=c q, self-consistency gives:")
    print("  q(1-q)/2 = c q")
    print("  q = 0 or q = 1 - 2c")
    print()
    candidates = [
        ("no projection", Fraction(1, 1), "s=q"),
        ("single radial-angular plane share", Fraction(1, 2), "s=q/2"),
        ("H1/S2 projection share", Fraction(1, 3), "s=q/3"),
        ("two-plane plus H1 mixed share", Fraction(1, 6), "s=q/6"),
        ("fixed constant source", None, "s=1/9"),
    ]
    for name, c, law in candidates:
        print(name)
        print(f"  law: {law}")
        if c is None:
            print("  fixed branches: q=1/3 and q=2/3 for s=1/9")
        else:
            q = nonzero_fixed_for_s_equals_cq(c)
            print(f"  nonzero fixed branch: q={fmt(q)}")
            if q <= 0:
                print("  status: rejects finite positive nontrivial branch")
            elif q >= Fraction(1, 2):
                print("  status: non-finite or threshold-risk branch for C1 endpoint")
            else:
                print("  status: finite positive branch")
        print()

    print("No-approximation verdict:")
    print("  s=q/3 is special among simple projection laws because it gives")
    print("  q=1/3, the finite self-similar branch. Other natural-looking")
    print("  coefficients either kill the branch or move it to a different value.")


if __name__ == "__main__":
    main()

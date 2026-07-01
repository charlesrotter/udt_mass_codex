from dataclasses import dataclass
from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


@dataclass(frozen=True)
class Candidate:
    name: str
    value: Fraction | None
    verdict: str


CANDIDATES = [
    Candidate(
        name="single isotropic S2 second moment <n_i^2>",
        value=Fraction(1, 3),
        verdict="too large; gives 1/3, not 1/9",
    ),
    Candidate(
        name="single-component S2 fourth moment <n_i^4>",
        value=Fraction(1, 5),
        verdict="wrong value; do not replace by (1/3)^2 unless two factors are independent",
    ),
    Candidate(
        name="two independent isotropic H1/S2 second-moment projections",
        value=Fraction(1, 9),
        verdict="correct value if the source genuinely factorizes into two independent projections",
    ),
    Candidate(
        name="curvature-share 1/3 times H1/S2 projection 1/3",
        value=Fraction(1, 9),
        verdict="correct value if curvature-share closure is already established",
    ),
    Candidate(
        name="fixed-point backsolve from q=1/3",
        value=Fraction(1, 9),
        verdict="algebraically true but circular as a derivation of s",
    ),
]


def main() -> None:
    print("H1 source one-ninth origin audit")
    print("=" * 37)
    for candidate in CANDIDATES:
        print(candidate.name)
        if candidate.value is not None:
            print(f"  value:   {fmt(candidate.value)}")
        print(f"  verdict: {candidate.verdict}")
        print()

    print("No-invention verdict:")
    print("  s=1/9 is not derived by saying 'one third appears twice'.")
    print("  It requires an exact two-factor structure:")
    print("    independent projection x independent projection, or")
    print("    established curvature-share x independent H1/S2 projection.")
    print("  Otherwise s=1/9 remains a postulate or a circular backsolve.")


if __name__ == "__main__":
    main()

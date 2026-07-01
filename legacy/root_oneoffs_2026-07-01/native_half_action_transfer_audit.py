import math
from dataclasses import dataclass


@dataclass(frozen=True)
class WeightRule:
    name: str
    exponent_factor: float
    interpretation: str

    def gamma(self, n: int, eta: float) -> float:
        return n * math.exp(-self.exponent_factor * eta)


RULES = [
    WeightRule(
        "full action",
        1.0,
        "A whole boundary unit is charged to each transfer step.",
    ),
    WeightRule(
        "half action",
        0.5,
        "A symmetric two-sided transfer assigns half the boundary unit to each side.",
    ),
    WeightRule(
        "quarter action",
        0.25,
        "A further split over two endpoints and two orientations; currently unmotivated.",
    ),
]


def main() -> None:
    n = 3
    eta = 1.0 / 18.0
    print("Half-action transfer audit")
    print("=" * 26)
    print("Inputs from scalar projection candidate:")
    print(f"  N={n}")
    print(f"  eta={eta:.12g}")
    print()
    print("Candidate transfer trace:")
    print("  gamma = Tr exp(-w eta I_N) = N exp(-w eta)")
    print()
    for rule in RULES:
        gamma = rule.gamma(n, eta)
        print(rule.name)
        print(f"  w={rule.exponent_factor:.9g}")
        print(f"  gamma={gamma:.12g}")
        print(f"  log gamma={math.log(gamma):.12g}")
        print(f"  interpretation: {rule.interpretation}")

    print("\nNative status:")
    print("  - w=1/2 is natural for a symmetric interface-to-interface transfer")
    print("    where one boundary scalar unit is shared by the two sides of a cell.")
    print("  - The metric calculation alone has not yet forced w=1/2.")
    print("  - To derive it, formulate the finite cell as a two-boundary variational")
    print("    problem and show the boundary scalar enters as B_left/2 + B_right/2.")
    print("  - Until then, w=1/2 is a transfer-postulate, not a mass fit.")


if __name__ == "__main__":
    main()

import math
from dataclasses import dataclass


def warped_b_ratio() -> float:
    x = 6.0 * math.sqrt(2.0)
    numerator = (
        math.cosh(x)
        - 6.0 * math.sinh(x) / x
        + 15.0 * math.cosh(x) / (x * x)
        - 15.0 * math.sinh(x) / (x * x * x)
    )
    denominator = (
        math.sinh(x)
        - 3.0 * math.cosh(x) / x
        + 3.0 * math.sinh(x) / (x * x)
    )
    return numerator / denominator


@dataclass(frozen=True)
class Branch:
    name: str
    use_if: str
    exact_form: str
    status: str


BRANCHES = [
    Branch(
        "interface-local H1 transfer",
        "the transfer action lives directly on phi0 boundary/edge data",
        "gamma_simple = 3 exp(-1/36)",
        "best current conditional branch; supported by localized q/2 identities",
    ),
    Branch(
        "warped bulk DtN transfer",
        "the transfer action is obtained by eliminating the negative-phi collar bulk",
        "gamma_warped = 3 exp(-B/36)",
        "exact discriminator branch; profile-sensitive through B",
    ),
]


def main() -> None:
    b = warped_b_ratio()
    gamma_simple = 3.0 * math.exp(-1.0 / 36.0)
    gamma_warped = 3.0 * math.exp(-b / 36.0)

    print("transfer branch selection gate")
    print("=" * 31)
    for branch in BRANCHES:
        print(branch.name)
        print(f"  use if:     {branch.use_if}")
        print(f"  exact form: {branch.exact_form}")
        print(f"  status:     {branch.status}")
        print()

    print("Warped branch exact expression:")
    print("  B = I_{7/2}(6 sqrt(2)) / I_{5/2}(6 sqrt(2))")
    print("  equivalently the half-integer hyperbolic rational form already recorded")
    print()
    print("Diagnostic numeric values:")
    print(f"  B = {b:.12g}")
    print(f"  gamma_simple = {gamma_simple:.12g}")
    print(f"  gamma_warped = {gamma_warped:.12g}")
    print(f"  gamma_warped/gamma_simple = {gamma_warped / gamma_simple:.12g}")
    print()
    print("Working verdict:")
    print("  Do not average or combine these branches.")
    print("  The action must decide whether transfer is interface-local or bulk-DtN.")


if __name__ == "__main__":
    main()

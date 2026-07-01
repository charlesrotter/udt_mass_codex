from dataclasses import dataclass


@dataclass(frozen=True)
class Tier:
    name: str
    banked_or_derived_inputs: str
    licensed_consequence: str
    not_licensed: str


TIERS = [
    Tier(
        "Tier A: eta foundation",
        "P_phi0 plus exact H1/S2 projection",
        "q=1/3, q/2=1/6, eta=1/18",
        "gamma, typed depths, branch coefficients, masses",
    ),
    Tier(
        "Tier B: interface transfer",
        "Tier A plus banked P_transfer on the interface-local branch",
        "gamma=3 exp(-1/36) as an exact conditional trace identity",
        "gamma powers, typed-depth ladders, branch coefficients, masses",
    ),
    Tier(
        "Tier C: typed graph",
        "Tier B plus banked or derived P_depth_M1/P_depth_E1",
        "symbolic ladder powers such as gamma^5 and gamma^7 inside the selected graph",
        "branch coefficient normalization and dimensional mass predictions",
    ),
    Tier(
        "Tier D: coefficient-complete dimensionless sector",
        "Tier C plus derived M1/E1 finite-cell and measure coefficients",
        "dimensionless mass ratios inside the chosen active-lane model",
        "absolute masses until the electron anchor is applied",
    ),
    Tier(
        "Tier E: anchored mass comparison",
        "Tier D plus electron mass as the single dimensionful anchor",
        "mass comparisons as downstream checks",
        "using observed masses to choose prior gates",
    ),
]


def main() -> None:
    print("active-lane consequence map")
    print("=" * 29)
    for tier in TIERS:
        print(tier.name)
        print(f"  inputs:        {tier.banked_or_derived_inputs}")
        print(f"  licenses:      {tier.licensed_consequence}")
        print(f"  not licensed:  {tier.not_licensed}")
        print()

    print("Map verdict:")
    print("  The current active lane is solid through Tier A.")
    print("  Tier B is bankable if P_transfer is explicitly accepted.")
    print("  Tiers C-E remain consequence-mapping territory until their gates are")
    print("  derived or intentionally banked.")


if __name__ == "__main__":
    main()

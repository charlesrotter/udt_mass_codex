from dataclasses import dataclass


@dataclass(frozen=True)
class Tier:
    tier: str
    current_license: str
    still_not_licensed: str


TIERS = [
    Tier(
        "Tier A: eta foundation",
        "eta=1/18 from banked P_phi0 plus exact H1/S2 projection",
        "q-origin",
    ),
    Tier(
        "Tier A2: H1 identity merge",
        "if H1 is selected, eta I3 and eta L1|H1 are the same operator",
        "value-action status",
    ),
    Tier(
        "Tier B: transfer",
        "if value action, side split, and trace are banked, gamma=3 exp(-1/36)",
        "gamma powers / node product",
    ),
    Tier(
        "Tier C: typed graph",
        "if P_depth is banked, symbolic gamma^5 and gamma^7 ladders",
        "branch coefficients and M2 coefficient/suppression",
    ),
    Tier(
        "Tier D: coefficients",
        "not licensed by H1 merge",
        "S_phi0 typed second jet",
    ),
]


def main() -> None:
    print("consequence map after H1 merge")
    print("=" * 32)
    for tier in TIERS:
        print(tier.tier)
        print(f"  licensed:       {tier.current_license}")
        print(f"  not licensed:   {tier.still_not_licensed}")
        print()

    print("Map verdict:")
    print("  The merge upgrades the operator gate, not the postulate ledger.")
    print("  It reduces P_transfer's burden but leaves q-origin, gluing/trace,")
    print("  typed depth, and coefficients separate.")


if __name__ == "__main__":
    main()

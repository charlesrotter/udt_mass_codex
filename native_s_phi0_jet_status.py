from dataclasses import dataclass


@dataclass(frozen=True)
class JetTier:
    tier: str
    status: str
    licenses: str
    does_not_license: str


TIERS = [
    JetTier(
        "zeroth/value tier",
        "partly specified as a_tail=0 requirement",
        "closed-cell boundary value condition",
        "momentum, eta, coefficients",
    ),
    JetTier(
        "first-variation tier",
        "specified conditionally by P_phi0 and H1 projection",
        "q/2 and eta=1/18",
        "Hessian, coefficients, branch weights",
    ),
    JetTier(
        "one-sided transfer tier",
        "specified only if P_transfer is banked",
        "eta/2 and gamma=3 exp(-1/36)",
        "typed-depth powers or branch coefficients",
    ),
    JetTier(
        "second-variation tier",
        "missing",
        "would license C_M1, C_M2, C_E1 or a coupled replacement",
        "anything until S_phi0[nodes] is derived",
    ),
]


def main() -> None:
    print("S_phi0 jet status")
    print("=" * 18)
    for tier in TIERS:
        print(tier.tier)
        print(f"  status:           {tier.status}")
        print(f"  licenses:         {tier.licenses}")
        print(f"  does not license: {tier.does_not_license}")
        print()

    print("Jet-status verdict:")
    print("  We have enough S_phi0 information for eta and conditional transfer.")
    print("  We do not have enough for Tier D coefficients.")


if __name__ == "__main__":
    main()

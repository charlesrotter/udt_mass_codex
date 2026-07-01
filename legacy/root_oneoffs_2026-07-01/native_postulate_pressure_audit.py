from dataclasses import dataclass


@dataclass(frozen=True)
class Scenario:
    name: str
    banked_items: str
    what_is_resolved: str
    what_remains_diagnostic: str
    verdict: str


SCENARIOS = [
    Scenario(
        name="one-postulate edge model",
        banked_items="P_phi0",
        what_is_resolved="q, s, eta",
        what_remains_diagnostic="gamma, typed depth, branch coefficients, full masses",
        verdict="cleanest native mass-emergence foundation; not a full ladder",
    ),
    Scenario(
        name="two-postulate multiplier model",
        banked_items="P_phi0 + P_transfer",
        what_is_resolved="q, s, eta, gamma",
        what_remains_diagnostic="typed depth, branch coefficients, full masses",
        verdict="still compact; useful working model but not a full derivation",
    ),
    Scenario(
        name="three-postulate ladder model",
        banked_items="P_phi0 + P_transfer + P_depth",
        what_is_resolved="q, s, eta, gamma, typed depth",
        what_remains_diagnostic="branch coefficients and coefficient normalization",
        verdict="postulate-heavy; should not be called minimal unless P_depth is derived",
    ),
]


def main() -> None:
    print("postulate pressure audit")
    print("=" * 24)
    for scenario in SCENARIOS:
        print(scenario.name)
        print(f"  banked items:              {scenario.banked_items}")
        print(f"  resolved:                  {scenario.what_is_resolved}")
        print(f"  remains diagnostic:         {scenario.what_remains_diagnostic}")
        print(f"  verdict:                   {scenario.verdict}")
        print()

    print("No-invention verdict:")
    print("  The cleanest current stopping point is P_phi0, or at most")
    print("  P_phi0 + P_transfer. Do not bank P_depth unless the project")
    print("  explicitly accepts a third postulate or derives it from an edge graph.")


if __name__ == "__main__":
    main()

from dataclasses import dataclass


@dataclass(frozen=True)
class Rule:
    name: str
    use: str
    violation: str


RULES = [
    Rule(
        "pre-registration",
        "state P_phi0, transfer branch, P_transfer, P_depth, Pbundle0, and coefficient functional before comparing ratios",
        "changing any of those after seeing residuals",
    ),
    Rule(
        "M2 inclusion",
        "include M2 as active, suppressed, or conditionally demoted before ratio comparison",
        "dropping M2 because it worsens the ratio story",
    ),
    Rule(
        "coefficient independence",
        "derive C_M1, C_M2, C_E1 without electron/muon/tau data",
        "solving coefficients from observed ratios",
    ),
    Rule(
        "anchor order",
        "apply the electron anchor only after dimensionless ratios are fixed",
        "using the electron anchor to choose branch assignments",
    ),
    Rule(
        "failure allowed",
        "if derived coefficients miss ratios, record the miss as falsification pressure",
        "retuning gates to absorb the miss",
    ),
]


def main() -> None:
    print("lepton-ratio falsification contract")
    print("=" * 38)
    for rule in RULES:
        print(rule.name)
        print(f"  use:       {rule.use}")
        print(f"  violation: {rule.violation}")
        print()

    print("Contract verdict:")
    print("  Lepton ratios become powerful only after the model is frozen.")
    print("  Before that, they are diagnostics, not construction tools.")


if __name__ == "__main__":
    main()

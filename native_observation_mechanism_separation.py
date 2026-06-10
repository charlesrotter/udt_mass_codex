from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    name: str
    allowed_use: str
    forbidden_use: str
    native_replacement: str


ITEMS = [
    Item(
        name="electron mass",
        allowed_use="single dimensionful anchor F",
        forbidden_use="evidence that the electron's SM generation mechanism is present",
        native_replacement="sets the scale after metric-native ratios are computed",
    ),
    Item(
        name="muon/tau masses",
        allowed_use="diagnostic comparison after target-blind structure is derived",
        forbidden_use="choosing closure counts, corrections, or branch assignments",
        native_replacement="test residual signs and branch-specific predictions",
    ),
    Item(
        name="spinor/Dirac analogs",
        allowed_use="legacy language for comparison only",
        forbidden_use="importing Form-T or requiring Dirac operator mechanics",
        native_replacement="negative-phi endpoint data, H1 frame data, compact projective data",
    ),
    Item(
        name="QED/Coulomb",
        allowed_use="metric-derived phi-blind abelian dynamics",
        forbidden_use="assuming full SM radiative mass mechanism",
        native_replacement="use only the Maxwell cancellation actually supplied by the metric",
    ),
    Item(
        name="SU(3)/color",
        allowed_use="round-S2 kinematic/selection structure and epsilon bookkeeping",
        forbidden_use="importing non-abelian color force or confinement dynamics",
        native_replacement="H1 frame, epsilon projection, color-singlet-like closure only if metric-derived",
    ),
    Item(
        name="generations",
        allowed_use="diagnostic label for mass ladder branches",
        forbidden_use="assuming SM generation ontology",
        native_replacement="finite-cell closure depths and branch filters",
    ),
]


def main() -> None:
    print("Observation/mechanism separation audit")
    print("=" * 39)
    print("UDT may match observed quantities without using the same mechanisms")
    print("as the Standard Model. Observations can anchor or test; mechanisms must")
    print("come from the metric/orchestra.")
    print()
    for item in ITEMS:
        print(item.name)
        print(f"  allowed use:      {item.allowed_use}")
        print(f"  forbidden use:    {item.forbidden_use}")
        print(f"  native substitute:{item.native_replacement}")
    print()
    print("Audit verdict:")
    print("  - Observed masses are diagnostics, not construction rules.")
    print("  - SM-like labels are translation labels, not mechanism imports.")
    print("  - The search target remains the metric's native orchestra, even when")
    print("    the output is compared to familiar particle-sector observations.")


if __name__ == "__main__":
    main()

from dataclasses import dataclass


@dataclass(frozen=True)
class Step:
    order: int
    task: str
    allowed_inputs: str
    completion_test: str


STEPS = [
    Step(
        1,
        "hold P_phi0 fixed",
        "q=1/3 as an explicit active-lane postulate",
        "eta=1/18 is used consistently, while q-origin claims stay parked",
    ),
    Step(
        2,
        "select transfer branch",
        "interface-local H1 action or warped bulk DtN, not both",
        "a native action/locality argument decides which gamma is admissible",
    ),
    Step(
        3,
        "derive or bank P_transfer",
        "only after branch selection",
        "the trace/multiplier role of the H1 triplet is stated as derived or conditional",
    ),
    Step(
        4,
        "audit typed depth",
        "edge graph variables after shared-frame merging",
        "node counts are fixed without double-counting M1/Hopf or E1 shape modes",
    ),
    Step(
        5,
        "audit branch coefficients",
        "finite-cell normalization, shape measure, compact bundle status",
        "M1/E1 coefficients are derived or explicitly marked diagnostic",
    ),
    Step(
        6,
        "use electron anchor only at the end",
        "one dimensionful scale after dimensionless structure is fixed",
        "mass comparisons are checks, not inputs to choose gates",
    ),
]


def main() -> None:
    print("active-lane work order")
    print("=" * 22)
    for step in STEPS:
        print(f"{step.order}. {step.task}")
        print(f"  allowed inputs:   {step.allowed_inputs}")
        print(f"  completion test:  {step.completion_test}")
        print()

    print("Loop-prevention rule:")
    print("  If a step cannot be completed exactly, mark it conditional and move")
    print("  to consequence mapping. Do not backfit it from observed masses.")


if __name__ == "__main__":
    main()

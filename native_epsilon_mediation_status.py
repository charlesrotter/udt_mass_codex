from dataclasses import dataclass


@dataclass(frozen=True)
class ConstraintClass:
    name: str
    count_formula: str
    epsilon_status: str
    reason: str
    failure_mode: str


CLASSES = [
    ConstraintClass(
        name="frame orientation closure",
        count_formula="N_frame",
        epsilon_status="direct",
        reason="The constraint is defined on the transported oriented N=3 frame.",
        failure_mode="If the frame is gauge-redundant rather than physical boundary data, its entropy should be divided out.",
    ),
    ConstraintClass(
        name="core-side non-scalar shape closure",
        count_formula="d-1",
        epsilon_status="conditional",
        reason="Non-scalar angular shape data must be projected onto the same transported H1/epsilon frame.",
        failure_mode="If shape modes close by scalar amplitude matching only, they contribute no N entropy.",
    ),
    ConstraintClass(
        name="phi0-side non-scalar shape closure",
        count_formula="d-1",
        epsilon_status="conditional",
        reason="The phi=0 interface has the metric-native scalar boundary jump and the S2 frame available.",
        failure_mode="If outer closure fixes the frame globally, these labels correlate with the core-side labels.",
    ),
]


def main() -> None:
    print("Epsilon mediation status")
    print("=" * 25)
    for item in CLASSES:
        print(item.name)
        print(f"  count: {item.count_formula}")
        print(f"  epsilon status: {item.epsilon_status}")
        print(f"  reason: {item.reason}")
        print(f"  failure mode: {item.failure_mode}")

    print("\nSurviving branch implication:")
    print("  M1: 3 direct frame constraints + 2 conditional shape constraints.")
    print("  E1: 3 direct frame constraints + 4 conditional shape constraints.")
    print()
    print("Independence requirement:")
    print("  Each accepted constraint must be a separate node in the boundary")
    print("  factor graph. Any equality edge collapses N^k to N^components.")
    print()
    print("Audit verdict:")
    print("  - Epsilon mediation is solid for the frame-closure part.")
    print("  - Epsilon mediation is still conditional for the 2(d-1) shape part.")
    print("  - The next derivation must show that non-scalar shape closure is")
    print("    measured in the transported H1 frame, not merely in scalar amplitude.")


if __name__ == "__main__":
    main()

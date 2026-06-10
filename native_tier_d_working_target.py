from dataclasses import dataclass


@dataclass(frozen=True)
class TargetStep:
    order: int
    step: str
    exact_requirement: str


STEPS = [
    TargetStep(
        1,
        "construct the typed boundary variable vector",
        "include shared H1 frame variables, M1 compact/radial variables, M2 compact triplet data, and E1 relative-shape variables",
    ),
    TargetStep(
        2,
        "write the post-P_phi0 boundary functional",
        "use only eta, H1/S2 projection, Hopf/CP1 map, relative-shape coordinates, and compact-bundle labels if Pbundle0 is banked",
    ),
    TargetStep(
        3,
        "compute the quadratic kernel or Hessian",
        "derive it from the functional; do not assign diagonal weights by hand",
    ),
    TargetStep(
        4,
        "evaluate M1, M2, and E1 under the same kernel",
        "produce C_M1, C_M2, C_E1 or a derived null/suppression result",
    ),
    TargetStep(
        5,
        "check invariance",
        "coefficients must be independent of coordinate basis, arbitrary measure normalization, and observed masses",
    ),
]


def main() -> None:
    print("Tier D working target")
    print("=" * 21)
    for step in STEPS:
        print(f"{step.order}. {step.step}")
        print(f"  exact requirement: {step.exact_requirement}")
        print()

    print("Target verdict:")
    print("  Tier D should now search for the typed boundary functional and its")
    print("  Hessian. If that object cannot be built, coefficients remain open.")


if __name__ == "__main__":
    main()

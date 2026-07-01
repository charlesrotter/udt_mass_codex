from dataclasses import dataclass


@dataclass(frozen=True)
class DepthModel:
    branch: str
    exact_native_support: str
    candidate_count: str
    open_assumption: str
    verdict: str


MODELS = [
    DepthModel(
        branch="M1 / compact primitive",
        exact_native_support=(
            "CP1/Hopf data maps exactly into the common H1/S2 frame; "
            "a primitive compact/radial scalar may appear at each boundary"
        ),
        candidate_count="3 H1 channel slots + 1 core shape + 1 phi0 shape = 5",
        open_assumption="H1 channel slots and the two boundary shape scalars are independent transfer nodes",
        verdict="candidate P_depth_M1, not derived from scalar edge rank alone",
    ),
    DepthModel(
        branch="E1 / ordinary H1",
        exact_native_support=(
            "after removing common amplitude, ordinary H1 relative shape is an exact two-dimensional plane"
        ),
        candidate_count="3 H1 channel slots + 2 core relative shapes + 2 phi0 relative shapes = 7",
        open_assumption="core and phi0 relative-shape coordinates are independent transfer nodes",
        verdict="candidate P_depth_E1, not derived from scalar edge rank alone",
    ),
]


def main() -> None:
    print("exact typed-depth status")
    print("=" * 26)
    for model in MODELS:
        print(model.branch)
        print(f"  exact native support:  {model.exact_native_support}")
        print(f"  candidate count:       {model.candidate_count}")
        print(f"  open assumption:       {model.open_assumption}")
        print(f"  verdict:               {model.verdict}")
        print()

    print("Depth verdict:")
    print("  The exact geometry supports the ingredients of 5 and 7, but not the")
    print("  transfer-node independence. If used, typed depth must be a separate")
    print("  P_depth postulate or derived from an edge graph.")


if __name__ == "__main__":
    main()

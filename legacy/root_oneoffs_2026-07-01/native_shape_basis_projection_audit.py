from dataclasses import dataclass


@dataclass(frozen=True)
class BranchShape:
    name: str
    branch_dimension: int
    frame_dimension: int
    embedding_status: str
    reason: str

    @property
    def relative_shape_modes(self) -> int:
        return max(0, self.branch_dimension - 1)

    @property
    def can_live_in_frame_space(self) -> bool:
        return self.branch_dimension <= self.frame_dimension


def main() -> None:
    frame_dimension = 3
    branches = [
        BranchShape(
            name="M1",
            branch_dimension=2,
            frame_dimension=frame_dimension,
            embedding_status="conditional",
            reason="The compact primitive doublet must close through the common phi=0 H1 frame.",
        ),
        BranchShape(
            name="E1",
            branch_dimension=3,
            frame_dimension=frame_dimension,
            embedding_status="direct",
            reason="The ordinary triplet is the full N=3 label/frame space.",
        ),
        BranchShape(
            name="M2",
            branch_dimension=5,
            frame_dimension=frame_dimension,
            embedding_status="fails elementary frame embedding",
            reason="A five-dimensional branch cannot embed as elementary relative data in an N=3 frame.",
        ),
    ]

    print("Shape-basis projection audit")
    print("=" * 29)
    print("A d-component branch has:")
    print("  1 common amplitude mode")
    print("  d-1 relative shape modes")
    print()
    print("For shape closure to be epsilon-mediated, the relative modes must be")
    print("represented as boundary data in the transported N=3 frame space.")
    print()

    for branch in branches:
        print(branch.name)
        print(f"  branch dimension d={branch.branch_dimension}")
        print(f"  relative shape modes d-1={branch.relative_shape_modes}")
        print(f"  frame dimension N={branch.frame_dimension}")
        print(f"  can fit inside N-frame={branch.can_live_in_frame_space}")
        print(f"  embedding status={branch.embedding_status}")
        print(f"  reason={branch.reason}")

    print("\nAudit verdict:")
    print("  - E1 shape closure is naturally frame-mediated.")
    print("  - M1 shape closure is frame-mediated only if the compact primitive")
    print("    doublet uses the common phi=0 H1 frame for closure.")
    print("  - M2 fails the elementary N=3 frame embedding, matching its demotion")
    print("    by primitivity/resonance filters.")
    print("  - This supports the orchestra picture: compact topology and ordinary")
    print("    angular frame have to meet at the same interface for M1.")


if __name__ == "__main__":
    main()

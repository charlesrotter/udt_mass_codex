from dataclasses import dataclass


@dataclass(frozen=True)
class BranchGraph:
    name: str
    selectors: list[str]
    shared_frame_nodes: int
    branch_shape_nodes_per_boundary: int
    boundary_count: int
    bridges: list[str]
    exclusions: list[str]

    @property
    def shape_nodes(self) -> int:
        return self.branch_shape_nodes_per_boundary * self.boundary_count

    @property
    def total_nodes(self) -> int:
        return self.shared_frame_nodes + self.shape_nodes


BRANCHES = [
    BranchGraph(
        name="M1",
        selectors=[
            "nontrivial primitive compact U1 sector |n|=1",
            "projective dimension CP1=S2 matches elementary interface",
        ],
        shared_frame_nodes=3,
        branch_shape_nodes_per_boundary=1,
        boundary_count=2,
        bridges=[
            "Hopf/CP1 bridge maps compact orientation into common H1 frame",
            "node-merge rule prevents double-counting CP1 as extra shape nodes",
        ],
        exclusions=[
            "requires Pbundle0 or a future metric reason for nontrivial compact occupation",
        ],
    ),
    BranchGraph(
        name="E1",
        selectors=[
            "ordinary H1 triplet",
            "p=1/3 endpoint resonance",
        ],
        shared_frame_nodes=3,
        branch_shape_nodes_per_boundary=2,
        boundary_count=2,
        bridges=[
            "ordinary H1 shape data directly uses the common frame",
        ],
        exclusions=[
            "none at the current elementary-interface level",
        ],
    ),
]


def main() -> None:
    print("Current typed branch graph")
    print("=" * 28)
    print("Typed graph rule: selectors and bridges do not automatically add nodes.")
    print()
    for branch in BRANCHES:
        print(branch.name)
        print("  selectors:")
        for item in branch.selectors:
            print(f"    - {item}")
        print("  bridges/mergers:")
        for item in branch.bridges:
            print(f"    - {item}")
        print(f"  shared frame nodes={branch.shared_frame_nodes}")
        print(f"  branch shape nodes per boundary={branch.branch_shape_nodes_per_boundary}")
        print(f"  boundary count={branch.boundary_count}")
        print(f"  shape nodes={branch.shape_nodes}")
        print(f"  total closure nodes={branch.total_nodes}")
        print("  remaining exclusions/gaps:")
        for item in branch.exclusions:
            print(f"    - {item}")
        print()

    print("Typed graph verdict:")
    print("  - M1 and E1 can differ in depth without assigning different eta/gamma.")
    print("  - The difference is in branch-shape node creation after typed merging:")
    print("      M1: 3 shared frame + 2 shape = 5")
    print("      E1: 3 shared frame + 4 shape = 7")
    print("  - This is an orchestra result: selectors, bridges, projectors, weights,")
    print("    and node creators play different roles.")


if __name__ == "__main__":
    main()

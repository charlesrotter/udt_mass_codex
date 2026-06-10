from dataclasses import dataclass


@dataclass(frozen=True)
class NodeSet:
    name: str
    frame_nodes: int
    shape_nodes_core: int
    shape_nodes_phi0: int
    merged_nodes: int
    explanation: str

    @property
    def total(self) -> int:
        return self.frame_nodes + self.shape_nodes_core + self.shape_nodes_phi0 - self.merged_nodes


SCENARIOS = [
    NodeSet(
        name="M1 shared Hopf-frame graph",
        frame_nodes=3,
        shape_nodes_core=1,
        shape_nodes_phi0=1,
        merged_nodes=0,
        explanation=(
            "Hopf/CP1 orientation is the bridge into the existing H1 frame nodes; "
            "only one primitive compact/radial shape scalar is added at each boundary."
        ),
    ),
    NodeSet(
        name="M1 double-counted Hopf graph",
        frame_nodes=3,
        shape_nodes_core=2,
        shape_nodes_phi0=2,
        merged_nodes=0,
        explanation=(
            "CP1 projective directions are counted as extra shape nodes in addition "
            "to the common H1 frame nodes."
        ),
    ),
    NodeSet(
        name="E1 ordinary H1 graph",
        frame_nodes=3,
        shape_nodes_core=2,
        shape_nodes_phi0=2,
        merged_nodes=0,
        explanation="E1 relative shape modes are directly H1 shape modes at both boundaries.",
    ),
    NodeSet(
        name="correlated global block",
        frame_nodes=3,
        shape_nodes_core=2,
        shape_nodes_phi0=2,
        merged_nodes=6,
        explanation="Extreme collapse where all but one node are tied by equality edges.",
    ),
]


def main() -> None:
    print("Orchestra node-merge audit")
    print("=" * 28)
    print("In an orchestra graph, couplings can merge nodes rather than add nodes.")
    print("This matters for M1: Hopf/CP1 can be a bridge into H1, not extra depth.")
    print()
    for scenario in SCENARIOS:
        print(scenario.name)
        print(f"  frame nodes={scenario.frame_nodes}")
        print(f"  core shape nodes={scenario.shape_nodes_core}")
        print(f"  phi0 shape nodes={scenario.shape_nodes_phi0}")
        print(f"  merged/correlated nodes={scenario.merged_nodes}")
        print(f"  effective total={scenario.total}")
        print(f"  explanation: {scenario.explanation}")
        print()

    print("Audit verdict:")
    print("  - Orchestra coupling is not simple addition.")
    print("  - Some couplings identify variables and prevent overcounting.")
    print("  - M1 depth 5 requires Hopf orientation to merge with the common H1")
    print("    frame nodes rather than creating separate CP1 shape nodes.")
    print("  - E1 depth 7 remains direct because its two relative modes are ordinary")
    print("    H1 shape modes at each boundary.")


if __name__ == "__main__":
    main()

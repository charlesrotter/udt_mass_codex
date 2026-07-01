from dataclasses import dataclass


@dataclass(frozen=True)
class Role:
    instrument: str
    role_type: str
    graph_effect: str
    current_example: str


ROLES = [
    Role(
        instrument="negative-phi endpoint",
        role_type="node condition",
        graph_effect="admits or excludes endpoint branches",
        current_example="finite action and p=1/3 self-similarity",
    ),
    Role(
        instrument="phi0 interface",
        role_type="weight source",
        graph_effect="supplies scalar budget B=p/2",
        current_example="B=1/6 for p=1/3",
    ),
    Role(
        instrument="round S2/H1",
        role_type="projector and rank source",
        graph_effect="turns scalar budget into eta delta_ab and rank-3 traces",
        current_example="<n_a n_b>=delta_ab/3",
    ),
    Role(
        instrument="symmetric transfer",
        role_type="edge weight",
        graph_effect="assigns one-sided eta/2 to composable boundary kernels",
        current_example="gamma=3 exp(-1/36)",
    ),
    Role(
        instrument="two-boundary variation",
        role_type="node creator",
        graph_effect="creates core-side and phi0-side shape closure opportunities",
        current_example="2(d-1) local shape data",
    ),
    Role(
        instrument="compact U1 primitive",
        role_type="branch selector",
        graph_effect="admits M1 primitive doublet if nontrivial compact bundle occupied",
        current_example="|n|=1",
    ),
    Role(
        instrument="Hopf/CP1 bridge",
        role_type="node merger/bridge",
        graph_effect="identifies M1 compact orientation with common H1 frame nodes",
        current_example="CP1=S2",
    ),
    Role(
        instrument="observed masses",
        role_type="diagnostic only",
        graph_effect="tests output after graph is built",
        current_example="electron anchor; mu/tau residual checks",
    ),
]


def main() -> None:
    print("Orchestra node-role taxonomy")
    print("=" * 29)
    print("Not every instrument adds a node. Some select, weight, bridge, or merge.")
    print()
    for role in ROLES:
        print(role.instrument)
        print(f"  role type: {role.role_type}")
        print(f"  graph effect: {role.graph_effect}")
        print(f"  current example: {role.current_example}")
    print()
    print("Taxonomy verdict:")
    print("  The safe orchestra rule is typed composition, not additive stacking.")
    print("  A proposed instrument must state whether it creates nodes, weights nodes,")
    print("  selects branches, bridges variables, merges nodes, or only diagnoses output.")


if __name__ == "__main__":
    main()

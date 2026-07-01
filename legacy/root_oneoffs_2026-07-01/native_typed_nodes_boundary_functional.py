from dataclasses import dataclass


@dataclass(frozen=True)
class NodeClass:
    name: str
    count_m1: int
    count_e1: int
    value_role: str
    derivative_role: str
    factorization_status: str


NODES = [
    NodeClass(
        name="shared H1 frame nodes",
        count_m1=3,
        count_e1=3,
        value_role="orient closure so a_tail functional can vanish in H1-projected sectors",
        derivative_role="project C1 boundary momentum q/2 into eta=q/6",
        factorization_status="direct H1 kernel; physical if non-scalar boundary data are allowed",
    ),
    NodeClass(
        name="core-side shape nodes",
        count_m1=1,
        count_e1=2,
        value_role="encode how endpoint/source data contribute to a_tail",
        derivative_role="supply variation of a_tail with respect to core-side shape",
        factorization_status="independent by local endpoint variation unless tied",
    ),
    NodeClass(
        name="phi0-side shape nodes",
        count_m1=1,
        count_e1=2,
        value_role="encode collar/source data needed for a_tail=0",
        derivative_role="supply variation of boundary functional with respect to collar shape",
        factorization_status="independent by local boundary variation unless tied",
    ),
]


def main() -> None:
    print("Typed nodes as boundary-functional variables")
    print("=" * 44)
    print("Hypothesis: the closure graph is the variable set of the phi0")
    print("two-condition boundary functional.")
    print()
    total_m1 = 0
    total_e1 = 0
    for node in NODES:
        total_m1 += node.count_m1
        total_e1 += node.count_e1
        print(node.name)
        print(f"  M1 count={node.count_m1}")
        print(f"  E1 count={node.count_e1}")
        print(f"  value role:      {node.value_role}")
        print(f"  derivative role: {node.derivative_role}")
        print(f"  factorization:   {node.factorization_status}")
        print()

    print("Totals:")
    print(f"  M1 nodes={total_m1}")
    print(f"  E1 nodes={total_e1}")
    print()
    print("Boundary-functional verdict:")
    print("  - The typed closure graph can be reinterpreted as the variable list")
    print("    of the phi0 boundary functional.")
    print("  - a_tail=0 is the value equation.")
    print("  - q/2 projection is the derivative/momentum equation.")
    print("  - Factorization becomes a claim about the Hessian/kernel of this")
    print("    boundary functional in the typed node variables.")


if __name__ == "__main__":
    main()

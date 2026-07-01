from dataclasses import dataclass


@dataclass(frozen=True)
class ClosureNode:
    name: str
    location: str
    variable: str
    kernel_source: str


NODES_M1 = [
    ClosureNode("frame_x", "collar transport", "H1/projective frame component x", "S2 isotropic kernel"),
    ClosureNode("frame_y", "collar transport", "H1/projective frame component y", "S2 isotropic kernel"),
    ClosureNode("frame_z", "collar transport", "H1/projective frame component z", "S2 isotropic kernel"),
    ClosureNode("core_shape", "core-side boundary", "M1 relative shape via CP1", "Hopf/H1 kernel"),
    ClosureNode("phi0_shape", "phi0 boundary", "M1 relative shape via CP1", "interface/H1 kernel"),
]

NODES_E1 = [
    ClosureNode("frame_x", "collar transport", "H1 frame component x", "S2 isotropic kernel"),
    ClosureNode("frame_y", "collar transport", "H1 frame component y", "S2 isotropic kernel"),
    ClosureNode("frame_z", "collar transport", "H1 frame component z", "S2 isotropic kernel"),
    ClosureNode("core_shape_1", "core-side boundary", "E1 relative shape mode 1", "H1 kernel"),
    ClosureNode("core_shape_2", "core-side boundary", "E1 relative shape mode 2", "H1 kernel"),
    ClosureNode("phi0_shape_1", "phi0 boundary", "E1 relative shape mode 1", "interface/H1 kernel"),
    ClosureNode("phi0_shape_2", "phi0 boundary", "E1 relative shape mode 2", "interface/H1 kernel"),
]


def print_nodes(label: str, nodes: list[ClosureNode]) -> None:
    print(label)
    for node in nodes:
        print(f"  {node.name}")
        print(f"    location: {node.location}")
        print(f"    variable: {node.variable}")
        print(f"    kernel:   {node.kernel_source}")
    print()


def main() -> None:
    print("Orchestra locality/independence audit")
    print("=" * 39)
    print("Equality edges are not automatic if nodes live on distinct boundary")
    print("locations or distinct variational variables.")
    print()

    print_nodes("M1 nodes", NODES_M1)
    print_nodes("E1 nodes", NODES_E1)

    print("Native independence supports:")
    print("  - core-side and phi0-side variables appear as separate endpoint")
    print("    variations in a local radial action.")
    print("  - H1 frame components are orthogonal under the round S2 measure.")
    print("  - M1 compact shape reaches H1 through phase-invariant CP1 bilinears,")
    print("    not through an arbitrary added connector.")
    print("  - The interface scalar kernel is isotropic, so it does not impose a")
    print("    preferred equality edge between components.")
    print()
    print("Collapse risks:")
    print("  - a global matching condition could tie core and phi0 shape variables.")
    print("  - a singlet-only closure rule could project out non-scalar H1 data.")
    print("  - a single-block transfer could replace tensor-product node traces.")
    print()
    print("Audit verdict:")
    print("  The orchestra graph has native locality reasons to remain factorized,")
    print("  but independence is still a structural hypothesis until the full")
    print("  boundary variation is written in these variables.")


if __name__ == "__main__":
    main()

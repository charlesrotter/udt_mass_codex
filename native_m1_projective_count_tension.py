from dataclasses import dataclass


@dataclass(frozen=True)
class CountView:
    name: str
    m1_shape_per_boundary: int
    e1_shape_per_boundary: int
    interpretation: str
    consequence: str

    def depth(self, branch: str, frame_nodes: int = 3) -> int:
        if branch == "M1":
            return frame_nodes + 2 * self.m1_shape_per_boundary
        if branch == "E1":
            return frame_nodes + 2 * self.e1_shape_per_boundary
        raise ValueError(branch)


VIEWS = [
    CountView(
        name="component-relative count",
        m1_shape_per_boundary=1,
        e1_shape_per_boundary=2,
        interpretation="A d-component branch contributes d-1 scalar relative shape equations per boundary.",
        consequence="Gives M1 depth 5 and E1 depth 7.",
    ),
    CountView(
        name="projective-real count",
        m1_shape_per_boundary=2,
        e1_shape_per_boundary=2,
        interpretation="Both primitive M1 CP1 and E1 unit H1 directions have S2 projective tangent dimension 2.",
        consequence="Gives M1 depth 7 and E1 depth 7; destroys M1/E1 depth separation.",
    ),
    CountView(
        name="shared-projective count",
        m1_shape_per_boundary=1,
        e1_shape_per_boundary=2,
        interpretation=(
            "M1 CP1 orientation is identified with the common H1 frame nodes; "
            "only one primitive compact/radial relative scalar remains per boundary."
        ),
        consequence="Preserves M1 depth 5 while using CP1 only as the bridge into existing H1 nodes.",
    ),
]


def main() -> None:
    print("M1 projective-count tension")
    print("=" * 29)
    print("Issue:")
    print("  The primitive compact doublet maps to CP1=S2.")
    print("  CP1 has two real projective directions.")
    print("  But the current M1 closure depth uses d-1=1 shape equation per boundary.")
    print()

    for view in VIEWS:
        print(view.name)
        print(f"  M1 shape per boundary={view.m1_shape_per_boundary}")
        print(f"  E1 shape per boundary={view.e1_shape_per_boundary}")
        print(f"  M1 depth={view.depth('M1')}")
        print(f"  E1 depth={view.depth('E1')}")
        print(f"  interpretation: {view.interpretation}")
        print(f"  consequence:    {view.consequence}")
        print()

    print("Audit verdict:")
    print("  - The Hopf/CP1 bridge should not automatically add two new M1 shape")
    print("    equations on top of the three common H1 frame nodes.")
    print("  - To preserve the M1 depth 5 route, CP1 orientation must be the way M1")
    print("    joins the existing H1 frame closure, not an extra pair of shape nodes.")
    print("  - The remaining M1-specific shape equation is then the primitive compact")
    print("    doublet's one relative scalar/radial closure per boundary.")
    print("  - This must be checked in the boundary action; otherwise M1 and E1")
    print("    collapse to the same depth in the projective-real count.")


if __name__ == "__main__":
    main()

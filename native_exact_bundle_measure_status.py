from dataclasses import dataclass


@dataclass(frozen=True)
class BundleFact:
    name: str
    exact_statement: str
    depth_consequence: str
    status: str


FACTS = [
    BundleFact(
        name="CP1 / Hopf bridge",
        exact_statement="normalized C2 modulo common U(1) phase is CP1, and CP1 is S2",
        depth_consequence="Hopf bilinears merge into the common H1/S2 frame; they do not add a second orientation frame",
        status="exact topology/geometry",
    ),
    BundleFact(
        name="CP1 measure pushforward",
        exact_statement="Fubini-Study measure on CP1 pushes to the round S2 measure",
        depth_consequence="bare M1 projective geometry has no anisotropic extra weighting",
        status="exact standard CP1/S2 measure fact",
    ),
    BundleFact(
        name="H1/S2 second moment",
        exact_statement="<n_a n_b> = delta_ab/3",
        depth_consequence="gives eta projection; does not create three unconstrained depth nodes",
        status="exact round-S2 integral",
    ),
    BundleFact(
        name="E1 relative-shape plane",
        exact_statement="R3 decomposes into common line span(1,1,1) plus a two-dimensional orthogonal relative plane",
        depth_consequence="supports two relative-shape coordinates per boundary if those boundaries are independent",
        status="exact linear algebra",
    ),
    BundleFact(
        name="relative-plane second moment",
        exact_statement="uniform unit circle in the relative plane has <u_i u_j> = delta_ij/2 in an orthonormal basis",
        depth_consequence="isotropic within relative shape; no branch correction by itself",
        status="exact circle integral",
    ),
]


def main() -> None:
    print("exact bundle/measure status")
    print("=" * 29)
    for fact in FACTS:
        print(fact.name)
        print(f"  exact statement:    {fact.exact_statement}")
        print(f"  depth consequence:  {fact.depth_consequence}")
        print(f"  status:             {fact.status}")
        print()

    print("No-approximation verdict:")
    print("  These are exact geometry/linear-algebra facts. They replace numerical")
    print("  measure probes as inputs to the current chain.")


if __name__ == "__main__":
    main()

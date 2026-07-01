from dataclasses import dataclass


@dataclass(frozen=True)
class AtlasEntry:
    name: str
    gr_math_role: str
    udt_relevance: str
    status: str


ENTRIES = [
    AtlasEntry(
        name="heat kernel / spectral semigroup",
        gr_math_role="uses exp(-t operator) and exact semigroup composition K(t1)K(t2)=K(t1+t2)",
        udt_relevance="directly matches a boundary operator L1 and exponential transfer structure",
        status="highest-priority atlas object",
    ),
    AtlasEntry(
        name="Dirichlet-to-Neumann map",
        gr_math_role="maps boundary values to normal derivatives for elliptic boundary problems",
        udt_relevance="P_phi0 is exactly a boundary momentum/normal-derivative condition at f=1",
        status="promising atlas object",
    ),
    AtlasEntry(
        name="Calderon projector / Cauchy data space",
        gr_math_role="splits allowable boundary Cauchy data and supports gluing formulas",
        udt_relevance="could formalize two-sided phi bridge as a boundary data split",
        status="promising but not derived",
    ),
    AtlasEntry(
        name="BFK determinant gluing",
        gr_math_role="factorizes determinants of operators on glued manifolds using boundary operators",
        udt_relevance="may explain composition of boundary spectra without inventing a force",
        status="caution: determinant factors can overdominate",
    ),
    AtlasEntry(
        name="Hamilton-Jacobi boundary functional",
        gr_math_role="on-shell action as a functional of boundary data; momenta are boundary derivatives",
        udt_relevance="C1 Pi_f is already an HJ-type boundary derivative",
        status="already partially used",
    ),
    AtlasEntry(
        name="corner / joint terms",
        gr_math_role="codimension-2 terms where boundary pieces meet",
        udt_relevance="phi0 is a radial/angular edge where scalar and angular data meet",
        status="promising but not yet enough",
    ),
    AtlasEntry(
        name="covariant phase space edge modes",
        gr_math_role="boundary degrees of freedom required by gauge/gravity symplectic structure",
        udt_relevance="could supply angular edge dynamics missing from scalar C1",
        status="open atlas object",
    ),
]


def main() -> None:
    print("GR boundary-kernel atlas")
    print("=" * 25)
    for entry in ENTRIES:
        print(entry.name)
        print(f"  GR/math role:  {entry.gr_math_role}")
        print(f"  UDT relevance: {entry.udt_relevance}")
        print(f"  status:        {entry.status}")
        print()

    print("Atlas verdict:")
    print("  The most direct GR-math pointer is spectral boundary-kernel theory:")
    print("  heat kernels, Dirichlet-to-Neumann maps, and gluing projectors.")
    print("  These are maps, not imported mechanisms; UDT still has to supply")
    print("  the actual phi0 boundary operator and action time.")


if __name__ == "__main__":
    main()

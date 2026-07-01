from dataclasses import dataclass


@dataclass(frozen=True)
class BridgeFact:
    name: str
    exact_statement: str
    relevance: str


FACTS = [
    BridgeFact(
        name="angular metric",
        exact_statement="g_AB = r^2 omega_AB on both phi signs",
        relevance="intrinsic S2 geometry is the shared interface arena",
    ),
    BridgeFact(
        name="angular Laplacian scaling",
        exact_statement="Delta_S2 = r^-2 Delta_unit",
        relevance="normalized operator -r^2 Delta_S2 is independent of r*",
    ),
    BridgeFact(
        name="angular eigenvalues",
        exact_statement="-r^2 Delta_S2 Y_lm = l(l+1) Y_lm",
        relevance="angular spectrum is invariant under scale changes and phi sign",
    ),
    BridgeFact(
        name="ell=1 bridge",
        exact_statement="L1=(-r^2 Delta_S2)/2 equals I3 on ell=1",
        relevance="lowest nonconstant angular identity sector is common to both sides",
    ),
    BridgeFact(
        name="phi0 interface",
        exact_statement="f=1 at phi0 while angular operator remains the same across the interface",
        relevance="negative-phi edge can couple to exterior/scalar background through angular invariants",
    ),
]


def main() -> None:
    print("angular invariant bridge between phi spaces")
    print("=" * 45)
    for fact in FACTS:
        print(fact.name)
        print(f"  exact statement: {fact.exact_statement}")
        print(f"  relevance:       {fact.relevance}")
        print()

    print("Bridge verdict:")
    print("  The angular spectrum is the natural bridge between negative-phi")
    print("  matter space and the positive-phi/scalar background because the")
    print("  normalized angular operators are invariant under r* and phi sign.")


if __name__ == "__main__":
    main()

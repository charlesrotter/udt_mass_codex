from dataclasses import dataclass


@dataclass(frozen=True)
class MirrorFact:
    name: str
    exact_statement: str
    consequence: str


FACTS = [
    MirrorFact(
        name="inside-out phi mirror",
        exact_statement="phi -> -phi swaps the positive-phi and negative-phi radial/time weights",
        consequence="matter-side and gravity/scalar-side sectors are related by the same metric form",
    ),
    MirrorFact(
        name="angular invariance under phi mirror",
        exact_statement="g_AB=r^2 omega_AB is unchanged by phi -> -phi",
        consequence="the intrinsic angular spectrum is common to both sides",
    ),
    MirrorFact(
        name="phi0 fixed surface",
        exact_statement="at phi=0, f=e^{-2phi}=1",
        consequence="both phi signs meet at the same angular geometry and flat radial value",
    ),
    MirrorFact(
        name="normalized angular operator",
        exact_statement="-r^2 Delta_S2 has eigenvalues l(l+1), independent of phi",
        consequence="angular modes can carry information across the phi-sign interface",
    ),
    MirrorFact(
        name="ell=1 identity bridge",
        exact_statement="L1=(-r^2 Delta_S2)/2=I3 on ell=1",
        consequence="the lowest nonconstant angular identity sector is shared by both phi sides",
    ),
]


def main() -> None:
    print("phi-sign mirror bridge audit")
    print("=" * 30)
    for fact in FACTS:
        print(fact.name)
        print(f"  exact statement: {fact.exact_statement}")
        print(f"  consequence:     {fact.consequence}")
        print()

    print("Mirror verdict:")
    print("  The two-sided bridge is native at the level of metric geometry:")
    print("  phi changes radial/time weights, while the normalized angular")
    print("  spectrum remains the common invariant across both phi signs.")


if __name__ == "__main__":
    main()

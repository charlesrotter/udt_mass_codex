from dataclasses import dataclass


@dataclass(frozen=True)
class Realm:
    name: str
    metric_role: str
    bridge_requirement: str


REALMS = [
    Realm(
        name="negative phi realm",
        metric_role="matter-side existence region; finite-action negative-phi cells live here",
        bridge_requirement="must remain accessible through phi0 rather than becoming a disconnected sheet",
    ),
    Realm(
        name="positive phi realm",
        metric_role="scalar/background support on which matter is externally/macroscopically accessible",
        bridge_requirement="must receive matter information without importing the negative-phi radial scale",
    ),
    Realm(
        name="phi=0 surface",
        metric_role="asymptotic-normalization / neutral bridge where f=1",
        bridge_requirement="must cancel exterior tail while preserving admissible interior first jet",
    ),
    Realm(
        name="scale-invariant angular sector",
        metric_role="common S2 spectrum with normalized operator -r^2 Delta_S2",
        bridge_requirement="carries labels across phi sign and scale changes",
    ),
]


def main() -> None:
    print("phi realm ontology bridge")
    print("=" * 27)
    for realm in REALMS:
        print(realm.name)
        print(f"  metric role:        {realm.metric_role}")
        print(f"  bridge requirement: {realm.bridge_requirement}")
        print()

    print("Exact bridge facts:")
    print("  g_AB = r^2 omega_AB is phi-blind")
    print("  -r^2 Delta_S2 has eigenvalues ell(ell+1), independent of r scale")
    print("  L1=(-r^2 Delta_S2)/2 equals I3 on ell=1")
    print("  phi=0 gives f=1, the common normalization surface")
    print()
    print("Ontology verdict:")
    print("  Matter belongs to negative phi.")
    print("  Positive phi is the scalar/macroscopic support realm.")
    print("  The scale-invariant angular sector is the native bridge that lets")
    print("  negative-phi matter be present in the macro-accessible realm.")
    print()
    print("Proof implication:")
    print("  The source inventory of the elementary phi0 bridge should be built")
    print("  from angular invariants and first-jet matching, not from a radial")
    print("  mechanism imported from either side alone.")


if __name__ == "__main__":
    main()

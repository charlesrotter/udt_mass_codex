from dataclasses import dataclass


@dataclass(frozen=True)
class ShapeSector:
    name: str
    dimension: int

    @property
    def nonscalar_modes(self) -> int:
        return max(0, self.dimension - 1)

    @property
    def independent_boundary_terms(self) -> int:
        return 2 * self.nonscalar_modes


def main() -> None:
    print("Two-boundary independence audit")
    print("=" * 32)
    print("For any local quadratic shape action on a finite radial interval:")
    print("  S_shape = integral L(q_a, q_a') dr")
    print("the variation contains endpoint terms:")
    print("  [ Pi_a delta q_a ]_core^phi0")
    print("  = Pi_a(phi0) delta q_a(phi0) - Pi_a(core) delta q_a(core)")
    print()
    print("Unless a separate matching condition ties the two endpoint variations,")
    print("delta q_a(core) and delta q_a(phi0) are independent boundary data.")
    print()

    sectors = [
        ShapeSector("O0", 1),
        ShapeSector("M1", 2),
        ShapeSector("E1", 3),
        ShapeSector("M2", 5),
    ]

    for sector in sectors:
        print(sector.name)
        print(f"  dimension d={sector.dimension}")
        print(f"  nonscalar shape modes d-1={sector.nonscalar_modes}")
        print(f"  two-boundary shape constraints=2(d-1)={sector.independent_boundary_terms}")

    print("\nAudit verdict:")
    print("  - The factor 2 in N+2(d-1) is variationally natural for local")
    print("    finite-cell shape data.")
    print("  - This supports independent core-side and phi=0 shape closure.")
    print("  - It does not prove epsilon mediation or the shared gamma weight.")
    print("  - If a future metric condition ties the two endpoints, the count collapses")
    print("    from 2(d-1) to d-1 and the current ladder would fail.")


if __name__ == "__main__":
    main()

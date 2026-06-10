from dataclasses import dataclass


@dataclass(frozen=True)
class Region:
    name: str
    spatial_form: str
    boundary_components: str
    composition_consequence: str


REGIONS = [
    Region(
        name="single negative-phi cell with regularized/excised core",
        spatial_form="[core, phi0] x S2",
        boundary_components="core-side S2 plus phi0 S2",
        composition_consequence="at most two radial boundary components before adding bundle variables",
    ),
    Region(
        name="single negative-phi cell with singular endpoint not treated as boundary",
        spatial_form="(0, phi0] x S2 with singular endpoint",
        boundary_components="phi0 S2 only",
        composition_consequence="only one explicit radial edge quantum",
    ),
    Region(
        name="two cells glued at a shared boundary",
        spatial_form="[a,b] x S2 union [b,c] x S2",
        boundary_components="shared b boundary is internal after gluing",
        composition_consequence="shared variables merge; boundary action should not be double-counted",
    ),
    Region(
        name="disconnected cells",
        spatial_form="disjoint union of intervals x S2",
        boundary_components="boundary components add over disconnected pieces",
        composition_consequence="actions can add if cells are independent",
    ),
]


def main() -> None:
    print("boundary topology composition audit")
    print("=" * 37)
    for region in REGIONS:
        print(region.name)
        print(f"  spatial form:             {region.spatial_form}")
        print(f"  boundary components:      {region.boundary_components}")
        print(f"  composition consequence:  {region.composition_consequence}")
        print()

    print("Topology verdict:")
    print("  A single spherical metric cell does not provide arbitrary radial")
    print("  transfer-node depth. Repeated nodes require either disconnected cells,")
    print("  independent boundary/bundle variables, or an explicit edge graph.")


if __name__ == "__main__":
    main()

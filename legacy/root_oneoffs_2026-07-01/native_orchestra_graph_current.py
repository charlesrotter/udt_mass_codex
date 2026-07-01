from dataclasses import dataclass


@dataclass(frozen=True)
class Instrument:
    name: str
    native_status: str
    role: str


@dataclass(frozen=True)
class Coupling:
    source: str
    target: str
    status: str
    result: str
    risk: str


INSTRUMENTS = [
    Instrument(
        "negative_phi_endpoint",
        "metric/action native",
        "Creates finite-action endpoint arena and self-similar p=1/3 condition.",
    ),
    Instrument(
        "phi0_interface",
        "metric native",
        "Supplies scalar boundary jump B=p/2.",
    ),
    Instrument(
        "round_S2_H1",
        "metric native",
        "Supplies N=3 lowest non-scalar frame and isotropic projection.",
    ),
    Instrument(
        "compact_U1_primitive",
        "conditional topology",
        "Selects primitive M1 doublet if nontrivial compact bundle is occupied.",
    ),
    Instrument(
        "Hopf_projective_bridge",
        "topology/geometry native once compact doublet exists",
        "Maps primitive compact doublet modulo phase to CP1=S2/H1 data.",
    ),
    Instrument(
        "symmetric_transfer_kernel",
        "composition native",
        "Assigns eta/2 to one side of a composable boundary transfer.",
    ),
    Instrument(
        "two_boundary_variation",
        "local action native",
        "Makes core-side and phi0-side shape boundary data independent unless tied.",
    ),
    Instrument(
        "closure_factor_graph",
        "open",
        "Decides whether closure nodes are independent physical kernel factors.",
    ),
]

COUPLINGS = [
    Coupling(
        "negative_phi_endpoint",
        "phi0_interface",
        "derived",
        "p=1/3 gives B=1/6.",
        "Requires C1 action and self-similar closure condition.",
    ),
    Coupling(
        "phi0_interface",
        "round_S2_H1",
        "derived if closure observable is n_a",
        "B <n_a n_b> = (1/18) delta_ab.",
        "Fails if boundary observable is anisotropic or scalar-only.",
    ),
    Coupling(
        "round_S2_H1",
        "symmetric_transfer_kernel",
        "conditional",
        "gamma=3 exp(-1/36).",
        "Requires closure constraints to be represented by composable kernels.",
    ),
    Coupling(
        "compact_U1_primitive",
        "Hopf_projective_bridge",
        "derived conditional on compact doublet",
        "primitive doublet / U(1) phase = CP1=S2.",
        "Still does not force nontrivial compact bundle occupation.",
    ),
    Coupling(
        "Hopf_projective_bridge",
        "round_S2_H1",
        "derived geometrically",
        "M1 compact shape can be read as H1/projective boundary data.",
        "Boundary action must use phase-invariant bilinears.",
    ),
    Coupling(
        "two_boundary_variation",
        "closure_factor_graph",
        "supported",
        "Provides two endpoint shape data sets.",
        "May collapse if a matching condition ties endpoints.",
    ),
    Coupling(
        "round_S2_H1",
        "closure_factor_graph",
        "partly supported",
        "H1 rank is physical if non-scalar boundary sectors are allowed.",
        "May collapse under singlet-only elementary closure.",
    ),
    Coupling(
        "symmetric_transfer_kernel",
        "closure_factor_graph",
        "open",
        "Each independent closure node would contribute one gamma.",
        "Granularity/independence not yet derived.",
    ),
]


def main() -> None:
    print("Current native orchestra graph")
    print("=" * 31)
    print("Instruments:")
    for item in INSTRUMENTS:
        print(f"  - {item.name}")
        print(f"    status: {item.native_status}")
        print(f"    role:   {item.role}")

    print("\nCouplings:")
    for edge in COUPLINGS:
        print(f"  {edge.source} -> {edge.target}")
        print(f"    status: {edge.status}")
        print(f"    result: {edge.result}")
        print(f"    risk:   {edge.risk}")

    print("\nOrchestra verdict:")
    print("  The strongest current pattern is not one mechanism.")
    print("  It is a coupled boundary graph:")
    print("    endpoint self-similarity supplies p")
    print("    interface geometry supplies B")
    print("    S2 isotropy supplies eta")
    print("    transfer composition supplies eta/2")
    print("    compact projective topology lets M1 play in the same H1 frame")
    print("    two-boundary variation supplies shape closure locations")
    print("  The open question is whether these couplings form independent")
    print("  physical closure nodes rather than a correlated/global block.")


if __name__ == "__main__":
    main()

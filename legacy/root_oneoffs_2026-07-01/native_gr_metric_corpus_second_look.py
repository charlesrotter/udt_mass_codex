from dataclasses import dataclass


@dataclass(frozen=True)
class GRTool:
    name: str
    udt_use: str
    status: str
    guardrail: str


TOOLS = [
    GRTool(
        name="Israel junction conditions",
        udt_use=(
            "exact thin-interface bookkeeping for jumps in extrinsic curvature; "
            "already matches the phi0 angular shell-stress signature"
        ),
        status="already useful",
        guardrail="do not import Einstein matter sourcing; use only the metric jump algebra",
    ),
    GRTool(
        name="ADM / Schwarzschild tail mass",
        udt_use=(
            "mathematical map between the 1/r tail coefficient and a conserved "
            "radial integration constant"
        ),
        status="already useful",
        guardrail="in UDT this is a tail/momentum diagnostic, not ordinary matter source mass",
    ),
    GRTool(
        name="Gibbons-Hawking-York boundary term",
        udt_use=(
            "reminder that a metric variational principle is incomplete unless "
            "boundary variations are controlled"
        ),
        status="promising target",
        guardrail="must derive any UDT boundary term from the native action/metric, not append EH action",
    ),
    GRTool(
        name="Brown-York quasilocal stress",
        udt_use=(
            "organizes boundary energy, pressure, and momentum on finite S2 collars"
        ),
        status="promising target",
        guardrail="use as a template for variables; derive UDT values from C1/angular terms",
    ),
    GRTool(
        name="corner / joint terms",
        udt_use=(
            "codimension-2 boundary contributions where radial and angular boundaries meet; "
            "a natural place for phi0 collar data to live"
        ),
        status="high-priority target",
        guardrail="must produce the exact C1 conjugate momentum q/2 after scale normalization",
    ),
    GRTool(
        name="Gauss-Codazzi constraints",
        udt_use=(
            "relates intrinsic S2 curvature, extrinsic curvature, and boundary constraints"
        ),
        status="promising target",
        guardrail="look for missing angular scalar/constraint; do not force Einstein equations",
    ),
    GRTool(
        name="mixed Robin boundary conditions",
        udt_use=(
            "classifies nonzero phi0 slope as a conjugate boundary condition rather "
            "than a bulk force"
        ),
        status="already useful",
        guardrail="classification is not derivation; it does not explain why q=1/3",
    ),
    GRTool(
        name="covariant phase space / edge modes",
        udt_use=(
            "boundary degrees of freedom can appear when gauge/metric symmetries meet a boundary"
        ),
        status="promising target",
        guardrail="H1 nodes may be edge variables only if their symplectic role is derived",
    ),
    GRTool(
        name="horizon and trapped-surface mechanics",
        udt_use="useful negative check for surface-gravity style structures",
        status="mostly diagnostic",
        guardrail="phi0 has f=1, not a horizon; do not force horizon thermodynamics",
    ),
    GRTool(
        name="domain walls / branes",
        udt_use="thin-shell language for surface tension analogies",
        status="import risk",
        guardrail="reject as mechanism unless its stress follows from UDT boundary geometry",
    ),
    GRTool(
        name="linearized perturbation theory",
        udt_use="local sanity checks and exploratory estimates",
        status="diagnostic only",
        guardrail="no approximation-based conclusions in the final chain",
    ),
]


def main() -> None:
    print("GR metric-corpus second-look inventory")
    print("=" * 43)
    print("Use GR as a mathematical atlas, not as a mechanism import.")
    print()
    for tool in TOOLS:
        print(tool.name)
        print(f"  UDT use:   {tool.udt_use}")
        print(f"  status:    {tool.status}")
        print(f"  guardrail: {tool.guardrail}")
        print()

    print("Priority conclusion:")
    print("  The best GR-derived search targets are not bulk Einstein sourcing.")
    print("  They are variational completion, quasilocal boundary momentum,")
    print("  junction stress, corner/joint terms, and possible edge modes.")


if __name__ == "__main__":
    main()

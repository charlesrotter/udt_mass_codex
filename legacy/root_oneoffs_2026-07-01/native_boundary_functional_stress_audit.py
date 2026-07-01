from dataclasses import dataclass


@dataclass(frozen=True)
class BoundaryFunctional:
    name: str
    variation_pattern: str
    native_status: str
    target_match: str
    risk: str


FUNCTIONALS = [
    BoundaryFunctional(
        name="area term on timelike shell",
        variation_pattern="proportional to full induced metric h_ab",
        native_status="geometric but would be an added brane tension unless derived",
        target_match="poor: includes time component",
        risk="imports a wall-like mechanism",
    ),
    BoundaryFunctional(
        name="S2 area term only",
        variation_pattern="angular metric variation only",
        native_status="possible if phi0 interface action is defined on spatial linking S2",
        target_match="good angular pattern",
        risk="must explain why time direction is excluded",
    ),
    BoundaryFunctional(
        name="Gibbons-Hawking-York / extrinsic curvature term",
        variation_pattern="cancels normal-derivative variations; leaves Brown-York-like boundary stress",
        native_status="standard metric variational boundary structure",
        target_match="promising but needs exact UDT C1 analogue",
        risk="may cancel rather than create the jump if used with smooth matching",
    ),
    BoundaryFunctional(
        name="corner / joint term at phi0 collar",
        variation_pattern="localized at intersection of radial cell and S2 boundary; can be angular",
        native_status="geometric when boundaries meet non-smoothly",
        target_match="strong candidate for angular-only interface action",
        risk="requires deriving the correct UDT joint term, not borrowing GR blindly",
    ),
    BoundaryFunctional(
        name="intrinsic S2 curvature integral",
        variation_pattern="topological in 2D for fixed topology; no local stress in pure form",
        native_status="Gauss-Bonnet native but dynamically inert locally",
        target_match="weak for stress; useful for topology/selection",
        risk="cannot create local shell stress by itself",
    ),
    BoundaryFunctional(
        name="H1 trace constraint action",
        variation_pattern="trace-subtracted angular projector stress",
        native_status="compatible with S2/H1 boundary variables",
        target_match="good if derived from constraint variation",
        risk="currently conditional; could become a postulate if not derived",
    ),
]


def main() -> None:
    print("Boundary functional stress audit")
    print("=" * 32)
    print("Target: angular-only phi0 interface stress with no time component.")
    print()
    for fn in FUNCTIONALS:
        print(fn.name)
        print(f"  variation pattern: {fn.variation_pattern}")
        print(f"  native status:     {fn.native_status}")
        print(f"  target match:      {fn.target_match}")
        print(f"  risk:              {fn.risk}")
        print()

    print("Functional verdict:")
    print("  - Full shell area/tension is a poor match because it includes time.")
    print("  - Pure intrinsic S2 curvature is topological and likely not enough.")
    print("  - Best second-look targets are:")
    print("      1. UDT/C1 boundary or joint term at phi0,")
    print("      2. S2-only interface action,")
    print("      3. derived H1 trace-constraint action.")
    print("  - These are metric boundary mechanisms, not conventional forces.")


if __name__ == "__main__":
    main()

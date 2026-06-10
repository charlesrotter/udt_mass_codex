from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    category: str
    status: str
    reason: str


ITEMS = [
    Item(
        category="connection / curvature identities",
        status="usable exactly",
        reason="they follow from the metric tensor itself, independent of field equations",
    ),
    Item(
        category="extrinsic curvature and shell-jump algebra",
        status="usable exactly as geometry",
        reason="junction bookkeeping follows from how hypersurfaces embed in the metric",
    ),
    Item(
        category="Einstein equations as source equations",
        status="not imported",
        reason="UDT treats the metric as definitional positional dilation, not matter-sourced GR",
    ),
    Item(
        category="Einstein-Hilbert action as dynamics",
        status="not imported",
        reason="UDT uses the C1 positional-dilation scalar action for phi dynamics",
    ),
    Item(
        category="GHY / Brown-York boundary objects",
        status="atlas only until native derivation",
        reason="they identify boundary variables, but UDT may assign different action weights",
    ),
    Item(
        category="ADM mass / quasilocal energy",
        status="diagnostic only",
        reason="UDT tail constants are scale/momentum diagnostics, not ordinary GR sourced mass",
    ),
    Item(
        category="horizon thermodynamics",
        status="not applicable at phi0",
        reason="phi0 has f=1 and is not a horizon",
    ),
    Item(
        category="energy conditions / domain-wall dynamics",
        status="import risk",
        reason="they assume GR matter-source interpretation rather than UDT positional dilation",
    ),
]


def main() -> None:
    print("Positional-dilation guardrail for GR math")
    print("=" * 45)
    print("Use GR as a metric-geometry atlas, not as the UDT dynamics.")
    print()
    for item in ITEMS:
        print(item.category)
        print(f"  status: {item.status}")
        print(f"  reason: {item.reason}")
        print()

    print("Operational rule:")
    print("  A GR result may be used directly only if it is a tensor/geometric")
    print("  identity of the metric. If it depends on the Einstein-Hilbert action,")
    print("  Einstein source equations, or GR boundary normalization, it becomes")
    print("  a candidate map that must be re-derived from UDT's C1/angular action.")


if __name__ == "__main__":
    main()

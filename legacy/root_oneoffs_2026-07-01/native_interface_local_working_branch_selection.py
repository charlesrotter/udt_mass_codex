from dataclasses import dataclass


@dataclass(frozen=True)
class Signal:
    name: str
    localization: str
    implication: str


SIGNALS = [
    Signal(
        "C1 momentum jump",
        "localized at phi0 when the exterior tail is flat",
        "supports an interface-local eta carrier",
    ),
    Signal(
        "distributional curvature jump",
        "delta-supported at the slope discontinuity",
        "supports a joint/interface reading",
    ),
    Signal(
        "Brown-York angular stress",
        "nonzero angular stress at f=1 with zero subtracted value energy",
        "supports angular boundary action rather than bulk propagation",
    ),
    Signal(
        "H1 angular identity",
        "intrinsic to the phi-blind S2 angular sector",
        "supports an interface H1 kernel if the scalar eta is supplied",
    ),
    Signal(
        "warped DtN map",
        "depends on propagation through the negative-phi collar profile",
        "kept as discriminator, not the working branch unless action requires bulk elimination",
    ),
]


def main() -> None:
    print("interface-local working branch selection")
    print("=" * 42)
    for signal in SIGNALS:
        print(signal.name)
        print(f"  localization: {signal.localization}")
        print(f"  implication:  {signal.implication}")
        print()

    print("Selection:")
    print("  Use interface-local H1 transfer as the active-lane working branch.")
    print()
    print("Guardrail:")
    print("  This is not a derivation of P_transfer. It only chooses which")
    print("  conditional branch to develop first. The warped DtN branch remains")
    print("  exact and available if the action is later shown to be bulk-eliminated.")


if __name__ == "__main__":
    main()

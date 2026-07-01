from dataclasses import dataclass


@dataclass(frozen=True)
class Step:
    name: str
    exact_piece: str
    open_piece: str


STEPS = [
    Step(
        name="edge scalar",
        exact_piece="P_phi0 supplies eta=1/18 if banked",
        open_piece="derivation of P_phi0 if not banked",
    ),
    Step(
        name="angular kernel",
        exact_piece="L1=(-R^2 Delta_S2)/2 restricted to ell=1 equals I3",
        open_piece="none for I3 identity",
    ),
    Step(
        name="coupling",
        exact_piece="A_side=(eta/2)L1 would give the transfer kernel",
        open_piece="why the edge scalar couples as eta/2 to L1",
    ),
    Step(
        name="trace",
        exact_piece="Tr exp[-(eta/2)I3]=3 exp(-eta/2)",
        open_piece="why trace over channels is the physical composition operation",
    ),
]


def main() -> None:
    print("phi0-to-ell=1 coupling hypothesis")
    print("=" * 41)
    for step in STEPS:
        print(step.name)
        print(f"  exact piece: {step.exact_piece}")
        print(f"  open piece:  {step.open_piece}")
        print()

    print("Hypothesis:")
    print("  The phi0 edge quantum acts on the lowest nonconstant angular identity")
    print("  sector through the normalized ell=1 Laplacian kernel.")
    print()
    print("Status:")
    print("  This is a compact native coupling hypothesis, not a derivation.")


if __name__ == "__main__":
    main()

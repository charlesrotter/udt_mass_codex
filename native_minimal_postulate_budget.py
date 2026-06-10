from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    name: str
    status: str
    note: str


ITEMS = [
    Item(
        name="P0 metric",
        status="foundation",
        note="positional-dilation metric; already UDT foundation",
    ),
    Item(
        name="P_phi0",
        status="candidate minimal mass-emergence postulate",
        note="at phi0, -Pi_f/R=1/6, equivalently K_rad/K_S2=1/6",
    ),
    Item(
        name="electron anchor",
        status="allowed dimensionful anchor",
        note="sets the absolute mass scale only",
    ),
    Item(
        name="H1/S2 projection",
        status="derived geometry",
        note="<n_a n_b>=delta_ab/3",
    ),
    Item(
        name="finite C1 action branch filter",
        status="derived filter",
        note="rejects q=2/3 branch under constant s=1/9",
    ),
    Item(
        name="gamma=N exp(-eta/2)",
        status="still candidate transfer rule",
        note="compact diagnostic but transfer normalization not fully derived",
    ),
    Item(
        name="depth rule",
        status="still ansatz-bearing",
        note="typed edge/cascade depth not fully derived",
    ),
    Item(
        name="branch coefficient ratios",
        status="still diagnostic",
        note="not upgraded by P_phi0 alone",
    ),
]


def main() -> None:
    print("minimal postulate budget")
    print("=" * 25)
    for item in ITEMS:
        print(item.name)
        print(f"  status: {item.status}")
        print(f"  note:   {item.note}")
        print()

    print("Budget verdict:")
    print("  P_phi0 would be one small new postulate on top of P0 and the electron")
    print("  anchor. It resolves eta/q if accepted, but it does not canonize the")
    print("  full mass ladder without separate transfer/depth derivations.")


if __name__ == "__main__":
    main()

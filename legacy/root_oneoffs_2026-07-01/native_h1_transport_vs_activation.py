from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    name: str
    statement: str
    status: str
    consequence: str


ITEMS = [
    Item(
        "H1 transport",
        "L1=(-r^2 Delta_S2)/2 equals I3 on every linking S2",
        "metric-derived",
        "the H1 frame is available throughout the collar",
    ),
    Item(
        "H1 activation",
        "the radial f equation couples to H1 with source s=1/9",
        "not derived",
        "needed for q=1/3 fixed flow",
    ),
    Item(
        "H1 source constancy",
        "s(t) is independent of collar position",
        "conditional",
        "follows if activation coefficient is built only from normalized H1 geometry",
    ),
    Item(
        "H1 shell transfer",
        "same H1 frame receives localized phi0 jump/stress",
        "partly derived",
        "supports eta as interface-local transfer scale",
    ),
]


def main() -> None:
    print("H1 transport versus activation")
    print("=" * 34)
    for item in ITEMS:
        print(item.name)
        print(f"  statement:   {item.statement}")
        print(f"  status:      {item.status}")
        print(f"  consequence: {item.consequence}")
        print()

    print("No-approximation verdict:")
    print("  The metric derives H1 transport, not H1 activation.")
    print("  Source constancy follows only if the activation coefficient is")
    print("  itself built from normalized, phi-blind H1 geometry.")


if __name__ == "__main__":
    main()

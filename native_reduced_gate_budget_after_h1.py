from dataclasses import dataclass


@dataclass(frozen=True)
class Gate:
    name: str
    old_status: str
    new_status: str


GATES = [
    Gate(
        "q=1/3 / P_phi0",
        "banked minimal postulate",
        "conditional theorem from H1 self-consistency if p=q",
    ),
    Gate(
        "p=q",
        "part of self-similar assumption",
        "equivalent to delta_h=0; supported by constant H1 source plus finite action",
    ),
    Gate(
        "H1 selector",
        "plausible lowest nonconstant angular sector",
        "strengthened by exact ell=0 trivial-branch exclusion",
    ),
    Gate(
        "eta/2 side action",
        "plausible half-boundary convention",
        "conditional theorem from symmetric composable gluing",
    ),
    Gate(
        "factor 3",
        "channel multiplicity candidate",
        "dim H1 after ell=0 exclusion, if physical role is boundary-state count",
    ),
]


def main() -> None:
    print("reduced gate budget after H1")
    print("=" * 31)
    for gate in GATES:
        print(gate.name)
        print(f"  old status: {gate.old_status}")
        print(f"  new status: {gate.new_status}")
        print()

    print("Remaining irreducible gates:")
    print("  1. no collar source running: delta_h=0")
    print("  2. intrinsic/interface-local transfer action")
    print("  3. boundary-state counting rather than averaging")


if __name__ == "__main__":
    main()

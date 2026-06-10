from dataclasses import dataclass


@dataclass(frozen=True)
class Gate:
    gate: str
    previous_status: str
    updated_status: str
    remaining_gap: str


GATES = [
    Gate(
        "transfer action branch",
        "intrinsic boundary versus warped DtN unresolved",
        "intrinsic interface is active branch; warped DtN is alternative bulk-propagation branch",
        "prove phi0 transfer is interface-local from the exact Calderon projector",
    ),
    Gate(
        "double counting",
        "guardrail only",
        "explicitly rejects multiplying intrinsic transfer by warped DtN for same H1 crossing",
        "identify any separate physical event before using both",
    ),
    Gate(
        "gamma kernel",
        "conditional P_transfer",
        "metric-composed first form gives gamma under internal phi0 interface reading",
        "derive q selection and exact projector",
    ),
    Gate(
        "warped DtN",
        "competing transfer possibility",
        "retained as collar response / possible correction, not active gamma transfer",
        "derive when bulk propagation, rather than interface transfer, is the observed operation",
    ),
]


def main() -> None:
    print("plain-sight transfer branch update")
    print("=" * 36)
    for gate in GATES:
        print(gate.gate)
        print(f"  previous status: {gate.previous_status}")
        print(f"  updated status:  {gate.updated_status}")
        print(f"  remaining gap:   {gate.remaining_gap}")
        print()

    print("Update verdict:")
    print("  The active lane should now be: intrinsic phi0 interface transfer,")
    print("  with warped DtN reserved for bulk collar propagation or corrections.")


if __name__ == "__main__":
    main()

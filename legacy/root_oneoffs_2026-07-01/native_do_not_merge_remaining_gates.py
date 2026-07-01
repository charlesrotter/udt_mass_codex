from dataclasses import dataclass


@dataclass(frozen=True)
class Gate:
    name: str
    why_not_merged: str
    status: str


GATES = [
    Gate(
        "P_phi0 / q=1/3",
        "H1 operator equivalence does not select the scalar edge slope q",
        "banked",
    ),
    Gate(
        "symmetric side split",
        "full H1 value action and one-sided transfer are different composition levels",
        "conditional P_transfer",
    ),
    Gate(
        "trace interpretation",
        "an operator on H1 does not automatically mean the physical operation is a trace",
        "conditional P_transfer",
    ),
    Gate(
        "typed depth",
        "H1 identity action does not prove independent repeated nodes",
        "conditional P_depth",
    ),
    Gate(
        "M1/M2/E1 coefficients",
        "H1 restriction does not compute the typed second jet",
        "open Tier D",
    ),
    Gate(
        "bulk DtN branch",
        "interface-local H1 merge and bulk propagation are alternative branches for the same variable",
        "kept separate",
    ),
]


def main() -> None:
    print("do-not-merge remaining gates")
    print("=" * 30)
    for gate in GATES:
        print(gate.name)
        print(f"  why not merged: {gate.why_not_merged}")
        print(f"  status:         {gate.status}")
        print()

    print("No-overmerge verdict:")
    print("  The forced merge is only eta-I3/L1-on-H1.")
    print("  Transfer, depth, coefficients, and q-origin remain separate gates.")


if __name__ == "__main__":
    main()

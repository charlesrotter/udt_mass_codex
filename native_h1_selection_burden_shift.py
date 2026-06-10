from dataclasses import dataclass


@dataclass(frozen=True)
class Gate:
    name: str
    before_simplification: str
    after_simplification: str
    status: str


GATES = [
    Gate(
        "full-S2 operator selection",
        "derive why S0_full uses eta L1 rather than eta I, eta nn^T, or another operator",
        "not needed for the trace if H1 is independently selected",
        "burden reduced",
    ),
    Gate(
        "H1 transfer-space selection",
        "needed but partly obscured by eta L1 language",
        "central gate: why exactly the ell=1 triplet carries the transfer",
        "still open/conditional",
    ),
    Gate(
        "constant-mode exclusion",
        "one reason to prefer L1 over I on the full S2",
        "becomes part of H1 selection rather than part of coefficient coupling",
        "supported by exact ell=0 endpoint exclusion",
    ),
    Gate(
        "isotropic angular value action",
        "had to be eta L1 on full S2",
        "can be eta I3 on H1",
        "supported by angular-only shell stress after projection, but value-action status still conditional",
    ),
    Gate(
        "side split and trace",
        "unchanged",
        "still requires composable side kernel and trace interpretation",
        "conditional P_transfer",
    ),
]


def main() -> None:
    print("H1 selection burden shift")
    print("=" * 27)
    for gate in GATES:
        print(gate.name)
        print(f"  before: {gate.before_simplification}")
        print(f"  after:  {gate.after_simplification}")
        print(f"  status: {gate.status}")
        print()

    print("Burden-shift verdict:")
    print("  The coupling problem may reduce to H1 selection plus isotropic")
    print("  angular value action. This is progress, but it does not derive")
    print("  P_transfer or typed-depth factorization.")


if __name__ == "__main__":
    main()

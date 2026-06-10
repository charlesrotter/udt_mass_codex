from dataclasses import dataclass
from fractions import Fraction
import math


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


@dataclass(frozen=True)
class Gate:
    name: str
    status: str
    consequence: str


ETA = Fraction(1, 18)
SIDE = ETA / 2
GAMMA = 3.0 * math.exp(-float(SIDE))


GATES = [
    Gate(
        "H1 selected transfer space",
        "conditional on ell=0 exclusion / lowest nonconstant bridge",
        "dim H1=3",
    ),
    Gate(
        "scalar side action",
        "conditional on symmetric composable boundary gluing",
        "A_side scalar=eta/2=1/36",
    ),
    Gate(
        "identity kernel on H1",
        "conditional on interface-local scalar-to-angular coupling",
        "A_side|H1=(1/36) I3",
    ),
    Gate(
        "trace interpretation",
        "conditional on unlabelled H1 boundary-state count",
        "Tr_H1 exp[-(1/36)I3]=3 exp(-1/36)",
    ),
    Gate(
        "node multiplication",
        "not supplied by P_transfer alone",
        "needed before gamma powers or typed-depth ladders are claimed",
    ),
]


def main() -> None:
    print("P_transfer active-lane status")
    print("=" * 29)
    print(f"eta={fmt(ETA)}")
    print(f"side action={fmt(SIDE)}")
    print(f"gamma_simple={GAMMA:.12g}")
    print()
    for gate in GATES:
        print(gate.name)
        print(f"  status:      {gate.status}")
        print(f"  consequence: {gate.consequence}")
        print()

    print("Status verdict:")
    print("  P_transfer is bankable as the second active-lane postulate.")
    print("  If banked, gamma=3 exp(-1/36) is exact inside the interface-local")
    print("  branch. It still does not derive typed depth or branch coefficients.")


if __name__ == "__main__":
    main()

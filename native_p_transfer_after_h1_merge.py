from dataclasses import dataclass
from fractions import Fraction
import math


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


ETA = Fraction(1, 18)
SIDE = ETA / 2
GAMMA = 3.0 * math.exp(-float(SIDE))


@dataclass(frozen=True)
class Gate:
    name: str
    revised_status: str
    consequence: str


GATES = [
    Gate(
        "H1 identity value action",
        "merged object if H1 selected and isotropic value-action status is derived/banked",
        "S0_full|H1=eta I3",
    ),
    Gate(
        "side split",
        "conditional on symmetric composable boundary action",
        "A_side|H1=(eta/2)I3",
    ),
    Gate(
        "trace operation",
        "conditional on unlabelled H1 boundary-state count",
        "gamma=3 exp(-eta/2)",
    ),
    Gate(
        "node product",
        "not supplied by P_transfer",
        "needed before gamma powers are licensed",
    ),
]


def main() -> None:
    print("P_transfer after H1 merge")
    print("=" * 27)
    print(f"eta={fmt(ETA)}")
    print(f"eta/2={fmt(SIDE)}")
    print(f"gamma={GAMMA:.12g}")
    print()
    for gate in GATES:
        print(gate.name)
        print(f"  revised status: {gate.revised_status}")
        print(f"  consequence:    {gate.consequence}")
        print()

    print("Transfer verdict:")
    print("  P_transfer no longer needs a separate full-S2 eta-L1 coupling.")
    print("  It still needs value-action status, side composability, trace, and")
    print("  later node-product structure.")


if __name__ == "__main__":
    main()

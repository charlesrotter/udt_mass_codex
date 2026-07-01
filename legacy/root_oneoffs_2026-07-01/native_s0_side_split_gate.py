from dataclasses import dataclass
from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


ETA = Fraction(1, 18)


@dataclass(frozen=True)
class Gate:
    name: str
    status: str
    consequence: str


GATES = [
    Gate(
        "full boundary action exists",
        "not yet derived",
        "needed before a side split has anything to split",
    ),
    Gate(
        "two-sided composability",
        "conditional boundary-kernel structure",
        "left side plus right side equals one full shared boundary action",
    ),
    Gate(
        "reflection symmetry",
        "natural if the two sides are the same boundary object",
        "left weight equals right weight",
    ),
    Gate(
        "side action",
        "exact after the previous gates",
        "S0_side=(eta/2)<a,L1 a>",
    ),
]


def main() -> None:
    print("S0 side-split gate")
    print("=" * 18)
    print(f"full scalar weight eta={fmt(ETA)}")
    print(f"side scalar weight eta/2={fmt(ETA / 2)}")
    print()
    for gate in GATES:
        print(gate.name)
        print(f"  status:      {gate.status}")
        print(f"  consequence: {gate.consequence}")
        print()

    print("Gate verdict:")
    print("  The half-factor is exact only after S0_full exists as a symmetric")
    print("  composable boundary action. It does not derive S0_full.")


if __name__ == "__main__":
    main()

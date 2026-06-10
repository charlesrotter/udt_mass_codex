from dataclasses import dataclass
from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


@dataclass(frozen=True)
class Operation:
    name: str
    expression: str
    result: str
    status: str


def main() -> None:
    eta = Fraction(1, 18)
    a = eta / 2
    ops = [
        Operation(
            "single prepared channel",
            "<m|exp(-a I3)|m>",
            "exp(-a)",
            "requires an external channel label or prepared direction",
        ),
        Operation(
            "unlabelled channel sum",
            "Tr_H1 exp(-a I3)",
            "3 exp(-a)",
            "valid if all H1 channels are accessible and no channel is selected",
        ),
        Operation(
            "normalized channel average",
            "(1/3) Tr_H1 exp(-a I3)",
            "exp(-a)",
            "valid if transfer is averaged rather than counted",
        ),
        Operation(
            "Gaussian determinant",
            "det(exp(-a I3))",
            "exp(-3a)",
            "different object; relevant only for determinant/path-integral measure",
        ),
    ]

    print("H1 trace operation audit")
    print("=" * 26)
    print(f"a = eta/2 = {fmt(a)}")
    print()
    for op in ops:
        print(op.name)
        print(f"  expression: {op.expression}")
        print(f"  result:     {op.result}")
        print(f"  status:     {op.status}")
        print()

    print("No-approximation verdict:")
    print("  The factor 3 comes from trace/counting over unlabelled H1 channels.")
    print("  It is not produced by a single channel, a normalized average, or a")
    print("  Gaussian determinant. The physical trace rule remains a gate.")


if __name__ == "__main__":
    main()

import math
from dataclasses import dataclass
from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


Q = Fraction(1, 3)
ETA = Q / 6
GAMMA = 3.0 * math.exp(-float(ETA / 2))
ELECTRON_MEV = 0.51099895


@dataclass(frozen=True)
class Layer:
    name: str
    status: str
    output: str


LAYERS = [
    Layer(
        name="P_phi0",
        status="banked minimal postulate",
        output="-Pi_f/R=1/6 -> q=1/3 -> eta=1/18",
    ),
    Layer(
        name="H1/S2 projection",
        status="derived geometry",
        output="<n_a n_b>=delta_ab/3",
    ),
    Layer(
        name="P_transfer",
        status="candidate second postulate",
        output="gamma=3 exp(-eta/2)",
    ),
    Layer(
        name="typed depths",
        status="not yet postulated here; diagnostic",
        output="M1=5, E1=7 in current graph",
    ),
    Layer(
        name="branch coefficients",
        status="diagnostic",
        output="current finite-cell coefficients only",
    ),
]


def main() -> None:
    print("two-postulate working model")
    print("=" * 29)
    print(f"eta = {fmt(ETA)}")
    print(f"gamma = {GAMMA:.12g}")
    print()
    for layer in LAYERS:
        print(layer.name)
        print(f"  status: {layer.status}")
        print(f"  output: {layer.output}")
        print()

    print("Model verdict:")
    print("  With P_phi0 and P_transfer banked, the ladder multiplier is fixed.")
    print("  The remaining non-canonized pieces are typed depths and branch")
    print("  coefficients. Do not call mass predictions derived until those are")
    print("  independently fixed or explicitly postulated.")


if __name__ == "__main__":
    main()

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
class ChainStep:
    step: str
    status: str
    output: str


STEPS = [
    ChainStep(
        "P_phi0 plus H1/S2 projection",
        "banked scalar slope plus exact projection",
        "eta=1/18",
    ),
    ChainStep(
        "H1 transfer-space selection",
        "supported by ell=0 exclusion and ell=1 first finite nonconstant bridge; still a gate",
        "transfer space H1 with dim=3",
    ),
    ChainStep(
        "forced H1 operator merge",
        "exact after H1 selection",
        "isotropic stress, eta L1|H1, and eta I3 are one object",
    ),
    ChainStep(
        "H1 full value action",
        "still requires value-action status",
        "S0_full|H1 = eta I3",
    ),
    ChainStep(
        "symmetric side split",
        "conditional P_transfer gluing",
        "A_side|H1=(eta/2)I3=(1/36)I3",
    ),
    ChainStep(
        "H1 trace",
        "conditional P_transfer trace interpretation",
        "gamma=Tr exp[-(1/36)I3]=3 exp(-1/36)",
    ),
]


def main() -> None:
    print("active chain after H1 merge")
    print("=" * 29)
    print(f"eta={fmt(ETA)}")
    print(f"eta/2={fmt(SIDE)}")
    print(f"gamma={GAMMA:.12g}")
    print()
    for step in STEPS:
        print(step.step)
        print(f"  status: {step.status}")
        print(f"  output: {step.output}")
        print()

    print("Chain verdict:")
    print("  The scalar-to-L1 product gate is replaced by a forced H1 identity")
    print("  merge. The remaining active gate is value-action status on H1,")
    print("  followed by optional P_transfer gluing and trace.")


if __name__ == "__main__":
    main()

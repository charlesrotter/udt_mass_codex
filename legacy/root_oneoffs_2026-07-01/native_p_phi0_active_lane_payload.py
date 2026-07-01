from dataclasses import dataclass
from fractions import Fraction
import math


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


Q = Fraction(1, 3)
BOUNDARY_UNIT = Q / 2
ETA = Q / 6
SIDE = ETA / 2
GAMMA_SIMPLE = 3.0 * math.exp(-float(SIDE))


@dataclass(frozen=True)
class Payload:
    item: str
    status: str
    value_or_rule: str


PAYLOADS = [
    Payload(
        "phi0 slope",
        "postulated by P_phi0",
        "q=1/3",
    ),
    Payload(
        "dimensionless boundary momentum/stress/slope-density unit",
        "exact consequence of metric identities plus P_phi0",
        "q/2=1/6",
    ),
    Payload(
        "H1/S2 projected eta",
        "exact consequence of round-S2 second moment",
        "eta=(q/2)/3=1/18",
    ),
    Payload(
        "one-sided action",
        "conditional on symmetric composable boundary gluing",
        "eta/2=1/36",
    ),
    Payload(
        "simple H1 trace multiplier",
        "conditional on P_transfer/interface-local identity kernel",
        "gamma=3 exp(-1/36)",
    ),
    Payload(
        "warped DtN multiplier",
        "separate conditional branch if transfer is literal bulk propagation",
        "gamma_warped=3 exp(-B/36), with B from exact self-similar DtN",
    ),
    Payload(
        "typed depths and branch coefficients",
        "not supplied by P_phi0",
        "must be derived or separately postulated before mass predictions are claimed",
    ),
]


def main() -> None:
    print("P_phi0 active-lane payload")
    print("=" * 28)
    print(f"q = {fmt(Q)}")
    print(f"q/2 = {fmt(BOUNDARY_UNIT)}")
    print(f"eta = {fmt(ETA)}")
    print(f"eta/2 = {fmt(SIDE)}")
    print(f"gamma_simple = {GAMMA_SIMPLE:.12g}")
    print()

    for payload in PAYLOADS:
        print(payload.item)
        print(f"  status:        {payload.status}")
        print(f"  value/rule:    {payload.value_or_rule}")
        print()

    print("Working verdict:")
    print("  In the active lane, P_phi0 is enough to derive eta exactly.")
    print("  It is not enough to claim gamma, typed depth, branch coefficients,")
    print("  or mass predictions without additional gates.")


if __name__ == "__main__":
    main()

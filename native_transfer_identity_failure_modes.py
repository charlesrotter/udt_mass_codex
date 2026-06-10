from dataclasses import dataclass


@dataclass(frozen=True)
class FailureMode:
    name: str
    consequence: str
    verdict: str


FAILURES = [
    FailureMode(
        name="nondegenerate channel actions",
        consequence="gamma becomes sum_i exp(-a_i), not 3 exp(-eta/2)",
        verdict="P_transfer rejected unless a_i are all eta/2",
    ),
    FailureMode(
        name="single normalized projector instead of channel trace",
        consequence="trace weight is one normalized share, not multiplicity three",
        verdict="3 factor rejected",
    ),
    FailureMode(
        name="full boundary action per side",
        consequence="single-step exponent is eta, not eta/2",
        verdict="half-factor rejected unless gluing/no-double-counting applies",
    ),
    FailureMode(
        name="correlated typed nodes",
        consequence="node weights do not multiply independently",
        verdict="depth exponent rejected or reduced",
    ),
    FailureMode(
        name="branch-dependent edge actions",
        consequence="one universal gamma fails",
        verdict="use branch-specific transfer or reject ladder",
    ),
]


def main() -> None:
    print("transfer identity failure modes")
    print("=" * 35)
    for failure in FAILURES:
        print(failure.name)
        print(f"  consequence: {failure.consequence}")
        print(f"  verdict:     {failure.verdict}")
        print()

    print("No-invention verdict:")
    print("  The transfer rule is fragile. It should be used only if these exact")
    print("  failure modes are ruled out by metric edge structure, not by observation.")


if __name__ == "__main__":
    main()

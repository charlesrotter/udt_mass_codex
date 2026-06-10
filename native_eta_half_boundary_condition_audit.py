from dataclasses import dataclass


@dataclass(frozen=True)
class HalfSource:
    name: str
    exact_rule: str
    applies_if: str
    verdict: str


SOURCES = [
    HalfSource(
        name="two-sided boundary kernel",
        exact_rule="full boundary action eta is split as eta/2 on each side",
        applies_if="the phi0-to-ell=1 coupling is a composable boundary kernel",
        verdict="valid source of eta/2 if boundary-kernel structure is present",
    ),
    HalfSource(
        name="interface jump alone",
        exact_rule="Delta Pi_f gives q/2 and eta after projection",
        applies_if="only C1 momentum jump is considered",
        verdict="does not by itself split eta into eta/2",
    ),
    HalfSource(
        name="single exterior boundary",
        exact_rule="one boundary component has one edge datum",
        applies_if="phi0 is treated as only an outer boundary, not a glued interface",
        verdict="no automatic half-factor",
    ),
    HalfSource(
        name="trace square-root convention",
        exact_rule="assign exp(-eta/2) so two sides multiply to exp(-eta)",
        applies_if="there is a symmetric transfer amplitude whose square gives boundary weight",
        verdict="valid only if amplitude/kernel interpretation is native",
    ),
]


def main() -> None:
    print("eta/2 boundary-condition audit")
    print("=" * 35)
    for source in SOURCES:
        print(source.name)
        print(f"  exact rule:  {source.exact_rule}")
        print(f"  applies if:  {source.applies_if}")
        print(f"  verdict:     {source.verdict}")
        print()

    print("Half-factor verdict:")
    print("  eta/2 is exact for a two-sided composable boundary kernel or native")
    print("  symmetric transfer amplitude. It is not derived by the edge quantum")
    print("  alone. The missing condition is kernel/amplitude structure at phi0.")


if __name__ == "__main__":
    main()

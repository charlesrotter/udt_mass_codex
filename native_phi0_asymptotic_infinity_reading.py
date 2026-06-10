from dataclasses import dataclass


@dataclass(frozen=True)
class Feature:
    name: str
    statement: str
    implication: str


FEATURES = [
    Feature(
        name="Schwarzschild normalization",
        statement="For an asymptotically flat Schwarzschild-type exterior, f -> 1 at spatial infinity.",
        implication="phi=-1/2 ln f -> 0 at infinity.",
    ),
    Feature(
        name="not a horizon",
        statement="A Schwarzschild horizon is f=0, not f=1.",
        implication="phi0 is an infinity/normalization-like surface, not horizon-like.",
    ),
    Feature(
        name="negative-mass / negative-phi branch",
        statement="For f=1+a/r with a>0, phi<0 and phi -> 0 as r -> infinity.",
        implication="the negative-phi well also approaches phi0 as its asymptotic normalization.",
    ),
    Feature(
        name="finite phi0 bridge",
        statement="A finite cell with f=1 at phi0 imposes the asymptotic normalization at a finite internal surface.",
        implication="phi0 acts like an internalized infinity boundary for the negative-phi cell.",
    ),
    Feature(
        name="first jet / tail data",
        statement="At f=1 the value is flat-normalized; the remaining radial information is f' or the 1/r tail coefficient.",
        implication="q is ADM/tail-like Cauchy data unless cancelled by gluing.",
    ),
    Feature(
        name="angular sphere",
        statement="The S2 boundary measure and normalized angular spectrum survive at the normalization surface.",
        implication="asymptotic-boundary math naturally brings in projectors, traces, and Cauchy data.",
    ),
]


def main() -> None:
    print("phi0 asymptotic-infinity reading")
    print("=" * 36)
    for feature in FEATURES:
        print(feature.name)
        print(f"  statement:   {feature.statement}")
        print(f"  implication: {feature.implication}")
        print()

    print("Ponder verdict:")
    print("  phi0=0 is better read as an asymptotic-normalization surface.")
    print("  If UDT places that surface at a finite bridge, it is an")
    print("  internalized asymptotic boundary for the negative-phi cell.")
    print()
    print("Consequence for the current proof:")
    print("  The Calderon/ADM/Brown-York/trace machinery is relevant because")
    print("  phi0 is doing infinity-boundary work: fixing the value f=1,")
    print("  carrying first-jet/tail data, and supporting angular boundary")
    print("  projectors. The missing rule is how the internalized infinity")
    print("  cancels exterior tail while preserving the interior first jet.")


if __name__ == "__main__":
    main()

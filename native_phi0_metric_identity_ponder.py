from dataclasses import dataclass


@dataclass(frozen=True)
class Reading:
    name: str
    forced_by_metric: str
    consequence: str
    proof_status: str


READINGS = [
    Reading(
        name="neutral fixed surface",
        forced_by_metric="phi=0 gives f=exp(-2phi)=1",
        consequence="radial/time dilation is reset to the flat normalization at the interface",
        proof_status="exact",
    ),
    Reading(
        name="phi-sign bridge",
        forced_by_metric="positive and negative phi branches meet at the same f=1 surface",
        consequence="phi0 is the natural crossing surface between exterior/scalar and negative-phi data",
        proof_status="exact as geometry; physical gluing still must be specified",
    ),
    Reading(
        name="angular invariant carrier",
        forced_by_metric="g_AB=r^2 omega_AB is phi-blind and -r^2 Delta_S2 is phi-sign invariant",
        consequence="angular labels can pass through phi0 without radial-dilation ambiguity",
        proof_status="exact",
    ),
    Reading(
        name="first-jet detector",
        forced_by_metric="at f=1, value data are trivial but f' can remain nonzero",
        consequence="nontrivial phi0 data live in the Cauchy momentum / extrinsic curvature jump",
        proof_status="exact",
    ),
    Reading(
        name="internal gluing surface",
        forced_by_metric="two-sided negative/positive phi continuation shares the same boundary S2",
        consequence="if both sides are part of one object, H1 labels are contracted, giving a trace",
        proof_status="conditional on treating phi0 as an internal bridge, not an external wall",
    ),
    Reading(
        name="single Cauchy graph",
        forced_by_metric="not forced by f=1 alone",
        consequence="would identify p=q and close q=1/3",
        proof_status="open; requires exclusion of independent boundary-layer h",
    ),
]


def main() -> None:
    print("phi0 metric identity ponder")
    print("=" * 29)
    for reading in READINGS:
        print(reading.name)
        print(f"  metric statement: {reading.forced_by_metric}")
        print(f"  consequence:      {reading.consequence}")
        print(f"  proof status:     {reading.proof_status}")
        print()

    print("Ponder verdict:")
    print("  The metric presents phi0 as a neutral first-jet bridge:")
    print("    value data are fixed by f=1,")
    print("    angular data are invariant across phi sign,")
    print("    nontrivial radial data are carried only by the first jet.")
    print()
    print("Implication:")
    print("  The next proof should not treat phi0 as a wall that creates q.")
    print("  It should treat phi0 as a Cauchy-data filter that decides which")
    print("  first jets are admissible at the neutral bridge.")
    print()
    print("Sharp remaining question:")
    print("  Does the neutral bridge admit an independent boundary-layer h,")
    print("  or does first-jet admissibility collapse the data to one graph?")


if __name__ == "__main__":
    main()

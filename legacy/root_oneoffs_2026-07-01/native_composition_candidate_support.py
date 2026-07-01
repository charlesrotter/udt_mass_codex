from dataclasses import dataclass


@dataclass(frozen=True)
class Candidate:
    name: str
    metric_support: str
    missing_piece: str
    current_verdict: str


CANDIDATES = [
    Candidate(
        name="single phi0 edge quantum",
        metric_support="C1 momentum, radial-angular curvature, H1/S2 projection",
        missing_piece="derivation of P_phi0 if not banked",
        current_verdict="strong native candidate",
    ),
    Candidate(
        name="two-sided boundary gluing",
        metric_support="boundary variations naturally have sides; glued boundaries add actions",
        missing_piece="actual edge kernel whose side action is eta/2",
        current_verdict="plausible composition framework, not yet a UDT result",
    ),
    Candidate(
        name="channel trace over H1",
        metric_support="three H1 components and round-S2 projection geometry",
        missing_piece="scalar identity action eta/2 I3",
        current_verdict="conditional only",
    ),
    Candidate(
        name="node product over typed graph",
        metric_support="exact CP1/Hopf bridge and exact E1 relative-shape plane",
        missing_piece="independence of graph nodes as action terms",
        current_verdict="diagnostic only",
    ),
    Candidate(
        name="coupled edge block",
        metric_support="orchestra metaphor and shared variables suggest correlations are possible",
        missing_piece="explicit native coupled kernel and its spectrum",
        current_verdict="open alternative; may replace gamma^n",
    ),
    Candidate(
        name="branch-specific source running",
        metric_support="q-flow allows s(t) or branch data to affect q",
        missing_piece="native exact running law",
        current_verdict="open; would modify eta rather than preserve universal gamma",
    ),
]


def main() -> None:
    print("composition candidate support")
    print("=" * 31)
    for candidate in CANDIDATES:
        print(candidate.name)
        print(f"  metric support:   {candidate.metric_support}")
        print(f"  missing piece:    {candidate.missing_piece}")
        print(f"  current verdict:  {candidate.current_verdict}")
        print()

    print("Support verdict:")
    print("  The only strongly supported object is the single phi0 edge quantum.")
    print("  All multi-edge composition laws remain open until a native edge kernel")
    print("  or coupled block is found.")


if __name__ == "__main__":
    main()

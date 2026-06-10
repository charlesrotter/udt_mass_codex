from dataclasses import dataclass


@dataclass(frozen=True)
class Candidate:
    name: str
    metric_supplies: str
    still_missing: str
    second_jet_status: str


CANDIDATES = [
    Candidate(
        "ell=1 angular Laplacian",
        "L1=(-R^2 Delta_S2)/2=I3 on H1",
        "action time/coupling that multiplies L1 by eta/2",
        "supplies identity operator shape, not coefficient weights",
    ),
    Candidate(
        "heat-kernel semigroup",
        "exp(-t L1), trace, and exact composition once t is given",
        "native identification of t with eta/2 and node factorization",
        "supplies transfer mathematics, not S_phi0 Hessian constants",
    ),
    Candidate(
        "Dirichlet-to-Neumann map",
        "a canonical way to map boundary values to conjugate momenta",
        "native phi0 DtN/Calderon map for typed boundary variables",
        "could supply second jet if constructed; not currently available",
    ),
    Candidate(
        "Hamilton-Jacobi on-shell action",
        "boundary momenta are first derivatives of on-shell action",
        "second functional derivative in typed variables",
        "right formal home for Hessian, but not yet computed",
    ),
    Candidate(
        "standard EH+GHY Dirichlet completion",
        "metric boundary completion for fixed induced metric",
        "does not preserve the phi0 slope momentum at f=1",
        "reject as eta/second-jet source in this active lane",
    ),
    Candidate(
        "corner/joint term",
        "localized codimension-2 boundary object where radial and S2 data meet",
        "UDT-specific joint action and its typed second variation",
        "promising location, not yet a computed kernel",
    ),
]


def main() -> None:
    print("metric-supplied second-jet candidate scan")
    print("=" * 43)
    for candidate in CANDIDATES:
        print(candidate.name)
        print(f"  metric supplies:    {candidate.metric_supplies}")
        print(f"  still missing:      {candidate.still_missing}")
        print(f"  second-jet status:  {candidate.second_jet_status}")
        print()

    print("Scan verdict:")
    print("  The metric supplies strong operator shapes: L1, heat semigroup,")
    print("  boundary momentum, and possible DtN/HJ homes.")
    print("  It has not yet supplied the typed second-jet constants or clock.")


if __name__ == "__main__":
    main()

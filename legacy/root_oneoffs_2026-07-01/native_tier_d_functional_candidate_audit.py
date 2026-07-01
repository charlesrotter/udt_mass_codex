from dataclasses import dataclass


@dataclass(frozen=True)
class Candidate:
    name: str
    native_inputs: str
    could_output: str
    current_status: str
    risk: str


CANDIDATES = [
    Candidate(
        "boundary Hessian determinant",
        "second variation of the phi0 boundary functional in typed node variables",
        "relative weights for M1, M2, and E1 after node merging",
        "best Tier D target, but boundary functional is not yet derived",
        "cannot be invented as a Gaussian measure",
    ),
    Candidate(
        "finite-cell action norm",
        "C1 radial action plus angular H1/compact-bundle terms after P_phi0",
        "dimensionless branch normalizations if action is finite and shared",
        "open; angular/bundle action still missing",
        "old numerical action scales do not define the coefficient",
    ),
    Candidate(
        "Dirichlet-to-Neumann determinant",
        "exact collar operator on selected branch data",
        "profile-sensitive determinant weights",
        "available only if transfer branch becomes bulk-DtN",
        "wrong branch for the current interface-local working lane",
    ),
    Candidate(
        "bare shape-measure volume",
        "CP1/S2 and E1 relative-plane measures",
        "only normalized measure factors after a boundary measure is chosen",
        "insufficient by itself; bare measures are isotropic",
        "volume ratios depend on normalization and can become arbitrary",
    ),
    Candidate(
        "compact occupation weight",
        "Pbundle0 plus primitive line-bundle occupancy",
        "M1 activation or M2 suppression factor",
        "conditional postulate, not coefficient calculation",
        "can hide fitting if assigned numerically",
    ),
]


def main() -> None:
    print("Tier D functional candidate audit")
    print("=" * 35)
    for candidate in CANDIDATES:
        print(candidate.name)
        print(f"  native inputs:  {candidate.native_inputs}")
        print(f"  could output:   {candidate.could_output}")
        print(f"  current status: {candidate.current_status}")
        print(f"  risk:           {candidate.risk}")
        print()

    print("Candidate verdict:")
    print("  The next promising object is a boundary Hessian or shared finite-cell")
    print("  action norm in the typed variables. No existing coefficient candidate")
    print("  is currently a derived Tier D functional.")


if __name__ == "__main__":
    main()

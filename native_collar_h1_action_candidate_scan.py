from dataclasses import dataclass


@dataclass(frozen=True)
class Candidate:
    name: str
    native_object: str
    useful_piece: str
    failure_or_gap: str
    status: str


CANDIDATES = [
    Candidate(
        "C1 radial bulk action",
        "(1/4) integral r^2 f'^2 dr",
        "gives exact boundary momentum Pi_f=(1/2)r^2 f'",
        "no H1 carrier and no q-dependent collar source",
        "reject as activation action",
    ),
    Candidate(
        "phi0 boundary momentum projected into H1",
        "(-Pi_f/R)/3 = q/6",
        "gives eta once q is already present",
        "endpoint projection cannot by itself enforce q through the collar",
        "transfer support only",
    ),
    Candidate(
        "spatial curvature fraction",
        "R3/R2=q at phi0",
        "native source of the q scalar as geometry, not analogy",
        "identity is local at the collar; no variational H1 action yet",
        "promising ingredient",
    ),
    Candidate(
        "Misner-Sharp slope density",
        "m_MS'=q/2 at phi0 while m_MS=0",
        "separates hidden value channel from exposed slope-density channel",
        "atlas identity does not supply the H1 action kernel",
        "promising ingredient",
    ),
    Candidate(
        "Brown-York angular stress",
        "dimensionless angular stress unit q/2 at f=1",
        "matches the angular-only shell signature",
        "GR boundary-stress map is not yet a UDT variational derivation",
        "promising atlas, not closure",
    ),
    Candidate(
        "ell=1 angular identity",
        "(-r^2 Delta_S2)/2 = I3 on H1",
        "supplies the exact triplet arena",
        "does not provide the scalar q budget or collar source",
        "necessary but insufficient",
    ),
    Candidate(
        "auxiliary transported H1 amplitude",
        "an unknown collar field A_H1(r) with an equation A_H1=q",
        "could produce q f^2/6 if A_H1 f^2/6 were native",
        "no such metric-supplied auxiliary action has been uncovered",
        "open only as search target",
    ),
]


def main() -> None:
    print("collar H1 action candidate scan")
    print("=" * 36)
    for candidate in CANDIDATES:
        print(candidate.name)
        print(f"  native object:  {candidate.native_object}")
        print(f"  useful piece:   {candidate.useful_piece}")
        print(f"  gap:            {candidate.failure_or_gap}")
        print(f"  status:         {candidate.status}")
        print()

    print("Scan verdict:")
    print("  The orchestra is visible: C1 momentum, curvature fraction,")
    print("  quasilocal slope-density, Brown-York angular stress, and H1 identity")
    print("  all point at the same collar channel. The missing piece is still an")
    print("  exact collar variational object that makes them one action.")


if __name__ == "__main__":
    main()

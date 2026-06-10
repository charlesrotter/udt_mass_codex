from dataclasses import dataclass


@dataclass(frozen=True)
class Candidate:
    name: str
    sees_q_over_2: str
    preserves_flat_exterior: str
    angular_signature: str
    derives_q: str
    verdict: str


CANDIDATES = [
    Candidate(
        name="C1 boundary momentum",
        sees_q_over_2="yes: -Pi_f/R = q/2",
        preserves_flat_exterior="yes if paired with an interface source",
        angular_signature="needs H1/S2 projection added or derived",
        derives_q="no",
        verdict="native conjugate variable; missing boundary functional",
    ),
    Candidate(
        name="Israel shell jump",
        sees_q_over_2="yes: trace-reversed angular jump has magnitude q/2",
        preserves_flat_exterior="yes by construction",
        angular_signature="yes: angular-only at phi0",
        derives_q="no",
        verdict="exact interface bookkeeping; not a native source by itself",
    ),
    Candidate(
        name="raw EH curvature primitive",
        sees_q_over_2="sees qR, equal to -2 Pi_f",
        preserves_flat_exterior="diagnostic only",
        angular_signature="distributional curvature includes angular delta stress",
        derives_q="no",
        verdict="strong atlas clue; import risk as action",
    ),
    Candidate(
        name="standard EH+GHY Dirichlet boundary action",
        sees_q_over_2="no: f' cancels at f=1 after completion/reference subtraction",
        preserves_flat_exterior="yes",
        angular_signature="no eta-producing slope dependence in action value",
        derives_q="no",
        verdict="rejected as eta mechanism",
    ),
    Candidate(
        name="Brown-York angular boundary stress",
        sees_q_over_2="yes: R tau^A_A -> q/2 at f=1",
        preserves_flat_exterior="yes: energy vanishes at f=1",
        angular_signature="yes: zero energy, nonzero angular stress",
        derives_q="no",
        verdict="best GR boundary-stress map; still not UDT derivation",
    ),
    Candidate(
        name="Maxwell/Coulomb sector",
        sees_q_over_2="no native coupling to Pi_f",
        preserves_flat_exterior="not as phi0 shell without added charge layer",
        angular_signature="no: radial electromagnetic stress",
        derives_q="no",
        verdict="real orchestra instrument, wrong boundary mechanism",
    ),
]


def main() -> None:
    print("phi0 boundary candidate scorecard")
    print("=" * 36)
    for candidate in CANDIDATES:
        print(candidate.name)
        print(f"  q/2 unit:       {candidate.sees_q_over_2}")
        print(f"  flat exterior:  {candidate.preserves_flat_exterior}")
        print(f"  angular form:   {candidate.angular_signature}")
        print(f"  derives q:      {candidate.derives_q}")
        print(f"  verdict:        {candidate.verdict}")
        print()

    print("Current exact status:")
    print("  The q/2 angular boundary unit is overdetermined by several metric")
    print("  diagnostics: C1 momentum, shell jump, and Brown-York angular stress.")
    print("  The missing derivation is not q/2 once q is given.")
    print("  The missing derivation is why the native phi0 closure selects q=1/3")
    print("  and why the H1/S2 edge variables are the right projection space.")


if __name__ == "__main__":
    main()

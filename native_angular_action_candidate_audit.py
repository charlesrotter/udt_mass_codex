from dataclasses import dataclass


@dataclass(frozen=True)
class Candidate:
    name: str
    exact_metric_fact: str
    can_supply_i3: str
    can_supply_action_weight: str
    verdict: str


CANDIDATES = [
    Candidate(
        name="S2 Laplacian restricted to ell=1",
        exact_metric_fact="-R^2 Delta_S2 = 2 I_3 on ell=1",
        can_supply_i3="yes",
        can_supply_action_weight="no; needs coupling to eta or a boundary action",
        verdict="best native angular kernel candidate",
    ),
    Candidate(
        name="S2 Killing algebra",
        exact_metric_fact="round S2 has three SO(3) Killing generators",
        can_supply_i3="gives a three-generator algebra, not an action kernel by itself",
        can_supply_action_weight="no",
        verdict="supports channel arena, not transfer weight",
    ),
    Candidate(
        name="Gauss-Bonnet integral",
        exact_metric_fact="integral_S2 R2 dA = 8 pi, fixed by topology",
        can_supply_i3="no",
        can_supply_action_weight="topological constant; no local transfer eigenvalues",
        verdict="not P_transfer",
    ),
    Candidate(
        name="S2 tangent metric",
        exact_metric_fact="gamma_AB = R^2 omega_AB",
        can_supply_i3="no; tangent space is two-dimensional",
        can_supply_action_weight="no",
        verdict="intrinsic geometry, not H1 channel kernel",
    ),
    Candidate(
        name="normalized H1/S2 second moment",
        exact_metric_fact="<n_a n_b> = delta_ab/3",
        can_supply_i3="supplies I_3/3, not I_3",
        can_supply_action_weight="supplies projection factor for eta",
        verdict="eta projection, not transfer kernel",
    ),
]


def main() -> None:
    print("angular action candidate audit")
    print("=" * 32)
    for candidate in CANDIDATES:
        print(candidate.name)
        print(f"  exact metric fact:        {candidate.exact_metric_fact}")
        print(f"  can supply I3:            {candidate.can_supply_i3}")
        print(f"  can supply action weight: {candidate.can_supply_action_weight}")
        print(f"  verdict:                  {candidate.verdict}")
        print()

    print("Angular verdict:")
    print("  The metric does contain a native I_3 structure: the ell=1 Laplacian")
    print("  eigenspace. What remains missing is the boundary action that couples")
    print("  the phi0 edge quantum eta to that ell=1 identity kernel.")


if __name__ == "__main__":
    main()

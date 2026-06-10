from dataclasses import dataclass


@dataclass(frozen=True)
class Candidate:
    name: str
    metric_native: str
    orchestra_role: str
    observation_mechanism_risk: str
    next_action: str


CANDIDATES = [
    Candidate(
        name="H1/projective boundary observable n_a",
        metric_native="round S2 coordinate vector and CP1 Hopf image",
        orchestra_role="connects interface scalar, E1 ordinary frame, and M1 compact doublet",
        observation_mechanism_risk="low; no SM force import",
        next_action="derive boundary action in n_a variables",
    ),
    Candidate(
        name="closure factor graph",
        metric_native="local endpoint variations plus H1 orthogonality",
        orchestra_role="decides whether instruments remain independent nodes",
        observation_mechanism_risk="medium; easy to tune depth counts to masses",
        next_action="derive graph from boundary variation before mass comparison",
    ),
    Candidate(
        name="Coulomb phi-blind sector",
        metric_native="Maxwell cancellation in UDT metric",
        orchestra_role="possible branch-selective interface energy",
        observation_mechanism_risk="medium; do not import SM radiative mass story",
        next_action="couple only the verified abelian boundary energy to the graph",
    ),
    Candidate(
        name="angular determinant finite part",
        metric_native="round S2 Laplacian and measure",
        orchestra_role="possible branch correction after base graph",
        observation_mechanism_risk="high; residual fitting hazard",
        next_action="use only target-blind subtraction-invariant signs",
    ),
    Candidate(
        name="nontrivial compact bundle occupation",
        metric_native="topology supports transport if admitted",
        orchestra_role="enables M1 primitive branch and Hopf bridge",
        observation_mechanism_risk="medium; do not choose because electron anchor works",
        next_action="search for interface obstruction requiring nonzero compact flux",
    ),
]


def main() -> None:
    print("Three-rule search protocol")
    print("=" * 26)
    print("Rule 1: uncover what the metric is already doing.")
    print("Rule 2: preserve the orchestra; test coupled instruments, not only solos.")
    print("Rule 3: observations anchor/test, but do not license imported mechanisms.")
    print()
    for candidate in CANDIDATES:
        print(candidate.name)
        print(f"  metric-native content: {candidate.metric_native}")
        print(f"  orchestra role:        {candidate.orchestra_role}")
        print(f"  import/fitting risk:   {candidate.observation_mechanism_risk}")
        print(f"  next action:           {candidate.next_action}")
    print()
    print("Protocol verdict:")
    print("  The next best calculation is still the boundary action in H1/projective")
    print("  variables, because it tests the main orchestra coupling without borrowing")
    print("  Standard Model machinery or fitting observed masses.")


if __name__ == "__main__":
    main()

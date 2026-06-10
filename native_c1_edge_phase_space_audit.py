from dataclasses import dataclass


@dataclass(frozen=True)
class EdgeCondition:
    name: str
    condition: str
    phase_space_consequence: str
    verdict: str


CONDITIONS = [
    EdgeCondition(
        name="bare C1 boundary variation",
        condition="delta S_C1 has edge term Pi_f delta f",
        phase_space_consequence="the scalar edge canonical data are (f, Pi_f)",
        verdict="one radial scalar canonical pair before boundary conditions",
    ),
    EdgeCondition(
        name="phi0 value condition",
        condition="f=1 at the phi0 boundary",
        phase_space_consequence="Dirichlet value removes delta f at the boundary",
        verdict="no free f variation if imposed",
    ),
    EdgeCondition(
        name="P_phi0 momentum condition",
        condition="-Pi_f/R=1/6",
        phase_space_consequence="Neumann momentum is fixed",
        verdict="fixes the remaining scalar edge momentum",
    ),
    EdgeCondition(
        name="H1/S2 orientation",
        condition="n_a n_a=1 and <n_a n_b>=delta_ab/3",
        phase_space_consequence="kinematic orientation arena, but no C1 conjugate momentum",
        verdict="not a dynamical edge phase space from C1 alone",
    ),
    EdgeCondition(
        name="shape / embedding data",
        condition="s^A_B and n(s)^A_B are isotropic at phi0",
        phase_space_consequence="carry q as scalar embedding data, no independent traceless modes",
        verdict="not enough for multi-node dynamics",
    ),
]


def main() -> None:
    print("C1 edge phase-space audit")
    print("=" * 28)
    for condition in CONDITIONS:
        print(condition.name)
        print(f"  condition:                {condition.condition}")
        print(f"  phase-space consequence:  {condition.phase_space_consequence}")
        print(f"  verdict:                  {condition.verdict}")
        print()

    print("Phase-space verdict:")
    print("  Scalar C1 gives one edge canonical pair (f, Pi_f). At phi0, f=1")
    print("  and P_phi0 fix that scalar pair. H1/S2 supplies kinematic orientation,")
    print("  but C1 alone does not supply an angular edge phase space or node graph.")


if __name__ == "__main__":
    main()

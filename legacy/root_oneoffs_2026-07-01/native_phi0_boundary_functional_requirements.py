from dataclasses import dataclass


@dataclass(frozen=True)
class Requirement:
    name: str
    exact_condition: str
    reason: str
    failure_if_absent: str


REQUIREMENTS = [
    Requirement(
        name="value closure",
        exact_condition="a_tail,outside = 0",
        reason="finite matter cell must not leave exterior negative-mass tail",
        failure_if_absent="object has long-range negative-mass tail, not a closed particle cell",
    ),
    Requirement(
        name="momentum jump",
        exact_condition="Delta Pi_f = Pi_outer - Pi_inner = q/2",
        reason="nonzero eta with flat exterior requires C1 boundary momentum jump",
        failure_if_absent="smooth flat matching forces q=0 and eta=0",
    ),
    Requirement(
        name="H1 projection",
        exact_condition="Delta Pi_f <n_a n_b> = (q/6) delta_ab",
        reason="round S2/H1 projection turns scalar boundary momentum into eta",
        failure_if_absent="no derived eta transfer unit",
    ),
    Requirement(
        name="self-similar fixed collar",
        exact_condition="q = 1/3 for the base finite-action H1 source",
        reason="gives eta=1/18 and follows from constant-source q-flow if s=1/9",
        failure_if_absent="eta becomes q/6 and branch/source running must be derived",
    ),
    Requirement(
        name="typed node variables",
        exact_condition="functional variables are shared H1 frame nodes plus branch shape nodes",
        reason="connects closure graph to variational structure",
        failure_if_absent="depth count remains bookkeeping",
    ),
    Requirement(
        name="factorized kernel",
        exact_condition="kernel factorization must be derived exactly, not assumed",
        reason="gamma^k requires independent rank-one H1/projective closure factors",
        failure_if_absent="node entropy collapses or becomes coefficient/determinant problem",
    ),
]


def main() -> None:
    print("phi0 boundary functional exact requirements")
    print("=" * 45)
    print("These are requirements, not an approximate model.")
    print()
    for req in REQUIREMENTS:
        print(req.name)
        print(f"  exact condition:   {req.exact_condition}")
        print(f"  reason:            {req.reason}")
        print(f"  failure if absent: {req.failure_if_absent}")
        print()
    print("Requirements verdict:")
    print("  A candidate phi0 boundary functional is not acceptable unless it satisfies")
    print("  these exact conditions or explicitly replaces one with a derived alternative.")


if __name__ == "__main__":
    main()

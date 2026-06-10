from dataclasses import dataclass


@dataclass(frozen=True)
class Requirement:
    name: str
    exact_input: str
    output_needed: str
    fail_condition: str


REQUIREMENTS = [
    Requirement(
        "post-Dirac variables",
        "use f, q, eta, H1/S2 projectors, Hopf/CP1 data, and relative-shape coordinates only",
        "a coefficient functional in native variables",
        "any dependence on the removed Dirac/Form-T structure",
    ),
    Requirement(
        "normalization domain",
        "finite negative-phi cell with phi0 boundary and endpoint/core side",
        "well-defined integrals or boundary determinants for M1, M2, and E1",
        "undefined cutoff dependence hidden in C_i",
    ),
    Requirement(
        "branch comparison",
        "evaluate M1, M2, and E1 in the same normalization convention",
        "C_M1, C_M2, C_E1 or a derived suppression of one branch",
        "silent omission of M2",
    ),
    Requirement(
        "no mass input",
        "do not use electron/muon/tau masses during coefficient calculation",
        "dimensionless coefficients before anchoring",
        "choosing coefficients by residual errors",
    ),
]


def main() -> None:
    print("next coefficient-calculation contract")
    print("=" * 37)
    for requirement in REQUIREMENTS:
        print(requirement.name)
        print(f"  exact input:    {requirement.exact_input}")
        print(f"  output needed:  {requirement.output_needed}")
        print(f"  fail condition: {requirement.fail_condition}")
        print()

    print("Contract verdict:")
    print("  The next real Tier D task is not another ladder fit.")
    print("  It is a post-Dirac finite-cell normalization calculation for M1, M2,")
    print("  and E1 under one shared boundary/cell convention.")


if __name__ == "__main__":
    main()

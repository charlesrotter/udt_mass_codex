from dataclasses import dataclass


@dataclass(frozen=True)
class SourceMechanism:
    name: str
    sign_allowed: str
    m1_relevance: str
    e1_relevance: str
    conclusion: str


MECHANISMS = [
    SourceMechanism(
        name="positive angular-gradient energy",
        sign_allowed="positive",
        m1_relevance="could raise q if compact bridge adds boundary angular load",
        e1_relevance="would raise q, opposite of tau-like diagnostic need",
        conclusion="can help M1-like damping but not E1-like boost",
    ),
    SourceMechanism(
        name="positive compact U1 flux energy",
        sign_allowed="positive",
        m1_relevance="direct compact primitive branch candidate",
        e1_relevance="not directly present",
        conclusion="natural M1-positive source candidate if Pbundle0 is occupied",
    ),
    SourceMechanism(
        name="subtraction/normalization of shape source",
        sign_allowed="negative effective after baseline subtraction",
        m1_relevance="possible but would need compact-specific normalization",
        e1_relevance="possible E1-lowering of effective q source",
        conclusion="only viable E1 q-lowering route, but must be derived as normalization not negative energy",
    ),
    SourceMechanism(
        name="branch coefficient normalization",
        sign_allowed="either branch direction",
        m1_relevance="can lower M1 mass without changing q",
        e1_relevance="can raise E1 mass without negative source",
        conclusion="cleaner explanation for opposite residual signs than forcing q shifts",
    ),
    SourceMechanism(
        name="node correlation entropy",
        sign_allowed="usually lowers entropy/mass scale",
        m1_relevance="can lower M1-like branch",
        e1_relevance="wrong direction for tau-like branch",
        conclusion="possible M1 damping only, not universal residual fix",
    ),
]


def main() -> None:
    print("Source-sign physics filter")
    print("=" * 27)
    print("Filter branch-specific q-source ideas by native sign constraints.")
    print()
    for mechanism in MECHANISMS:
        print(mechanism.name)
        print(f"  sign allowed: {mechanism.sign_allowed}")
        print(f"  M1 relevance: {mechanism.m1_relevance}")
        print(f"  E1 relevance: {mechanism.e1_relevance}")
        print(f"  conclusion:   {mechanism.conclusion}")
        print()

    print("Filter verdict:")
    print("  - Positive-definite source terms are compatible with the M1-required")
    print("    positive q shift.")
    print("  - They are not compatible with the E1-required negative q shift.")
    print("  - Therefore E1/tau-like residual should first be sought in coefficient")
    print("    normalization, subtraction/renormalized source definition, or another")
    print("    branch-specific boundary effect, not ordinary positive angular energy.")


if __name__ == "__main__":
    main()

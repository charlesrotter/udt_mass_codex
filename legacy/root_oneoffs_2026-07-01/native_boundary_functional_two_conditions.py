from dataclasses import dataclass


@dataclass(frozen=True)
class BoundaryFunctionalModel:
    name: str
    value_condition: str
    derivative_condition: str
    can_cancel_tail: str
    can_set_q: str
    status: str


MODELS = [
    BoundaryFunctionalModel(
        name="Dirichlet wall f=1",
        value_condition="fixes f at phi0",
        derivative_condition="does not cancel Pi_f dynamically",
        can_cancel_tail="only if exterior is imposed flat",
        can_set_q="no; q is inherited from interior or imposed",
        status="hard-wall-like; not the desired mechanism",
    ),
    BoundaryFunctionalModel(
        name="Neumann smooth flat match",
        value_condition="can set exterior f=1",
        derivative_condition="sets Pi_f=0",
        can_cancel_tail="yes",
        can_set_q="kills q, hence eta=0",
        status="wrong for nonzero eta",
    ),
    BoundaryFunctionalModel(
        name="conjugate phi0 boundary functional",
        value_condition="can encode exterior flat/tail cancellation as boundary Hamiltonian value",
        derivative_condition="dS_boundary/df=q/2 cancels C1 Pi_f",
        can_cancel_tail="possible if value condition imposes a_tail=0",
        can_set_q="yes, through derivative condition",
        status="best candidate; needs derivation",
    ),
    BoundaryFunctionalModel(
        name="global closure functional of typed nodes",
        value_condition="a_tail[nodes]=0",
        derivative_condition="variation gives node-level momentum constraints",
        can_cancel_tail="yes by construction if derived",
        can_set_q="yes if H1 projection controls derivative",
        status="orchestra form of conjugate boundary functional",
    ),
]


def main() -> None:
    print("Boundary functional two-condition audit")
    print("=" * 41)
    print("A real phi0 mechanism must handle two conditions:")
    print("  1. value/global condition: exterior tail a_tail=0")
    print("  2. derivative/local condition: boundary momentum Pi_f=-q/2")
    print()
    for model in MODELS:
        print(model.name)
        print(f"  value condition:      {model.value_condition}")
        print(f"  derivative condition: {model.derivative_condition}")
        print(f"  can cancel tail:      {model.can_cancel_tail}")
        print(f"  can set q:            {model.can_set_q}")
        print(f"  status:               {model.status}")
        print()

    print("Two-condition verdict:")
    print("  - Dirichlet and smooth Neumann closures each do only half the job.")
    print("  - The needed object is a conjugate boundary functional with both value")
    print("    and derivative content.")
    print("  - In orchestra language: a_tail=0 is the global closure value, while")
    print("    q/2 is the local H1-projected boundary momentum.")


if __name__ == "__main__":
    main()

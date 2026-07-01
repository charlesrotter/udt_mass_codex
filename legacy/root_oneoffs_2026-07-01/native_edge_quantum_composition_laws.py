from dataclasses import dataclass
from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


@dataclass(frozen=True)
class CompositionLaw:
    name: str
    exact_rule: str
    consequence: str
    status: str


LAWS = [
    CompositionLaw(
        name="independent action addition",
        exact_rule="S_total = sum_i S_i",
        consequence="weights multiply: exp(-S_total)=prod_i exp(-S_i)",
        status="exact if edge quanta are independent action terms",
    ),
    CompositionLaw(
        name="glued boundary half-action",
        exact_rule="two half-boundaries glue to one full boundary action",
        consequence="one side carries eta/2; glued internal boundary carries eta",
        status="exact bookkeeping if the object is a composable boundary kernel",
    ),
    CompositionLaw(
        name="shared variable merge",
        exact_rule="two nominal nodes constrained to the same edge variable count once",
        consequence="depth is reduced; multiplication overcounts",
        status="exact constraint-counting warning",
    ),
    CompositionLaw(
        name="correlated edge block",
        exact_rule="edge variables form one coupled block rather than product factors",
        consequence="trace/eigenvalues of full block replace gamma^n",
        status="exact alternative if metric supplies a coupled kernel",
    ),
    CompositionLaw(
        name="channel trace",
        exact_rule="Tr exp(-a I_N) = N exp(-a)",
        consequence="factor N appears only for an actual N-channel identity kernel",
        status="exact but conditional",
    ),
    CompositionLaw(
        name="normalized projection",
        exact_rule="<n_a n_b> = delta_ab/3",
        consequence="gives projection factor 1/3; does not by itself give multiplicity 3",
        status="exact projection, not transfer multiplication",
    ),
]


def main() -> None:
    print("edge quantum composition laws")
    print("=" * 31)
    eta = Fraction(1, 18)
    print(f"edge quantum eta = {fmt(eta)} if P_phi0 is banked")
    print()
    for law in LAWS:
        print(law.name)
        print(f"  exact rule:   {law.exact_rule}")
        print(f"  consequence:  {law.consequence}")
        print(f"  status:       {law.status}")
        print()

    print("No-invention verdict:")
    print("  The metric has exposed an edge quantum. A mass ladder requires an")
    print("  exact composition law for multiple edge quanta. The allowed laws are")
    print("  action addition, boundary gluing, variable merging, coupled-block")
    print("  tracing, or channel tracing. They are not interchangeable.")


if __name__ == "__main__":
    main()

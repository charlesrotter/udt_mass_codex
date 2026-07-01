from dataclasses import dataclass


@dataclass(frozen=True)
class FunctionalCandidate:
    name: str
    depends_on_f: str
    can_supply_df_derivative: str
    can_supply_tail_value: str
    exact_status: str


CANDIDATES = [
    FunctionalCandidate(
        name="pure intrinsic S2 curvature integral",
        depends_on_f="no, for fixed round S2 topology/radius in the current collar variables",
        can_supply_df_derivative="no",
        can_supply_tail_value="no",
        exact_status="reject as local momentum-jump source; useful only for topology",
    ),
    FunctionalCandidate(
        name="pure S2 area at fixed R",
        depends_on_f="no if R and angular metric are fixed independently of f",
        can_supply_df_derivative="no",
        can_supply_tail_value="no",
        exact_status="reject unless a derived coupling to f or phi0 embedding exists",
    ),
    FunctionalCandidate(
        name="timelike shell area/tension",
        depends_on_f="yes through induced time metric sqrt(f)",
        can_supply_df_derivative="yes",
        can_supply_tail_value="possibly",
        exact_status="wrong stress signature unless trace-subtracted/derived specially",
    ),
    FunctionalCandidate(
        name="C1 conjugate boundary functional",
        depends_on_f="yes by definition",
        can_supply_df_derivative="yes: must give dS/df=q/2 at f=1",
        can_supply_tail_value="yes if value condition encodes a_tail=0",
        exact_status="acceptable target, not yet derived",
    ),
    FunctionalCandidate(
        name="H1 trace-projected conjugate functional",
        depends_on_f="yes through C1 boundary momentum and H1 projection",
        can_supply_df_derivative="yes: projected derivative eta=q/6",
        can_supply_tail_value="possible if tied to typed closure nodes",
        exact_status="best exact target, but still to derive",
    ),
]


def main() -> None:
    print("Exact boundary functional accept/reject audit")
    print("=" * 47)
    print("A candidate phi0 functional must supply dS/df=q/2 or an exact replacement.")
    print()
    for candidate in CANDIDATES:
        print(candidate.name)
        print(f"  depends on f:        {candidate.depends_on_f}")
        print(f"  supplies dS/df:      {candidate.can_supply_df_derivative}")
        print(f"  supplies tail value: {candidate.can_supply_tail_value}")
        print(f"  exact status:        {candidate.exact_status}")
        print()

    print("Accept/reject verdict:")
    print("  Pure S2 topology or fixed-area terms cannot carry the C1 momentum jump")
    print("  unless an exact f-coupling is derived.")
    print("  Timelike area can depend on f but has the wrong stress pattern.")
    print("  The exact target remains a C1 conjugate/H1 trace-projected boundary")
    print("  functional, not a generic geometric area term.")


if __name__ == "__main__":
    main()

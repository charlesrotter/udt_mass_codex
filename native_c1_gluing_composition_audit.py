from dataclasses import dataclass


@dataclass(frozen=True)
class GluingCase:
    name: str
    exact_condition: str
    action_consequence: str
    verdict: str


CASES = [
    GluingCase(
        name="smooth gluing",
        exact_condition="f and f' match across the interface",
        action_consequence="no interface source; C1 bulk actions add over intervals",
        verdict="no new edge quantum at the glued interface",
    ),
    GluingCase(
        name="continuous f with slope jump",
        exact_condition="f matches, Delta f' != 0",
        action_consequence="interface source J with Delta Pi_f=(1/2)R^2 Delta f'",
        verdict="one localized edge datum, not two independent nodes",
    ),
    GluingCase(
        name="flat exterior with inner q",
        exact_condition="f=1, f'_out=0, f'_in=-q/R",
        action_consequence="Delta Pi_f=qR/2; P_phi0 fixes q=1/3 if banked",
        verdict="single phi0 edge quantum",
    ),
    GluingCase(
        name="two nominal nodes sharing one edge variable",
        exact_condition="same f, Pi_f, or H1/S2 direction variable",
        action_consequence="constraint identifies variables",
        verdict="nodes merge; product counting overcounts",
    ),
]


def main() -> None:
    print("C1 gluing composition audit")
    print("=" * 31)
    for case in CASES:
        print(case.name)
        print(f"  exact condition:      {case.exact_condition}")
        print(f"  action consequence:   {case.action_consequence}")
        print(f"  verdict:              {case.verdict}")
        print()

    print("Gluing verdict:")
    print("  C1 gluing supplies additive bulk action and localized interface")
    print("  momentum jumps. It does not by itself turn one phi0 edge quantum into")
    print("  a multiplicative ladder.")


if __name__ == "__main__":
    main()

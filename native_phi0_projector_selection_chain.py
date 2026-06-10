from dataclasses import dataclass


@dataclass(frozen=True)
class Step:
    name: str
    metric_input: str
    selection_result: str
    status: str


STEPS = [
    Step(
        "phi0 value surface",
        "f(phi0)=1",
        "scalar boundary value is fixed, not a transfer label",
        "exact",
    ),
    Step(
        "C1 momentum jump",
        "Delta Pi/R=q/2",
        "sets eta=q/6 after H1/S2 projection",
        "exact once q is selected/banked",
    ),
    Step(
        "endpoint admissibility",
        "p(1-p)/2=eta ell(ell+1), finite C1 requires p<1/2",
        "at eta=1/18, ell=0 is trivial, ell=1 is only nontrivial finite, ell>=2 rejected",
        "exact after eta",
    ),
    Step(
        "boundary angular projector",
        "round S2 harmonic decomposition",
        "P_adm,nontrivial = P_ell=1 = P_H1",
        "derived after previous filters",
    ),
    Step(
        "boundary measure",
        "induced round S2 measure",
        "Tr P_H1=3",
        "exact",
    ),
]


def main() -> None:
    print("phi0 projector selection chain")
    print("=" * 32)
    for step in STEPS:
        print(step.name)
        print(f"  metric input:      {step.metric_input}")
        print(f"  selection result:  {step.selection_result}")
        print(f"  status:            {step.status}")
        print()

    print("Chain verdict:")
    print("  Once q/eta is supplied, H1 is not merely the first useful sector.")
    print("  It is the only nontrivial finite angular endpoint sector that survives")
    print("  the phi0 boundary/admissibility filters.")


if __name__ == "__main__":
    main()

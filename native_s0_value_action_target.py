from dataclasses import dataclass


@dataclass(frozen=True)
class Target:
    name: str
    required_form: str
    metric_clue: str
    open_problem: str


TARGETS = [
    Target(
        "interface-local H1 value action",
        "S0[a]|H1 = (eta/2)<a,L1 a> for one side, with L1=I3",
        "ell=1 angular Laplacian supplies L1; interface jump supplies eta scale",
        "derive why the value action uses side time eta/2",
    ),
    Target(
        "two-sided full value action",
        "S0_full[a]|H1 = eta<a,L1 a>",
        "symmetric gluing would split this into eta/2 per side",
        "derive gluing from the boundary variational principle",
    ),
    Target(
        "bulk-DtN value action",
        "S0[a]=<a,K_DtN a>/2 with warped K_DtN",
        "positional dilation supplies the warped normal operator",
        "action must choose bulk propagation and its normalization",
    ),
    Target(
        "typed coefficient Hessian",
        "S0[x]=1/2 x^a K_ab x^b over H1, M1, M2, and E1 variables",
        "symmetry constrains K_ab block forms",
        "derive block weights and cross-couplings from S_phi0, not from fits",
    ),
]


def main() -> None:
    print("S0 value-action target")
    print("=" * 22)
    for target in TARGETS:
        print(target.name)
        print(f"  required form: {target.required_form}")
        print(f"  metric clue:   {target.metric_clue}")
        print(f"  open problem:  {target.open_problem}")
        print()

    print("Target verdict:")
    print("  The next uncovered object is S0[a], the angular/value part of")
    print("  S_phi0. The metric has supplied its natural operators, but not yet")
    print("  the action-time normalization or typed Hessian weights.")


if __name__ == "__main__":
    main()

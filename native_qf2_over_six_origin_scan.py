from dataclasses import dataclass


@dataclass(frozen=True)
class Origin:
    name: str
    native_object: str
    can_supply_qf2_over_six: str
    verdict: str


ORIGINS = [
    Origin(
        "bare C1 radial action",
        "(1/4) r^2 f'^2",
        "no; supplies kinetic term and endpoint momentum only",
        "reject as source of q f^2/6",
    ),
    Origin(
        "ordinary f-only potential",
        "V(f,r)",
        "no for q-dependent source; q contains f'",
        "reject for s(q)=q/3",
    ),
    Origin(
        "naive derivative substitution",
        "V=(q/6)f^2 with q=-rf'/f",
        "no; reduces to boundary term plus fixed s=1/6",
        "reject",
    ),
    Origin(
        "constrained q phase-space action",
        "independent q plus constraint q+rf'/f=0",
        "only if q f^2/6 term is itself supplied",
        "repackages gate, does not derive it",
    ),
    Origin(
        "EH/curvature primitive atlas",
        "B_EH=-r^2 f' at phi0",
        "identifies q boundary jump, not collar q f^2 action",
        "useful atlas, not enough",
    ),
    Origin(
        "H1 projected boundary action",
        "B<n_a n_b>",
        "supplies eta projection after scalar budget exists",
        "transfer support, not collar activation",
    ),
    Origin(
        "unknown collar H1 action",
        "transported H1 data on each linking S2",
        "possible if variation produces q f^2/6",
        "only remaining primary-route source",
    ),
]


def main() -> None:
    print("q f^2 / 6 origin scan")
    print("=" * 25)
    for origin in ORIGINS:
        print(origin.name)
        print(f"  native object: {origin.native_object}")
        print(f"  can supply:    {origin.can_supply_qf2_over_six}")
        print(f"  verdict:       {origin.verdict}")
        print()

    print("No-approximation verdict:")
    print("  Known C1/boundary/curvature pieces do not yet derive q f^2/6.")
    print("  The primary route survives only as an unknown collar H1 action.")


if __name__ == "__main__":
    main()

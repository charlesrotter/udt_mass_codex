from dataclasses import dataclass


@dataclass(frozen=True)
class MetricAction:
    layer: str
    exact_metric_object: str
    what_it_already_does: str
    boundary_status: str


ACTIONS = [
    MetricAction(
        "negative-phi arena",
        "f=e^{-2phi}>1 for phi<0",
        "creates the finite-action endpoint/collar problem without Dirac/Form-T",
        "native background arena",
    ),
    MetricAction(
        "phi-blind angular sector",
        "g_AB=r^2 omega_AB",
        "preserves the round S2 spectrum and H1 triplet across phi sign",
        "native operator arena",
    ),
    MetricAction(
        "C1 boundary momentum",
        "Pi_f=(1/2)r^2 f'",
        "at phi0 gives -Pi_f/R=q/2, the local edge slope unit",
        "first variation fixed once q is banked",
    ),
    MetricAction(
        "interface curvature jump",
        "flat exterior plus inner f'=-q/R",
        "produces angular-only shell stress and Delta K R=q/2",
        "localized phi0/joint object",
    ),
    MetricAction(
        "H1/S2 projection",
        "<n_a n_b>=delta_ab/3",
        "turns q/2 into eta=q/6",
        "projection identity, not a transfer kernel by itself",
    ),
    MetricAction(
        "ell=1 Laplacian identity",
        "L1=(-R^2 Delta_S2)/2=I3 on H1",
        "supplies the three-channel identity operator shape",
        "operator shape supplied",
    ),
    MetricAction(
        "proper radial refactor",
        "d rho=dr/sqrt(f), r''/r=f'/(2r)",
        "adds the positional-dilation/extrinsic term to the normal operator",
        "bulk DtN branch supplied if bulk propagation is chosen",
    ),
    MetricAction(
        "heat semigroup",
        "exp(-t L1)",
        "supplies trace/composition mathematics once the action time t is given",
        "clock t not supplied by semigroup itself",
    ),
    MetricAction(
        "local boundary expansion",
        "S_b(F,a)=S0[a]+S1[a](F-1)+O((F-1)^2)",
        "separates value/angular action S0 from slope closure S1",
        "shows why first variation does not determine coefficients",
    ),
]


def main() -> None:
    print("metric already-doing inventory")
    print("=" * 32)
    for action in ACTIONS:
        print(action.layer)
        print(f"  exact metric object: {action.exact_metric_object}")
        print(f"  already does:        {action.what_it_already_does}")
        print(f"  boundary status:     {action.boundary_status}")
        print()

    print("Inventory verdict:")
    print("  The metric is already supplying the arena, slope unit, angular")
    print("  identity, projection, interface jump, and warped normal operator.")
    print("  The unresolved piece is narrower: the angular value action / second")
    print("  jet S0[a] or K_ab on typed boundary variables.")


if __name__ == "__main__":
    main()

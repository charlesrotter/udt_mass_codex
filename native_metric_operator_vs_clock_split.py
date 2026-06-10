from dataclasses import dataclass


@dataclass(frozen=True)
class Layer:
    name: str
    metric_status: str
    active_lane_role: str


LAYERS = [
    Layer(
        "operator shape",
        "metric supplies L1=I3 on ell=1 and I2 on the E1 relative plane by symmetry",
        "known",
    ),
    Layer(
        "edge scalar",
        "banked P_phi0 plus projection supplies eta=1/18",
        "known only because P_phi0 is banked",
    ),
    Layer(
        "side clock",
        "eta/2 is supplied only if P_transfer gluing is banked",
        "conditional",
    ),
    Layer(
        "second-jet weights",
        "not supplied by operator symmetry or eta",
        "missing",
    ),
    Layer(
        "node factorization",
        "not supplied by heat-kernel semigroup alone; needs boundary graph/action",
        "missing/conditional P_depth",
    ),
]


def main() -> None:
    print("metric operator vs clock split")
    print("=" * 32)
    for layer in LAYERS:
        print(layer.name)
        print(f"  metric status:    {layer.metric_status}")
        print(f"  active-lane role: {layer.active_lane_role}")
        print()

    print("Split verdict:")
    print("  The metric is supplying the operator arena more strongly than the")
    print("  coefficient clock. This supports the interface-transfer route but")
    print("  does not close Tier D.")


if __name__ == "__main__":
    main()

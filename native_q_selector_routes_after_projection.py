from dataclasses import dataclass
from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


@dataclass(frozen=True)
class Route:
    name: str
    exact_equation: str
    metric_reading: str
    status: str


ROUTES = [
    Route(
        name="self-similar Cauchy graph",
        exact_equation="p=q and p(1-p)/2=(q/6)*2 -> q=0 or q=1/3",
        metric_reading="phi=0 bridge admits one first-jet graph, not independent boundary-layer memory",
        status="best Calderon/projector route; still must exclude running h",
    ),
    Route(
        name="self-coupled H1 source inventory",
        exact_equation="s(q)=q/3 and dq/dt=q^2-q+2s -> dq/dt=q(q-1/3)",
        metric_reading="curvature share q and H1 share 1/3 form the active collar source",
        status="best source-inventory route; product rule not yet derived",
    ),
    Route(
        name="projected C1 side-action compatibility",
        exact_equation="q^2/[12(1-2q)] = q/12 -> q=0 or q=1/3",
        metric_reading="projected radial C1 action value equals the one-side bridge action",
        status="strong value-action compatibility; needs physical rule selecting equality",
    ),
]


def main() -> None:
    print("q selector routes after projection")
    print("=" * 36)
    print("Projection intersection has narrowed the problem but does not select q.")
    print("Exact routes that do select q=1/3:")
    print()
    for route in ROUTES:
        print(route.name)
        print(f"  exact equation: {route.exact_equation}")
        print(f"  metric reading: {route.metric_reading}")
        print(f"  status:         {route.status}")
        print()

    q = Fraction(1, 3)
    print("Common nontrivial output:")
    print(f"  q = {fmt(q)}")
    print(f"  Delta Pi/R = q/2 = {fmt(q / 2)}")
    print(f"  eta = q/6 = {fmt(q / 6)}")
    print(f"  eta/2 = {fmt(q / 12)}")
    print()
    print("Metric-only priority after the bridge reframe:")
    print("  1. self-similar Cauchy graph / source inventory are primary")
    print("     because they speak directly to admissible first-jet data;")
    print("  2. side-action compatibility is consilience unless the boundary")
    print("     action proves that equality is the stationarity condition.")
    print()
    print("Audit verdict:")
    print("  q=1/3 has three exact metric-native convergence routes, but")
    print("  one of their premise rules must still be derived from the phi=0")
    print("  internalized-asymptotic gluing.")


if __name__ == "__main__":
    main()

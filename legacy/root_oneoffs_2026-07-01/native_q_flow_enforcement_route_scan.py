from dataclasses import dataclass


@dataclass(frozen=True)
class Route:
    name: str
    metric_object: str
    how_it_would_enforce_delta_h_zero: str
    status: str
    next_test: str


ROUTES = [
    Route(
        "constant H1 source",
        "phi-blind ell=1 angular eigenvalue and isotropic H1 shell stress",
        "s(t)=1/9 throughout the active collar makes q=1/3 a fixed solution",
        "best current route, but source constancy is not derived",
        "derive whether the H1 source is a collar density or a phi0-local delta source",
    ),
    Route(
        "integral cancellation",
        "two-sided phi bridge and possible positive/negative source regions",
        "nonconstant q-flow integrates to zero between endpoint and phi0",
        "possible but less clean; high risk of disguised fitting",
        "look for an exact antisymmetry or conservation law before using it",
    ),
    Route(
        "q-matching boundary condition",
        "joint/slope boundary term or phase-space endpoint condition",
        "variation imposes q_phi0=p directly",
        "possible only if a genuine slope/extrinsic-curvature boundary term exists",
        "derive a UDT-native joint term; do not import GHY/Israel dynamics blindly",
    ),
    Route(
        "bulk DtN memory",
        "warped collar Cauchy-data map",
        "does not enforce delta_h=0; instead keeps profile dependence",
        "important discriminator, but opposite of simple branch",
        "use only if transfer action is bulk propagation rather than interface-local",
    ),
]


def main() -> None:
    print("q-flow enforcement route scan")
    print("=" * 35)
    for route in ROUTES:
        print(route.name)
        print(f"  metric object: {route.metric_object}")
        print(f"  enforcement:   {route.how_it_would_enforce_delta_h_zero}")
        print(f"  status:        {route.status}")
        print(f"  next test:     {route.next_test}")
        print()

    print("No-approximation verdict:")
    print("  The cleanest route is constant H1 source.")
    print("  Integral cancellation needs an exact symmetry/conservation law.")
    print("  Direct q-matching needs a real slope/joint boundary term.")


if __name__ == "__main__":
    main()

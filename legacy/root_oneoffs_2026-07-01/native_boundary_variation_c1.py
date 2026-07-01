from dataclasses import dataclass


@dataclass(frozen=True)
class EndpointPower:
    p: float
    label: str

    @property
    def action_exponent(self) -> float:
        return 1.0 - 2.0 * self.p

    @property
    def finite_action(self) -> bool:
        return self.action_exponent > 0.0

    @property
    def boundary_flux_exponent(self) -> float:
        return 1.0 - 2.0 * self.p

    @property
    def self_similarity_gap(self) -> float:
        return self.action_exponent - self.p


def angular_source_from_p(p: float) -> float:
    return 0.5 * p * (1.0 - p)


def p_from_angular_source(s: float) -> tuple[float, float] | None:
    disc = 1.0 - 8.0 * s
    if disc < 0.0:
        return None
    root = disc**0.5
    return ((1.0 - root) / 2.0, (1.0 + root) / 2.0)


def main() -> None:
    print("C1 boundary variation in f=e^{-2phi}")
    print("=" * 42)
    print("Metric determinant: sqrt(-g)=r^2 sin(theta)")
    print("Static radial C1 density:")
    print("  e^{-2phi} g^rr phi'^2 sqrt(-g) = r^2 e^{-4phi} phi'^2")
    print("With f=e^{-2phi}, phi'=-f'/(2f):")
    print("  density = (1/4) r^2 f'^2")
    print()
    print("Thus the native scalar action is a radial Dirichlet energy for f.")
    print("The boundary variation carries the canonical flux:")
    print("  Pi_f proportional to r^2 f'")
    print()

    endpoints = [
        EndpointPower(0.0, "scalar O0 / no endpoint"),
        EndpointPower(1.0 / 3.0, "self-similar finite endpoint"),
        EndpointPower(0.5, "finite-action threshold"),
        EndpointPower(1.0, "vacuum negative-mass branch"),
        EndpointPower(2.0, "charged/Reissner-like singular branch"),
    ]

    print("Endpoint f=A r^-p:")
    for endpoint in endpoints:
        print(f"  {endpoint.label}")
        print(f"    p={endpoint.p:.9g}")
        print(f"    action remainder exponent 1-2p={endpoint.action_exponent:.9g}")
        print(f"    finite action: {endpoint.finite_action}")
        print(f"    boundary flux exponent={endpoint.boundary_flux_exponent:.9g}")
        print(f"    self-similarity gap (1-2p)-p={endpoint.self_similarity_gap:.9g}")
        print(f"    angular source s=p(1-p)/2={angular_source_from_p(endpoint.p):.9g}")

    print("\nAngular source check:")
    for s in [0.0, 1.0 / 9.0, 1.0 / 8.0, 1.0 / 4.0]:
        roots = p_from_angular_source(s)
        if roots is None:
            print(f"  s={s:.9g}: no real endpoint powers")
        else:
            print(f"  s={s:.9g}: p={roots[0]:.9g}, {roots[1]:.9g}")

    print("\nBoundary verdict:")
    print("  - C1 alone gives the finite-action filter p<1/2.")
    print("  - C1 written in f does not by itself contain eta, N, or closure count.")
    print("  - p=1/3 is visible as the point where action remainder scaling equals profile scaling.")
    print("  - Any eta-like unit action must come from angular/bundle/interface data,")
    print("    not from the bare radial C1 boundary flux alone.")


if __name__ == "__main__":
    main()

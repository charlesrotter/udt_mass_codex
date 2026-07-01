import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Profile:
    name: str
    p: float
    a: float
    kind: str

    def h(self, x: float) -> float:
        if self.kind == "power":
            return 1.0
        if self.kind == "linear_shape":
            return 1.0 + self.a * (1.0 - x)
        if self.kind == "quadratic_shape":
            return 1.0 + self.a * (1.0 - x) ** 2
        if self.kind == "boundary_flattened":
            return math.exp(self.a * (1.0 - x) ** 2)
        raise ValueError(self.kind)

    def h_prime_at_1(self) -> float:
        if self.kind == "power":
            return 0.0
        if self.kind == "linear_shape":
            return -self.a
        if self.kind == "quadratic_shape":
            return 0.0
        if self.kind == "boundary_flattened":
            return 0.0
        raise ValueError(self.kind)

    def boundary_slope(self) -> float:
        # f(x)=x^-p h(x), h(1)=1.
        # f'(1)=-p+h'(1).
        return -self.p + self.h_prime_at_1()

    def boundary_scalar(self) -> float:
        # B = Delta K R = -f'_inner(1)/2 for flat exterior.
        return -0.5 * self.boundary_slope()

    def endpoint_prefactor(self, epsilon: float = 1.0e-6) -> float:
        # f x^p -> h(0-ish), diagnostic only.
        return self.h(epsilon)


def main() -> None:
    p = 1.0 / 3.0
    profiles = [
        Profile("pure self-similar power", p, 0.0, "power"),
        Profile("linear shape a=+0.10", p, 0.10, "linear_shape"),
        Profile("linear shape a=-0.10", p, -0.10, "linear_shape"),
        Profile("quadratic interior shape a=+0.30", p, 0.30, "quadratic_shape"),
        Profile("quadratic interior shape a=-0.30", p, -0.30, "quadratic_shape"),
        Profile("boundary-flattened exp shape a=+0.50", p, 0.50, "boundary_flattened"),
    ]

    print("Finite-cell interface slope audit")
    print("=" * 35)
    print("Profiles use f(x)=x^-p h(x), x=r/R, f(1)=1.")
    print("The interface scalar for flat exterior is:")
    print("  B = Delta K R = -f'(1)/2")
    print()
    print(f"endpoint p={p:.12g}")
    print(f"pure-power B=p/2={p / 2.0:.12g}")
    print()

    for profile in profiles:
        print(profile.name)
        print(f"  h'(1)={profile.h_prime_at_1():+.12g}")
        print(f"  f'(1)={profile.boundary_slope():+.12g}")
        print(f"  B=-f'(1)/2={profile.boundary_scalar():.12g}")
        print(f"  eta candidate B/3={profile.boundary_scalar() / 3.0:.12g}")
        print(f"  endpoint prefactor h(eps)~{profile.endpoint_prefactor():.12g}")

    print("\nAudit verdict:")
    print("  - The endpoint exponent p alone does not fix the interface scalar B.")
    print("  - B=p/2 holds for profiles whose shape factor has h'(1)=0.")
    print("  - Linear finite-cell shape corrections shift B at first order.")
    print("  - The metric/orchestra must derive the boundary slope or show why")
    print("    allowed nonlinear shape factors satisfy h'(1)=0 at the phi=0 collar.")


if __name__ == "__main__":
    main()

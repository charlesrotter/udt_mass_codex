import math
from dataclasses import dataclass


@dataclass(frozen=True)
class SourceCase:
    label: str
    s: float

    @property
    def discriminant(self) -> float:
        return 1.0 - 8.0 * self.s

    @property
    def roots(self) -> tuple[float, float] | None:
        if self.discriminant < 0.0:
            return None
        root = math.sqrt(self.discriminant)
        return ((1.0 - root) / 2.0, (1.0 + root) / 2.0)


def beta(q: float, s: float) -> float:
    # Exact q-flow for f'' + 2 f'/r + 2s f/r^2 = 0,
    # with q=-d ln f/d ln r and t=ln r.
    return q * q - q + 2.0 * s


def beta_prime(q: float) -> float:
    return 2.0 * q - 1.0


def integrate_q(q0: float, s: float, dt: float = 0.02, steps: int = 300) -> float:
    q = q0
    for _ in range(steps):
        # RK4 on dq/dt=beta(q,s), t=ln r outward.
        k1 = beta(q, s)
        k2 = beta(q + 0.5 * dt * k1, s)
        k3 = beta(q + 0.5 * dt * k2, s)
        k4 = beta(q + dt * k3, s)
        q += (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
    return q


def main() -> None:
    print("Derived q-flow from radial angular-source equation")
    print("=" * 52)
    print("Start with the constant-source radial equation:")
    print("  f'' + 2 f'/r + 2s f/r^2 = 0")
    print("Define:")
    print("  t = ln r")
    print("  q = - d ln f / d ln r")
    print("Then:")
    print("  f_tt + f_t + 2s f = 0")
    print("  dq/dt = q^2 - q + 2s")
    print()
    print("Fixed points obey:")
    print("  q(1-q)/2 = s")
    print()

    cases = [
        SourceCase("scalar/vacuum source", 0.0),
        SourceCase("self-similar H1 source", 1.0 / 9.0),
        SourceCase("finite-action threshold", 1.0 / 8.0),
        SourceCase("overcritical source", 0.14),
    ]
    for case in cases:
        print(case.label)
        print(f"  s={case.s:.12g}")
        roots = case.roots
        if roots is None:
            print("  no real fixed slopes")
            continue
        for qstar in roots:
            bp = beta_prime(qstar)
            stability = "outward-attractive" if bp < 0 else "outward-repulsive" if bp > 0 else "marginal"
            print(f"  q*={qstar:.12g}")
            print(f"    beta'={bp:+.12g}")
            print(f"    stability for increasing r: {stability}")
        print()

    s = 1.0 / 9.0
    print("Numerical outward flow for s=1/9:")
    for q0 in [0.05, 0.2, 0.32, 0.45, 0.6]:
        q_end = integrate_q(q0, s)
        print(f"  q0={q0:.6f} -> q(t+6)={q_end:.12g}")

    print("\nFlow verdict:")
    print("  - For constant s=1/9, q=1/3 is the outward-attractive finite-action fixed point.")
    print("  - q=2/3 is the companion outward-repulsive/non-finite-action fixed point.")
    print("  - This supports q_phi0=1/3 if the cell boundary layer is governed by")
    print("    the same constant H1 source through the collar.")
    print("  - Remaining nonlinear risk: s may run with radius or branch data,")
    print("    in which case q_phi0 follows the forced flow rather than the fixed point.")


if __name__ == "__main__":
    main()

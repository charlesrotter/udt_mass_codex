import math
from dataclasses import dataclass


S0 = 1.0 / 9.0
Q0 = 1.0 / 3.0


@dataclass(frozen=True)
class SourceProfile:
    name: str
    delta_s: float
    kind: str

    def s(self, x: float) -> float:
        # x in [0, 1], core -> phi0 collar.
        if self.kind == "constant":
            return S0 + self.delta_s
        if self.kind == "core_bump":
            return S0 + self.delta_s * math.exp(-((x - 0.2) / 0.15) ** 2)
        if self.kind == "collar_bump":
            return S0 + self.delta_s * math.exp(-((x - 0.85) / 0.12) ** 2)
        if self.kind == "linear":
            return S0 + self.delta_s * x
        raise ValueError(self.kind)


def beta(q: float, s: float) -> float:
    return q * q - q + 2.0 * s


def integrate(profile: SourceProfile, q_initial: float = Q0, length: float = 6.0, steps: int = 1200) -> float:
    q = q_initial
    dt = length / steps
    for step in range(steps):
        x = step / max(1, steps - 1)

        def rhs(q_value: float, x_value: float) -> float:
            x_clamped = min(1.0, max(0.0, x_value))
            return beta(q_value, profile.s(x_clamped))

        k1 = rhs(q, x)
        k2 = rhs(q + 0.5 * dt * k1, x + 0.5 / steps)
        k3 = rhs(q + 0.5 * dt * k2, x + 0.5 / steps)
        k4 = rhs(q + dt * k3, x + 1.0 / steps)
        q += (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
    return q


def source_for_fixed_q(q: float) -> float:
    return 0.5 * q * (1.0 - q)


def main() -> None:
    print("q-flow source-running audit")
    print("=" * 29)
    print("Derived flow:")
    print("  dq/dt = q^2 - q + 2s(t)")
    print()
    print(f"baseline S0={S0:.12g}, Q0={Q0:.12g}")
    print()

    profiles = [
        SourceProfile("constant +0.005", +0.005, "constant"),
        SourceProfile("constant -0.005", -0.005, "constant"),
        SourceProfile("core bump +0.02", +0.02, "core_bump"),
        SourceProfile("core bump -0.02", -0.02, "core_bump"),
        SourceProfile("collar bump +0.02", +0.02, "collar_bump"),
        SourceProfile("collar bump -0.02", -0.02, "collar_bump"),
        SourceProfile("linear +0.01", +0.01, "linear"),
        SourceProfile("linear -0.01", -0.01, "linear"),
    ]

    for profile in profiles:
        q_end = integrate(profile)
        print(profile.name)
        print(f"  q_phi0={q_end:.12g}")
        print(f"  delta q={q_end - Q0:+.12g}")
        print(f"  eta=q/6={q_end / 6.0:.12g}")

    print("\nDiagnostic source values for residual-required q:")
    for label, q_req in [("M1/mu-like", 0.387510439043), ("E1/tau-like", 0.264116906769)]:
        s_req = source_for_fixed_q(q_req)
        print(label)
        print(f"  q_req={q_req:.12g}")
        print(f"  fixed-source s_req={s_req:.12g}")
        print(f"  delta s={s_req - S0:+.12g}")

    print("\nSource-running verdict:")
    print("  - Branch-specific effective source s(t) can shift q_phi0 with either sign.")
    print("  - Collar-local source changes have stronger direct leverage on q_phi0")
    print("    than core-local bumps of the same size after outward attraction.")
    print("  - This is a native nonlinear correction channel, but using observed")
    print("    masses to choose s(t) would be fitting. Derive s(t) from branch data.")


if __name__ == "__main__":
    main()

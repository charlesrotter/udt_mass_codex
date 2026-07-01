from dataclasses import dataclass


@dataclass(frozen=True)
class ShellCase:
    label: str
    q_inside: float

    @property
    def delta_k_t(self) -> float:
        # Mixed extrinsic curvature jump outer-inner at R=1:
        # K^t_t(inner)=f'/2=-q/2, K^t_t(outer)=0.
        return self.q_inside / 2.0

    @property
    def delta_k_theta(self) -> float:
        return 0.0

    @property
    def delta_k_trace(self) -> float:
        return self.delta_k_t

    @property
    def surface_stress_trace_reversed(self) -> tuple[float, float, float]:
        # Israel form up to the common factor -1/(8piG):
        # S^a_b proportional to -([K^a_b]-delta^a_b [K]).
        # Return dimensionless components inside brackets:
        # T_a = [K^a_a] - [K].
        dk = self.delta_k_trace
        return (
            self.delta_k_t - dk,
            self.delta_k_theta - dk,
            self.delta_k_theta - dk,
        )


def main() -> None:
    cases = [
        ShellCase("self-similar eta collar", 1.0 / 3.0),
        ShellCase("M1-positive q diagnostic", 0.387510439043),
        ShellCase("E1-negative q diagnostic", 0.264116906769),
    ]

    print("phi0 shell-stress signature")
    print("=" * 29)
    print("For flat exterior and inner f'(R)=-q/R:")
    print("  [K^a_b] = diag(q/2R, 0, 0) in (t, theta, phi)")
    print("  [K] = q/2R")
    print()
    print("Israel surface stress is proportional to:")
    print("  -([K^a_b] - delta^a_b [K])")
    print("Common constants and sign convention are omitted; the pattern matters.")
    print()
    for case in cases:
        bracket = case.surface_stress_trace_reversed
        print(case.label)
        print(f"  q={case.q_inside:.12g}")
        print(f"  [K^t_t]={case.delta_k_t:.12g}")
        print(f"  [K^theta_theta]={case.delta_k_theta:.12g}")
        print(f"  [K]={case.delta_k_trace:.12g}")
        print(
            "  bracket [K^a_b]-delta[K] = "
            f"({bracket[0]:+.12g}, {bracket[1]:+.12g}, {bracket[2]:+.12g})"
        )
        print()

    print("Shell signature verdict:")
    print("  - The eta-producing jump has no t-component in the trace-reversed bracket")
    print("    and equal angular components.")
    print("  - The required shell stress is angular/tension-like on the S2 interface.")
    print("  - This is compatible with an H1/angular boundary layer as the carrier.")
    print("  - It is not a radial Coulomb tail; it is an interface angular stress signature.")


if __name__ == "__main__":
    main()

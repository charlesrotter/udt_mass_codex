from dataclasses import dataclass


@dataclass(frozen=True)
class InterfacePower:
    p: float
    label: str

    @property
    def inner_slope_at_unit_radius(self) -> float:
        # f=(R/r)^p, evaluated at R=1.
        return -self.p

    @property
    def trace_curvature_inner(self) -> float:
        # Timelike shell r=R in ds^2=-fdt^2+f^-1dr^2+r^2dOmega^2, R=1, f(R)=1.
        # K = f'/(2 sqrt(f)) + 2 sqrt(f)/R.
        return 2.0 - 0.5 * self.p

    @property
    def trace_curvature_flat_outer(self) -> float:
        return 2.0

    @property
    def trace_jump_outer_minus_inner(self) -> float:
        return self.trace_curvature_flat_outer - self.trace_curvature_inner

    @property
    def angular_mean_jump(self) -> float:
        # Split the trace jump over the three transported frame directions.
        return self.trace_jump_outer_minus_inner / 3.0

    @property
    def half_angular_mean_jump(self) -> float:
        # Half appears naturally in several quadratic/unit-action normalizations;
        # keep it marked as a diagnostic, not a derivation.
        return 0.5 * self.angular_mean_jump


def main() -> None:
    print("Phi=0 interface geometry")
    print("=" * 25)
    print("Metric form: ds^2=-f dt^2+f^-1 dr^2+r^2 dOmega^2")
    print("Timelike shell r=R, f(R)=1:")
    print("  K^t_t = f'/2")
    print("  K^theta_theta = K^phi_phi = 1/R")
    print("  K = f'/2 + 2/R")
    print()
    print("For an inner finite endpoint profile f=(R/r)^p:")
    print("  f'(R)=-p/R")
    print("  K_inner=(2-p/2)/R")
    print("  K_flat_outer=2/R")
    print("  Delta K = K_outer-K_inner = p/(2R)")
    print()

    cases = [
        InterfacePower(0.0, "O0 scalar/no endpoint"),
        InterfacePower(1.0 / 3.0, "self-similar p=1/3 endpoint"),
        InterfacePower(0.5, "finite-action threshold"),
        InterfacePower(1.0, "vacuum p=1 singular branch"),
    ]

    for case in cases:
        print(f"{case.label}:")
        print(f"  p={case.p:.9g}")
        print(f"  f'(R) at R=1 = {case.inner_slope_at_unit_radius:.9g}")
        print(f"  K_inner R = {case.trace_curvature_inner:.9g}")
        print(f"  Delta K R = {case.trace_jump_outer_minus_inner:.9g}")
        print(f"  frame-mean Delta K R /3 = {case.angular_mean_jump:.9g}")
        print(f"  half frame-mean diagnostic = {case.half_angular_mean_jump:.9g}")

    print("\nInterface verdict:")
    print("  - The phi=0 collar contains a native jump Delta K R = p/2.")
    print("  - At the self-similar endpoint p=1/3, Delta K R = 1/6.")
    print("  - Sharing that jump over the three transported frame directions gives 1/18.")
    print("  - This is a real metric occurrence of the eta-sized number,")
    print("    but the equal sharing rule still has to be derived from the boundary form.")


if __name__ == "__main__":
    main()

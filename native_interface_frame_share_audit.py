from dataclasses import dataclass


@dataclass(frozen=True)
class JumpAudit:
    p: float
    label: str

    @property
    def delta_k_t(self) -> float:
        # Mixed component jump outer-inner at R=1:
        # K^t_t(inner)=f'/2=-p/2, K^t_t(outer)=0.
        return self.p / 2.0

    @property
    def delta_k_theta(self) -> float:
        return 0.0

    @property
    def delta_k_phi(self) -> float:
        return 0.0

    @property
    def trace_jump(self) -> float:
        return self.delta_k_t + self.delta_k_theta + self.delta_k_phi

    @property
    def equal_trace_share(self) -> float:
        return self.trace_jump / 3.0

    @property
    def equal_share_squared_error(self) -> float:
        q = self.equal_trace_share
        return (
            (self.delta_k_t - q) ** 2
            + (self.delta_k_theta - q) ** 2
            + (self.delta_k_phi - q) ** 2
        )


def main() -> None:
    print("Interface frame-share audit")
    print("=" * 29)
    print("The shell mixed extrinsic-curvature jump is tensorial:")
    print("  Delta K^a_b = diag(p/2R, 0, 0) in (t, theta, phi) shell directions.")
    print("The scalar trace is:")
    print("  Delta K = p/2R")
    print()
    print("Therefore equal sharing over three labels is not the tensor jump itself.")
    print("It is an additional scalar projection/averaging rule unless derived separately.")
    print()

    for audit in [
        JumpAudit(1.0 / 3.0, "self-similar p=1/3 endpoint"),
        JumpAudit(0.5, "finite-action threshold"),
        JumpAudit(1.0, "vacuum singular p=1 branch"),
    ]:
        print(audit.label)
        print(f"  tensor jump diag = ({audit.delta_k_t:.9g}, 0, 0)")
        print(f"  trace jump = {audit.trace_jump:.9g}")
        print(f"  equal trace share = {audit.equal_trace_share:.9g}")
        print(f"  tensor mismatch squared = {audit.equal_share_squared_error:.9g}")

    print("\nAudit verdict:")
    print("  - p=1/3 gives a native interface scalar Delta K R=1/6.")
    print("  - Dividing by N=3 gives 1/18, but this division is not forced by")
    print("    the extrinsic-curvature tensor on the shell.")
    print("  - To derive eta=1/18, the boundary action must project the scalar")
    print("    jump onto the transported epsilon basis, not the shell tangent tensor.")


if __name__ == "__main__":
    main()

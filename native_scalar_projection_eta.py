from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectionCase:
    p: float
    n: int
    label: str

    @property
    def scalar_jump(self) -> float:
        # Dimensionless interface scalar Delta K * R = p/2.
        return self.p / 2.0

    @property
    def per_label_action(self) -> float:
        # Normalized trace of scalar_jump * I_N.
        return self.scalar_jump / self.n

    @property
    def half_action_weight(self) -> float:
        return 0.5 * self.per_label_action

    @property
    def transfer_trace_prefactor(self) -> float:
        return self.n


def main() -> None:
    print("Scalar projection eta audit")
    print("=" * 27)
    print("Native scalar from phi=0 interface:")
    print("  B = Delta K * R = p/2")
    print()
    print("If B acts on an N-label transported frame space and carries no label index,")
    print("label symmetry makes the operator B * I_N.")
    print("The normalized per-label scalar is:")
    print("  eta = Tr(B I_N) / N^2 = B/N")
    print("equivalently, the action per label is B/N.")
    print()

    cases = [
        ProjectionCase(1.0 / 3.0, 3, "self-similar endpoint on N=3 frame"),
        ProjectionCase(1.0 / 3.0, 2, "self-similar endpoint on N=2 test frame"),
        ProjectionCase(0.5, 3, "finite-action threshold on N=3 frame"),
    ]
    for case in cases:
        print(case.label)
        print(f"  p={case.p:.9g}, N={case.n}")
        print(f"  B=p/2={case.scalar_jump:.9g}")
        print(f"  per-label action B/N={case.per_label_action:.9g}")
        print(f"  half-action weight B/(2N)={case.half_action_weight:.9g}")
        print(f"  transfer trace form: N * exp(-B/(2N))")

    print("\nFor p=1/3 and N=3:")
    print("  B=1/6")
    print("  eta=B/N=1/18")
    print("  eta/2=B/(2N)=1/36")
    print("  gamma=N exp(-eta/2)=3 exp(-1/36)")
    print()
    print("Projection verdict:")
    print("  - The extrinsic-curvature tensor does not split equally.")
    print("  - The scalar boundary jump can split by normalized trace if it acts")
    print("    on a symmetric transported N-label space.")
    print("  - Thus eta=1/18 is conditional on scalar-to-frame projection,")
    print("    not on isotropic shell curvature.")


if __name__ == "__main__":
    main()

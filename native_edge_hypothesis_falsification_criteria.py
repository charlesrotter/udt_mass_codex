from dataclasses import dataclass


@dataclass(frozen=True)
class Criterion:
    name: str
    requirement: str
    failure_mode: str


CRITERIA = [
    Criterion(
        name="native-variable closure",
        requirement="uses f, Pi_f, K_S2, shape data, K_rad, and H1/S2 projection only",
        failure_mode="requires an imported force, EH dynamics, SM label, or fitted mass ratio",
    ),
    Criterion(
        name="linear boundary unit",
        requirement="produces the linear edge unit -Pi_f/R = K_rad/K_S2 = q/2",
        failure_mode="uses ordinary C1 bulk stress, which is quadratic in q",
    ),
    Criterion(
        name="flat exterior",
        requirement="keeps f_out=1 and f'_out=0 outside phi0",
        failure_mode="leaks an exterior 1/r tail or requires exterior mass charge",
    ),
    Criterion(
        name="slope selection",
        requirement="derives or explicitly postulates q_phi0=1/3",
        failure_mode="assumes q without naming the closure input",
    ),
    Criterion(
        name="slope-renormalization audit",
        requirement="accounts for q_phi0=p+delta_h",
        failure_mode="silently identifies endpoint p with collar q",
    ),
    Criterion(
        name="angular projection",
        requirement="uses the exact H1/S2 projection <n_a n_b>=delta_ab/3",
        failure_mode="adds an angular coefficient or degeneracy by hand",
    ),
    Criterion(
        name="scale covariance",
        requirement="depends on dimensionless units such as -Pi_f/R and K_rad/K_S2",
        failure_mode="introduces a dimensionful scale other than the later electron anchor",
    ),
]


def main() -> None:
    print("edge-embedding hypothesis falsification criteria")
    print("=" * 52)
    for criterion in CRITERIA:
        print(criterion.name)
        print(f"  requirement:  {criterion.requirement}")
        print(f"  failure mode: {criterion.failure_mode}")
        print()

    print("Work rule:")
    print("  Treat the edge-embedding hypothesis as a candidate only while it")
    print("  passes these tests. If it fails one, downgrade it immediately.")


if __name__ == "__main__":
    main()

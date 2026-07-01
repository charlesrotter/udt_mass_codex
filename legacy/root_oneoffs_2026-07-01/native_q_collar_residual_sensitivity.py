import math
from dataclasses import dataclass


N = 3
Q0 = 1.0 / 3.0
ELECTRON = 0.51099895
M1_COEFF = 1.1343262
E1_COEFF = 2.10394
TARGET_MU = 105.6583755
TARGET_TAU = 1776.86


@dataclass(frozen=True)
class Branch:
    name: str
    nodes: int
    coeff_ratio: float
    target: float


def gamma_from_q(q: float) -> float:
    # eta=q/6, one-sided action eta/2=q/12.
    return N * math.exp(-q / 12.0)


def mass(branch: Branch, q: float) -> float:
    return ELECTRON * branch.coeff_ratio * gamma_from_q(q) ** branch.nodes


def required_q(branch: Branch) -> float:
    ratio = branch.target / (ELECTRON * branch.coeff_ratio)
    # ratio = (N exp(-q/12))^nodes
    return -12.0 * (math.log(ratio) / branch.nodes - math.log(N))


def main() -> None:
    branches = [
        Branch("M1/mu-like", 5, 1.0, TARGET_MU),
        Branch("E1/tau-like", 7, E1_COEFF / M1_COEFF, TARGET_TAU),
    ]

    print("q-collar residual sensitivity")
    print("=" * 31)
    print("Diagnostic only: observations test whether a collar-slope shift could")
    print("explain residuals after the typed graph is fixed.")
    print()
    print(f"baseline q={Q0:.12g}")
    print(f"baseline gamma={gamma_from_q(Q0):.12g}")
    print()

    for branch in branches:
        baseline = mass(branch, Q0)
        q_req = required_q(branch)
        print(branch.name)
        print(f"  nodes={branch.nodes}")
        print(f"  baseline mass={baseline:.9g} MeV")
        print(f"  target mass={branch.target:.9g} MeV")
        print(f"  baseline fractional error={baseline / branch.target - 1.0:+.4%}")
        print(f"  required q={q_req:.12g}")
        print(f"  required delta q={q_req - Q0:+.12g}")
        print(f"  required eta=q/6={q_req / 6.0:.12g}")

    print("\nSensitivity verdict:")
    print("  - Mu-like branch wants larger q than 1/3 to lower its mass.")
    print("  - Tau-like branch wants smaller q than 1/3 to raise its mass.")
    print("  - A single common nonlinear collar slope cannot fix both residuals.")
    print("  - If residuals are nonlinear q effects, they must be branch-specific")
    print("    or come through branch coefficients/measure factors, not a universal q.")


if __name__ == "__main__":
    main()

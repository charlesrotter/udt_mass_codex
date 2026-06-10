import math
from dataclasses import dataclass
from fractions import Fraction


ELECTRON_MEV = 0.51099895
Q = Fraction(1, 3)
ETA = Q / 6
GAMMA = 3.0 * math.exp(-float(ETA / 2))

M1_COEFF = 1.1343262
E1_COEFF = 2.10394

TARGETS = {
    "mu_like": 105.6583755,
    "tau_like": 1776.86,
}


@dataclass(frozen=True)
class Branch:
    label: str
    sector: str
    typed_nodes: int
    coeff: float
    status: str


BRANCHES = [
    Branch(
        label="mu_like",
        sector="M1",
        typed_nodes=5,
        coeff=M1_COEFF,
        status="typed depth and coefficient still diagnostic",
    ),
    Branch(
        label="tau_like",
        sector="E1",
        typed_nodes=7,
        coeff=E1_COEFF,
        status="typed depth and coefficient still diagnostic",
    ),
]


def main() -> None:
    print("banked P_phi0 mass diagnostic")
    print("=" * 35)
    print("Resolved by banked P_phi0:")
    print("  q=1/3, eta=1/18")
    print()
    print("Still diagnostic:")
    print(f"  gamma=3 exp(-eta/2)={GAMMA:.12g}")
    print("  typed node depths")
    print("  branch coefficient ratio")
    print()

    anchor_coeff = M1_COEFF
    for branch in BRANCHES:
        coeff_ratio = branch.coeff / anchor_coeff
        ratio = coeff_ratio * GAMMA**branch.typed_nodes
        mass = ELECTRON_MEV * ratio
        target = TARGETS[branch.label]
        print(branch.label)
        print(f"  sector={branch.sector}")
        print(f"  typed_nodes={branch.typed_nodes}")
        print(f"  coeff_ratio={coeff_ratio:.12g}")
        print(f"  predicted_mass_MeV={mass:.12g}")
        print(f"  diagnostic_target_MeV={target:.12g}")
        print(f"  fractional_error={mass / target - 1.0:+.4%}")
        print(f"  status={branch.status}")
        print()

    print("Verdict:")
    print("  P_phi0 improves the foundation of eta.")
    print("  It does not by itself validate gamma, depths, or coefficients.")


if __name__ == "__main__":
    main()

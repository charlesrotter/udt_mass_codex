import math
from dataclasses import dataclass


N = 3
P = 1.0 / 3.0
B = P / 2.0
ETA = B / 3.0
GAMMA = N * math.exp(-ETA / 2.0)
ELECTRON_MEV = 0.51099895

# Current finite-cell angular coefficients retained as diagnostics from the
# earlier working ladder. They are not Standard Model inputs.
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
    graph_status: str


BRANCHES = [
    Branch(
        label="mu_like",
        sector="M1",
        typed_nodes=5,
        coeff=M1_COEFF,
        graph_status="3 shared H1 frame nodes + 2 primitive compact/radial shape nodes",
    ),
    Branch(
        label="tau_like",
        sector="E1",
        typed_nodes=7,
        coeff=E1_COEFF,
        graph_status="3 shared H1 frame nodes + 4 ordinary H1 shape nodes",
    ),
]


def main() -> None:
    print("Typed graph mass diagnostic")
    print("=" * 29)
    print("Metric/orchestra chain:")
    print(f"  p={P:.12g}")
    print(f"  B=p/2={B:.12g}")
    print(f"  eta=B/3={ETA:.12g}")
    print(f"  gamma=3 exp(-eta/2)={GAMMA:.12g}")
    print()
    print("Observation use:")
    print("  electron mass anchors the scale.")
    print("  mu/tau masses are diagnostics only.")
    print("  branch coefficients are current finite-cell diagnostics, not SM imports.")
    print()

    anchor_coeff = M1_COEFF
    for branch in BRANCHES:
        coeff_ratio = branch.coeff / anchor_coeff
        ratio = coeff_ratio * GAMMA**branch.typed_nodes
        mass = ELECTRON_MEV * ratio
        target = TARGETS[branch.label]
        print(branch.label)
        print(f"  sector={branch.sector}")
        print(f"  typed closure nodes={branch.typed_nodes}")
        print(f"  graph status={branch.graph_status}")
        print(f"  coeff ratio={coeff_ratio:.12g}")
        print(f"  predicted mass={mass:.9g} MeV")
        print(f"  diagnostic target={target:.9g} MeV")
        print(f"  fractional error={mass / target - 1.0:+.4%}")
        print()

    print("Diagnostic verdict:")
    print("  - The typed graph reproduces the previous compact ladder structure.")
    print("  - Agreement remains diagnostic, not a derivation.")
    print("  - Current open items: graph factorization, Pbundle0/nontrivial compact")
    print("    occupation, and branch coefficient derivation.")


if __name__ == "__main__":
    main()

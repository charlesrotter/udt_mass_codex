from dataclasses import dataclass
import math


ELECTRON_MEV = 0.51099895
MUON_MEV = 105.6583755
TAU_MEV = 1776.86

ETA = 1.0 / 18.0
GAMMA = 3.0 * math.exp(-ETA / 2.0)
N_M1 = 5
N_E1 = 7


@dataclass(frozen=True)
class Diagnostic:
    name: str
    value: float
    allowed_use: str
    forbidden_use: str


def main() -> None:
    mu_ratio = MUON_MEV / ELECTRON_MEV
    tau_ratio = TAU_MEV / ELECTRON_MEV
    gamma5 = GAMMA**N_M1
    gamma7 = GAMMA**N_E1
    required_c_m1 = mu_ratio / gamma5
    required_c_e1 = tau_ratio / gamma7
    required_ratio = (tau_ratio / mu_ratio) / (GAMMA ** (N_E1 - N_M1))

    diagnostics = [
        Diagnostic(
            "mu/e ratio pressure on C_M1",
            required_c_m1,
            "compare against a later derived C_M1",
            "define C_M1 from this value",
        ),
        Diagnostic(
            "tau/e ratio pressure on C_E1",
            required_c_e1,
            "compare against a later derived C_E1",
            "define C_E1 from this value",
        ),
        Diagnostic(
            "tau/mu pressure on C_E1/C_M1",
            required_ratio,
            "test a later derived coefficient ratio",
            "choose E1 over M2 or tune branch weights",
        ),
    ]

    print("lepton-ratio diagnostic lane")
    print("=" * 30)
    print(f"gamma = {GAMMA:.12g}")
    print(f"gamma^5 = {gamma5:.12g}")
    print(f"gamma^7 = {gamma7:.12g}")
    print()
    print(f"mu/e observed ratio = {mu_ratio:.12g}")
    print(f"tau/e observed ratio = {tau_ratio:.12g}")
    print(f"tau/mu observed ratio = {tau_ratio / mu_ratio:.12g}")
    print()
    for diagnostic in diagnostics:
        print(diagnostic.name)
        print(f"  diagnostic value: {diagnostic.value:.12g}")
        print(f"  allowed use:      {diagnostic.allowed_use}")
        print(f"  forbidden use:    {diagnostic.forbidden_use}")
        print()

    print("Diagnostic verdict:")
    print("  Lepton ratios are useful as downstream pressure tests.")
    print("  They cannot select P_transfer, P_depth, Pbundle0, M2 suppression,")
    print("  or coefficient values inside Tier D.")


if __name__ == "__main__":
    main()

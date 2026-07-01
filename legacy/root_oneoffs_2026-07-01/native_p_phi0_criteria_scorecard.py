from dataclasses import dataclass


@dataclass(frozen=True)
class Check:
    criterion: str
    status: str
    reason: str


CHECKS = [
    Check(
        criterion="native-variable closure",
        status="passes",
        reason="uses Pi_f, K_rad, K_S2, and H1/S2 projection only",
    ),
    Check(
        criterion="linear boundary unit",
        status="passes",
        reason="postulates -Pi_f/R = K_rad/K_S2 = 1/6",
    ),
    Check(
        criterion="flat exterior",
        status="passes if treated as interface Neumann data",
        reason="flat exterior has Pi_out=0; the jump is localized at phi0",
    ),
    Check(
        criterion="slope selection",
        status="passes as postulate, not derivation",
        reason="selects q=1/3 explicitly rather than hiding it",
    ),
    Check(
        criterion="slope-renormalization audit",
        status="passes under constant s=1/9 plus finite-action filter",
        reason="finite action removes q=2/3 branch, leaving delta_h=0",
    ),
    Check(
        criterion="angular projection",
        status="passes",
        reason="eta uses exact <n_a n_b>=delta_ab/3",
    ),
    Check(
        criterion="scale covariance",
        status="passes",
        reason="closure uses dimensionless -Pi_f/R and K_rad/K_S2",
    ),
    Check(
        criterion="non-circular s=1/9 derivation",
        status="open",
        reason="requires a native two-factor edge kernel or remains part of P_phi0",
    ),
]


def main() -> None:
    print("P_phi0 criteria scorecard")
    print("=" * 29)
    for check in CHECKS:
        print(check.criterion)
        print(f"  status: {check.status}")
        print(f"  reason: {check.reason}")
        print()

    print("Scorecard verdict:")
    print("  P_phi0 is internally clean as a minimal closure postulate.")
    print("  It is not yet internally derived because the non-circular two-factor")
    print("  source kernel remains open.")


if __name__ == "__main__":
    main()

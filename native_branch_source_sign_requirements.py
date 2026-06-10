from dataclasses import dataclass


ETA = 1.0 / 18.0
S0 = 1.0 / 9.0


@dataclass(frozen=True)
class BranchRequirement:
    branch: str
    q_required: float
    native_role: str
    possible_native_source: str
    caution: str

    @property
    def s_required(self) -> float:
        return 0.5 * self.q_required * (1.0 - self.q_required)

    @property
    def delta_s(self) -> float:
        return self.s_required - S0

    @property
    def delta_s_over_eta(self) -> float:
        return self.delta_s / ETA


REQUIREMENTS = [
    BranchRequirement(
        branch="M1 / mu-like",
        q_required=0.387510439043,
        native_role="primitive compact branch bridged into H1",
        possible_native_source="compact primitive boundary data could add positive collar source",
        caution="do not assign this source unless compact boundary action derives it",
    ),
    BranchRequirement(
        branch="E1 / tau-like",
        q_required=0.264116906769,
        native_role="ordinary H1 endpoint-resonant branch",
        possible_native_source="ordinary relative-shape normalization could reduce effective collar source",
        caution="negative source shift must come from derived shape/action weighting, not residual fitting",
    ),
]


def main() -> None:
    print("Branch-specific source-sign requirements")
    print("=" * 41)
    print("Diagnostic only: translate residual-required q shifts into effective")
    print("fixed-source shifts using s=q(1-q)/2.")
    print()
    print(f"baseline s0={S0:.12g}")
    print(f"eta={ETA:.12g}")
    print()
    for req in REQUIREMENTS:
        sign = "positive" if req.delta_s > 0 else "negative" if req.delta_s < 0 else "zero"
        print(req.branch)
        print(f"  q_required={req.q_required:.12g}")
        print(f"  s_required={req.s_required:.12g}")
        print(f"  delta_s={req.delta_s:+.12g}")
        print(f"  delta_s/eta={req.delta_s_over_eta:+.12g}")
        print(f"  sign needed={sign}")
        print(f"  native role={req.native_role}")
        print(f"  possible native source={req.possible_native_source}")
        print(f"  caution={req.caution}")
        print()

    print("Sign verdict:")
    print("  - M1 wants a positive effective collar-source shift.")
    print("  - E1 wants a negative effective collar-source shift.")
    print("  - This sign split is compatible with an orchestra picture where compact")
    print("    topology and ordinary H1 shape weighting affect the collar differently.")
    print("  - It is not a derivation. The source profile must come from the nonlinear")
    print("    boundary action before this can be used.")


if __name__ == "__main__":
    main()

from dataclasses import dataclass


@dataclass(frozen=True)
class DepthClaim:
    branch: str
    current_depth: int
    current_count: str
    risk: str
    required_derivation: str


CLAIMS = [
    DepthClaim(
        branch="M1 / mu-like",
        current_depth=5,
        current_count="3 shared H1 frame nodes + 2 primitive compact/radial shape nodes",
        risk="primitive compact nodes may be bridge variables rather than independent transfer nodes",
        required_derivation="show which compact/radial variables produce independent transfer factors",
    ),
    DepthClaim(
        branch="E1 / tau-like",
        current_depth=7,
        current_count="3 shared H1 frame nodes + 4 ordinary H1 shape nodes",
        risk="ordinary H1 shape nodes may double-count frame or boundary variables",
        required_derivation="derive four independent E1 edge-shape transfer nodes",
    ),
]


def main() -> None:
    print("typed depth next audit")
    print("=" * 24)
    for claim in CLAIMS:
        print(claim.branch)
        print(f"  current depth:        {claim.current_depth}")
        print(f"  current count:        {claim.current_count}")
        print(f"  risk:                 {claim.risk}")
        print(f"  required derivation:  {claim.required_derivation}")
        print()

    print("No-invention verdict:")
    print("  After P_phi0 and P_transfer, typed depth is the next major load-bearing")
    print("  piece. It must be derived as independent edge-transfer nodes, not tuned")
    print("  from the observed mu/tau masses.")


if __name__ == "__main__":
    main()

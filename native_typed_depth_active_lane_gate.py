from dataclasses import dataclass


@dataclass(frozen=True)
class BranchDepth:
    branch: str
    exact_geometry: str
    candidate_depth: str
    missing_gate: str
    active_status: str


DEPTHS = [
    BranchDepth(
        "M1 compact primitive",
        "CP1/Hopf data pushes into the common H1 frame; primitive compact/radial scalar can add one shape node per side",
        "3 shared H1 frame nodes + 1 core shape + 1 phi0 shape = 5",
        "prove those five variables are independent transfer factors after Hopf-frame merging",
        "candidate P_depth_M1, not derived",
    ),
    BranchDepth(
        "E1 ordinary H1",
        "ordinary H1 after common-amplitude removal has a two-dimensional relative-shape plane",
        "3 shared H1 frame nodes + 2 core shapes + 2 phi0 shapes = 7",
        "prove the two relative-shape coordinates at each side factor as independent transfer nodes",
        "candidate P_depth_E1, not derived",
    ),
]


def main() -> None:
    print("typed-depth active-lane gate")
    print("=" * 30)
    for depth in DEPTHS:
        print(depth.branch)
        print(f"  exact geometry:   {depth.exact_geometry}")
        print(f"  candidate depth:  {depth.candidate_depth}")
        print(f"  missing gate:     {depth.missing_gate}")
        print(f"  active status:    {depth.active_status}")
        print()

    print("Depth verdict:")
    print("  The geometry supports the ingredients of 5 and 7.")
    print("  The transfer-node independence is still a graph/action claim.")
    print("  Therefore typed depth remains conditional unless a boundary Hessian")
    print("  or edge graph derives the factorization.")


if __name__ == "__main__":
    main()

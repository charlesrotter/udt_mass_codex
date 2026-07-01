from dataclasses import dataclass


@dataclass(frozen=True)
class Split:
    item: str
    uncovered_status: str
    missing_status: str


SPLITS = [
    Split(
        "eta carrier",
        "q/2 appears as boundary momentum, curvature jump, and angular stress; H1 projection gives q/6",
        "q=1/3 remains banked as P_phi0",
    ),
    Split(
        "transfer operator shape",
        "L1=I3 on ell=1 and heat-kernel trace gives 3 exp(-t)",
        "metric has not identified t=eta/2 without P_transfer",
    ),
    Split(
        "bulk propagation alternative",
        "positional dilation gives exact warped DtN operator",
        "action has not selected bulk-DtN over interface-local transfer",
    ),
    Split(
        "typed node arena",
        "H1 frame, Hopf/CP1 bridge, and E1 relative plane are exact geometries",
        "node independence and factorization remain P_depth unless derived",
    ),
    Split(
        "coefficient arena",
        "symmetry restricts Hessian blocks to identity/scalar forms",
        "free constants/couplings remain until S_phi0 second jet is derived",
    ),
    Split(
        "M2 handling",
        "metric/topology demotes M2 if Pbundle0 is admitted because n=2 is nonprimitive",
        "compact bundle occupancy Pbundle0 itself is not forced by the bare metric",
    ),
]


def main() -> None:
    print("metric uncovered vs missing split")
    print("=" * 34)
    for split in SPLITS:
        print(split.item)
        print(f"  uncovered: {split.uncovered_status}")
        print(f"  missing:   {split.missing_status}")
        print()

    print("Split verdict:")
    print("  This is not an empty fit scaffold: several load-bearing structures")
    print("  are metric-uncovered. But the remaining gaps are real and should stay")
    print("  named rather than filled by coefficient choices.")


if __name__ == "__main__":
    main()

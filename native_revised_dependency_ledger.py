from dataclasses import dataclass


@dataclass(frozen=True)
class Dependency:
    item: str
    old_status: str
    new_status: str
    remaining_gap: str


DEPENDENCIES = [
    Dependency(
        item="eta=1/18",
        old_status="Pepsilon normalization postulate",
        new_status="conditional scalar-boundary projection: p=1/3, B=1/6, eta=B/N",
        remaining_gap="derive trace-preserving lift Tr(S_label)=B",
    ),
    Dependency(
        item="gamma=N exp(-eta/2)",
        old_status="native-looking transfer ansatz",
        new_status="conditional trace of symmetric one-sided boundary kernel",
        remaining_gap="show each closure constraint is represented by the kernel",
    ),
    Dependency(
        item="M1 to H1 frame mediation",
        old_status="conditional compact branch frame assumption",
        new_status="Hopf/projective bridge CP1=S2 for primitive compact doublet",
        remaining_gap="show boundary action uses phase-invariant bilinears",
    ),
    Dependency(
        item="M1 primitive selection",
        old_status="primitive nonzero compact flux if Pbundle0 admitted",
        new_status="primitive flux plus unique projective S2 interface match",
        remaining_gap="derive why nontrivial compact bundle is occupied",
    ),
    Dependency(
        item="2(d-1) shape count",
        old_status="boundary-count ansatz",
        new_status="variationally natural independent endpoint shape data",
        remaining_gap="check no metric condition ties the two endpoints",
    ),
    Dependency(
        item="N_frame=3",
        old_status="epsilon/angular postulate pressure",
        new_status="metric-native lowest non-scalar S2 frame",
        remaining_gap="derive universal use by all surviving branch closures",
    ),
    Dependency(
        item="closure independence",
        old_status="factorized entropy assumption",
        new_status="still the main unresolved hierarchy condition",
        remaining_gap="derive factor graph; rule out equality correlations",
    ),
    Dependency(
        item="electron anchor",
        old_status="dimensionful input F",
        new_status="unchanged accepted anchor",
        remaining_gap="none within current one-anchor program",
    ),
]


def main() -> None:
    print("Revised dependency ledger")
    print("=" * 26)
    for dep in DEPENDENCIES:
        print(dep.item)
        print(f"  old: {dep.old_status}")
        print(f"  new: {dep.new_status}")
        print(f"  gap: {dep.remaining_gap}")

    print("\nCurrent bottleneck:")
    print("  The largest remaining live assumption is not eta or gamma directly.")
    print("  It is the boundary closure factor graph: which constraints exist,")
    print("  whether they use the common frame kernel, and whether they are independent.")


if __name__ == "__main__":
    main()

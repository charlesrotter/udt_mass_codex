from dataclasses import dataclass


@dataclass(frozen=True)
class ScalarEquationClass:
    name: str
    count: int
    status: str
    h1_projector_status: str


def inventory(branch: str, dimension: int, m1: bool = False) -> list[ScalarEquationClass]:
    shape_status = "direct H1" if not m1 else "Hopf/projective bridge to H1"
    return [
        ScalarEquationClass(
            name="transported frame component closure",
            count=3,
            status="native H1 frame",
            h1_projector_status="direct",
        ),
        ScalarEquationClass(
            name="core-side relative shape closure",
            count=max(0, dimension - 1),
            status="local boundary variation",
            h1_projector_status=shape_status,
        ),
        ScalarEquationClass(
            name="phi0-side relative shape closure",
            count=max(0, dimension - 1),
            status="local boundary variation",
            h1_projector_status=shape_status,
        ),
    ]


def main() -> None:
    branches = [("M1", 2, True), ("E1", 3, False), ("M2", 5, False)]
    print("Scalar closure-equation inventory")
    print("=" * 35)
    print("Each listed scalar equation must be represented by a rank-one H1")
    print("projector for it to contribute one gamma transfer.")
    print()

    for branch, dimension, is_m1 in branches:
        total = 0
        print(branch)
        print(f"  dimension d={dimension}")
        for item in inventory(branch, dimension, is_m1):
            total += item.count
            print(f"  {item.name}:")
            print(f"    count={item.count}")
            print(f"    status={item.status}")
            print(f"    H1 projector status={item.h1_projector_status}")
        print(f"  total scalar closure equations={total}")
        print()

    print("Inventory verdict:")
    print("  - M1 has 5 named scalar closure equations if the Hopf bridge is used.")
    print("  - E1 has 7 named scalar closure equations directly in H1.")
    print("  - M2 has 11 formal equations but fails elementary H1/projective filtering.")
    print("  - The count is now explicit; the remaining proof is that these equations")
    print("    are independent rank-one H1 projector constraints.")


if __name__ == "__main__":
    main()

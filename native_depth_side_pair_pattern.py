from dataclasses import dataclass


@dataclass(frozen=True)
class Branch:
    name: str
    common_h1_frame: int
    side_shape_dimension: int
    side_count: int
    current_status: str

    @property
    def depth(self) -> int:
        return self.common_h1_frame + self.side_count * self.side_shape_dimension


BRANCHES = [
    Branch(
        "M1 compact primitive",
        common_h1_frame=3,
        side_shape_dimension=1,
        side_count=2,
        current_status="candidate: compact residual shape scalar per side",
    ),
    Branch(
        "E1 ordinary H1",
        common_h1_frame=3,
        side_shape_dimension=2,
        side_count=2,
        current_status="candidate: relative H1 shape plane per side",
    ),
]


def main() -> None:
    print("depth side-pair pattern")
    print("=" * 25)
    print("Candidate depth pattern:")
    print("  depth = common H1 frame + two boundary sides * side-shape dimension")
    print("        = 3 + 2s")
    print()
    for branch in BRANCHES:
        print(branch.name)
        print(f"  common H1 frame nodes = {branch.common_h1_frame}")
        print(f"  side shape dimension  = {branch.side_shape_dimension}")
        print(f"  boundary sides        = {branch.side_count}")
        print(f"  depth                 = {branch.depth}")
        print(f"  status                = {branch.current_status}")
        print()

    print("Pattern verdict:")
    print("  The 5 and 7 depths have a shared metric form: 3 + 2s.")
    print("  This is stronger than two unrelated counts, but it still depends")
    print("  on proving that each side-shape coordinate is an independent")
    print("  internal transfer label.")


if __name__ == "__main__":
    main()

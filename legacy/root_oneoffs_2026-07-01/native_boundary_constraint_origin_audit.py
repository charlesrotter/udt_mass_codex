from dataclasses import dataclass


@dataclass(frozen=True)
class Branch:
    name: str
    dimension: int
    status: str

    def constraints(self, frame_count: int) -> dict[str, int]:
        non_scalar = max(0, self.dimension - 1)
        return {
            "frame_orientation": frame_count,
            "core_shape": non_scalar,
            "phi0_shape": non_scalar,
        }

    def total(self, frame_count: int) -> int:
        return sum(self.constraints(frame_count).values())


def main() -> None:
    frame_count = 3
    branches = [
        Branch("O0", 1, "formal scalar, no negative-phi matter endpoint"),
        Branch("M1", 2, "compact/primitive doublet candidate"),
        Branch("E1", 3, "ordinary triplet endpoint-resonant candidate"),
        Branch("M2", 5, "nonprimitive or nonresonant higher branch"),
    ]

    print("Boundary constraint-origin audit")
    print("=" * 32)
    print("Candidate count:")
    print("  n_close(d) = N_frame + 2(d-1)")
    print()
    print("Metric-native ingredients:")
    print("  N_frame: transported oriented frame/epsilon closure count.")
    print("  d-1: non-scalar sector-shape data after removing the common scalar mode.")
    print("  factor 2: two finite-cell boundaries, core-side and phi=0 side.")
    print()

    for branch in branches:
        constraints = branch.constraints(frame_count)
        print(branch.name)
        print(f"  dimension d={branch.dimension}")
        print(f"  status={branch.status}")
        for name, value in constraints.items():
            print(f"  {name} constraints={value}")
        print(f"  total closure count={branch.total(frame_count)}")

    print("\nWhat this count derives if accepted:")
    print("  - M1 has 3+1+1=5 closure constraints.")
    print("  - E1 has 3+2+2=7 closure constraints.")
    print("  - O0 has a formal count of 3 but no non-scalar endpoint branch.")
    print("  - M2 has 11 and should not be elementary under the primitive/resonance filter.")
    print()
    print("Open links:")
    print("  1. Why each closure constraint is epsilon-mediated.")
    print("  2. Why the frame-orientation count is N_frame=3 for every surviving branch.")
    print("  3. Why the two boundary shape constraints are independent rather than correlated.")
    print("  4. Why each accepted constraint contributes the same transfer trace gamma.")
    print()
    print("Audit verdict:")
    print("  n=5 and n=7 can be stated as boundary data counts, not mass-read values.")
    print("  The formula is still conditional until the four open links are derived.")


if __name__ == "__main__":
    main()

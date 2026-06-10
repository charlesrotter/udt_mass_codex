from dataclasses import dataclass


@dataclass(frozen=True)
class MeasureResult:
    branch: str
    space: str
    result: str
    implication: str


RESULTS = [
    MeasureResult(
        branch="M1",
        space="CP1/Fubini-Study via Hopf",
        result="pushes forward to round S2 with <n_a n_b>=delta_ab/3",
        implication="no bare compact-projective anisotropy",
    ),
    MeasureResult(
        branch="E1",
        space="relative-shape plane after removing common amplitude",
        result="isotropic two-dimensional plane with <u_i u_j>=delta_ij/2",
        implication="no bare ordinary relative-shape anisotropy",
    ),
]


def main() -> None:
    print("Measure audit summary")
    print("=" * 21)
    for result in RESULTS:
        print(result.branch)
        print(f"  space:       {result.space}")
        print(f"  result:      {result.result}")
        print(f"  implication: {result.implication}")
    print()
    print("Summary verdict:")
    print("  Bare geometry measures are clean on both M1 and E1 sides.")
    print("  This strengthens the shared isotropic skeleton.")
    print("  Residual-sized corrections are more likely to come from:")
    print("    - nonlinear boundary action weights")
    print("    - gluing/Jacobian determinants")
    print("    - branch coefficient normalization")
    print("    - branch-specific q-flow/boundary layers")
    print("  rather than from simple measure anisotropy.")


if __name__ == "__main__":
    main()

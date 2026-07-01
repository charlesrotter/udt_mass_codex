from dataclasses import dataclass


@dataclass(frozen=True)
class TwoSideCase:
    name: str
    cross_coupling: str
    eigenvalues: str
    schur_if_one_side_eliminated: str
    verdict: str


CASES = [
    TwoSideCase(
        "local independent sides",
        "c = 0",
        "k, k on each side-shape coordinate",
        "k",
        "product trace allowed if labels are internal and independent",
    ),
    TwoSideCase(
        "symmetric same-representation coupling",
        "c != 0 in [[kI_s,cI_s],[cI_s,kI_s]]",
        "k+c and k-c, each with degeneracy s",
        "k - c^2/k",
        "exact reduction formula, but c must come from the metric boundary action",
    ),
    TwoSideCase(
        "hard side matching",
        "constraint x_core = x_phi0",
        "one side-pair variable instead of two independent variables",
        "not a Schur coefficient; it changes depth",
        "would reduce depth and invalidate gamma^(3+2s)",
    ),
]


def main() -> None:
    print("two-side shape Schur pattern")
    print("=" * 30)
    print("Let each side-shape space have dimension s and isotropic block k I_s.")
    print()
    for case in CASES:
        print(case.name)
        print(f"  cross coupling:              {case.cross_coupling}")
        print(f"  eigenvalues:                 {case.eigenvalues}")
        print(f"  if one side is eliminated:   {case.schur_if_one_side_eliminated}")
        print(f"  verdict:                     {case.verdict}")
        print()

    print("Pattern verdict:")
    print("  The depth pattern 3+2s requires the local independent-sides case.")
    print("  Any same-representation cross coupling or hard matching must be")
    print("  derived before it can modify coefficients or depth.")


if __name__ == "__main__":
    main()

from dataclasses import dataclass


@dataclass(frozen=True)
class HiddenMetricItem:
    structure: str
    native_object: str
    already_used: str
    possible_missing_piece: str
    fit_guardrail: str


ITEMS = [
    HiddenMetricItem(
        structure="phi=0 interface",
        native_object="induced metric, extrinsic curvature, and jump/boundary variation",
        already_used="Used qualitatively as the cell boundary.",
        possible_missing_piece="A boundary action or matching condition that sets closure count or eta.",
        fit_guardrail="Must be derived before comparing to mu/tau residuals.",
    ),
    HiddenMetricItem(
        structure="punctured endpoint topology",
        native_object="linking S2, collar S2 x I, orientation class",
        already_used="Used for primitive compact U(1) sectors after Pbundle0.",
        possible_missing_piece="A native obstruction that makes the nontrivial bundle compulsory.",
        fit_guardrail="Cannot choose flux sector by mass success alone.",
    ),
    HiddenMetricItem(
        structure="angular measure and Laplacian",
        native_object="round S2 eigenbasis, degeneracy, determinant, heat-kernel finite part",
        already_used="Used for orthogonality and representation labels.",
        possible_missing_piece="Branch-dependent determinant contribution, especially E1-positive.",
        fit_guardrail="Require a fixed subtraction prescription and target-blind sign prediction.",
    ),
    HiddenMetricItem(
        structure="radial proper distance",
        native_object="dl=e^{phi} dr and redshifted radial measure",
        already_used="Used in finite-action scaling and radius-flow probes.",
        possible_missing_piece="A scale-flow invariant that changes depth count rather than mass directly.",
        fit_guardrail="Must not introduce a freely tunable branch coefficient.",
    ),
    HiddenMetricItem(
        structure="Maxwell cancellation",
        native_object="sqrt(-g) g^rr g^tt = -r^2 sin(theta)",
        already_used="Pinned as real phi-blind Coulomb dynamics.",
        possible_missing_piece="Coulomb boundary energy could be branch-selective through angular charge labels.",
        fit_guardrail="Use charge/selection labels already present; do not add a non-abelian force.",
    ),
    HiddenMetricItem(
        structure="self-adjoint endpoint data",
        native_object="deficiency index, limit-point/limit-circle behavior, admissible boundary form",
        already_used="Used earlier for core regularization in old spinor language.",
        possible_missing_piece="Import-free scalar/frame version may define allowed endpoint channels.",
        fit_guardrail="Avoid re-importing Dirac Form T; express the result in metric/angular boundary data.",
    ),
    HiddenMetricItem(
        structure="nonlinear angular back-reaction",
        native_object="angular stress shape feeding the phi equation",
        already_used="Approximated by s/r^2 source softening.",
        possible_missing_piece="Multiple angular instruments may add nonlinearly, creating the orchestra effect.",
        fit_guardrail="Derive the interaction matrix first; do not assign residual coefficients.",
    ),
]


def main() -> None:
    print("Hidden metric audit")
    print("=" * 19)
    for idx, item in enumerate(ITEMS, start=1):
        print(f"\n{idx}. {item.structure}")
        print(f"   native object: {item.native_object}")
        print(f"   already used:  {item.already_used}")
        print(f"   missing piece: {item.possible_missing_piece}")
        print(f"   guardrail:     {item.fit_guardrail}")

    print("\nImmediate target-blind tests:")
    print("  - Derive phi=0 boundary variation terms from the C1 action.")
    print("  - Couple the pinned Coulomb sector to the branch ledger before using determinants.")
    print("  - Recast endpoint admissibility without spinor/Dirac Form T language.")
    print("  - Build the angular interaction matrix from metric objects, then compare to residual signs.")


if __name__ == "__main__":
    main()

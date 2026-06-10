from dataclasses import dataclass


@dataclass(frozen=True)
class Piece:
    name: str
    supplied_by_metric: str
    current_status: str


PIECES = [
    Piece(
        "boundary value projector",
        "phi0 definition f=1",
        "filled",
    ),
    Piece(
        "momentum-jump projector",
        "C1 boundary momentum Delta Pi/R=q/2",
        "filled after q is selected/banked",
    ),
    Piece(
        "H1 angular projector",
        "round S2 ell=1 subspace",
        "filled after H1 selection",
    ),
    Piece(
        "trace measure",
        "induced S2 measure, Tr P_H1=3",
        "filled",
    ),
    Piece(
        "internal gluing contraction",
        "opposite-orientation boundary symplectic form",
        "filled if phi0 is the two-sided bridge",
    ),
    Piece(
        "exact two-sided Calderon projector",
        "bulk extension problem on both phi sides",
        "not yet constructed",
    ),
    Piece(
        "transfer-action branch",
        "intrinsic boundary action or warped on-shell DtN",
        "still a fork",
    ),
]


def main() -> None:
    print("Calderon projector gap status")
    print("=" * 30)
    for piece in PIECES:
        print(piece.name)
        print(f"  supplied by metric: {piece.supplied_by_metric}")
        print(f"  current status:     {piece.current_status}")
        print()

    print("Status verdict:")
    print("  Most projector ingredients are now visible. The remaining nontrivial")
    print("  construction is the exact two-sided Calderon projector and the choice")
    print("  of intrinsic-boundary versus warped-DtN action inside it.")


if __name__ == "__main__":
    main()

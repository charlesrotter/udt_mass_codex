from dataclasses import dataclass


@dataclass(frozen=True)
class Piece:
    name: str
    current_status: str
    hessian_role: str


PIECES = [
    Piece(
        "value closure a_tail=0",
        "required but not written as an explicit functional",
        "sets the value side of the boundary problem",
    ),
    Piece(
        "momentum condition q/2",
        "available only through banked P_phi0 in the active lane",
        "sets the first variation at phi0",
    ),
    Piece(
        "H1 projection eta=q/6",
        "derived after P_phi0 from round-S2 second moment",
        "projects scalar first variation into H1",
    ),
    Piece(
        "typed node variables",
        "candidate variables identified for M1, M2, and E1",
        "provide coordinates for a possible Hessian",
    ),
    Piece(
        "boundary functional S_phi0[nodes]",
        "not derived",
        "required before any Hessian exists",
    ),
    Piece(
        "second variation / Hessian",
        "not constructible yet",
        "would define C_M1, C_M2, C_E1 or coupled spectra",
    ),
]


def main() -> None:
    print("boundary Hessian constructibility audit")
    print("=" * 41)
    for piece in PIECES:
        print(piece.name)
        print(f"  current status: {piece.current_status}")
        print(f"  Hessian role:   {piece.hessian_role}")
        print()

    print("Constructibility verdict:")
    print("  The active lane has boundary conditions and typed variables.")
    print("  It does not yet have S_phi0[nodes].")
    print("  Therefore the coefficient Hessian cannot be claimed or evaluated.")


if __name__ == "__main__":
    main()

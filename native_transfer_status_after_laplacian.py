from dataclasses import dataclass


@dataclass(frozen=True)
class Piece:
    name: str
    previous_status: str
    updated_status: str


PIECES = [
    Piece(
        name="I_3 channel identity",
        previous_status="not found in scalar edge variables",
        updated_status="found in round S2 ell=1 Laplacian eigenspace",
    ),
    Piece(
        name="eta scalar",
        previous_status="resolved by P_phi0 if banked",
        updated_status="unchanged",
    ),
    Piece(
        name="eta/2 side action",
        previous_status="candidate P_transfer condition",
        updated_status="still needs boundary-gluing/action derivation",
    ),
    Piece(
        name="exponential trace",
        previous_status="exact conditional identity",
        updated_status="unchanged",
    ),
    Piece(
        name="node independence",
        previous_status="open",
        updated_status="unchanged; not supplied by Laplacian degeneracy",
    ),
]


def main() -> None:
    print("transfer status after Laplacian audit")
    print("=" * 40)
    for piece in PIECES:
        print(piece.name)
        print(f"  previous status: {piece.previous_status}")
        print(f"  updated status:  {piece.updated_status}")
        print()

    print("Updated verdict:")
    print("  P_transfer is less unsupported than before: the I_3 part is native")
    print("  to the angular metric. The remaining non-derived piece is the")
    print("  boundary action coupling eta/2 to the normalized ell=1 kernel, plus")
    print("  independent composition over nodes.")


if __name__ == "__main__":
    main()

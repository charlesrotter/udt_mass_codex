from dataclasses import dataclass


@dataclass(frozen=True)
class Block:
    name: str
    metric_supplied: str
    allowed_reductions: str
    current_best_status: str


BLOCKS = [
    Block(
        "scalar q block",
        "A(1/3)=1/12, A'(1/3)=1, A''(1/3)=27/2",
        "fixed by boundary condition, constrained to q=1/3, or integrated with a derived measure",
        "not stationary by bare C1; likely fixed/constrained, not traced",
    ),
    Block(
        "H1 identity block",
        "I3 with side action eta/2, or warped D1 I3 if on-shell collar is used",
        "internal trace, fixed label, normalized average, determinant, or Gaussian integration",
        "gamma requires internal trace",
    ),
    Block(
        "E1 relative plane",
        "k I2 if it is the common-amplitude quotient of H1",
        "two independent side traces, side matching, or same-representation Schur coupling",
        "depth=7 requires two independent side planes",
    ),
    Block(
        "M1 compact residual scalar",
        "one side-shape scalar per side if CP1/Hopf quotient supplies s=1",
        "two independent side traces, side matching, or scalar 2x2 Schur reduction",
        "depth=5 requires two independent side scalars",
    ),
    Block(
        "higher ell blocks",
        "D_ell I_(2ell+1) from warped DtN for ell>=2",
        "suppressed, fixed, integrated, or included as correction voices",
        "not currently part of active ladder unless a selection rule admits them",
    ),
]


def main() -> None:
    print("current boundary-reduction map")
    print("=" * 32)
    for block in BLOCKS:
        print(block.name)
        print(f"  metric supplied:      {block.metric_supplied}")
        print(f"  allowed reductions:   {block.allowed_reductions}")
        print(f"  current best status:  {block.current_best_status}")
        print()

    print("Map verdict:")
    print("  Boundary reduction is now a finite decision table over metric-supplied")
    print("  blocks. The next hidden metric piece to seek is not another number;")
    print("  it is the boundary condition/measure that chooses the reduction column.")


if __name__ == "__main__":
    main()

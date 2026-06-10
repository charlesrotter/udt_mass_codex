from dataclasses import dataclass


@dataclass(frozen=True)
class Block:
    block: str
    metric_origin: str
    first_variation: str
    second_variation: str
    consequence: str


BLOCKS = [
    Block(
        "radial q / scalar branch",
        "self-similar C1 action A(q)=q^2/[4(1-2q)]",
        "nonzero at q=1/3: A'(1/3)=1",
        "A''(1/3)=27/2; H1-projected scalar stiffness 9/2",
        "q selection needs a constraint/boundary condition, not bare stationarity",
    ),
    Block(
        "ell=0 angular boundary mode",
        "constant S2 mode",
        "couples to scalar/radial normalization",
        "DtN eigenvalue D_0=0 for constant finite mode",
        "not a particle transfer triplet",
    ),
    Block(
        "ell=1 / H1 triplet",
        "round S2 degeneracy plus warped collar DtN",
        "orthogonal to scalar radial first variation",
        "D_1 I3 for warped on-shell action, or I3 for intrinsic boundary action",
        "metric supplies the threefold identity block",
    ),
    Block(
        "ell>=2 shape blocks",
        "higher S2 harmonics / relative-shape variables",
        "orthogonal to ell=0 and ell=1 by S2 harmonic orthogonality",
        "D_ell I_(2ell+1) inside each irreducible block",
        "candidate home for typed shape Hessian pieces",
    ),
]


def main() -> None:
    print("metric variation block diagonal pattern")
    print("=" * 39)
    for block in BLOCKS:
        print(block.block)
        print(f"  metric origin:    {block.metric_origin}")
        print(f"  first variation:  {block.first_variation}")
        print(f"  second variation: {block.second_variation}")
        print(f"  consequence:      {block.consequence}")
        print()

    print("Block verdict:")
    print("  The metric action naturally separates scalar/radial, H1 triplet,")
    print("  and higher-shape Hessian blocks. Coefficients should be searched")
    print("  as exact block eigenvalues or Schur complements, not inserted.")


if __name__ == "__main__":
    main()

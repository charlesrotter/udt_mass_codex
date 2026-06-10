from dataclasses import dataclass


@dataclass(frozen=True)
class Block:
    name: str
    variables: str
    symmetry_constraint: str
    unknown: str


BLOCKS = [
    Block(
        "shared H1 frame block",
        "three H1/S2 frame components with unit/projective constraints",
        "round-S2 symmetry restricts identity-like pieces to multiples of I3",
        "whether this block is traced once, three times, or coupled to shapes",
    ),
    Block(
        "M1 compact/radial block",
        "primitive compact-bundle data plus one residual shape scalar per side if Pbundle0 is banked",
        "Hopf/CP1 bridge maps orientation into the shared H1 frame",
        "compact occupation and residual scalar kernel",
    ),
    Block(
        "M2 compact triplet block",
        "nonprimitive compact n=2 triplet data",
        "eligible as d=3 representation but nonprimitive in compact flux",
        "derived suppression, diagnostic coefficient, or exclusion",
    ),
    Block(
        "E1 relative-shape block",
        "two-dimensional relative plane per side after removing common amplitude",
        "isotropy restricts bare relative metric to multiples of I2",
        "boundary-action weight and cross-coupling to shared H1 frame",
    ),
    Block(
        "cross-coupling blocks",
        "couplings among shared frame, compact data, and relative shapes",
        "symmetry may force some blocks to vanish, but this must be derived",
        "whether the kernel factorizes or has a coupled spectrum",
    ),
]


def main() -> None:
    print("Tier D block-kernel skeleton")
    print("=" * 30)
    for block in BLOCKS:
        print(block.name)
        print(f"  variables:           {block.variables}")
        print(f"  symmetry constraint: {block.symmetry_constraint}")
        print(f"  unknown:             {block.unknown}")
        print()

    print("Skeleton verdict:")
    print("  Symmetry constrains the possible kernel blocks, but it does not set")
    print("  their weights or prove factorization. A block-diagonal kernel would")
    print("  be a result, not an assumption.")


if __name__ == "__main__":
    main()

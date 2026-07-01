from dataclasses import dataclass


@dataclass(frozen=True)
class Sector:
    ell: int
    dimension: int
    laplacian_eigenvalue: int
    metric_role: str
    transfer_relevance: str


SECTORS = [
    Sector(
        ell=0,
        dimension=1,
        laplacian_eigenvalue=0,
        metric_role="constant scalar on S2",
        transfer_relevance="no angular identity variation; no nonzero angular Laplacian kernel",
    ),
    Sector(
        ell=1,
        dimension=3,
        laplacian_eigenvalue=2,
        metric_role="lowest nonconstant angular sector; coordinate-vector/H1 arena",
        transfer_relevance="first native angular identity kernel with I3 after normalization",
    ),
    Sector(
        ell=2,
        dimension=5,
        laplacian_eigenvalue=6,
        metric_role="quadrupolar/traceless-shape sector",
        transfer_relevance="higher angular shape response, not minimal edge identity",
    ),
]


def main() -> None:
    print("lowest nontrivial angular sector audit")
    print("=" * 43)
    for sector in SECTORS:
        print(f"ell={sector.ell}")
        print(f"  dimension:             {sector.dimension}")
        print(f"  -R^2 Delta eigenvalue: {sector.laplacian_eigenvalue}")
        print(f"  metric role:           {sector.metric_role}")
        print(f"  transfer relevance:    {sector.transfer_relevance}")
        print()

    print("Angular-sector verdict:")
    print("  ell=1 is selected as the lowest nonconstant angular identity sector")
    print("  of the round S2 metric. This is not a Standard Model import.")
    print("  It explains why the first transfer-kernel candidate should use")
    print("  the normalized ell=1 Laplacian if any angular kernel is used.")


if __name__ == "__main__":
    main()

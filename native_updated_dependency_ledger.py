"""Updated dependency ledger after angular-frame transport audit."""

from __future__ import annotations


ROWS = [
    (
        "Pframe-ordinary",
        "ordinary S2 angular frame transports identically across radius",
        "derived from g_ang=r^2 dOmega^2 after unit-sphere rescaling",
        "applies to E1; not automatically to compact-flux sectors",
    ),
    (
        "Pbundle-M1",
        "primitive compact-flux anchor has fixed bundle transport across cell",
        "needed for M1 identity frame/anchor branch",
        "still postulated unless compact flux sector is derived",
    ),
    (
        "Ptransfer",
        "epsilon transfer is diagonal with trace N",
        "ordinary basis overlap supports trace N for E1",
        "needs relation between epsilon labels and transported orthonormal basis",
    ),
    (
        "Punit",
        "unit transferred label has action eta/2",
        "quadratic unit-transfer route",
        "unit norm and boundary action not yet derived",
    ),
    (
        "Pdepth",
        "n_close(d)=N+2(d-1)",
        "finite interval gives independent angular endpoint variations",
        "constraint-to-transfer mapping not yet derived",
    ),
]


def main() -> None:
    print("Updated dependency ledger")
    print()
    for key, claim, support, gap in ROWS:
        print(key)
        print(f"  claim: {claim}")
        print(f"  support: {support}")
        print(f"  gap: {gap}")
        print()
    print("verdict:")
    print("  Pframe is partially derived for the ordinary E1 branch")
    print("  the compact-flux M1 anchor still carries Pbundle/Pflux")


if __name__ == "__main__":
    main()

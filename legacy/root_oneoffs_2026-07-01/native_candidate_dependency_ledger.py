"""Dependency ledger for the current native mass-ladder candidate."""

from __future__ import annotations


ROWS = [
    (
        "Pepsilon",
        "eta=1/(2N^2), N=3",
        "native clue: unique epsilon sector and quadratic half-factor",
        "still a postulate until endpoint-source normalization is derived",
    ),
    (
        "Ptransfer-space",
        "N-dimensional diagonal transfer",
        "needed to get N rather than N^2 or 1",
        "must be derived from boundary matching/orientation closure",
    ),
    (
        "Pgamma",
        "gamma=N exp(-eta/2)",
        "conditional on quadratic unit transfer",
        "raw shell/core loads do not derive it",
    ),
    (
        "Pdepth",
        "n_close(d)=N+2(d-1)",
        "closure-count candidate",
        "must derive why each constraint maps to one gamma transfer",
    ),
    (
        "Pselect-M1",
        "primitive compact-flux doublet",
        "n=1 flux avoids superadditive flux cost",
        "compact flux itself remains optional/postulated",
    ),
    (
        "Pselect-E1",
        "ordinary ell=1 triplet",
        "self-similar endpoint p=1/3 selects lambda=2",
        "p=1/3 closure principle still not variational theorem",
    ),
    (
        "Pexclude-scalar",
        "d=1 is not elementary matter",
        "no non-scalar boundary data; scalar sector gapless",
        "must be formalized as admissibility rule",
    ),
    (
        "F",
        "electron mass anchor",
        "accepted dimensionful input",
        "not derived by UDT geometry",
    ),
]


def main() -> None:
    print("Native candidate dependency ledger")
    print()
    for key, claim, support, gap in ROWS:
        print(key)
        print(f"  claim: {claim}")
        print(f"  support: {support}")
        print(f"  gap: {gap}")
        print()
    print("verdict:")
    print("  the candidate is compact, but not derived")
    print("  Pgamma/Ptransfer-space/Pdepth are the next proof targets")


if __name__ == "__main__":
    main()

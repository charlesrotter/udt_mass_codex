from dataclasses import dataclass


@dataclass(frozen=True)
class CorrectionSource:
    name: str
    affects_m1: str
    affects_e1: str
    common_or_branch: str
    sign_flexibility: str
    status: str
    next_test: str


SOURCES = [
    CorrectionSource(
        name="collar log-slope q_phi0",
        affects_m1="yes, through gamma(q)^5",
        affects_e1="yes, through gamma(q)^7",
        common_or_branch="common if q is universal; branch-specific if boundary layers differ",
        sign_flexibility="common q cannot fix opposite residual signs",
        status="skeleton exposed",
        next_test="derive q-flow for M1 and E1 boundary data separately",
    ),
    CorrectionSource(
        name="S2 boundary distribution",
        affects_m1="yes, through Hopf/projective image distribution",
        affects_e1="yes, through ordinary H1 distribution",
        common_or_branch="branch-specific if induced distributions differ",
        sign_flexibility="can move branches differently if measures are not uniform",
        status="open nonlinear measure",
        next_test="derive induced n_a distribution for each branch before using <n_a n_b>=delta/3",
    ),
    CorrectionSource(
        name="CP1/Fubini-Study measure",
        affects_m1="directly",
        affects_e1="no direct compact CP1 role",
        common_or_branch="M1-specific",
        sign_flexibility="can damp or enhance M1 coefficient/closure weight",
        status="exact geometry known; action coupling open",
        next_test="compute Hopf bilinear measure and compare to round S2 normalization",
    ),
    CorrectionSource(
        name="ordinary H1 shape measure",
        affects_m1="only through shared frame after Hopf merge",
        affects_e1="directly",
        common_or_branch="E1-heavy",
        sign_flexibility="can alter E1 coefficient or effective shape-node weight",
        status="open boundary measure",
        next_test="derive E1 relative-shape measure after removing common amplitude mode",
    ),
    CorrectionSource(
        name="transfer gluing determinant",
        affects_m1="yes, if every closure kernel glues",
        affects_e1="yes, if every closure kernel glues",
        common_or_branch="common unless determinant depends on branch dimension/node type",
        sign_flexibility="common determinant cannot fix opposite residual signs",
        status="open composition measure",
        next_test="derive kernel composition including normalization determinant by node type",
    ),
    CorrectionSource(
        name="node granularity/correlation",
        affects_m1="yes, changes effective node count below 5",
        affects_e1="yes, changes effective node count below 7",
        common_or_branch="branch-specific if graph correlations differ",
        sign_flexibility="usually lowers entropy; cannot raise tau-like mass unless coefficients change",
        status="major open graph condition",
        next_test="write boundary variation in node variables and identify equality edges",
    ),
    CorrectionSource(
        name="branch coefficient normalization",
        affects_m1="sets anchor branch and M1 excited branch coefficient",
        affects_e1="sets E1/M1 coefficient ratio",
        common_or_branch="branch-specific",
        sign_flexibility="can naturally move M1 and E1 in opposite directions",
        status="not yet derived in typed graph",
        next_test="recompute coefficients from nonlinear typed boundary action",
    ),
]


def main() -> None:
    print("Distributed approximation-correction map")
    print("=" * 41)
    print("Approximation corrections can affect multiple orchestra instruments.")
    print("Classify them before treating residuals as physics.")
    print()
    for source in SOURCES:
        print(source.name)
        print(f"  affects M1:          {source.affects_m1}")
        print(f"  affects E1:          {source.affects_e1}")
        print(f"  common/branch:       {source.common_or_branch}")
        print(f"  sign flexibility:    {source.sign_flexibility}")
        print(f"  status:              {source.status}")
        print(f"  next test:           {source.next_test}")
        print()

    print("Map verdict:")
    print("  - Common corrections are useful for validating the skeleton but cannot")
    print("    explain opposite-sign residuals by themselves.")
    print("  - Branch-specific measures and coefficient normalization are the first")
    print("    places to look after the nonlinear boundary graph is written.")
    print("  - Do not add residual terms until these native correction channels are")
    print("    derived or ruled out.")


if __name__ == "__main__":
    main()

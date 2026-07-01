from dataclasses import dataclass


@dataclass(frozen=True)
class Entry:
    name: str
    status: str
    metric_content: str
    current_use: str
    risk: str
    next_test: str


ENTRIES = [
    Entry(
        name="negative phi sheet",
        status="metric-forced",
        metric_content="phi<0 gives f=e^{-2phi}>1 and the inside-out matter-side endpoint problem.",
        current_use="Defines the finite-action endpoint/cell arena.",
        risk="Deep phi->-infty is a singular background, not automatically a particle.",
        next_test="Keep separating endpoint geometry from normalizable cell observables.",
    ),
    Entry(
        name="round S2 angular block",
        status="metric-forced",
        metric_content="g_theta_theta=r^2 and g_phi_phi=r^2 sin^2 theta are phi-blind.",
        current_use="Provides ordinary angular frames, orthogonality, and ell selection.",
        risk="May hide additional boundary/measure effects if only representation labels are tracked.",
        next_test="Derive boundary variation terms using the full angular measure and extrinsic curvature.",
    ),
    Entry(
        name="finite-action endpoint bound",
        status="metric-forced under C1 action",
        metric_content="For f~r^-p, the radial action is finite only for p<1/2.",
        current_use="Excludes singular vacuum-like endpoints as elementary finite-action cells.",
        risk="Depends on using the C1 phi action as the active mass-side action.",
        next_test="Audit boundary terms and possible renormalized finite parts at p=1/2 and p=1.",
    ),
    Entry(
        name="angular source softening",
        status="conditional metric consequence",
        metric_content="An angular source s/r^2 yields p(1-p)/2=s.",
        current_use="Turns angular labels into endpoint exponents.",
        risk="The source normalization eta*lambda is not metric-derived yet.",
        next_test="Derive s from the metric variation rather than assigning eta lambda.",
    ),
    Entry(
        name="endpoint self-similarity",
        status="metric-pattern constraint",
        metric_content="Matching profile and action-remainder scaling gives 1-2p=p, hence p=1/3.",
        current_use="Selects an N=3-compatible endpoint resonance.",
        risk="A resonance condition is weaker than a full dynamical selection law.",
        next_test="Check whether the boundary Euler term independently enforces p=1/3.",
    ),
    Entry(
        name="abelian Coulomb sector",
        status="metric-forced",
        metric_content="sqrt(-g) g^rr g^tt cancels phi, giving flat static Coulomb form.",
        current_use="A real phi-blind metric interaction available to the ensemble.",
        risk="Not yet coupled into the negative-phi endpoint ladder.",
        next_test="Test whether Coulomb boundary energy shifts E1 but leaves M1 anchor mostly unchanged.",
    ),
    Entry(
        name="compact U(1) line bundle",
        status="minimal postulate, then topological consequence",
        metric_content="If admitted on the collar S2 x I, H2 gives integer flux sectors.",
        current_use="Primitive |n|=1 selects the M1 anchor branch.",
        risk="The occupation of a nontrivial compact bundle is not forced by the metric alone.",
        next_test="Search for a metric boundary obstruction that requires nonzero compact flux.",
    ),
    Entry(
        name="epsilon sector N=3",
        status="working postulate",
        metric_content="The oriented S2 frame supports a 3-label transported basis, but eta=1/18 is extra.",
        current_use="Sets gamma=N exp(-eta/2) and the closure entropy base.",
        risk="Can become a hidden fit if eta is only chosen to make the ladder work.",
        next_test="Derive eta from a boundary norm, frame-volume action, or curvature measure.",
    ),
    Entry(
        name="boundary closure entropy",
        status="working postulate plus native pressure",
        metric_content="Independent epsilon-mediated constraints would contribute log N - eta/2 each.",
        current_use="Best current hierarchy source.",
        risk="Overcounts if closure labels are correlated or not epsilon-mediated.",
        next_test="Derive the constraint graph from boundary variation instead of assigning depths.",
    ),
    Entry(
        name="angular determinant/RG finite part",
        status="open hidden-metric candidate",
        metric_content="The angular Laplacian and measure may leave branch-dependent finite determinants.",
        current_use="Possible E1-positive correction instrument.",
        risk="High scheme-dependence and high residual-fitting risk.",
        next_test="Only admit corrections invariant under a stated subtraction rule.",
    ),
]


def main() -> None:
    buckets: dict[str, list[Entry]] = {}
    for entry in ENTRIES:
        buckets.setdefault(entry.status, []).append(entry)

    print("Metric discovery ledger")
    print("=" * 24)
    for status, entries in buckets.items():
        print(f"\n{status}:")
        for entry in entries:
            print(f"  - {entry.name}")
            print(f"    metric: {entry.metric_content}")
            print(f"    use:    {entry.current_use}")
            print(f"    risk:   {entry.risk}")
            print(f"    test:   {entry.next_test}")

    postulate_like = [
        entry.name
        for entry in ENTRIES
        if "postulate" in entry.status or entry.status.startswith("working")
    ]
    print("\nPostulate pressure points:")
    for name in postulate_like:
        print(f"  - {name}")

    print("\nDiscovery priority:")
    print("  1. Boundary variation: derive source normalization and constraint graph.")
    print("  2. Coulomb/phi-blind dynamics: test branch-specific shifts without a color-force import.")
    print("  3. Determinants: use only subtraction-invariant finite differences.")
    print("  4. Compact flux: search for a metric reason the primitive bundle must be occupied.")


if __name__ == "__main__":
    main()

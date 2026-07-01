from dataclasses import dataclass


@dataclass(frozen=True)
class Candidate:
    name: str
    sector: str
    metric_native_content: str
    possible_mechanism_role: str
    prior_status: str
    why_revisit_now: str
    next_probe: str


CANDIDATES = [
    Candidate(
        name="phi0 boundary layer",
        sector="phi/interface",
        metric_native_content="finite cell matching, extrinsic curvature jump, tail cancellation",
        possible_mechanism_role="sets q_phi0, cancels exterior negative-mass tail, creates physical closure nodes",
        prior_status="postulated/needed for finite cell",
        why_revisit_now="q-flow and typed graph show collar physics controls eta and residual-sensitive source running",
        next_probe="derive boundary layer source required for a_tail=0 and q_phi0=1/3",
    ),
    Candidate(
        name="angular-source running",
        sector="angular/phi coupling",
        metric_native_content="angular gradients supply 1/r^2 source shape; q-flow obeys dq/dt=q^2-q+2s(t)",
        possible_mechanism_role="branch-specific collar source shifts and nonlinear endpoint softening",
        prior_status="constant-source softening studied; running source not derived",
        why_revisit_now="opposite residual signs require branch-sensitive source or coefficient effects",
        next_probe="derive s(t) for M1 Hopf/projective and E1 ordinary H1 boundary data",
    ),
    Candidate(
        name="tail cancellation/global closure",
        sector="phi/global",
        metric_native_content="localized positive angular source creates exterior negative-mass tail unless canceled",
        possible_mechanism_role="global finite-cell quantization or closure condition",
        prior_status="identified as missing finite-cell condition",
        why_revisit_now="typed graph gives candidate closure nodes that could be the cancellation conditions",
        next_probe="express a_tail as a boundary functional of typed nodes",
    ),
    Candidate(
        name="abelian Coulomb boundary energy",
        sector="phi-blind force",
        metric_native_content="Maxwell cancellation gives exact Coulomb form in UDT metric",
        possible_mechanism_role="branch-selective interface energy or compact occupation pressure",
        prior_status="real force, but radial flux singular and not a ladder alone",
        why_revisit_now="could participate as one orchestra instrument without importing SM radiative mechanisms",
        next_probe="compute finite-cell Coulomb boundary energy under primitive compact/topological closure",
    ),
    Candidate(
        name="compact bundle occupation obstruction",
        sector="topology/angular",
        metric_native_content="S2 x I supports integer line-bundle sectors; |n|=1 gives CP1=S2 bridge",
        possible_mechanism_role="forces or favors M1 primitive branch",
        prior_status="Pbundle0 remains postulate",
        why_revisit_now="Hopf bridge makes primitive sector geometrically special at the interface",
        next_probe="search for boundary regularity/phase patching obstruction that excludes trivial-only closure",
    ),
    Candidate(
        name="angular determinant with fixed normalization",
        sector="angular measure",
        metric_native_content="round S2 Laplacian and finite-dimensional H1/shape kernels",
        possible_mechanism_role="finite normalized coefficient correction after graph is fixed",
        prior_status="high overfit risk; unnormalized determinants dangerous",
        why_revisit_now="bare measures are isotropic, so only normalized action determinants remain plausible",
        next_probe="derive normalized determinant ratios from typed kernels, target-blind",
    ),
    Candidate(
        name="phi stiffness / matter-side C",
        sector="phi dynamics",
        metric_native_content="C1 action stiffness not fixed by macro gravity normalization",
        possible_mechanism_role="sets nonlinear back-reaction strength or finite-cell coefficient normalization",
        prior_status="magnitude open in UDT_REBUILD",
        why_revisit_now="coefficients may be where residuals live",
        next_probe="track whether C cancels in ratios or enters branch coefficient normalization",
    ),
]


def main() -> None:
    print("Unidentified metric-spawned mechanism second look")
    print("=" * 52)
    print("Do not import new forces. Revisit native metric structures that may")
    print("act as mechanisms only in the coupled orchestra.")
    print()
    for candidate in CANDIDATES:
        print(candidate.name)
        print(f"  sector:          {candidate.sector}")
        print(f"  native content:  {candidate.metric_native_content}")
        print(f"  possible role:   {candidate.possible_mechanism_role}")
        print(f"  prior status:    {candidate.prior_status}")
        print(f"  why revisit:     {candidate.why_revisit_now}")
        print(f"  next probe:      {candidate.next_probe}")
        print()

    print("Second-look verdict:")
    print("  The best hidden-mechanism candidates are not new SM-like forces.")
    print("  They are boundary/interface/global-closure effects generated by the")
    print("  phi-angular-topology orchestra.")
    print("  Priority: phi0 boundary layer, angular-source running, and global tail")
    print("  cancellation before residual fitting.")


if __name__ == "__main__":
    main()

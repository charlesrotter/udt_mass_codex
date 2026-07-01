from dataclasses import dataclass


@dataclass(frozen=True)
class Mode:
    name: str
    metric_reading: str
    what_it_would_explain: str
    proof_test: str
    risk: str


MODES = [
    Mode(
        name="binding-to-both-realms",
        metric_reading="an angular component has support on both phi<0 matter data and phi>0 scalar/background data",
        what_it_would_explain="why negative-phi matter remains macro-accessible instead of becoming a disconnected sheet",
        proof_test="derive a two-sided boundary action whose angular variable is shared across the phi=0 bridge",
        risk="can sound like an imported force unless kept as boundary/gluing support",
    ),
    Mode(
        name="resonance",
        metric_reading="the same scale-invariant angular eigenvalue is admissible on both sides and at the finite-action endpoint",
        what_it_would_explain="why H1/ell=1, p=1/3, and eta=1/18 keep appearing together",
        proof_test="show the angular eigenvalue, endpoint exponent, and first-jet slope are one admissible Cauchy graph",
        risk="resonance language can hide the still-open graph uniqueness proof",
    ),
    Mode(
        name="interference / cancellation",
        metric_reading="two-sided bridge data cancel exterior radial tail while preserving the interior angular first-jet imprint",
        what_it_would_explain="how matter can be present in the macro realm without leaking a negative-phi radial tail",
        proof_test="derive a gluing condition where radial tail terms cancel and H1-projected first-jet data survive",
        risk="highest fitting risk unless the cancellation follows from a symplectic/gluing identity",
    ),
]


def main() -> None:
    print("angular bridge coupling modes")
    print("=" * 31)
    for mode in MODES:
        print(mode.name)
        print(f"  metric reading:          {mode.metric_reading}")
        print(f"  would explain:           {mode.what_it_would_explain}")
        print(f"  proof test:              {mode.proof_test}")
        print(f"  risk:                    {mode.risk}")
        print()

    print("Exact common substrate:")
    print("  g_AB = r^2 omega_AB is shared across phi signs")
    print("  -r^2 Delta_S2 is scale-invariant")
    print("  phi=0 is the internalized asymptotic normalization surface")
    print("  first-jet data q/2 can be projected through H1")
    print()
    print("Ponder verdict:")
    print("  The likely missing object is an angular bridge component that is")
    print("  shared by both phi realms. Its observable job may be a composition")
    print("  of binding, resonance, and interference: shared support, endpoint")
    print("  admissibility, and radial-tail cancellation.")
    print()
    print("Next test:")
    print("  Search for a two-sided phi=0 gluing identity where the radial")
    print("  tail cancels but the scale-invariant H1 first-jet imprint survives.")


if __name__ == "__main__":
    main()

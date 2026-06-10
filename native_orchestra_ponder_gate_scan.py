from dataclasses import dataclass


@dataclass(frozen=True)
class Candidate:
    name: str
    native_object: str
    gates_addressed: str
    promise: str
    risk: str
    next_probe: str


CANDIDATES = [
    Candidate(
        "phi0 boundary variation",
        "C1 boundary momentum, induced S2 metric, extrinsic-curvature jump",
        "delta_h=0; interface-local transfer; possibly boundary-state count",
        "highest: all current gates touch this object",
        "can become an imposed boundary action if not derived from variation",
        "write the local phi0 variation in variables (F, q, n_a, H1 data) and identify value/action terms",
    ),
    Candidate(
        "collar source-running law",
        "q-flow dq/dt=q^2-q+2s(t) and H1 angular source",
        "delta_h=0",
        "high: directly decides whether P_phi0 is derived",
        "approximating s(t) would reintroduce AI linearization drift",
        "derive whether H1 shell source is constant along the collar or distributional at phi0",
    ),
    Candidate(
        "Calderon/interface Cauchy data",
        "boundary map relating field value and normal derivative at phi0",
        "interface-local transfer versus bulk-DtN branch",
        "high: exact branch discriminator",
        "ordinary PDE probe may not be the physical mass-transfer action",
        "construct the UDT phi0 Cauchy-data space and ask whether it is local or collar-memory bearing",
    ),
    Candidate(
        "H1 boundary-state measure",
        "round S2 H1 triplet, isotropic shell stress, transported angular frame",
        "boundary-state counting rather than averaging",
        "medium-high: decides trace versus average",
        "easy to confuse degeneracy count with normalized probability",
        "classify the boundary object as state-count, transition amplitude, average, or determinant",
    ),
    Candidate(
        "compact/Hopf bridge",
        "primitive U1 line bundle and CP1 -> S2/H1 map",
        "later branch/node independence; not primary current gates",
        "medium: important for M1 participation in the same H1 frame",
        "can overcount if Hopf data merely reuses existing H1 variables",
        "only revisit after phi0/H1 transfer kernel is fixed",
    ),
    Candidate(
        "Coulomb phi-blind sector",
        "Maxwell cancellation in UDT metric",
        "later residual/branch shifts; not primary current gates",
        "medium-low for current theorem, higher for corrections",
        "tempting to import force analogs",
        "defer until transfer kernel and q/eta chain are settled",
    ),
    Candidate(
        "angular determinant/RG finite part",
        "regulated S2/H1 operator determinants",
        "possibly later coefficient corrections, not current gates",
        "low now",
        "high scheme/fitting risk",
        "defer unless a fixed subtraction rule is derived from the boundary action",
    ),
]


def main() -> None:
    print("orchestra ponder gate scan")
    print("=" * 28)
    for item in CANDIDATES:
        print(item.name)
        print(f"  native object:   {item.native_object}")
        print(f"  gates addressed: {item.gates_addressed}")
        print(f"  promise:         {item.promise}")
        print(f"  risk:            {item.risk}")
        print(f"  next probe:      {item.next_probe}")
        print()

    print("Ponder verdict:")
    print("  Yes: an orchestra scan is appropriate now.")
    print("  The scan says to focus on phi0 boundary variation and collar source")
    print("  running before adding later instruments such as compact flux, Coulomb,")
    print("  or determinant corrections.")


if __name__ == "__main__":
    main()

from dataclasses import dataclass


@dataclass(frozen=True)
class KernelCandidate:
    name: str
    form: str
    native_parts: str
    supplies_bridge: str
    verdict: str


CANDIDATES = [
    KernelCandidate(
        name="C1 scalar boundary kernel",
        form="B_phi0(f, Pi_f) or fixed -Pi_f/R",
        native_parts="C1 boundary momentum and P_phi0",
        supplies_bridge="no angular L1 operator",
        verdict="supplies eta, not transfer kernel",
    ),
    KernelCandidate(
        name="angular Laplacian kernel",
        form="L1=(-R^2 Delta_S2)/2 on ell=1",
        native_parts="round S2 metric",
        supplies_bridge="supplies I3, no eta coefficient",
        verdict="supplies channel identity, not edge action",
    ),
    KernelCandidate(
        name="separable product kernel",
        form="A_side=(eta/2) L1",
        native_parts="P_phi0 edge scalar times normalized ell=1 Laplacian",
        supplies_bridge="yes, if side-action coupling is native",
        verdict="best current bridge candidate; coupling still not derived",
    ),
    KernelCandidate(
        name="rank-one direction kernel",
        form="A=(eta/2) n n^T",
        native_parts="H1/S2 unit direction",
        supplies_bridge="no; eigenvalues are eta/2,0,0",
        verdict="wrong trace for P_transfer",
    ),
    KernelCandidate(
        name="projected normalized kernel",
        form="A=(eta/2)(I3/3)",
        native_parts="H1/S2 second moment",
        supplies_bridge="no; gives 3 exp(-eta/6)",
        verdict="eta projection, not transfer",
    ),
    KernelCandidate(
        name="ell=0 scalar kernel",
        form="L0=0 or constant mode",
        native_parts="round S2 scalar sector",
        supplies_bridge="no nonzero angular identity action",
        verdict="not mass-edge angular identity",
    ),
]


def main() -> None:
    print("phi0-to-ell=1 boundary kernel candidates")
    print("=" * 49)
    for candidate in CANDIDATES:
        print(candidate.name)
        print(f"  form:             {candidate.form}")
        print(f"  native parts:     {candidate.native_parts}")
        print(f"  supplies bridge:  {candidate.supplies_bridge}")
        print(f"  verdict:          {candidate.verdict}")
        print()

    print("Candidate verdict:")
    print("  The only candidate with the right bridge is the separable product")
    print("  A_side=(eta/2)L1. It is native in parts, but the coupling that forms")
    print("  the product is still the missing object.")


if __name__ == "__main__":
    main()

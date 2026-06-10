from dataclasses import dataclass


@dataclass(frozen=True)
class CauchyDatum:
    datum: str
    metric_object: str
    role: str
    status: str


DATA = [
    CauchyDatum(
        "Dirichlet value",
        "f(phi0)=1",
        "sets the phi0 interface surface",
        "exact by definition of phi0",
    ),
    CauchyDatum(
        "Neumann momentum",
        "-Pi_f/R=q/2",
        "sets the C1 boundary momentum jump",
        "exact once q is selected/banked",
    ),
    CauchyDatum(
        "H1 boundary data",
        "ell=1 projector on the round S2 boundary",
        "finite angular interface label space",
        "exact after H1 selection",
    ),
    CauchyDatum(
        "two-sided extension",
        "negative-phi side plus positive/scalar side sharing phi0",
        "turns phi0 data into internal Cauchy data",
        "supported by bridge geometry; projector not fully constructed",
    ),
]


def main() -> None:
    print("phi0 Calderon plain-sight audit")
    print("=" * 36)
    for item in DATA:
        print(item.datum)
        print(f"  metric object: {item.metric_object}")
        print(f"  role:          {item.role}")
        print(f"  status:        {item.status}")
        print()

    print("Calderon reading:")
    print("  The missing boundary-reduction rule may be the phi0 Cauchy-data")
    print("  projector: keep only boundary data that extend to both sides of")
    print("  the interface, then contract internal H1 labels with the induced")
    print("  S2 measure.")
    print()
    print("Plain-sight verdict:")
    print("  The metric already exposes the ingredients of the reduction rule:")
    print("  phi0 value, C1 momentum, H1 projector, and two-sided interface data.")
    print("  What remains is constructing the exact projector, not inventing a force.")


if __name__ == "__main__":
    main()

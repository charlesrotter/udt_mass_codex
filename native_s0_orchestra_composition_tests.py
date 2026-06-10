from dataclasses import dataclass


@dataclass(frozen=True)
class Composition:
    name: str
    form: str
    status: str
    rejection_or_next_test: str


COMPOSITIONS = [
    Composition(
        "interface-local scalar-times-L1",
        "S0_side = (eta/2)<a,L1 a>",
        "allowed conditional target",
        "derive side split and scalar-to-L1 coupling",
    ),
    Composition(
        "two-sided full scalar-times-L1",
        "S0_full = eta<a,L1 a>",
        "allowed conditional target",
        "derive symmetric gluing to get side action",
    ),
    Composition(
        "bulk DtN quadratic form",
        "S0 = (1/2)<a,K_warped a>",
        "allowed alternative branch",
        "use instead of interface-local S0, not in addition",
    ),
    Composition(
        "interface-local plus bulk DtN product",
        "S0 = eta L1 plus K_warped for same H1 variable",
        "reject by double counting",
        "only allowed if variables are distinct and boundary graph proves it",
    ),
    Composition(
        "bare measure volume coefficient",
        "C_i from CP1/S2 or relative-plane volume",
        "reject",
        "bare measures are isotropic and normalization-dependent",
    ),
    Composition(
        "block Hessian with free constants",
        "K = diag(alpha I3, beta I2, ...)",
        "not Tier D",
        "derive constants from S_phi0 or keep as P_coeff",
    ),
]


def main() -> None:
    print("S0 orchestra composition tests")
    print("=" * 32)
    for composition in COMPOSITIONS:
        print(composition.name)
        print(f"  form:      {composition.form}")
        print(f"  status:    {composition.status}")
        print(f"  next/test: {composition.rejection_or_next_test}")
        print()

    print("Composition verdict:")
    print("  The orchestra can explain how eta, L1, gluing, and DtN alternatives")
    print("  meet, but it also makes double counting easier. Each instrument must")
    print("  have one role in one branch unless a boundary graph proves otherwise.")


if __name__ == "__main__":
    main()

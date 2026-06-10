from dataclasses import dataclass


@dataclass(frozen=True)
class AngularFact:
    name: str
    exact_statement: str
    transfer_relevance: str
    caveat: str


FACTS = [
    AngularFact(
        name="round S2 Laplacian",
        exact_statement="Delta_S2 Y_lm = -l(l+1)Y_lm/R^2",
        transfer_relevance="on each fixed l eigenspace, the angular operator is scalar",
        caveat="requires choosing an angular action using this operator",
    ),
    AngularFact(
        name="ell=1 eigenspace",
        exact_statement="dim H_l=1 = 2l+1 = 3",
        transfer_relevance="gives an exact three-channel arena",
        caveat="channel degeneracy is kinematic unless coupled to edge action",
    ),
    AngularFact(
        name="ell=1 restricted operator",
        exact_statement="-R^2 Delta_S2 |_{l=1} = 2 I_3",
        transfer_relevance="supplies a native I_3 structure, unlike the normalized projector I_3/3",
        caveat="eigenvalue is 2, not eta/2; coefficient/coupling remains separate",
    ),
    AngularFact(
        name="edge quantum coupling",
        exact_statement="P_phi0 supplies scalar eta=1/18 if banked",
        transfer_relevance="could weight the l=1 identity kernel if a boundary action couples them",
        caveat="the coupling rule is not derived by the Laplacian alone",
    ),
]


def main() -> None:
    print("S2 ell=1 identity-kernel audit")
    print("=" * 37)
    for fact in FACTS:
        print(fact.name)
        print(f"  exact statement:      {fact.exact_statement}")
        print(f"  transfer relevance:   {fact.transfer_relevance}")
        print(f"  caveat:               {fact.caveat}")
        print()

    print("Kernel verdict:")
    print("  The round S2 ell=1 Laplacian supplies a native three-dimensional")
    print("  identity structure. This is a better candidate for the I_3 part of")
    print("  P_transfer than the normalized second-moment projector.")
    print("  It still does not derive the eta/2 coefficient or the exponential")
    print("  transfer rule by itself.")


if __name__ == "__main__":
    main()

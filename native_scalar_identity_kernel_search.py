from dataclasses import dataclass


@dataclass(frozen=True)
class Source:
    name: str
    native_object: str
    kernel_supplied: str
    verdict: str


SOURCES = [
    Source(
        name="C1 boundary momentum",
        native_object="Pi_f = -qR/2",
        kernel_supplied="scalar edge momentum, no H1 channel matrix",
        verdict="does not supply I_3 transfer kernel",
    ),
    Source(
        name="radial-angular curvature",
        native_object="K_rad/K_S2 = q/2",
        kernel_supplied="scalar curvature ratio, no H1 channel matrix",
        verdict="does not supply I_3 transfer kernel",
    ),
    Source(
        name="H1/S2 projection",
        native_object="<n_a n_b> = delta_ab/3",
        kernel_supplied="normalized identity I_3/3",
        verdict="supplies eta projection, not eta/2 I_3 action",
    ),
    Source(
        name="round S2 intrinsic metric",
        native_object="gamma_AB = R^2 omega_AB",
        kernel_supplied="2D tangent metric on S2",
        verdict="not a 3D H1 channel identity",
    ),
    Source(
        name="S2 shape operator",
        native_object="s^A_B = (1/R) delta^A_B",
        kernel_supplied="2D tangent identity on embedded S2",
        verdict="not a 3D H1 channel identity",
    ),
    Source(
        name="CP1/Hopf bridge",
        native_object="CP1 -> S2 via phase-invariant bilinears",
        kernel_supplied="maps compact data into existing H1/S2 orientation",
        verdict="does not add an independent I_3 transfer kernel",
    ),
    Source(
        name="E1 relative-shape plane",
        native_object="two-dimensional plane orthogonal to common amplitude",
        kernel_supplied="2D relative-shape identity if a shape action exists",
        verdict="not the universal 3D scalar H1 transfer kernel",
    ),
]


def main() -> None:
    print("scalar identity kernel search")
    print("=" * 31)
    for source in SOURCES:
        print(source.name)
        print(f"  native object:    {source.native_object}")
        print(f"  kernel supplied:  {source.kernel_supplied}")
        print(f"  verdict:          {source.verdict}")
        print()

    print("Search verdict:")
    print("  No current native edge variable supplies the required eta/2 I_3")
    print("  transfer action. The known metric pieces supply scalars, tangent")
    print("  identities, or the normalized H1/S2 projector I_3/3.")
    print("  Therefore P_transfer remains a separate postulate unless a new")
    print("  native edge kernel is uncovered.")


if __name__ == "__main__":
    main()

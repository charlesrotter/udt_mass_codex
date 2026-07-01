from dataclasses import dataclass


@dataclass(frozen=True)
class BlockForm:
    block: str
    symmetry_allowed_form: str
    free_data: str
    consequence: str


BLOCKS = [
    BlockForm(
        "shared H1 frame",
        "K_H1 = alpha I_3 on the ell=1 triplet",
        "alpha",
        "round-S2 symmetry gives identity form, not the weight alpha",
    ),
    BlockForm(
        "E1 relative shape per side",
        "K_E1 = beta I_2 on the two-dimensional relative plane",
        "beta, plus possible core-phi0 coupling beta_cross",
        "relative-plane isotropy gives I_2 form, not the coefficient",
    ),
    BlockForm(
        "M1 compact residual scalar",
        "K_M1 is a symmetric 2x2 scalar-side matrix for core/phi0 residuals",
        "three scalar entries before additional gluing constraints",
        "scalar symmetry does not reduce it to a unique number",
    ),
    BlockForm(
        "M2 compact triplet",
        "K_M2 = alpha_2 I_3 if the nonprimitive compact triplet remains active",
        "alpha_2",
        "same dimension as E1 does not imply same coefficient or status",
    ),
    BlockForm(
        "cross blocks",
        "zero only if representation, parity, bundle, or endpoint symmetries forbid them",
        "all allowed couplings not killed by exact symmetry",
        "factorization is a derived property, not a default",
    ),
]


def main() -> None:
    print("symmetry-allowed second-jet form")
    print("=" * 36)
    for block in BLOCKS:
        print(block.block)
        print(f"  symmetry-allowed form: {block.symmetry_allowed_form}")
        print(f"  free data:             {block.free_data}")
        print(f"  consequence:           {block.consequence}")
        print()

    print("Symmetry verdict:")
    print("  Symmetry narrows the Hessian to block forms and a finite set of")
    print("  constants/couplings. It does not compute those constants.")
    print("  Therefore symmetry alone cannot produce C_M1, C_M2, or C_E1.")


if __name__ == "__main__":
    main()

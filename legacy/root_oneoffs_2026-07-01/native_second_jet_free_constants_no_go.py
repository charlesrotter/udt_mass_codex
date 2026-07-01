from dataclasses import dataclass


@dataclass(frozen=True)
class FreeConstant:
    name: str
    what_it_controls: str
    why_it_cannot_be_chosen: str


CONSTANTS = [
    FreeConstant(
        "alpha",
        "shared H1 frame block weight",
        "choosing it fixes transfer/trace strength beyond eta if not derived",
    ),
    FreeConstant(
        "beta",
        "E1 relative-shape block weight",
        "choosing it can create the needed E1 coefficient pressure by hand",
    ),
    FreeConstant(
        "beta_cross",
        "core-phi0 E1 relative-shape coupling",
        "choosing it decides factorization versus coupled spectrum",
    ),
    FreeConstant(
        "M1 scalar-side matrix entries",
        "primitive compact/radial residual weight",
        "choosing them can tune the M1 coefficient pressure",
    ),
    FreeConstant(
        "alpha_2 or null rule",
        "M2 compact triplet activity or suppression",
        "choosing it silently decides the competing d=3 branch",
    ),
]


def main() -> None:
    print("second-jet free-constants no-go")
    print("=" * 34)
    for constant in CONSTANTS:
        print(constant.name)
        print(f"  controls:             {constant.what_it_controls}")
        print(f"  cannot be chosen by:  {constant.why_it_cannot_be_chosen}")
        print()

    print("No-go verdict:")
    print("  A symmetry-allowed Hessian with free constants is not Tier D.")
    print("  Tier D begins only when S_phi0[nodes] fixes those constants or")
    print("  derives a parameter-free coupled spectrum.")


if __name__ == "__main__":
    main()

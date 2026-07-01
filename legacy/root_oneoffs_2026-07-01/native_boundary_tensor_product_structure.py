from dataclasses import dataclass


@dataclass(frozen=True)
class TensorFactor:
    name: str
    factor_space: str
    native_operator: str
    role: str


FACTORS = [
    TensorFactor(
        name="radial/edge scalar factor",
        factor_space="one-dimensional scalar edge data at phi0",
        native_operator="multiplication by eta or eta/2 if a side kernel exists",
        role="sets edge action scale",
    ),
    TensorFactor(
        name="angular ell=1 factor",
        factor_space="H_ell=1(S2), dimension 3",
        native_operator="L1=(-R^2 Delta_S2)/2 = I3",
        role="sets lowest nonconstant angular identity kernel",
    ),
]


def main() -> None:
    print("boundary tensor-product structure")
    print("=" * 35)
    for factor in FACTORS:
        print(factor.name)
        print(f"  factor space:     {factor.factor_space}")
        print(f"  native operator:  {factor.native_operator}")
        print(f"  role:             {factor.role}")
        print()

    print("Tensor product:")
    print("  edge scalar space tensor H_ell=1(S2)")
    print("  operator form: scalar_edge_action tensor L1")
    print()
    print("If scalar_edge_action = eta/2:")
    print("  A_side = (eta/2) L1")
    print()
    print("Structure verdict:")
    print("  The product form is structurally native to a boundary field/operator:")
    print("  radial edge scalars multiply angular boundary operators. What remains")
    print("  missing is the derivation that the scalar side action is eta/2 and")
    print("  that this tensor product is the physical transfer kernel.")


if __name__ == "__main__":
    main()

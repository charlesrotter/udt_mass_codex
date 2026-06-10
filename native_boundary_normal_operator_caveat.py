from dataclasses import dataclass


@dataclass(frozen=True)
class Layer:
    name: str
    exact_statement: str
    implication: str


LAYERS = [
    Layer(
        name="collar coordinates",
        exact_statement="near a smooth boundary, a metric can be written as d rho^2 + h_rho",
        implication="there is an exact normal/tangential split of variables",
    ),
    Layer(
        name="product collar",
        exact_statement="h_rho = h_0 throughout the collar",
        implication="Poisson kernel exp(-rho sqrt(L_h0)) is exact",
    ),
    Layer(
        name="non-product collar",
        exact_statement="h_rho varies with rho",
        implication="extrinsic-curvature and h_rho variation terms modify the exact kernel",
    ),
    Layer(
        name="phi0 boundary value",
        exact_statement="at phi0, f=1 and h_0=R^2 omega",
        implication="the boundary angular operator L1 is exact at the interface",
    ),
    Layer(
        name="UDT missing step",
        exact_statement="the exact bridge kernel has not been derived from the full phi0 collar",
        implication="do not treat the product-collar Poisson kernel as a conclusion yet",
    ),
]


def main() -> None:
    print("boundary-normal operator caveat")
    print("=" * 33)
    for layer in LAYERS:
        print(layer.name)
        print(f"  exact statement: {layer.exact_statement}")
        print(f"  implication:     {layer.implication}")
        print()

    print("Caveat verdict:")
    print("  The product-collar Poisson semigroup is the right atlas object,")
    print("  but UDT must derive that the phi0 bridge reduces to that exact")
    print("  boundary-normal kernel. Otherwise curvature/collar variation may")
    print("  change the composition law.")


if __name__ == "__main__":
    main()

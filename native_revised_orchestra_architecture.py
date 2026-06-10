from dataclasses import dataclass


@dataclass(frozen=True)
class Layer:
    name: str
    role: str
    exact_output: str
    open_gate: str


LAYERS = [
    Layer(
        "H1 collar source",
        "preserve endpoint slope through the collar",
        "delta_h=0 and q=1/3 if s=1/9 is constant",
        "derive source constancy from metric/angular data",
    ),
    Layer(
        "phi0 shell stress",
        "localize the boundary momentum and angular transfer scale",
        "q/2 shell scale and eta=q/6 after H1/S2 projection",
        "derive full S0 value action, not only F-derivative",
    ),
    Layer(
        "symmetric interface gluing",
        "turn full boundary action into one-sided transfer",
        "A_side=(eta/2) I3 on H1",
        "prove transfer object is composable and side-symmetric",
    ),
    Layer(
        "H1 boundary-state measure",
        "count unlabelled bridge channels",
        "Tr_H1 exp[-(eta/2)I3]=3 exp(-eta/2)",
        "prove state counting rather than averaging",
    ),
]


def main() -> None:
    print("revised orchestra architecture")
    print("=" * 33)
    for layer in LAYERS:
        print(layer.name)
        print(f"  role:         {layer.role}")
        print(f"  exact output: {layer.exact_output}")
        print(f"  open gate:    {layer.open_gate}")
        print()

    print("No-approximation verdict:")
    print("  The current best architecture is not one mechanism.")
    print("  It is a layered metric orchestra with distinct collar, shell,")
    print("  gluing, and state-measure roles.")


if __name__ == "__main__":
    main()

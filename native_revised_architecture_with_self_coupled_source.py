from dataclasses import dataclass


@dataclass(frozen=True)
class Layer:
    name: str
    revised_role: str
    exact_or_conditional_output: str
    remaining_gate: str


LAYERS = [
    Layer(
        "self-coupled H1 collar source",
        "one H1 channel share of scalar curvature-share q",
        "s(q)=q/3 -> q-flow dq/dt=q(q-1/3)",
        "derive the activation law from boundary/collar variation",
    ),
    Layer(
        "finite-action branch filter",
        "reject trivial or companion non-finite branches",
        "selects nontrivial finite q=1/3 branch if activation law holds",
        "verify no hidden running/window alters the source law",
    ),
    Layer(
        "phi0 shell transfer",
        "carry q/2 boundary momentum into H1-projected eta",
        "eta=q/6=1/18 on q=1/3 branch",
        "derive S0 value action",
    ),
    Layer(
        "H1 state-count transfer",
        "count unlabelled H1 bridge channels",
        "gamma=3 exp(-eta/2) if trace role holds",
        "derive state-count measure rather than average",
    ),
]


def main() -> None:
    print("revised architecture with self-coupled source")
    print("=" * 52)
    for layer in LAYERS:
        print(layer.name)
        print(f"  revised role: {layer.revised_role}")
        print(f"  output:       {layer.exact_or_conditional_output}")
        print(f"  gate:         {layer.remaining_gate}")
        print()

    print("No-approximation verdict:")
    print("  The collar layer is now best framed as a self-coupled channel-share")
    print("  law, not as an assumed constant source.")


if __name__ == "__main__":
    main()

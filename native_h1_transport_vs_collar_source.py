from dataclasses import dataclass


@dataclass(frozen=True)
class Layer:
    name: str
    exact_metric_fact: str
    consequence: str
    limitation: str


LAYERS = [
    Layer(
        name="kinematic H1 transport",
        exact_metric_fact="each linking S2 has g_AB=r^2 omega_AB and normalized operator -r^2 Delta_S2",
        consequence="ell=1/H1 is identifiable at every radius in the collar",
        limitation="identifiability is not yet a source term",
    ),
    Layer(
        name="constant angular eigenvalue",
        exact_metric_fact="-r^2 Delta_S2 Y_lm=ell(ell+1)Y_lm; for H1, lambda=2",
        consequence="the H1 eigenvalue does not run through the collar",
        limitation="a non-running eigenvalue does not by itself fix source normalization",
    ),
    Layer(
        name="collar source law",
        exact_metric_fact="radial q-flow would use dq/dt=q^2-q+2s(t)",
        consequence="if H1 supplies s=1/9, q=1/3 is fixed and delta_h=0",
        limitation="the map H1 transport -> s=1/9 remains unproved",
    ),
    Layer(
        name="boundary-only H1 projector",
        exact_metric_fact="at phi=0, H1 is the first nontrivial scale-invariant angular imprint",
        consequence="explains macro-accessible imprint after eta/q is supplied",
        limitation="does not control q-running inside the collar",
    ),
]


def main() -> None:
    print("H1 transport versus collar source")
    print("=" * 35)
    for layer in LAYERS:
        print(layer.name)
        print(f"  exact metric fact: {layer.exact_metric_fact}")
        print(f"  consequence:       {layer.consequence}")
        print(f"  limitation:        {layer.limitation}")
        print()

    print("Metric-only verdict:")
    print("  H1 is transported kinematically through the collar because the")
    print("  normalized angular spectrum is radius/phi invariant.")
    print("  But a kinematically transported H1 sector becomes a q-selecting")
    print("  collar source only if the UDT action couples it into s(t).")
    print()
    print("Next proof target:")
    print("  Derive or reject the map:")
    print("    transported H1 angular data -> constant collar source s=1/9")


if __name__ == "__main__":
    main()

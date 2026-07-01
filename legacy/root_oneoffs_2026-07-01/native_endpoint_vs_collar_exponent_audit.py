from dataclasses import dataclass


@dataclass(frozen=True)
class CellCase:
    name: str
    endpoint_p: float
    collar_q: float
    interpretation: str

    @property
    def boundary_scalar(self) -> float:
        return self.collar_q / 2.0

    @property
    def eta(self) -> float:
        return self.boundary_scalar / 3.0


def main() -> None:
    cases = [
        CellCase(
            "pure self-similar cell",
            endpoint_p=1.0 / 3.0,
            collar_q=1.0 / 3.0,
            interpretation="same scaling controls endpoint and phi0 collar",
        ),
        CellCase(
            "endpoint-resonant but shallow collar",
            endpoint_p=1.0 / 3.0,
            collar_q=0.2,
            interpretation="endpoint has p=1/3 but finite-cell profile relaxes before boundary",
        ),
        CellCase(
            "endpoint-resonant but steep collar",
            endpoint_p=1.0 / 3.0,
            collar_q=0.45,
            interpretation="endpoint has p=1/3 but boundary matching steepens the collar",
        ),
        CellCase(
            "smooth flat closure",
            endpoint_p=1.0 / 3.0,
            collar_q=0.0,
            interpretation="f'(R)=0, no extrinsic-curvature jump and no eta from this route",
        ),
    ]

    print("Endpoint vs collar exponent audit")
    print("=" * 36)
    print("Nonlinear finite cells can distinguish:")
    print("  endpoint exponent p_core from f~r^-p_core")
    print("  collar slope q_phi0=-R f'(R)/f(R)")
    print()
    print("The interface scalar uses q_phi0, not p_core directly:")
    print("  B = q_phi0 / 2")
    print("  eta = q_phi0 / 6 after S2 isotropic projection")
    print()

    for case in cases:
        print(case.name)
        print(f"  endpoint p_core={case.endpoint_p:.12g}")
        print(f"  collar q_phi0={case.collar_q:.12g}")
        print(f"  B=q/2={case.boundary_scalar:.12g}")
        print(f"  eta=B/3={case.eta:.12g}")
        print(f"  interpretation: {case.interpretation}")

    print("\nAudit verdict:")
    print("  - p_core=1/3 does not by itself derive eta=1/18.")
    print("  - The eta chain requires q_phi0=1/3 at the interface collar.")
    print("  - A globally self-similar cell has p_core=q_phi0=1/3.")
    print("  - The nonlinear boundary problem must determine whether the metric")
    print("    enforces this equality or allows p_core and q_phi0 to differ.")


if __name__ == "__main__":
    main()

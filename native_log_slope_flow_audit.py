from dataclasses import dataclass


@dataclass(frozen=True)
class FlowCase:
    name: str
    p_core: float
    q_phi0: float
    reason: str

    @property
    def eta(self) -> float:
        return self.q_phi0 / 6.0

    @property
    def fixed_point_preserved(self) -> bool:
        return abs(self.p_core - self.q_phi0) < 1.0e-12


def main() -> None:
    cases = [
        FlowCase(
            "fixed-flow cell",
            1.0 / 3.0,
            1.0 / 3.0,
            "logarithmic slope q=-d ln f/d ln r stays at the self-similar fixed point",
        ),
        FlowCase(
            "irrelevant interior deformation",
            1.0 / 3.0,
            1.0 / 3.0,
            "shape changes h(x) have h'(1)=0 and do not alter the collar slope",
        ),
        FlowCase(
            "boundary-layer deformation",
            1.0 / 3.0,
            0.25,
            "a nonlinear boundary layer changes q at the phi0 collar",
        ),
        FlowCase(
            "smooth exterior matching",
            1.0 / 3.0,
            0.0,
            "f' is forced to vanish at the flat exterior boundary",
        ),
    ]

    print("Log-slope flow audit")
    print("=" * 22)
    print("Define the local logarithmic slope:")
    print("  q(r) = - d ln f / d ln r")
    print("For a pure power f~r^-p, q=p everywhere.")
    print()
    print("Eta depends on the collar value:")
    print("  eta = q_phi0 / 6")
    print()

    for case in cases:
        print(case.name)
        print(f"  p_core={case.p_core:.12g}")
        print(f"  q_phi0={case.q_phi0:.12g}")
        print(f"  fixed point preserved={case.fixed_point_preserved}")
        print(f"  eta={case.eta:.12g}")
        print(f"  reason={case.reason}")

    print("\nFlow verdict:")
    print("  - The nonlinear question is whether q=1/3 is a finite-cell flow")
    print("    fixed point that survives from core to phi0 collar.")
    print("  - If yes, eta=1/18 remains metric-native.")
    print("  - If no, eta must be replaced by q_phi0/6 and the compact ladder shifts.")
    print("  - The next real calculation is the q-flow equation from the full")
    print("    negative-phi/angular boundary action.")


if __name__ == "__main__":
    main()

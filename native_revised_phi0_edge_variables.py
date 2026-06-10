from dataclasses import dataclass


@dataclass(frozen=True)
class EdgeVariable:
    symbol: str
    meaning: str
    phi0_value: str
    role: str


VARIABLES = [
    EdgeVariable(
        symbol="f",
        meaning="metric value at the phi0 collar",
        phi0_value="f=1",
        role="sets the collar as the zero-phi interface",
    ),
    EdgeVariable(
        symbol="Pi_f",
        meaning="C1 conjugate boundary momentum",
        phi0_value="Pi_f=-qR/2",
        role="native linear boundary object",
    ),
    EdgeVariable(
        symbol="K_S2",
        meaning="intrinsic round-S2 sectional curvature",
        phi0_value="K_S2=1/R^2",
        role="phi-blind angular representation arena",
    ),
    EdgeVariable(
        symbol="s^A_B",
        meaning="shape operator of the S2 collar in the spatial slice",
        phi0_value="s^A_B=(1/R) delta^A_B",
        role="embedding value; same as flat at phi0",
    ),
    EdgeVariable(
        symbol="n(s)",
        meaning="normal/radial evolution of the shape operator",
        phi0_value="n(s)=-(1+q/2)/R^2",
        role="embedding evolution; carries q",
    ),
    EdgeVariable(
        symbol="K_rad",
        meaning="radial-angular sectional curvature",
        phi0_value="K_rad=q/(2R^2)",
        role="linear curvature-share object; equals eta source unit before H1 projection",
    ),
    EdgeVariable(
        symbol="n_a",
        meaning="unit H1/S2 direction observable",
        phi0_value="<n_a n_b>=delta_ab/3",
        role="isotropic projection from edge curvature to eta",
    ),
]


def main() -> None:
    print("revised phi0 edge variable set")
    print("=" * 36)
    for variable in VARIABLES:
        print(variable.symbol)
        print(f"  meaning: {variable.meaning}")
        print(f"  phi0:    {variable.phi0_value}")
        print(f"  role:    {variable.role}")
        print()

    print("No-invention verdict:")
    print("  The candidate boundary functional should be searched over these")
    print("  native edge variables before introducing any new mechanism.")


if __name__ == "__main__":
    main()

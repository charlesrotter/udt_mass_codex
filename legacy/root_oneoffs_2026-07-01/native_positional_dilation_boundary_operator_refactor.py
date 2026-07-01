from dataclasses import dataclass


@dataclass(frozen=True)
class RefactorStep:
    name: str
    exact_statement: str
    implication: str


STEPS = [
    RefactorStep(
        name="spatial metric",
        exact_statement="dl^2 = f^-1 dr^2 + r^2 dOmega^2",
        implication="normal distance is not dr; it is d rho = dr/sqrt(f)",
    ),
    RefactorStep(
        name="proper radial coordinate",
        exact_statement="dr/d rho = sqrt(f)",
        implication="the collar is a warped product d rho^2 + r(rho)^2 dOmega^2",
    ),
    RefactorStep(
        name="spatial Laplacian",
        exact_statement="Delta u = u_rhorho + 2(r_rho/r)u_rho + r^-2 Delta_S2 u",
        implication="a first-normal-derivative term appears unless the collar is treated as product",
    ),
    RefactorStep(
        name="angular mode equation",
        exact_statement="for u=a(rho)Y_lm: -a'' - 2(r'/r)a' + l(l+1)a/r^2 = 0",
        implication="ordinary product Poisson kernel is modified by spherical warping",
    ),
    RefactorStep(
        name="Liouville transform",
        exact_statement="with v=r a, the equation is -v'' + [r''/r + l(l+1)/r^2]v = 0",
        implication="the normal operator contains an exact positional-dilation/extrinsic term r''/r",
    ),
    RefactorStep(
        name="UDT radial acceleration",
        exact_statement="r'' = d^2r/d rho^2 = f'/2",
        implication="the extra potential is f'/(2r), directly tied to phi0 slope q",
    ),
]


def main() -> None:
    print("positional-dilation boundary-operator refactor")
    print("=" * 54)
    for step in STEPS:
        print(step.name)
        print(f"  exact statement: {step.exact_statement}")
        print(f"  implication:     {step.implication}")
        print()

    print("Refactor verdict:")
    print("  The GR product-collar Poisson kernel must be refactored through")
    print("  UDT proper radial distance. The exact normal operator gains the")
    print("  warping/extrinsic term r''/r = f'/(2r).")


if __name__ == "__main__":
    main()

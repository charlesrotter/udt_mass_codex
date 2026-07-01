from dataclasses import dataclass


@dataclass(frozen=True)
class Path:
    name: str
    kernel: str
    exact_status: str
    consequence: str


PATHS = [
    Path(
        name="abstract boundary action path",
        kernel="A_side = (eta/2)L1 on boundary data",
        exact_status="valid if UDT boundary action is defined directly on phi0 angular data",
        consequence="gives 3 exp(-eta/2) without using bulk collar propagation",
    ),
    Path(
        name="product-collar Poisson path",
        kernel="exp(-x sqrt(L1))",
        exact_status="exact only for product normal operator -d_x^2+L1",
        consequence="gives 3 exp(-x) with x=eta/2 if side time is eta/2",
    ),
    Path(
        name="UDT warped DtN path",
        kernel="DtN of -d_rho^2 + [r''/r + l(l+1)/r^2]",
        exact_status="the correct bulk-collar path after positional-dilation refactor",
        consequence="generically differs from product kernel; must be solved or characterized",
    ),
    Path(
        name="Calderon boundary-selection path",
        kernel="projector onto two-sided admissible Cauchy data",
        exact_status="promising GR/PDE atlas object; not constructed for UDT phi0",
        consequence="could derive P_phi0 and/or side split if found",
    ),
]


def main() -> None:
    print("DtN kernel path split")
    print("=" * 22)
    for path in PATHS:
        print(path.name)
        print(f"  kernel:       {path.kernel}")
        print(f"  exact status: {path.exact_status}")
        print(f"  consequence:  {path.consequence}")
        print()

    print("Path verdict:")
    print("  There are now distinct paths. The simple gamma path is an abstract")
    print("  boundary-action or product-collar path. The literal UDT bulk DtN path")
    print("  is warped and must be solved separately.")


if __name__ == "__main__":
    main()

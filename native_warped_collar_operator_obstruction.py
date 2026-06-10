from dataclasses import dataclass


@dataclass(frozen=True)
class OperatorCase:
    name: str
    exact_operator: str
    consequence: str
    verdict: str


CASES = [
    OperatorCase(
        name="product cylinder",
        exact_operator="-d_x^2 + L with L independent of x",
        consequence="Poisson kernel is exactly exp(-x sqrt(L))",
        verdict="gives exact semigroup transfer",
    ),
    OperatorCase(
        name="spherical warped collar",
        exact_operator="-a'' - 2(r'/r)a' + l(l+1)a/r^2 for each Y_lm mode",
        consequence="radial first-derivative and r-dependent angular term appear",
        verdict="not the product-cylinder operator",
    ),
    OperatorCase(
        name="phi0 boundary value",
        exact_operator="at phi0, f=1 and boundary angular operator L1=I3",
        consequence="boundary operator is exact at the interface",
        verdict="does not make the whole collar product",
    ),
    OperatorCase(
        name="abstract boundary action",
        exact_operator="A_side=(eta/2)L1 defined directly on boundary data",
        consequence="no bulk propagation through a warped collar is assumed",
        verdict="viable if derived as a boundary action",
    ),
]


def main() -> None:
    print("warped collar operator obstruction")
    print("=" * 36)
    for case in CASES:
        print(case.name)
        print(f"  exact operator: {case.exact_operator}")
        print(f"  consequence:    {case.consequence}")
        print(f"  verdict:        {case.verdict}")
        print()

    print("Obstruction verdict:")
    print("  Ordinary scalar propagation through a spherical collar is not exactly")
    print("  the product Poisson semigroup. The semigroup remains viable only as")
    print("  an abstract boundary action/kernel, or if UDT derives a variable change")
    print("  that exactly reduces the bridge to product form.")


if __name__ == "__main__":
    main()

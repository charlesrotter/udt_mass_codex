from dataclasses import dataclass


@dataclass(frozen=True)
class Gap:
    name: str
    newly_calculated: str
    still_missing: str


GAPS = [
    Gap(
        "q selection",
        "bare C1 A'(1/3)=1, so q=1/3 is not bare-action stationary",
        "the constraint or boundary condition whose stationarity selects the self-similar balance",
    ),
    Gap(
        "H1 identity Hessian",
        "ell=1 second variation is an exact identity block by S2 degeneracy",
        "choice between intrinsic boundary I3 and warped DtN B I3 as the physical transfer action",
    ),
    Gap(
        "trace/product",
        "internal-label contraction plus tensor-product locality explains trace and powers",
        "proof that typed particle slots are internal, local, and independent",
    ),
    Gap(
        "typed coefficients",
        "radial second-jet and angular DtN blocks are calculable metric-action pieces",
        "the typed boundary reduction/Schur complement that maps those blocks to C_M1 and C_E1",
    ),
]


def main() -> None:
    print("variation gap update")
    print("=" * 20)
    for gap in GAPS:
        print(gap.name)
        print(f"  newly calculated: {gap.newly_calculated}")
        print(f"  still missing:    {gap.still_missing}")
        print()

    print("Update verdict:")
    print("  The metric action is producing variation data. The next exact task")
    print("  is not coefficient fitting; it is boundary reduction: identify which")
    print("  variation block is integrated out, fixed, traced, or left internal.")


if __name__ == "__main__":
    main()

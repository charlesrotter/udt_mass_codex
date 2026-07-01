from dataclasses import dataclass


@dataclass(frozen=True)
class Operation:
    name: str
    action_on_block: str
    result_for_k_identity: str
    status: str


OPERATIONS = [
    Operation(
        "fixed external label",
        "select one diagonal channel of exp(-a I_d)",
        "exp(-a)",
        "not gamma; no multiplicity factor",
    ),
    Operation(
        "internal unobserved label",
        "contract the boundary index: Tr exp(-a I_d)",
        "d exp(-a)",
        "gamma form for d=3 and a=eta/2",
    ),
    Operation(
        "normalized average",
        "(1/d) Tr exp(-a I_d)",
        "exp(-a)",
        "removes the multiplicity; not gamma",
    ),
    Operation(
        "determinant",
        "det exp(-a I_d)",
        "exp(-a d)",
        "different exponent; not gamma",
    ),
    Operation(
        "Gaussian integration",
        "integral exp[-(1/2) x^T k I_d x] dx",
        "(2 pi/k)^(d/2), up to measure",
        "measure-sensitive; dangerous unless metric measure is derived",
    ),
    Operation(
        "Schur complement",
        "integrate/fix a coupled block [[A,C],[C^T,B]]",
        "B - C^T A^(-1) C",
        "requires an exact cross block C",
    ),
]


def main() -> None:
    print("boundary operation reduction table")
    print("=" * 34)
    for op in OPERATIONS:
        print(op.name)
        print(f"  action on block: {op.action_on_block}")
        print(f"  result:          {op.result_for_k_identity}")
        print(f"  status:          {op.status}")
        print()

    print("Reduction verdict:")
    print("  The metric can supply the block. The physical boundary operation")
    print("  decides whether that block contributes a trace, determinant, average,")
    print("  Gaussian measure, or Schur complement. These are not interchangeable.")


if __name__ == "__main__":
    main()

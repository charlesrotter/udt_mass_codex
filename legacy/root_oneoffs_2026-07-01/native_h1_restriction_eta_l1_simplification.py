from dataclasses import dataclass
from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


@dataclass(frozen=True)
class Operator:
    name: str
    full_s2_form: str
    h1_restriction: str
    implication: str


ETA = Fraction(1, 18)


OPERATORS = [
    Operator(
        "isotropic angular surface stress",
        "eta I on the selected angular boundary data",
        "eta I3",
        "enough for an H1 value action if H1 is already selected",
    ),
    Operator(
        "normalized ell=1 Laplacian",
        "eta L1, L1=(-R^2 Delta_S2)/2",
        "eta I3",
        "equivalent to isotropic stress after H1 restriction",
    ),
    Operator(
        "rank-one direction stress",
        "eta n n^T",
        "eigenvalues depend on the chosen direction",
        "not equivalent to the H1 identity trace unless averaged or traced differently",
    ),
    Operator(
        "normalized second moment",
        "eta I3/3 if applied as an operator after eta is already formed",
        "eta I3/3",
        "wrong if used after eta; the 1/3 projection has already been spent forming eta",
    ),
]


def main() -> None:
    print("H1 restriction eta-L1 simplification")
    print("=" * 39)
    print(f"eta={fmt(ETA)}")
    print()
    for operator in OPERATORS:
        print(operator.name)
        print(f"  full S2 form:    {operator.full_s2_form}")
        print(f"  H1 restriction:  {operator.h1_restriction}")
        print(f"  implication:     {operator.implication}")
        print()

    print("Simplification verdict:")
    print("  If the transfer space is already H1, the metric does not need to")
    print("  derive a full-S2 eta L1 coupling. It only needs an isotropic angular")
    print("  value action with scalar eta on H1.")


if __name__ == "__main__":
    main()

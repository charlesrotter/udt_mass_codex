from dataclasses import dataclass


@dataclass(frozen=True)
class Coefficient:
    symbol: str
    role: str
    allowed_origin: str
    forbidden_origin: str


COEFFICIENTS = [
    Coefficient(
        "C_M1",
        "dimensionless coefficient multiplying the M1 depth-5 ladder factor",
        "post-Dirac finite-cell normalization, compact occupation, or boundary-action weight",
        "fitted correction chosen after comparing to observed muon mass",
    ),
    Coefficient(
        "C_E1",
        "dimensionless coefficient multiplying the E1 depth-7 ladder factor",
        "endpoint-resonant H1 finite-cell normalization or boundary-action weight",
        "fitted correction chosen after comparing to observed tau mass",
    ),
    Coefficient(
        "C_M2",
        "dimensionless coefficient for the competing compact triplet branch",
        "same compact-bundle sector that defines or suppresses M2",
        "silent omission",
    ),
]


def main() -> None:
    print("Tier C to Tier D coefficient requirements")
    print("=" * 42)
    for coefficient in COEFFICIENTS:
        print(coefficient.symbol)
        print(f"  role:             {coefficient.role}")
        print(f"  allowed origin:   {coefficient.allowed_origin}")
        print(f"  forbidden origin: {coefficient.forbidden_origin}")
        print()

    print("Coefficient gate:")
    print("  Tier D begins only when these coefficients are computed from the")
    print("  post-P_phi0 boundary/cell variables or explicitly banked.")
    print("  Until then, Tier C remains symbolic.")


if __name__ == "__main__":
    main()

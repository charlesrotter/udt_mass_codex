from dataclasses import dataclass


@dataclass(frozen=True)
class Insertion:
    name: str
    inserted_object: str
    why_invalid: str


INSERTIONS = [
    Insertion(
        "assign M1 weight by residual",
        "C_M1 chosen to improve anchored mu-like comparison",
        "uses observed mass before Tier D is complete",
    ),
    Insertion(
        "assign E1 weight by residual",
        "C_E1 chosen to improve anchored tau-like comparison",
        "turns coefficient calculation into fitting",
    ),
    Insertion(
        "drop M2 by coefficient zero",
        "C_M2=0 without compact-bundle or boundary-action derivation",
        "silent omission of a competing d=3 branch",
    ),
    Insertion(
        "assume diagonal Hessian",
        "no cross-coupling among H1, compact, and relative-shape variables",
        "factorization is exactly what the boundary functional must derive",
    ),
]


def main() -> None:
    print("diagonal weight insertion no-go")
    print("=" * 32)
    for insertion in INSERTIONS:
        print(insertion.name)
        print(f"  inserted object: {insertion.inserted_object}")
        print(f"  why invalid:     {insertion.why_invalid}")
        print()

    print("No-go verdict:")
    print("  Any numerical C_i or diagonal block weight inserted before deriving")
    print("  S_phi0[nodes] is P_coeff. P_coeff is not banked in the active lane.")


if __name__ == "__main__":
    main()

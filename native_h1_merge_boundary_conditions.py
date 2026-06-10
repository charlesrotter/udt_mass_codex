from dataclasses import dataclass


@dataclass(frozen=True)
class Condition:
    name: str
    required_status: str
    why_needed: str


CONDITIONS = [
    Condition(
        "H1 transfer-space selection",
        "must be derived or explicitly banked",
        "without H1 restriction, eta I and eta L1 differ on the full S2",
    ),
    Condition(
        "ell=0 exclusion",
        "supported by exact endpoint equation",
        "prevents the constant mode from carrying the transfer action",
    ),
    Condition(
        "isotropic value-action status",
        "still to derive",
        "shell stress gives angular scale, but value action is more than stress signature",
    ),
    Condition(
        "projection not reused",
        "must be enforced",
        "the 1/3 has already been spent forming eta; do not apply I3/3 again",
    ),
]


def main() -> None:
    print("H1 merge boundary conditions")
    print("=" * 30)
    for condition in CONDITIONS:
        print(condition.name)
        print(f"  required status: {condition.required_status}")
        print(f"  why needed:      {condition.why_needed}")
        print()

    print("Condition verdict:")
    print("  The merge is legitimate only after H1 selection.")
    print("  It does not by itself prove the value-action status or transfer trace.")


if __name__ == "__main__":
    main()

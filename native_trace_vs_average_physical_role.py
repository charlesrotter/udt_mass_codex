from dataclasses import dataclass


@dataclass(frozen=True)
class Role:
    name: str
    operation: str
    interpretation: str
    native_fit: str


ROLES = [
    Role(
        "boundary-state count",
        "Tr_H1 exp(-A)",
        "sum over accessible unlabelled bridge channels",
        "natural for a partition/measure multiplier",
    ),
    Role(
        "prepared-channel amplitude",
        "<m|exp(-A)|m>",
        "one selected H1 channel",
        "requires a preferred angular label not supplied by round phi0 geometry",
    ),
    Role(
        "ignorance average",
        "(1/3) Tr_H1 exp(-A)",
        "normalized probability over unknown channel",
        "requires probability normalization external to the boundary action",
    ),
    Role(
        "Gaussian field integral",
        "det(A)^(-1/2) or related",
        "continuous boundary-field measure",
        "requires a specified path-integral measure and normalization",
    ),
]


def main() -> None:
    print("trace versus average physical role")
    print("=" * 38)
    for role in ROLES:
        print(role.name)
        print(f"  operation:      {role.operation}")
        print(f"  interpretation: {role.interpretation}")
        print(f"  native fit:     {role.native_fit}")
        print()

    print("No-approximation verdict:")
    print("  The trace is the correct operation only if the phi0 transfer")
    print("  multiplier is a boundary-state count or partition weight.")
    print("  It is not correct if the quantity is a normalized transition")
    print("  probability for an unknown prepared channel.")


if __name__ == "__main__":
    main()

from dataclasses import dataclass


@dataclass(frozen=True)
class Evidence:
    object_name: str
    support: str
    branch_pressure: str
    caveat: str


ITEMS = [
    Evidence(
        "C1 momentum jump",
        "Delta Pi_f is localized at phi0 when exterior is flat",
        "intrinsic/interface-local",
        "fixes eta scale, not the transfer operation by itself",
    ),
    Evidence(
        "distributional curvature jump",
        "f'' contains a delta term at the slope discontinuity",
        "intrinsic/interface-local",
        "GR curvature is atlas math, not imported dynamics",
    ),
    Evidence(
        "angular-only shell signature",
        "trace-reversed stress has zero time part and isotropic angular parts",
        "intrinsic/interface-local H1 coupling",
        "requires H1 selector and state-count interpretation",
    ),
    Evidence(
        "warped DtN map",
        "on-shell harmonic elimination through the negative-phi collar",
        "bulk/profile-sensitive",
        "correct only if transfer is bulk propagation",
    ),
]


def main() -> None:
    print("transfer locality evidence")
    print("=" * 28)
    for item in ITEMS:
        print(item.object_name)
        print(f"  support:         {item.support}")
        print(f"  branch pressure: {item.branch_pressure}")
        print(f"  caveat:          {item.caveat}")
        print()

    print("No-approximation verdict:")
    print("  The eta-producing native objects currently point to an interface-local")
    print("  shell. The warped DtN branch remains necessary only if the transfer")
    print("  operation is identified with bulk harmonic propagation through the collar.")


if __name__ == "__main__":
    main()

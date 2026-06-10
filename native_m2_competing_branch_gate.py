from dataclasses import dataclass


@dataclass(frozen=True)
class Branch:
    name: str
    dimension: int
    active_role: str
    issue: str


BRANCHES = [
    Branch(
        "M1 compact primitive",
        2,
        "candidate lower-depth compact branch",
        "requires compact primitive occupation if used as anchor branch",
    ),
    Branch(
        "M2 compact triplet",
        3,
        "competing d=3 compact branch",
        "shares the same dimension-depth as E1 unless excluded or weighted by a native rule",
    ),
    Branch(
        "E1 ordinary H1",
        3,
        "candidate d=3 ordinary branch",
        "endpoint resonance and ell=1 support it, but do not by themselves eliminate M2",
    ),
]


def main() -> None:
    print("M2 competing-branch gate")
    print("=" * 26)
    print("If typed depth depends only on dimension d via n=3+2(d-1),")
    print("then all d=3 branches inherit n=7.")
    print()
    for branch in BRANCHES:
        depth = 3 + 2 * (branch.dimension - 1)
        print(branch.name)
        print(f"  dimension d={branch.dimension}")
        print(f"  depth n={depth}")
        print(f"  active role: {branch.active_role}")
        print(f"  issue:       {branch.issue}")
        print()

    print("Gate verdict:")
    print("  The active lane cannot simply choose E1 over M2 by target matching.")
    print("  It needs a native selector: endpoint resonance, compact-bundle")
    print("  occupancy, boundary coefficient suppression, or an edge-graph rule.")


if __name__ == "__main__":
    main()

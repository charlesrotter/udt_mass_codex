from dataclasses import dataclass


@dataclass(frozen=True)
class Branch:
    name: str
    action: str
    claim_allowed: str
    claim_not_allowed: str


BRANCHES = [
    Branch(
        name="derive-kernel branch",
        action="search for an exact separable H1/S2 edge kernel producing s=1/9",
        claim_allowed="P_phi0 can be upgraded from postulate to derived boundary condition if found",
        claim_not_allowed="do not assume factorization before the kernel exists",
    ),
    Branch(
        name="bank-postulate branch",
        action="declare P_phi0 as a minimal native postulate",
        claim_allowed="q, s, and eta are consequences of P_phi0 plus derived H1/S2 projection",
        claim_not_allowed="do not call the phi0 closure derived; do not canonize the full ladder",
    ),
]


def main() -> None:
    print("phi0 decision point")
    print("=" * 20)
    for branch in BRANCHES:
        print(branch.name)
        print(f"  action:             {branch.action}")
        print(f"  claim allowed:      {branch.claim_allowed}")
        print(f"  claim not allowed:  {branch.claim_not_allowed}")
        print()

    print("Decision verdict:")
    print("  The ponder hypothesis has a concrete candidate resolution.")
    print("  The only honest fork is whether P_phi0 is derived now or banked as")
    print("  a minimal postulate while the rest of the orchestra is built around it.")


if __name__ == "__main__":
    main()

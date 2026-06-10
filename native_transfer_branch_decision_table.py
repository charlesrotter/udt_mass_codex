from dataclasses import dataclass


@dataclass(frozen=True)
class Branch:
    name: str
    kernel: str
    physical_reading: str
    accepted_when: str
    rejected_when: str


BRANCHES = [
    Branch(
        "intrinsic interface",
        "A_side = (eta/2) I3",
        "local phi0 boundary transfer / internal interface label contraction",
        "transfer is a boundary event at phi0 using value, momentum jump, H1 projector, and induced measure",
        "a later derivation proves transfer is full bulk-collar propagation",
    ),
    Branch(
        "warped bulk DtN",
        "A_side = (eta/2) B I3 or a normalized D1 form",
        "on-shell finite-collar propagation of angular boundary data",
        "transfer is defined by eliminating the negative-phi collar bulk",
        "used in addition to intrinsic interface action for the same H1 crossing",
    ),
    Branch(
        "product of both",
        "3 exp(-eta/2) times 3 exp(-eta B/2), or equivalent",
        "two transfer kernels assigned to one H1 crossing",
        "never without a proof of two independent physical events",
        "default rejected as double counting",
    ),
]


def main() -> None:
    print("transfer branch decision table")
    print("=" * 31)
    for branch in BRANCHES:
        print(branch.name)
        print(f"  kernel:           {branch.kernel}")
        print(f"  physical reading: {branch.physical_reading}")
        print(f"  accepted when:    {branch.accepted_when}")
        print(f"  rejected when:    {branch.rejected_when}")
        print()

    print("Decision verdict:")
    print("  Keep the intrinsic interface branch as the active transfer branch.")
    print("  Keep warped DtN as the bulk-propagation alternative/correction branch.")
    print("  Do not multiply them for the same H1 transfer event.")


if __name__ == "__main__":
    main()

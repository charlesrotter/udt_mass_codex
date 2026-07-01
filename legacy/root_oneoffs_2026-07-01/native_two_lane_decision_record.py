from dataclasses import dataclass


@dataclass(frozen=True)
class Lane:
    name: str
    status: str
    allowed_work: str
    forbidden_work: str


LANES = [
    Lane(
        "conditional particle-sector lane",
        "active",
        "bank q=1/3 as P_phi0 and derive exact consequences for eta, H1 transfer, DtN discriminator, and particle-sector structure",
        "claim q=1/3 is derived by the already-tested C1/H1/curvature algebra",
    ),
    Lane(
        "foundational q-origin lane",
        "parked but open",
        "search for a genuinely new native boundary, joint, edge-mode, or covariant phase-space object",
        "continue cycling through ordinary scalar potentials or the same q-flow algebra",
    ),
]


def main() -> None:
    print("two-lane decision record")
    print("=" * 24)
    print("Decision:")
    print("  Stop spending primary effort on deriving q=1/3 from the same")
    print("  already-tested local C1/H1/curvature pieces.")
    print()
    for lane in LANES:
        print(lane.name)
        print(f"  status:         {lane.status}")
        print(f"  allowed work:   {lane.allowed_work}")
        print(f"  forbidden work: {lane.forbidden_work}")
        print()

    print("Working rule:")
    print("  P_phi0 is allowed as a minimal explicit postulate/anchor in the")
    print("  particle-sector lane. Any q-origin derivation must come from a new")
    print("  native variational object, not from relabeling the existing pattern.")


if __name__ == "__main__":
    main()

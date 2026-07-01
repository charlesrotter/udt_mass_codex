from dataclasses import dataclass


@dataclass(frozen=True)
class Requirement:
    name: str
    exact_requirement: str
    current_status: str


REQUIREMENTS = [
    Requirement(
        name="scalar edge quantum",
        exact_requirement="eta must be fixed by phi0 edge data",
        current_status="available if P_phi0 is banked",
    ),
    Requirement(
        name="angular identity kernel",
        exact_requirement="L1=(-R^2 Delta_S2)/2 must equal I3 on ell=1",
        current_status="derived metric fact",
    ),
    Requirement(
        name="separable coupling",
        exact_requirement="edge action must factor as scalar eta/2 times L1",
        current_status="not derived",
    ),
    Requirement(
        name="boundary-sidedness",
        exact_requirement="eta must split into eta/2 per side by gluing or amplitude structure",
        current_status="not derived for phi0-to-L1 coupling",
    ),
    Requirement(
        name="channel trace",
        exact_requirement="physical composition must trace over ell=1 channels",
        current_status="not derived",
    ),
    Requirement(
        name="composition over nodes",
        exact_requirement="multiple kernels must be independent or have known coupled spectrum",
        current_status="not derived",
    ),
]


def main() -> None:
    print("coupled kernel exact requirements")
    print("=" * 37)
    for req in REQUIREMENTS:
        print(req.name)
        print(f"  exact requirement: {req.exact_requirement}")
        print(f"  current status:    {req.current_status}")
        print()

    print("Requirement verdict:")
    print("  The metric now supplies the scalar and angular factors. The missing")
    print("  native object is the separable boundary coupling and its composition")
    print("  rule.")


if __name__ == "__main__":
    main()

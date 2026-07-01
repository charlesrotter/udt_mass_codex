from dataclasses import dataclass


@dataclass(frozen=True)
class Selector:
    name: str
    effect_on_m2: str
    status: str
    caveat: str


SELECTORS = [
    Selector(
        "primitive compact-bundle selector",
        "demotes M2 because flux n=2 is nonprimitive while M1 has |n|=1",
        "conditional on compact U(1) bundle occupancy Pbundle0",
        "does not derive why a nontrivial compact bundle must be occupied",
    ),
    Selector(
        "flux-energy superadditivity",
        "demotes M2 because radial flux energy scales as n^2, so n=2 costs more than two primitives",
        "native energy-ordering pressure if compact flux is admitted",
        "does not prove a decay channel or absolute exclusion",
    ),
    Selector(
        "ordinary endpoint resonance",
        "favors E1 over M2 for the d=3 ordinary branch because E1 is the p=1/3 endpoint-resonant H1 sector",
        "strong active-lane selector inside the ordinary angular sector",
        "does not by itself compare ordinary E1 to compact M2 unless compact sectors are separately classified",
    ),
    Selector(
        "silent omission",
        "would remove M2 by not counting it",
        "rejected",
        "this is target-shaped bookkeeping, not a metric rule",
    ),
]


def main() -> None:
    print("active M2 selector status")
    print("=" * 26)
    for selector in SELECTORS:
        print(selector.name)
        print(f"  effect on M2: {selector.effect_on_m2}")
        print(f"  status:       {selector.status}")
        print(f"  caveat:       {selector.caveat}")
        print()

    print("Selector verdict:")
    print("  M2 can be demoted conditionally, not silently.")
    print("  The clean active-lane statement is: if Pbundle0 is banked, then")
    print("  M1 is the primitive compact branch and M2 is nonprimitive/diagnostic,")
    print("  while E1 is the ordinary endpoint-resonant d=3 branch.")


if __name__ == "__main__":
    main()

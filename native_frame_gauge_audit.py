import math
from dataclasses import dataclass


@dataclass(frozen=True)
class CountScenario:
    name: str
    description: str
    subtract_global_frame_gauge: bool
    include_frame_nodes: bool
    include_shape_nodes: bool

    def count(self, dimension: int, frame_count: int) -> int:
        total = 0
        if self.include_frame_nodes:
            total += frame_count
        if self.include_shape_nodes:
            total += 2 * max(0, dimension - 1)
        if self.subtract_global_frame_gauge and total > 0:
            total -= 1
        return total


def mass_from_depth(me: float, gamma: float, depth: int) -> float:
    return me * gamma**depth


def main() -> None:
    frame_count = 3
    eta = 1.0 / 18.0
    gamma = frame_count * math.exp(-eta / 2.0)
    me = 0.51099895
    branches = [("M1", 2), ("E1", 3)]
    scenarios = [
        CountScenario(
            name="physical boundary sectors",
            description="frame and shape constraints are physical boundary nodes",
            subtract_global_frame_gauge=False,
            include_frame_nodes=True,
            include_shape_nodes=True,
        ),
        CountScenario(
            name="one global frame gauge",
            description="one common frame label is gauge and divided out",
            subtract_global_frame_gauge=True,
            include_frame_nodes=True,
            include_shape_nodes=True,
        ),
        CountScenario(
            name="shape nodes only",
            description="frame labels are pure gauge; only shape endpoints count",
            subtract_global_frame_gauge=False,
            include_frame_nodes=False,
            include_shape_nodes=True,
        ),
        CountScenario(
            name="frame nodes only",
            description="shape closure is scalar amplitude only",
            subtract_global_frame_gauge=False,
            include_frame_nodes=True,
            include_shape_nodes=False,
        ),
    ]

    print("Frame gauge/physical audit")
    print("=" * 28)
    print(f"N={frame_count}, eta={eta:.12g}, gamma={gamma:.12g}")
    print()
    for scenario in scenarios:
        print(scenario.name)
        print(f"  {scenario.description}")
        for branch, dimension in branches:
            depth = scenario.count(dimension, frame_count)
            mass = mass_from_depth(me, gamma, depth)
            print(f"  {branch}: d={dimension}, depth={depth}, diagnostic mass={mass:.6g} MeV")
        print()

    print("Audit verdict:")
    print("  - The hierarchy depends strongly on treating frame labels as physical")
    print("    boundary sector data, not as removable gauge coordinates.")
    print("  - A global frame gauge quotient would lower every non-anchor depth by one.")
    print("  - If shape closure is not frame-mediated, the ladder collapses.")
    print("  - The needed derivation is therefore a boundary observable showing that")
    print("    the transported frame label is measured by the interface kernel.")


if __name__ == "__main__":
    main()

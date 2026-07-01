import math


def chain_weight(boundary_action: float, intervals: int, endpoint_half: bool) -> float:
    """Return total exponent assigned by local interval transfer factors.

    Each interval has two boundary sides. If endpoint_half=True, each side
    contributes B/2; gluing two intervals across one internal boundary recovers
    one full B. If False, each side contributes B and internal boundaries are
    double-counted.
    """
    if intervals <= 0:
        return 0.0
    side_weight = 0.5 * boundary_action if endpoint_half else boundary_action
    return 2 * intervals * side_weight


def physical_boundary_count(intervals: int) -> tuple[int, int]:
    external = 2
    internal = max(0, intervals - 1)
    return external, internal


def physical_total(boundary_action: float, intervals: int, external_half: bool) -> float:
    external, internal = physical_boundary_count(intervals)
    external_weight = 0.5 * boundary_action if external_half else boundary_action
    return internal * boundary_action + external * external_weight


def main() -> None:
    eta = 1.0 / 18.0
    print("Symmetric boundary-transfer audit")
    print("=" * 35)
    print("A local interval transfer has a left and right boundary side.")
    print("For composable transfer kernels, a shared internal boundary should")
    print("contribute one boundary action after gluing, not two.")
    print()
    print("Symmetric assignment:")
    print("  each side carries B/2")
    print("  two adjacent sides at a glued boundary give B")
    print()

    for intervals in range(1, 5):
        half_total = chain_weight(eta, intervals, endpoint_half=True)
        full_total = chain_weight(eta, intervals, endpoint_half=False)
        physical_half_ext = physical_total(eta, intervals, external_half=True)
        print(f"intervals={intervals}")
        print(f"  side-half transfer exponent={half_total:.12g}")
        print(f"  physical total with half external endpoints={physical_half_ext:.12g}")
        print(f"  side-full transfer exponent={full_total:.12g}")
        print(f"  double-count excess={full_total - physical_half_ext:.12g}")

    gamma_half = 3.0 * math.exp(-eta / 2.0)
    gamma_full = 3.0 * math.exp(-eta)
    print("\nSingle transfer step:")
    print(f"  half-side trace gamma = 3 exp(-eta/2) = {gamma_half:.12g}")
    print(f"  full-side trace gamma = 3 exp(-eta)   = {gamma_full:.12g}")
    print()
    print("Audit verdict:")
    print("  - eta/2 is natural for a composable symmetric transfer kernel.")
    print("  - The full boundary action eta is recovered only after two sides are glued.")
    print("  - This derives the half as a no-double-counting rule if the mass step is")
    print("    one side of a boundary transfer.")
    print("  - Remaining condition: show each closure constraint is represented by")
    print("    such a composable boundary kernel.")


if __name__ == "__main__":
    main()

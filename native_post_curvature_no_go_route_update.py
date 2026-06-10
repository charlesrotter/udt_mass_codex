from dataclasses import dataclass


@dataclass(frozen=True)
class Route:
    name: str
    updated_status: str
    reason: str
    next_test: str


ROUTES = [
    Route(
        "ordinary scalar collar action",
        "demote",
        "raw R3/R2 coefficient loses the q source under exact variation",
        "do not pursue unless a new non-scalar variable is found",
    ),
    Route(
        "self-coupled activation s(q)=q/3",
        "conditional only",
        "algebraic fixed branch remains exact, but action origin is missing",
        "keep as a minimal postulate candidate, not a derived result",
    ),
    Route(
        "boundary/joint slope channel",
        "promote as search target",
        "q survives naturally as C1 momentum jump, angular stress, and slope-density",
        "look for a native variational boundary or edge term that fixes q",
    ),
    Route(
        "interface-local H1 transfer",
        "promote as best current conditional theorem",
        "once q is supplied, eta=q/6 and gamma=3 exp(-eta/2) follow cleanly",
        "derive the q-setting boundary condition or state q as conditional",
    ),
    Route(
        "warped DtN collar propagation",
        "keep as discriminator",
        "it is exact if transfer is bulk-eliminated instead of interface-local",
        "use only after the action chooses a bulk propagation interpretation",
    ),
]


def main() -> None:
    print("post curvature no-go route update")
    print("=" * 36)
    for route in ROUTES:
        print(route.name)
        print(f"  updated status: {route.updated_status}")
        print(f"  reason:         {route.reason}")
        print(f"  next test:      {route.next_test}")
        print()

    print("Ponder verdict:")
    print("  The metric orchestra is not pointing to a simple scalar bulk")
    print("  mechanism. It is pointing to a collar boundary/joint channel where")
    print("  value, slope, angular stress, and H1 projection meet.")


if __name__ == "__main__":
    main()

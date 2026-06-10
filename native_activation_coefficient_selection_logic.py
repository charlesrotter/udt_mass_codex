from dataclasses import dataclass


@dataclass(frozen=True)
class Logic:
    candidate: str
    coefficient: str
    metric_reason: str
    problem: str


LOGICS = [
    Logic(
        "use full curvature share",
        "c=1",
        "activate all spatial curvature share without projection",
        "over-activates; no finite positive branch",
    ),
    Logic(
        "use one radial-angular plane",
        "c=1/2",
        "split q across two radial-angular planes",
        "selects only trivial branch",
    ),
    Logic(
        "use H1 isotropic channel share",
        "c=1/3",
        "project scalar curvature share into three equivalent H1 channels",
        "best current candidate; needs variational activation proof",
    ),
    Logic(
        "use radial plane plus H1 share",
        "c=1/6",
        "combine per-plane share with H1 projection",
        "lands on non-finite companion branch",
    ),
]


def main() -> None:
    print("activation coefficient selection logic")
    print("=" * 43)
    for item in LOGICS:
        print(item.candidate)
        print(f"  coefficient:   {item.coefficient}")
        print(f"  metric reason: {item.metric_reason}")
        print(f"  problem:       {item.problem}")
        print()

    print("No-approximation verdict:")
    print("  The c=1/3 law has the cleanest metric role: scalar curvature-share")
    print("  activation distributed over the three transported H1 channels.")
    print("  It remains a variational coupling gate.")


if __name__ == "__main__":
    main()

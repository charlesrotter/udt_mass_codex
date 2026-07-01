from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    name: str
    statement: str
    status: str


POINTS = [
    Point(
        "curvature-share identity",
        "R3/R2=q at phi0",
        "exact metric identity",
    ),
    Point(
        "H1 projection factor",
        "<n_a n_b>=delta_ab/3",
        "exact round-S2 average",
    ),
    Point(
        "source law",
        "s(q)=q/3",
        "candidate coupling, not yet variationally derived",
    ),
    Point(
        "fixed branch",
        "q=1/3, s=1/9",
        "exact consequence if source law holds",
    ),
]


def main() -> None:
    print("s(q)=q/3 status audit")
    print("=" * 26)
    for point in POINTS:
        print(point.name)
        print(f"  statement: {point.statement}")
        print(f"  status:    {point.status}")
        print()

    print("No-approximation verdict:")
    print("  The ingredients of s(q)=q/3 are exact.")
    print("  The multiplication into a source law is the remaining gate.")
    print("  Derive it from the boundary/collar action before treating P_phi0")
    print("  as fully derived.")


if __name__ == "__main__":
    main()

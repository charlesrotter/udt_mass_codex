from dataclasses import dataclass


@dataclass(frozen=True)
class Side:
    name: str
    role: str
    shared_object: str
    consequence: str


SIDES = [
    Side(
        name="negative-phi side",
        role="matter-side radial closure / edge momentum",
        shared_object="phi0 S2 angular spectrum",
        consequence="supplies the edge scalar eta through P_phi0 if banked",
    ),
    Side(
        name="positive-phi / scalar-background side",
        role="accessibility/exterior continuation arena",
        shared_object="same normalized angular spectrum",
        consequence="provides the other side of the angular bridge",
    ),
    Side(
        name="phi0 bridge",
        role="interface where both sides share f=1 and the same S2 operator",
        shared_object="L1=I3 on ell=1",
        consequence="makes a two-sided angular boundary-kernel interpretation plausible",
    ),
]


def main() -> None:
    print("two-sided phi bridge interpretation")
    print("=" * 39)
    for side in SIDES:
        print(side.name)
        print(f"  role:          {side.role}")
        print(f"  shared object: {side.shared_object}")
        print(f"  consequence:   {side.consequence}")
        print()

    print("Interpretation verdict:")
    print("  This gives a native reason to revisit the eta/2 half-factor: if phi0")
    print("  is a bridge between negative-phi matter closure and positive-phi/scalar")
    print("  accessibility, the edge quantum may be naturally two-sided. This is")
    print("  still an interpretation until the boundary action is derived.")


if __name__ == "__main__":
    main()

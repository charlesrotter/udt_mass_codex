from dataclasses import dataclass


@dataclass(frozen=True)
class Filter:
    name: str
    result: str
    status: str


FILTERS = [
    Filter(
        "phi-sign/angular invariance",
        "normalized angular spectrum is shared across phi<0, phi=0, and exterior phi>0",
        "derived metric fact",
    ),
    Filter(
        "constant-mode rejection",
        "ell=0 is scalar/background, not an angular bridge with nonzero operator",
        "selector assumption unless tied to accessibility/shape constraint",
    ),
    Filter(
        "lowest nonconstant sector",
        "ell=1 is the first nonconstant angular eigenspace",
        "derived once ell=0 is rejected",
    ),
    Filter(
        "triplet multiplicity",
        "dim H1 = 2 ell + 1 = 3",
        "derived angular spectrum fact",
    ),
    Filter(
        "identity action on selected space",
        "isotropic stress and normalized L1 both restrict to I3 on H1",
        "derived restricted-operator fact",
    ),
]


def main() -> None:
    print("H1 transfer-space selector status")
    print("=" * 39)
    for item in FILTERS:
        print(item.name)
        print(f"  result: {item.result}")
        print(f"  status: {item.status}")
        print()

    print("No-approximation verdict:")
    print("  H1 is strongly native if the constant mode is excluded.")
    print("  The remaining selector burden is to justify ell=0 rejection")
    print("  as a metric/accessibility condition, not a desired outcome.")


if __name__ == "__main__":
    main()

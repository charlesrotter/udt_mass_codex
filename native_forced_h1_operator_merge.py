from dataclasses import dataclass
from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


@dataclass(frozen=True)
class MergeItem:
    name: str
    pre_merge_form: str
    h1_form: str
    merge_status: str


ETA = Fraction(1, 18)


MERGE_ITEMS = [
    MergeItem(
        "isotropic H1 value action",
        "eta I on selected angular data",
        "eta I3",
        "merge allowed if selected data are H1",
    ),
    MergeItem(
        "normalized ell=1 Laplacian action",
        "eta L1, with L1=(-R^2 Delta_S2)/2",
        "eta I3",
        "merge forced after H1 projection",
    ),
    MergeItem(
        "H1 trace action",
        "eta times the identity on a three-state transfer space",
        "eta I3",
        "same object after transfer-space selection",
    ),
]


def main() -> None:
    print("forced H1 operator merge")
    print("=" * 25)
    print(f"eta={fmt(ETA)}")
    print()
    for item in MERGE_ITEMS:
        print(item.name)
        print(f"  pre-merge form: {item.pre_merge_form}")
        print(f"  H1 form:        {item.h1_form}")
        print(f"  merge status:   {item.merge_status}")
        print()

    print("Forced-merge verdict:")
    print("  After H1 transfer-space selection, these are not separate mechanisms.")
    print("  They are the same H1 identity value action written in different")
    print("  metric languages.")


if __name__ == "__main__":
    main()

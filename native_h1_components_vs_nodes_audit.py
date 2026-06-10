from dataclasses import dataclass


@dataclass(frozen=True)
class Quantity:
    name: str
    exact_value: str
    meaning: str
    transfer_status: str


QUANTITIES = [
    Quantity(
        name="H1 component count",
        exact_value="3",
        meaning="three ambient components n_a",
        transfer_status="may support channel multiplicity if a transfer rule is postulated or derived",
    ),
    Quantity(
        name="unit constraint",
        exact_value="n_a n_a = 1",
        meaning="one exact constraint on the three components",
        transfer_status="prevents reading component count as unconstrained degrees of freedom",
    ),
    Quantity(
        name="S2 manifold dimension",
        exact_value="2",
        meaning="the unit vector n_a lives on S2",
        transfer_status="geometric degree count, not automatically transfer-node count",
    ),
    Quantity(
        name="isotropic second moment",
        exact_value="<n_a n_b> = delta_ab/3",
        meaning="projection identity over the round S2",
        transfer_status="derived projection factor for eta",
    ),
    Quantity(
        name="projector trace",
        exact_value="tr(delta_ab/3) = 1",
        meaning="the normalized projector sums to one total share",
        transfer_status="does not by itself create three independent transfer nodes",
    ),
]


def main() -> None:
    print("H1 components vs transfer nodes audit")
    print("=" * 43)
    for quantity in QUANTITIES:
        print(quantity.name)
        print(f"  exact value:      {quantity.exact_value}")
        print(f"  meaning:          {quantity.meaning}")
        print(f"  transfer status:  {quantity.transfer_status}")
        print()

    print("No-invention verdict:")
    print("  The exact H1/S2 geometry derives a 1/3 projection and a three-component")
    print("  channel arena. It does not by itself derive three independent transfer")
    print("  depth nodes. Treat 3-as-multiplicity and 3-as-depth separately.")


if __name__ == "__main__":
    main()

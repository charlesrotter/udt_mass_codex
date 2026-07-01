from fractions import Fraction


def fmt(value):
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main():
    q = Fraction(1, 3)
    eta = Fraction(1, 18)
    c1_action = Fraction(1, 12)
    scalar_boundary_momentum = q / 2
    h1_projected_unit = eta
    one_sided_transfer = eta / 2

    residuals = {
        "A3_wedge_A3_to_A3": Fraction(-1, 6),
        "S5_wedge_S5_to_A3": Fraction(1, 36),
        "A3_wedge_S5_to_S5": Fraction(0, 1),
    }

    instruments = {
        "scalar_boundary_momentum_q_over_2": scalar_boundary_momentum,
        "projected_H1_unit_eta": h1_projected_unit,
        "one_sided_transfer_eta_over_2": one_sided_transfer,
        "unprojected_C1_action": c1_action,
    }

    typed_closures = {
        "A3A3_plus_scalar_boundary_momentum": (
            residuals["A3_wedge_A3_to_A3"] + scalar_boundary_momentum
        ),
        "S5S5_minus_one_sided_transfer": (
            residuals["S5_wedge_S5_to_A3"] - one_sided_transfer
        ),
        "pure_pair_with_boundary_supply_and_side_export": (
            residuals["A3_wedge_A3_to_A3"]
            + residuals["S5_wedge_S5_to_A3"]
            + scalar_boundary_momentum
            - one_sided_transfer
        ),
    }

    identities = {
        "A3A3_deficit_is_minus_scalar_boundary_momentum": (
            residuals["A3_wedge_A3_to_A3"] == -scalar_boundary_momentum
        ),
        "S5S5_surplus_is_one_sided_transfer": (
            residuals["S5_wedge_S5_to_A3"] == one_sided_transfer
        ),
        "mixed_channel_already_balanced": residuals["A3_wedge_S5_to_S5"] == 0,
        "typed_pure_pair_accounting_closes": (
            typed_closures["pure_pair_with_boundary_supply_and_side_export"] == 0
        ),
        "image_unit_is_half_scalar_boundary_momentum": (
            c1_action == scalar_boundary_momentum / 2
        ),
        "domain_unit_is_one_sided_transfer": (
            Fraction(1, 36) == one_sided_transfer
        ),
    }

    printable_residuals = {key: fmt(value) for key, value in residuals.items()}
    printable_instruments = {key: fmt(value) for key, value in instruments.items()}
    printable_closures = {key: fmt(value) for key, value in typed_closures.items()}

    interpretation = {
        "A3A3": "its negative residual is exactly the scalar C1 boundary momentum with opposite sign",
        "S5S5": "its positive residual is exactly one one-sided H1 transfer unit",
        "mixed": "A3 wedge S5 needs no source accounting at this layer",
        "gate": "pure channels may enter only through typed boundary accounting, not as free spectrum terms",
        "guard": "closure identities are necessary accounting checks, not particle assignments",
    }

    print(f"residuals: {printable_residuals}")
    print(f"instruments: {printable_instruments}")
    print(f"typed_closures: {printable_closures}")
    print(f"identities: {identities}")
    print(f"interpretation: {interpretation}")


if __name__ == "__main__":
    main()

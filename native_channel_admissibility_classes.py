from fractions import Fraction


def fmt(value):
    if isinstance(value, Fraction):
        if value.denominator == 1:
            return str(value.numerator)
        return f"{value.numerator}/{value.denominator}"
    return value


def main():
    q = Fraction(1, 3)
    eta = Fraction(1, 18)

    instruments = {
        "scalar_boundary_momentum": q / 2,
        "one_sided_H1_transfer": eta / 2,
        "C1_image_unit": Fraction(1, 12),
        "C1_domain_unit": Fraction(1, 36),
    }

    channels = {
        "A3_wedge_S5_to_S5": {
            "domain_load": Fraction(5, 12),
            "image_action": Fraction(5, 12),
            "residual": Fraction(0),
            "class": "freely_balanced_interaction",
            "boundary_instrument": "none",
            "admissibility": "admissible before source accounting",
        },
        "A3_wedge_A3_to_A3": {
            "domain_load": Fraction(1, 12),
            "image_action": Fraction(1, 4),
            "residual": Fraction(-1, 6),
            "class": "boundary_momentum_coupled",
            "boundary_instrument": "scalar_boundary_momentum",
            "admissibility": "admissible only with q/2 boundary supply",
        },
        "S5_wedge_S5_to_A3": {
            "domain_load": Fraction(5, 18),
            "image_action": Fraction(1, 4),
            "residual": Fraction(1, 36),
            "class": "one_sided_transfer_coupled",
            "boundary_instrument": "one_sided_H1_transfer",
            "admissibility": "admissible only with eta/2 transfer export",
        },
        "trace_wedge_T8": {
            "domain_load": Fraction(2, 9),
            "image_action": Fraction(0),
            "residual": Fraction(2, 9),
            "class": "silent_kernel_load",
            "boundary_instrument": "not yet identified",
            "admissibility": "parked until trace-kernel role is derived",
        },
    }

    for channel in channels.values():
        instrument = channel["boundary_instrument"]
        if instrument in instruments:
            channel["closed_residual"] = channel["residual"] + (
                instruments[instrument]
                if channel["residual"] < 0
                else -instruments[instrument]
            )
        else:
            channel["closed_residual"] = channel["residual"]

    order = [
        "A3_wedge_S5_to_S5",
        "S5_wedge_S5_to_A3",
        "A3_wedge_A3_to_A3",
        "trace_wedge_T8",
    ]

    identities = {
        "mixed_is_only_freely_balanced_channel": (
            channels["A3_wedge_S5_to_S5"]["residual"] == 0
        ),
        "S5S5_closes_with_eta_half": (
            channels["S5_wedge_S5_to_A3"]["closed_residual"] == 0
        ),
        "A3A3_closes_with_q_half": (
            channels["A3_wedge_A3_to_A3"]["closed_residual"] == 0
        ),
        "trace_kernel_not_closed_by_current_pair": (
            channels["trace_wedge_T8"]["closed_residual"] != 0
        ),
    }

    printable_channels = {
        key: {k: fmt(v) for k, v in value.items()} for key, value in channels.items()
    }
    printable_instruments = {key: fmt(value) for key, value in instruments.items()}

    verdict = {
        "taxonomy": "the two-form sector splits into free, boundary-momentum, transfer, and silent-kernel classes",
        "first_spectrum_use": "use freely balanced and typed-boundary classes before any observed-particle assignment",
        "guard": "do not convert trace-kernel load or boundary instruments into masses without a derived readout",
    }

    print(f"instruments: {printable_instruments}")
    print(f"channels: {printable_channels}")
    print(f"admissibility_order: {order}")
    print(f"identities: {identities}")
    print(f"verdict: {verdict}")


if __name__ == "__main__":
    main()

from fractions import Fraction


def fmt(value):
    if isinstance(value, Fraction):
        if value.denominator == 1:
            return str(value.numerator)
        return f"{value.numerator}/{value.denominator}"
    return value


def units(value, unit):
    return value / unit


def main():
    domain_unit = Fraction(1, 36)
    image_unit = Fraction(1, 12)
    eta = Fraction(1, 18)
    ninth_unit = Fraction(1, 9)

    quotient = {
        "scalar_anchor": Fraction(1, 9),
        "trace_bridge": Fraction(2, 9),
        "active_image": Fraction(2, 3),
    }

    unit_table = {}
    for name, value in quotient.items():
        unit_table[name] = {
            "value": value,
            "domain_units": units(value, domain_unit),
            "image_units": units(value, image_unit),
            "eta_units": units(value, eta),
            "ninth_units": units(value, ninth_unit),
        }

    local_channels = {
        "trace_wedge_T8_domain": 8 * domain_unit,
        "A3_wedge_A3_domain": 3 * domain_unit,
        "A3_wedge_S5_domain": 15 * domain_unit,
        "S5_wedge_S5_domain": 10 * domain_unit,
        "global_T8_image": 8 * image_unit,
    }

    local_units = {
        name: {
            "value": value,
            "domain_units": units(value, domain_unit),
            "image_units": units(value, image_unit),
            "eta_units": units(value, eta),
            "ninth_units": units(value, ninth_unit),
        }
        for name, value in local_channels.items()
    }

    identities = {
        "trace_bridge_equals_trace_wedge_T8_domain": (
            quotient["trace_bridge"] == local_channels["trace_wedge_T8_domain"]
        ),
        "active_image_equals_global_T8_image": (
            quotient["active_image"] == local_channels["global_T8_image"]
        ),
        "scalar_anchor_is_four_domain_units": (
            units(quotient["scalar_anchor"], domain_unit) == 4
        ),
        "scalar_anchor_is_two_eta_units": units(quotient["scalar_anchor"], eta) == 2,
        "scalar_anchor_is_not_a_local_twoform_channel": (
            units(quotient["scalar_anchor"], domain_unit)
            not in [8, 3, 15, 10]
        ),
        "quotient_closes_full_domain_units": (
            sum(units(value, domain_unit) for value in quotient.values()) == 36
        ),
    }

    interpretation = {
        "trace_bridge": "same object as trace wedge T8 domain load",
        "active_image": "same object as global commutator T8 image action",
        "scalar_anchor": "not one of the local two-form channel domains; it is the central End(H1) normalization anchor",
        "unit_warning": "local channel domains live naturally in 36ths; quotient completion lives cleanly in ninths",
        "guard": "do not force scalar_anchor into a missing local channel just because it is four domain units",
    }

    printable = {
        "units": {
            "domain_unit": domain_unit,
            "image_unit": image_unit,
            "eta": eta,
            "ninth_unit": ninth_unit,
        },
        "quotient": unit_table,
        "local": local_units,
    }
    printable = {
        section: (
            {key: fmt(value) for key, value in data.items()}
            if section == "units"
            else {
                key: {k: fmt(v) for k, v in value.items()}
                for key, value in data.items()
            }
        )
        for section, data in printable.items()
    }

    print(f"report: {printable}")
    print(f"identities: {identities}")
    print(f"interpretation: {interpretation}")


if __name__ == "__main__":
    main()

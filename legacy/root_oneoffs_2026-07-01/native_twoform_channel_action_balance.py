from fractions import Fraction


def fmt(value):
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main():
    domain_unit = Fraction(1, 36)
    image_unit = Fraction(1, 12)

    channels = {
        "trace_wedge_T8": {
            "domain_dim": 8,
            "image_rank": 0,
            "kernel_dim": 8,
            "image_sector": "none",
        },
        "A3_wedge_A3": {
            "domain_dim": 3,
            "image_rank": 3,
            "kernel_dim": 0,
            "image_sector": "A3",
        },
        "A3_wedge_S5": {
            "domain_dim": 15,
            "image_rank": 5,
            "kernel_dim": 10,
            "image_sector": "S5",
        },
        "S5_wedge_S5": {
            "domain_dim": 10,
            "image_rank": 3,
            "kernel_dim": 7,
            "image_sector": "A3",
        },
    }

    report = {}
    for name, data in channels.items():
        domain_load = data["domain_dim"] * domain_unit
        image_action = data["image_rank"] * image_unit
        residual = domain_load - image_action
        report[name] = {
            **data,
            "domain_load": domain_load,
            "image_action": image_action,
            "residual_domain_minus_image": residual,
            "balanced": residual == 0,
        }

    notable = {
        "A3_wedge_S5_balanced": report["A3_wedge_S5"]["balanced"],
        "S5_wedge_S5_residual_equals_eta_half": report["S5_wedge_S5"][
            "residual_domain_minus_image"
        ]
        == Fraction(1, 36),
        "A3_wedge_A3_deficit_equals_minus_q_over_2": report["A3_wedge_A3"][
            "residual_domain_minus_image"
        ]
        == Fraction(-1, 6),
        "trace_wedge_T8_load": report["trace_wedge_T8"]["domain_load"],
    }

    interpretation = {
        "balanced_channel": "A3 wedge S5 has domain load 15/36 and image action 5/12; these are equal.",
        "S5S5_residual": "S5 wedge S5 leaves residual +1/36, exactly eta/2.",
        "A3A3_deficit": "A3 wedge A3 has image action larger than domain load by 1/6, the unprojected boundary momentum q/2.",
        "trace_channel": "trace wedge T8 carries C1 domain load 2/9 but no commutator image.",
        "caution": "These are channel action balances, not particle assignments or mass formulas.",
    }

    printable_report = {
        key: {
            k: fmt(v) if isinstance(v, Fraction) else v
            for k, v in value.items()
        }
        for key, value in report.items()
    }
    printable_notable = {
        key: fmt(value) if isinstance(value, Fraction) else value
        for key, value in notable.items()
    }

    print(f"channel_report: {printable_report}")
    print(f"notable: {printable_notable}")
    print(f"interpretation: {interpretation}")


if __name__ == "__main__":
    main()

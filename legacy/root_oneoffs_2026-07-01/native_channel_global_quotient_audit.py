from fractions import Fraction


def fmt(value):
    if isinstance(value, Fraction):
        if value.denominator == 1:
            return str(value.numerator)
        return f"{value.numerator}/{value.denominator}"
    return value


def main():
    domain_unit = Fraction(1, 36)
    image_unit = Fraction(1, 12)

    channels = {
        "trace_wedge_T8": {"domain": 8, "local_image": 0, "target": "none"},
        "A3_wedge_A3": {"domain": 3, "local_image": 3, "target": "A3"},
        "A3_wedge_S5": {"domain": 15, "local_image": 5, "target": "S5"},
        "S5_wedge_S5": {"domain": 10, "local_image": 3, "target": "A3"},
    }

    local_image_sum = sum(item["local_image"] for item in channels.values())
    global_image_rank = 8
    image_overlap = local_image_sum - global_image_rank

    total_domain = sum(item["domain"] for item in channels.values())
    local_image_action = local_image_sum * image_unit
    global_image_action = global_image_rank * image_unit
    overlap_action = image_overlap * image_unit
    total_domain_load = total_domain * domain_unit

    local_residual = total_domain_load - local_image_action
    global_residual = total_domain_load - global_image_action

    a3_local_sources = {
        "A3_wedge_A3": channels["A3_wedge_A3"]["local_image"],
        "S5_wedge_S5": channels["S5_wedge_S5"]["local_image"],
    }

    report = {
        "total_domain_dim": total_domain,
        "total_domain_load": total_domain_load,
        "local_image_rank_sum": local_image_sum,
        "global_image_rank": global_image_rank,
        "image_overlap_rank": image_overlap,
        "local_image_action": local_image_action,
        "global_image_action": global_image_action,
        "overlap_action": overlap_action,
        "local_residual": local_residual,
        "global_residual": global_residual,
        "local_plus_overlap_equals_global": local_residual + overlap_action == global_residual,
        "a3_local_sources": a3_local_sources,
    }

    identities = {
        "overlap_action_equals_A3_weight": overlap_action == Fraction(1, 4),
        "local_residual_equals_C1_unprojected_action": local_residual == Fraction(1, 12),
        "global_residual_equals_trace_kernel_fraction": global_residual == Fraction(1, 3),
        "global_image_action_equals_active_threeform_fraction": global_image_action == Fraction(2, 3),
    }

    interpretation = {
        "local": "Channel-local image actions sum to 11 image directions because A3 appears from both A3^A3 and S5^S5.",
        "global": "The global commutator image is only T8=8; the repeated A3 image is quotiented as a 3-rank overlap.",
        "overlap": "The overlap action is 3/12=1/4, the A3 projector weight.",
        "residual_shift": "Local residual 1/12 becomes global residual 1/3 after adding the A3 overlap action 1/4.",
        "caution": "Use global quotient quantities for spectrum readout; local channel balances diagnose interaction structure.",
    }

    printable_report = {key: fmt(value) for key, value in report.items()}
    printable_identities = {key: fmt(value) for key, value in identities.items()}

    print(f"report: {printable_report}")
    print(f"identities: {printable_identities}")
    print(f"interpretation: {interpretation}")


if __name__ == "__main__":
    main()

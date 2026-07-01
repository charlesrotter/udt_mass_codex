from fractions import Fraction


def fmt(value):
    if isinstance(value, Fraction):
        if value.denominator == 1:
            return str(value.numerator)
        return f"{value.numerator}/{value.denominator}"
    return value


def main():
    q = Fraction(1, 3)
    dim_trace = 1
    dim_t8 = 8
    dim_end = 9

    s = Fraction(1, dim_end)
    trace_share_in_end = Fraction(dim_trace, dim_end)
    t8_share_in_end = Fraction(dim_t8, dim_end)

    w_t8 = Fraction(2, 3)
    trace_kernel_load = q * w_t8
    active_image_action = w_t8
    trace_plus_image_load = trace_kernel_load + active_image_action
    residue = 1 - trace_plus_image_load

    identities = {
        "s_is_trace_share_in_End": s == trace_share_in_end,
        "T8_share_in_End_is_8s": t8_share_in_end == 8 * s,
        "trace_plus_image_load_is_T8_share": (
            trace_plus_image_load == t8_share_in_end
        ),
        "residue_is_s": residue == s,
        "residue_is_trace_share": residue == trace_share_in_end,
        "trace_plus_image_plus_residue_closes_unit": (
            trace_plus_image_load + residue == 1
        ),
        "trace_kernel_load_is_q_WT8": trace_kernel_load == q * w_t8,
    }

    readings = {
        "End_quotient": "the load split reproduces End(H1)=trace+T8 as 1/9 + 8/9",
        "scalar_anchor": "the leftover s=1/9 is exactly the central trace share, not an arbitrary correction",
        "active_share": "trace-kernel plus active-image loads account for the full T8 share of End(H1)",
        "guard": "this is a normalization/quotient identity, not an observed mass or particle label",
    }

    report = {
        "dimensions": {
            "trace": dim_trace,
            "T8": dim_t8,
            "End_H1": dim_end,
        },
        "shares": {
            "s": s,
            "trace_share_in_End": trace_share_in_end,
            "T8_share_in_End": t8_share_in_end,
        },
        "loads": {
            "trace_kernel_load": trace_kernel_load,
            "active_image_action": active_image_action,
            "trace_plus_image_load": trace_plus_image_load,
            "residue": residue,
        },
    }

    printable_report = {
        section: {key: fmt(value) for key, value in values.items()}
        for section, values in report.items()
    }

    print(f"report: {printable_report}")
    print(f"identities: {identities}")
    print(f"readings: {readings}")


if __name__ == "__main__":
    main()

from fractions import Fraction


def fmt(value):
    if isinstance(value, Fraction):
        if value.denominator == 1:
            return str(value.numerator)
        return f"{value.numerator}/{value.denominator}"
    return value


def main():
    q = Fraction(1, 3)
    s = Fraction(1, 9)
    domain_unit = Fraction(1, 36)
    image_unit = Fraction(1, 12)

    dims = {
        "trace_wedge_T8_kernel_copy": 8,
        "commutator_image_T8": 8,
        "Lambda2_End_domain": 36,
        "End_H1": 9,
    }

    values = {
        "trace_kernel_load": dims["trace_wedge_T8_kernel_copy"] * domain_unit,
        "active_image_action": dims["commutator_image_T8"] * image_unit,
        "one_EndH1_unit": s,
        "full_domain_load": dims["Lambda2_End_domain"] * domain_unit,
    }

    values["trace_plus_image"] = (
        values["trace_kernel_load"] + values["active_image_action"]
    )
    values["full_minus_trace_plus_image"] = (
        values["full_domain_load"] - values["trace_plus_image"]
    )

    identities = {
        "trace_copy_dim_equals_image_dim": (
            dims["trace_wedge_T8_kernel_copy"] == dims["commutator_image_T8"]
        ),
        "trace_load_is_q_times_image_action": (
            values["trace_kernel_load"] == q * values["active_image_action"]
        ),
        "image_action_is_three_trace_loads": (
            values["active_image_action"] == 3 * values["trace_kernel_load"]
        ),
        "trace_plus_image_leaves_End_unit": (
            values["full_minus_trace_plus_image"] == s
        ),
        "trace_plus_image_is_eight_End_units": values["trace_plus_image"] == 8 * s,
        "End_unit_is_one_ninth": s == Fraction(1, dims["End_H1"]),
    }

    candidate_readings = {
        "q_scaled_shadow": "trace kernel is a q-scaled scalar copy of the active T8 image",
        "quotient_pair": "central T8 copy and active T8 image form an 8+8 paired structure before quotient/readout",
        "normalization_gap": "trace+image accounts for 8/9 of the full two-form load, leaving one End(H1) unit s=1/9",
    }

    guards = {
        "not_mass": "none of these identities assigns a particle mass",
        "not_force": "the trace copy is central and has no commutator image",
        "next_gate": "derive whether the remaining s=1/9 is a normalization residue, trace scalar anchor, or quotient measure",
    }

    printable = {
        "dims": dims,
        "values": {key: fmt(value) for key, value in values.items()},
        "q": fmt(q),
        "s": fmt(s),
    }

    print(f"report: {printable}")
    print(f"identities: {identities}")
    print(f"candidate_readings: {candidate_readings}")
    print(f"guards: {guards}")


if __name__ == "__main__":
    main()

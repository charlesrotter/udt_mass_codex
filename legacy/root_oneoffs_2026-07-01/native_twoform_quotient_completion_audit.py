from fractions import Fraction


def fmt(value):
    if isinstance(value, Fraction):
        if value.denominator == 1:
            return str(value.numerator)
        return f"{value.numerator}/{value.denominator}"
    return value


def main():
    dim_end = 9
    dim_t8 = 8
    q = Fraction(1, 3)
    s = Fraction(1, dim_end)

    scalar_anchor = s
    active_image = Fraction(2, 3)
    trace_bridge = q * active_image
    total = scalar_anchor + trace_bridge + active_image

    normalized_ninths = {
        "scalar_anchor": scalar_anchor / s,
        "trace_bridge": trace_bridge / s,
        "active_image": active_image / s,
        "total": total / s,
    }

    identities = {
        "scalar_anchor_is_one_End_unit": scalar_anchor == s,
        "trace_bridge_is_two_End_units": trace_bridge == 2 * s,
        "active_image_is_six_End_units": active_image == 6 * s,
        "completion_sums_to_one": total == 1,
        "ninth_count_sums_to_End_dim": normalized_ninths["total"] == dim_end,
        "active_plus_trace_bridge_is_T8_share": (
            active_image + trace_bridge == Fraction(dim_t8, dim_end)
        ),
        "scalar_plus_T8_share_is_End": (
            scalar_anchor + Fraction(dim_t8, dim_end) == 1
        ),
    }

    roles = {
        "scalar_anchor": {
            "value": scalar_anchor,
            "ninth_units": normalized_ninths["scalar_anchor"],
            "role": "central trace share of End(H1)",
        },
        "trace_bridge": {
            "value": trace_bridge,
            "ninth_units": normalized_ninths["trace_bridge"],
            "role": "q-scaled scalar bridge/shadow of active T8",
        },
        "active_image": {
            "value": active_image,
            "ninth_units": normalized_ninths["active_image"],
            "role": "global commutator image action W(T8)",
        },
    }

    warnings = {
        "not_local_channel_sum": "this is a top-level quotient/load split, not the local channel residual ledger",
        "not_mass_formula": "the 1:2:6 ninth-unit split is not an observed particle spectrum",
        "next": "connect this quotient layer to admissible two-form roads and radial/depth rules",
    }

    printable_roles = {
        name: {key: fmt(value) for key, value in data.items()}
        for name, data in roles.items()
    }
    printable = {
        "q": fmt(q),
        "s": fmt(s),
        "roles": printable_roles,
        "normalized_ninths": {
            key: fmt(value) for key, value in normalized_ninths.items()
        },
        "total": fmt(total),
    }

    print(f"report: {printable}")
    print(f"identities: {identities}")
    print(f"warnings: {warnings}")


if __name__ == "__main__":
    main()

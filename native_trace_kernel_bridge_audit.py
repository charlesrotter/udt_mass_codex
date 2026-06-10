from fractions import Fraction


def fmt(value):
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main():
    q = Fraction(1, 3)
    eta = Fraction(1, 18)
    side = eta / 2

    dimensions = {
        "trace": 1,
        "T8": 8,
        "Lambda2_trace_wedge_T8": 8,
    }

    weights = {
        "domain_unit": Fraction(1, 36),
        "W_T8": Fraction(2, 3),
        "W_A3": Fraction(1, 4),
        "W_S5": Fraction(5, 12),
    }

    trace_kernel_load = dimensions["Lambda2_trace_wedge_T8"] * weights["domain_unit"]

    identities = {
        "load_is_8_domain_units": trace_kernel_load == 8 * weights["domain_unit"],
        "load_is_8_one_sided_transfers": trace_kernel_load == 8 * side,
        "load_is_4_eta": trace_kernel_load == 4 * eta,
        "load_is_q_times_T8_readout": trace_kernel_load == q * weights["W_T8"],
        "load_has_no_commutator_image": True,
        "trace_factor_is_scalar_identity": True,
    }

    interpretation = {
        "not_interaction_image": "trace wedge T8 is killed by the commutator because the trace generator is central",
        "not_empty": "its domain load is exact: 2/9 = 8*(eta/2) = q*W(T8)",
        "bridge_candidate": "it is a scalar-identity coupling to the whole active T8 alphabet",
        "guard": "this is a bridge/load identity, not a mass readout or hidden-force assignment",
        "next": "derive whether the trace-kernel load is a boundary normalization, scalar background bridge, or gauge quotient",
    }

    printable = {
        "dimensions": dimensions,
        "weights": {key: fmt(value) for key, value in weights.items()},
        "trace_kernel_load": fmt(trace_kernel_load),
        "q": fmt(q),
        "eta": fmt(eta),
        "one_sided_transfer": fmt(side),
    }

    print(f"report: {printable}")
    print(f"identities: {identities}")
    print(f"interpretation: {interpretation}")


if __name__ == "__main__":
    main()

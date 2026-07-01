from fractions import Fraction


def main():
    domain_dim = 36
    image_ranks = {
        "A3": 3,
        "S5": 5,
        "T8": 8,
    }

    readouts = {}
    for name, rank in image_ranks.items():
        readouts[name] = {
            "commutator_action_readout": Fraction(rank, 12),
            "independent_product_trace_count": domain_dim * rank,
            "normalized_image_share": Fraction(rank, image_ranks["T8"]),
            "domain_average_weight": Fraction(domain_dim * rank, domain_dim * image_ranks["T8"]),
        }

    gate = {
        "commutator_action_readout": {
            "status": "native current candidate",
            "requires": "C1 domain weight plus commutator isotropy",
            "formula": "Tr(P)/12",
        },
        "independent_product_trace_count": {
            "status": "not selected",
            "requires": "independent tensor-product trace over Lambda^2 End(H1) cells and image-sector labels",
            "formula": "36*Tr(P)",
            "warning": "commutator selector couples/quotients the two-form domain to T8; it does not by itself supply an independent product trace",
        },
        "normalized_image_share": {
            "status": "dimension share only",
            "requires": "choosing normalized probability over T8 image directions",
            "formula": "Tr(P)/8",
        },
    }

    verdict = {
        "108_180_status": "available only under independent_product_trace_count, not under current commutator_action_readout",
        "mass_coefficient_status": "open",
        "proof_obligation": "derive independent product-trace readout from boundary gluing, source overlap, or a separate partition trace before using 108 or 180 as observable coefficients",
    }

    print(f"readouts: {readouts}")
    print(f"gate: {gate}")
    print(f"verdict: {verdict}")


if __name__ == "__main__":
    main()

from fractions import Fraction


def fmt(frac):
    if frac.denominator == 1:
        return str(frac.numerator)
    return f"{frac.numerator}/{frac.denominator}"


def split_fraction(part, whole):
    return Fraction(part, whole)


def main():
    twoform = {
        "full_domain": 36,
        "full_image": 8,
        "full_kernel": 28,
        "central_kernel": 8,
        "active_domain": 28,
        "active_image": 8,
        "active_kernel": 20,
    }

    twoform_fractions = {
        "image_over_full_domain": split_fraction(twoform["full_image"], twoform["full_domain"]),
        "kernel_over_full_domain": split_fraction(twoform["full_kernel"], twoform["full_domain"]),
        "central_kernel_over_full_domain": split_fraction(twoform["central_kernel"], twoform["full_domain"]),
        "active_domain_over_full_domain": split_fraction(twoform["active_domain"], twoform["full_domain"]),
        "image_over_active_domain": split_fraction(twoform["active_image"], twoform["active_domain"]),
        "kernel_over_active_domain": split_fraction(twoform["active_kernel"], twoform["active_domain"]),
    }

    block_fractions = {
        "Lambda2_A3_image_fraction": split_fraction(3, 3),
        "A3_wedge_S5_image_fraction": split_fraction(5, 15),
        "A3_wedge_S5_kernel_fraction": split_fraction(10, 15),
        "Lambda2_S5_image_fraction": split_fraction(3, 10),
        "Lambda2_S5_kernel_fraction": split_fraction(7, 10),
    }

    threeform = {
        "full_domain": 84,
        "trace_kernel": 28,
        "active_domain": 56,
        "active_support_block_domain": 31,
        "active_zero_block_domain": 25,
    }

    threeform_fractions = {
        "trace_kernel_over_full_domain": split_fraction(threeform["trace_kernel"], threeform["full_domain"]),
        "active_domain_over_full_domain": split_fraction(threeform["active_domain"], threeform["full_domain"]),
        "support_block_over_active_domain": split_fraction(threeform["active_support_block_domain"], threeform["active_domain"]),
        "zero_block_over_active_domain": split_fraction(threeform["active_zero_block_domain"], threeform["active_domain"]),
    }

    report = {
        "twoform_dimensions": twoform,
        "twoform_fractions": {k: fmt(v) for k, v in twoform_fractions.items()},
        "block_fractions": {k: fmt(v) for k, v in block_fractions.items()},
        "threeform_dimensions": threeform,
        "threeform_fractions": {k: fmt(v) for k, v in threeform_fractions.items()},
        "notable_native_fractions": {
            "twoform_full_image": "2/9",
            "twoform_full_kernel": "7/9",
            "twoform_active_image": "2/7",
            "twoform_active_kernel": "5/7",
            "threeform_trace_kernel": "1/3",
            "threeform_active_domain": "2/3",
        },
        "interpretation": {
            "seven": "The 7 first appears as the denominator of active two-form filtering: image 2/7, kernel 5/7.",
            "not_imported": "These are exact commutator-domain fractions, not nuclear or Standard Model couplings.",
            "candidate_use": "Legacy 2/7, 5/7, and 7 fingerprints should be retested against this native active-domain filter.",
        },
    }

    for key, value in report.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()

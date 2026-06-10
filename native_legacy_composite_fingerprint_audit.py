from fractions import Fraction
from math import comb


def main():
    dims = {
        "H1": 3,
        "EndH1": 9,
        "T8": 8,
        "A3": 3,
        "S5": 5,
        "Lambda2_EndH1": comb(9, 2),
        "Lambda2_T8": comb(8, 2),
        "Lambda3_EndH1": comb(9, 3),
        "Lambda3_T8": comb(8, 3),
    }

    fractions = {
        "active_twoform_image_fraction": Fraction(2, 7),
        "active_twoform_kernel_fraction": Fraction(5, 7),
        "full_twoform_kernel_fraction": Fraction(7, 9),
    }

    composites = {
        "63": {
            "value": 63,
            "native_forms": [
                "EndH1 * active_twoform_denominator = 9 * 7",
                "Lambda2_EndH1 + Lambda2_T8 - 1 = 36 + 28 - 1",
            ],
            "status": "fingerprint only; not a native dimension or operator trace yet",
        },
        "84": {
            "value": 84,
            "native_forms": [
                "Lambda3_EndH1 = C(9,3)",
                "H1 * Lambda2_T8 = 3 * 28",
                "trace_kernel_28 + active_threeform_domain_56",
            ],
            "status": "native three-form domain; not a mass coefficient",
        },
        "108": {
            "value": 108,
            "native_forms": [
                "A3 * Lambda2_EndH1 = 3 * 36",
            ],
            "status": "native composite fingerprint; no readout rule",
        },
        "180": {
            "value": 180,
            "native_forms": [
                "S5 * Lambda2_EndH1 = 5 * 36",
            ],
            "status": "native composite fingerprint; no readout rule",
        },
        "5/3": {
            "value": Fraction(5, 3),
            "native_forms": [
                "S5 / A3",
                "180 / 108",
            ],
            "status": "native image-split ratio; not a coupling by itself",
        },
    }

    checks = {
        "63_as_9_times_7": dims["EndH1"] * 7 == 63,
        "84_as_C9_3": dims["Lambda3_EndH1"] == 84,
        "84_as_3_times_28": dims["H1"] * dims["Lambda2_T8"] == 84,
        "108_as_3_times_36": dims["A3"] * dims["Lambda2_EndH1"] == 108,
        "180_as_5_times_36": dims["S5"] * dims["Lambda2_EndH1"] == 180,
        "180_over_108": Fraction(180, 108),
    }

    interpretation = {
        "native_read": "108 and 180 are C1 two-form-domain 36 weighted by the active image split 3 and 5.",
        "ratio": "5/3 is the S5/A3 split ratio of the active T8 image.",
        "caution": "These are composite fingerprints only until a metric readout rule maps them to observables.",
        "63_caution": "63 has a simple 9*7 native fingerprint, but unlike 84/108/180 it is not yet a dimension of a constructed native space.",
    }

    print(f"dims: {dims}")
    print(f"fractions: {fractions}")
    print(f"checks: {checks}")
    print(f"composites: {composites}")
    print(f"interpretation: {interpretation}")


if __name__ == "__main__":
    main()

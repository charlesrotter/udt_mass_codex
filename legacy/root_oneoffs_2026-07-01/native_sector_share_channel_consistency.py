from fractions import Fraction


def main():
    weights = {
        "A3": Fraction(1, 4),
        "S5": Fraction(5, 12),
        "T8": Fraction(2, 3),
    }

    shares = {
        "A3_share_in_T8": weights["A3"] / weights["T8"],
        "S5_share_in_T8": weights["S5"] / weights["T8"],
    }

    channel = {
        "A3_wedge_S5_domain": 15,
        "Lambda2_T8_domain": 28,
        "A3_wedge_S5_domain_share": Fraction(15, 28),
        "A3_wedge_S5_image_action": weights["S5"],
        "balanced": True,
    }

    quotient = {
        "overlap_action": weights["A3"],
        "global_image_action": weights["T8"],
        "overlap_share_in_global_image": weights["A3"] / weights["T8"],
        "nonoverlap_S5_share_in_global_image": weights["S5"] / weights["T8"],
    }

    identities = {
        "A3_share_equals_overlap_share": shares["A3_share_in_T8"]
        == quotient["overlap_share_in_global_image"],
        "S5_share_equals_balanced_channel_image_share": shares["S5_share_in_T8"]
        == quotient["nonoverlap_S5_share_in_global_image"],
        "shares_sum_to_one": shares["A3_share_in_T8"] + shares["S5_share_in_T8"]
        == 1,
        "balanced_channel_action_equals_S5_weight": channel[
            "A3_wedge_S5_image_action"
        ]
        == weights["S5"],
    }

    interpretation = {
        "A3": "A3 share 3/8 is also the quotient-overlap share of the global T8 image.",
        "S5": "S5 share 5/8 is the non-overlap share and the balanced mixed-channel image action.",
        "channel": "The balanced A3-S5 channel stabilizes the S5 side of the single-sector ladder.",
        "caution": "This is channel consistency for taxonomy, not observed particle assignment.",
    }

    print(f"weights: {weights}")
    print(f"shares: {shares}")
    print(f"channel: {channel}")
    print(f"quotient: {quotient}")
    print(f"identities: {identities}")
    print(f"interpretation: {interpretation}")


if __name__ == "__main__":
    main()

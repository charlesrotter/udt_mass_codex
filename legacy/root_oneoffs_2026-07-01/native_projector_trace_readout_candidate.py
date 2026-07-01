from fractions import Fraction


def main():
    image_weight_per_direction = Fraction(1, 12)

    ranks = {
        "A3": 3,
        "S5": 5,
        "T8": 8,
    }

    weights = {
        name: rank * image_weight_per_direction
        for name, rank in ranks.items()
    }

    identities = {
        "A3_weight": weights["A3"],
        "S5_weight": weights["S5"],
        "T8_weight": weights["T8"],
        "A3_plus_S5_equals_T8": weights["A3"] + weights["S5"] == weights["T8"],
        "A3_weight_equals_1_over_4": weights["A3"] == Fraction(1, 4),
        "S5_weight_equals_5_over_12": weights["S5"] == Fraction(5, 12),
        "T8_weight_equals_2_over_3": weights["T8"] == Fraction(2, 3),
        "S5_over_A3": weights["S5"] / weights["A3"],
        "S5_minus_A3": weights["S5"] - weights["A3"],
    }

    readout_rule_candidate = {
        "rule": "For a canonical image-sector projector P inside T8, read the scalar weight as Tr(P)/12.",
        "source": "C1 side action 1/36 pushed through commutator isotropy BBt=3P_T8 gives 1/12 per T8 direction.",
        "invariant": "Tr(P) is conjugation-invariant within the canonical A3/S5 split.",
        "not_claimed": "No mapping to particle masses or couplings is made by this rule alone.",
    }

    print(f"ranks: {ranks}")
    print(f"weights: {weights}")
    print(f"identities: {identities}")
    print(f"readout_rule_candidate: {readout_rule_candidate}")


if __name__ == "__main__":
    main()

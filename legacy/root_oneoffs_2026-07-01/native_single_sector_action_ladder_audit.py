from fractions import Fraction


def fmt(value):
    if isinstance(value, Fraction):
        if value.denominator == 1:
            return str(value.numerator)
        return f"{value.numerator}/{value.denominator}"
    return value


def main():
    weights = {
        "A3": Fraction(1, 4),
        "S5": Fraction(5, 12),
        "T8": Fraction(2, 3),
    }

    ordered = sorted(weights.items(), key=lambda item: item[1])

    gaps = {
        "S5_minus_A3": weights["S5"] - weights["A3"],
        "T8_minus_S5": weights["T8"] - weights["S5"],
        "T8_minus_A3": weights["T8"] - weights["A3"],
    }

    ratios = {
        "S5_over_A3": weights["S5"] / weights["A3"],
        "T8_over_S5": weights["T8"] / weights["S5"],
        "T8_over_A3": weights["T8"] / weights["A3"],
    }

    complements = {
        f"1_minus_{name}": 1 - weight for name, weight in weights.items()
    }

    normalized_to_total = {
        name: weight / weights["T8"] for name, weight in weights.items()
    }

    audit = {
        "ordered_weights": [(name, fmt(weight)) for name, weight in ordered],
        "gaps": {key: fmt(value) for key, value in gaps.items()},
        "ratios": {key: fmt(value) for key, value in ratios.items()},
        "complements": {key: fmt(value) for key, value in complements.items()},
        "normalized_to_T8": {key: fmt(value) for key, value in normalized_to_total.items()},
        "gap_pattern_arithmetic": gaps["S5_minus_A3"] == Fraction(1, 6)
        and gaps["T8_minus_S5"] == Fraction(1, 4),
        "classification": {
            "native_order": "A3 < S5 < T8",
            "native_gaps": "1/6 then 1/4",
            "native_ratios": "5/3, 8/5, 8/3",
            "status": "classification ladder seed, not mass ladder",
        },
        "proof_gap": "No rule maps action weights, gaps, ratios, or complements to observed mass ratios.",
    }

    print(f"audit: {audit}")


if __name__ == "__main__":
    main()

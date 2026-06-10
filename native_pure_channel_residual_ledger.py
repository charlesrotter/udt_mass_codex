from fractions import Fraction


def fmt(value):
    if isinstance(value, Fraction):
        if value.denominator == 1:
            return str(value.numerator)
        return f"{value.numerator}/{value.denominator}"
    return value


def main():
    q = Fraction(1, 3)
    eta = Fraction(1, 18)
    eta_half = Fraction(1, 36)
    c1 = Fraction(1, 12)

    residuals = {
        "S5_wedge_S5_to_A3": eta_half,
        "A3_wedge_A3_to_A3": -q / 2,
        "balanced_A3_wedge_S5_to_S5": Fraction(0),
        "local_channel_total": eta_half - q / 2,
    }

    combinations = {
        "pure_residual_sum": residuals["S5_wedge_S5_to_A3"]
        + residuals["A3_wedge_A3_to_A3"],
        "pure_residual_sum_plus_C1": residuals["S5_wedge_S5_to_A3"]
        + residuals["A3_wedge_A3_to_A3"]
        + c1,
        "pure_residual_sum_plus_q_over_2": residuals["S5_wedge_S5_to_A3"]
        + residuals["A3_wedge_A3_to_A3"]
        + q / 2,
        "pure_residual_sum_plus_eta": residuals["S5_wedge_S5_to_A3"]
        + residuals["A3_wedge_A3_to_A3"]
        + eta,
    }

    identities = {
        "S5S5_residual_is_eta_half": residuals["S5_wedge_S5_to_A3"] == eta_half,
        "A3A3_residual_is_minus_q_over_2": residuals["A3_wedge_A3_to_A3"]
        == -q / 2,
        "pure_sum_is_minus_5_over_36": combinations["pure_residual_sum"]
        == Fraction(-5, 36),
        "pure_sum_plus_q_over_2_is_eta_half": combinations[
            "pure_residual_sum_plus_q_over_2"
        ]
        == eta_half,
        "pure_sum_plus_C1_is_minus_eta": combinations["pure_residual_sum_plus_C1"]
        == -eta,
    }

    interpretation = {
        "S5S5": "pure S5 channel underfills image action by eta/2; it carries a small positive side-action residual.",
        "A3A3": "pure A3 channel overdemands image action by q/2; it needs boundary momentum/source supply.",
        "not_closed": "The pure residuals do not cancel each other or close to zero with the balanced channel.",
        "next": "Treat pure channels as source-accounting branches, not as the first balanced interaction branch.",
    }

    print(f"residuals: {{ {', '.join(f'{k}: {fmt(v)}' for k, v in residuals.items())} }}")
    print(f"combinations: {{ {', '.join(f'{k}: {fmt(v)}' for k, v in combinations.items())} }}")
    print(f"identities: {identities}")
    print(f"interpretation: {interpretation}")


if __name__ == "__main__":
    main()

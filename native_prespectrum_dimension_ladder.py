from fractions import Fraction
from math import comb


def main():
    h1 = 3
    end_h1 = h1 * h1
    lambda2_end_h1 = comb(end_h1, 2)

    prespectrum = {
        "q": Fraction(1, 3),
        "s": Fraction(1, 9),
        "Delta_Pi_over_R": Fraction(1, 6),
        "eta": Fraction(1, 18),
        "eta_half": Fraction(1, 36),
    }

    dimension_ladder = {
        "dim_H1": h1,
        "dim_End_H1": end_h1,
        "dim_Lambda2_End_H1": lambda2_end_h1,
    }

    matches = {
        "q_equals_1_over_dim_H1": prespectrum["q"] == Fraction(1, h1),
        "s_equals_1_over_dim_End_H1": prespectrum["s"] == Fraction(1, end_h1),
        "Delta_Pi_over_R_equals_1_over_2_dim_H1": prespectrum["Delta_Pi_over_R"]
        == Fraction(1, 2 * h1),
        "eta_equals_2_over_dim_Lambda2_End_H1": prespectrum["eta"]
        == Fraction(2, lambda2_end_h1),
        "eta_half_equals_1_over_dim_Lambda2_End_H1": prespectrum["eta_half"]
        == Fraction(1, lambda2_end_h1),
    }

    interpretation = {
        "native_pattern": "The pre-spectrum constants align with reciprocals of H1, End(H1), and Lambda^2 End(H1) dimensions.",
        "selector_candidate": "eta/2=1/36 gives a metric-action reason to examine Lambda^2 End(H1) before higher exterior sectors.",
        "not_closed": "This is a dimension-ladder consilience, not yet a proof that Lambda^2 End(H1) is a particle sector.",
        "consequence": "If Lambda^2 End(H1) is selected, its 9D Hodge complement is Lambda^7 End(H1), giving a native candidate for the old 7.",
    }

    print(f"dimension_ladder: {dimension_ladder}")
    print(f"prespectrum: {prespectrum}")
    print(f"matches: {matches}")
    print(f"all_matches: {all(matches.values())}")
    print(f"interpretation: {interpretation}")


if __name__ == "__main__":
    main()

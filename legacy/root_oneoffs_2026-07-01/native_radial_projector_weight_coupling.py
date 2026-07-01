from fractions import Fraction
from math import sqrt


def c1_action(q):
    return q * q / (4 * (1 - 2 * q))


def q_from_action(weight):
    # Solve q^2/[4(1-2q)] = weight on the finite-action branch 0<q<1/2.
    w = float(weight)
    return -4 * w + 2 * sqrt(w * (4 * w + 1))


def main():
    q0 = Fraction(1, 3)
    base_action = c1_action(q0)
    ranks = {"A3": 3, "S5": 5, "T8": 8}
    weights = {name: Fraction(rank, 12) for name, rank in ranks.items()}

    fixed_branch = {
        name: {
            "rank": rank,
            "q": q0,
            "base_radial_action": base_action,
            "sector_action": rank * base_action,
            "matches_WP": rank * base_action == weights[name],
        }
        for name, rank in ranks.items()
    }

    selected_branch = {
        name: {
            "target_action_WP": weight,
            "q_solving_Aq_equals_WP": q_from_action(weight),
            "finite_action_q_lt_half": q_from_action(weight) < 0.5,
            "status": "candidate only; equation A(q)=W(P) not derived",
        }
        for name, weight in weights.items()
    }

    verdict = {
        "derived_coupling": "At fixed q=1/3, sector action equals rank(P)*S_C1/R = Tr(P)/12 = W(P).",
        "not_derived": "A sector-dependent q(P) from A(q)=W(P).",
        "meaning": "The metric currently supports projector-weighted action readout on one radial branch, not separate radial depths per sector.",
        "next": "Look for an actual boundary condition or radial equation that would select q(P), otherwise keep q common and W(P) as taxonomy action weights.",
    }

    print(f"base_q: {q0}")
    print(f"base_action: {base_action}")
    print(f"weights: {weights}")
    print(f"fixed_branch: {fixed_branch}")
    print(f"selected_branch_hypothesis: {selected_branch}")
    print(f"verdict: {verdict}")


if __name__ == "__main__":
    main()

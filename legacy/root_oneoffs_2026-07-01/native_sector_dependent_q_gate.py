from fractions import Fraction
from math import sqrt


def q_from_action(weight):
    w = float(weight)
    return -4 * w + 2 * sqrt(w * (4 * w + 1))


def main():
    elementary_q = Fraction(1, 3)
    elementary_eta = Fraction(1, 18)
    elementary_eta_half = Fraction(1, 36)

    weights = {
        "A3": Fraction(1, 4),
        "S5": Fraction(5, 12),
        "T8": Fraction(2, 3),
    }

    hypotheses = {}
    for name, weight in weights.items():
        q_candidate = q_from_action(weight)
        eta_if_recomputed = q_candidate / 6
        hypotheses[name] = {
            "W(P)": weight,
            "q_candidate_from_Aq_equals_WP": q_candidate,
            "finite_action": 0 < q_candidate < 0.5,
            "equals_elementary_q": abs(q_candidate - float(elementary_q)) < 1e-12,
            "eta_if_recomputed": eta_if_recomputed,
            "eta_would_change": abs(eta_if_recomputed - float(elementary_eta)) > 1e-12,
        }

    gates = {
        "elementary_branch": {
            "q": elementary_q,
            "eta": elementary_eta,
            "eta_half": elementary_eta_half,
            "status": "derived/pre-spectrum ground branch",
        },
        "sector_dependent_q": {
            "status": "not elementary unless a new boundary rule supersedes q=1/3",
            "allowed_role": "candidate excitation/depth branch",
            "blocked_role": "cannot be used as ground taxonomy while eta=1/18 and eta/2=1/36 are held fixed",
        },
    }

    verdict = {
        "common_q_ground": "keep q=1/3 for current taxonomy",
        "qP_hypothesis": "park as possible radial excitation/depth mechanism",
        "proof_obligation": "derive a boundary condition that either selects q(P) as an excitation or replaces the elementary q=1/3 branch",
    }

    print(f"hypotheses: {hypotheses}")
    print(f"gates: {gates}")
    print(f"verdict: {verdict}")


if __name__ == "__main__":
    main()

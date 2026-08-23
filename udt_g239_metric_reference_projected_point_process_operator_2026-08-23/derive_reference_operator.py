#!/usr/bin/env python3
"""Exact finite-dimensional witnesses for the G239 point-process operator."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent
LANDING = (
    "REFERENCE_PROJECTED_METRIC_INTENSITY_OPERATOR_DERIVED_CONDITIONALLY"
    "__MATCHED_REFERENCE_AND_ANGULARLY_CONSTANT_RESPONSE_CANCEL_EXACTLY"
    "__NONCONSTANT_METRIC_PUSHFORWARD_CAN_SURVIVE_FIXED_SURVEY_REFERENCE"
    "__CONNECTED_PAIR_TERM_SEPARATES_EXACTLY"
    "__PHYSICAL_HISTORY_SOURCE_AND_BRANCH_POPULATION_OPEN"
)


def normalize(values: list[Fraction]) -> list[Fraction]:
    total = sum(values, Fraction(0))
    if total <= 0:
        raise ValueError("normalization requires positive total")
    return [value / total for value in values]


def bilinear(left: list[Fraction], kernel: list[list[Fraction]], right: list[Fraction]) -> Fraction:
    n = len(left)
    if len(right) != n or len(kernel) != n or any(len(row) != n for row in kernel):
        raise ValueError("incompatible bilinear dimensions")
    return sum(
        (left[i] * kernel[i][j] * right[j] for i in range(n) for j in range(n)),
        Fraction(0),
    )


def matrix_pairing(kernel: list[list[Fraction]], measure: list[list[Fraction]]) -> Fraction:
    n = len(kernel)
    if len(measure) != n or any(len(row) != n for row in kernel + measure):
        raise ValueError("incompatible matrix dimensions")
    return sum(
        (kernel[i][j] * measure[i][j] for i in range(n) for j in range(n)),
        Fraction(0),
    )


def outer(left: list[Fraction], right: list[Fraction]) -> list[list[Fraction]]:
    return [[x * y for y in right] for x in left]


def add_matrix(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[x + y for x, y in zip(row_a, row_b)] for row_a, row_b in zip(a, b)]


def scale_matrix(scale: Fraction, a: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[scale * x for x in row] for row in a]


def subtract(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    return [x - y for x, y in zip(left, right)]


def subtract_matrix(
    a: list[list[Fraction]], b: list[list[Fraction]]
) -> list[list[Fraction]]:
    return [[x - y for x, y in zip(row_a, row_b)] for row_a, row_b in zip(a, b)]


def fraction_payload(value: Fraction) -> dict[str, object]:
    return {
        "exact": f"{value.numerator}/{value.denominator}",
        "numerator": value.numerator,
        "denominator": value.denominator,
        "decimal": float(value),
    }


def compute() -> dict[str, object]:
    # Exact G127 metric witness: q=r=1 and sin(alpha)=4/5 gives the displayed
    # optical-tidal eigenvalues.  The point-vertex Jacobi determinant is
    # lambda^2[1-lambda^2 tr(T)/6+O(lambda^3)], unlike the radial lambda^2 control.
    tilted_tidal = [Fraction(8, 25), Fraction(4, 25)]
    tilted_trace = sum(tilted_tidal, Fraction(0))
    determinant_lambda4_coefficient = -tilted_trace / 6
    if tilted_trace != Fraction(12, 25) or determinant_lambda4_coefficient != Fraction(-2, 25):
        raise AssertionError("G127 local metric-Jacobi witness changed")

    # Q is a fixed survey-reference distribution on four observer cells.
    q = normalize([Fraction(1), Fraction(2), Fraction(3), Fraction(4)])

    # This positive response stands for the complete metric/source pushforward relative to Q.
    response = [Fraction(1), Fraction(2), Fraction(1), Fraction(3)]
    p = normalize([q_i * m_i for q_i, m_i in zip(q, response)])

    # One symmetric angular-separation-bin kernel on the four-cell control sky.
    kernel = [
        [Fraction(0), Fraction(1), Fraction(0), Fraction(1)],
        [Fraction(1), Fraction(0), Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(0), Fraction(1)],
        [Fraction(1), Fraction(0), Fraction(1), Fraction(0)],
    ]

    dd = bilinear(p, kernel, p)
    dr = bilinear(p, kernel, q)
    rr = bilinear(q, kernel, q)
    if rr <= 0:
        raise AssertionError("registered bin must have positive RR")
    ls = (dd - 2 * dr + rr) / rr
    mismatch = subtract(p, q)
    mismatch_form = bilinear(mismatch, kernel, mismatch) / rr
    if ls != mismatch_form or ls == 0:
        raise AssertionError("nonconstant-response witness failed")

    # A common radial multiplier cancels after probability normalization.
    constant_response = [Fraction(7)] * len(q)
    p_constant = normalize([q_i * m_i for q_i, m_i in zip(q, constant_response)])
    ls_constant = (
        bilinear(p_constant, kernel, p_constant)
        - 2 * bilinear(p_constant, kernel, q)
        + rr
    ) / rr
    if p_constant != q or ls_constant != 0:
        raise AssertionError("constant-response cancellation failed")

    # A reference constructed from the pushed intensity cancels the factorized response exactly.
    q_matched = p[:]
    rr_matched = bilinear(q_matched, kernel, q_matched)
    ls_matched = (
        bilinear(p, kernel, p)
        - 2 * bilinear(p, kernel, q_matched)
        + rr_matched
    ) / rr_matched
    if ls_matched != 0:
        raise AssertionError("matched-reference cancellation failed")

    # A small connected factorial-pair remainder is kept distinct from the intensity mismatch.
    v = [Fraction(1), Fraction(-1), Fraction(0), Fraction(0)]
    epsilon = Fraction(1, 1000)
    gamma = scale_matrix(epsilon, outer(v, v))
    pair_measure = add_matrix(outer(p, p), gamma)
    if any(value < 0 for row in pair_measure for value in row):
        raise AssertionError("connected control is not a nonnegative pair measure")
    if sum((sum(row, Fraction(0)) for row in pair_measure), Fraction(0)) != 1:
        raise AssertionError("connected pair measure is not normalized")
    dd_connected = matrix_pairing(kernel, pair_measure)
    ls_connected = (dd_connected - 2 * dr + rr) / rr
    connected_term = matrix_pairing(kernel, gamma) / rr
    if ls_connected != mismatch_form + connected_term or connected_term == 0:
        raise AssertionError("connected decomposition failed")

    # A finite single-image marking kernel proves product pushforward factorization exactly.
    # Every source event chooses exactly one observed output.  The calculation pushes forward
    # distinct-source factorial pairs; it does not cover several sibling images of one event.
    source = normalize([Fraction(2), Fraction(3)])
    branch_map = [
        [Fraction(1, 2), Fraction(0)],
        [Fraction(1, 2), Fraction(1, 3)],
        [Fraction(0), Fraction(1, 3)],
        [Fraction(0), Fraction(1, 3)],
    ]
    mapped = [
        sum((branch_map[i][a] * source[a] for a in range(2)), Fraction(0))
        for i in range(4)
    ]
    mapped_pair_direct = [
        [
            sum(
                (
                    branch_map[i][a]
                    * branch_map[j][b]
                    * source[a]
                    * source[b]
                    for a in range(2)
                    for b in range(2)
                ),
                Fraction(0),
            )
            for j in range(4)
        ]
        for i in range(4)
    ]
    if mapped_pair_direct != outer(mapped, mapped):
        raise AssertionError("factorized branch pushforward failed")

    # Exact counterexample to generic multibranch factorization.  A Poisson parent process of
    # intensity one produces one image in cell A and one in cell B for every event.  Distinct
    # parents still contribute nu_1 tensor nu_1, while each parent adds the ordered sibling pairs
    # A-B and B-A.  The parent is Poisson, but the observed image process is not factorized.
    parent_intensity = Fraction(1)
    sibling_nu_1 = [parent_intensity, parent_intensity]
    sibling_product = outer(sibling_nu_1, sibling_nu_1)
    sibling_measure = [
        [Fraction(0), parent_intensity],
        [parent_intensity, Fraction(0)],
    ]
    sibling_nu_2 = add_matrix(sibling_product, sibling_measure)
    if sibling_nu_2 != [
        [Fraction(1), Fraction(2)],
        [Fraction(2), Fraction(1)],
    ]:
        raise AssertionError("same-source sibling pair measure changed")
    if sibling_nu_2 == sibling_product:
        raise AssertionError("same-source sibling pairs were suppressed")

    # Gamma is defined from normalized measures.  Consequently the normalized sibling
    # contribution contains both Sigma_sib/nu_2(total) and the compensating normalization shift
    # relative to P tensor P.
    sibling_p = normalize(sibling_nu_1)
    sibling_nu_2_total = sum(
        (sum(row, Fraction(0)) for row in sibling_nu_2), Fraction(0)
    )
    sibling_bar_nu_2 = scale_matrix(Fraction(1, 1) / sibling_nu_2_total, sibling_nu_2)
    sibling_gamma = subtract_matrix(sibling_bar_nu_2, outer(sibling_p, sibling_p))
    expected_sibling_gamma = [
        [Fraction(-1, 12), Fraction(1, 12)],
        [Fraction(1, 12), Fraction(-1, 12)],
    ]
    if sibling_gamma != expected_sibling_gamma:
        raise AssertionError("normalized sibling contribution to Gamma changed")

    return {
        "audit": "G239_METRIC_REFERENCE_PROJECTED_POINT_PROCESS_OPERATOR",
        "landing": LANDING,
        "boss_outcomes_opened": False,
        "feature_or_scale_used": False,
        "profile_fit_performed": False,
        "source_status": "CHOSE_OBSERVATIONAL_HYPOTHESIS__HOMOGENEOUS_POISSON_PARENT_CONTROL",
        "metric_status": "DERIVED_CONDITIONAL_EVALUATOR_ON_SUPPLIED_HISTORY_QUERY_AND_BRANCHES",
        "reference_status": "OBSERVED_AND_CHOSE_SURVEY_FOOTPRINT_REFERENCE__NOT_PHYSICAL_SOURCE_LAW",
        "reference_projected_identity": (
            "w_K=<K,(P-Q)x(P-Q)>/<K,QxQ>+<K,Gamma>/<K,QxQ>"
        ),
        "metric_local_jacobi_liveness": {
            "source": "G127 q=r=1, cos(alpha)=3/5, sin(alpha)=4/5 exact witness",
            "radial_tidal_eigenvalues": [fraction_payload(Fraction(0)), fraction_payload(Fraction(0))],
            "tilted_tidal_eigenvalues": [fraction_payload(x) for x in tilted_tidal],
            "tilted_trace": fraction_payload(tilted_trace),
            "jacobi_determinant_lambda4_coefficient": fraction_payload(
                determinant_lambda4_coefficient
            ),
            "meaning": (
                "det(D_tilted)=lambda^2-(2/25)lambda^4+O(lambda^5), "
                "while det(D_radial)=lambda^2+O(lambda^5)"
            ),
        },
        "factorized_witness": {
            "q": [fraction_payload(x) for x in q],
            "metric_response": [fraction_payload(x) for x in response],
            "p": [fraction_payload(x) for x in p],
            "dd": fraction_payload(dd),
            "dr": fraction_payload(dr),
            "rr": fraction_payload(rr),
            "landy_szalay": fraction_payload(ls),
            "mismatch_form": fraction_payload(mismatch_form),
            "nonzero": ls != 0,
        },
        "cancellation_controls": {
            "constant_response_p_equals_q": p_constant == q,
            "constant_response_landy_szalay": fraction_payload(ls_constant),
            "matched_reference_landy_szalay": fraction_payload(ls_matched),
        },
        "connected_control": {
            "epsilon": fraction_payload(epsilon),
            "connected_term": fraction_payload(connected_term),
            "full_landy_szalay": fraction_payload(ls_connected),
            "decomposition_exact": ls_connected == mismatch_form + connected_term,
            "pair_measure_nonnegative": all(value >= 0 for row in pair_measure for value in row),
        },
        "branch_factorization": {
            "assumption": "ONE_OBSERVED_IMAGE_PER_SOURCE_EVENT__INDEPENDENT_SINGLE_BRANCH_MARK",
            "no_same_source_sibling_multiplicity": True,
            "source": [fraction_payload(x) for x in source],
            "mapped": [fraction_payload(x) for x in mapped],
            "direct_product_equals_product_pushforward": mapped_pair_direct == outer(mapped, mapped),
        },
        "sibling_image_control": {
            "parent_process": "POISSON_INTENSITY_ONE",
            "images_per_parent": "ONE_IN_A_AND_ONE_IN_B",
            "nu_1": [fraction_payload(x) for x in sibling_nu_1],
            "distinct_source_product": [
                [fraction_payload(x) for x in row] for row in sibling_product
            ],
            "raw_sibling_measure": [
                [fraction_payload(x) for x in row] for row in sibling_measure
            ],
            "nu_2": [[fraction_payload(x) for x in row] for row in sibling_nu_2],
            "raw_decomposition_exact": sibling_nu_2
            == add_matrix(sibling_product, sibling_measure),
            "factorization_false": sibling_nu_2 != sibling_product,
            "normalized_gamma": [
                [fraction_payload(x) for x in row] for row in sibling_gamma
            ],
            "normalized_gamma_nonzero": any(
                value != 0 for row in sibling_gamma for value in row
            ),
            "status": "POISSON_PARENT_CAN_GENERATE_CONNECTED_OBSERVED_SIBLING_PAIRS",
        },
        "open": [
            "continuous physical metric history",
            "observer/source incidence",
            "physical null-branch population and weights",
            "physical source one- and two-point measures",
            "native radiative transfer",
            "BOSS outcome comparison",
        ],
        "forbidden_inputs_absent": [
            "P1",
            "X_max",
            "Lambda-CDM distance",
            "BOSS curve value",
            "feature location",
            "fitted coefficient",
            "post-readout orchestra",
            "protected package",
        ],
    }


def main() -> None:
    result = compute()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    (ROOT / "DERIVATION_RESULT.json").write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()

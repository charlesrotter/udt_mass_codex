#!/usr/bin/env python3
"""Injected algebraic and semantic mutation catches for G221."""

from __future__ import annotations

import copy
import json

import sympy as sp


if not __debug__:
    raise RuntimeError("G221 evidence must run with Python assertions enabled; -O is forbidden")


def canonical_payload() -> dict[str, object]:
    N, A, beta = sp.Rational(2), sp.Rational(5), sp.Rational(1, 2)
    Q = sp.Matrix([[2, 1], [1, 3]])
    H = Q.T * Q
    st = sp.Matrix([sp.Rational(1, 3), sp.Rational(-1, 4)])
    sx = sp.Matrix([sp.Rational(2, 5), sp.Rational(1, 7)])
    px = sp.Rational(3, 2)
    pz = sp.Matrix([sp.Rational(4, 3), sp.Rational(-2, 5)])
    D = A**2 - N**2 * beta**2
    P2 = N**2 - (st.T * H * st)[0]
    Pi = px - (sx.T * pz)[0]
    q2 = (pz.T * H.inv() * pz)[0]
    R = sp.sqrt(Pi**2 + D * q2)
    p0_future = (-N * beta * Pi - A * R) / D
    p0_past = (-N * beta * Pi + A * R) / D
    pt = (st.T * pz)[0] + N * p0_future
    W = -pt / sp.sqrt(P2)
    return {
        "N": N,
        "A": A,
        "beta": beta,
        "Q": Q,
        "H": H,
        "st": st,
        "sx": sx,
        "px": px,
        "pz": pz,
        "D": D,
        "P2": P2,
        "Pi": Pi,
        "q2": q2,
        "R": R,
        "p0_future": p0_future,
        "p0_past": p0_past,
        "pt": pt,
        "W": W,
        "HJ_sign": -1,
        "endpoint_ratio_orientation": "W_A_over_W_B",
        "screen_covector_transform": "K_transpose",
        "affine_scaling": "both_endpoints",
        "null_query_typed": True,
        "full_pair_plane_constructed": False,
        "G176_independently_proved": False,
        "Jacobi_channel_separate": True,
        "strict_D_gate": True,
        "strict_P_gate": True,
    }


def valid(payload: dict[str, object]) -> bool:
    try:
        N, A, beta = payload["N"], payload["A"], payload["beta"]
        H, st, sx = payload["H"], payload["st"], payload["sx"]
        px, pz = payload["px"], payload["pz"]
        D = A**2 - N**2 * beta**2
        P2 = N**2 - (st.T * H * st)[0]
        Pi = px - (sx.T * pz)[0]
        q2 = (pz.T * H.inv() * pz)[0]
        R = sp.sqrt(Pi**2 + D * q2)
        p0f = (-N * beta * Pi - A * R) / D
        p0p = (-N * beta * Pi + A * R) / D
        pt = (st.T * pz)[0] + N * p0f
        W = -pt / sp.sqrt(P2)
        algebra = (
            sp.simplify(payload["D"] - D) == 0
            and sp.simplify(payload["P2"] - P2) == 0
            and sp.simplify(payload["Pi"] - Pi) == 0
            and sp.simplify(payload["q2"] - q2) == 0
            and sp.simplify(payload["R"] - R) == 0
            and sp.simplify(payload["p0_future"] - p0f) == 0
            and sp.simplify(payload["p0_past"] - p0p) == 0
            and sp.simplify(payload["pt"] - pt) == 0
            and sp.simplify(payload["W"] - W) == 0
            and bool(sp.N(p0f, 50) < 0 < sp.N(p0p, 50))
            and bool(sp.N(W, 50) > 0)
        )
        semantics = (
            payload["HJ_sign"] == -1
            and payload["endpoint_ratio_orientation"] == "W_A_over_W_B"
            and payload["screen_covector_transform"] == "K_transpose"
            and payload["affine_scaling"] == "both_endpoints"
            and payload["null_query_typed"] is True
            and payload["full_pair_plane_constructed"] is False
            and payload["G176_independently_proved"] is False
            and payload["Jacobi_channel_separate"] is True
            and payload["strict_D_gate"] is True
            and payload["strict_P_gate"] is True
            and D > 0
            and P2 > 0
        )
        return bool(algebra and semantics)
    except Exception:
        return False


def catches() -> dict[str, object]:
    base = canonical_payload()
    if not valid(base):
        raise RuntimeError("canonical G221 payload rejected")

    mutations = {
        "future_root_sign_flip": ("p0_future", base["p0_past"]),
        "past_root_sign_flip": ("p0_past", base["p0_future"]),
        "omit_time_mixing_from_observer_lapse": ("P2", base["N"] ** 2),
        "omit_longitudinal_mixing_from_Pi": ("Pi", base["px"]),
        "use_H_instead_of_H_inverse": ("q2", (base["pz"].T * base["H"] * base["pz"])[0]),
        "omit_time_mixing_energy_shift": ("pt", base["N"] * base["p0_future"]),
        "replace_full_R_with_absolute_Pi": ("R", sp.Abs(base["Pi"])),
        "divide_frequency_by_P2": ("W", -base["pt"] / base["P2"]),
        "reverse_Hamilton_Jacobi_sign": ("HJ_sign", 1),
        "invert_endpoint_clock_ratio": ("endpoint_ratio_orientation", "W_B_over_W_A"),
        "wrong_screen_covector_transform": ("screen_covector_transform", "K_inverse"),
        "one_endpoint_affine_rescaling": ("affine_scaling", "source_only"),
        "promote_null_to_universal_protocol": ("null_query_typed", False),
        "promote_clock_leg_to_full_pair_plane": ("full_pair_plane_constructed", True),
        "call_compatibility_independent_G176_proof": ("G176_independently_proved", True),
        "collapse_Jacobi_into_scalar_chord": ("Jacobi_channel_separate", False),
        "allow_D_zero_continuation": ("strict_D_gate", False),
        "allow_P_zero_continuation": ("strict_P_gate", False),
    }

    caught: dict[str, bool] = {}
    for name, (field, value) in mutations.items():
        mutant = copy.deepcopy(base)
        mutant[field] = value
        caught[name] = not valid(mutant)
    if not all(caught.values()):
        raise RuntimeError({name: value for name, value in caught.items() if not value})
    return {
        "canonical_pass": True,
        "injected_mutation_catches": len(caught),
        "catches": caught,
    }


if __name__ == "__main__":
    print(json.dumps(catches(), indent=2, sort_keys=True))

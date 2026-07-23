#!/usr/bin/env python3
"""Exact, CPU-only algebra for the Xmax dilation-asymptote correction."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
PREREG_COMMIT = "94c6ee3eae92cc67a8e3f370c98e93d75da4d4f8"
PARENT = "udt_invariant_xmax_asymptotic_boundary_audit_2026-07-23"
PARENT_MANIFEST_SHA256 = (
    "8798461fbd59891c1eff90c36311e38a29a3753dd4066d75360a813a859955c0"
)
MAXIMUM = (
    "XMAX_IS_OWNER_DEFINED_AS_THE_INVARIANT_POSITIONAL_SCALE_OF_THE_UDT_"
    "DILATION_ASYMPTOTE;THE_RECORDED_WRL_BRANCH_DERIVES_R_OVER_X_EQUALS_"
    "ONE_MINUS_EXP_MINUS_TWO_PHI_CONDITIONAL_ON_RESIDUAL_RECENTERING_AND_"
    "THE_ACCEPTED_WALL_REGULARITY_PACKAGE;PANTHEON_OBSERVATION_FAVORS_"
    "THAT_LINEAR_CEILING_OVER_THE_HYPERBOLIC_J1_DISPLAY_BUT_DOES_NOT_"
    "DERIVE_IT;GLOBAL_BRANCH_SELECTION_XMAX_VALUE_AND_NATIVE_MASS_REMAIN_OPEN"
)

SOURCE_HASHES = {
    "SIMPLE_METRIC_MACRO.md":
        "f0c045abf9810dc327d249d0df385cd7e8d6914eedfaf5b31c78d186eaa13d44",
    "simple_metric_xmax_POSTULATE.md":
        "35bb2a2d6d01cb48287e218902d087cf954e4c9eeda3142f865731742e8e681d",
    "simple_metric_c_analogy_MAP.md":
        "e080a56e068f420b8ecbd516cbfb8fa854a6aab6f071540c94fdde9114f3530c",
    "simple_metric_c_analogy_rederive_results.md":
        "f72ae6fc34fb17aea7792e122546a0b0dab8555d51aa15ec5457cecd028f7e8e",
    "simple_metric_elegance_SNe_character_results.md":
        "4d0712b32f6c34872135808501d4d9a9fe6cc5d011eaba5039a8d9be8641f00e",
    "simple_metric_SNe_shape_clue_results.md":
        "e460f07fca464315316c906f5580434adc9a4e6a23ee55e15363bef1f7507dbe",
    "simple_metric_SNe_shape_clue_out.json":
        "1a794998d4f6e6c60459e08ac02617aef0233f96962cb0df1165bddd51e81460",
    "simple_metric_pantheon_xmax_fit.py":
        "6118f4d6d5e53cd669fa2d889273e815efb9e6b1d1c7887d06ef914c0da65e01",
    "simple_metric_pantheon_xmax_fit_results.md":
        "c0ccac653a2fbc007256424e286e06dba35275efc05c6575546f5edb6da81b8e",
    "simple_metric_pantheon_xmax_fit_out.json":
        "26abb55b2afd958910feed55b025f8aa93860dc9ac2475a6c3ca35c1d2de68b9",
    "simple_metric_pantheon_xmax_fit_fullcov.py":
        "27e08872d55495d2b3d1922f4fe9141c65df1273f2e940b506ea01bbb537e038",
    "simple_metric_pantheon_xmax_fit_fullcov_out.json":
        "1b2ecade641fea438c55d6aef3324b83ee2d02abfe6b097b7256088f71b3d1d1",
    "sne_test_derived_law.py":
        "0ac392945475d0c9184b80c397d29a906dd33a232d0affdfe9e1ec003503920a",
    "sne_test_derived_n.py":
        "617f587ea93d346c50332db2666828017d54364df818ffa08da269a0a414fee0",
    "sne_native_background_n2.py":
        "5e96a98bc84961fded84ef04eb6a603fa370d45970f786098089729dd39e6c01",
    "simple_metric_hyperbolic_derive.md":
        "c5ab7f7e7a09784b59384c8f32d7b1462e86c94ece3757d0cb0411508df38e5f",
    "derive_xmax_boost.py":
        "c1c3898b41a0357e1323ecf7b420b3b17d37e59200a1aaf304937cca4a5412e9",
    "simple_metric_L_wall_regularity_closure_results.md":
        "0c68719277edb652fcb825d225f02cb8bb25f16a36efe6b40f3b1d9a5147b6b8",
    "simple_metric_L_wall_regularity_closure_out.json":
        "cf756f06f15010133bb370c442a025b1d9a75d46188c1d023558a96fc9982f13",
    "simple_metric_L_native_optical_derive_results.md":
        "3da5b6a53d77c5433348daa55f9d06cff33f8d6809adf84e55c76a5dba2474e1",
    "asymptotic_boundary_lineage_audit_2026-07-19/AUDIT_REPORT.md":
        "bf10dc2d525e26723ee2eb2eaacf368ad8546e76b0a8d3ba0d3baa0b9639d11d",
    "CANON.md":
        "5d99c0ba09fcee0429a34ac6b3dda4faff489b7d214b622fcbd286deb3785314",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md":
        "af6bcc49535fd9cf4c8a60e997935d10619f2d52d146482ee40ad9d968f76810",
}


class ContractError(RuntimeError):
    """Raised when a source, algebra, or status premise is violated."""


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for piece in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(piece)
    return value.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def source_checks() -> int:
    for relative, expected in SOURCE_HASHES.items():
        path = ROOT / relative
        require(path.is_file(), f"missing source: {relative}")
        require(digest(path) == expected, f"source drift: {relative}")

    macro = (ROOT / "SIMPLE_METRIC_MACRO.md").read_text(encoding="utf-8")
    wrl = (
        ROOT / "simple_metric_L_wall_regularity_closure_results.md"
    ).read_text(encoding="utf-8")
    hyperbolic = (
        ROOT / "simple_metric_hyperbolic_derive.md"
    ).read_text(encoding="utf-8")
    sne = (
        ROOT / "simple_metric_SNe_shape_clue_results.md"
    ).read_text(encoding="utf-8")
    require("g_{tt}=-e^{-2\\phi}c^2" in macro, "metric lapse missing")
    require(
        "Dynamical field" in macro
        and "**\\(\\phi(r)\\) only**" in macro
        and "does \\(\\phi(r)\\) give" in macro,
        "metric leaves the profile as a field question",
    )
    require("A=1-r/X" in wrl, "WR-L profile missing")
    require("not bare R1–R3 alone" in wrl, "WR-L premise caveat missing")
    require(
        "does not" in hyperbolic
        and "by itself name a coordinate" in hyperbolic,
        "hyperbolic metric-alone caveat missing",
    )
    require("SNe as clue" in sne, "SNe observation caveat missing")
    return len(SOURCE_HASHES)


def exact_profile_checks() -> dict[str, object]:
    witnesses = []
    for q in (Fraction(1, 2), Fraction(1, 3), Fraction(2, 3)):
        # q=e^-phi; A=q^2 on the reciprocal metric.
        lapse = q * q
        coordinate_fraction = 1 - lapse
        proper_fraction = 1 - q
        projective_display = (1 - lapse) / (1 + lapse)
        one_plus_z = 1 / q
        z = one_plus_z - 1
        luminosity_over_x = one_plus_z * one_plus_z * coordinate_fraction
        require(
            luminosity_over_x == z * (z + 2),
            "WR-L full-light identity failed",
        )
        require(
            coordinate_fraction != projective_display,
            "WR-L coordinate and projective display conflated",
        )
        witnesses.append(
            {
                "q_exp_minus_phi": str(q),
                "A": str(lapse),
                "r_over_X": str(coordinate_fraction),
                "proper_over_2X": str(proper_fraction),
                "projective_tanh": str(projective_display),
                "z": str(z),
                "dL_over_X": str(luminosity_over_x),
            }
        )
    return {
        "metric_identity": "A=exp(-2phi)",
        "wrl_profile": "r/X=1-exp(-2phi)",
        "inverse_profile": "phi=-log(1-r/X)/2",
        "clock_factor": "exp(-phi)=sqrt(1-r/X)",
        "asymptote": {
            "phi": "+infinity",
            "r_over_X": "1 from below",
            "A": "0 from above",
            "clock_factor": "0 from above",
        },
        "full_light_identity": "dL/X=z(z+2)",
        "witnesses": witnesses,
    }


def wall_selector_checks() -> dict[str, object]:
    # Exact exponent logic from the preregistered WR-L family A=epsilon^alpha.
    bands = [
        {
            "range": "alpha<1",
            "infinite_optical": False,
            "finite_proper": True,
            "finite_wall_second_derivative": "NOT_SELECTOR_BAND",
        },
        {
            "range": "alpha=1",
            "infinite_optical": True,
            "finite_proper": True,
            "finite_wall_second_derivative": True,
        },
        {
            "range": "1<alpha<2",
            "infinite_optical": True,
            "finite_proper": True,
            "finite_wall_second_derivative": False,
        },
        {
            "range": "alpha=2",
            "infinite_optical": True,
            "finite_proper": False,
            "finite_wall_second_derivative": True,
        },
        {
            "range": "alpha>2",
            "infinite_optical": True,
            "finite_proper": False,
            "finite_wall_second_derivative": True,
        },
    ]
    survivors = [
        row["range"]
        for row in bands
        if row["infinite_optical"]
        and row["finite_proper"]
        and row["finite_wall_second_derivative"] is True
    ]
    require(survivors == ["alpha=1"], "WR-L selector not unique in its band")
    return {
        "family": "A=(1-r/X)^alpha",
        "premises": [
            "residual composition and affine areal recentering",
            "finite proper reach",
            "infinite optical reach",
            "finite wall angular-curvature readout",
        ],
        "bands": bands,
        "survivor": "alpha=1",
        "status": "DERIVED_CONDITIONAL_WRL",
        "not_status": "DERIVED_FROM_BARE_LINE_ELEMENT",
    }


def sne_checks() -> dict[str, object]:
    observed = json.loads(
        (ROOT / "simple_metric_SNe_shape_clue_out.json").read_text(
            encoding="utf-8"
        )
    )
    named = {row["name"]: row for row in observed["named"]}
    linear = named["linear_ceiling p=1"]
    hyperbolic = named["hyp_J1 (elegant kinematic)"]
    require(observed["N"] == 1580, "SNe count drift")
    require(observed["best_power_p"]["p"] == 1.0, "power minimum drift")
    require(
        abs(linear["chi2_dof"] - 0.9098574003059215) < 1e-15,
        "linear-ceiling score drift",
    )
    require(
        abs(hyperbolic["chi2_dof"] - 2.166501637078457) < 1e-15,
        "hyperbolic score drift",
    )
    return {
        "sample_count": 1580,
        "linear_ceiling_chi2_dof": linear["chi2_dof"],
        "linear_ceiling_rms_mag": linear["rms"],
        "hyperbolic_J1_chi2_dof": hyperbolic["chi2_dof"],
        "hyperbolic_J1_rms_mag": hyperbolic["rms"],
        "best_scanned_power": observed["best_power_p"]["p"],
        "epistemic_status": "OBSERVED_SHAPE_CONTRAST",
        "derives_profile": False,
    }


def status_contract(overrides: dict[str, object] | None = None) -> None:
    state: dict[str, object] = {
        "xmax_owner": "OWNER_WORKING_POSTULATE",
        "wrl_profile": "DERIVED_CONDITIONAL_WRL",
        "bare_metric_profile": "OPEN",
        "sne_role": "OBSERVED_NOT_DERIVATION",
        "tanh_role": "DERIVED_CONDITIONAL_PROJECTIVE",
        "native_mass": "WORKING_OPEN",
        "global_wrl_equals_xmax": "OPEN",
        "xmax_value": "OPEN",
        "observer_limit": "OWNER_LOCKED_CONDITIONAL_CONSISTENCY",
        "angular_lambda": "OPEN",
        "c_g_determine_xmax": False,
    }
    if overrides:
        state.update(overrides)
    require(
        state["xmax_owner"] == "OWNER_WORKING_POSTULATE",
        "downstream readout cannot define Xmax",
    )
    require(
        state["wrl_profile"] == "DERIVED_CONDITIONAL_WRL",
        "WR-L status must retain its selector premises",
    )
    require(state["bare_metric_profile"] == "OPEN", "bare metric overclaim")
    require(
        state["sne_role"] == "OBSERVED_NOT_DERIVATION",
        "SNe fit promoted into a derivation",
    )
    require(
        state["tanh_role"] == "DERIVED_CONDITIONAL_PROJECTIVE",
        "tanh promoted beyond its projective premise",
    )
    require(state["native_mass"] == "WORKING_OPEN", "native mass overclaim")
    require(state["global_wrl_equals_xmax"] == "OPEN", "global branch overclaim")
    require(state["xmax_value"] == "OPEN", "Xmax value overclaim")
    require(
        state["observer_limit"] == "OWNER_LOCKED_CONDITIONAL_CONSISTENCY",
        "observer coordinates confused with invariant limit",
    )
    require(state["angular_lambda"] == "OPEN", "angular lambda overclaim")
    require(state["c_g_determine_xmax"] is False, "dimensional closure overclaim")


def catch_proofs() -> list[dict[str, str]]:
    mutations = [
        ("C01", {"xmax_owner": "WRL_PROPER_READOUT"}),
        ("C02", {"wrl_profile": "DERIVED_FROM_BARE_METRIC"}),
        ("C03", {"bare_metric_profile": "DERIVED"}),
        ("C04", {"sne_role": "DERIVES_PROFILE"}),
        ("C05", {"tanh_role": "DERIVED_FROM_INVARIANT_BOUND_ALONE"}),
        ("C06", {"native_mass": "DERIVED"}),
        ("C07", {"global_wrl_equals_xmax": "DERIVED"}),
        ("C08", {"xmax_value": "PANTHEON_DERIVED"}),
        ("C09", {"observer_limit": "IDENTICAL_COORDINATES"}),
        ("C10", {"angular_lambda": "DERIVED_EQUALS_ONE"}),
        ("C11", {"c_g_determine_xmax": True}),
    ]
    results = []
    for catch_id, mutation in mutations:
        try:
            status_contract(mutation)
        except ContractError as error:
            results.append(
                {
                    "catch_id": catch_id,
                    "result": "PASS_REJECTED",
                    "message": str(error),
                }
            )
        else:
            raise ContractError(f"mutation survived: {catch_id}")
    require(len(results) == 11, "catch-proof count")
    return results


def build_result() -> dict[str, object]:
    sources = source_checks()
    status_contract()
    profile = exact_profile_checks()
    wall = wall_selector_checks()
    sne = sne_checks()
    catches = catch_proofs()
    require(
        digest(ROOT / PARENT / "MANIFEST.sha256") == PARENT_MANIFEST_SHA256,
        "frozen parent manifest drift",
    )
    return {
        "schema": "udt-xmax-dilation-asymptote-correction-1.0",
        "result": "PASS",
        "grade": "VERIFIED-WITH-CAVEATS",
        "preregistration_commit": PREREG_COMMIT,
        "parent_package": PARENT,
        "parent_manifest_sha256": PARENT_MANIFEST_SHA256,
        "parent_package_unchanged": True,
        "source_hash_checks": sources,
        "profile": profile,
        "wrl_selector": wall,
        "sne": sne,
        "catch_count": len(catches),
        "catch_pass_count": len(catches),
        "maximum_conclusion": MAXIMUM,
        "corrections": {
            "xmax_semantics":
                "OWNER_DEFINED_INVARIANT_POSITIONAL_DILATION_ASYMPTOTE",
            "readouts": "DOWNSTREAM_NOT_DEFINITIONS_OF_XMAX",
            "strongest_profile":
                "WRL_DERIVED_CONDITIONAL_R_OVER_X_EQUALS_ONE_MINUS_EXP_MINUS_TWO_PHI",
            "hyperbolic_tanh":
                "CONDITIONAL_PROJECTIVE_DISPLAY_NOT_NATIVE_POSITION_LAW",
            "mass_dilation": "WORKING_OPEN",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args()
    result = build_result()
    print(
        json.dumps(
            result,
            indent=None if args.compact else 2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

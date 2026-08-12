#!/usr/bin/env python3
"""Derive the preregistered G85 mixed time-live completion archetype atlas."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
G75 = ROOT / "udt_cmb_G75_center_regular_axial_profile_family_2026-08-11/PROFILE_ATLAS.tsv"
G84 = ROOT / "udt_cmb_G84_am_global_completion_pair_diameter_audit_2026-08-12/PROFILE_COMPLETION_ATLAS.tsv"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def write_tsv(path: Path, records: list[dict[str, object]]) -> None:
    assert records
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)


def verify_sources() -> int:
    rows = read_tsv(HERE / "SOURCE_MANIFEST.tsv")
    assert len(rows) == len({row["path"] for row in rows}) == 11
    for row in rows:
        path = ROOT / row["path"]
        assert path.is_file() and digest(path) == row["sha256"], path
    return len(rows)


def exact_seam_algebra() -> dict[str, str]:
    u, b, h, D, z = sp.symbols("u b h D z", real=True)
    C = D * z
    H = h * z
    metric = sp.Matrix([
        [u, b, 0, H],
        [b, 4, 0, 0],
        [0, 0, D, 0],
        [H, 0, 0, C],
    ])
    determinant = sp.factor(metric.det())
    expected = sp.factor(D * ((4 * u - b**2) * C - 4 * H**2))
    assert sp.simplify(determinant - expected) == 0
    spatial = sp.diag(4, D, C)
    temporal_cross = sp.Matrix([b, 0, H])
    schur = sp.factor(u - (temporal_cross.T * spatial.inv() * temporal_cross)[0])
    assert sp.simplify(schur - (u - b**2 / 4 - h**2 * z / D)) == 0
    induced = metric.extract([0, 2, 3], [0, 2, 3])
    induced_det = sp.factor(induced.det())
    assert sp.simplify(induced_det - D * (u * C - H**2)) == 0
    axis_gate = sp.det(sp.Matrix([[u, b], [b, 4]]))
    assert axis_gate == 4 * u - b**2
    return {
        "metric_determinant": sp.sstr(determinant),
        "time_schur_complement": sp.sstr(schur),
        "axis_clock_radial_determinant": sp.sstr(axis_gate),
        "induced_seam_determinant": sp.sstr(induced_det),
        "regular_lorentz_axis_gate": "4*u_H-b_H**2<0",
        "uniform_null_gate_with_u_H_zero": "h_H=0",
    }


def frozen_profiles() -> list[dict[str, object]]:
    s = sp.symbols("s", real=True)
    g75 = {row["profile_id"]: row for row in read_tsv(G75) if row["lapse_name"] == "AM"}
    g84 = read_tsv(G84)
    assert len(g75) == len(g84) == 197
    output: list[dict[str, object]] = []
    for row in g84:
        if row["profile_id"] == "G75_F01_AM":
            continue
        source = g75[row["profile_id"]]
        q = sp.Poly(sp.sympify(source["q_of_s"], locals={"s": s}), s).as_expr()
        q4 = sp.factor(q.subs(s, 4))
        h4 = sp.factor(4 * q4)
        assert q4 != 0
        assert sp.simplify(q4 - sp.sympify(row["q_at_s_4_exact"])) == 0
        assert sp.simplify(h4 - sp.sympify(row["h_at_x_2_exact"])) == 0
        output.append({
            "profile_id": row["profile_id"],
            "shape_id": row["shape_id"],
            "amplitude": row["amplitude"],
            "behavior_class": source["behavior_class"],
            "q_of_s": sp.sstr(q),
            "q_at_4_exact": sp.sstr(q4),
            "h_H_original_exact": sp.sstr(h4),
        })
    assert len(output) == len({str(row["profile_id"]) for row in output}) == 196
    return output


def channel_atlas() -> list[dict[str, object]]:
    return [
        {
            "channel_case": "C01_STATIONARY_NONZERO_MIX",
            "u_H": "0", "b_H": "0", "h_H": "nonzero",
            "axis_gate": "0", "full_metric": "POINTWISE_DEGENERATE_AT_AXIAL_FIXED_SET",
            "seam_type": "TIMELIKE_OFF_AXIS__NULL_DEGENERATE_ON_AXIS",
            "scope": "exact G84 stationary polynomial seam germ",
        },
        {
            "channel_case": "C02_DERIVATIVE_ONLY_MIXING",
            "u_H": "0", "b_H": "0", "h_H": "nonzero_function_of_time",
            "axis_gate": "0", "full_metric": "POINTWISE_DEGENERATE_AT_EACH_TIME",
            "seam_type": "TIME_DERIVATIVES_DO_NOT_CHANGE_RANK",
            "scope": "mixing-only time-live chart",
        },
        {
            "channel_case": "C03_NONZERO_RADIAL_SHIFT",
            "u_H": "0", "b_H": "nonzero", "h_H": "nonzero",
            "axis_gate": "-b_H**2<0", "full_metric": "REGULAR_LORENTZ",
            "seam_type": "TIMELIKE_OFF_AXIS__NULL_ON_AXIAL_SUBSET",
            "scope": "global R_times_S3 witness when shift gate is smooth",
        },
        {
            "channel_case": "C04_NEGATIVE_LAPSE_LIFT",
            "u_H": "negative", "b_H": "0", "h_H": "nonzero",
            "axis_gate": "4*u_H<0", "full_metric": "REGULAR_LORENTZ",
            "seam_type": "TIMELIKE_EVERYWHERE",
            "scope": "global R_times_S3 witness when lift gate is smooth",
        },
        {
            "channel_case": "C05_TAPER_PLUS_SHIFT",
            "u_H": "0", "b_H": "nonzero", "h_H": "0",
            "axis_gate": "-b_H**2<0", "full_metric": "REGULAR_LORENTZ",
            "seam_type": "UNIFORMLY_NULL",
            "scope": "global R_times_S3 witness",
        },
        {
            "channel_case": "C06_TAPER_ORDER_A_ZERO_SHIFT",
            "u_H": "0", "b_H": "0", "h_H": "A*h_tilde",
            "axis_gate": "static_chart_zero", "full_metric": "SMOOTH_LOCAL_BIFURCATE_EXTENSION",
            "seam_type": "UNIFORMLY_NULL",
            "scope": "Kruskal_local; h*dτ=(h_tilde/4)*(U*dV-V*dU)",
        },
        {
            "channel_case": "C07_SHIFT_ZERO_CROSSING",
            "u_H": "0", "b_H": "0_at_t0", "h_H": "nonzero",
            "axis_gate": "0_at_t0", "full_metric": "DEGENERATE_AT_T0",
            "seam_type": "REGULARITY_NOT_UNIFORM_IN_TIME",
            "scope": "hostile boundary of C03",
        },
        {
            "channel_case": "C08_GENERAL_AXIS_GATE",
            "u_H": "free", "b_H": "free", "h_H": "irrelevant_on_axis",
            "axis_gate": "4*u_H-b_H**2", "full_metric": "REGULAR_LORENTZ_IFF_GATE_NEGATIVE",
            "seam_type": "requires induced-metric test",
            "scope": "declared positive radial coefficient 4",
        },
    ]


def archetype_rows(profiles: list[dict[str, object]]) -> list[dict[str, object]]:
    definitions = {
        "A01_PRESERVE_STATIONARY_GERM": (
            "0", "0", "h_H_original!=0", "POINTWISE_DEGENERATE",
            "none", "original G84 stationary-axis obstruction retained",
        ),
        "A02_MIXING_ONLY_TIMELIVE": (
            "0", "0", "h_H(t)!=0", "POINTWISE_DEGENERATE",
            "h time-live only", "time derivatives cannot change seam rank",
        ),
        "A03_RADIAL_SHIFT_TIMELIVE": (
            "0", "b_H(t)!=0", "h_H(t)!=0", "CONDITIONAL_ON_NONVANISHING_SHIFT",
            "b=B*w(chi)*(1+eps*sin(omega*tau)); B>0 and abs(eps)<1",
            "regular Lorentz global witness; seam timelike off-axis and null on axial subset",
        ),
        "A04_LAPSE_LIFT_TIMELIVE": (
            "u_H(t)<0", "0", "h_H(t)!=0", "REGULAR_LORENTZ_NONNULL_SEAM",
            "u=-A-L*w(chi)*(1+eps*sin(omega*tau)); L>0 and abs(eps)<1",
            "regular Lorentz global witness; seam timelike and lapse asymptote removed",
        ),
        "A05_MIXING_TAPER_BEFORE_SEAM": (
            "0", "zero_or_nonzero", "h=A*h_tilde near seam", "REGULAR_LORENTZ_UNIFORM_NULL_SEAM",
            "C-infinity gate equals original h on cell and A*h_tilde near seam",
            "zero-shift local bifurcate or nonzero-shift global witness; mere h_H=0 is insufficient",
        ),
    }
    output: list[dict[str, object]] = []
    for profile in profiles:
        for archetype, values in definitions.items():
            u_h, b_h, h_h, classification, witness, detail = values
            output.append({
                **profile,
                "archetype_id": archetype,
                "u_H_condition": u_h,
                "b_H_condition": b_h,
                "h_H_condition": h_h,
                "classification": classification,
                "constructive_witness": witness,
                "seam_detail": detail,
                "frozen_cell_preserved": "true",
                "physical_status": "CONTROL_CLASSIFICATION_NOT_SELECTED_PHYSICS",
            })
    assert len(output) == 980
    assert len({(row["profile_id"], row["archetype_id"]) for row in output}) == 980
    return output


def main() -> None:
    sources = verify_sources()
    algebra = exact_seam_algebra()
    profiles = frozen_profiles()
    channels = channel_atlas()
    atlas = archetype_rows(profiles)
    write_tsv(HERE / "SEAM_CHANNEL_ATLAS.tsv", channels)
    write_tsv(HERE / "PROFILE_ARCHETYPE_ATLAS.tsv", atlas)
    class_counts = Counter(str(row["classification"]) for row in atlas)
    behavior_counts = Counter(str(row["behavior_class"]) for row in profiles)
    sign_counts = Counter("positive" if sp.sympify(row["q_at_4_exact"]) > 0 else "negative" for row in profiles)
    result = {
        "schema": "udt-cmb-g85-mixed-timelive-completion-v1",
        "status": "PASS",
        "landing": "COMPLETE_METRIC_CHANNELS_ADMIT_MULTIPLE_KINEMATIC_COMPLETION_CLASSES__NO_NATIVE_HISTORY_SELECTED",
        "maximum_conclusion": "BOUNDED_KINEMATIC_TIME_LIVE_COMPLETION_ARCHETYPE_ATLAS_ON_THE_G84_CANDIDATE",
        "source_manifest_rows": sources,
        "mixed_profile_rows": len(profiles),
        "archetypes_per_profile": 5,
        "profile_archetype_rows": len(atlas),
        "unique_profile_archetype_pairs": len({(row["profile_id"], row["archetype_id"]) for row in atlas}),
        "classification_counts": dict(sorted(class_counts.items())),
        "profile_behavior_counts": dict(sorted(behavior_counts.items())),
        "q4_sign_counts": dict(sorted(sign_counts.items())),
        "seam_channel_rows": len(channels),
        "exact_algebra": algebra,
        "physical_profile_selected": False,
        "physical_topology_selected": False,
        "physical_Xmax_selected": False,
        "native_dynamics_selected": False,
        "all_completion_functions_status": "FREE_AND_EXPLORED",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

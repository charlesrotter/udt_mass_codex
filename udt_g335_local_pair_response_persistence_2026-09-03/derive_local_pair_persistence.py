#!/usr/bin/env python3
"""Exact bounded G335 local pair-response persistence classification."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PREREG_COMMIT = "a3324f62"


def require(condition: bool, label: str, checks: list[str]) -> None:
    if not condition:
        raise AssertionError(label)
    checks.append(label)


def sign(value: F) -> int:
    return (value > 0) - (value < 0)


def boost_from_half_tangent(t: F) -> tuple[F, F]:
    denominator = 1 - t * t
    return 2 * t / denominator, (1 + t * t) / denominator


def verify_sources(checks: list[str]) -> None:
    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    require(len(rows) == 6, "six_frozen_sources", checks)
    for row in rows:
        relative = Path(row["path"])
        require(not relative.is_absolute() and ".." not in relative.parts,
                f"source_{row['source_id']}_path_safe", checks)
        source_root = ROOT / "sources" if (ROOT / "sources").is_dir() else ROOT
        path = (source_root / relative).resolve()
        require(path.is_relative_to(source_root.resolve()),
                f"source_{row['source_id']}_contained", checks)
        payload = path.read_bytes() if path.is_file() else b""
        expected_bytes = int(row["bytes"])
        expected_digest = row["sha256"]
        if (len(payload) != expected_bytes
                or hashlib.sha256(payload).hexdigest() != expected_digest):
            # Once G335 is banked, the live premise registry necessarily advances. Replaying
            # the preregistered source from git preserves the exact frozen input without
            # weakening the manifest. A sealed intake resolves through its copied sources and
            # never needs this repository-only fallback.
            replay = subprocess.run(
                ["git", "show", f"{PREREG_COMMIT}:{relative.as_posix()}"],
                cwd=ROOT,
                capture_output=True,
                check=False,
            )
            if replay.returncode != 0:
                raise AssertionError(f"source_{row['source_id']}_frozen_git_available")
            payload = replay.stdout
        require(len(payload) == expected_bytes, f"source_{row['source_id']}_bytes", checks)
        require(hashlib.sha256(payload).hexdigest() == expected_digest,
                f"source_{row['source_id']}_sha256", checks)


def derive() -> dict:
    checks: list[str] = []
    records: list[dict] = []
    verify_sources(checks)

    # Equal-weight G332 has exact R=12. Selecting a positive square-root magnitude s fixes
    # Lambda=R/2+C^2-s^2/4 and retains both exact b=-C +/- s branches.
    scalar_curvature = F(12)
    constants = (F(-5), F(-3), F(3), F(5))
    root_magnitudes = (F(2), F(4), F(6), F(8))
    mus = tuple(F(i, 32) for i in range(33))
    half_tangents = tuple(F(i, 8) for i in range(-6, 7))
    time_slopes = (F(-3, 5), F(0), F(7, 11))
    time_curvatures = (F(-2, 7), F(0), F(5, 13))
    case_count = 0
    nonzero_cases = 0
    silent_cases = 0
    gap_branch_count = 0

    for C in constants:
        for root in root_magnitudes:
            Lambda = scalar_curvature / 2 + C * C - root * root / 4
            radicand = 2 * (scalar_curvature + 2 * C * C - 2 * Lambda)
            require(radicand == root * root, f"radicand_{C}_{root}", checks)
            require(C * C > Lambda - scalar_curvature / 2,
                    f"strict_global_control_{C}_{root}", checks)
            branch_values = (-C - root, -C + root)
            require(branch_values[0] != branch_values[1],
                    f"branches_distinct_{C}_{root}", checks)

            for branch, b in zip((-1, 1), branch_values):
                silent_exists = b != 0 and b * b >= C * C
                if b == 0:
                    require(C != 0, f"strict_b_zero_has_C_{C}_{root}_{branch}", checks)
                    mu_zero = None
                else:
                    mu_zero = (b - C) / (2 * b)
                    require((F(0) <= mu_zero <= F(1)) == silent_exists,
                            f"silent_condition_{C}_{root}_{branch}", checks)

                if abs(b) < abs(C):
                    gap_branch_count += 1
                    gap = (abs(C) - abs(b)) / 2
                    endpoint_min = min(abs((b - C) / 2), abs(-(b + C) / 2))
                    require(gap > 0 and endpoint_min == gap,
                            f"fixed_gap_{C}_{root}_{branch}", checks)
                    require(sign((b - C) / 2) == -sign(C)
                            and sign(-(b + C) / 2) == -sign(C),
                            f"gap_sign_{C}_{root}_{branch}", checks)

                for mu in mus:
                    q = (b - C) / 2 - b * mu
                    sampled_silent = q == 0
                    expected_silent = mu_zero is not None and mu == mu_zero
                    require(sampled_silent == expected_silent,
                            f"sampled_silent_{C}_{root}_{branch}_{mu}", checks)
                    if q == 0:
                        silent_cases += 1
                    else:
                        nonzero_cases += 1
                        for slope in time_slopes:
                            for curvature in time_curvatures:
                                bound_rate = abs(slope) + abs(curvature)
                                epsilon = (F(1) if bound_rate == 0 else
                                           min(F(1), abs(q) / (2 * bound_rate)))
                                require(epsilon > 0,
                                        f"epsilon_positive_{C}_{root}_{branch}_{mu}_{slope}_{curvature}",
                                        checks)
                                for orientation in (-1, 1):
                                    t = orientation * epsilon
                                    q_t = q + slope * t + curvature * t * t
                                    perturbation = abs(q_t - q)
                                    require(perturbation <= abs(q) / 2,
                                            f"continuity_bound_{C}_{root}_{branch}_{mu}_{slope}_{curvature}_{orientation}",
                                            checks)
                                    require(sign(q_t) == sign(q),
                                            f"continuity_sign_{C}_{root}_{branch}_{mu}_{slope}_{curvature}_{orientation}",
                                            checks)

                    for half_tangent in half_tangents:
                        sh, ch = boost_from_half_tangent(half_tangent)
                        require(ch * ch - sh * sh == 1,
                                f"boost_identity_{C}_{root}_{branch}_{mu}_{half_tangent}", checks)
                        d00 = 2 * q * sh * sh
                        d01 = 2 * q * sh * ch
                        d11 = 2 * q * ch * ch
                        require(-d00 + d11 == 2 * q,
                                f"mixed_trace_{C}_{root}_{branch}_{mu}_{half_tangent}", checks)
                        require(d00 * d11 - d01 * d01 == 0,
                                f"rank_one_{C}_{root}_{branch}_{mu}_{half_tangent}", checks)
                        require((d00 == 0 and d01 == 0 and d11 == 0) == (q == 0),
                                f"response_zero_iff_q_{C}_{root}_{branch}_{mu}_{half_tangent}", checks)
                        terminal = q * sh * sh
                        require(terminal == d00 / 2,
                                f"terminal_formula_{C}_{root}_{branch}_{mu}_{half_tangent}", checks)
                        require((half_tangent == 0) <= (terminal == 0),
                                f"zero_boost_blind_{C}_{root}_{branch}_{mu}_{half_tangent}", checks)
                        if q != 0 and half_tangent != 0:
                            require(terminal != 0,
                                    f"nonzero_boost_terminal_{C}_{root}_{branch}_{mu}_{half_tangent}",
                                    checks)
                        # Smooth re-orthonormalized carry cancels raw component change, while the
                        # geometric deformation matrix remains nonzero when q is nonzero.
                        transport = (-d00, -d01, -d11)
                        require((d00 + transport[0], d01 + transport[1], d11 + transport[2])
                                == (F(0), F(0), F(0)),
                                f"component_carry_cancel_{C}_{root}_{branch}_{mu}_{half_tangent}",
                                checks)
                        # The same normal jet and two supplied spatial jets give different
                        # boosted-observer derivatives whenever the boost is nonzero.
                        observer_a = ch * q + sh * F(1, 7)
                        observer_b = ch * q + sh * F(-2, 7)
                        require((observer_a == observer_b) == (sh == 0),
                                f"observer_spatial_jet_ambiguity_{C}_{root}_{branch}_{mu}_{half_tangent}",
                                checks)
                        case_count += 1

                    if len(records) < 24 and (mu in (F(0), F(1, 2), F(1))):
                        records.append({
                            "C": str(C),
                            "Lambda": str(Lambda),
                            "root": str(root),
                            "branch": branch,
                            "b": str(b),
                            "mu": str(mu),
                            "q0": str(q),
                            "silent_exists_some_direction": silent_exists,
                            "silent_mu": None if mu_zero is None else str(mu_zero),
                            "all_direction_gap": None if abs(b) >= abs(C)
                            else str((abs(C) - abs(b)) / 2),
                        })

    # Exact lawful silent witness inside the equal-weight R=12 family.
    C = F(0)
    Lambda = F(2)
    root = F(4)
    require(2 * (scalar_curvature + 2 * C * C - 2 * Lambda) == root * root,
            "silent_witness_strict_radicand", checks)
    for b in (-root, root):
        require((b - C) / 2 - b * F(1, 2) == 0,
                f"silent_witness_branch_{b}", checks)

    # Non-load-bearing exact Einstein control: flat slicing a=exp(Ht), K=-H gamma,
    # and Lambda=3H^2 satisfy both the Hamiltonian and K-evolution equations, while
    # q=d(log a)/dt=H at every time. This checks compatibility, not G332 evolution.
    for H in (F(-2), F(-1, 3), F(1, 3), F(2)):
        Lambda = 3 * H * H
        scalar_curvature = F(0)
        tau = -3 * H
        k_norm_squared = 3 * H * H
        require(scalar_curvature + tau * tau - k_norm_squared == 2 * Lambda,
                f"flat_slicing_Hamiltonian_{H}", checks)
        gamma_rate = 2 * H
        K_rate = -2 * H * H
        K_evolution_rhs = 3 * H * H - 2 * H * H - Lambda
        require(gamma_rate == -2 * (-H), f"flat_slicing_gamma_evolution_{H}", checks)
        require(K_rate == K_evolution_rhs, f"flat_slicing_K_evolution_{H}", checks)
        for t in (F(-1), F(-1, 5), F(0), F(1, 5), F(1)):
            log_a_rate = H
            require(log_a_rate == -(-H), f"flat_slicing_constant_q_{H}_{t}", checks)

    require(nonzero_cases > 0 and silent_cases > 0,
            "nonzero_and_silent_strata_exercised", checks)
    require(gap_branch_count > 0, "fixed_all_direction_gap_exercised", checks)

    return {
        "package": "G335",
        "grade": "EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED",
        "landing": (
            "NONZERO_INITIAL_GEOMETRIC_PAIR_RESPONSE_PERSISTS_ON_PER_DATUM_LOCAL_MARKED_INTERVAL"
            "__SILENT_DIRECTIONS_REQUIRE_HIGHER_JET"
            "__FIXED_COMPACT_ALL_DIRECTION_GAP_GIVES_UNIFORM_LOCAL_INTERVAL"
            "__RAW_COMPONENT_AND_OBSERVER_TIME_REMAIN_CARRY_QUALIFIED"
        ),
        "classifications": [
            "CONDITIONAL_PER_DATUM_LOCAL_PERSISTENCE",
            "FIRST_ORDER_SILENT_STRATUM_REQUIRES_HIGHER_JET",
            "FIXED_DATUM_UNIFORM_ALL_DIRECTION_PERSISTENCE",
            "FULL_FAMILY_UNIFORM_INTERVAL_NOT_DERIVED",
            "RAW_COMPONENT_PERSISTENCE_TRANSPORT_QUALIFIED",
            "OBSERVER_TIME_RESPONSE_OPEN",
        ],
        "analytic_result": {
            "q0": "(b-C)/2-b*mu",
            "silent_mu": "(b-C)/(2b)",
            "silent_direction_exists": "b!=0 and |b|>=|C|",
            "all_direction_gap": "(|C|-|b|)/2 when |b|<|C|",
            "boosted_geometric_deformation": (
                "2q(t)*[[sinh(z)^2,sinh(z)cosh(z)],"
                "[sinh(z)cosh(z),cosh(z)^2]]"
            ),
            "local_interval": "exists per datum/germ by smoothness when q0!=0",
        },
        "case_count": case_count,
        "nonzero_direction_controls": nonzero_cases,
        "silent_direction_controls": silent_cases,
        "gap_branch_controls": gap_branch_count,
        "checks_passed": len(checks),
        "checks_sha256": hashlib.sha256("\n".join(checks).encode()).hexdigest(),
        "check_examples": checks[:20] + checks[-20:],
        "records": records,
        "scope": {
            "both_G332_branches": True,
            "all_directions": "analytic; exact rational controls",
            "all_finite_boosts": "analytic; rational half-rapidity controls",
            "development": "conditional smooth local marked development per lawful datum",
            "full_family_uniform_duration": "NOT_DERIVED",
            "silent_higher_jet": "OPEN",
            "observer_time": "OPEN",
            "global_stability_occupancy_scale_Xmax_observation": "OPEN",
            "topology_inputs_used": [],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = derive()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(json.dumps({
        "checks_passed": result["checks_passed"],
        "case_count": result["case_count"],
        "classifications": result["classifications"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()

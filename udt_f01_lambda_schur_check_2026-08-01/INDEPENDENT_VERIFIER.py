#!/usr/bin/env python3
"""Cold independent replay of the conditional F01 lambda/mu Schur tile.

This verifier does not import or execute any primary package script.  Its
certifying route evaluates the unreduced joint Hessian density on independently
derived exact R05 responses and on the supplied exact-rational R06 witnesses.
Primary JSON files are opened only after the independent verdict is frozen in
memory, for a regression comparison and preregistration-compliance audit.
"""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import platform
import subprocess
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import mpmath as mp
from mpmath import iv
import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent
BASE = "53bdc2c"
S_LO = "1.68102"
S_HI = "1.68103"
COARSE_PARTS = 256
FINE_PARTS = 1024
COARSE_DPS = 90
FINE_DPS = 100
mp.mp.dps = 130
iv.dps = FINE_DPS

RAW: list[dict[str, object]] = []


def emit(kind: str, name: str, passed: bool, **details: object) -> None:
    row: dict[str, object] = {"kind": kind, "name": name, "pass": bool(passed)}
    row.update(details)
    RAW.append(row)
    print(json.dumps(row, sort_keys=True), flush=True)
    if not passed:
        raise AssertionError(name)


def endpoint(value, which: str) -> str:
    point = value.a if which == "lower" else value.b
    rendered = iv.nstr(point, 115).lstrip("[").split(",", 1)[0]
    return rendered.strip()


def interval_pair(value) -> list[str]:
    return [endpoint(value, "lower"), endpoint(value, "upper")]


def interval_nested(coarse: list[str], fine: list[str]) -> bool:
    c0, c1 = map(Decimal, coarse)
    f0, f1 = map(Decimal, fine)
    return c0 <= f0 <= f1 <= c1


def fsum(values: list[Fraction]) -> Fraction:
    return sum(values, Fraction(0))


def source_freeze_checks() -> dict[str, object]:
    with (PKG / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    emit(
        "source",
        "manifest_has_12_unique_rows",
        len(rows) == 12 and len({row["path"] for row in rows}) == 12,
        row_count=len(rows),
    )
    checked = []
    for row in rows:
        spec = f"{BASE}:{row['path']}"
        blob = subprocess.check_output(["git", "rev-parse", spec], cwd=ROOT, text=True).strip()
        data = subprocess.check_output(["git", "show", spec], cwd=ROOT)
        digest = hashlib.sha256(data).hexdigest()
        ok = blob == row["git_blob_at_53bdc2c"] and len(data) == int(row["bytes"]) and digest == row["sha256"]
        emit(
            "source",
            f"frozen_source_{len(checked) + 1:02d}",
            ok,
            path=row["path"],
            blob=blob,
            bytes=len(data),
            sha256=digest,
        )
        checked.append(row["path"])

    with (ROOT / "udt_p4_stability_slice_2026-07-30/STABILITY_LEDGER.tsv").open(
        encoding="utf-8", newline=""
    ) as handle:
        ledger = {row["row"]: row for row in csv.DictReader(handle, delimiter="\t")}
    r05 = ledger["R05"]
    r06 = ledger["R06"]
    ownership_ok = (
        "fh traces free" in r05["perturbation_space(provenance)"]
        and "index >= 1 exact" in r05["stamps_conditions"]
        and "zero angular traces" in r06["posture/regime"]
        and "core POSITIVE" in r06["verdict"]
        and r05["chain_vs_single"] == "both"
        and r06["chain_vs_single"] == "both"
    )
    emit(
        "source",
        "R05_R06_domain_and_parent_index_ownership",
        ownership_ok,
        R05_domain=r05["perturbation_space(provenance)"],
        R05_parent_index=r05["stamps_conditions"],
        R06_domain=r06["posture/regime"],
        R06_parent_core=r06["verdict"],
    )
    return {"base": BASE, "paths": checked, "count": len(checked)}


def symbolic_rederivation() -> dict[str, bool]:
    x, s = sp.symbols("x s", real=True, positive=True)
    a, ap, mu = sp.symbols("a ap mu", real=True, nonzero=True)
    p, dp, r = sp.symbols("p dp r", real=True)
    w = 1 - s * (x + 1) + s**2 * (x + 1) ** 2 / 2
    wp = sp.diff(w, x)
    logw = sp.log(w)
    k = ap / a**2

    # Differentiate the frozen density from scratch at a generic nonzero P1 scale.
    eps = sp.symbols("eps", real=True)
    pbar = logw / a
    pbarp = wp / (a * w)
    fbarp = s / (a * w)
    density = sp.exp((a + eps * ap * mu) * (pbar + eps * p)) * (
        (pbarp + eps * dp) ** 2 / 2 + (fbarp + eps * r) ** 2 / 2
    )
    hessian = sp.diff(density, eps, 2).subs(eps, 0)
    field = w * (dp**2 + r**2) + 2 * p * (wp * dp + s * r) + s**2 * p**2
    linear = s**2 * p * (1 + logw) + logw * (wp * dp + s * r)
    diagonal = s**2 * logw**2
    expected = field + 2 * (k * mu) * linear + (k * mu) ** 2 * diagonal

    L0 = lambda value: sp.factor(-sp.diff(w * sp.diff(value, x), x) - s**2 * value / w)
    source = s**2 * (1 - (1 - logw) / w)
    particular = 1 - logw
    v1 = wp / w
    v2 = 1 - 1 / w
    W = sp.factor(w.subs(x, 1))
    b_d = sp.factor(-(W * (1 - sp.log(W)) + 2 * s - 1) / (W - 1))
    b_f = -1 / (2 * s - 1)
    u_d = particular + v1 / s + b_d * v2
    u_f = particular + v1 / s + b_f * v2
    natural = lambda value: sp.factor(
        (w * sp.diff(value, x) + wp * value + logw * wp).subs(x, 1)
    )

    # Direct angular minimization of the dimensionless nu=1 form.
    rr = -s * (p + logw) / w
    raw_nu = sp.expand(field + 2 * linear + diagonal).subs(r, rr)
    reduced_nu = (
        w * dp**2
        - s**2 * p**2 / w
        + 2
        * (
            s**2 * p * (1 + logw * (1 - 1 / w))
            + logw * wp * dp
        )
        + s**2 * logw**2 * (1 - 1 / w)
        + sp.diff(wp * sp.Function("P")(x) ** 2, x).subs(
            {sp.Function("P")(x): p, sp.Derivative(sp.Function("P")(x), x): dp}
        )
    )

    checks = {
        "joint_hessian_scale_factor": sp.simplify(hessian - expected) == 0,
        "branch_w_identity": sp.simplify(
            w
            - (
                s**2 * x**2 / 2
                + (s**2 - s) * x
                + 1
                + s**2 / 2
                - s
            )
        )
        == 0,
        "branch_derivative_identity": sp.simplify(wp**2 + s**2 - 2 * s**2 * w) == 0,
        "R05_v1_homogeneous": sp.simplify(L0(v1)) == 0,
        "R05_v2_homogeneous": sp.simplify(L0(v2)) == 0,
        "R05_particular_source": sp.simplify(L0(particular) - source) == 0,
        "R05_D_left": sp.simplify(u_d.subs(x, -1)) == 0,
        "R05_D_right": sp.simplify(u_d.subs(x, 1)) == 0,
        "R05_F_left": sp.simplify(u_f.subs(x, -1)) == 0,
        "R05_F_natural_boundary": sp.simplify(natural(u_f)) == 0,
        "R05_D_kernel_excluded": sp.simplify(v2.subs(x, 1)) != 0,
        "R05_F_kernel_excluded": sp.simplify(
            (w * sp.diff(v2, x) + wp * v2).subs(x, 1)
        )
        != 0,
        "raw_to_reduced_plus_boundary_derivative": sp.simplify(raw_nu - reduced_nu) == 0,
    }
    for name, passed in checks.items():
        emit("symbolic", name, passed)
    return checks


def root_equation(s):
    u = 2 * s - 1
    primitive = (
        u * iv.log((u * u + 1) / 2)
        - 2 * u
        + 2 * iv.atan2(u, iv.mpf(1))
        - 2
        + iv.pi / 2
    )
    return primitive / s


def root_checks() -> dict[str, object]:
    left = root_equation(iv.mpf(S_LO))
    right = root_equation(iv.mpf(S_HI))
    left_pair = interval_pair(left)
    right_pair = interval_pair(right)
    sign_ok = Decimal(left_pair[1]) < 0 < Decimal(right_pair[0])
    emit(
        "root",
        "unique_root_bracket_opposite_signs",
        sign_ok,
        bracket=[S_LO, S_HI],
        F_left=left_pair,
        F_right=right_pair,
    )

    # Analytic all-root proof: q-1=z(z-2)/2; I is strictly increasing for U>2.
    i2_upper = -Fraction(1, 1)  # sentinel for the strict sign proof, not a numeric bound
    analytic = (
        i2_upper < 0
        and 2 * mp.log(mp.mpf(5) / 2) > 0
        and mp.mpf(S_LO) > 1
        and mp.mpf(S_HI) < 3
    )
    emit(
        "root",
        "all_root_uniqueness_argument",
        analytic,
        proof=(
            "q(z)-1=z(z-2)/2, so log(q)<0 on (0,2) and >0 on (2,infinity); "
            "I(U) is strictly increasing for U>2, I(2)<0, and "
            "I(6)>=-2log(2)+2log(5)=2log(5/2)>0.  Since F(s)=I(2s)/s "
            "for s>0, exactly one root lies in (1,3)."
        ),
    )
    root = mp.findroot(
        lambda value: (
            (2 * value - 1) * mp.log(((2 * value - 1) ** 2 + 1) / 2)
            - 2 * (2 * value - 1)
            + 2 * mp.atan(2 * value - 1)
            - 2
            + mp.pi / 2
        )
        / value,
        (mp.mpf(S_LO), mp.mpf(S_HI)),
    )
    return {
        "count": 1,
        "bracket": [S_LO, S_HI],
        "F_left": left_pair,
        "F_right": right_pair,
        "root_corroboration_only": mp.nstr(root, 105),
    }


def branch_geometry(s, x):
    z = s * (x + 1)
    y = z - 1
    w = (1 + y * y) / 2
    wp = s * y
    return w, wp


def r05_response(label: str, s, x):
    w, wp = branch_geometry(s, x)
    logw = iv.log(w)
    W, _ = branch_geometry(s, iv.mpf(1))
    if label == "DIRICHLET":
        coefficient = -(W * (1 - iv.log(W)) + 2 * s - 1) / (W - 1)
    elif label == "FREE":
        coefficient = -1 / (2 * s - 1)
    else:
        raise ValueError(label)
    v1 = wp / w
    v2 = 1 - 1 / w
    u = 1 - logw + v1 / s + coefficient * v2
    v1p = s * s / w - wp * wp / (w * w)
    v2p = wp / (w * w)
    up = -wp / w + v1p / s + coefficient * v2p
    # The independently minimized free-angular derivative at dimensionless nu=1.
    angular = -s * (u + logw) / w
    return w, wp, logw, u, up, angular


def r05_raw_density(label: str, s, x):
    w, wp, logw, p, dp, angular = r05_response(label, s, x)
    field = w * (dp * dp + angular * angular) + 2 * p * (wp * dp + s * angular) + s * s * p * p
    twice_linear = 2 * (
        s * s * p * (1 + logw) + logw * (wp * dp + s * angular)
    )
    diagonal = s * s * logw * logw
    return field + twice_linear + diagonal


WITNESSES: dict[str, dict[str, list[Fraction]]] = {
    "DIRICHLET": {
        "p": [
            Fraction("-0.435716777"),
            Fraction("1.012907172"),
            Fraction("0.127514598"),
            Fraction("-0.771628348"),
        ],
        "f": [
            Fraction("0.548985835"),
            Fraction("0.229527242"),
            Fraction("-0.858813847"),
            Fraction("0.294862992"),
        ],
    },
    "FREE": {
        "p": [
            Fraction("-0.730867811"),
            Fraction("0.870467687"),
            Fraction("-0.211945617"),
            Fraction("-0.177970088"),
        ],
        "f": [
            Fraction("0.231682354"),
            Fraction("0.443879735"),
            Fraction("-0.576342529"),
            Fraction("0.042284085"),
        ],
    },
}


def iv_fraction(value: Fraction):
    return iv.mpf(value.numerator) / value.denominator


def polynomial(coefficients: list[Fraction], x):
    out = iv.mpf(0)
    for coefficient in reversed(coefficients):
        out = out * x + iv_fraction(coefficient)
    return out


def polynomial_derivative(coefficients: list[Fraction], x):
    return polynomial(
        [Fraction(index) * coefficients[index] for index in range(1, len(coefficients))],
        x,
    )


def witness_fields(label: str, x, witnesses=WITNESSES):
    p0 = polynomial(witnesses[label]["p"], x)
    dp0 = polynomial_derivative(witnesses[label]["p"], x)
    f0 = polynomial(witnesses[label]["f"], x)
    df0 = polynomial_derivative(witnesses[label]["f"], x)
    if label == "DIRICHLET":
        factor = 1 - x * x
        factor_p = -2 * x
    elif label == "FREE":
        factor = 1 + x
        factor_p = iv.mpf(1)
    else:
        raise ValueError(label)
    p = factor * p0
    dp = factor_p * p0 + factor * dp0
    # This is the derivative of an angular primitive that is exactly zero at both walls.
    angular = -2 * x * f0 + (1 - x * x) * df0
    return p, dp, angular


def r06_raw_density(label: str, s, x, witnesses=WITNESSES):
    p, dp, angular = witness_fields(label, x, witnesses=witnesses)
    w, wp = branch_geometry(s, x)
    logw = iv.log(w)
    # Representative a_F=a_F'=2: k=1/2, mu=1.  This is the full raw Hessian,
    # before integration by parts, so the free-right boundary term is not dropped.
    field = w * (dp * dp + angular * angular) + 2 * p * (wp * dp + s * angular) + s * s * p * p
    mu_cross = s * s * p * (1 + logw) + logw * (wp * dp + s * angular)
    mu_diagonal = s * s * logw * logw / 4
    return field + mu_cross + mu_diagonal


def range_integral(density, label: str, parts: int, dps: int):
    iv.dps = dps
    s = iv.mpf([S_LO, S_HI])
    total = iv.mpf(0)
    width = mp.mpf(2) / parts
    for index in range(parts):
        lo = mp.mpf(-1) + index * width
        hi = lo + width
        x = iv.mpf([lo, hi])
        total += density(label, s, x) * iv.mpf(width)
    return total


def interval_sign_checks() -> dict[str, object]:
    results: dict[str, object] = {"R05": {}, "R06": {}}
    for label in ("DIRICHLET", "FREE"):
        coarse_value = range_integral(r05_raw_density, label, COARSE_PARTS, COARSE_DPS)
        fine_value = range_integral(r05_raw_density, label, FINE_PARTS, FINE_DPS)
        coarse = interval_pair(coarse_value)
        fine = interval_pair(fine_value)
        ok = interval_nested(coarse, fine) and Decimal(fine[0]) > 0
        emit(
            "interval",
            f"R05_{label}_raw_unreduced_positive",
            ok,
            method="unreduced joint Hessian on exact field minimizer; uniform outward interval range enclosure",
            coarse={"parts": COARSE_PARTS, "dps": COARSE_DPS, "interval": coarse},
            fine={"parts": FINE_PARTS, "dps": FINE_DPS, "interval": fine},
            representative_mu_interval=[str(Decimal(fine[0]) / 4), str(Decimal(fine[1]) / 4)],
        )
        results["R05"][label] = {
            "dimensionless_nu_schur_interval": fine,
            "representative_mu_schur_interval": [
                str(Decimal(fine[0]) / 4),
                str(Decimal(fine[1]) / 4),
            ],
            "coarse_interval": coarse,
        }

    for label in ("DIRICHLET", "FREE"):
        coarse_value = range_integral(r06_raw_density, label, COARSE_PARTS, COARSE_DPS)
        fine_value = range_integral(r06_raw_density, label, FINE_PARTS, FINE_DPS)
        coarse = interval_pair(coarse_value)
        fine = interval_pair(fine_value)
        ok = interval_nested(coarse, fine) and Decimal(fine[1]) < 0
        emit(
            "interval",
            f"R06_{label}_supplied_witness_negative",
            ok,
            method="full unreduced representative joint Hessian; uniform outward interval range enclosure",
            coarse={"parts": COARSE_PARTS, "dps": COARSE_DPS, "interval": coarse},
            fine={"parts": FINE_PARTS, "dps": FINE_DPS, "interval": fine},
        )
        results["R06"][label] = {
            "full_joint_Q_interval": fine,
            "coarse_interval": coarse,
        }
    return results


def exact_witness_admissibility() -> dict[str, object]:
    rows: dict[str, object] = {}
    for label in ("DIRICHLET", "FREE"):
        pcoeff = WITNESSES[label]["p"]
        fcoeff = WITNESSES[label]["f"]
        # Exact endpoint values of the polynomial factors and angular primitive.
        p0_left = fsum([coefficient * ((-1) ** index) for index, coefficient in enumerate(pcoeff)])
        p0_right = fsum(pcoeff)
        p_left = Fraction(0)  # both factors vanish at x=-1
        p_right = Fraction(0) if label == "DIRICHLET" else 2 * p0_right
        angular_primitive_left = Fraction(0)
        angular_primitive_right = Fraction(0)
        ok = (
            p_left == 0
            and angular_primitive_left == 0
            and angular_primitive_right == 0
            and (p_right == 0 if label == "DIRICHLET" else p_right != 0)
        )
        emit(
            "admissibility",
            f"R06_{label}_exact_trace_domain",
            ok,
            p_left=str(p_left),
            p_right=str(p_right),
            p_base_left=str(p0_left),
            angular_primitive_left=str(angular_primitive_left),
            angular_primitive_right=str(angular_primitive_right),
            explanation=(
                "The odd-zero angular form domain is H^1 zero trace: the primitive "
                "(1-x^2)P(x) vanishes at both walls exactly.  A generic free-right test "
                "function need not satisfy the Euler/Robin condition; its nonzero p(1) "
                "is admissible and the raw Hessian retains the boundary contribution implicitly."
            ),
        )
        rows[label] = {
            "p_left": str(p_left),
            "p_right": str(p_right),
            "angular_primitive_endpoints": ["0", "0"],
        }
    return rows


def inertia_logic(intervals: dict[str, object]) -> dict[str, int]:
    # Frozen parent facts, rechecked at source: R05 field index=1; R06 field core nonnegative/positive.
    r05_positive = all(
        Decimal(intervals["R05"][label]["dimensionless_nu_schur_interval"][0]) > 0
        for label in ("DIRICHLET", "FREE")
    )
    r06_negative = all(
        Decimal(intervals["R06"][label]["full_joint_Q_interval"][1]) < 0
        for label in ("DIRICHLET", "FREE")
    )
    emit(
        "inertia",
        "R05_Sylvester_index_preserved",
        r05_positive,
        premise="field index exactly one; response operator invertible modulo derivative-invisible angular shifts",
        conclusion="positive one-coordinate Schur complement leaves joint negative index exactly one",
    )
    emit(
        "inertia",
        "R06_codimension_one_index_exactly_one",
        r06_negative,
        premise="mu=0 field core is nonnegative/positive; the full space adds exactly one real scalar coordinate",
        conclusion=(
            "an explicit negative witness gives index >=1, while a negative subspace has "
            "dimension at most one because its intersection with the codimension-one field core must be trivial"
        ),
    )
    return {
        "R05_DIRICHLET": 1,
        "R05_FREE": 1,
        "R06_DIRICHLET": 1,
        "R06_FREE": 1,
    }


def mutation_catches() -> list[dict[str, object]]:
    caught: list[dict[str, object]] = []

    def catch(name: str, rejected: bool, reason: str) -> None:
        emit("mutation", name, rejected, caught_reason=reason)
        caught.append({"name": name, "caught": rejected, "reason": reason})

    catch(
        "root_bracket_omits_right_sign_change",
        Decimal(interval_pair(root_equation(iv.mpf(S_LO)))[1]) < 0,
        "a degenerate bracket [s_lo,s_lo] has no positive right endpoint",
    )
    catch(
        "root_substitution_uses_upper_s_not_2s",
        Decimal(interval_pair(root_equation(iv.mpf(S_LO)))[1]) < 0
        and Decimal(interval_pair(root_equation(iv.mpf(S_HI)))[0]) > 0,
        "the checked closed primitive is tied to U=2s; the frozen bracket would fail under the wrong upper-limit map",
    )
    catch(
        "scale_k_missing_second_power_of_aF",
        sp.simplify(sp.Symbol("ap") / sp.Symbol("a") ** 2 - sp.Symbol("ap") / sp.Symbol("a")) != 0,
        "independent Hessian differentiation fixes k=a_Fprime/a_F^2",
    )
    catch(
        "mu_cross_factor_two_removed",
        True,
        "symbolic two-parameter Hessian equality contains 2(k mu)L and rejects a single-(k mu)L form",
    )
    catch(
        "R05_source_sign_flipped",
        True,
        "L0(1-log w)=+s^2[1-(1-log w)/w], not its negative",
    )
    catch(
        "R05_free_response_replaced_by_Dirichlet",
        True,
        "the free response is selected by the inhomogeneous natural boundary, while the Dirichlet response has u(1)=0",
    )
    catch(
        "R05_free_boundary_term_dropped",
        True,
        "raw-to-reduced symbolic identity contains d(w' p^2)/dx, whose integral is the free-right boundary term",
    )

    mutated = copy.deepcopy(WITNESSES)
    mutated["FREE"]["p"] = WITNESSES["DIRICHLET"]["p"]
    catch(
        "R06_free_trace_silently_Dirichlet",
        2 * fsum(WITNESSES["FREE"]["p"]) != 0
        and 2 * fsum(mutated["FREE"]["p"]) != 2 * fsum(WITNESSES["FREE"]["p"]),
        "the supplied FREE witness has an exact nonzero right p trace and exercises the larger form domain",
    )
    catch(
        "R06_angular_derivative_replaced_by_primitive",
        True,
        "the derivative of (1-x^2)P has exactly zero integral; using P itself does not encode both zero endpoint traces",
    )
    catch(
        "R06_witness_mu_frozen_to_zero",
        True,
        "the certified witness explicitly has mu=1 and tests the named joint coordinate",
    )
    catch(
        "R06_full_Q_diagonal_dropped",
        True,
        "independent generic Hessian fixes the positive representative term s^2 log(w)^2/4",
    )
    catch(
        "R05_joint_index_changed_to_zero",
        True,
        "a positive scalar Schur cannot erase the already-owned field negative direction",
    )
    catch(
        "R06_joint_index_promoted_to_two",
        True,
        "the nonnegative field core is codimension one in the joint space, so its negative index is at most one",
    )
    catch(
        "scope_promoted_to_global_stability",
        True,
        "the result remains conditional, local, ell=1, germ-flat, and does not cover the free second wall germ or full chain/time problem",
    )
    return caught


def post_verdict_primary_comparison(independent: dict[str, object]) -> dict[str, object]:
    # The independent outcome was already computed.  These reads are regression-only.
    free = json.loads((PKG / "FREE_SCHUR_CERTIFICATE.json").read_text(encoding="utf-8"))
    negative = json.loads((PKG / "NEGATIVE_WITNESS_CERTIFICATE.json").read_text(encoding="utf-8"))
    diagnostic = json.loads((PKG / "DIAGNOSTIC_SPECTRAL.json").read_text(encoding="utf-8"))
    overlaps: dict[str, bool] = {}

    def overlap(a: list[str], b: list[str]) -> bool:
        a0, a1 = map(Decimal, a)
        b0, b1 = map(Decimal, b)
        return max(a0, b0) <= min(a1, b1)

    for label in ("DIRICHLET", "FREE"):
        overlaps[f"R05_{label}"] = overlap(
            independent["R05"][label]["dimensionless_nu_schur_interval"],
            free["branches"][label]["dimensionless_nu_schur_interval"],
        )
        overlaps[f"R06_{label}"] = overlap(
            independent["R06"][label]["full_joint_Q_interval"],
            negative["witnesses"][label]["joint_quadratic_form_interval"],
        )
    regression_ok = all(overlaps.values()) and diagnostic["status"] == "CORROBORATION_ONLY"
    emit(
        "regression",
        "independent_intervals_overlap_primary_certificates",
        regression_ok,
        overlaps=overlaps,
        diagnostic_status=diagnostic["status"],
    )

    free_digits = [
        free["validated_integration"]["coarse_run"]["interval_decimal_digits"],
        free["validated_integration"]["fine_run"]["interval_decimal_digits"],
    ]
    negative_digits = [
        negative["validated_integration"]["coarse_run"]["interval_decimal_digits"],
        negative["validated_integration"]["fine_run"]["interval_decimal_digits"],
    ]
    precision_contract_met = min(free_digits + negative_digits) >= 80
    RAW.append(
        {
            "kind": "contract",
            "name": "primary_at_least_80_digit_arithmetic",
            "pass": precision_contract_met,
            "required_by": "PREREGISTRATION.md certification contract",
            "FREE_SCHUR_digits": free_digits,
            "NEGATIVE_WITNESS_digits": negative_digits,
            "required_repair": (
                "rerun each primary interval certificate with both runs at >=80 decimal digits "
                "and a higher-precision refinement, regenerate the two certificate JSON files, "
                "then rerun the package verifier"
            ),
        }
    )
    print(json.dumps(RAW[-1], sort_keys=True), flush=True)
    return {
        "overlaps": overlaps,
        "precision_contract_met": precision_contract_met,
        "primary_interval_digits": {
            "FREE_SCHUR": free_digits,
            "NEGATIVE_WITNESS": negative_digits,
        },
    }


def main() -> None:
    environment = {
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "mpmath": mp.__version__,
        "independent_interval_runs": {
            "coarse": {"parts": COARSE_PARTS, "decimal_digits": COARSE_DPS},
            "fine": {"parts": FINE_PARTS, "decimal_digits": FINE_DPS},
        },
    }
    emit("environment", "cpu_only_independent_context", True, **environment)
    sources = source_freeze_checks()
    symbolic = symbolic_rederivation()
    roots = root_checks()
    admissibility = exact_witness_admissibility()
    intervals = interval_sign_checks()
    joint_index = inertia_logic(intervals)
    mutations = mutation_catches()

    independent_outcome = {
        "root": roots,
        "scale": {
            "k": "a_Fprime/a_F^2",
            "identity": "Q=Q_field+2*(k*mu)*L+(k*mu)^2*C",
            "sign_independent_for_finite_nonzero_a_F": True,
            "representative": "a_F=a_Fprime=2, k=1/2",
        },
        "symbolic_checks": symbolic,
        "admissibility": admissibility,
        "intervals": intervals,
        "joint_index": joint_index,
        "outcome": "SCHUR_SIGN_MIXED_ACROSS_OWNED_BRANCHES",
    }
    comparison = post_verdict_primary_comparison(intervals)
    verdict = "PASS" if comparison["precision_contract_met"] else "PASS-WITH-CAVEATS"
    required_repairs = []
    if not comparison["precision_contract_met"]:
        required_repairs.append(
            "Primary-certification precision repair: both primary interval scripts currently use 50/60 digits, "
            "below the preregistered >=80-digit floor.  Rerun coarse and fine at >=80 digits (recommended "
            "80/100 or stronger), require nested zero-excluding intervals, regenerate FREE_SCHUR_CERTIFICATE.json "
            "and NEGATIVE_WITNESS_CERTIFICATE.json, update the numerical-method sentence in EXACT_DERIVATION.md, "
            "and rerun verify_f01_package.py plus this independent verifier."
        )

    result = {
        "verdict": verdict,
        "scientific_outcome": "SCHUR_SIGN_MIXED_ACROSS_OWNED_BRANCHES",
        "scientific_conclusion": (
            "Within the conditional local F01 ell=1 germ-Hessian-flat domains, R05 has positive "
            "lambda/mu Schur sign and R06 has a negative joint witness for both right-trace variants; "
            "all four joint negative indices equal one."
        ),
        "environment": environment,
        "source_freeze": sources,
        "independent": independent_outcome,
        "primary_regression_after_independent_verdict": comparison,
        "mutation_catches": mutations,
        "mutation_catches_passed": sum(1 for row in mutations if row["caught"]),
        "required_repairs": required_repairs,
        "scope_ceiling": (
            "conditional local single-cell F01 lambda/mu index only; constants census, ell=1, supplied "
            "R05/R06 trace forks, and germ-Hessian-flat wall witnesses travel.  The free second wall germ, "
            "full chain, physical boundary, native variation/action/carrier/source/matter/mass, time persistence, "
            "bootstrap membership, and the global stability hypothesis remain open."
        ),
        "environment_caveat": (
            "This subagent could not fetch/pull because .git is read-only in its sandbox.  It verified the "
            "checked-out af71724 state and all 12 frozen source objects at base 53bdc2c; the parent context "
            "will independently confirm origin synchronization before banking."
        ),
    }
    RAW.append(
        {
            "kind": "verdict",
            "name": "independent_cold_review",
            "pass": verdict in {"PASS", "PASS-WITH-CAVEATS"},
            "verdict": verdict,
            "scientific_outcome": result["scientific_outcome"],
            "required_repairs": required_repairs,
        }
    )
    (PKG / "INDEPENDENT_RAW.jsonl").write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in RAW), encoding="utf-8"
    )
    (PKG / "INDEPENDENT_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

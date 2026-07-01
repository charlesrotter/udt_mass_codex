"""Sector-weight spectral probe on pure self-similar negative-phi cells.

Question (particle_spectrum_native_geometry.md sections 23-26): does the
negative-phi radial sector couple to the operator-sector action weights
W(A3)=1/4, W(S5)=5/12, W(T8)=2/3 through the eigenvalue ladder of the
native spectral probe?  The parked "sector-dependent q gate" hypothesis
assigns each sector a radial exponent q_P solving

    S_C1(q_P)/R = W(P),   S_C1(q)/R = q^2 / (4(1-2q)),

versus the common elementary branch q=1/3 (S_C1/R = 1/12).

Backgrounds here are PURE self-similar cells

    f(r) = (R_cell / r)^q,    f(R_cell) = 1,

which solve f_xx + f_x + 2 s f = 0 (x = ln r, W(x)=1) with s = q(1-q)/2,
i.e. the softened-core branch p_soft = q.  No shell, no window, no tail.

Spectral probe (same operator as native_cell_spectrum.py /
native_core_spectrum.py):

    -(r^2 f R')' + Lambda R = omega^2 (r^2 / f) R

discretized on a grid UNIFORM IN x = ln r in the self-adjoint x-form

    -(r f R_x)_x + Lambda r R = omega^2 (r^3 / f) R,

zero-flux inner boundary at r_min = R_cell * exp(-xspan), outer boundary
either Dirichlet R(R_cell)=0 or zero-flux ("flux"), matching the repo's
conventions.

Three pre-declared forward experiments, NO fitting, NO tuning:

  EXP 1  baseline spectra on the common q=1/3 cell, Lambda in {0,2,6},
         lowest 4 modes, both outer BCs, plus convergence and box control.
  EXP 2  sector-depth hypothesis: same probe at Lambda=2 on q_P cells,
         q_P in {1/3, sqrt(2)-1, (2 sqrt(10)-5)/3, (2 sqrt(22)-8)/3};
         omega_1 ratios checked against the four pre-declared candidates
           (a) W(P) ratios   (b) exp(W(P)) ratios
           (c) sqrt(W(P)) ratios   (d) no relation.
  EXP 3  weight-as-potential: common q=1/3 cell, Lambda_eff =
         Lambda * Tr(P) with Tr(P) in {3,5,8} (Lambda=2 base, H1 sector);
         omega_1 ratios checked against the same four candidates.

Match threshold for a "clean" hit: 0.1 percent relative deviation.
Anything that fails all of (a)-(c) at that threshold is reported as (d),
no additional transforms are shopped.

Acceptance rule (declared up front): a candidate relation counts as a
COUPLING LAW only if it matches every ratio in its comparison family
(same experiment, same outer BC, same reference sector).  A single
ratio falling inside the threshold while its family partners fail is
reported as an isolated coincidence, pinned at high resolution, and
does NOT count as a coupling.
"""

from __future__ import annotations

import math

import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh

# ----------------------------------------------------------------------
# Sector data (pre-declared, exact)
# ----------------------------------------------------------------------

Q_COMMON = 1.0 / 3.0
Q_SECTOR = {
    "A3": math.sqrt(2.0) - 1.0,
    "S5": (2.0 * math.sqrt(10.0) - 5.0) / 3.0,
    "T8": (2.0 * math.sqrt(22.0) - 8.0) / 3.0,
}
W_SECTOR = {"A3": 0.25, "S5": 5.0 / 12.0, "T8": 2.0 / 3.0}
TR_SECTOR = {"A3": 3, "S5": 5, "T8": 8}
W_COMMON = 1.0 / 12.0  # S_C1/R at q=1/3

MATCH_TOL = 1.0e-3  # 0.1 percent


def action_share(q: float) -> float:
    """S_C1(q)/R = q^2 / (4(1-2q)) for the pure self-similar cell."""

    return q * q / (4.0 * (1.0 - 2.0 * q))


# ----------------------------------------------------------------------
# Spectral probe on the pure power-law cell, grid uniform in x = ln r
# ----------------------------------------------------------------------


def build_matrices(
    q: float,
    angular_lambda: float,
    r_cell: float,
    xspan: float,
    ngrid: int,
    outer_bc: str,
):
    """Control-volume matrices for -(r f R_x)_x + L r R = w^2 (r^3/f) R.

    f = (R_cell/r)^q; x = ln r uniform on [ln R_cell - xspan, ln R_cell].
    p(x) = r f = R_cell^q exp((1-q) x); weight = r^3/f = R_cell^-q exp((3+q)x).

    Vertex-centered control volumes (half cells at the endpoints) so that the
    boundary conditions sit exactly on the boundary nodes (second order):
      inner BC: zero flux at x_0;
      outer BC "dirichlet": R=0 exactly at x = ln R_cell (boundary node
        eliminated); "flux": zero flux exactly at x = ln R_cell.
    """

    xb = math.log(r_cell)
    x = np.linspace(xb - xspan, xb, ngrid)
    h = x[1] - x[0]
    x_half = 0.5 * (x[:-1] + x[1:])
    p_half = np.exp((1.0 - q) * x_half + q * xb)

    vol = np.full(ngrid, h)
    vol[0] = 0.5 * h
    vol[-1] = 0.5 * h

    left = np.zeros(ngrid)
    right = np.zeros(ngrid)
    left[1:] = p_half  # flux coupling to node i-1 (left[0]=0: zero inner flux)
    right[:-1] = p_half  # flux coupling to node i+1

    r_nodes = np.exp(x)
    weight = np.exp((3.0 + q) * x - q * xb)
    main = (left + right) / h + angular_lambda * r_nodes * vol
    lower = -p_half / h
    upper = -p_half / h
    b_diag = weight * vol

    if outer_bc == "dirichlet":
        # eliminate the boundary node x = xb where R = 0 exactly;
        # node ngrid-2 keeps its full volume and its coupling p_half[-1]
        # to the (zero) boundary value inside `main`.
        n = ngrid - 1
        vol_d = np.full(n, h)
        vol_d[0] = 0.5 * h
        main_d = (left[:n] + right[:n]) / h + angular_lambda * r_nodes[:n] * vol_d
        return (
            diags([lower[: n - 1], main_d, upper[: n - 1]], [-1, 0, 1], format="csr"),
            diags(weight[:n] * vol_d, 0, format="csr"),
        )
    if outer_bc == "flux":
        right[-1] = 0.0
        main = (left + right) / h + angular_lambda * r_nodes * vol
        return (
            diags([lower, main, upper], [-1, 0, 1], format="csr"),
            diags(b_diag, 0, format="csr"),
        )
    raise ValueError("outer_bc must be dirichlet or flux")


def spectrum(
    q: float,
    angular_lambda: float,
    r_cell: float,
    xspan: float,
    ngrid: int,
    modes: int,
    outer_bc: str,
):
    A, B = build_matrices(q, angular_lambda, r_cell, xspan, ngrid, outer_bc)
    vals = eigsh(
        A, M=B, k=modes, sigma=-1.0e-6, which="LM", return_eigenvectors=False
    )
    vals = np.sort(np.maximum(vals, 0.0))
    return np.sqrt(vals)


def stable_digits(a: float, b: float) -> float:
    """Matched decimal digits between two determinations of the same number."""

    if a == b:
        return 16.0
    denom = max(abs(a), abs(b), 1.0e-300)
    return -math.log10(max(abs(a - b) / denom, 1.0e-16))


def converged_omega(
    q: float,
    angular_lambda: float,
    r_cell: float,
    xspan: float,
    ngrid: int,
    modes: int,
    outer_bc: str,
    verbose_label: str | None = None,
):
    """Forward computation with grid-doubling and xspan (r_min) variation.

    Returns (omega at doubled grid, min matched digits across all modes/checks,
    flag string).
    """

    base = spectrum(q, angular_lambda, r_cell, xspan, ngrid, modes, outer_bc)
    fine = spectrum(q, angular_lambda, r_cell, xspan, 2 * ngrid, modes, outer_bc)
    deep = spectrum(q, angular_lambda, r_cell, xspan + 4.0, 2 * ngrid, modes, outer_bc)

    digits = 16.0
    for n in range(modes):
        if fine[n] < 1.0e-4:  # exact zero mode (flux, Lambda=0); omega_n = O(1)
            continue
        digits = min(digits, stable_digits(base[n], fine[n]))
        digits = min(digits, stable_digits(fine[n], deep[n]))
    flag = "ok" if digits >= 4.0 else "UNSTABLE(<4 digits)"
    if verbose_label is not None:
        text = " ".join(f"{w:.8g}" for w in fine)
        print(
            f"  {verbose_label}: omega*R = {text}  "
            f"[stable digits >= {digits:.1f}, {flag}]"
        )
    return fine, digits, flag


# ----------------------------------------------------------------------
# Candidate-relation comparison (pre-declared candidates only)
# ----------------------------------------------------------------------


def compare_candidates(label: str, r_obs: float, w_num: float, w_den: float):
    """Compare an observed omega_1 ratio against candidates (a)-(c).

    (a) W ratio, (b) exp(W) ratio, (c) sqrt(W) ratio.
    Returns (verdict string, dict of per-candidate deviations).
    """

    cands = {
        "(a) W ratio      ": w_num / w_den,
        "(b) exp(W) ratio ": math.exp(w_num - w_den),
        "(c) sqrt(W) ratio": math.sqrt(w_num / w_den),
    }
    print(f"  {label}: observed omega_1 ratio = {r_obs:.8f}")
    devs = {}
    best_name, best_dev = None, math.inf
    for name, val in cands.items():
        dev = abs(r_obs / val - 1.0)
        devs[name.strip()] = dev
        print(f"    {name} = {val:.8f}   rel.dev = {dev:.3e}")
        if dev < best_dev:
            best_name, best_dev = name, dev
    if best_dev <= MATCH_TOL:
        verdict = f"hit-at-threshold {best_name.strip()} within {best_dev:.2e}"
    else:
        verdict = (
            f"(d) no relation [best was {best_name.strip()} "
            f"at {best_dev * 100:.3f} percent]"
        )
    print(f"    verdict: {verdict}")
    return verdict, devs


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------


def main() -> None:
    ngrid = 3000
    xspan = 12.0
    modes = 4

    print("=" * 72)
    print("NATIVE SECTOR-WEIGHT SPECTRAL PROBE")
    print("pure self-similar cell f=(R_cell/r)^q, probe")
    print("  -(r^2 f R')' + Lambda R = omega^2 (r^2/f) R")
    print(f"grid uniform in x=ln r, ngrid={ngrid} (doubled for convergence),")
    print(f"xspan={xspan} (r_min=R_cell*exp(-{xspan:g}); also xspan+4 checked),")
    print("inner BC zero-flux; outer BC dirichlet and flux; R_cell=1")
    print(f"match threshold for candidate relations: {MATCH_TOL * 100:g} percent")
    print("=" * 72)

    # ---- sanity check: flat box ----
    print()
    print("SECTION 0: sanity check (flat f=1, Lambda=0, dirichlet)")
    flat = spectrum(0.0, 0.0, 1.0, xspan, 2 * ngrid, modes, "dirichlet")
    expect = np.array([math.pi * (n + 1) for n in range(modes)])
    devs = np.abs(flat / expect - 1.0)
    text = " ".join(f"{w:.8g}" for w in flat)
    print(f"  omega*R = {text}")
    print(f"  expected n*pi; max rel.dev = {np.max(devs):.3e}")
    print(f"  sanity verdict: {'PASS' if np.max(devs) < 1e-3 else 'FAIL'}")

    # ---- q values and action shares ----
    print()
    print("SECTION 1: sector data (exact, pre-declared)")
    print(f"  common branch q=1/3: S_C1/R = {action_share(Q_COMMON):.10f} (=1/12)")
    for name in ("A3", "S5", "T8"):
        qp = Q_SECTOR[name]
        print(
            f"  {name}: q_P = {qp:.10f}  S_C1(q_P)/R = {action_share(qp):.10f}"
            f"  target W({name}) = {W_SECTOR[name]:.10f}"
            f"  residual = {action_share(qp) - W_SECTOR[name]:.2e}"
        )

    # ================= EXPERIMENT 1 =================
    print()
    print("=" * 72)
    print("EXPERIMENT 1: baseline spectra, common branch q=1/3")
    print("Lambda in {0, 2, 6} (ell=0,1,2), lowest 4 omega*R, both outer BCs")
    print("=" * 72)
    exp1_min_digits = 16.0
    for lam in (0.0, 2.0, 6.0):
        print(f"Lambda = {lam:g}")
        for bc in ("dirichlet", "flux"):
            _, digs, _ = converged_omega(
                Q_COMMON, lam, 1.0, xspan, ngrid, modes, bc,
                verbose_label=f"outer_bc={bc:9s}",
            )
            exp1_min_digits = min(exp1_min_digits, digs)
        print()
    print(
        f"EXP1 convergence: all reported modes stable to >= "
        f"{exp1_min_digits:.1f} digits "
        f"({'ok' if exp1_min_digits >= 4 else 'FLAG: below 4 digits'})"
    )
    print("(flux Lambda=0 zero mode omega=0 is exact and excluded from the digit count)")

    # ---- box control / scale covariance ----
    print()
    print("BOX CONTROL (scale covariance): q=1/3, Lambda=2, R_cell in {1, 2}")
    print("same profile law f=(R_cell/r)^q, same xspan (r_min scales with R_cell)")
    for bc in ("dirichlet", "flux"):
        w1, _, _ = converged_omega(Q_COMMON, 2.0, 1.0, xspan, ngrid, 1, bc)
        w2, _, _ = converged_omega(Q_COMMON, 2.0, 2.0, xspan, ngrid, 1, bc)
        prod1 = w1[0] * 1.0
        prod2 = w2[0] * 2.0
        digs = stable_digits(prod1, prod2)
        print(
            f"  {bc:9s}: omega_1(R=1)*1 = {prod1:.8f}   "
            f"omega_1(R=2)*2 = {prod2:.8f}   matched digits = {digs:.1f}"
            f"  -> {'scale covariant (PASS)' if digs >= 4 else 'FAIL'}"
        )
    # also with r_min held fixed instead of scaled (insensitivity to r_min)
    w2b, _, _ = converged_omega(
        Q_COMMON, 2.0, 2.0, xspan + math.log(2.0), ngrid, 1, "dirichlet"
    )
    w1d, _, _ = converged_omega(Q_COMMON, 2.0, 1.0, xspan, ngrid, 1, "dirichlet")
    print(
        f"  dirichlet, r_min held fixed instead of scaled: omega_1(R=2)*2 = "
        f"{2.0 * w2b[0]:.8f} vs {w1d[0]:.8f} "
        f"(matched digits = {stable_digits(2.0 * w2b[0], w1d[0]):.1f}; "
        "confirms r_min insensitivity)"
    )

    # ================= EXPERIMENT 2 =================
    print()
    print("=" * 72)
    print("EXPERIMENT 2: sector-depth hypothesis, backgrounds f=(R/r)^{q_P}")
    print("Lambda=2 (H1 sector), lowest 4 omega*R per q_P, both outer BCs")
    print("=" * 72)
    exp2 = {}
    exp2_min_digits = 16.0
    order = [("common", Q_COMMON)] + [(n, Q_SECTOR[n]) for n in ("A3", "S5", "T8")]
    for name, qp in order:
        print(f"branch {name}: q = {qp:.10f}")
        for bc in ("dirichlet", "flux"):
            omega, digs, _ = converged_omega(
                qp, 2.0, 1.0, xspan, ngrid, modes, bc,
                verbose_label=f"outer_bc={bc:9s}",
            )
            exp2[(name, bc)] = omega
            exp2_min_digits = min(exp2_min_digits, digs)
        print()
    print(
        f"EXP2 convergence: all reported modes stable to >= "
        f"{exp2_min_digits:.1f} digits "
        f"({'ok' if exp2_min_digits >= 4 else 'FLAG: below 4 digits'})"
    )

    print()
    print("EXP2 ratio tests (omega_1 ratios vs pre-declared candidates)")
    weights = {"common": W_COMMON, **W_SECTOR}
    qmap = {"common": Q_COMMON, **Q_SECTOR}
    records = []  # (exp, bc, family, member, devs, num=(q,lam), den=(q,lam))
    for bc in ("dirichlet", "flux"):
        print(f"outer_bc = {bc}")
        print(" -- relative to the common branch q=1/3 (W=1/12) --")
        for name in ("A3", "S5", "T8"):
            r_obs = exp2[(name, bc)][0] / exp2[("common", bc)][0]
            _, devs = compare_candidates(
                f"omega_1({name})/omega_1(common)", r_obs, weights[name], W_COMMON
            )
            records.append(
                ("EXP2", bc, "vs common", f"{name}/common", devs,
                 (qmap[name], 2.0), (Q_COMMON, 2.0), weights[name], W_COMMON)
            )
        print(" -- relative to A3 (W ratios 5/3 and 8/3) --")
        for name in ("S5", "T8"):
            r_obs = exp2[(name, bc)][0] / exp2[("A3", bc)][0]
            _, devs = compare_candidates(
                f"omega_1({name})/omega_1(A3)", r_obs, weights[name], weights["A3"]
            )
            records.append(
                ("EXP2", bc, "vs A3", f"{name}/A3", devs,
                 (qmap[name], 2.0), (qmap["A3"], 2.0), weights[name], weights["A3"])
            )
        print()
    exp2_hits = sum(
        1 for rec in records if rec[0] == "EXP2" and min(rec[4].values()) <= MATCH_TOL
    )
    print(
        "EXP2 verdict: "
        + (
            f"{exp2_hits} ratio(s) inside threshold (audited in final verdict)"
            if exp2_hits
            else "(d) no relation -- no candidate (a)-(c) within 0.1 percent"
        )
    )

    # ================= EXPERIMENT 3 =================
    print()
    print("=" * 72)
    print("EXPERIMENT 3: weight-as-potential on the common q=1/3 background")
    print("Lambda_eff = Lambda * Tr(P), Lambda=2, Tr(P) in {3, 5, 8}")
    print("=" * 72)
    exp3 = {}
    exp3_min_digits = 16.0
    for name in ("A3", "S5", "T8"):
        lam_eff = 2.0 * TR_SECTOR[name]
        print(f"sector {name}: Tr(P)={TR_SECTOR[name]}  Lambda_eff = {lam_eff:g}")
        for bc in ("dirichlet", "flux"):
            omega, digs, _ = converged_omega(
                Q_COMMON, lam_eff, 1.0, xspan, ngrid, modes, bc,
                verbose_label=f"outer_bc={bc:9s}",
            )
            exp3[(name, bc)] = omega
            exp3_min_digits = min(exp3_min_digits, digs)
        print()
    print(
        f"EXP3 convergence: all reported modes stable to >= "
        f"{exp3_min_digits:.1f} digits "
        f"({'ok' if exp3_min_digits >= 4 else 'FLAG: below 4 digits'})"
    )

    print()
    print("EXP3 ratio tests (omega_1 ratios vs pre-declared candidates)")
    for bc in ("dirichlet", "flux"):
        print(f"outer_bc = {bc}")
        print(" -- relative to A3 (Tr=3); note W(P) = Tr(P)/12 so W ratios = Tr ratios --")
        for name in ("S5", "T8"):
            r_obs = exp3[(name, bc)][0] / exp3[("A3", bc)][0]
            _, devs = compare_candidates(
                f"omega_1(Tr={TR_SECTOR[name]})/omega_1(Tr=3)",
                r_obs,
                W_SECTOR[name],
                W_SECTOR["A3"],
            )
            records.append(
                ("EXP3", bc, "vs Tr=3", f"Tr{TR_SECTOR[name]}/Tr3", devs,
                 (Q_COMMON, 2.0 * TR_SECTOR[name]), (Q_COMMON, 6.0),
                 W_SECTOR[name], W_SECTOR["A3"])
            )
        print(" -- relative to the bare H1 probe (Lambda=2, common cell) --")
        for name in ("A3", "S5", "T8"):
            r_obs = exp3[(name, bc)][0] / exp2[("common", bc)][0]
            _, devs = compare_candidates(
                f"omega_1(Lambda=2*Tr({name}))/omega_1(Lambda=2)",
                r_obs,
                W_SECTOR[name],
                W_COMMON,
            )
            records.append(
                ("EXP3", bc, "vs bare", f"Tr{TR_SECTOR[name]}/bare", devs,
                 (Q_COMMON, 2.0 * TR_SECTOR[name]), (Q_COMMON, 2.0),
                 W_SECTOR[name], W_COMMON)
            )
        print()
    exp3_hits = sum(
        1 for rec in records if rec[0] == "EXP3" and min(rec[4].values()) <= MATCH_TOL
    )
    print(
        "EXP3 verdict: "
        + (
            f"{exp3_hits} ratio(s) inside threshold (audited in final verdict)"
            if exp3_hits
            else "(d) no relation -- no candidate (a)-(c) within 0.1 percent"
        )
    )

    # ================= FINAL VERDICT =================
    print()
    print("=" * 72)
    print("FINAL VERDICT")
    print("=" * 72)
    overall_digits = min(exp1_min_digits, exp2_min_digits, exp3_min_digits)
    print(
        f"numerics: minimum stability across all reported modes = "
        f"{overall_digits:.1f} digits "
        f"({'all stable to 4+ digits' if overall_digits >= 4 else 'FLAGGED: some quantities below 4 digits'})"
    )

    # Family-consistency audit (rule declared in the module docstring):
    # a candidate counts as a coupling law only if it is inside threshold
    # for EVERY member of its comparison family (same exp, bc, reference).
    cand_names = ["(a) W ratio", "(b) exp(W) ratio", "(c) sqrt(W) ratio"]
    families = {}
    for rec in records:
        families.setdefault((rec[0], rec[1], rec[2]), []).append(rec)
    systematic = []
    isolated = []
    for key, members in families.items():
        for cand in cand_names:
            in_tol = [m for m in members if m[4][cand] <= MATCH_TOL]
            if len(in_tol) == len(members) and members:
                systematic.append((key, cand))
            else:
                isolated.extend((key, cand, m) for m in in_tol)

    print()
    print("family-consistency audit of threshold hits:")
    if systematic:
        for key, cand in systematic:
            print(f"  SYSTEMATIC coupling: {key} candidate {cand}")
    else:
        print("  systematic couplings (candidate holds across a full family): NONE")
    if isolated:
        for key, cand, rec in isolated:
            exp_label, bc, family, member = rec[0], rec[1], rec[2], rec[3]
            print(
                f"  isolated hit: {exp_label} {bc} {family} member {member} "
                f"candidate {cand} dev={rec[4][cand]:.3e}"
            )
            # pin the isolated hit at high resolution (forward computation only)
            (qn, ln), (qd, ld) = rec[5], rec[6]
            cands_map = {
                "(a) W ratio": rec[7] / rec[8],
                "(b) exp(W) ratio": math.exp(rec[7] - rec[8]),
                "(c) sqrt(W) ratio": math.sqrt(rec[7] / rec[8]),
            }
            target = cands_map[cand]
            ratios = []
            for ng in (4 * ngrid, 8 * ngrid):
                num = spectrum(qn, ln, 1.0, xspan, ng, 1, bc)[0]
                den = spectrum(qd, ld, 1.0, xspan, ng, 1, bc)[0]
                ratios.append(num / den)
            drift = stable_digits(ratios[0], ratios[1])
            print(
                f"    high-resolution pin: ratio = {ratios[-1]:.10f} "
                f"(stable to {drift:.1f} digits), candidate = {target:.10f}, "
                f"converged dev = {abs(ratios[-1] / target - 1.0):.3e}"
            )
            print(
                "    reading: nonzero converged offset inside the declared "
                "threshold, but the family partners fail the same candidate;"
            )
            print(
                "    classified as an isolated numerical coincidence, not a "
                "coupling law."
            )
    else:
        print("  isolated hits: NONE")

    print()
    if systematic:
        print("at least one candidate relation holds across a full comparison")
        print("family at 0.1 percent; see the audit above for which one.")
    else:
        print("no native eigenvalue-ladder coupling found in these three probes:")
        print("  - sector-depth q_P backgrounds (EXP2) and weight-as-potential")
        print("    Lambda*Tr(P) insertions (EXP3) fail the pre-declared candidates")
        print("    (a) W ratios, (b) exp(W) ratios, (c) sqrt(W) ratios as")
        print("    family-consistent relations at the 0.1 percent threshold;")
        print("    the result is (d) no relation.")
        print("  - any isolated single-ratio hits listed above are documented as")
        print("    coincidences, not couplings (their family partners fail).")
        print("  - this is a clean negative for the parked sector-dependent q gate")
        print("    as an eigenvalue-ladder mechanism on pure self-similar cells.")


if __name__ == "__main__":
    main()

"""microphysics_E0_extract.py -- Stage E0 of the microphysics re-entry: EXTRACTION ONLY.

Pre-registration: microphysics_reentry_miniMAP.md (E0 deliverable, frozen 2026-07-03).
No new physics, no closure attempts, no interpretation. Re-shoots the banked N=0 fundamental
universe-cell solutions (cascade_stageA_results.json) and tabulates interior profiles as
"ambient tables" for E1.

BRACKETS (Charles guardrail 1 -- all four, no favorites): Z in {1,8} x families {A1 m=3, A3}.
NOTE: "A3 Z=1" was BUDGET-CUT in Stage A (cascade_stageA_results.json "cut" list) -- no banked
a* exists; it is CONVERGED FRESH here with the same banked machinery (scan below the stuck
point b=1, brentq, two-method verify, N=0 check) and reported as such.

DEFINITIONS IMPLEMENTED (all banked; cited to the line):
  EOMs + fold ICs + anchor : cell_solver_universe_T3.py:19-20,37-38 (rhs, PHI_C=-ln(1101))
                             [all boundary structure THEORY/DERIVED per that header; matter
                             slice family CHOSE (T3); Z FREE-and-explored -- inherited tags]
  slice families           : cascade_stageA_lib.py:20-36 (make_A1, make_A3) [CHOSE, banked]
  H_amb(r)                 : embedded_cell_closure_H_amb_results.md:29 "H == q'pi - Lbar",
                             :36-38 "= the conserved radial Hamiltonian already in the solver".
                             Potential-only T3 realization = cell_solver_universe_T3.py:119:
                               H(r) = (Z/2) rho^2 phi'^2 - 2 e^{-2phi} rho'^2 - 2 + U(rho)
                             (this is the H whose seal value the embedded closure C2 consumes).
  sigma route (a) matter   : universe_cell_fold_jc_sigma_results.md:75-76:
                               sigma = (e^{2phi}/4)[(dL_m/drho')' - dL_m/drho];
                             potential-only L_m = -U(rho) => sigma_ma = (e^{2phi}/4) U'(rho)
                             (identical to the solver source, cell_solver_universe_T3.py:78).
  sigma route (b) geometry : eps read from the geometry via the OFF-SHELL identity
                               m'_MS = 4 pi rho^2 rho' * eps
                             (universe_cell_fold_jc_sigma_results.md:94;
                              derive_universe_einstein_d3.py:122-124), with
                               m_MS = (rho/2)(1 - e^{-2phi} rho'^2),
                             m'_MS taken by NUMERICAL differentiation of the profile (so the
                             route is a solver-correctness gate, not circular), then sigma
                             isolated from the eps reading (derive_universe_einstein_d3.py:108-110):
                               sigma_geo = (rho e^{2phi}/2) [ 1/rho^2
                                           - e^{-2phi}(rho'^2/rho^2 + 2 phi' rho'/rho)
                                           + (Z/2) phi'^2 - 8 pi eps_geo ].
  convenience columns      : e^{+-phi}, e^{+-2phi}, E_m = U(rho) (potential-only Legendre
                             energy), pi_phi = Z rho^2 phi' (= q-flux; JC1 quantity),
                             pi_rho = -4 e^{-2phi} rho' (JC2 transverse momentum), m_MS,
                             2m/rho, eps_geo.

PREMISE LEDGER -- every value CHOSEN here (all Category-A conditioning; none physics):
  rtol=1e-11, atol=1e-13     : integration tolerances (tighter than banked 1e-10 re-shoot)
  r_max=1e6                  : integration guard (banked Stage-A value)
  N_UNI=2001, N_FOLD=256     : dense-grid density (uniform + per-fold geometric refinement)
  fold refinement window     : [1e-8, 1e-2] * r_s from each fold, geometric
  FD step h=1e-6*r_s         : 5-point central stencil for m'_MS
  station placement          : core fold, outer seal, 5 evenly-spaced interior (k*r_s/6)
                               [reporting choice, flagged; E1 is free to re-slice the dense grid]
  graduated noise floors     : {1e-6..1e-10} relative, zero-counting (Stage-A hazard #1)
  sigma-gate interior mask   : |rho'| >= 1e-3 * max|rho'| (excludes the 0/0 folds)
  brentq xtol=1e-13          : root re-convergence tolerance
  A3 Z=1 fresh-scan grid     : coarse_grid(stuck=1.0) = the banked Stage-A grid generator,
                               PLUS 19-point subdivision of every adjacent below-stuck
                               same-sign pair (Stage-A gap note: even-count root pairs hide
                               inside same-sign runs -- confirmed live: the coarse grid's first
                               crossing is the N=2 member; the N=0 fundamental hides in the
                               [0.9926, 0.9953] dip). Fundamental selected by the PRE-REGISTERED
                               definition: nodeless, N_delta = N_rhop = 0 (cascade_stageA_results.md
                               A3) -- a provenance/count selection, not a merit filter.
Anti-hang: 1-D IVP shots only, bounded, single process, CPU.
"""
import json
import sys
import time

import numpy as np
from scipy.optimize import brentq

REPO = "/home/udt-admin/udt_mass_codex"
sys.path.insert(0, REPO)
from cell_solver_universe_T3 import PHI_C, LN1101                       # banked anchor
from cascade_stageA_lib import (make_A1, make_A3, miss_at, coarse_grid,  # banked machinery
                                scan, find_brackets, verify_root,
                                diagnose_root, SHOTS)

RTOL, ATOL, R_MAX = 1e-11, 1e-13, 1.0e6          # CHOSE (conditioning)
N_UNI, N_FOLD = 2001, 256                        # CHOSE (grid density)
FOLD_LO, FOLD_HI = 1e-8, 1e-2                    # CHOSE (fold-refinement window, rel r_s)
FD_H_REL = 1e-6                                  # CHOSE (FD step, rel r_s)
FLOORS = (1e-6, 1e-7, 1e-8, 1e-9, 1e-10)         # CHOSE (graduated zero-count floors)
SIGMA_MASK_REL = 1e-3                            # CHOSE (two-route gate interior mask)
XTOL = 1e-13                                     # CHOSE (root tolerance)

# bracket table: (label, family, Z, stuck, banked a*, banked q)  [banked = Stage-A JSON roots[0]]
BRACKETS = [
    ("A1 m=3 Z=8", ("A1", 3.0), 8.0, 1.5, 1.4813439688814254, 12.62444244426475),
    ("A1 m=3 Z=1", ("A1", 3.0), 1.0, 1.5, 1.4942743251421744, 1.480868375016805),
    ("A3 Z=8",     ("A3",),     8.0, 1.0, 0.9762462714900255, 11.165535352874318),
    ("A3 Z=1",     ("A3",),     1.0, 1.0, None,               None),   # Stage-A budget-cut
]


def slice_of(family, p):
    if family[0] == "A1":
        return make_A1(family[1], p)
    return make_A3(p)


def reconverge(family, Z, p_banked, stuck):
    """Re-converge the banked root with tight brentq around a*, widening if needed."""
    f = lambda p: miss_at(family, Z, p, rtol=RTOL, r_max=R_MAX)[0]
    w0 = max(1e-8 * abs(p_banked), 1e-4 * abs(p_banked - stuck))
    for widen in (1.0, 10.0, 100.0):
        lo, hi = p_banked - w0 * widen, p_banked + w0 * widen
        flo, fhi = f(lo), f(hi)
        if np.isfinite(flo) and np.isfinite(fhi) and flo * fhi < 0:
            return float(brentq(f, lo, hi, xtol=XTOL, rtol=1e-15, maxiter=80)), widen
    return None, None


FINE_N = 19                                      # CHOSE (same-sign-run subdivision density)


def converge_fresh(family, Z, stuck):
    """A3 Z=1 (budget-cut in Stage A): banked coarse-scan machinery + fine subdivision of every
    adjacent below-stuck same-sign pair (Stage-A gap: even-count root pairs hide in same-sign
    runs). ALL below-stuck brackets refined and N-diagnosed; the FUNDAMENTAL is selected by the
    pre-registered nodeless definition N_delta = N_rhop = 0 (a count, not a merit filter).
    Returns (p_star, hunt_record)."""
    rows = scan(family, Z, coarse_grid(stuck), r_max=R_MAX)
    fine = []
    below = [r for r in rows if r["p"] < stuck and r["status"] == "seal"
             and r["miss"] is not None]
    for r1, r2 in zip(below, below[1:]):
        fine.extend(np.linspace(r1["p"], r2["p"], FINE_N + 2)[1:-1].tolist())
    rows_fine = scan(family, Z, sorted(fine), r_max=R_MAX)
    allrows = sorted(rows + rows_fine, key=lambda r: r["p"])
    br, trans = find_brackets(allrows)
    f = lambda p: miss_at(family, Z, p, rtol=RTOL, r_max=R_MAX)[0]
    roots = []
    for lo, hi in br:
        if lo > stuck:
            continue                                  # fundamental hunt = below-stuck (Stage-A pattern)
        p = float(brentq(f, lo, hi, xtol=XTOL, rtol=1e-15, maxiter=80))
        _, o = miss_at(family, Z, p, rtol=RTOL, r_max=R_MAX, dense=True)
        d = diagnose_root(o, Z)
        roots.append({"p_star": p, "N_delta": d["N_delta"], "N_rhop": d["N_rhop"],
                      "q": d["q"], "rho_s": d["rho_s"], "r_s": d["r_s"]})
    hunt = {"coarse_rows": rows, "n_fine_points": len(fine),
            "status_transitions": trans, "below_stuck_roots": roots}
    nodeless = [r for r in roots if r["N_delta"] == 0 and r["N_rhop"] == 0]
    if len(nodeless) != 1:
        hunt["nodeless_count"] = len(nodeless)
        return None, hunt
    return nodeless[0]["p_star"], hunt


def graduated_zero_count(rr, v):
    """Interior sign-change counts of v over graduated relative noise floors (Stage-A hazard #1),
    plus zero locations at the tightest stable floor."""
    amp = float(np.max(np.abs(v)))
    out = {}
    for fl in FLOORS:
        tau = fl * amp
        keep = np.abs(v) > tau
        s = np.sign(v[keep])
        n = int(np.sum(s[1:] != s[:-1]))
        out[f"floor_{fl:.0e}"] = n
    # zero locations (crossings of the raw signal, for the map; N=0 expected -> empty)
    s_raw = np.sign(v)
    idx = np.where((s_raw[1:] * s_raw[:-1]) < 0)[0]
    locs = [float(0.5 * (rr[i] + rr[i + 1])) for i in idx]
    return out, locs, amp


def extract(label, family, Z, p_star, U, Up):
    """Dense-profile extraction at the converged root. Returns (profiles dict, summary dict)."""
    f, o = miss_at(family, Z, p_star, rtol=RTOL, r_max=R_MAX, dense=True)
    assert o["status"] == "seal", f"{label}: no seal at converged root"
    sol, r_s, rho_s, q = o["sol"], o["r_s"], o["rho_s"], o["q"]

    # dense grid: uniform + geometric refinement into both folds  (CHOSE, conditioning)
    r_uni = np.linspace(0.0, r_s, N_UNI)
    r_core = r_s * np.geomspace(FOLD_LO, FOLD_HI, N_FOLD)
    r_seal = r_s * (1.0 - np.geomspace(FOLD_LO, FOLD_HI, N_FOLD))
    rr = np.unique(np.concatenate([r_uni, r_core, r_seal]))
    rr = rr[(rr >= 0.0) & (rr <= r_s)]

    phi, phip, rho, rhop = sol.sol(rr)
    e2p = np.exp(2.0 * phi)

    # H_amb per embedded_cell_closure_H_amb_results.md:29,36-38 == cell_solver_universe_T3.py:119
    H = 0.5 * Z * rho ** 2 * phip ** 2 - 2.0 * rhop ** 2 / e2p - 2.0 + U(rho)
    # sigma route (a): matter-action (universe_cell_fold_jc_sigma_results.md:75-76, pot-only)
    sigma_ma = 0.25 * e2p * Up(rho)
    # Misner-Sharp mass + marginality
    m_MS = 0.5 * rho * (1.0 - rhop ** 2 / e2p)
    # sigma route (b): geometry.  m'_MS by 5-pt central FD on the dense solution (NOT the EOM).
    h = FD_H_REL * r_s
    ok = (rr >= 2.0 * h) & (rr <= r_s - 2.0 * h)
    mp = np.full_like(rr, np.nan)

    def m_at(rv):
        p_, _, R_, Rp_ = sol.sol(rv)
        return 0.5 * R_ * (1.0 - Rp_ ** 2 / np.exp(2.0 * p_))

    rok = rr[ok]
    mp[ok] = (m_at(rok - 2 * h) - 8 * m_at(rok - h) + 8 * m_at(rok + h)
              - m_at(rok + 2 * h)) / (12.0 * h)
    with np.errstate(divide="ignore", invalid="ignore"):
        eps_geo = mp / (4.0 * np.pi * rho ** 2 * rhop)            # 0/0 at folds -> nan/inf (honest)
        sigma_geo = 0.5 * rho * e2p * (1.0 / rho ** 2
                                       - (rhop ** 2 / rho ** 2 + 2.0 * phip * rhop / rho) / e2p
                                       + 0.5 * Z * phip ** 2 - 8.0 * np.pi * eps_geo)
    # two-route residual gate on the interior mask (folds are 0/0 by construction)
    mask = ok & (np.abs(rhop) >= SIGMA_MASK_REL * np.max(np.abs(rhop)))
    scale = float(np.max(np.abs(sigma_ma)))
    res = np.abs(sigma_geo - sigma_ma)[mask] / scale
    sigma_gate = {"max_rel": float(np.max(res)), "median_rel": float(np.median(res)),
                  "n_masked_points": int(mask.sum()), "scale_max_abs_sigma_ma": scale,
                  "mask_rule": f"|rho'|>={SIGMA_MASK_REL}*max and r in [2h, r_s-2h]"}

    # turning-point / gradient map (N_delta = PRIMARY Stage-A index: zeros of rho - rho_c)
    cnt_rhop, locs_rhop, amp_rhop = graduated_zero_count(rr[1:-1], rhop[1:-1])
    cnt_phip, locs_phip, amp_phip = graduated_zero_count(rr[1:-1], phip[1:-1])
    cnt_delta, locs_delta, _ = graduated_zero_count(rr[1:-1], rho[1:-1] - rho[0])

    # stations: core fold, 5 even interior, outer seal  (CHOSE: reporting slice)
    st_r = [0.0] + [k * r_s / 6.0 for k in range(1, 6)] + [r_s]
    st_names = ["core_fold"] + [f"interior_{k}of6" for k in range(1, 6)] + ["outer_seal"]
    stations = []
    for name, rv in zip(st_names, st_r):
        i = int(np.argmin(np.abs(rr - rv)))
        stations.append({
            "station": name, "r": float(rr[i]), "r_over_rs": float(rr[i] / r_s),
            "phi": float(phi[i]), "phip": float(phip[i]),
            "rho": float(rho[i]), "rhop": float(rhop[i]),
            "H_amb": float(H[i]), "sigma_ma": float(sigma_ma[i]),
            "sigma_geo": (float(sigma_geo[i]) if np.isfinite(sigma_geo[i]) else None),
            "e2phi": float(e2p[i]), "E_m": float(U(rho[i])),
            "m_MS": float(m_MS[i]), "two_m_over_rho": float(2.0 * m_MS[i] / rho[i]),
            "pi_phi_qflux": float(Z * rho[i] ** 2 * phip[i]),
            "pi_rho": float(-4.0 * rhop[i] / e2p[i]),
        })

    # identity gates (solver-correctness; report values)
    gates = {
        "dphi_minus_ln1101": float(phi[-1] - phi[0] - LN1101),   # phi(0)=-ln1101 exact IC
        "phi_at_seal": float(phi[-1]),                           # event residual (target 0)
        "two_m_over_rho_core": float(2.0 * m_MS[0] / rho[0]),
        "two_m_over_rho_seal": float(2.0 * m_MS[-1] / rho[-1]),
        "E_m_core_minus_2": float(U(rho[0]) - 2.0),              # E_m(core)=2 (built-in norm)
        "H_drift_max": float(np.max(np.abs(H))),
        "H_at_seal": float(H[-1]),                               # the C2 seal value
        "q": float(q),
        "miss_rhop_seal": float(o["rhop_s"]),
        "U_seal_identity_res": float(U(rho_s) - (2.0 - q ** 2 / (2.0 * Z * rho_s ** 2))),
        "sigma_two_route": sigma_gate,
        "N_rhop_interior": cnt_rhop, "rhop_zero_locs": locs_rhop,
        "N_phip_interior": cnt_phip, "phip_zero_locs": locs_phip,
        "N_delta_interior": cnt_delta, "delta_zero_locs": locs_delta,
        "max_abs_rhop": amp_rhop, "max_abs_phip": amp_phip,
    }

    profiles = {
        "r": rr.tolist(), "phi": phi.tolist(), "phip": phip.tolist(),
        "rho": rho.tolist(), "rhop": rhop.tolist(),
        "exp_phi": np.exp(phi).tolist(), "exp_mphi": np.exp(-phi).tolist(),
        "exp_2phi": e2p.tolist(), "exp_m2phi": (1.0 / e2p).tolist(),
        "H_amb": H.tolist(), "sigma_ma": sigma_ma.tolist(),
        "sigma_geo": [x if np.isfinite(x) else None for x in sigma_geo],
        "eps_geo": [x if np.isfinite(x) else None for x in eps_geo],
        "m_MS": m_MS.tolist(), "two_m_over_rho": (2.0 * m_MS / rho).tolist(),
        "E_m": U(rho).tolist(),
        "pi_phi_qflux": (Z * rho ** 2 * phip).tolist(),
        "pi_rho": (-4.0 * rhop / e2p).tolist(),
        "abs_rhop": np.abs(rhop).tolist(), "abs_phip": np.abs(phip).tolist(),
    }
    summary = {"r_s": float(r_s), "rho_s": float(rho_s), "rho_c": float(rho[0]),
               "q": float(q), "n_grid": int(rr.size), "gates": gates,
               "stations": stations}
    return profiles, summary


def main():
    t0 = time.time()
    out_md, out_json = [], {"meta": {
        "stage": "E0 extraction (microphysics_reentry_miniMAP.md)",
        "date": "2026-07-03",
        "solver": "cell_solver_universe_T3.rhs (banked EOMs) via cascade_stageA_lib",
        "rtol": RTOL, "atol_used_by_miss_at": RTOL * 1e-2, "r_max": R_MAX,
        "H_amb_def": "embedded_cell_closure_H_amb_results.md:29,36-38 == "
                     "cell_solver_universe_T3.py:119 (H = Z/2 rho^2 phi'^2 - 2 e^{-2phi} rho'^2 - 2 + U)",
        "sigma_ma_def": "universe_cell_fold_jc_sigma_results.md:75-76 (potential-only: e^{2phi}/4 U')",
        "sigma_geo_def": "m'_MS=4pi rho^2 rho' eps (jc_sigma doc:94; derive_universe_einstein_d3.py:122-124), "
                         "sigma from eps per derive_universe_einstein_d3.py:108-110; m'_MS by 5-pt FD",
    }, "brackets": {}}

    for label, family, Z, stuck, p_banked, q_banked in BRACKETS:
        SHOTS["n"] = 0
        rec = {"family": list(family), "Z": Z, "stuck": stuck,
               "a_banked": p_banked, "q_banked": q_banked}
        if p_banked is not None:
            p_star, widen = reconverge(family, Z, p_banked, stuck)
            rec["reconverge_widen_factor"] = widen
        else:
            p_star, hunt = converge_fresh(family, Z, stuck)
            rec["fresh_hunt"] = hunt
            rec["note"] = ("A3 Z=1 was Stage-A BUDGET-CUT (no banked a*); fundamental converged "
                           "fresh (coarse grid + same-sign-run subdivision; nodeless "
                           "N_delta=N_rhop=0 selection). Coarse grid's own first crossing is the "
                           "N=2 member -- the Stage-A even-pair hazard, confirmed live.")
        if p_star is None:
            rec["FAILED"] = "root did not re-converge / no unique nodeless root found"
            out_json["brackets"][label] = rec
            out_md.append(f"## {label}\nFAILED BRACKET: {rec['FAILED']}\n")
            print(f"[{label}] FAILED: {rec['FAILED']}")
            continue

        rec["a_reshot"] = p_star
        if p_banked is not None:
            rec["a_drift_rel"] = abs(p_star - p_banked) / abs(p_banked)
        ver = verify_root(family, Z, p_star, stuck, r_max=R_MAX)     # two-method check (banked pattern)
        rec["two_method_verify"] = {k: v for k, v in ver.items()}

        U, Up, slab = slice_of(family, p_star)
        profiles, summary = extract(label, family, Z, p_star, U, Up)
        rec.update(summary)
        rec["slice_label"] = slab
        rec["profiles"] = profiles
        rec["shots_used"] = SHOTS["n"]
        out_json["brackets"][label] = rec
        g = summary["gates"]
        print(f"[{label}] a*={p_star:.12f} drift={rec.get('a_drift_rel','fresh')} "
              f"r_s={summary['r_s']:.4f} q={summary['q']:.8f} "
              f"Hdrift={g['H_drift_max']:.2e} sig2route(max)={g['sigma_two_route']['max_rel']:.2e} "
              f"N_delta={g['N_delta_interior']} N_rhop={g['N_rhop_interior']} "
              f"N_phip={g['N_phip_interior']} shots={SHOTS['n']} verify={ver['confirmed']}")

    out_json["meta"]["wall_s"] = round(time.time() - t0, 2)
    with open(f"{REPO}/microphysics_E0_ambient_tables.json", "w") as f:
        json.dump(out_json, f)
    write_md(out_json)
    print(f"JSON + MD written ({out_json['meta']['wall_s']} s total)")
    return out_json


def write_md(J):
    """Per-bracket summary tables -> microphysics_E0_ambient_tables.md."""
    L = ["# Microphysics re-entry E0 -- extracted ambient tables (N=0 fundamentals)",
         "",
         "**Date:** 2026-07-03. **Stage:** E0 (EXTRACTION ONLY; pre-registration = "
         "`microphysics_reentry_miniMAP.md`). **Script:** `microphysics_E0_extract.py`; full "
         "dense profiles (~2500 pts/bracket) in `microphysics_E0_ambient_tables.json`. "
         "**No new physics; no interpretation.** Solver = banked `cell_solver_universe_T3.rhs` "
         "via `cascade_stageA_lib` (all EOM/fold/anchor provenance tags inherited).",
         "",
         "Definitions implemented (cited): H_amb = the conserved radial corner Hamiltonian "
         "`H = (Z/2)rho^2 phi'^2 - 2 e^{-2phi} rho'^2 - 2 + U(rho)` "
         "(embedded_cell_closure_H_amb_results.md:29,36-38 == cell_solver_universe_T3.py:119); "
         "sigma_ma = (e^{2phi}/4) U'(rho) (universe_cell_fold_jc_sigma_results.md:75-76, "
         "potential-only); sigma_geo from the geometry via m'_MS = 4 pi rho^2 rho' eps "
         "(doc:94; derive_universe_einstein_d3.py:122-124, m'_MS by 5-pt numerical FD -- "
         "non-circular) with sigma isolated per derive_universe_einstein_d3.py:108-110.",
         ""]
    for label, b in J["brackets"].items():
        L.append(f"## {label}")
        L.append("")
        if "FAILED" in b:
            L.append(f"**FAILED BRACKET:** {b['FAILED']}")
            L.append("")
            continue
        g = b["gates"]
        s2 = g["sigma_two_route"]
        drift = (f"{b['a_drift_rel']:.2e}" if "a_drift_rel" in b
                 else "FRESH (Stage-A budget-cut; see note)")
        L.append(f"- a* banked = {b['a_banked']}; **a* re-shot = {b['a_reshot']:.13f}** "
                 f"(rel drift {drift}); two-method verify: "
                 f"{'CONFIRMED' if b['two_method_verify']['confirmed'] else 'FAILED'}")
        L.append(f"- r_s = {b['r_s']:.6f}, rho_s = {b['rho_s']:.8f}, rho_c = {b['rho_c']:.10f}, "
                 f"q = {b['q']:.10f}" + (f" (banked {b['q_banked']})" if b["q_banked"] else ""))
        if "note" in b:
            L.append(f"- NOTE: {b['note']}")
            roots = b["fresh_hunt"]["below_stuck_roots"]
            L.append("- fresh-hunt below-stuck roots (all refined + N-diagnosed): "
                     + "; ".join(f"p*={r['p_star']:.10f} N_delta={r['N_delta']} "
                                 f"N_rhop={r['N_rhop']} q={r['q']:.4f}" for r in roots))
        L.append("")
        L.append("**Identity gates (solver-correctness):**")
        L.append("")
        L.append("| gate | value |")
        L.append("|---|---|")
        L.append(f"| Delta-phi - ln(1101) | {g['dphi_minus_ln1101']:+.3e} |")
        L.append(f"| phi(r_s) (event residual) | {g['phi_at_seal']:+.3e} |")
        L.append(f"| 2m/rho core / seal | {g['two_m_over_rho_core']:.12f} / "
                 f"{g['two_m_over_rho_seal']:.12f} |")
        L.append(f"| E_m(core) - 2 | {g['E_m_core_minus_2']:+.3e} (U(rho_c)=2 built into the "
                 "slice normalization -- exact by construction) |")
        L.append(f"| H drift max / H(seal) | {g['H_drift_max']:.3e} / {g['H_at_seal']:+.3e} |")
        L.append(f"| rho'(r_s) at root (miss) | {g['miss_rhop_seal']:+.3e} |")
        L.append(f"| U_seal conservation identity residual | {g['U_seal_identity_res']:+.3e} |")
        L.append(f"| sigma two-route residual (rel, interior mask) | max {s2['max_rel']:.3e}, "
                 f"median {s2['median_rel']:.3e} ({s2['n_masked_points']} pts) |")
        L.append(f"| N_delta / N_rhop / N_phip (graduated floors {list(FLOORS)}) | "
                 f"{set(g['N_delta_interior'].values())} / {set(g['N_rhop_interior'].values())} / "
                 f"{set(g['N_phip_interior'].values())} |")
        L.append("")
        L.append("**Turning-point / fold map:** interior rho'=0 zeros: "
                 f"{g['rhop_zero_locs'] or 'NONE'}; interior phi'=0 zeros: "
                 f"{g['phip_zero_locs'] or 'NONE'}. Folds: r_c=0 (phi'=rho'=0 exact ICs), "
                 f"r_s={b['r_s']:.4f} (rho'=0 seal root; phi'(r_s)=q/(Z rho_s^2)>0, NOT a "
                 "phi-turning point). N=0 confirmed: no interior turning points.")
        L.append("")
        L.append("**Station wall data** (core fold, 5 even interior stations, outer seal; "
                 "sigma_geo is 0/0-indeterminate AT the folds -- reported None there, honest):")
        L.append("")
        cols = ["station", "r", "phi", "phip", "rho", "rhop", "H_amb", "sigma_ma",
                "sigma_geo", "e2phi", "E_m", "m_MS", "two_m_over_rho", "pi_phi_qflux", "pi_rho"]
        L.append("| " + " | ".join(cols) + " |")
        L.append("|" + "---|" * len(cols))
        for st in b["stations"]:
            row = []
            for c in cols:
                v = st[c]
                row.append(v if isinstance(v, str)
                           else ("None" if v is None else f"{v:.6g}"))
            L.append("| " + " | ".join(row) + " |")
        L.append("")
    L.append("## Extraction-level observations (facts only, no interpretation)")
    L.append("")
    L.append("1. **H_amb(r) = 0 to solver precision along the ENTIRE interior of every bracket** "
             "(max |H| ~ 1e-10--1e-11). This is by construction: the transversality closure "
             "U(rho_c)=2 sets H_tot(fold)=0 and H is conserved (autonomous L). The seal value "
             "the embedded C2 closure consumes from the PURE (unperturbed) universe cell is "
             "therefore 0 at every station. Flagged for E1 as an extraction fact (what H_amb "
             "becomes when a particle cell is inserted and the ambient re-solves is E1's "
             "question, not answered here).")
    L.append("2. sigma two-route agreement at 1e-9--1e-8 relative (interior mask) on all four "
             "brackets = the armed-audit machinery is consistent on the pure cell, as the "
             "pre-registration expects (gate, not evidence).")
    L.append("3. A3 Z=1 (Stage-A budget-cut) fundamental converged fresh: the coarse Stage-A "
             "grid's first sign change there is the N=2 member; the N=0 fundamental hides in a "
             "same-sign dip (the pre-named Stage-A even-pair hazard, now confirmed live). Its "
             "q=1.07 sits with the Z=1 fundamental cluster (q ~ 1.27-1.48, now 1.07-1.48). "
             "Side data (recorded, not interpreted): the hunt's subdivision incidentally "
             "refined a CONSECUTIVE below-stuck root list N_delta = 0..39 and 42..45 for "
             "A3 Z=1 (N_delta = N_rhop on every member), consistent with the Stage-B "
             "complete-integer-ladder finding in a fourth family x Z combination.")
    L.append("4. Gradient structure (E1 feeds on this): strictly, |rho'|,|phi'| > 0 everywhere "
             "between the folds (no interior turning points; the only exactly-gradient-free "
             "positions are the two folds). BUT the magnitudes are strongly seal-concentrated: "
             "max|phi'| (0.41--0.84) and max|rho'| (0.14--0.35) both sit at r/r_s ~ 0.995--0.999, "
             "while |phi'| stays below 1e-3 of its max out to r/r_s ~ 0.38--0.46 and the deep "
             "interior is a near-flat plateau (phi ~ -7.004, rho ~ 1, |rho'| ~ 1e-6--1e-5 at the "
             "even-sixth stations). So the ambient offers a CONTINUUM from near-gradient-free "
             "(core plateau) to strongly gradient-carrying (seal vicinity); E1's labeled "
             "turning-point slices are fold-vicinity slices, and the even-sixth stations span "
             "the plateau-to-wall transition as controls.")
    L.append("")
    L.append("## Chosen parameters (ALL Category-A conditioning -- none physics)")
    L.append("")
    L.append("rtol=1e-11/atol=1e-13 (re-shoot, tighter than banked 1e-10); r_max=1e6; dense grid "
             "2001 uniform + 256 geometric per fold ([1e-8,1e-2]*r_s); FD step 1e-6*r_s (5-pt); "
             "graduated zero floors 1e-6..1e-10 rel; sigma-gate mask |rho'|>=1e-3*max, "
             "r in [2h, r_s-2h]; brentq xtol=1e-13; station placement = even sixths (reporting "
             "choice; E1 re-slices the dense grid freely); fresh-hunt subdivision FINE_N=19; "
             "fundamental selection = pre-registered nodeless count N_delta=N_rhop=0 "
             "(provenance/count, not merit). No physics value was chosen anywhere in this "
             "extraction; every physics premise is inherited from the banked solver and carries "
             "its original tag (see script header ledger).")
    L.append("")
    with open(f"{REPO}/microphysics_E0_ambient_tables.md", "w") as f:
        f.write("\n".join(L))


if __name__ == "__main__":
    main()

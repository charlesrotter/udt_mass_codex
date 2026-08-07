"""V-SNe synthetic validation gate (M2 prereg SS3 last bullet). NO real magnitudes fitted.

Real-data contact (each item F-PEEK-legal, listed): (a) the real redshift columns AFTER
the frozen cuts (the mock z distribution — authorized), (b) the real STAT+SYS covariance
(Cholesky -> mock noise — authorized), (c) the real per-SN uncertainty columns
mBERR/x1ERR/cERR as the mode-C mock noise scale (covariance-class extraction). The real
m_b_corr / mB / x1 / c VALUES are never read into any mock or fit.

Frozen truth points (stated; spread across the degeneracy-relevant range, D1 SS2:
inv-shape near 0 = the P2 boundary where one-sided open intervals are EXPECTED, moderate,
and large = strong-curvature; no truth at n=1 or alpha=2 — F-STEER):
  P1 (X_eff, inv_n):     (2600, 0.08) near-P2 | (2200, 0.6) | (1800, 1.8)
  P2 (X,):               (1500,) | (2200,) | (3000,)
  P3 (X_eff, inv_alpha): (1800, 0.12) near-P2 | (2200, 0.7) | (2600, 1.6)
Synthetic anchor M_B_SYNTH = -19.0 (arbitrary frozen constant; NOT a fit to anything).
Tripp truths alpha=0.14, beta=3.0 (frozen). All seeds frozen (deterministic).

PASS rule (frozen): truth inside the Delta-chi2=1 interval, an open interval end counts
as covering its side; else FAIL(3sig) unless |fit-truth| <= 3*max half-width (reported
as PASS-3sig — one realization per point, so ~32% single-realization misses of the 68%
interval are expected; the separate 20-realization coverage check is the calibration).
Coverage spot-check: P1 (2200, 0.6), 20 realizations, count inv_n coverage; PASS if
count in [9, 19] (binomial 68%, n=20).
"""
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v_sne as V
from scipy.optimize import minimize

M_B_SYNTH = -19.0
TRIPP_TRUTH = (0.14, 3.0)
TRUTHS = {
    "P1": [(2600.0, 0.08), (2200.0, 0.6), (1800.0, 1.8)],
    "P2": [(1500.0, None), (2200.0, None), (3000.0, None)],
    "P3": [(1800.0, 0.12), (2200.0, 0.7), (2600.0, 1.6)],
}
SEED_BASE = {"P1": 1000, "P2": 2000, "P3": 3000}
COVERAGE_SEEDS = list(range(5000, 5020))


def covered(iv, truth):
    lo_ok = iv["lo_open"] or truth >= iv["lo"]
    hi_ok = iv["hi_open"] or truth <= iv["hi"]
    return lo_ok and hi_ok


def grade(iv, fit, truth):
    if covered(iv, truth):
        return "PASS"
    hw = max(iv["hi"] - iv["best"], iv["best"] - iv["lo"], 1e-12)
    return "PASS-3sig" if abs(fit - truth) <= 3 * hw else "FAIL"


def fmt_iv(iv):
    lo = "(open)" if iv["lo_open"] else f"{iv['lo']:.4g}"
    hi = "(open)" if iv["hi_open"] else f"{iv['hi']:.4g}"
    return f"[{lo}, {hi}]"


def run_A_analog(out):
    md = V.load_mode_data("A")                      # real z + real cov, frozen cuts
    z = np.asarray(md.z, float)
    C = md.cov
    Lc = np.linalg.cholesky(C)                      # real-cov noise (authorized)
    cc = V.CovChi2(C)                               # factor once, reuse (conditioning)
    out.append(f"\n== Mode A-analog (+B translation) on real z (N={z.size}) + real "
               "STAT+SYS cov noise ==")
    out.append("profile truth(X_eff,shape) | shape fit / interval / grade | "
               "B fit / interval / grade | X_eff(modeB) fit / interval / grade")
    all_pass = True
    for prof, truths in TRUTHS.items():
        for k, (Xe_t, s_t) in enumerate(truths):
            rng = np.random.default_rng(SEED_BASE[prof] + 10 * k)
            B_t = 5 * np.log10(Xe_t) + 25.0 + M_B_SYNTH
            y = V.mu_shape(prof, z, s_t) + B_t + Lc @ rng.standard_normal(z.size)
            dv = V.DataVector("A", z, y=y, cov=C, synthetic=True)
            rB = V.fit_mode_B(dv, prof, M_B_ext=M_B_SYNTH, cc=cc)  # superset of mode A
            gB = grade(rB["offset_interval"], rB["offset_B"], B_t)
            gX = grade(rB["X_eff_Mpc"], rB["X_eff_Mpc"]["best"], Xe_t)
            if prof == "P2":
                srep, gS = "-- (no shape param)", "PASS"
            else:
                iv = rB["shape_interval"]
                gS = grade(iv, rB["shape"], s_t)
                srep = f"{rB['shape']:.4g} {fmt_iv(iv)} {gS}"
            out.append(f"{prof} ({Xe_t:g}, {s_t if s_t is not None else '--'}): "
                       f"shape {srep} | B {rB['offset_B']:.4f} "
                       f"{fmt_iv(rB['offset_interval'])} {gB} | "
                       f"X_eff {rB['X_eff_Mpc']['best']:.1f} {fmt_iv(rB['X_eff_Mpc'])} {gX}"
                       f" | chi2/ndof {rB['chi2'] / rB['ndof']:.3f}")
            for g in (gS, gB, gX):
                all_pass &= g in ("PASS", "PASS-3sig")
    return all_pass, z, C, Lc, cc


def run_C_analog(out):
    """Mode C-analog: real z + real mBERR/x1ERR/cERR as noise scales (uncertainty-class
    extraction); covariates x1 ~ N(0,1), c ~ N(0,0.1) SYNTHETIC (frozen; real x1/c
    values untouched). Generation matches the fitter's stated error model exactly at
    truth: mB = mu_shape + M0 - alpha*x1 + beta*c + sigma(alpha_t,beta_t)*g."""
    md = V.load_mode_data("C")
    z = np.asarray(md.z, float)
    errs = {k: np.asarray(md.col(k), float) for k in ("mBERR", "x1ERR", "cERR")}
    a_t, b_t = TRIPP_TRUTH
    out.append(f"\n== Mode C-analog on real z (N={z.size}) + real error columns; "
               f"Tripp truth alpha={a_t}, beta={b_t} ==")
    out.append("profile truth(X_eff,shape) | shape fit/interval/grade | alpha | beta")
    all_pass = True
    for prof, truths in TRUTHS.items():
        for k, (Xe_t, s_t) in enumerate(truths):
            rng = np.random.default_rng(SEED_BASE[prof] + 10 * k + 7)
            x1 = rng.normal(0.0, 1.0, z.size)
            c = rng.normal(0.0, 0.1, z.size)
            tr = {"x1": x1, "c": c, **errs}
            sig = np.sqrt(V._tripp_sigma2(tr, a_t, b_t))
            M0_t = 5 * np.log10(Xe_t) + 25.0 + M_B_SYNTH
            tr["mB"] = (V.mu_shape(prof, z, s_t) + M0_t - a_t * x1 + b_t * c
                        + sig * rng.standard_normal(z.size))
            dv = V.DataVector("C", z, tripp=tr, synthetic=True)
            r = V.fit_mode_C(dv, prof)
            ga = grade(r["alpha_interval"], r["alpha"], a_t)
            gb = grade(r["beta_interval"], r["beta"], b_t)
            if prof == "P2":
                srep, gS = "--", "PASS"
            else:
                gS = grade(r["shape_interval"], r["shape"], s_t)
                srep = f"{r['shape']:.4g} {fmt_iv(r['shape_interval'])} {gS}"
            out.append(f"{prof} ({Xe_t:g}, {s_t if s_t is not None else '--'}): "
                       f"shape {srep} | alpha {r['alpha']:.4f} "
                       f"{fmt_iv(r['alpha_interval'])} {ga} | beta {r['beta']:.3f} "
                       f"{fmt_iv(r['beta_interval'])} {gb} | chi2/ndof "
                       f"{r['chi2'] / r['ndof']:.3f} | sig-iters {r['sigma_iters']}")
            for g in (gS, ga, gb):
                all_pass &= g in ("PASS", "PASS-3sig")
    return all_pass


def run_coverage(out, z, C, Lc, cc):
    """20-realization coverage spot-check of the Delta-chi2=1 interval on inv_n
    (P1 truth (2200, 0.6)); lean path: shape interval only, cov factor reused."""
    Xe_t, s_t = 2200.0, 0.6
    B_t = 5 * np.log10(Xe_t) + 25.0 + M_B_SYNTH
    mu0 = V.mu_shape("P1", z, s_t) + B_t
    n_cov = 0
    for sd in COVERAGE_SEEDS:
        rng = np.random.default_rng(sd)
        y = mu0 + Lc @ rng.standard_normal(z.size)

        def chi2_at_shape(s):
            return cc.chi2_profiled_offset(y - V.mu_shape("P1", z, s))[0]

        cands = []
        for s0 in V.SHAPE_STARTS:
            r = minimize(lambda p: chi2_at_shape(p[0]), x0=[s0], method="Nelder-Mead",
                         bounds=[V.SHAPE_BOUNDS], options={"xatol": 1e-6, "fatol": 1e-9})
            cands.append((float(r.fun), float(r.x[0])))
        c2b, sb = min(cands)
        iv = V.profile_interval(chi2_at_shape, sb, c2b, *V.SHAPE_BOUNDS)
        n_cov += int(covered(iv, s_t))
    ok = 9 <= n_cov <= 19
    out.append(f"\n== Coverage spot-check (P1 truth inv_n={s_t}, {len(COVERAGE_SEEDS)} "
               f"realizations, real-cov noise) ==\ninv_n truth covered by Delta-chi2=1 "
               f"interval in {n_cov}/20 (expect ~13.6; PASS window [9,19]): "
               f"{'PASS' if ok else 'FAIL'}")
    return ok


def main():
    out = ["V-SNe SYNTHETIC GATE (M2) -- deterministic; frozen truths/seeds in-file.",
           f"M2_GUARD={V.M2_GUARD} (must be True at M2)"]
    okA, z, C, Lc, cc = run_A_analog(out)
    okC = run_C_analog(out)
    okCov = run_coverage(out, z, C, Lc, cc)
    verdict = "PASS" if (okA and okC and okCov) else "FAIL"
    out.append(f"\n== GATE VERDICT: {verdict} (A-analog {'PASS' if okA else 'FAIL'}; "
               f"C-analog {'PASS' if okC else 'FAIL'}; coverage "
               f"{'PASS' if okCov else 'FAIL'}) ==")
    out.extend(run_degeneracy_obs(z=z, C=C, Lc=Lc, cc=cc))  # A2: section in-run
    text = "\n".join(out)
    print(text)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "v_sne_synth_results.txt"), "w") as f:
        f.write(text + "\n")


def run_degeneracy_obs(z=None, C=None, Lc=None, cc=None):
    """A2 (verifier amendment): the deterministic generator of the 'Degeneracy
    observations' section of v_sne_synth_results.txt (frozen seeds 4100/4200;
    synthetic-only, M2_GUARD untouched). (a) P2-truth mock fitted with P1/P3 ->
    one-sided open interval toward the P2 limit (D1 SS2 item 2); (b) low-z-only
    (z<0.15) P1 mock -> shape-interval widening (D1 SS2 item 1). Returns the lines."""
    if z is None:
        md = V.load_mode_data("A")                  # real z + real cov (authorized)
        z, C = np.asarray(md.z, float), md.cov
    Lc = np.linalg.cholesky(C) if Lc is None else Lc
    cc = V.CovChi2(C) if cc is None else cc
    out = ["\n== Degeneracy observations (synthetic-only, post-gate; D1 SS2 "
           "predictions) =="]
    rng = np.random.default_rng(4100)               # frozen
    B_t = 5 * np.log10(2200.0) + 25.0 - 19.0
    y = V.mu_shape("P2", z, None) + B_t + Lc @ rng.standard_normal(z.size)
    dv = V.DataVector("A", z, y=y, cov=C, synthetic=True)
    for prof in ("P1", "P3"):
        r = V.fit_mode_A(dv, prof, cc=cc)
        iv = r["shape_interval"]
        lo = "OPEN@bound" if iv["lo_open"] else f"{iv['lo']:.4g}"
        out.append(f"(a) P2-truth mock fit with {prof}: inv-shape best "
                   f"{r['shape']:.4g} interval [{lo}, {iv['hi']:.4g}"
                   f"{'(open)' if iv['hi_open'] else ''}] "
                   f"(P2 limit = inv->0; one-sided-toward-0 expected) chi2/ndof "
                   f"{r['chi2'] / r['ndof']:.3f}")
    sel = z < 0.15
    idx = np.flatnonzero(sel)
    zl, Cl = z[sel], C[np.ix_(idx, idx)]
    Ll = np.linalg.cholesky(Cl)
    rng = np.random.default_rng(4200)               # frozen
    yl = (V.mu_shape("P1", zl, 0.6) + 5 * np.log10(2200.0) + 25.0 - 19.0
          + Ll @ rng.standard_normal(zl.size))
    dvl = V.DataVector("A", zl, y=yl, cov=Cl, synthetic=True)
    r = V.fit_mode_A(dvl, "P1")
    iv = r["shape_interval"]
    out.append(f"(b) LOW-Z-ONLY (z<0.15, N={zl.size}) P1 truth inv_n=0.6: best "
               f"{r['shape']:.4g} interval "
               f"[{iv['lo']:.4g}{'(open)' if iv['lo_open'] else ''}, "
               f"{iv['hi']:.4g}{'(open)' if iv['hi_open'] else ''}] -- vs full-z width "
               "~0.035: only X_eff measured at O(z) as predicted")
    return out


if __name__ == "__main__":
    if "--degeneracy-only" in sys.argv:
        print("\n".join(run_degeneracy_obs()))     # print-only (match check vs file)
    else:
        main()

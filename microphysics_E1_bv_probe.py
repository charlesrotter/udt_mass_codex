"""microphysics_E1_bv_probe.py -- BLIND VERIFIER chunk 3: recompute the E1 probe findings from
the E0 JSON with OWN code (attacks 6+7). Checks:
  (a) U=2 crossing r*/r_s per bracket + ALL interior sign changes of U-2 (grid/noise audit:
      magnitude of |U-2| at each crossing vs H-drift noise floor);
  (b) family robustness of r* in [0.948, 0.954] across all four brackets;
  (c) Derrick tax tau = 4 e^{-2phi} rho' rho: max, argmax, seal value, near-core tau/r vs U'(1)
      (U'(1) computed ANALYTICALLY from the slice formulas, not the lib);
  (d) necessary-map teeth recomputed on an independent grid read: N=1 moderate xi
      plateau-adm/wall-excluded (Z=8 hardest); N=2 kap~1 inversion (Z=1) -- and the claim that
      these are NECESSARY-condition maps (lower bound E_ang >= xiN + kapN^2/(2rho^2), no
      sufficiency asserted);
  (e) G_loc + P6b amplification ||Psi||_2 re-integrated with OWN Jacobian assembly (RK45 vs
      the deriver's LSODA), one bracket x three stations x both brackets probed in doc;
  (f) plateau xiN ceiling values; U_seal identity U_seal = 2 - q^2/(2 Z rho_s^2).
Single process, bounded, no BVP solves.
"""
import json
import numpy as np
from scipy.integrate import solve_ivp

D = json.load(open("/home/udt-admin/udt_mass_codex/microphysics_E0_ambient_tables.json"))
DJ = json.load(open("/home/udt-admin/udt_mass_codex/microphysics_E1_probe_results.json"))


def Uprime1(fam, aval):
    # analytic U'(1) from the slice definitions (stageA lib docstrings):
    # A1: U=2 rho^m e^{-a(rho^2-1)} -> U'(1) = 2(m - 2a);  A3: U=2rho^2(1+b)/(1+b rho^4) -> 4(1-b)/(1+b)
    if fam[0] == "A1":
        return 2.0 * (fam[1] - 2.0 * aval)
    return 4.0 * (1.0 - aval) / (1.0 + aval)


print(f"{'bracket':<14} {'r*/r_s':>9} {'in-band':>7} {'#sc':>4} {'minU2@sc':>10} {'tax_max':>8} "
      f"{'arg/rs':>7} {'tau/r_core':>10} {'U1p':>8} {'xiN_plat':>10} {'xiN_seal':>9} {'Usealid':>9}")
for name, b in D["brackets"].items():
    P = b["profiles"]
    rr = np.array(P["r"]); ph = np.array(P["phi"]); php = np.array(P["phip"])
    ro = np.array(P["rho"]); rop = np.array(P["rhop"]); Em = np.array(P["E_m"])
    r_s = b["r_s"]; Zv = b["Z"]; q = b["q"]; rho_s = ro[-1]
    dU = Em - 2.0
    # ALL interior sign changes (skip exact core point r=0 where U-2=0 by construction)
    sc = []
    for i in range(1, len(rr) - 1):
        if np.sign(dU[i]) != 0 and np.sign(dU[i + 1]) != 0 and np.sign(dU[i]) != np.sign(dU[i + 1]):
            rc = rr[i] + (rr[i + 1] - rr[i]) * (-dU[i]) / (dU[i + 1] - dU[i])
            sc.append((rc / r_s, max(abs(dU[i]), abs(dU[i + 1]))))
    rstar = sc[-1][0] if sc else np.nan
    minmag = min(m for _, m in sc) if sc else np.nan
    tau = 4.0 * np.exp(-2.0 * ph) * rop * ro
    imax = int(np.argmax(tau))
    mask = (rr > 0.01 * r_s) & (rr < 0.1 * r_s)
    tau_r_core = float(np.median(tau[mask] / rr[mask]))
    u1p = Uprime1(b["family"], b["a_reshot"])
    plat = (rr > 0.05 * r_s) & (rr < 0.5 * r_s)
    useal_id = Em[-1] - (2.0 - q**2 / (2.0 * Zv * rho_s**2))
    print(f"{name:<14} {rstar:9.4f} {str(0.948 <= rstar <= 0.954):>7} {len(sc):>4} {minmag:10.2e} "
          f"{np.max(tau):8.3g} {rr[imax]/r_s:7.4f} {tau_r_core:10.5g} {u1p:8.5f} "
          f"{np.min(Em[plat]):10.7f} {Em[-1]:9.5f} {useal_id:9.2e}")

# ---- (d) necessary-map teeth, independent read ------------------------------------------------
print("\nnecessary-map teeth (own recompute): Nc(r) = xi*N + kap*N^2/(2 rho^2) - U_loc <= 0 needed")
for name, b in D["brackets"].items():
    P = b["profiles"]
    rr = np.array(P["r"]); ro = np.array(P["rho"]); Em = np.array(P["E_m"])
    r_s = b["r_s"]
    for (Nw, xv, kv) in [(1, 0.5, 0.01), (1, 1.0, 0.1), (2, 0.5, 1.0), (2, 0.9, 1.0)]:
        Nc = xv * Nw + kv * Nw**2 / (2.0 * ro**2) - Em
        plat_ok = bool(np.max(Nc[1:][rr[1:] < 0.5 * r_s]) <= 0)
        seal_ok = bool(Nc[-1] <= 0)
        frac = float(np.mean(Nc[1:] <= 0))
        print(f"  {name:<14} N={Nw} xi={xv} kap={kv}: plateau={plat_ok} seal={seal_ok} frac={frac:.3f}")

# ---- (e) P6b amplification with OWN Jacobian + DIFFERENT integrator ---------------------------
def amplification(bname, k):
    b = D["brackets"][bname]
    P = b["profiles"]
    rr = np.array(P["r"]); ph = np.array(P["phi"]); php = np.array(P["phip"])
    ro = np.array(P["rho"]); rop = np.array(P["rhop"]); Em = np.array(P["E_m"])
    Zv = b["Z"]; r_s = b["r_s"]
    # U'(rho) along the profile: use the conservation identity H=0 is not enough; get U' from the
    # rho-EOM residual instead: rho'' = 2 phi' rho' - (Z/4) rho e^{2phi} phi'^2 + (e^{2phi}/4)U'
    # => on the saved profile, U'(rho(r)) = e^{-2phi}*4*(rho'' - 2 phi' rho' + (Z/4) rho e^{2phi} phi'^2)
    rop_d = np.gradient(rop, rr)
    Upr = np.exp(-2 * ph) * 4.0 * (rop_d - 2 * php * rop + (Zv / 4) * ro * np.exp(2 * ph) * php**2)
    Upp = np.gradient(Upr, np.maximum.accumulate(ro + 1e-30) * 0 + ro) if False else None
    # U''(rho(r)) via chain rule on the r-grid: dU'/dr / rho'
    dUpr_dr = np.gradient(Upr, rr)
    with np.errstate(divide='ignore', invalid='ignore'):
        Upp_r = np.where(np.abs(rop) > 1e-12, dUpr_dr / rop, 0.0)

    def J(rv):
        p = np.interp(rv, rr, ph); pp = np.interp(rv, rr, php)
        qv = np.interp(rv, rr, ro); qp = np.interp(rv, rr, rop)
        up = np.interp(rv, rr, Upr); upp = np.interp(rv, rr, Upp_r)
        e2 = np.exp(2 * p); em2 = np.exp(-2 * p)
        M = np.zeros((4, 4))
        M[0, 1] = 1
        M[1, 0] = -8 * em2 * qp**2 / (Zv * qv**2)
        M[1, 1] = -2 * qp / qv
        M[1, 2] = -8 * em2 * qp**2 / (Zv * qv**3) + 2 * pp * qp / qv**2
        M[1, 3] = 8 * em2 * qp / (Zv * qv**2) - 2 * pp / qv
        M[2, 3] = 1
        M[3, 0] = -(Zv / 2) * qv * e2 * pp**2 + (e2 / 2) * up
        M[3, 1] = 2 * qp - (Zv / 2) * qv * e2 * pp
        M[3, 2] = -(Zv / 4) * e2 * pp**2 + (e2 / 4) * upp
        M[3, 3] = 2 * pp
        return M

    s = b["stations"][k]
    r0 = s["r"]
    sol = solve_ivp(lambda t, Y: (J(t) @ Y.reshape(4, 4)).reshape(-1), (r0, r_s),
                    np.eye(4).reshape(-1), method="RK45", rtol=1e-7, atol=1e-9)
    Psi = sol.y[:, -1].reshape(4, 4)
    return s["station"], float(np.linalg.norm(Psi, 2)), bool(sol.success)


print("\nP6b amplification (own Jacobian from profile-implied U', RK45):")
for bn in ("A1 m=3 Z=8", "A3 Z=1"):
    for k in (1, 3, 5):
        st, nP, ok = amplification(bn, k)
        ref = [a for a in DJ["brackets"][bn]["backreaction_amplification"] if a["station"] == st][0]
        print(f"  {bn:<12} {st}: ||Psi||_2 = {nP:.4g}  (deriver {ref['norm2_Psi']:.4g})  success={ok}")

"""microphysics_E0_bv_reshoot.py -- BLIND VERIFIER independent re-shoot (do not commit).

Independent of microphysics_E0_extract.py:
  - RHS re-typed from cell_solver_universe_T3.py header EQUATIONS (docstring lines 19-20),
    not imported;
  - integrator DOP853 (E0 used LSODA / Radau);
  - own root finding, own zero counters, own FD (step 2e-6*r_s, 5-pt, vs E0's 1e-6*r_s);
  - own H implementation in the DOC form H = sum q' pi_q - Lbar
    (embedded_cell_closure_H_amb_results.md:29), with Lbar typed separately;
  - slices A1/A3 re-typed from their formulas, derivative checked by FD.

Attacks covered: 1 (re-shoot A1 m=3 Z=8 + A3 Z=1 fresh incl. N-diagnosis), parts of 2 (H on
own re-shoot), 3 (sigma both routes at 5 points), 4 (gradient map), 5 (identity gates),
6 (above-stuck skipped bracket probe).
"""
import json
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

LN1101 = float(np.log(1101.0))
PHI_C = -LN1101
RTOL, ATOL, RMAX = 1e-11, 1e-13, 1.0e6


# ---------------- slices, re-typed from formulas ----------------
def sl_A1(m, a):
    def U(rho):  return 2.0 * rho**m * np.exp(-a * (rho * rho - 1.0))
    def Up(rho): return U(rho) * (m / rho - 2.0 * a * rho)
    return U, Up


def sl_A3(b):
    def U(rho):  return 2.0 * rho**2 * (1.0 + b) / (1.0 + b * rho**4)
    def Up(rho):
        return (4.0 * rho * (1.0 + b) * (1.0 + b * rho**4)
                - 2.0 * rho**2 * (1.0 + b) * 4.0 * b * rho**3) / (1.0 + b * rho**4)**2
    return U, Up


# derivative sanity: analytic U' vs central FD at a few rho (my own check on my own typing)
def check_slice(U, Up, tag):
    h = 1e-7
    worst = 0.0
    for rho in (0.7, 1.0, 1.3, 2.0):
        fd = (U(rho + h) - U(rho - h)) / (2 * h)
        worst = max(worst, abs(fd - Up(rho)) / max(abs(Up(rho)), 1e-12))
    print(f"  [slice-check {tag}] worst rel U' vs FD = {worst:.2e}")


# ---------------- EOMs, re-typed from the T3 doc equations ----------------
def make_rhs(Z, Up):
    def rhs(r, y):
        phi, phip, rho, rhop = y
        e2p = np.exp(2.0 * phi)
        sigma = 0.25 * e2p * Up(rho)
        phipp = 4.0 * rhop * rhop / (e2p * Z * rho * rho) - 2.0 * phip * rhop / rho
        rhopp = 2.0 * phip * rhop - 0.25 * Z * rho * e2p * phip * phip + sigma
        return (phip, phipp, rhop, rhopp)
    return rhs


def shoot(Z, Up, method="DOP853", rmax=RMAX, dense=False):
    seal = lambda r, y: y[0]
    seal.terminal, seal.direction = True, +1
    coll = lambda r, y: y[2] - 1e-9
    coll.terminal, coll.direction = True, -1
    sol = solve_ivp(make_rhs(Z, Up), (0.0, rmax), [PHI_C, 0.0, 1.0, 0.0],
                    method=method, rtol=RTOL, atol=ATOL, events=[seal, coll],
                    dense_output=dense)
    if sol.t_events[1].size:
        return {"status": "collapse", "sol": sol}
    if not sol.t_events[0].size:
        return {"status": "no-seal", "sol": sol}
    r_s = float(sol.t_events[0][0])
    phi_s, phip_s, rho_s, rhop_s = [float(v) for v in sol.y_events[0][0]]
    return {"status": "seal", "sol": sol, "r_s": r_s, "rho_s": rho_s,
            "rhop_s": rhop_s, "phip_s": phip_s, "q": Z * rho_s**2 * phip_s}


def miss_A1(m, Z, a, **kw):
    U, Up = sl_A1(m, a)
    o = shoot(Z, Up, **kw)
    return (o["rhop_s"] if o["status"] == "seal" else np.nan), o


def miss_A3(Z, b, **kw):
    U, Up = sl_A3(b)
    o = shoot(Z, Up, **kw)
    return (o["rhop_s"] if o["status"] == "seal" else np.nan), o


# ---------------- H in the DOC form: H = sum q' pi_q - Lbar ----------------
def H_doc(Z, U, phi, phip, rho, rhop):
    """pi_phi = Z rho^2 phi'; pi_rho = -4 e^{-2phi} rho';
    Lbar = (Z/2) rho^2 phi'^2 - 2 e^{-2phi} rho'^2 + 2 - U(rho)  (typed from the reduced action;
    EL of this Lbar reproduces the T3 EOMs -- verified symbolically in the companion script)."""
    e2p = np.exp(2.0 * phi)
    pi_phi = Z * rho**2 * phip
    pi_rho = -4.0 * rhop / e2p
    Lbar = 0.5 * Z * rho**2 * phip**2 - 2.0 * rhop**2 / e2p + 2.0 - U(rho)
    return phip * pi_phi + rhop * pi_rho - Lbar


# ---------------- my own counters (graduated floors) ----------------
FLOORS = (1e-6, 1e-7, 1e-8, 1e-9, 1e-10)


def counts(v):
    amp = float(np.max(np.abs(v)))
    out = {}
    for fl in FLOORS:
        s = np.sign(v[np.abs(v) > fl * amp])
        out[fl] = int(np.sum(s[1:] != s[:-1]))
    return out


def diagnose(o, Z, U, n=40001):
    sol, r_s = o["sol"], o["r_s"]
    rr = np.linspace(r_s * 1e-6, r_s * (1 - 1e-6), n)
    phi, phip, rho, rhop = sol.sol(rr)
    H = H_doc(Z, U, phi, phip, rho, rhop)
    m = 0.5 * rho * (1.0 - rhop**2 / np.exp(2 * phi))
    return {"r_s": r_s, "rho_s": o["rho_s"], "q": o["q"],
            "N_delta": counts(rho - 1.0), "N_rhop": counts(rhop), "N_phip": counts(phip),
            "H_drift": float(np.max(np.abs(H))),
            "dphi_minus_ln1101": float(sol.sol(r_s)[0] - PHI_C - LN1101),
            "ms_core": float(2 * m[0] / rho[0]), "ms_seal": float(2 * m[-1] / rho[-1]),
            "U_seal_ident": float(U(o["rho_s"]) - (2.0 - o["q"]**2 / (2 * Z * o["rho_s"]**2))),
            "i_max_phip": float(rr[np.argmax(np.abs(phip))] / r_s),
            "i_max_rhop": float(rr[np.argmax(np.abs(rhop))] / r_s),
            "max_abs_phip": float(np.max(np.abs(phip))),
            "max_abs_rhop": float(np.max(np.abs(rhop)))}


def sigma_two_routes(o, Z, U, Up, rvals):
    """Route (a) matter action vs route (b) geometry with MY OWN FD (h = 2e-6 r_s, 5-pt)."""
    sol, r_s = o["sol"], o["r_s"]
    h = 2e-6 * r_s
    rows = []
    for rv in rvals:
        phi, phip, rho, rhop = [float(x) for x in sol.sol(rv)]
        e2p = np.exp(2.0 * phi)
        sig_a = 0.25 * e2p * Up(rho)

        def mMS(x):
            p, _, R, Rp = sol.sol(x)
            return 0.5 * R * (1.0 - Rp**2 / np.exp(2.0 * p))
        mp = (mMS(rv - 2*h) - 8*mMS(rv - h) + 8*mMS(rv + h) - mMS(rv + 2*h)) / (12.0 * h)
        eps = mp / (4.0 * np.pi * rho**2 * rhop)
        sig_b = 0.5 * rho * e2p * (1.0/rho**2 - (rhop**2/rho**2 + 2*phip*rhop/rho)/e2p
                                   + 0.5*Z*phip**2 - 8.0*np.pi*eps)
        rows.append((rv, sig_a, sig_b, abs(sig_b - sig_a)/abs(sig_a)))
    return rows


def main():
    rng = np.random.default_rng(20260703)
    J = json.load(open("/home/udt-admin/udt_mass_codex/microphysics_E0_ambient_tables.json"))

    # ================= ATTACK 1a: A1 m=3 Z=8 re-shoot =================
    print("=========== A1 m=3 Z=8 (independent re-shoot, DOP853) ===========")
    U, Up = sl_A1(3.0, 1.4813439683)   # slice at nominal a only for check; root refound below
    check_slice(*sl_A1(3.0, 1.4813439683), "A1 m=3 a~1.4813")
    f = lambda a: miss_A1(3.0, 8.0, a)[0]
    lo, hi = 1.48125, 1.48145
    flo, fhi = f(lo), f(hi)
    print(f"  bracket miss: f({lo})={flo:+.4e}  f({hi})={fhi:+.4e}")
    a1 = brentq(f, lo, hi, xtol=1e-13, rtol=1e-15)
    print(f"  MY a* = {a1:.13f}   (E0 re-shot 1.4813439682567, banked 1.4813439688814)")
    U, Up = sl_A1(3.0, a1)
    _, o = miss_A1(3.0, 8.0, a1, dense=True)
    d = diagnose(o, 8.0, U)
    print(f"  r_s={o['r_s']:.6f} rho_s={o['rho_s']:.8f} q={o['q']:.10f}")
    for k in ("H_drift", "dphi_minus_ln1101", "ms_core", "ms_seal", "U_seal_ident"):
        print(f"  {k} = {d[k]:.6e}" if isinstance(d[k], float) else f"  {k} = {d[k]}")
    print(f"  N_delta={d['N_delta']} N_rhop={d['N_rhop']} N_phip={d['N_phip']}")
    print(f"  argmax|phip|/r_s={d['i_max_phip']:.6f} (val {d['max_abs_phip']:.4f}); "
          f"argmax|rhop|/r_s={d['i_max_rhop']:.6f} (val {d['max_abs_rhop']:.4f})")

    # spot-check vs JSON at 5 seeded-random interior radii + both folds
    b = J["brackets"]["A1 m=3 Z=8"]
    pr = b["profiles"]
    rj = np.array(pr["r"])
    interior = np.where((rj > 0.05 * b["r_s"]) & (rj < 0.95 * b["r_s"]))[0]
    picks = sorted(rng.choice(interior, 5, replace=False).tolist()) + [0, len(rj) - 1]
    print("  --- spot-check vs JSON (5 random interior + both folds) ---")
    print("  r | field | JSON | mine | rel diff")
    worst = {}
    for i in picks:
        rv = rj[i]
        phi, phip, rho, rhop = [float(x) for x in o["sol"].sol(rv)]
        mine = {"phi": phi, "phip": phip, "rho": rho, "rhop": rhop,
                "sigma_ma": 0.25 * np.exp(2 * phi) * Up(rho)}
        for k in ("phi", "phip", "rho", "rhop", "sigma_ma"):
            jv = pr[k][i]
            dv = abs(mine[k] - jv) / max(abs(jv), 1e-300) if jv != 0 else abs(mine[k])
            worst[k] = max(worst.get(k, 0.0), dv)
            print(f"  {rv:12.5f} {k:9s} {jv:+.10e} {mine[k]:+.10e} {dv:.2e}")
        if pr["sigma_geo"][i] is not None:
            rows = sigma_two_routes(o, 8.0, U, Up, [rv])
            _, sa, sb, rr_ = rows[0]
            dg = abs(sb - pr["sigma_geo"][i]) / abs(pr["sigma_geo"][i])
            worst["sigma_geo"] = max(worst.get("sigma_geo", 0.0), dg)
            print(f"  {rv:12.5f} sigma_geo {pr['sigma_geo'][i]:+.10e} {sb:+.10e} {dg:.2e} "
                  f"(my two-route rel {rr_:.2e})")
    print("  worst rel diffs:", {k: f"{v:.2e}" for k, v in worst.items()})

    # ATTACK 3: sigma two routes at 5 fresh points (my own FD)
    r_s = o["r_s"]
    print("  --- sigma two-route (my implementation) at 5 points ---")
    for rv, sa, sb, rr_ in sigma_two_routes(o, 8.0, U, Up,
                                            [0.15*r_s, 0.35*r_s, 0.55*r_s, 0.75*r_s, 0.93*r_s]):
        print(f"  r={rv:10.3f}  sig_ma={sa:+.8e}  sig_geo={sb:+.8e}  rel={rr_:.2e}")

    # plateau value vs -ln(1101)
    phi_plateau = float(o["sol"].sol(0.25 * r_s)[0])
    print(f"  phi(0.25 r_s) = {phi_plateau:.8f} vs -ln1101 = {PHI_C:.8f} "
          f"(diff {phi_plateau - PHI_C:+.2e}); phi(0)={float(o['sol'].sol(0.0)[0]):+.10f}")

    # ================= ATTACK 1b + 6: A3 Z=1 fresh, independent ==============
    print("\n=========== A3 Z=1 (independent hunt, DOP853) ===========")
    check_slice(*sl_A3(0.99), "A3 b=0.99")
    g = lambda p: miss_A3(1.0, p)[0]
    # my own scan of the dip region (uniform, NOT the E0 grid)
    grid = np.linspace(0.9910, 0.9958, 25)
    vals = [(p, g(p)) for p in grid]
    print("  my dip scan:")
    for p, v in vals:
        print(f"    b={p:.6f}  miss={v:+.6e}")
    roots = []
    for (p1, v1), (p2, v2) in zip(vals, vals[1:]):
        if np.isfinite(v1) and np.isfinite(v2) and v1 * v2 < 0:
            roots.append(float(brentq(g, p1, p2, xtol=1e-13, rtol=1e-15)))
    print(f"  sign-change roots found in [0.9910,0.9958]: {[f'{x:.10f}' for x in roots]}")
    for x in roots:
        U3, Up3 = sl_A3(x)
        _, o3 = miss_A3(1.0, x, dense=True)
        d3 = diagnose(o3, 1.0, U3)
        print(f"    b*={x:.10f}: N_delta={d3['N_delta']} N_rhop={d3['N_rhop']} "
              f"q={d3['q']:.6f} r_s={d3['r_s']:.4f} rho_s={d3['rho_s']:.8f} "
              f"Hdrift={d3['H_drift']:.2e} dphi-ln1101={d3['dphi_minus_ln1101']:+.2e} "
              f"ms={d3['ms_core']:.6f}/{d3['ms_seal']:.6f} Useal_id={d3['U_seal_ident']:+.2e}")
        if abs(x - 0.9928086030) < 2e-4:
            print(f"    argmax|phip|/r_s={d3['i_max_phip']:.6f} ({d3['max_abs_phip']:.4f}); "
                  f"argmax|rhop|/r_s={d3['i_max_rhop']:.6f} ({d3['max_abs_rhop']:.4f})")
            print("    sigma two-route at 3 pts:")
            for rv, sa, sb, rr_ in sigma_two_routes(o3, 1.0, U3, Up3,
                                                    [0.3*d3['r_s'], 0.6*d3['r_s'], 0.9*d3['r_s']]):
                print(f"      r={rv:9.2f} sig_ma={sa:+.6e} sig_geo={sb:+.6e} rel={rr_:.2e}")
            ph0 = float(o3["sol"].sol(0.25 * d3["r_s"])[0])
            print(f"    phi(0.25 r_s)={ph0:.8f} vs -ln1101={PHI_C:.8f} (diff {ph0-PHI_C:+.2e})")

    # the coarse-grid "first crossing" claim: refine E0's coarse bracket (0.995277, 0.996970)
    print("  --- coarse first-crossing member (E0 claims N=2) ---")
    xc = float(brentq(g, 0.995277, 0.996970, xtol=1e-13, rtol=1e-15))
    U3, Up3 = sl_A3(xc)
    _, oc = miss_A3(1.0, xc, dense=True)
    dc = diagnose(oc, 1.0, U3)
    print(f"  b*={xc:.10f}  N_delta={dc['N_delta']} N_rhop={dc['N_rhop']} q={dc['q']:.6f}")

    # ATTACK 6 probe: the ABOVE-stuck bracket the E0 hunt skipped: (1.0015, 1.0040)
    print("  --- ABOVE-stuck skipped bracket (1.0015, 1.0040) ---")
    v1, v2 = g(1.0015), g(1.0040)
    print(f"  miss(1.0015)={v1:+.5e}  miss(1.0040)={v2:+.5e}")
    if np.isfinite(v1) and np.isfinite(v2) and v1 * v2 < 0:
        xa = float(brentq(g, 1.0015, 1.0040, xtol=1e-13, rtol=1e-15))
        U3, Up3 = sl_A3(xa)
        _, oa = miss_A3(1.0, xa, dense=True)
        da = diagnose(oa, 1.0, U3)
        print(f"  ABOVE-STUCK ROOT b*={xa:.10f}: N_delta={da['N_delta']} "
              f"N_rhop={da['N_rhop']} q={da['q']:.6f} r_s={da['r_s']:.4f} "
              f"Hdrift={da['H_drift']:.2e}")


if __name__ == "__main__":
    main()

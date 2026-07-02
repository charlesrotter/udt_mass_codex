"""T3 shooter -- the FLUX-SEALED UNIVERSE CELL (round-static Branch-P, sigma-slices).

Object (all boundary structure DERIVED, universe_cell_fold_jc_sigma_results.md):
  inner even fold r_c=0:  phi'(0)=rho'(0)=0, rho_c>0            # THEORY (D1: stationarity alone)
  outer odd fold  r_s  :  phi(r_s)=0  AND  rho'(r_s)=0          # THEORY (D1-derived; rho'_s=0 robust, 3 routes)
  anchor          phi_c = -ln(1101)                              # OBSERVATIONAL PIN (Delta-phi reading, Charles-ruled 2026-07-02)
  breathing edges H_tot == 0  =>  U(rho_c) = 2                   # THEORY (transversality) + Charles RULING 2026-07-02
  matter          potential-only phi-blind L_m = -U(rho)         # CHOSE (T3 slice family; D3: realizes any smooth sigma)
  slice shapes    u(rho) below                                   # CHOSE (labeled slices per T3 pre-registration)
  Z in {1, 8}                                                    # FREE-and-explored (Route A: Z_phi FREE, no mixing
                                                                 # term forced; 8 = Route-B's value carried as a probe,
                                                                 # NOT derived. Tension RESOLVED 2026-07-02: nothing on
                                                                 # the live path claims Z=8 derived; both Z run always.
                                                                 # Z is now observationally constrained by derived laws:
                                                                 # window ceiling ~sqrt(Z), a_seal ~ sqrt(Z), q ~ Z --
                                                                 # the Route fork = a consilience/observation call later.)
  r_c = 0                                                        # gauge pin
EOMs (banked, CAS-verified; cell_solver_round.py + derive_universe_*):
  phi'' = 4 e^{-2phi} rho'^2/(Z rho^2) - 2 phi' rho'/rho
  rho'' = 2 phi' rho' - (Z/4) rho e^{2phi} phi'^2 + sigma ,  sigma = (e^{2phi}/4) U'(rho)   [D3, potential-only]
Counting (Charles-checked, square per slice): closure U(rho_c)=2 absorbed into the slice
normalization => ONE unknown per shot vs ONE seal condition rho'(r_s)=0 at the phi=0 crossing.
POWER-LAW slices are homothety-covariant (rho_c drops out entirely -- rho_c=1 WLOG, the root
lands on the SHAPE parameter n; scale is a free family, consistent with T2 window=shape).
SCALEFUL slices (intrinsic scale in u: CHOSE) break the degeneracy -> isolated rho_c possible.
Acceptance identities per solution (T2, blind-verified): H_tot drift ~ 0; MS marginality
m=rho/2 at BOTH edges (specialized form, Charles rider 1); q = Z rho_s^2 phi'_s = 4*int(1-2m/rho);
U(rho_s) = 2 - q^2/(2 Z rho_s^2)  [conservation identity -- solver check, not physics].
Window report (Charles rider 2, UNLABELED): q vs 2*rho_s*sqrt(Z) per (slice, Z)
[upper side rides on H_m(seal)>=0 = FRESH PREMISE, tagged in universe_cell_T2_identities_results.md];
lower bound q >= Z*Dphi/int(dr/rho^2) [derived; automatic on exact solutions -- reported as margin].
Anti-hang: 1-D IVP shooting, CPU, adaptive; every scan bounded; single process.
"""
import numpy as np
from scipy.integrate import solve_ivp

LN1101 = float(np.log(1101.0))   # anchor magnitude: OBSERVATIONAL PIN (1+z_CMB = e^Dphi, canon)
PHI_C = -LN1101                  # fold pins phi(r_s)=0 => phi_c = -ln(1101)   # THEORY (D1)


# ----------------------------------------------------------------------------- slices (CHOSE)
def make_power_slice(n, rho_c=1.0):
    """U(rho) = 2*(rho/rho_c)^n  -- closure U(rho_c)=2 built in; homothety-covariant (rho_c WLOG 1)."""
    def U(rho):  return 2.0 * (rho / rho_c) ** n
    def Up(rho): return 2.0 * n * rho ** (n - 1.0) / rho_c ** n
    return U, Up, f"power n={n:+.4f}"


def make_risefall_slice(a, m=2.0, rho_c=1.0):
    """U(rho) = 2*(rho/rho_c)^m * exp(-a*((rho/rho_c)^2 - 1))  -- rise-then-fall potential.
    CHOSE (slice 3). Motivation is ANALYTIC, not a fit: the T2-C conservation identity requires
    U(rho_s) = 2 - q^2/(2 Z rho_s^2) < 2 = U(rho_c) at any closed seal, so closure needs U to
    rise from 2 then FALL below 2 by the seal -- a sign-changing sigma, inexpressible in the
    monotone families (both scanned: no closure, consistent with the identity). a=0 recovers
    power n=m. U(rho_c)=2 closure built in; homothety-covariant (rho_c WLOG 1)."""
    def U(rho):
        x = rho / rho_c
        return 2.0 * x ** m * np.exp(-a * (x * x - 1.0))
    def Up(rho):
        x = rho / rho_c
        return (2.0 * x ** m * np.exp(-a * (x * x - 1.0))) * (m / x - 2.0 * a * x) / rho_c
    return U, Up, f"risefall m={m} a={a:+.4f}"


def make_scaleful_slice(rho_c, c4=1.0):
    """U(rho) = 2*(rho^2 + c4*rho^4)/(rho_c^2 + c4*rho_c^4) -- intrinsic scale via the relative
    weight of the two powers (c4: CHOSE, fixed across the scan -- no per-solution retuning)."""
    norm = rho_c ** 2 + c4 * rho_c ** 4
    def U(rho):  return 2.0 * (rho ** 2 + c4 * rho ** 4) / norm
    def Up(rho): return 2.0 * (2.0 * rho + 4.0 * c4 * rho ** 3) / norm
    return U, Up, f"scaleful c4={c4} rho_c={rho_c:.4f}"


# ----------------------------------------------------------------------------- shoot
def rhs(r, y, Z, Up):
    phi, phip, rho, rhop = y
    e2p = np.exp(2.0 * phi)
    sigma = 0.25 * e2p * Up(rho)                       # D3 potential-only source
    phipp = 4.0 * rhop * rhop / (e2p * Z * rho * rho) - 2.0 * phip * rhop / rho
    rhopp = 2.0 * phip * rhop - 0.25 * Z * rho * e2p * phip * phip + sigma
    return [phip, phipp, rhop, rhopp]


def shoot(Z, U, Up, rho_c, r_max=5.0e7, rtol=1e-10, atol=1e-12):
    """Integrate from the inner fold to the phi=0 crossing. Returns dict (status + seal data)."""
    seal = lambda r, y, *a: y[0]                        # phi = 0 crossing = the odd fold
    seal.terminal, seal.direction = True, +1
    collapse = lambda r, y, *a: y[2] - 1e-9 * rho_c     # rho -> 0 termination (metric degeneration)
    collapse.terminal, collapse.direction = True, -1
    sol = solve_ivp(rhs, (0.0, r_max), [PHI_C, 0.0, rho_c, 0.0], args=(Z, Up),
                    method="LSODA", rtol=rtol, atol=atol, events=[seal, collapse],
                    dense_output=True)
    out = {"status": "no-seal", "sol": sol}
    if sol.t_events[1].size:
        out["status"] = "collapse"; return out
    if not sol.t_events[0].size:
        return out                                       # phi never reached 0 within r_max (report honestly)
    r_s = sol.t_events[0][0]
    phi_s, phip_s, rho_s, rhop_s = sol.y_events[0][0]
    e_geo = 0.5 * Z * rho_s ** 2 * phip_s ** 2 - 2.0 * np.exp(-2.0 * phi_s) * rhop_s ** 2
    out.update(status="seal", r_s=r_s, rho_s=rho_s, rhop_s=rhop_s,
               q=Z * rho_s ** 2 * phip_s, H_seal=e_geo - 2.0 + U(rho_s))
    return out


def miss(Z, U, Up, rho_c, **kw):
    """Root function: rho'(r_s) at the phi=0 crossing (nan if no seal reached)."""
    o = shoot(Z, U, Up, rho_c, **kw)
    return (o["rhop_s"] if o["status"] == "seal" else np.nan), o


# ----------------------------------------------------------------------------- diagnostics (T2)
def diagnose(o, Z, U):
    """Acceptance identities + UNLABELED window report for a converged (rho'_s ~ 0) solution."""
    sol, r_s, rho_s, q = o["sol"], o["r_s"], o["rho_s"], o["q"]
    rr = np.linspace(0.0, r_s, 4001)
    phi, phip, rho, rhop = sol.sol(rr)
    e2p = np.exp(2.0 * phi)
    H = 0.5 * Z * rho ** 2 * phip ** 2 - 2.0 * rhop ** 2 / e2p - 2.0 + U(rho)   # H_tot (== 0 exact)
    m = 0.5 * rho * (1.0 - rhop ** 2 / e2p)                                     # Misner-Sharp
    inv_rho2 = np.trapezoid(1.0 / rho ** 2, rr)
    q_int = 4.0 * np.trapezoid(1.0 - 2.0 * m / rho, rr)                         # T2-A integral
    return {
        "r_s": r_s, "rho_s": rho_s, "rho_c": rho[0], "q": q,
        "H_drift": float(np.max(np.abs(H))),
        "ms_core": (2.0 * m[0] / rho[0]),  "ms_seal": (2.0 * m[-1] / rho[-1]),  # both -> 1 (marginal)
        "q_vs_integral_rel": abs(q - q_int) / abs(q) if q else np.nan,
        "U_seal": U(rho_s),                                                     # = 2 - q^2/(2 Z rho_s^2) by conservation
        "U_seal_identity_res": U(rho_s) - (2.0 - q ** 2 / (2.0 * Z * rho_s ** 2)),
        "q_upper": 2.0 * rho_s * np.sqrt(Z),                                    # specialized bound (rho'_s=0)
        "window_upper_ok": bool(q <= 2.0 * rho_s * np.sqrt(Z)),                 # <=> U_seal >= 0 (premise-tagged)
        "q_lower": Z * LN1101 / inv_rho2,                                       # derived lower bound
        "lower_margin": q / (Z * LN1101 / inv_rho2),
        "int_dr_rho2": inv_rho2, "rho_min": float(rho.min()),
        "rho_nonmonotone": bool(np.any(np.diff(rho) < 0) and np.any(np.diff(rho) > 0)),
    }


# ----------------------------------------------------------------------------- scans (bounded)
def scan_power(Z, n_grid, rho_c=1.0):
    """rho'_s vs n curve + bisected roots. rho_c=1 WLOG (homothety); degeneracy checked separately."""
    rows, roots = [], []
    for n in n_grid:
        U, Up, _ = make_power_slice(n, rho_c)
        f, o = miss(Z, U, Up, rho_c)
        rows.append((n, f, o["status"], o.get("q", np.nan), o.get("rho_s", np.nan)))
    for (n1, f1, s1, *_), (n2, f2, s2, *_) in zip(rows, rows[1:]):
        if s1 == s2 == "seal" and np.isfinite(f1) and np.isfinite(f2) and f1 * f2 < 0:
            a, b, fa = n1, n2, f1
            for _ in range(60):                                   # bounded bisection
                mid = 0.5 * (a + b)
                U, Up, _ = make_power_slice(mid, rho_c)
                fm, om = miss(Z, U, Up, rho_c)
                if not np.isfinite(fm): break
                if fa * fm <= 0: b = mid
                else: a, fa = mid, fm
            U, Up, lab = make_power_slice(0.5 * (a + b), rho_c)
            fm, om = miss(Z, U, Up, rho_c)
            if om["status"] == "seal":
                roots.append((0.5 * (a + b), diagnose(om, Z, U)))
    return rows, roots


def scan_scaleful(Z, rho_c_grid, c4=1.0):
    """rho'_s vs rho_c for the intrinsic-scale slice (isolated rho_c = discreteness locus if any)."""
    rows, roots = [], []
    for rc in rho_c_grid:
        U, Up, _ = make_scaleful_slice(rc, c4)
        f, o = miss(Z, U, Up, rc)
        rows.append((rc, f, o["status"], o.get("q", np.nan), o.get("rho_s", np.nan)))
    for (r1, f1, s1, *_), (r2, f2, s2, *_) in zip(rows, rows[1:]):
        if s1 == s2 == "seal" and np.isfinite(f1) and np.isfinite(f2) and f1 * f2 < 0:
            a, b, fa = r1, r2, f1
            for _ in range(60):
                mid = 0.5 * (a + b)
                U, Up, _ = make_scaleful_slice(mid, c4)
                fm, om = miss(Z, U, Up, mid)
                if not np.isfinite(fm): break
                if fa * fm <= 0: b = mid
                else: a, fa = mid, fm
            U, Up, lab = make_scaleful_slice(0.5 * (a + b), c4)
            fm, om = miss(Z, U, Up, 0.5 * (a + b))
            if om["status"] == "seal":
                roots.append((0.5 * (a + b), diagnose(om, Z, U)))
    return rows, roots


if __name__ == "__main__":
    # Null check (derived expectation): U = const => sigma = 0 => even-fold vacuum = constant
    # cylinder (blind-verified corollary) => phi must NEVER move; a seal-reach here = solver bug.
    U0, Up0 = (lambda rho: 2.0), (lambda rho: 0.0)
    o = shoot(8.0, U0, Up0, 1.0, r_max=1e4)
    print(f"[null U=const] status={o['status']} (expect no-seal)")

    for Z in (1.0, 8.0):
        print(f"\n===== Z = {Z:g} =====")
        rows, roots = scan_power(Z, np.linspace(-4.0, 4.0, 33))
        for n, f, s, q, rho_s in rows:
            print(f"  n={n:+7.3f}  rho'_s={f if np.isfinite(f) else float('nan'):+12.4e}  [{s}]"
                  + (f"  q={q:9.4g} rho_s={rho_s:9.4g}" if s == 'seal' else ""))
        for n, d in roots:
            print(f"  ROOT n*={n:+.6f}:")
            for k, v in d.items(): print(f"      {k:22s} = {v}")
        # homothety degeneracy check at one root (rho_c=2 must reproduce the root, scaled)
        if roots:
            n0 = roots[0][0]
            U, Up, _ = make_power_slice(n0, 2.0)
            f, o2 = miss(Z, U, Up, 2.0)
            print(f"  [homothety check n*={n0:+.4f}, rho_c=2] rho'_s={f:+.3e} (expect ~0; scale family)")
        rows2, roots2 = scan_scaleful(Z, np.linspace(0.05, 4.0, 25))
        seal_rows = [(rc, f) for rc, f, s, *_ in rows2 if s == "seal"]
        print(f"  [scaleful c4=1] seal-reaching rho_c points: {len(seal_rows)}/{len(rows2)}")
        for rc, f in seal_rows: print(f"      rho_c={rc:7.4f}  rho'_s={f:+12.4e}")
        for rc, d in roots2:
            print(f"  SCALEFUL ROOT rho_c*={rc:.6f}:")
            for k, v in d.items(): print(f"      {k:22s} = {v}")

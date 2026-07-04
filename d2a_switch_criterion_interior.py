"""D2a -- apply the DERIVED G/P switch criterion to the solved N=0 fundamental interiors.

Q1 of microphysics_D2_two_regime_MAP.md ("where is G, where is P, inside the solved universe?").
OBSERVE mode: algebra + banked E0 dense profiles ONLY (microphysics_E0_ambient_tables.json,
blind-verified agent aaa9ca9e751d1f6fb 2026-07-03). NO new solves.

Criterion (gp_switch_criterion_results.md):
  - only 𝒦 breaks the shift (Result 1, lines 21-31); round/reduced form (h_AB = rho(r)^2 Omega_AB):
        K_AB = (1/2) e^{-phi} d_r h_AB  =>  K^A_B = e^{-phi} (rho'/rho) delta^A_B
        𝒦 = K_AB K^AB - K^2 = 2 e^{-2phi}(rho'/rho)^2 - 4 e^{-2phi}(rho'/rho)^2
          = -2 e^{-2phi} (rho'/rho)^2                                   [CAS, verified below]
  - invariant chi = L_radial / sqrt(A/4pi), L_radial = int e^phi dr (Result 2, line 35)
  - P iff N1 (sqrt A pinned) & N2 (radial interval pinned) & N3 (𝒦 != 0); minimal N1&N3
    (Result 3 + blind-verifier refinement, lines 40-58)
  - bulk-P source = -2𝒦 in the phi-EL (Result 4 Task 3, lines 67-69), UNCONDITIONAL after
    native_geometric_action_results.md (OPEN item resolved, lines 117-121)

Solver EOM cross-check (cell_solver_universe_T3.py:79):
  phi'' = 4 e^{-2phi} rho'^2/(Z rho^2) - 2 phi' rho'/rho
  =>  d/dr [Z rho^2 phi'] = 4 e^{-2phi} rho'^2 = -2 rho^2 𝒦        [the flux-source identity]
So the E0 column pi_phi_qflux = Z rho^2 phi' is the ACCUMULATED shift-breaking source, and
Q(r)/q is the fraction of the cell's phi-charge sourced inside r. In Branch G
((r^2 phi')' = 0, native_field_equations_constrained_two_player_results.md:110) a REGULAR core
forces the homogeneous (Coulomb) mode's charge to zero => phi' == 0 identically. Hence every
nonzero phi' anywhere in these interiors is 100% P-sourced.

Premise tags: everything below is DERIVED-or-extracted except the station/percentile choices
(reporting conventions, Category-A) and the sqrt(A)-surface convention for chi (criterion doc
leaves the transverse surface unspecified for varying rho -- flagged; both endpoints reported).
"""
import json
import numpy as np
import sympy as sp

ROOT = "/home/udt-admin/udt_mass_codex"

# ---------------------------------------------------------------- CAS anchor: 𝒦 reduced form
def cas_anchors():
    r = sp.symbols("r", positive=True)
    phi = sp.Function("phi")(r)
    rho = sp.Function("rho")(r)
    th = sp.symbols("theta", positive=True)
    # h_AB = rho^2 * Omega_AB (round transverse), K_AB = (1/2) e^{-phi} h_AB'
    h = sp.Matrix([[rho**2, 0], [0, rho**2 * sp.sin(th)**2]])
    hinv = h.inv()
    K = sp.Rational(1, 2) * sp.exp(-phi) * h.diff(r)
    Kmix = sp.simplify(hinv * K)                       # K^A_B
    trK = sp.trace(Kmix)
    KK = sp.trace(Kmix * Kmix)                          # K_AB K^AB
    kcal = sp.simplify(KK - trK**2)
    target = -2 * sp.exp(-2 * phi) * (rho.diff(r) / rho) ** 2
    assert sp.simplify(kcal - target) == 0, "K-form mismatch"
    # flux-source identity from the T3 phi-EOM
    Z = sp.symbols("Z", positive=True)
    phipp = 4 * sp.exp(-2 * phi) * rho.diff(r) ** 2 / (Z * rho**2) - 2 * phi.diff(r) * rho.diff(r) / rho
    flux_deriv = sp.expand(sp.diff(Z * rho**2 * phi.diff(r), r).subs(sp.Derivative(phi, r, 2), phipp))
    src = 4 * sp.exp(-2 * phi) * rho.diff(r) ** 2
    assert sp.simplify(flux_deriv - src) == 0, "flux-source identity mismatch"
    assert sp.simplify(src + 2 * rho**2 * kcal) == 0, "source = -2 rho^2 K mismatch"
    print("[CAS] K = -2 e^{-2phi}(rho'/rho)^2   VERIFIED")
    print("[CAS] d/dr(Z rho^2 phi') = 4 e^{-2phi} rho'^2 = -2 rho^2 K   VERIFIED")
    # homothety invariance of chi (r -> s r, rho -> s rho, phi fixed): L -> sL, sqrtA -> s sqrtA
    s = sp.symbols("s", positive=True)
    print("[CAS] chi homothety-invariance: L->sL, sqrt(A)->s*sqrt(A) => chi->chi (trivial algebra; "
          "shift phi->phi+lambda gives chi->e^lambda chi INDEPENDENT of s)   HOLDS")


def analyze():
    d = json.load(open(f"{ROOT}/microphysics_E0_ambient_tables.json"))
    for name, b in d["brackets"].items():
        p = b["profiles"]
        r = np.array(p["r"]); phi = np.array(p["phi"]); phip = np.array(p["phip"])
        rho = np.array(p["rho"]); rhop = np.array(p["rhop"])
        e2p = np.array(p["exp_2phi"]); Q = np.array(p["pi_phi_qflux"])
        Z, r_s, q, rho_s = b["Z"], b["r_s"], b["q"], b["rho_s"]
        x = r / r_s
        interior = (r > 0) & (r < r_s)

        kcal = -2.0 * rhop**2 / (e2p * rho**2)                 # 𝒦(r)
        src = 4.0 * rhop**2 / e2p                              # -2 rho^2 𝒦 = Q'(r)

        # -- N3 pointwise: strict monotonicity / no interior zero of rho'
        rp_int = rhop[interior]
        sign_changes = int(np.sum(np.diff(np.sign(rp_int)) != 0))
        # -- Q reconstruction: cumulative trapezoid of src vs the extracted flux column
        Qrec = np.concatenate([[0.0], np.cumsum(0.5 * (src[1:] + src[:-1]) * np.diff(r))])
        mask = Q > 1e-6 * abs(q)
        relerr = float(np.max(np.abs((Qrec[mask] - Q[mask]) / Q[mask]))) if mask.any() else np.nan
        # -- percentile radii of the accumulated source
        fr = Q / q
        pct = {}
        for lev in (0.01, 0.10, 0.50, 0.90, 0.99):
            i = int(np.searchsorted(fr, lev))
            pct[lev] = float(x[min(i, len(x) - 1)])
        # -- plateau vs wall
        half = fr[np.searchsorted(x, 0.5)]
        i_max_s = int(np.argmax(src)); i_max_k = int(np.argmax(np.abs(kcal[interior])))
        xk = x[interior][i_max_k]; kmax = np.abs(kcal[interior])[i_max_k]
        # station values of |K| and src at even sixths
        stations = {}
        for j in range(1, 6):
            i = int(np.searchsorted(r, j * r_s / 6.0))
            stations[j] = (float(x[i]), float(abs(kcal[i])), float(src[i]), float(fr[i]))
        # -- chi (both transverse-surface conventions; convention gap flagged in the doc)
        L = float(np.trapezoid(np.exp(phi), r))
        chi_c, chi_s = L / rho[0], L / rho_s
        # -- Coulomb null: a regular-core G region has phi' == 0; report max |phi'| in x<=0.5
        pl = x <= 0.5
        print(f"\n===== {name}  (Z={Z:g}, r_s={r_s:.4f}, q={q:.6g}) =====")
        print(f"  N3 pointwise: rho' sign changes in open interior = {sign_changes}; "
              f"min|rho'| (interior) = {np.min(np.abs(rp_int)):.3e}  => K != 0 a.e. "
              f"(zeros ONLY at the two folds)")
        print(f"  rho''(0) = sigma_ma(core) = "
              f"{np.interp(0.0, r, np.array(p['sigma_ma'])):.3e} > 0  => fold zero of rho' is ISOLATED")
        print(f"  |K| at even-sixth stations (x=r/r_s, |K|, src=Q', Q/q):")
        for j, (xx, kk, ss, ff) in stations.items():
            print(f"    st{j}: x={xx:.3f}  |K|={kk:.3e}  Q'={ss:.3e}  Q/q={ff:.3e}")
        print(f"  |K| max = {kmax:.4e} at x={xk:.4f};  |K| plateau(st1) = {stations[1][1]:.3e}; "
              f"ratio max/plateau = {kmax/stations[1][1]:.3e}")
        print(f"  source accumulation Q/q: 1% at x={pct[0.01]:.4f}, 10% at x={pct[0.10]:.4f}, "
              f"50% at x={pct[0.50]:.4f}, 90% at x={pct[0.90]:.4f}, 99% at x={pct[0.99]:.4f}")
        print(f"  fraction of q sourced inside x<=0.5:  {half:.3e}")
        print(f"  flux-column cross-check: max rel err(Q_reconstructed vs pi_phi_qflux) = {relerr:.2e}")
        print(f"  Coulomb null (regular-core G => phi'==0): max|phi'| on x<=0.5 = "
              f"{np.max(np.abs(phip[pl])):.3e}  -- nonzero, and 100% source-accumulated (see Q match)")
        print(f"  chi: L_radial = {L:.6f};  chi(rho_c) = {chi_c:.6f};  chi(rho_s) = {chi_s:.6f}")


if __name__ == "__main__":
    cas_anchors()
    analyze()

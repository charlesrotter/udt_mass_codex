"""bv16 numeric attack: Y3(ii) inequivalence + Y4(c) values on the two banked rungs.
Shot ledger: shot1 = rung0 (a=1.4813439655172531), shot2 = rung1 (a=1.4903071093405713).
Z=8, risefall m=3, rho_c=1, solver-default tolerances. CPU, single process."""
import sys, numpy as np
sys.path.insert(0, '/home/udt-admin/udt_mass_codex')
from cell_solver_universe_T3 import make_risefall_slice, shoot, LN1101

Z = 8.0
JSON_REF = {  # from cascade_stageB_rungs.json (for reproduction check only)
    'rung0': dict(a=1.4813439655172531, rho_s=2.2614034898623525, r_s=577.5026522756837,
                  q=12.624451257557586),
    'rung1': dict(a=1.4903071093405713, rho_s=0.6426014077682966, r_s=847.8866403225392,
                  q=2.1916694402365264),
}

for tag in ('rung0', 'rung1'):
    ref = JSON_REF[tag]
    U, Up, lab = make_risefall_slice(ref['a'], m=3.0, rho_c=1.0)
    o = shoot(Z, U, Up, 1.0)
    assert o['status'] == 'seal', o['status']
    r_s, rho_s, q, rhop_s = o['r_s'], o['rho_s'], o['q'], o['rhop_s']
    print(f"\n===== {tag}  ({lab}, Z={Z:g}) =====")
    print(f"  reproduction: r_s={r_s:.10g} (ref {ref['r_s']:.10g}, rel {abs(r_s/ref['r_s']-1):.2e})")
    print(f"                rho_s={rho_s:.10g} (ref {ref['rho_s']:.10g}, rel {abs(rho_s/ref['rho_s']-1):.2e})")
    print(f"                q={q:.10g} (ref {ref['q']:.10g}, rel {abs(q/ref['q']-1):.2e})")
    print(f"                rho'(r_s)={rhop_s:+.3e} (root residual), H_seal={o['H_seal']:+.3e}")

    rr = np.linspace(0.0, r_s, 400001)
    phi_, phip_, rho_, rhop_ = o['sol'].sol(rr)
    e2p = np.exp(2.0*phi_)
    Uv, Upv = U(rho_), Up(rho_)

    # banked L and H
    L = 0.5*Z*rho_**2*phip_**2 - 2.0*rhop_**2/e2p + 2.0 - Uv
    H = 0.5*Z*rho_**2*phip_**2 - 2.0*rhop_**2/e2p - 2.0 + Uv
    print(f"  H drift: max|H| = {np.max(np.abs(H)):.3e}  (H==0 on cell)")

    intL = np.trapezoid(L, rr)
    intL_onshell = np.trapezoid(4.0 - 2.0*Uv, rr)                      # Y2.i on-shell form
    bnd = (-2.0*rho_*rhop_/e2p)[-1] - (-2.0*rho_*rhop_/e2p)[0]         # Y2.ii boundary term
    intL_chain = bnd + np.trapezoid(2.0 - Uv + 0.5*rho_*Upv, rr)       # Y2.ii chain form
    print(f"  int L dr           = {intL:+.8g}")
    print(f"  int (4-2U) dr      = {intL_onshell:+.8g}   (rel diff {abs(intL_onshell/intL-1):.2e})")
    print(f"  chain form         = {intL_chain:+.8g}   (boundary term = {bnd:+.3e})")

    # MS mass
    m = 0.5*rho_*(1.0 - rhop_**2/e2p)
    m_c, m_s = m[0], m[-1]
    dm = (rho_s - 1.0)/2.0
    print(f"  m_c={m_c:.8g} (rho_c/2=0.5), m_s={m_s:.8g} (rho_s/2={rho_s/2:.8g}), dm=(rho_s-rho_c)/2={dm:+.8g}")
    print(f"  m[-1]-m[0] = {m_s-m_c:+.8g} (vs dm rel {abs((m_s-m_c)/dm-1):.2e})")

    # epsilon (on-shell reduction of -G^t_t/8pi, CAS-derived above)
    eps8 = (0.5*Z*rho_**2*phip_**2 - 0.5*rho_*Upv - 2.0*rho_*phip_*rhop_/e2p
            + 1.0 - rhop_**2/e2p)
    eps = eps8/(8.0*np.pi*rho_**2)
    # independent check of m' = 4 pi rho^2 rho' eps via finite differences of m(r)
    mp_fd = np.gradient(m, rr)
    rhs_ms = 4.0*np.pi*rho_**2*rhop_*eps
    i_int = slice(200, -200)
    denom = np.max(np.abs(rhs_ms[i_int])) or 1.0
    print(f"  MS-identity FD check: max|m'_fd - 4pi rho^2 rho' eps| / max = "
          f"{np.max(np.abs(mp_fd[i_int]-rhs_ms[i_int]))/denom:.2e}")
    frac_r = np.mean(eps > 0)
    w = np.exp(phi_)                       # proper radial length weight
    frac_proper = np.trapezoid(w*(eps > 0), rr)/np.trapezoid(w, rr)
    print(f"  eps>0 fraction: coordinate-r {100*frac_r:.2f}%  proper-length {100*frac_proper:.2f}%")
    print(f"  eps range: [{eps.min():.4g}, {eps.max():.4g}]; eps(core)={eps[0]:.4g}, eps(seal)={eps[-1]:.4g}")

    E_can = -intL
    print(f"  E_can = -int L     = {E_can:+.8g}")
    print(f"  ratio int L / dm   = {intL/dm:+.6g}")
    print(f"  ratio E_can / dm   = {E_can/dm:+.6g}")
    # matter-only vs geometric split of E_can (for the Y4 adjudication)
    E_matter = np.trapezoid(Uv, rr)          # -int L_m with L_m = -U
    E_geo = E_can - E_matter
    print(f"  E split: matter +int U dr = {E_matter:+.8g};  geometric rest = {E_geo:+.8g}")
    print(f"  (of geometric: -2*r_s from the +2 angular term = {-2.0*r_s:+.8g};"
          f" kinetic -int[(Z/2)rho^2 phi'^2 - 2 e^-2phi rho'^2] = "
          f"{-np.trapezoid(0.5*Z*rho_**2*phip_**2 - 2.0*rhop_**2/e2p, rr):+.8g})")

"""V2 + V3 — exact discrete scale response and localization/surface-stress audit
(Charles dispatch 2026-07-16, sections 4-5). Reuses ONLY the corrected eight-orientation functional.

V2 (exact, per grid): at fixed field arrays and fixed N, h -> lambda*h gives EXACTLY
E(lambda) = lambda*E2 + (1/lambda)*E4 for this functional; verified by direct recomputation at
lambda = 1 +/- eps, eps in {2e-4, 1e-4, 5e-5} (required rel agreement < 1e-9) and by the analytic
split; dE/dln(lambda)|_1 = E2 - E4 via central differences. Also: integral(S) = E4 - E2 vs
2E4-(E2+E4) to roundoff; residual work of the dilation generator W_res = <g_raw, P(x . grad n)>
with the projection stated explicitly (tangential + free-mask HBW=2; generator derivative =
eight-orientation-averaged one-sided); Cauchy bound ||g_f|| * ||P(x.grad n)||.
NOTE: this is an exact conjugate response of the FIXED-BOX family — not evidence about large L.

V3 (convergence test, per grid): nested cube+sphere enclosed fractions for BOTH E2 and E4 (same
radii as G); eight-orientation-averaged stress T_ij from the same one-sided derivatives;
B(a) = surface integral of x_j T_ij nu_i over nested cubic surfaces (site-plane quadrature, with a
half-cell in/out placement sensitivity); V(a) = integral over the cube of (rho4 - rho2);
W_res(a) = enclosed residual work; closure error V - B - W_res per surface/grid. A site-based
one-sided discretization need not have an exact local Noether identity — this is a CONVERGENCE
test (128 -> 192 -> 256 at matched physical a), not an assumed lattice theorem.
Output: noNull_boundary_virial_ALL.json.
"""
import gc, json, numpy as np, torch
from noNull_energy import energy_noNull, grad_noNull, _ORIENTS, _dop, _cross
torch.set_default_dtype(torch.float64); dev = 'cuda' if torch.cuda.is_available() else 'cpu'

HBW = 2
EPS_LIST = (2e-4, 1e-4, 5e-5)
CUBE_HALFWIDTHS = (1.0, 1.5, 2.0, 2.5, 2.95)
SPHERE_RADII = (0.5, 1.0, 1.5, 2.0, 2.5, 2.95)
GRIDS = [(128, 'noNull_critical_field_128.npz'),
         (192, 'noNull_critical_field_192.npz'),
         (256, 'noNull_critical_field.npz')]

def fields_all(n, h, xi, kap):
    """Eight-orientation-averaged: rho2, rho4, stress T[i][j] (site fields), and dbar[j][a] =
    averaged one-sided derivative (the generator/residual-work derivative convention)."""
    N = n.shape[1]
    z = lambda: torch.zeros(N, N, N, device=dev)
    rho2, rho4 = z(), z()
    T = [[z() for _ in range(3)] for _ in range(3)]
    dbar = [torch.zeros(3, N, N, N, device=dev) for _ in range(3)]
    for s in _ORIENTS:
        dn = [_dop(n, 1, s[0], h), _dop(n, 2, s[1], h), _dop(n, 3, s[2], h)]
        X = sum((dn[i] * dn[i]).sum(0) for i in range(3))
        F = [[z() for _ in range(3)] for _ in range(3)]
        Y = z()
        for i in range(3):
            for j in range(3):
                if i == j: continue
                F[i][j] = (n * _cross(dn[i], dn[j])).sum(0)
                Y = Y + F[i][j] * F[i][j]
        rho2 += (0.5 * xi) * X / 8; rho4 += (0.25 * kap) * Y / 8
        for i in range(3):
            for j in range(3):
                Tij = xi * ((dn[i] * dn[j]).sum(0) - (0.5 * X if i == j else 0)) \
                    + kap * (sum(F[i][k] * F[j][k] for k in range(3)) - (0.25 * Y if i == j else 0))
                T[i][j] += Tij / 8
            dbar[i] += dn[i] / 8
        del dn, X, F, Y
    return rho2, rho4, T, dbar

result = dict(dispatch='V2+V3 boundary-virial (2026-07-16)',
              conventions=dict(generator_derivative='eight-orientation-averaged one-sided (matches production densities)',
                               projection='tangential (v-(v.n)n) then free mask (zero outer HBW=2 layers)',
                               surface_quadrature='site-plane faces at the outermost enclosed layer, h^2 weights; '
                                                  'sensitivity = coordinate face at half-cell out (x_f = x_layer + h/2)',
                               sign='V(a) = B(a) + W_res(a) per the DERIVED identity (see derivation record)'),
              grids={})

for (Ng, critf) in GRIDS:
    dc = np.load(critf)
    N, L, h, xi, kap = int(dc['N']), float(dc['L']), float(dc['h']), float(dc['xi']), float(dc['kappa'])
    n = torch.tensor(dc['n'], device=dev); n = n / n.norm(dim=0, keepdim=True)
    g = dict(N=N, L=L, h=h)
    E, E2t, E4t = energy_noNull(n, h, xi, kap)
    E2, E4 = float(E2t), float(E4t)
    print(f"\n=== V2/V3 N={Ng}: E2={E2:.6f} E4={E4:.6f} ===", flush=True)

    # ---------- V2: exact scale response ----------
    v2 = dict(E2=E2, E4=E4)
    sweep = {}
    for eps in EPS_LIST:
        row = {}
        for lam in (1 + eps, 1 - eps):
            Ev = float(energy_noNull(n, lam * h, xi, kap)[0])
            Ea = lam * E2 + E4 / lam
            row[f'{lam:.6f}'] = dict(E_recomputed=Ev, E_analytic=Ea, rel=abs(Ev - Ea) / abs(Ea))
        dE = (row[f'{1+eps:.6f}']['E_recomputed'] - row[f'{1-eps:.6f}']['E_recomputed']) / (2 * eps)
        row['dE_dlnlam_FD'] = dE; row['E2_minus_E4'] = E2 - E4
        row['dE_rel_err'] = abs(dE - (E2 - E4)) / max(abs(E2 - E4), 1e-30)
        sweep[f'{eps:g}'] = row
    worst = max(r[k]['rel'] for r in sweep.values() for k in r if isinstance(r[k], dict))
    v2['lambda_sweep'] = sweep
    v2['exactness_gate_1e9'] = bool(worst < 1e-9); v2['worst_rel'] = worst
    rho2, rho4, T, dbar = fields_all(n, h, xi, kap)
    intS = float((rho4 - rho2).sum()) * h**3
    v2['int_S_dV'] = intS; v2['E4_minus_E2'] = E4 - E2
    v2['twoE4_minus_Esum'] = 2 * E4 - (E2 + E4)
    v2['equality_roundoff'] = dict(intS_vs_E4mE2=abs(intS - (E4 - E2)),
                                   E4mE2_vs_2E4mEsum=abs((E4 - E2) - (2 * E4 - (E2 + E4))))
    # residual work of the dilation generator
    ax = torch.tensor((np.arange(N) - (N - 1) / 2) * h, device=dev)
    Xc = ax.view(N, 1, 1); Yc = ax.view(1, N, 1); Zc = ax.view(1, 1, N)
    D = Xc * dbar[0] + Yc * dbar[1] + Zc * dbar[2]                  # x . grad n (stated convention)
    FM = torch.zeros(N, N, N, device=dev); FM[HBW:-HBW, HBW:-HBW, HBW:-HBW] = 1.0
    def proj(v): return (v - (v * n).sum(0, keepdim=True) * n) * FM
    gr = grad_noNull(n, h, xi, kap)
    gf = proj(gr); Dp = proj(D)
    W_res = float((gr * Dp).sum())                                   # <g_raw, P(D)> = <P(g), D>
    cauchy = float(gf.norm()) * float(Dp.norm())
    v2['residual_work_W'] = W_res; v2['cauchy_bound'] = cauchy
    v2['W_over_gap'] = W_res / (E4 - E2)
    g['V2'] = v2
    print(f"  V2: worst lambda rel {worst:.2e}; intS={intS:.6f} (=E4-E2 to {v2['equality_roundoff']['intS_vs_E4mE2']:.1e}); "
          f"W_res={W_res:+.4f} (Cauchy<= {cauchy:.4f}; W/(E4-E2)={W_res/(E4-E2):+.3f})", flush=True)

    # ---------- V3: localization (E2 AND E4) + surface stress ----------
    rho2n = rho2.cpu().numpy(); rho4n = rho4.cpu().numpy()
    axn = (np.arange(N) - (N - 1) / 2) * h
    X3, Y3, Z3 = np.meshgrid(axn, axn, axn, indexing='ij')
    R3 = np.sqrt(X3**2 + Y3**2 + Z3**2); Am = np.maximum.reduce([np.abs(X3), np.abs(Y3), np.abs(Z3)])
    loc = dict(cubes={}, spheres={})
    for a in CUBE_HALFWIDTHS:
        loc['cubes'][f'{a:g}'] = dict(E2_frac=float(rho2n[Am <= a].sum() * h**3 / E2),
                                      E4_frac=float(rho4n[Am <= a].sum() * h**3 / E4))
    for r in SPHERE_RADII:
        loc['spheres'][f'{r:g}'] = dict(E2_frac=float(rho2n[R3 <= r].sum() * h**3 / E2),
                                        E4_frac=float(rho4n[R3 <= r].sum() * h**3 / E4))
    g['V3_localization'] = loc
    # residual-work density (per site): w(x) = x_j * g_a(x) * dbar_j n_a(x)  [g = site-integrated Rhat]
    wden = (gr * (Xc * dbar[0])).sum(0) + (gr * (Yc * dbar[1])).sum(0) + (gr * (Zc * dbar[2])).sum(0)
    wden_n = wden.cpu().numpy()                                      # already carries dV via g
    Tn = [[T[i][j].cpu().numpy() for j in range(3)] for i in range(3)]
    ctr = ((N - 1) // 2, N // 2)
    surf = {}
    for a in CUBE_HALFWIDTHS:
        m = int(round(a / h))
        i0 = max(ctr[1] - m, 0); i1 = min(ctr[0] + m, N - 1)
        sl = np.s_[i0:i1 + 1]
        V_a = float((rho4n - rho2n)[sl, sl, sl].sum() * h**3)
        W_a = float(wden_n[i0:i1 + 1, i0:i1 + 1, i0:i1 + 1].sum())
        def B_of(xshift):
            tot = 0.0
            for (axis, layer, sgn) in ((0, i1, +1), (0, i0, -1), (1, i1, +1), (1, i0, -1), (2, i1, +1), (2, i0, -1)):
                xf = axn[layer] + sgn * xshift
                idx = [sl, sl, sl]; idx[axis] = layer
                face = tuple(idx)
                integ = np.zeros_like(Tn[0][0][face])
                for j in range(3):
                    if j == axis: xj = xf
                    elif j == 0: xj = X3[face]
                    elif j == 1: xj = Y3[face]
                    else: xj = Z3[face]
                    integ = integ + xj * Tn[axis][j][face]
                tot += sgn * integ.sum() * h**2
            return tot
        B_site = B_of(0.0); B_half = B_of(h / 2)
        err_site = V_a - B_site - W_a; err_half = V_a - B_half - W_a
        surf[f'{a:g}'] = dict(index_halfwidth=m, V=V_a, W_res=W_a, B_siteplane=B_site, B_halfcell=B_half,
                              closure_err_site=err_site, closure_err_half=err_half,
                              closure_rel_site=err_site / max(abs(V_a), 1e-30),
                              closure_rel_half=err_half / max(abs(V_a), 1e-30))
    g['V3_surface'] = surf
    print(f"  V3 a=2.95: V={surf['2.95']['V']:.4f} B_site={surf['2.95']['B_siteplane']:.4f} "
          f"B_half={surf['2.95']['B_halfcell']:.4f} W={surf['2.95']['W_res']:+.4f} "
          f"rel_err site/half = {surf['2.95']['closure_rel_site']:+.3e}/{surf['2.95']['closure_rel_half']:+.3e}", flush=True)
    result['grids'][str(Ng)] = g
    del rho2, rho4, T, dbar, gr, gf, D, Dp, n; gc.collect(); torch.cuda.empty_cache()

json.dump(result, open('noNull_boundary_virial_ALL.json', 'w'), indent=1, default=float)
print('\nwrote noNull_boundary_virial_ALL.json', flush=True)

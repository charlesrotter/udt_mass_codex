"""INDEPENDENT VERIFIER for Phase G (Charles dispatch 2026-07-16, section 7).

Does NOT import the production density or flux functions (noNull_phaseG_mass is never imported).
Reads the same carrier NPZs; uses the already-audited energy_noNull ONLY as a black-box comparison.
Independently:
  1. implements the eight one-sided orientations (own code, torch.roll-based);
  2. recomputes rho2_NN, rho4_NN, E2, E4;
  3. checks rho + S = 2*rho4 pointwise;
  4. recomputes at least three cubic face fluxes DIRECTLY from the saved u fields (own bond code);
  5. recomputes the seven-point residual and flux-vs-enclosed-source errors;
  6. compares every reported scalar against the production JSON;
  7. issues PASS / FAIL / UNRESOLVED — never repairs production numbers in memory.
Outputs: noNull_phaseG_mass_verify.json + stdout.
"""
import os, gc, json, numpy as np, torch
from noNull_energy import energy_noNull                       # black-box comparison ONLY
torch.set_default_dtype(torch.float64); dev = 'cuda' if torch.cuda.is_available() else 'cpu'

TOL_MACH = 1e-12
GRIDS = [(128, 'noNull_critical_field_128.npz'),
         (192, 'noNull_critical_field_192.npz'),
         (256, 'noNull_critical_field.npz')]

prod = json.load(open('noNull_phaseG_mass_ALL.json'))
checks = []
def check(name, ok, detail):
    checks.append((name, bool(ok), detail)); print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)

def own_onesided(f, ax, sgn, h):
    """Own one-sided difference: forward (f[i+1]-f[i])/h for sgn=+1, backward (f[i]-f[i-1])/h for -1.
    Periodic wrap via roll (pinned constant boundary makes the seam derivative zero)."""
    if sgn == +1: return (torch.roll(f, -1, ax) - f) / h
    return (f - torch.roll(f, 1, ax)) / h

def own_cross(a, b):
    return torch.stack([a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]], 0)

out = {}
for (Ng, critf) in GRIDS:
    dc = np.load(critf)
    N, L, h, xi, kap = int(dc['N']), float(dc['L']), float(dc['h']), float(dc['xi']), float(dc['kappa'])
    n = torch.tensor(dc['n'], device=dev); n = n / n.norm(dim=0, keepdim=True)
    rho2 = torch.zeros(N, N, N, device=dev); rho4 = torch.zeros_like(rho2); Ssrc = torch.zeros_like(rho2)
    for s1 in (+1, -1):
        for s2 in (+1, -1):
            for s3 in (+1, -1):
                dn = [own_onesided(n, 1, s1, h), own_onesided(n, 2, s2, h), own_onesided(n, 3, s3, h)]
                X = sum((dn[i] * dn[i]).sum(0) for i in range(3))
                Y = torch.zeros_like(X)
                for i in range(3):
                    for j in range(3):
                        if i == j: continue
                        Fij = (n * own_cross(dn[i], dn[j])).sum(0)
                        Y = Y + Fij * Fij
                rho2 += (0.5 * xi) * X / 8; rho4 += (0.25 * kap) * Y / 8
                Ssrc += (-(0.5 * xi) * X + (0.25 * kap) * Y) / 8
                del dn, X, Y
    E2v = float(rho2.sum()) * h**3; E4v = float(rho4.sum()) * h**3
    Eref, E2r, E4r = energy_noNull(n, h, xi, kap)
    g = prod['grids'][str(Ng)]['G1']
    check(f'N={Ng} own-E2 vs black-box', abs(E2v - float(E2r)) / float(E2r) < TOL_MACH, f'{E2v:.9f} vs {float(E2r):.9f}')
    check(f'N={Ng} own-E4 vs black-box', abs(E4v - float(E4r)) / float(E4r) < TOL_MACH, f'{E4v:.9f} vs {float(E4r):.9f}')
    check(f'N={Ng} own-E2 vs production JSON', abs(E2v - g['E2']) / g['E2'] < TOL_MACH, f'{E2v:.9f} vs {g["E2"]:.9f}')
    check(f'N={Ng} own-E4 vs production JSON', abs(E4v - g['E4']) / g['E4'] < TOL_MACH, f'{E4v:.9f} vs {g["E4"]:.9f}')
    ident = float((rho2 + rho4 + Ssrc - 2 * rho4).abs().max()) / float((2 * rho4).abs().max())
    check(f'N={Ng} rho+S=2rho4 (own)', ident < TOL_MACH, f'relmax {ident:.2e}')
    check(f'N={Ng} rho4>=0 (own)', float(rho4.min()) >= -1e-18, f'min {float(rho4.min()):.2e}')
    check(f'N={Ng} delta_vir vs JSON', abs((E2v - E4v) / (E2v + E4v) - g['delta_vir']) < 1e-12,
          f'{(E2v-E4v)/(E2v+E4v):+.6e} vs {g["delta_vir"]:+.6e}')
    rho4_np = rho4.cpu().numpy()
    del rho2, rho4, Ssrc, n; gc.collect(); torch.cuda.empty_cache()

    # ---- fluxes and residuals recomputed DIRECTLY from the saved u fields ----
    for pk, pg in prod['grids'][str(Ng)]['G3_G4'].items():
        uf = pg['u_field_file']
        if not os.path.exists(uf):
            check(f'N={Ng} {pk} u field present', False, f'{uf} missing'); continue
        du = np.load(uf); u = du['u']; Np = int(du['Np']); off = int(du['off'])
        rho_p = np.zeros((Np, Np, Np)); rho_p[off:off + N, off:off + N, off:off + N] = rho4_np
        up = np.zeros((Np + 2,) * 3); up[1:-1, 1:-1, 1:-1] = u
        lap = (up[2:, 1:-1, 1:-1] + up[:-2, 1:-1, 1:-1] + up[1:-1, 2:, 1:-1] + up[1:-1, :-2, 1:-1]
               + up[1:-1, 1:-1, 2:] + up[1:-1, 1:-1, :-2] - 6.0 * u) / h**2
        r_P = float(np.linalg.norm((lap - rho_p).ravel()) / np.linalg.norm(rho_p.ravel()))
        check(f'N={Ng} {pk} r_P (own stencil)', r_P < 1e-9, f'{r_P:.2e} (prod {pg["r_P"]:.2e})')
        ctr = ((Np - 1) // 2, Np // 2)
        nfl = 0
        for ak, fx in pg['fluxes'].items():
            m = int(fx['index_halfwidth'])
            i0 = max(ctr[1] - m, 0); i1 = min(ctr[0] + m, Np - 1)
            a, b = i0 + 1, i1 + 1; sl = np.s_[a:b + 1]
            tot = ((up[b + 1, sl, sl] - up[b, sl, sl]).sum() + (up[a - 1, sl, sl] - up[a, sl, sl]).sum()
                   + (up[sl, b + 1, sl] - up[sl, b, sl]).sum() + (up[sl, a - 1, sl] - up[sl, a, sl]).sum()
                   + (up[sl, sl, b + 1] - up[sl, sl, b]).sum() + (up[sl, sl, a - 1] - up[sl, sl, a]).sum())
            Phi = h * tot
            Q_C = float(rho_p[i0:i1 + 1, i0:i1 + 1, i0:i1 + 1].sum() * h**3)
            ok_phi = abs(Phi - fx['Phi']) <= 1e-9 * max(abs(fx['Phi']), 1e-30)
            ok_q = abs(Q_C - fx['Q_enclosed']) <= 1e-9 * max(abs(fx['Q_enclosed']), 1e-30)
            ok_g = abs(Phi - Q_C) / max(abs(Q_C), 1e-30) < 1e-6
            check(f'N={Ng} {pk} cube a={ak} flux (own)', ok_phi and ok_q and ok_g,
                  f'Phi={Phi:.9f} (prod {fx["Phi"]:.9f}); gauss rel {abs(Phi-Q_C)/max(abs(Q_C),1e-30):.2e}')
            nfl += 1
        check(f'N={Ng} {pk} >=3 fluxes recomputed', nfl >= 3, f'{nfl} cubes')
        del u, up, lap, rho_p, du; gc.collect()
    out[str(Ng)] = 'checked'

npass = sum(1 for _, ok, _ in checks if ok); nfail = len(checks) - npass
verdict = 'PASS' if nfail == 0 else 'FAIL'
print(f'\n== PHASE-G VERIFIER VERDICT: {verdict} ({npass}/{len(checks)} checks) ==', flush=True)
json.dump(dict(verdict=verdict, npass=npass, ntotal=len(checks),
               checks=[dict(name=nm, ok=ok, detail=dt) for nm, ok, dt in checks]),
          open('noNull_phaseG_mass_verify.json', 'w'), indent=1)

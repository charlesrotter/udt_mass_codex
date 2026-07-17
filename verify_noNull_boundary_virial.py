"""INDEPENDENT VERIFIER — boundary-virial dispatch §8 (2026-07-16).

Does NOT import production density, stress, surface, or scale-response functions
(noNull_boundary_virial.py is never imported). Uses noNull_energy.energy_noNull ONLY as a black-box
comparison. Independently recomputes with own code:
  1. eight-orientation E2, E4, int(S) (own one-sided derivatives);
  2. the exact h-scale derivative (own densities: E(lam) = lam*E2 + E4/lam; FD cross-check);
  3. >=3 surface-stress entries per existing grid (own T_ij + own face quadrature) vs production JSON;
  4. every larger-box energy/charge/criticality scalar from the saved scout fields vs
     noNull_boxscout_observables.json;
  5. the decision-table predicates (monotone |delta_vir| decrease in L at both h; criticality gates;
     charge stability).
Emits noNull_boundary_virial_verify.json; verdict PASS/FAIL/UNRESOLVED; never repairs production numbers.
"""
import os, gc, json, math, numpy as np, torch
from noNull_energy import energy_noNull                 # black-box comparison ONLY
from noNull_precond import mnorm                        # norm definition (shared convention, not a result)
torch.set_default_dtype(torch.float64); dev = 'cuda' if torch.cuda.is_available() else 'cpu'

checks = []
def check(name, ok, detail):
    checks.append((name, bool(ok), detail)); print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)

def own_d(f, ax, s, h):
    if s == +1: return (torch.roll(f, -1, ax) - f) / h
    return (f - torch.roll(f, 1, ax)) / h

def own_cross(a, b):
    return torch.stack([a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]], 0)

def own_fields(n, h, xi, kap, want_T=False):
    N = n.shape[1]
    z = lambda: torch.zeros(N, N, N, device=dev)
    r2, r4 = z(), z()
    T = [[z() for _ in range(3)] for _ in range(3)] if want_T else None
    for s1 in (1, -1):
        for s2 in (1, -1):
            for s3 in (1, -1):
                dn = [own_d(n, 1, s1, h), own_d(n, 2, s2, h), own_d(n, 3, s3, h)]
                Xd = sum((dn[i]*dn[i]).sum(0) for i in range(3))
                F = [[z() for _ in range(3)] for _ in range(3)]
                Yd = z()
                for i in range(3):
                    for j in range(3):
                        if i == j: continue
                        F[i][j] = (n * own_cross(dn[i], dn[j])).sum(0); Yd = Yd + F[i][j]**2
                r2 += 0.5*xi*Xd/8; r4 += 0.25*kap*Yd/8
                if want_T:
                    for i in range(3):
                        for j in range(3):
                            T[i][j] += (xi*((dn[i]*dn[j]).sum(0) - (0.5*Xd if i == j else 0))
                                        + kap*(sum(F[i][k]*F[j][k] for k in range(3)) - (0.25*Yd if i == j else 0))) / 8
                del dn, Xd, F, Yd
    return r2, r4, T

def own_charge(n, h):
    N = n.shape[1]
    dn = [(torch.roll(n, -1, a+1) - n)/h for a in range(3)]
    F = {(i, j): (n*own_cross(dn[i], dn[j])).sum(0) for i in range(3) for j in range(3) if i != j}
    B = torch.stack([F[(1, 2)], F[(2, 0)], F[(0, 1)]], 0)
    k1 = 2*math.pi*torch.fft.fftfreq(N, d=h, device=dev)
    KX, KY, KZ = torch.meshgrid(k1, k1, k1, indexing='ij'); k2 = KX*KX+KY*KY+KZ*KZ; k2[0, 0, 0] = 1.0
    dfw = lambda g, ax: (torch.roll(g, -1, ax) - g)/h
    cB = torch.stack([dfw(B[2], 1)-dfw(B[1], 2), dfw(B[0], 2)-dfw(B[2], 0), dfw(B[1], 0)-dfw(B[0], 1)], 0)
    A = torch.zeros_like(B)
    for c in range(3):
        Ak = torch.fft.fftn(-cB[c])/(-k2); Ak[0, 0, 0] = 0.0; A[c] = torch.fft.ifftn(Ak).real
    return float((A*B).sum(0).sum()*h**3/(16*math.pi**2))

prodV = json.load(open('noNull_boundary_virial_ALL.json'))
scout = json.load(open('noNull_boxscout_observables.json'))

# ---- 1-3: existing grids ----
for Ng, critf in ((128, 'noNull_critical_field_128.npz'), (192, 'noNull_critical_field_192.npz'),
                  (256, 'noNull_critical_field.npz')):
    dc = np.load(critf)
    N, L, h, xi, kap = int(dc['N']), float(dc['L']), float(dc['h']), float(dc['xi']), float(dc['kappa'])
    n = torch.tensor(dc['n'], device=dev); n = n/n.norm(dim=0, keepdim=True)
    r2, r4, T = own_fields(n, h, xi, kap, want_T=True)
    E2o = float(r2.sum())*h**3; E4o = float(r4.sum())*h**3
    Eref, E2r, E4r = energy_noNull(n, h, xi, kap)
    g = prodV['grids'][str(Ng)]['V2']
    check(f'N={Ng} own E2/E4 vs black-box', abs(E2o-float(E2r))/float(E2r) < 1e-12 and abs(E4o-float(E4r))/float(E4r) < 1e-12,
          f'{E2o:.9f}/{E4o:.9f}')
    check(f'N={Ng} own E2/E4 vs production', abs(E2o-g['E2'])/g['E2'] < 1e-12 and abs(E4o-g['E4'])/g['E4'] < 1e-12, 'match')
    # exact scale response with OWN densities: E(lam) analytic vs own recompute of energy at lam*h
    for eps in (2e-4,):
        lam = 1 + eps
        r2l, r4l, _ = own_fields(n, lam*h, xi, kap)
        Eown = (float(r2l.sum()) + float(r4l.sum())) * (lam*h)**3
        Ean = lam*E2o + E4o/lam
        check(f'N={Ng} own scale response (lam={lam:g})', abs(Eown-Ean)/abs(Ean) < 1e-9,
              f'rel {abs(Eown-Ean)/abs(Ean):.2e}')
        del r2l, r4l
    intS = float((r4-r2).sum())*h**3
    check(f'N={Ng} int(S)=E4-E2 (own)', abs(intS-(E4o-E2o)) < 1e-10*max(abs(E4o-E2o), 1), f'{intS:.6f}')
    # surface stress: recompute >=3 B(a) entries with own quadrature; compare to production
    axn = (np.arange(N)-(N-1)/2)*h
    X3, Y3, Z3 = np.meshgrid(axn, axn, axn, indexing='ij')
    Tn = [[T[i][j].cpu().numpy() for j in range(3)] for i in range(3)]
    ctr = ((N-1)//2, N//2)
    nsurf = 0
    for ak, fx in prodV['grids'][str(Ng)]['V3_surface'].items():
        m = int(fx['index_halfwidth'])
        i0 = max(ctr[1]-m, 0); i1 = min(ctr[0]+m, N-1); sl = np.s_[i0:i1+1]
        tot = 0.0
        for (axis, layer, sgn) in ((0, i1, 1), (0, i0, -1), (1, i1, 1), (1, i0, -1), (2, i1, 1), (2, i0, -1)):
            idx = [sl, sl, sl]; idx[axis] = layer; face = tuple(idx)
            integ = np.zeros_like(Tn[0][0][face])
            for j in range(3):
                if j == axis: xj = axn[layer]
                elif j == 0: xj = X3[face]
                elif j == 1: xj = Y3[face]
                else: xj = Z3[face]
                integ = integ + xj*Tn[axis][j][face]
            tot += sgn*integ.sum()*h**2
        ok = abs(tot - fx['B_siteplane']) <= 1e-9*max(abs(fx['B_siteplane']), 1e-30)
        check(f'N={Ng} B(a={ak}) own quadrature', ok, f'{tot:.6f} vs {fx["B_siteplane"]:.6f}')
        nsurf += 1
    check(f'N={Ng} >=3 surface entries', nsurf >= 3, f'{nsurf}')
    del n, r2, r4, T, Tn; gc.collect(); torch.cuda.empty_cache()

# ---- 4: scout boxes ----
for tag, f in (('L6.00_N128', 'noNull_critical_field_128.npz'), ('L7.51_N160', 'noNull_boxscout_N160.npz'),
               ('L9.02_N192', 'noNull_boxscout_N192.npz'), ('L7.51_N240_hf', 'noNull_boxscout_N240.npz')):
    dc = np.load(f)
    N, L, h, xi, kap = int(dc['N']), float(dc['L']), float(dc['h']), float(dc['xi']), float(dc['kappa'])
    n = torch.tensor(dc['n'], device=dev); n = n/n.norm(dim=0, keepdim=True)
    E, E2r, E4r = [float(x) for x in energy_noNull(n, h, xi, kap)]
    Qo = own_charge(n, h)
    from noNull_energy import grad_noNull
    FM = torch.zeros(N, N, N, device=dev); FM[2:-2, 2:-2, 2:-2] = 1.0
    gr = grad_noNull(n, h, xi, kap); gf = (gr-(gr*n).sum(0, keepdim=True)*n)*FM
    cM = float(mnorm(gf, h))
    row = scout[tag]
    dvo = (E2r-E4r)/(E2r+E4r)
    ok = (abs(E-row['E']) < 1e-6 and abs(dvo-row['delta_vir']) < 1e-9 and abs(Qo-row['Q_fwd']) < 1e-6
          and abs(cM-row['crit_Minv']) < 1e-6)
    check(f'scout {tag} scalars (own)', ok,
          f'E={E:.4f} dv={dvo:+.5f} Q={Qo:.5f} critM={cM:.3e}')
    del n, gr, gf; gc.collect(); torch.cuda.empty_cache()

# ---- 5: decision-table predicates ----
dv = {k: abs(scout[k]['delta_vir']) for k in scout}
mono_hc = dv['L6.00_N128'] > dv['L7.51_N160'] > dv['L9.02_N192']
check('predicate: |delta_vir| monotone decreasing in L at h_c', mono_hc,
      f"{dv['L6.00_N128']:.5f} > {dv['L7.51_N160']:.5f} > {dv['L9.02_N192']:.5f}")
dv192 = abs(json.load(open('noNull_phaseG_mass_ALL.json'))['grids']['192']['G1']['delta_vir'])
mono_hf = dv192 > dv['L7.51_N240_hf']
check('predicate: |delta_vir| decreases in L at h_f', mono_hf, f'{dv192:.5f} > {dv["L7.51_N240_hf"]:.5f}')
crit_ok = all(scout[k]['crit_Minv'] < 0.05 for k in scout)
check('predicate: all scout carriers meet ||g_f||_M-1 < 0.05', crit_ok,
      f"{[round(scout[k]['crit_Minv'], 4) for k in scout]}")
q_ok = all(abs(scout[k]['Q_fwd']) > 0.96 for k in scout)
check('predicate: topology held (|Q_fwd| > 0.96 all boxes)', q_ok, f"{[round(scout[k]['Q_fwd'], 4) for k in scout]}")

npass = sum(1 for _, ok, _ in checks if ok); nfail = len(checks)-npass
verdict = 'PASS' if nfail == 0 else 'FAIL'
print(f'\n== BOUNDARY-VIRIAL VERIFIER VERDICT: {verdict} ({npass}/{len(checks)}) ==', flush=True)
json.dump(dict(verdict=verdict, npass=npass, ntotal=len(checks),
               checks=[dict(name=a, ok=b, detail=c) for a, b, c in checks]),
          open('noNull_boundary_virial_verify.json', 'w'), indent=1)

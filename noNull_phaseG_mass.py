"""PHASE G — conditional mass readout on the CORRECTED carrier (Charles dispatch 2026-07-16).

G1: eight-orientation one-sided local densities rho2_NN, rho4_NN (the EXACT operators of the
    certified energy: _dop/_cross/_ORIENTS from noNull_energy — NO centered derivative anywhere in
    the production path). Exact checks: energy reproduction <1e-12; rho4>=0; pointwise
    rho + S = 2*rho4 <1e-12; virial delta; both no-null charge readouts; carrier criticality.
G2: source localization (nested cubes + spheres, omitted-tail reporting — the carrier boundary is a
    SOLVER boundary, not a physical wall) + three-grid convergence audit (independent carriers, not
    subsamples): raw values, successive h^2 slopes, fine-pair Richardson, 3-point h^2+h^4.
G3: unit Poisson response Delta_h u = rho4_NN with the standard SEVEN-POINT Laplacian, zero-Dirichlet
    on a centered zero-source-padded cube, padding p in {1, 1.5, 2} at fixed physical h. Solver =
    DIRECT DST-I spectral inversion of the same seven-point operator (category-A technique; exact to
    roundoff — no continuum-kernel mismatch like the old 1.75% Hockney residual). Raw gate
    r_P = ||Delta_h u - rho4||_2 / ||rho4||_2 < 1e-9 verified by explicit stencil application.
G4: exact discrete bond flux Phi_h(C) = h * sum_{bonds crossing dC} (u_out - u_in) telescoping the
    seven-point Laplacian, vs enclosed source Q_h(C); gate max_C |Phi-Q|/max(|Q|,1e-30) < 1e-6, with
    the flux error EXPLAINED by the accumulated Poisson residual (reported side by side).
    Conditional readout: M_N^(0)(C) = 2*Phi_h(C), ratio to 2*E4.

STATUS LABELS (binding): the S^2 carrier + L2+L4 functional are POSIT/CHOSE; the lapse identity is
CONDITIONAL on the EH metric-only action premise; G is a CONDITIONAL CONSISTENCY READOUT, not a
native-UDT mass derivation. DATA-BLIND: no particle labels, observed masses, or fitted couplings.
No kappa_g value is used (unit-response test). Outputs: noNull_phaseG_mass_ALL.json + stdout log.
"""
import os, gc, json, math, time, hashlib, numpy as np, torch
from scipy.fft import dstn, idstn
from noNull_energy import energy_noNull, grad_noNull, _ORIENTS, _dop, _cross
from noNull_precond import make_precond, mnorm
torch.set_default_dtype(torch.float64); dev = 'cuda' if torch.cuda.is_available() else 'cpu'

HBW = 2
GRIDS = [(128, 'noNull_critical_field_128.npz'),
         (192, 'noNull_critical_field_192.npz'),
         (256, 'noNull_critical_field.npz')]
PADDINGS = (1.0, 1.5, 2.0)
CUBE_HALFWIDTHS = (1.0, 1.5, 2.0, 2.5, 2.95)      # physical, within the carrier box (L=6 half-width 3)
SPHERE_RADII = (0.5, 1.0, 1.5, 2.0, 2.5, 2.95)

def sha256(p):
    hh = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''): hh.update(b)
    return hh.hexdigest()

# ---------------- G1: local densities from the certified one-sided operators ----------------
def densities_NN(n, h, xi, kap):
    """Eight-orientation-averaged site densities. Uses noNull_energy's _dop/_cross/_ORIENTS —
    the exact operators of the certified energy. Returns (rho2, rho4, S) site fields."""
    N = n.shape[1]
    rho2 = torch.zeros(N, N, N, device=dev); rho4 = torch.zeros_like(rho2); Ssrc = torch.zeros_like(rho2)
    for s in _ORIENTS:
        dn = [_dop(n, 1, s[0], h), _dop(n, 2, s[1], h), _dop(n, 3, s[2], h)]
        Xs = sum((dn[i] * dn[i]).sum(0) for i in range(3))
        Ys = torch.zeros_like(Xs)
        for i in range(3):
            for j in range(3):
                if i == j: continue
                Fij = (n * _cross(dn[i], dn[j])).sum(0)
                Ys = Ys + Fij * Fij
        rho2 = rho2 + (0.5 * xi) * Xs / 8
        rho4 = rho4 + (0.25 * kap) * Ys / 8
        Ssrc = Ssrc + (-(0.5 * xi) * Xs + (0.25 * kap) * Ys) / 8
        del dn, Xs, Ys
    return rho2, rho4, Ssrc

def charge_fwd_local(n, h):
    """No-null Hopf charge, forward-difference F (audited formula, local copy — noNull_resolve.py
    cannot be imported without executing a STAGE)."""
    N = n.shape[1]
    dn = [(torch.roll(n, -1, a + 1) - n) / h for a in range(3)]
    F = {(i, j): (n * _cross(dn[i], dn[j])).sum(0) for i in range(3) for j in range(3) if i != j}
    return _hopf_from_F(F, N, h)

def charge_sym_local(n, h):
    """No-null Hopf charge, eight-orientation-averaged F (audited formula, local copy)."""
    N = n.shape[1]
    F = {(i, j): torch.zeros(N, N, N, device=dev) for i in range(3) for j in range(3) if i != j}
    for s in _ORIENTS:
        dn = [_dop(n, 1, s[0], h), _dop(n, 2, s[1], h), _dop(n, 3, s[2], h)]
        for i in range(3):
            for j in range(3):
                if i != j: F[(i, j)] = F[(i, j)] + (n * _cross(dn[i], dn[j])).sum(0) / 8
    return _hopf_from_F(F, N, h)

def _hopf_from_F(Fjk, N, h):
    Bx = Fjk[(1, 2)]; By = Fjk[(2, 0)]; Bz = Fjk[(0, 1)]; B = torch.stack([Bx, By, Bz], 0)
    k1 = 2 * math.pi * torch.fft.fftfreq(N, d=h, device=dev)
    KX, KY, KZ = torch.meshgrid(k1, k1, k1, indexing='ij'); k2 = KX * KX + KY * KY + KZ * KZ; k2[0, 0, 0] = 1.0
    def dfwd(f, ax): return (torch.roll(f, -1, ax) - f) / h
    def curl(V):
        return torch.stack([dfwd(V[2], 1) - dfwd(V[1], 2), dfwd(V[0], 2) - dfwd(V[2], 0), dfwd(V[1], 0) - dfwd(V[0], 1)], 0)
    cB = curl(B); A = torch.zeros_like(B)
    for c in range(3):
        Ak = torch.fft.fftn(-cB[c]) / (-k2); Ak[0, 0, 0] = 0.0; A[c] = torch.fft.ifftn(Ak).real
    return float((A * B).sum(0).sum() * h**3 / (16 * math.pi**2))

# ---------------- G3: seven-point Dirichlet Poisson via direct DST-I inversion ----------------
def poisson_7pt_dst(rho_np, h):
    """Solve Delta_h u = rho on the cube with u=0 Dirichlet at the outer boundary (nodes outside the
    array are zero). Direct DST-I diagonalization of the SAME seven-point operator — exact to
    roundoff. rho_np: (M,M,M) float64 numpy. Returns u (M,M,M)."""
    M = rho_np.shape[0]
    k = np.arange(1, M + 1)
    lam1 = (2.0 * np.cos(np.pi * k / (M + 1)) - 2.0) / h**2       # per-axis eigenvalues (negative)
    LAM = lam1[:, None, None] + lam1[None, :, None] + lam1[None, None, :]
    R = dstn(rho_np, type=1, workers=-1)
    U = R / LAM
    u = idstn(U, type=1, workers=-1)
    return u

def lap7(u, h):
    """Explicit seven-point Laplacian with zero-Dirichlet exterior (for the RAW residual gate)."""
    up = np.zeros((u.shape[0] + 2,) * 3)
    up[1:-1, 1:-1, 1:-1] = u
    lap = (up[2:, 1:-1, 1:-1] + up[:-2, 1:-1, 1:-1] + up[1:-1, 2:, 1:-1] + up[1:-1, :-2, 1:-1]
           + up[1:-1, 1:-1, 2:] + up[1:-1, 1:-1, :-2] - 6.0 * u) / h**2
    return lap

def bond_flux(u, i0, i1, h):
    """Phi_h(C) = h * sum over bonds crossing the boundary of the index cube [i0, i1]^3 (inclusive)
    of (u_outside - u_inside). Telescopes the seven-point Laplacian exactly."""
    tot = 0.0
    # +x face: inside layer i1, outside i1+1 (zero-Dirichlet handled by array bounds: pad)
    up = np.zeros((u.shape[0] + 2,) * 3); up[1:-1, 1:-1, 1:-1] = u
    a, b = i0 + 1, i1 + 1                                          # indices in padded array
    sl = np.s_[a:b + 1]
    tot += (up[b + 1, sl, sl] - up[b, sl, sl]).sum()
    tot += (up[a - 1, sl, sl] - up[a, sl, sl]).sum()
    tot += (up[sl, b + 1, sl] - up[sl, b, sl]).sum()
    tot += (up[sl, a - 1, sl] - up[sl, a, sl]).sum()
    tot += (up[sl, sl, b + 1] - up[sl, sl, b]).sum()
    tot += (up[sl, sl, a - 1] - up[sl, sl, a]).sum()
    return h * tot

# =====================================================================================
result = dict(dispatch='H3 PHASE G — conditional mass readout on the corrected carrier (2026-07-16)',
              status_labels=dict(carrier='POSIT/CHOSE (S^2 carrier, L2+L4 functional)',
                                 discretization='DERIVED numerically (8-orientation, no Nyquist null, O(h^2))',
                                 lapse_identity='CONDITIONAL on the EH metric-only action premise',
                                 G='conditional consistency readout, NOT a native-UDT mass derivation',
                                 data_blind=True, kappa_g='not used (unit-response test)'),
              solver_note=('G3 Poisson: direct DST-I diagonalization of the seven-point Dirichlet operator '
                           '(exact to roundoff; supersedes continuum-kernel Hockney which had ~1.75% 7-point residual)'),
              torch=torch.__version__, scipy_dst='scipy.fft.dstn type-1',
              inputs={p: sha256(p) for p in ('noNull_critical_field_128.npz', 'noNull_critical_field_192.npz',
                                             'noNull_critical_field.npz', 'noNull_energy.py')},
              grids={})

scalars = {k: {} for k in ('E2', 'E4', 'Esum', 'twoE4', 'delta_vir')}
for (Ng, critf) in GRIDS:
    t0 = time.time()
    dc = np.load(critf)
    N, L, h, xi, kap = int(dc['N']), float(dc['L']), float(dc['h']), float(dc['xi']), float(dc['kappa'])
    n = torch.tensor(dc['n'], device=dev); n = n / n.norm(dim=0, keepdim=True)
    print(f"\n=== G: N={Ng} (h={h:.6f}) ===", flush=True)
    g = dict(N=N, L=L, h=h)

    # ---- G1 ----
    rho2, rho4, Ssrc = densities_NN(n, h, xi, kap)
    E_ref, E2_ref, E4_ref = energy_noNull(n, h, xi, kap)
    E2 = float(rho2.sum()) * h**3; E4 = float(rho4.sum()) * h**3
    rel2 = abs(E2 - float(E2_ref)) / abs(float(E2_ref)); rel4 = abs(E4 - float(E4_ref)) / abs(float(E4_ref))
    rho4_min = float(rho4.min())
    ident = float((rho2 + rho4 + Ssrc - 2 * rho4).abs().max()) / float((2 * rho4).abs().max())
    dvir = (E2 - E4) / (E2 + E4)
    Qf = charge_fwd_local(n, h); Qs = charge_sym_local(n, h)
    FM = torch.zeros(N, N, N, device=dev); FM[HBW:-HBW, HBW:-HBW, HBW:-HBW] = 1.0
    gr = grad_noNull(n, h, xi, kap); gf = (gr - (gr * n).sum(0, keepdim=True) * n) * FM
    precond, shift = make_precond(N, h, xi, dev)
    crit_raw = float(gf.norm()); crit_M = float(mnorm(gf, h))
    del gr, gf, precond
    g['G1'] = dict(E2=E2, E4=E4, Esum=E2 + E4, twoE4=2 * E4, E2_over_E4=E2 / E4, delta_vir=dvir,
                   energy_reproduction_rel=dict(E2=rel2, E4=rel4, gate_1e12=bool(rel2 < 1e-12 and rel4 < 1e-12)),
                   rho4_min=rho4_min, rho4_nonneg=bool(rho4_min >= -1e-18),
                   identity_rho_plus_S_eq_2rho4_relmax=ident, identity_gate_1e12=bool(ident < 1e-12),
                   Q_fwd=Qf, Q_sym=Qs, criticality_raw=crit_raw, criticality_Minv=crit_M)
    print(f"  G1: E2={E2:.6f} E4={E4:.6f} E2/E4={E2/E4:.6f} delta_vir={dvir:+.3e} | "
          f"reprod rel {rel2:.1e}/{rel4:.1e} | rho4_min={rho4_min:.1e} | ident={ident:.1e} | "
          f"Qf={Qf:.5f} Qs={Qs:.5f} | crit raw={crit_raw:.2e} M={crit_M:.2e}", flush=True)
    for k, v in (('E2', E2), ('E4', E4), ('Esum', E2 + E4), ('twoE4', 2 * E4), ('delta_vir', dvir)):
        scalars[k][Ng] = v

    # ---- G2: localization ----
    rho4_np = rho4.cpu().numpy(); rho2_np = rho2.cpu().numpy()
    del rho2, rho4, Ssrc, n; gc.collect(); torch.cuda.empty_cache()
    ax = (np.arange(N) - (N - 1) / 2) * h
    X3, Y3, Z3 = np.meshgrid(ax, ax, ax, indexing='ij')
    R3 = np.sqrt(X3**2 + Y3**2 + Z3**2); Amax = np.maximum.reduce([np.abs(X3), np.abs(Y3), np.abs(Z3)])
    loc = dict(cubes={}, spheres={})
    for a in CUBE_HALFWIDTHS:
        f = float(rho4_np[Amax <= a].sum() * h**3 / E4)
        loc['cubes'][f'{a:g}'] = dict(enclosed_E4_fraction=f, omitted_tail=1 - f)
    for r in SPHERE_RADII:
        f = float(rho4_np[R3 <= r].sum() * h**3 / E4)
        loc['spheres'][f'{r:g}'] = dict(enclosed_E4_fraction=f, omitted_tail=1 - f)
    g['G2_localization'] = loc
    del X3, Y3, Z3, R3, Amax
    print(f"  G2: cube tails {[(k, round(v['omitted_tail'], 6)) for k, v in loc['cubes'].items()]}", flush=True)

    # ---- G3 + G4 per padding ----
    g['G3_G4'] = {}
    for p in PADDINGS:
        Np = int(round(p * N))
        off = (Np - N) // 2
        rho_p = np.zeros((Np, Np, Np))
        rho_p[off:off + N, off:off + N, off:off + N] = rho4_np     # embed, zero outside — no interpolation
        t1 = time.time()
        u = poisson_7pt_dst(rho_p, h)
        res = lap7(u, h) - rho_p
        r_P = float(np.linalg.norm(res.ravel()) / np.linalg.norm(rho_p.ravel()))
        Lp = Np * h
        ctr = ((Np - 1) // 2, Np // 2)                             # site pair around center for even N
        u0 = float(u[ctr[0], ctr[0], ctr[0]] + u[ctr[1], ctr[1], ctr[1]]) / 2
        umin = float(u.min())
        radial = {}
        for r in (1.0, 2.0, 2.95):
            j = ctr[1] + int(round(r / h))
            if j < Np: radial[f'{r:g}'] = float(u[j, ctr[1], ctr[1]])
        # G4 fluxes on nested cubes (indices within the padded array, centered on the source)
        Q_tot = float(rho_p.sum() * h**3)
        fluxes = {}
        gate_worst = 0.0
        for a in CUBE_HALFWIDTHS + ((Lp / 2 - 2 * h) / 1,) if p > 1.0 else CUBE_HALFWIDTHS:
            m = int(round(a / h))
            i0 = max(ctr[1] - m, 0); i1 = min(ctr[0] + m, Np - 1)   # 2m sites, symmetric about the center plane
            Phi = bond_flux(u, i0, i1, h)
            Q_C = float(rho_p[i0:i1 + 1, i0:i1 + 1, i0:i1 + 1].sum() * h**3)
            res_C = float(res[i0:i1 + 1, i0:i1 + 1, i0:i1 + 1].sum() * h**3)
            err = abs(Phi - Q_C) / max(abs(Q_C), 1e-30)
            gate_worst = max(gate_worst, err)
            fluxes[f'{a:g}'] = dict(index_halfwidth=m, Phi=Phi, Q_enclosed=Q_C,
                                    flux_gauss_relerr=err, residual_integral_explains=res_C,
                                    Phi_minus_Q=Phi - Q_C,
                                    tail_fraction=1 - Q_C / Q_tot,
                                    M_N0=2 * Phi, M_N0_over_2E4=2 * Phi / (2 * E4))
        uf = f'noNull_phaseG_u_N{Ng}_p{p:g}.npz'
        np.savez(uf, u=u, Np=Np, Lp=Lp, h=h, off=off, N=N)           # saved response field (verifier input)
        g['G3_G4'][f'p{p:g}'] = dict(Np=Np, Lp=Lp, r_P=r_P, r_P_gate_1e9=bool(r_P < 1e-9),
                                     u_field_file=uf, u_field_sha256=sha256(uf),
                                     u_center=u0, u_min=umin, u_radial=radial,
                                     Q_total=Q_tot, fluxes=fluxes,
                                     gauss_gate_1e6=bool(gate_worst < 1e-6), gauss_worst=gate_worst,
                                     solve_seconds=time.time() - t1)
        print(f"  G3/G4 p={p:g}: Np={Np} r_P={r_P:.2e} u0={u0:.6f} umin={umin:.6f} "
              f"gauss_worst={gate_worst:.2e} M/2E4@a=2.95: "
              f"{fluxes['2.95']['M_N0_over_2E4']:.8f} (tail {fluxes['2.95']['tail_fraction']:.2e})", flush=True)
        del u, res, rho_p; gc.collect()
    result['grids'][str(Ng)] = g
    print(f"  N={Ng} done ({time.time()-t0:.0f}s)", flush=True)
    del rho4_np, rho2_np; gc.collect()

# ---- G2 continuum audit across grids ----
H = {Ng: float(np.load(f)['h']) for (Ng, f) in GRIDS}
conv = {}
for k, vals in scalars.items():
    v128, v192, v256 = vals[128], vals[192], vals[256]
    h2 = {Ng: H[Ng]**2 for Ng in (128, 192, 256)}
    sc = (v128 - v192) / (h2[128] - h2[192]); sf = (v192 - v256) / (h2[192] - h2[256])
    rich = v256 - sf * h2[256]
    A = np.array([[1, h2[Ng], h2[Ng]**2] for Ng in (128, 192, 256)])
    b = np.array([v128, v192, v256]); lam0q, cq, dq = np.linalg.solve(A, b)
    conv[k] = dict(raw={'128': v128, '192': v192, '256': v256},
                   h2_slope_coarse=sc, h2_slope_fine=sf, pure_h2=bool(abs(sc - sf) < 0.05 * max(abs(sc), abs(sf), 1e-30)),
                   richardson_fine_pair=rich, three_point_h2h4=float(lam0q),
                   h4_coeff=float(dq))
    print(f"  conv {k}: 128={v128:.6f} 192={v192:.6f} 256={v256:.6f} slopes {sc:+.4f}/{sf:+.4f} "
          f"Richardson={rich:.6f} 3pt={lam0q:.6f}", flush=True)
result['G2_continuum_audit'] = conv
result['conclusion'] = ('CONDITIONAL on the EH lapse identity, weak-field unit response: M_N^(0) = 2*E4 '
                        'within the displayed discretization, source-tail, linearization, and boundary errors. '
                        '2E4 vs E2+E4 differ by the measured virial discrepancy delta_vir (reported; not '
                        'silently identified). This is a Gauss-identity consistency readout on the certified '
                        'carrier — the informative outputs are the corrected E4, virial relation, convergence, '
                        'localization, and the conditional readout itself.')
json.dump(result, open('noNull_phaseG_mass_ALL.json', 'w'), indent=1, default=float)
print('\nwrote noNull_phaseG_mass_ALL.json', flush=True)

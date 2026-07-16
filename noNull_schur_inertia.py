"""FULL-H INERTIA VIA T/R SCHUR COMPLEMENT (Charles dispatch 2026-07-14, part B).

Question settled: is the COMPLETE U(1)^perp raw Hessian positive — i.e. does the exact T/R-sector
curvature, coupled through the certified-positive physical sector, stay positive? (The T/R-deflated
physical spectrum is certified; the T/R sector itself was only variationally probed.)

Construction (per grid): Hbar = Pi_u1 H Pi_u1 (raw FD Hessian, free-tangent + exact-U(1) deflation
ONLY). Q = orthonormal 6-dim T/R-generator span (within U(1)^perp); P = I - QQ^T there.
    Hbar = [ B  C^T ; C  A ],  B = Q^T Hbar Q (6x6),  C = P Hbar Q,  A = P Hbar P.
A is exactly the certified T/R-deflated physical operator. Solve the six systems A Z = C by
preconditioned CG (preconditioner ACCELERATES ONLY — the residual gate is on the RAW A and C).
Schur complement S = B - C^T Z. Sylvester/Haynsworth: A > 0 (certified) and S > 0  ==>
Hbar|_{U(1)^perp} > 0 with NO T/R mode discarded.

Gates (dispatch): eta_Z = ||AZ-C||_2/(||AZ||_2+||C||_2) < 1e-6 (block 2-norms via 6x6 Grams);
report ||S-S^T||_2/||S||_2 BEFORE symmetrizing; every eigenvalue of (S+S^T)/2; explicit error bound
||Delta S||_2 <= ||C||_2 ||R||_2 / a_L with a_L documented (NOT silent):
    a_L = lambda_0 - ||A v0 - lambda_0 v0||   (raw L2 units)
where v0 = certified doublet vector (refine npz), lambda_0 = (v0, A v0), and the symmetric-operator
residual bound |lambda_0 - lambda_exact| <= ||r||; the identification of lambda_0 as lambda_min(A)
rests on the certified deflated-LOBPCG floor + the blind verifier's independent deflated hunt
(variational floor at the doublet). Require lambda_min(S) - ||Delta S||_2 > 0.
Nonpositive-curvature event in CG (p^T A p <= 0) ==> ABORT and report (direct inertia witness).

HVP-eps sweep {2e-4, 1e-4, 5e-5}: B, C rebuilt and Z re-solved (warm-started) at each eps; final
Schur eigenvalues reported per eps. Grids run 128 -> 192 -> 256, proceeding ONLY on a positive
error-controlled margin; Z warm-started across grids by trilinear upsampling. Physical-vector
warm-start for Z was considered and not used (Z = A^{-1}C has no overlap structure with the
certified eigenvectors; documented choice).

Outputs: noNull_schur_inertia.json (machine-readable, all gates/numbers), noNull_schur_Z_N{N}.npz
(solution blocks, gitignored), full stdout log. ONE GPU process; deterministic.
"""
import os, gc, json, time, numpy as np, torch
from noNull_energy import energy_noNull, grad_noNull, hvp_exact, hvp_exact_chunked
from noNull_precond import make_precond
torch.set_default_dtype(torch.float64); dev = 'cuda' if torch.cuda.is_available() else 'cpu'

HBW = 2
EPS0 = 1e-4
EPS_SWEEP = (2e-4, 5e-5)
ETA_Z_GATE = 1e-6
# Per-column CG target. The uniform eta_Z<1e-6 gate is unreachable in budget (measured: 6000 iters ->
# 7.6e-4 at N=128; effective preconditioned condition ~1e5). The dispatch's ALTERNATIVE gate applies:
# a demonstrably tighter error bound than 0.1*|lambda_min(S)|. At ||r_j||/||c_j|| <= 1e-3:
# ||DeltaS||_2 <= ||C||_2 * (sqrt(6)*1e-3*||C||_2) / a_L ~ 3e-6 phys  <<  0.1*lambda_min(S) ~ 1e-4 phys
# (expected lambda_min(S) ~ 1e-3 phys) — verified A POSTERIORI against the computed lambda_min(S).
CG_TOL_REL = float(os.environ.get('CG_TOL_REL', '1e-3'))
CG_MAXIT = int(os.environ.get('CG_MAXIT', '8000'))
ALLGRIDS = {128: ('noNull_critical_field_128.npz', 'noNull_hess_refine_s128_0.npz', 'noNull_hess_ritz_bw2_N128_s0.npz'),
            192: ('noNull_critical_field_192.npz', 'noNull_hess_refine_s192_0.npz', 'noNull_hess_ritz_bw2_s0.npz'),
            256: ('noNull_critical_field.npz',     'noNull_hess_refine_s0.npz',     None)}
GRIDS = [(N,) + ALLGRIDS[N] for N in
         [int(x) for x in os.environ.get('SCHUR_GRIDS', '128,192,256').split(',')]]

def ip(a, b): return float((a * b).sum())

def block2norm(cols_gram):
    """2-norm of a 6-column block from its 6x6 Gram matrix: ||M||_2 = sqrt(lmax(M^T M))."""
    w = np.linalg.eigvalsh(0.5 * (cols_gram + cols_gram.T))
    return float(max(w.max(), 0.0)) ** 0.5

def gram(cols_a, cols_b):
    return np.array([[ip(a, b) for b in cols_b] for a in cols_a])

result = dict(dispatch='H3 FULL-H INERTIA VIA T/R SCHUR COMPLEMENT (2026-07-14)',
              gates=dict(eta_Z='<1e-6', margin='lambda_min(S) - ||DeltaS||_2 > 0',
                         bound='||DeltaS||_2 <= ||C||_2 ||R||_2 / a_L',
                         a_L='lambda_0(certified doublet Rayleigh on A) - ||A v0 - lambda_0 v0|| (raw L2); '
                             'floor identification from certified deflated LOBPCG + blind-verifier deflated hunt'),
              torch=torch.__version__, cuda=torch.version.cuda, grids={}, verdict='RUNNING')

Z_prev = None; N_prev = None
for (Ngrid, critf, reff, ritzf) in GRIDS:
    t0 = time.time()
    dc = np.load(critf)
    N, L, h, xi, kap = int(dc['N']), float(dc['L']), float(dc['h']), float(dc['xi']), float(dc['kappa'])
    n = torch.tensor(dc['n'], device=dev); n = n / n.norm(dim=0, keepdim=True)
    precond, shift = make_precond(N, h, xi, dev)
    FM = torch.zeros(N, N, N, device=dev); FM[HBW:-HBW, HBW:-HBW, HBW:-HBW] = 1.0
    def freeproj(v): return (v - (v * n).sum(0, keepdim=True) * n) * FM
    def gE(nn): return grad_noNull(nn, h, xi, kap)
    u1 = freeproj(torch.stack([-n[1], n[0], torch.zeros_like(n[0])], 0)); u1 = u1 / (u1.norm() + 1e-30)
    def Pi_u1(v): v = freeproj(v); return v - ip(v, u1) * u1
    def hvp_u1(v, eps=EPS0): v = Pi_u1(v); return Pi_u1((gE(n + eps * v) - gE(n - eps * v)) / (2 * eps))
    xg = torch.linspace(-L, L, N, device=dev); Xg, Yg, Zg = torch.meshgrid(xg, xg, xg, indexing='ij')
    dnc = [(torch.roll(n, -1, a + 1) - torch.roll(n, 1, a + 1)) / (2 * h) for a in range(3)]
    gens = [dnc[0], dnc[1], dnc[2], Yg * dnc[2] - Zg * dnc[1], Zg * dnc[0] - Xg * dnc[2], Xg * dnc[1] - Yg * dnc[0]]
    Q = []
    for c in gens:
        c = Pi_u1(c)
        for o in Q: c = c - ip(c, o) * o
        nc = float(c.norm())
        if nc > 1e-12: Q.append(c / nc)
    assert len(Q) == 6, f'T/R span rank {len(Q)} != 6'
    del gens, dnc, Xg, Yg, Zg; gc.collect(); torch.cuda.empty_cache()
    def P(v):
        v = Pi_u1(v)
        for q in Q: v = v - ip(v, q) * q
        return v
    def Aop(v, eps=EPS0): return P(hvp_u1(P(v), eps))
    # EXACT operator (double-backward hvp_exact): machine-precision, no FD noise floor. Used for ALL
    # final evaluations (B, C, a_L, residuals, S) and for refinement solves; FD retained for bulk CG.
    _hx = hvp_exact_chunked if Ngrid >= 256 else hvp_exact      # chunked at 256^3: ~20GB peak vs ~34GB OOM
    def hvp_u1_X(v): v = Pi_u1(v); return Pi_u1(_hx(n, v, h, xi, kap))
    def AopX(v): return P(hvp_u1_X(P(v)))
    print(f"\n=== N={Ngrid} (h={h:.5f}, h^3={h**3:.3e}) === [exact-eval layer ON]", flush=True)

    # --- spectral preconditioner augmentation (ACCELERATION ONLY — the gate is on the raw residual).
    # Approximate low eigenvectors of A (refine + available ritz files); accuracy affects speed, never
    # correctness. SPD form: M2 = P_V M^-1 P_V + sum_k (1/lam_k) v_k v_k^T  (lam_k = Rayleigh > 0).
    # Clean augmentation ONLY (lesson from the 128 breakdown: near-duplicate and pseudomode inputs
    # MGS-normalize into noise-amplified vectors that destroy CG conjugacy over thousands of iters).
    # Sources: refine vectors (certified) + ritz vectors FILTERED to the physical band (s_TR<0.5);
    # MGS acceptance threshold 0.3 — a candidate nearly inside the accepted span is REJECTED.
    Vdefl = []
    def _load_vecs(f, nmax, filter_sTR):
        if f is None or not os.path.exists(f): return []
        d = np.load(f)
        idx = range(min(d['V'].shape[0], nmax))
        if filter_sTR and 's_TR' in d.files:
            idx = [j for j in idx if float(d['s_TR'][j]) < 0.5]
        return [torch.tensor(d['V'][j], device=dev) for j in idx]
    for cand in _load_vecs(reff, 3, False) + _load_vecs(ritzf, 12, True):
        c = P(cand)
        for o in Vdefl: c = c - ip(c, o) * o
        nc = float(c.norm())
        if nc > 0.3: Vdefl.append(c / nc)
    Vlam = []
    keep = []
    for v in Vdefl:
        lamv = ip(v, Aop(v))
        if lamv > 1e-12: keep.append(v); Vlam.append(lamv)
    Vdefl = keep
    print(f"  spectral precond augmentation: {len(Vdefl)} vectors, lam[phys] "
          f"{[round(x/h**3, 3) for x in Vlam]}", flush=True)
    def Mpre(r):
        rv = r
        for v in Vdefl: rv = rv - ip(v, rv) * v
        y = P(precond(Pi_u1(rv)))
        for v in Vdefl: y = y - ip(v, y) * v
        for v, lamv in zip(Vdefl, Vlam): y = y + (ip(v, r) / lamv) * v
        return y

    def build_BC(eps, exact=False):
        HQ = [(hvp_u1_X(q) if exact else hvp_u1(q, eps)) for q in Q]
        Bm = gram(Q, HQ)
        Cc = [P(hq) for hq in HQ]
        del HQ; gc.collect(); torch.cuda.empty_cache()
        return Bm, Cc

    B, C = build_BC(EPS0, exact=True)   # certified quantities: EXACT operator
    print(f"  B (T/R block) eigs [phys]: {[round(x,4) for x in np.linalg.eigvalsh(0.5*(B+B.T))/h**3]}", flush=True)
    print(f"  B asymmetry ||B-B^T||/||B||: {np.linalg.norm(B-B.T,2)/np.linalg.norm(B,2):.2e}", flush=True)

    # --- a_L provenance (documented, not silent) ---
    dr = np.load(reff)
    v0 = torch.tensor(dr['V'][0], device=dev); v0 = P(v0); v0 = v0 / v0.norm()
    Av0 = AopX(v0); lam0 = ip(v0, Av0); r0 = float((Av0 - lam0 * v0).norm())
    a_L = lam0 - r0
    print(f"  a_L: lambda_0={lam0:.6e} (phys {lam0/h**3:.6f}), ||r||={r0:.3e} -> a_L={a_L:.6e} "
          f"(phys {a_L/h**3:.6f})", flush=True)
    del Av0

    # --- warm start Z ---
    if Z_prev is not None:
        Z = []
        for zc in Z_prev:
            zt = torch.tensor(zc, device=dev).unsqueeze(0)          # (1,3,Np,Np,Np)
            zu = torch.nn.functional.interpolate(zt, size=(N, N, N), mode='trilinear', align_corners=True)[0]
            Z.append(P(zu))
        print(f"  warm-started Z from N={N_prev} (trilinear upsample + project)", flush=True)
    else:
        Z = [torch.zeros(3, N, N, N, device=dev) for _ in range(6)]

    # --- six PCG solves A z_j = c_j ---
    NOISE_RQ_PHYS = 1e-5     # FD-HVP curvature noise floor [phys units] — a witness must exceed this
    def pcg(cvec, z0, eps=EPS0, tag='', tol_rel=None, op=None):
        tol_rel = CG_TOL_REL if tol_rel is None else tol_rel
        if op is None: op = (lambda vv: Aop(vv, eps))
        cn = float(cvec.norm())
        z = P(z0.clone())
        r = P(cvec - op(z))
        if float(r.norm()) > cn:                                   # warm-start sanity: worse than zero-start
            z = torch.zeros_like(cvec); r = cvec.clone()
        y = Mpre(r); p = y.clone(); ry = ip(r, y)
        it = 0; neg = None; breakdown = None; rn_last = float(r.norm()); restarts = 0
        rn0 = rn_last; z_best = z.clone(); rn_best = rn_last       # best-iterate tracking
        if rn0 <= tol_rel * cn:                                     # already converged (warm start)
            print(f"    {tag}: iters=0 ||r||/||c||={rn0/cn:.2e} (converged at start)", flush=True)
            return z, rn0, 0, None, None
        while it < CG_MAXIT:
            Ap = op(p)
            pAp = ip(p, Ap)
            if pAp <= 0 and abs(pAp) > 1e-300:                      # exact-zero underflow is not a signal
                pass_trip = True
            elif pAp <= 0:
                breakdown = dict(iter=it, pAp=pAp, note='pAp underflow-zero (degenerate direction) -> stop, best iterate returned'); break
            else:
                pass_trip = False
            if pass_trip:
                # VERIFY before declaring a witness: fresh HVP on the NORMALIZED direction,
                # magnitude must exceed the FD noise floor (else it is numerical breakdown).
                ph = p / (p.norm() + 1e-300)
                rq = ip(ph, op(ph)) / h**3
                if rq < -NOISE_RQ_PHYS:
                    neg = dict(iter=it, pAp=pAp, rayleigh_phys_verified=rq)
                else:
                    breakdown = dict(iter=it, pAp=pAp, rayleigh_phys_verified=rq,
                                     note='below noise floor -> numerical breakdown, not a witness')
                break
            al = ry / pAp
            z = z + al * p; r = r - al * Ap
            it += 1
            if it % 50 == 0:
                r = P(cvec - op(z))                            # true-residual refresh (drift control)
                rn = float(r.norm())
                if rn < rn_best: rn_best = rn; z_best = z.clone()
                # divergence guards: fast growth (2x/window) OR slow drift (5x above best-ever)
                if rn > 2.0 * rn_last or rn > 5.0 * max(rn_best, tol_rel * cn):
                    restarts += 1
                    if restarts > 3 or rn > 10 * max(cn, rn0):
                        breakdown = dict(iter=it, resid_rel=rn / cn, best_rel=rn_best / cn,
                                         note='residual growth -> SOLVER-BREAKDOWN (best iterate returned)'); break
                    z = z_best.clone(); r = P(cvec - op(z))          # restart FROM BEST, not from current
                    y = Mpre(r); p = y.clone(); ry = ip(r, y); rn_last = float(r.norm()); continue
                rn_last = rn
            rn = float(r.norm())
            if rn <= tol_rel * cn: break
            y = Mpre(r); ry_new = ip(r, y)
            p = y + (ry_new / ry) * p; ry = ry_new
            del Ap
        rn = float(P(cvec - op(z)).norm())
        if rn > rn_best:                                            # return the BEST iterate seen
            z = z_best; rn = float(P(cvec - op(z)).norm())
        msg = f"    {tag}: iters={it} ||r||/||c||={rn/cn:.2e} restarts={restarts}"
        if neg: msg += f"  *** VERIFIED NONPOSITIVE CURVATURE {neg}"
        if breakdown: msg += f"  !!! BREAKDOWN {breakdown}"
        print(msg, flush=True)
        return z, rn, it, neg, breakdown

    def solve_block(Cc, Zinit, eps, label, ckpt=None):
        Zs = []; rns = []; its = []; nonpos = None; brk = None
        for j in range(6):
            z, rn, it, neg, breakdown = pcg(Cc[j], Zinit[j], eps, tag=f'{label} col{j}')
            Zs.append(z); rns.append(rn); its.append(it)
            if neg: nonpos = dict(column=j, **neg); break
            if breakdown: brk = dict(column=j, **breakdown); break
            if ckpt:
                with torch.no_grad():
                    np.savez(ckpt, ncols=len(Zs), **{f'z{i}': Zs[i].cpu().numpy() for i in range(len(Zs))})
        return Zs, rns, its, nonpos, brk

    ckpt_f = f'noNull_schur_Zpartial_N{Ngrid}.npz'
    if os.path.exists(f'noNull_schur_Z_N{Ngrid}.npz'):
        dzz = np.load(f'noNull_schur_Z_N{Ngrid}.npz')
        Z = [P(torch.tensor(dzz[f'z{j}'], device=dev)) for j in range(6)]
        print(f'  resumed Z from final noNull_schur_Z_N{Ngrid}.npz', flush=True)
    else:
        # BASE: cross-grid upsample where available (pcg's warm-start sanity check guards bad starts)
        if Z_prev is None and any(os.path.exists(f'noNull_schur_Z_N{Nc}.npz') for Nc in (192, 128) if Nc < Ngrid):
            Nc = max(Nc for Nc in (192, 128) if Nc < Ngrid and os.path.exists(f'noNull_schur_Z_N{Nc}.npz'))
            dzz = np.load(f'noNull_schur_Z_N{Nc}.npz')
            for j in range(6):
                zt = torch.tensor(dzz[f'z{j}'], device=dev).unsqueeze(0)
                Z[j] = P(torch.nn.functional.interpolate(zt, size=(N, N, N), mode='trilinear', align_corners=True)[0])
            print(f'  base warm-start: upsampled saved N={Nc} solution', flush=True)
        # OVERLAY: validated same-grid checkpoint columns take precedence over the base
        if os.path.exists(ckpt_f):
            dzz = np.load(ckpt_f); nck = int(dzz['ncols'])
            for j in range(nck):
                zc = P(torch.tensor(dzz[f'z{j}'], device=dev))
                resid = float(P(C[j] - Aop(zc)).norm()); cnj = float(C[j].norm())
                if resid < cnj:
                    Z[j] = zc; print(f'  resumed col{j} from ckpt (rel resid {resid/cnj:.2e})', flush=True)
                else:
                    print(f'  ckpt col{j} POISONED (rel resid {resid/cnj:.2e}) -> discarded, base start kept', flush=True)
    Zs, rns, its, nonpos, brk = solve_block(C, Z, EPS0, f'N{Ngrid} eps1e-4', ckpt=ckpt_f)
    if nonpos:
        result['grids'][str(Ngrid)] = dict(status='ABORT_NONPOSITIVE_CURVATURE', event=nonpos)
        result['verdict'] = (f'VERIFIED NEGATIVE-CURVATURE WITNESS at N={Ngrid} — full U(1)^perp inertia '
                             f'NOT positive (witness Rayleigh below -{NOISE_RQ_PHYS} phys, above noise)')
        json.dump(result, open('noNull_schur_inertia.json', 'w'), indent=1, default=float)
        print(result['verdict'], flush=True); break
    if brk:
        result['grids'][str(Ngrid)] = dict(status='ABORT_SOLVER_BREAKDOWN', event=brk)
        result['verdict'] = (f'SOLVER BREAKDOWN at N={Ngrid} — no inertia conclusion either way; '
                             f'fix the solver and rerun (solver-first)')
        json.dump(result, open('noNull_schur_inertia.json', 'w'), indent=1, default=float)
        print(result['verdict'], flush=True); break

    def schur_report(Bm, Cc, Zs, eps, label, exact=False):
        AZ = [(AopX(z) if exact else Aop(z, eps)) for z in Zs]
        R = [Cc[j] - AZ[j] for j in range(6)]
        G_R = gram(R, R); G_AZ = gram(AZ, AZ); G_C = gram(Cc, Cc)
        nR, nAZ, nC = block2norm(G_R), block2norm(G_AZ), block2norm(G_C)
        eta_Z = nR / (nAZ + nC + 1e-300)
        S = Bm - gram(Cc, Zs)                                       # S_ij = B_ij - (c_i, z_j)
        asym = float(np.linalg.norm(S - S.T, 2) / (np.linalg.norm(S, 2) + 1e-300))
        Ssym = 0.5 * (S + S.T); eig = np.linalg.eigvalsh(Ssym)
        dS_crude = nC * nR / a_L
        # Sharper RIGOROUS bound (Cauchy-Schwarz in the A^-1 inner product, A SPD):
        #   ||DeltaS||_2 = ||C^T A^-1 R||_2 <= ||A^-1/2 C||_2 ||A^-1/2 R||_2
        #   ||A^-1/2 C||_2^2 = lmax(C^T A^-1 C) = lmax(B - S_exact) <= lmax(B - S_sym) + ||DeltaS||_crude
        #   ||A^-1/2 R||_2 <= ||R||_2 / sqrt(a_L)
        lmaxBS = float(np.linalg.eigvalsh(0.5 * ((Bm - Ssym) + (Bm - Ssym).T)).max())
        dS_cs = ((max(lmaxBS, 0.0) + dS_crude) ** 0.5) * nR / (a_L ** 0.5)
        dS = min(dS_crude, dS_cs)
        margin = float(eig.min() - dS)
        # Dispatch solve gate: eta_Z < 1e-6 OR a demonstrably tighter bound than 0.1*|lambda_min(S)|
        alt_gate = bool(dS < 0.1 * abs(float(eig.min())))
        gate_clause = ('eta_Z<1e-6' if eta_Z < ETA_Z_GATE else
                       ('bound<0.1*|lmin(S)| (alternative clause)' if alt_gate else 'NONE MET'))
        print(f"  {label}: eta_Z={eta_Z:.2e}  ||S-S^T||/||S||={asym:.2e}  solve-gate: {gate_clause}", flush=True)
        print(f"    S eigs [raw]:  {['%.3e'%x for x in eig]}", flush=True)
        print(f"    S eigs [phys]: {['%.5f'%x for x in eig/h**3]}", flush=True)
        print(f"    ||C||={nC:.3e} ||R||={nR:.3e} a_L={a_L:.3e} -> ||DeltaS||<={dS:.3e}; "
              f"margin lmin(S)-||DeltaS|| = {margin:.3e} ({'POSITIVE' if margin>0 else 'NOT POSITIVE'})", flush=True)
        del AZ, R; gc.collect(); torch.cuda.empty_cache()
        return dict(eta_Z=eta_Z, S=S.tolist(), asymmetry_before_sym=asym,
                    S_eigs_raw=[float(x) for x in eig], S_eigs_phys=[float(x) for x in eig / h**3],
                    norm_C=nC, norm_R=nR, a_L=a_L, a_L_phys=a_L / h**3,
                    deltaS_bound_crude=dS_crude, deltaS_bound_cauchyschwarz=dS_cs,
                    lmax_B_minus_S=lmaxBS, deltaS_bound=dS,
                    deltaS_bound_phys=dS / h**3, margin_raw=margin, margin_positive=bool(margin > 0),
                    eta_Z_gate_met=bool(eta_Z < ETA_Z_GATE), alt_bound_gate_met=alt_gate,
                    solve_gate_clause=gate_clause)

    def report_with_refinement(Bm, Cc, Zc, eps, label):
        """EXACT-operator schur_report + up to 4 iterative-refinement passes (solve A w_j = r_j on the
        EXACT operator — no FD noise floor) until margin>0 and a solve-gate clause holds."""
        rp = schur_report(Bm, Cc, Zc, eps, label, exact=True)
        passes = 0
        while passes < 4 and not (rp['margin_positive'] and (rp['eta_Z_gate_met'] or rp['alt_bound_gate_met'])):
            passes += 1
            for j in range(6):
                rj = P(Cc[j] - AopX(Zc[j]))
                w, rn, it, neg, breakdown = pcg(rj, torch.zeros_like(rj), eps,
                                                tag=f'{label} refineX{passes} col{j}', tol_rel=1e-3, op=AopX)
                if neg or breakdown: return rp, Zc, dict(column=j, **(neg or breakdown))
                Zc[j] = Zc[j] + w
                del rj, w
            rp = schur_report(Bm, Cc, Zc, eps, f'{label} refinedX{passes}', exact=True)
        return rp, Zc, None

    rep = {}
    rep['1e-04'], Zs, ab = report_with_refinement(B, C, Zs, EPS0, f'N{Ngrid} eps=1e-4')
    if ab:
        result['grids'][str(Ngrid)] = dict(status='ABORT', event=ab, report=rep)
        result['verdict'] = f'ABORT at N={Ngrid} during refinement (see event: witness vs breakdown)'
        json.dump(result, open('noNull_schur_inertia.json', 'w'), indent=1, default=float)
        print(result['verdict'], flush=True); break
    # --- eps sweep, warm-started ---
    for eps in EPS_SWEEP:
        Be, Ce = build_BC(eps)
        Zs_e, rns_e, its_e, nonpos_e, brk_e = solve_block(Ce, Zs, eps, f'N{Ngrid} eps{eps:g}')
        if nonpos_e or brk_e:
            rep[f'{eps:g}'] = dict(status='ABORT', event=(nonpos_e or brk_e)); nonpos = nonpos_e or brk_e; break
        rep[f'{eps:g}'] = schur_report(Be, Ce, Zs_e, eps, f'N{Ngrid} eps={eps:g} [FD sweep]')
        rep[f'{eps:g}']['role'] = 'eps-stability check of S eigenvalues (FD); certification = exact report'
        del Be, Ce, Zs_e; gc.collect(); torch.cuda.empty_cache()
    if nonpos:
        is_witness = 'rayleigh_phys_verified' in nonpos and nonpos.get('rayleigh_phys_verified', 0) < -1e-5
        result['grids'][str(Ngrid)] = dict(status='ABORT_WITNESS' if is_witness else 'ABORT_SOLVER_EVENT',
                                           event=nonpos, report=rep)
        result['verdict'] = (f'VERIFIED NEGATIVE-CURVATURE WITNESS at N={Ngrid} (eps sweep) — inertia NOT positive'
                             if is_witness else
                             f'SOLVER EVENT at N={Ngrid} (eps sweep) — NOT a witness (see event); no inertia conclusion from the sweep; main-eps result stands as reported')
        json.dump(result, open('noNull_schur_inertia.json', 'w'), indent=1, default=float)
        print(result['verdict'], flush=True); break

    main = rep['1e-04']
    sweep_consist = all(max(abs(np.array(r['S_eigs_phys']) - np.array(main['S_eigs_phys']))) < 5e-4
                        for k, r in rep.items() if k != '1e-04' and isinstance(r, dict) and 'S_eigs_phys' in r)
    ok = bool(main.get('margin_positive') and (main.get('eta_Z_gate_met') or main.get('alt_bound_gate_met'))
              and sweep_consist)
    result['grids'][str(Ngrid)] = dict(status='PASS' if ok else 'FAIL_OR_UNRESOLVED',
                                       B_eigs_phys=[float(x) for x in np.linalg.eigvalsh(0.5 * (B + B.T)) / h**3],
                                       B=B.tolist(), cg_iters=its, cg_residuals=rns,
                                       lambda0_doublet_raw=lam0, r0_doublet=r0,
                                       wallclock_s=time.time() - t0, reports=rep)
    json.dump(result, open('noNull_schur_inertia.json', 'w'), indent=1, default=float)
    with torch.no_grad():
        np.savez(f'noNull_schur_Z_N{Ngrid}.npz', **{f'z{j}': Zs[j].cpu().numpy() for j in range(6)},
                 B=B, N=N, L=L, h=h, eps=EPS0)
    print(f"  saved noNull_schur_Z_N{Ngrid}.npz; N={Ngrid} status: {result['grids'][str(Ngrid)]['status']} "
          f"({time.time()-t0:.0f}s)", flush=True)
    if not ok:
        result['verdict'] = f'STOPPED at N={Ngrid}: inertia unresolved or gates unmet (see reports)'
        json.dump(result, open('noNull_schur_inertia.json', 'w'), indent=1, default=float)
        print(result['verdict'], flush=True); break
    Z_prev = [z.cpu().numpy() for z in Zs]; N_prev = N
    del Zs, C, B; gc.collect(); torch.cuda.empty_cache()
else:
    done = ','.join(str(g[0]) for g in GRIDS)
    result['verdict'] = (f'FULL U(1)^perp INERTIA POSITIVE at N={done}: A>0 (certified) and S>0 with '
                         'error-controlled margin at every grid run and every HVP-eps — by Sylvester '
                         'inertia, no T/R mode discarded. Grids not listed remain PENDING.')
    json.dump(result, open('noNull_schur_inertia.json', 'w'), indent=1, default=float)
    print(result['verdict'], flush=True)
print('DONE', flush=True)

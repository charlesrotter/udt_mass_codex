"""FRESH INDEPENDENT VERIFIER for the Schur inertia seal (Charles dispatch 2026-07-14, item 9).

Imports ONLY the black-box noNull energy/gradient. Reads the saved solution blocks
(noNull_schur_Z_N{N}.npz) and the critical fields, and INDEPENDENTLY recomputes with its own code:
  - the T/R generator span Q and its orthogonality (within free-tangent, U(1)-deflated space);
  - B = Q^T Hbar Q, C = P Hbar Q, the block residual AZ - C (own HVP, own projections);
  - the Schur matrix S = B - C^T Z, its pre-symmetrization asymmetry, its eigenvalues;
  - the error bound ||DeltaS||_2 <= ||C||_2 ||R||_2 / a_L with its own a_L recomputation
    (certified doublet vector from the refine npz; a_L = lambda_0 - ||A v0 - lambda_0 v0||);
  - the inertia verdict: A>0 (certified floor, cross-checked via v0) AND S>0 with margin
    ==> full U(1)^perp Hessian positive by Sylvester inertia.
No quantity is copied from noNull_schur_inertia.json; that file is only compared against at the end.
Emits noNull_schur_verify_output.txt + noNull_schur_verify.json. ONE GPU process.
"""
import os, gc, json, numpy as np, torch
from noNull_energy import grad_noNull, hvp_exact, hvp_exact_chunked   # black-box energy derivatives ONLY
# (hvp_exact* are autograd double-backward of the SAME black-box energy — machine-precision H, no FD
#  noise floor; the FD-HVP verifier variant hits the measurement floor at 256^3 and cannot resolve
#  the margin there. Chunked variant used at N>=256 for memory.)
torch.set_default_dtype(torch.float64); dev = 'cuda' if torch.cuda.is_available() else 'cpu'

W = 2                                            # pinned boundary width (fixed layers)
EPS = 1e-4
GRIDS = [(128, 'noNull_critical_field_128.npz', 'noNull_hess_refine_s128_0.npz'),
         (192, 'noNull_critical_field_192.npz', 'noNull_hess_refine_s192_0.npz'),
         (256, 'noNull_critical_field.npz',     'noNull_hess_refine_s0.npz')]

lines = []
def say(s):
    lines.append(s); print(s, flush=True)

def dot(a, b): return float((a * b).sum())

out = {}
for (Ng, critf, reff) in GRIDS:
    zf = f'noNull_schur_Z_N{Ng}.npz'
    if not os.path.exists(zf):
        say(f'N={Ng}: {zf} MISSING (solve not run or aborted earlier) — skipped'); out[str(Ng)] = 'missing'; continue
    dc = np.load(critf)
    N, L, h, xi, kap = int(dc['N']), float(dc['L']), float(dc['h']), float(dc['xi']), float(dc['kappa'])
    n = torch.tensor(dc['n'], device=dev); n = n / n.norm(dim=0, keepdim=True)
    mask = torch.zeros(N, N, N, device=dev); mask[W:-W, W:-W, W:-W] = 1.0
    def tanfree(v): return (v - (v * n).sum(0, keepdim=True) * n) * mask
    # own U(1) generator and projector
    g_u1 = tanfree(torch.stack([-n[1], n[0], torch.zeros_like(n[0])], 0)); g_u1 = g_u1 / g_u1.norm()
    def proj_u1perp(v): v = tanfree(v); return v - dot(v, g_u1) * g_u1
    # own Hbar via the EXACT black-box Hessian (double-backward of the energy)
    _hx = hvp_exact_chunked if N >= 256 else hvp_exact
    def Hbar(v):
        v = proj_u1perp(v)
        return proj_u1perp(_hx(n, v, h, xi, kap))
    # own T/R span (Gram-Schmidt of centered-difference translation + rotation generators)
    ax = torch.linspace(-L, L, N, device=dev); X3, Y3, Z3 = torch.meshgrid(ax, ax, ax, indexing='ij')
    dcen = [(torch.roll(n, -1, k + 1) - torch.roll(n, 1, k + 1)) / (2 * h) for k in range(3)]
    raw = [dcen[0], dcen[1], dcen[2],
           Y3 * dcen[2] - Z3 * dcen[1], Z3 * dcen[0] - X3 * dcen[2], X3 * dcen[1] - Y3 * dcen[0]]
    Q = []
    for g in raw:
        g = proj_u1perp(g)
        for q in Q: g = g - dot(g, q) * q
        Q.append(g / g.norm())
    del raw, dcen, X3, Y3, Z3; gc.collect(); torch.cuda.empty_cache()
    G_Q = np.array([[dot(a, b) for b in Q] for a in Q])
    ortho_err = float(np.abs(G_Q - np.eye(6)).max())
    u1_leak = max(abs(dot(q, g_u1)) for q in Q)
    say(f'N={Ng}: Q orthogonality max|Q^TQ - I| = {ortho_err:.2e}; max|<q,u1>| = {u1_leak:.2e}')
    def projP(v):
        v = proj_u1perp(v)
        for q in Q: v = v - dot(v, q) * q
        return v
    # own B and C
    HQ = [Hbar(q) for q in Q]
    B = np.array([[dot(Q[i], HQ[j]) for j in range(6)] for i in range(6)])
    C = [projP(hq) for hq in HQ]
    del HQ; gc.collect(); torch.cuda.empty_cache()
    # load Z; residual R = C - A Z with OWN operator (A = P Hbar P)
    dz = np.load(zf)
    Zc = [projP(torch.tensor(dz[f'z{j}'], device=dev)) for j in range(6)]
    AZ = [projP(Hbar(z)) for z in Zc]
    R = [C[j] - AZ[j] for j in range(6)]
    def b2n(cols):
        G = np.array([[dot(a, b) for b in cols] for a in cols])
        return float(max(np.linalg.eigvalsh(0.5 * (G + G.T)).max(), 0.0)) ** 0.5
    nR, nAZ, nC = b2n(R), b2n(AZ), b2n(C)
    eta_Z = nR / (nAZ + nC)
    S = B - np.array([[dot(C[i], Zc[j]) for j in range(6)] for i in range(6)])
    asym = float(np.linalg.norm(S - S.T, 2) / np.linalg.norm(S, 2))
    eig = np.linalg.eigvalsh(0.5 * (S + S.T))
    # own a_L from the certified doublet vector
    dr = np.load(reff)
    v0 = projP(torch.tensor(dr['V'][0], device=dev)); v0 = v0 / v0.norm()
    Av0 = projP(Hbar(v0)); lam0 = dot(v0, Av0); r0 = float((Av0 - lam0 * v0).norm())
    a_L = lam0 - r0
    dS_crude = nC * nR / a_L
    lmaxBS = float(np.linalg.eigvalsh(0.5 * ((B - S) + (B - S).T)).max())
    dS_cs = ((max(lmaxBS, 0.0) + dS_crude) ** 0.5) * nR / (a_L ** 0.5)
    dS = min(dS_crude, dS_cs)
    margin = float(eig.min() - dS)
    say(f'N={Ng}: eta_Z={eta_Z:.3e}  ||S-S^T||/||S||={asym:.2e}')
    say(f'N={Ng}: S eigs [phys] = {["%.5f" % x for x in eig / h**3]}')
    say(f'N={Ng}: a_L={a_L:.4e} (lam0={lam0/h**3:.5f} phys, r0={r0:.2e}); ||DeltaS||<={dS:.3e}; '
        f'margin={margin:.3e} -> {"POSITIVE" if margin > 0 else "NOT POSITIVE"}')
    verdict = bool(margin > 0 and eta_Z < 1e-6 and a_L > 0)
    say(f'N={Ng}: INERTIA VERDICT (own recompute): '
        f'{"S>0 with error-controlled margin; A>0 via certified floor (a_L>0) => Hbar|U(1)perp POSITIVE" if verdict else "NOT ESTABLISHED"}')
    out[str(Ng)] = dict(ortho_err=ortho_err, u1_leak=u1_leak, eta_Z=eta_Z, asymmetry=asym,
                        S_eigs_phys=[float(x) for x in eig / h**3], S=S.tolist(),
                        a_L=a_L, lam0_phys=lam0 / h**3, r0=r0, deltaS_bound=dS,
                        margin_raw=margin, inertia_positive=verdict)
    # compare with the solver's JSON (report only)
    if os.path.exists('noNull_schur_inertia.json'):
        sj = json.load(open('noNull_schur_inertia.json'))
        rep = sj.get('grids', {}).get(str(Ng), {}).get('reports', {}).get('1e-04')
        if rep:
            d = max(abs(np.array(rep['S_eigs_phys']) - eig / h**3))
            say(f'N={Ng}: vs solver JSON: max |S-eig diff| = {d:.2e} phys')
            out[str(Ng)]['vs_solver_Seig_maxdiff_phys'] = float(d)
    del Zc, AZ, R, C, v0, Av0; gc.collect(); torch.cuda.empty_cache()

allpos = [g for g in out.values() if isinstance(g, dict)]
final = ('FULL U(1)^perp INERTIA POSITIVE at all verified grids (independent recompute)'
         if allpos and all(g['inertia_positive'] for g in allpos)
         else 'INERTIA NOT ESTABLISHED at one or more grids — see per-grid lines')
say(f'\n== FRESH-VERIFIER VERDICT: {final} ==')
json.dump(out, open('noNull_schur_verify.json', 'w'), indent=1, default=float)
open('noNull_schur_verify_output.txt', 'w').write('\n'.join(lines) + '\n')

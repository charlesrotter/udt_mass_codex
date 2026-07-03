"""sf_d5_spotcheck.py -- D5 sanity check of the constrained second-variation operator.

NOT stage-2 results: computability + pre-named zero/soft modes only.
Backgrounds: banked rungs risefall m=3, Z=8, rho_c=1: N=0 a*=1.4813439655172531,
N=5 a*=1.4928688994263575 (cascade_stageB_rungs.json). 2 IVP shots total.

Per rung, per column (FREE / ANCHORED / FIXED), grid M in {400, 800}:
  - assemble Q (midpoint rule for the bulk integrand; boundary bilinears; alpha DOF),
    lumped trapezoid mass (alpha weight 1: CHOSE normalization, flagged);
  - n_neg, 5 eigenvalues nearest 0;
  - translation-mode Rayleigh quotient + residual (FREE/ANCHORED: expect ~0; FIXED: excluded);
  - Schur identity: n_neg(Q) == n_neg(Vblock) + n_neg(S_u)  (exact matrix identity check);
  - lambda_max(Vblock) sign (definite-reduction criterion) + n_pos(Vblock);
  - n_neg(S_u) (the finite reduced count -- sanity only);
  - homothety direction Rayleigh quotient (FREE column; scale-breaking size).
"""
import numpy as np, sys, json
sys.path.insert(0, '/home/udt-admin/udt_mass_codex')
from cell_solver_universe_T3 import shoot, make_risefall_slice, PHI_C
from scipy.linalg import eigh, eigvalsh

Z = 8.0
RUNGS = [("N=0", 1.4813439655172531), ("N=5", 1.4928688994263575)]

def Upp_risefall(a, m=3.0):
    def upp(rho):
        x = rho
        base = 2.0 * x**m * np.exp(-a*(x*x-1.0))
        # U' = base*(m/x - 2 a x); U'' = d/dx [base*(m/x-2ax)]
        f = m/x - 2*a*x
        return base*(f*f) + base*(-m/x**2 - 2*a)
    return upp

def assemble(bg, column, M):
    """bg: dict with arrays on nodes r[0..M]: phi,phip,rho,rhop, plus scalars."""
    r = bg['r']; h = np.diff(r)
    # midpoint background values
    mid = lambda a: 0.5*(a[:-1]+a[1:])
    phi_m, phip_m, rho_m, rhop_m = (mid(bg[k]) for k in ('phi','phip','rho','rhop'))
    Upp_m = bg['Upp'](rho_m)
    A = 0.5*Z*rho_m**2
    B = -2.0*np.exp(-2*phi_m)
    C = Z*rho_m*phip_m
    D = 4.0*np.exp(-2*phi_m)*rhop_m
    E = -4.0*np.exp(-2*phi_m)*rhop_m**2
    F = 0.5*Z*phip_m**2 - 0.5*Upp_m
    n = M+1
    has_alpha = column in ('FREE','ANCHORED')
    ndof = 2*n + (1 if has_alpha else 0)   # [u(0..M), v(0..M), alpha]
    Q = np.zeros((ndof, ndof))
    iu = lambda i: i; iv = lambda i: n+i; ia = 2*n
    for j in range(M):
        hj = h[j]
        # local DOFs: [u_j, u_{j+1}, v_j, v_{j+1}]
        du = np.array([-1/hj, 1/hj, 0.0, 0.0]); ub = np.array([0.5, 0.5, 0.0, 0.0])
        dv = np.array([0.0, 0.0, -1/hj, 1/hj]); vb = np.array([0.0, 0.0, 0.5, 0.5])
        loc = np.zeros((4, 4))
        for coef, x, y in ((A[j],du,du),(B[j],dv,dv),(C[j],du,vb),(C[j],vb,du),
                           (D[j],ub,dv),(D[j],dv,ub),(E[j],ub,ub),(F[j],vb,vb)):
            loc += hj*coef*np.outer(x, y)
        gidx = [iu(j), iu(j+1), iv(j), iv(j+1)]
        Q[np.ix_(gidx, gidx)] += loc
    # boundary bilinears
    L_rho_s = bg['L_rho_s']; phip_s = bg['phip_s']; Upc = bg['Up_c']
    # outer: -(L_rho_s/phip_s) u_M v_M   (beta eliminated by essential constraint)
    cM = -L_rho_s/phip_s
    Q[iu(M), iv(M)] += 0.5*cM
    Q[iv(M), iu(M)] += 0.5*cM
    if has_alpha:
        Q[ia, iv(0)] += 0.5*Upc
        Q[iv(0), ia] += 0.5*Upc
    # mass (lumped trapezoid) + alpha weight 1 (CHOSE)
    w = np.zeros(n); w[0] = h[0]/2; w[-1] = h[-1]/2; w[1:-1] = 0.5*(h[:-1]+h[1:])
    Mm = np.concatenate([w, w, [1.0]] if has_alpha else [w, w])
    Mmat = np.diag(Mm)
    # essential constraints: delete DOFs
    delete = []
    if column == 'ANCHORED': delete.append(iu(0))
    if column == 'FIXED':    delete.append(iu(M))
    keep = [i for i in range(ndof) if i not in delete]
    Q = Q[np.ix_(keep, keep)]; Mmat = Mmat[np.ix_(keep, keep)]
    return Q, Mmat, keep, dict(n=n, iu=iu, iv=iv, ia=(ia if has_alpha else None))

def analyze(bg, column, M):
    Q, Mmat, keep, idx = assemble(bg, column, M)
    asym = np.max(np.abs(Q - Q.T))
    Q = 0.5*(Q+Q.T)
    evals, evecs = eigh(Q, Mmat)
    n_neg = int((evals < 0).sum())
    near0 = evals[np.argsort(np.abs(evals))[:5]]
    out = dict(column=column, M=M, asym=float(asym), n_neg=n_neg, ndof=len(evals),
               near0=sorted(near0.tolist(), key=abs))
    # translation mode check (FREE/ANCHORED)
    n = idx['n']
    if column in ('FREE','ANCHORED'):
        full = np.zeros(2*n+1)
        full[:n] = -bg['phip']; full[n:2*n] = -bg['rhop']; full[2*n] = 1.0
        t = full[keep]
        num = t @ Q @ t; den = t @ Mmat @ t
        res = np.linalg.norm(Q @ t)/(np.linalg.norm(t)*np.linalg.norm(Q, 2))
        out['translation_RQ'] = float(num/den); out['translation_res'] = float(res)
    # Schur split: u-DOFs vs (v-DOFs + alpha)
    kept = np.array(keep)
    upos = [i for i, k in enumerate(kept) if k < n]
    vpos = [i for i, k in enumerate(kept) if k >= n]
    Quu = Q[np.ix_(upos, upos)]; Qvv = Q[np.ix_(vpos, vpos)]; Quv = Q[np.ix_(upos, vpos)]
    evV = eigvalsh(Qvv)
    n_negV = int((evV < 0).sum()); n_posV = int((evV > 0).sum())
    S_u = Quu - Quv @ np.linalg.solve(Qvv, Quv.T)
    evS = eigvalsh(S_u)
    n_negS = int((evS < 0).sum())
    out.update(n_negV=n_negV, n_posV=n_posV, lam_maxV=float(evV.max()),
               n_negS=n_negS, schur_ok=bool(n_neg == n_negV + n_negS),
               lam_minS=float(evS.min()), evS_low=sorted(evS.tolist(), key=abs)[:3])
    # homothety direction (FREE only)
    if column == 'FREE':
        full = np.zeros(2*n+1)
        full[:n] = -bg['r']*bg['phip']; full[n:2*n] = bg['rho'] - bg['r']*bg['rhop']
        full[2*n] = 0.0
        hvec = full[keep]
        out['homothety_RQ'] = float((hvec @ Q @ hvec)/(hvec @ Mmat @ hvec))
    return out

def get_bg(a, M):
    U, Up, lab = make_risefall_slice(a, m=3.0)
    o = shoot(Z, U, Up, 1.0)
    assert o['status'] == 'seal', o['status']
    r_s = o['r_s']
    r = np.linspace(0.0, r_s, M+1)
    phi, phip, rho, rhop = o['sol'].sol(r)
    # exact seal values from event
    phis, phips, rhos, rhops = o['sol'].y_events[0][0]
    Upc = Up(1.0)
    L_rho_s = Z*rhos*phips**2 - Up(rhos)
    upp = Upp_risefall(a)
    return dict(r=r, phi=phi, phip=phip, rho=rho, rhop=rhop, Upp=upp,
                phip_s=phips, L_rho_s=L_rho_s, Up_c=Upc,
                meta=dict(a=a, r_s=r_s, rho_s=rhos, rhop_s=rhops, q=o['q'],
                          H_seal=o['H_seal'], Up_c=Upc, L_rho_s=L_rho_s, phip_s=phips))

if __name__ == '__main__':
    results = {}
    for tag, a in RUNGS:
        for M in (400, 800):
            bg = get_bg(a, M)
            if M == 400:
                print(f"\n== rung {tag} a*={a}: r_s={bg['meta']['r_s']:.4f} rho_s={bg['meta']['rho_s']:.6f} "
                      f"rho'_s={bg['meta']['rhop_s']:.2e} H_seal={bg['meta']['H_seal']:.2e} "
                      f"U'(rho_c)={bg['Up_c']:.5f} L_rho(r_s)={bg['L_rho_s']:.5f}")
            for col in ('FREE','ANCHORED','FIXED'):
                res = analyze(bg, col, M)
                results[f"{tag}/{col}/M{M}"] = res
                print(f"  [{tag} {col} M={M}] ndof={res['ndof']} n_neg={res['n_neg']} "
                      f"(V:{res['n_negV']}-,{res['n_posV']}+ lamMaxV={res['lam_maxV']:.3e}) "
                      f"n_neg(S_u)={res['n_negS']} schur_ok={res['schur_ok']} asym={res['asym']:.1e}")
                print(f"      near0: {['%.3e'%x for x in res['near0']]}")
                if 'translation_RQ' in res:
                    print(f"      translation RQ={res['translation_RQ']:.3e} rel-res={res['translation_res']:.1e}")
                if 'homothety_RQ' in res:
                    print(f"      homothety RQ={res['homothety_RQ']:.4e}")
                print(f"      S_u low |ev|: {['%.3e'%x for x in res['evS_low']]} lam_min(S_u)={res['lam_minS']:.3e}")
    with open('sf_d5_out.json','w') as f: json.dump(results, f, indent=1)

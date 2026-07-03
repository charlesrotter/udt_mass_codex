"""s2_validate.py -- machinery validation BEFORE production counts.
Gates: (V1) reproduce banked pinned-convention FREE pairs: B00 -> (0,0), B05 -> (2,6);
(V2) translation-zero Rayleigh quotient O(h^2) (ratio ~4 per doubling);
(V3) block-inertia == dense-inertia (same matrix, exact);
(V4) Sturm V^ (independent construction) == dense V^ inertia;
(V5) identities (hyperbolic, Haynsworth) exact at both dense grids;
(V6) x^T Q x vs fine-quadrature continuum form (translation of the bv13 validation)."""
import numpy as np, json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from s2_core import (load_registry, get_background, dense_analysis, bigM_analysis,
                     build_blocks, blocks_to_dense, dense_indices, trans_border,
                     block_inertia, makeUfns, element_data)

reg = load_registry()
ok_all = True

def gate(name, cond, detail=""):
    global ok_all
    print(f"[{'PASS' if cond else 'FAIL'}] {name} {detail}")
    if not cond: ok_all = False

# ---- V6 continuum-form validation on B00 (before trusting anything else)
rr = reg['B00']; bg = get_background(rr)
r_s = bg['r_s']; phip_s = bg['phip_s']
U, Up, Upp = makeUfns(bg['a'], bg['m'])
beta = 0.7; alpha = 1.3
base = lambda r: np.sin(2.5*np.pi*r/r_s) + 0.3*(r/r_s)**2
corr = -phip_s*beta - base(np.array([r_s]))[0]
ufun = lambda r: base(r) + corr*(r/r_s)**2
vfun = lambda r: np.cos(1.7*np.pi*r/r_s) - 0.2*(r/r_s)
K = 400001
rq = np.linspace(0.0, r_s, K)
phi, phip, rho, rhop = bg['sol'].sol(rq)
Z = bg['Z']; em2p = np.exp(-2.0*phi)
cku = 0.5*Z*rho**2; ckv = -2.0*em2p; cc1 = 2.0*Z*rho*phip
cc2 = 8.0*em2p*rhop; cmu = -4.0*em2p*rhop**2; cmv = 0.5*Z*phip**2 - 0.5*Upp(rho)
u = ufun(rq); v = vfun(rq)
up = np.gradient(u, rq); vp = np.gradient(v, rq)
integ = cku*up**2 + ckv*vp**2 + cc1*v*up + cc2*u*vp + cmu*u**2 + cmv*v**2
ref = np.trapezoid(integ, rq) + bg['Lrho_s']*beta*vfun(np.array([r_s]))[0] \
      + Up(1.0)*alpha*vfun(np.array([0.0]))[0]
vals = []
for M in (800, 1600, 3200):
    D, E, lay, C = build_blocks(bg, M, 'FREE')
    Q, offs, sizes = blocks_to_dense(D, E, lay)
    ia, iu, ib, iv = dense_indices(lay, offs)
    rrn = np.arange(M+1)*lay['h']
    x = np.zeros(Q.shape[0])
    x[iu] = ufun(rrn[:M]); x[ib] = beta; x[iv] = vfun(rrn); x[ia] = alpha
    vals.append(float(x @ Q @ x))
drift = [abs(v-ref) for v in vals]
gate('V6 continuum-form', drift[2] < drift[0] and abs(vals[2]-ref)/abs(ref) < 5e-3,
     f"ref={ref:.8f} discrete={['%.8f'%v for v in vals]}")

# ---- V1/V3/V4/V5 on B00 and B05
banked_pairs = {'B00': (0, 0), 'B05': (2, 6)}
for tag in ('B00', 'B05'):
    rr = reg[tag]; bg = get_background(rr)
    rep_ok = True
    for k, bv in rr['banked'].items():
        rel = abs(bg[k]-bv)/abs(bv)
        rep_ok &= rel < 5e-7
    gate(f'{tag} background reproduction', rep_ok,
         f"r_s={bg['r_s']:.6f} rho_s={bg['rho_s']:.8f} q={bg['q']:.8f}")
    for M in (800, 1600):
        d = dense_analysis(bg, M, 'FREE')
        gate(f'{tag} FREE M={M} banked pair', tuple(d['pair']) == banked_pairs[tag],
             f"pair={d['pair']} (banked {banked_pairs[tag]})")
        gate(f'{tag} FREE M={M} hyperbolic identity', d['identity_hyperbolic'] is True,
             f"nneg_full={d['inertia_full_raw'][0]} nneg_qhat={d['inertia_qhat'][0]}")
        gate(f'{tag} FREE M={M} Haynsworth identity', d['identity_haynsworth'],
             f"nneg_qhat={d['inertia_qhat'][0]} = nnegV {d['inertia_V'][0]} + nnegSu {d['inertia_Su'][0]}?")
        gate(f'{tag} FREE M={M} block==dense nneg',
             d['block_nneg'] == d['inertia_full_raw'][0],
             f"block={d['block_nneg']} dense={d['inertia_full_raw'][0]} (nzero={d['inertia_full_raw'][2]})")
        gate(f'{tag} FREE M={M} Sturm==dense V^', d['V_sturm_match'],
             f"sturm={d['V_sturm']} dense={d['inertia_V']}")
        gate(f'{tag} FREE M={M} V^ tridiagonal', d['V_tridiag_maxoff'] == 0.0,
             f"maxoff={d['V_tridiag_maxoff']:.1e}")
        # deflation consistency: dense eig-identified vs bordered block
        gate(f'{tag} FREE M={M} deflation dense==bordered',
             d['inertia_full_deflated'][0] == d['block_nneg_deflated'],
             f"dense-defl={d['inertia_full_deflated'][0]} bordered={d['block_nneg_deflated']}")
    # V2: translation RQ O(h^2)
    rqs = []
    for M in (800, 1600, 3200):
        b = bigM_analysis(bg, M, 'FREE')
        rqs.append(b['translation_RQ'])
    r1 = rqs[0]/rqs[1]; r2 = rqs[1]/rqs[2]
    gate(f'{tag} translation RQ O(h^2)', 2.5 < abs(r1) < 6.0 and 2.5 < abs(r2) < 6.0,
         f"RQ={['%.3e'%x for x in rqs]} ratios={r1:.2f},{r2:.2f}")
    # other columns: identities + block==dense at M=800
    for col in ('ANCHORED', 'FIXED'):
        d = dense_analysis(bg, 800, col)
        hyp = d['identity_hyperbolic'] if col == 'ANCHORED' else True
        gate(f'{tag} {col} M=800 identities', bool(hyp) and d['identity_haynsworth'],
             f"pair={d['pair']} nneg={d['inertia_full_raw'][0]}")
        gate(f'{tag} {col} M=800 block==dense', d['block_nneg'] == d['inertia_full_raw'][0],
             f"block={d['block_nneg']} dense={d['inertia_full_raw'][0]}")
    # bigM pair vs banked (B00/B05 pairs are banked as grid-stable to 51200)
    from s2_core import rung_M
    Mr, lam, s1 = rung_M(bg)
    b1 = bigM_analysis(bg, Mr, 'FREE')
    gate(f'{tag} FREE bigM M={Mr} pair == banked',
         tuple(b1['pair']) == banked_pairs[tag],
         f"pair={b1['pair']} defl-diag={b1['translation_resolved_negative']}")

print('\nALL GATES PASS' if ok_all else '\nGATE FAILURE(S) -- do not proceed')

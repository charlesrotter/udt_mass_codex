"""sf_d5b_extra.py -- D5 addenda:
 (a) hyperbolic-pair identity: n_neg(FREE with alpha) == 1 + n_neg(FREE, alpha dropped, v(0)=0)
     [exact linear-algebra identity; numeric confirmation at both rungs, M=400]
 (b) N=5 rung at M=1600 (resolution drift check for the finite invariants)
No new shots: reuse the same two backgrounds (2 re-shoots, same as sf_d5; total stays <= 4).
"""
import numpy as np, sys
sys.path.insert(0, '/tmp/claude-1000/-home-udt-admin-udt-mass-codex/749e82df-e440-4596-af14-d52dfbde5fed/scratchpad')
sys.path.insert(0, '/home/udt-admin/udt_mass_codex')
from sf_d5_spotcheck import get_bg, assemble, analyze, RUNGS
from scipy.linalg import eigvalsh
import numpy as np

for tag, a in RUNGS:
    bg = get_bg(a, 400)
    Q, Mm, keep, idx = assemble(bg, 'FREE', 400)
    Q = 0.5*(Q+Q.T)
    ev = eigvalsh(Q, Mm); n_neg_ext = int((ev < 0).sum())
    # drop alpha (last dof), impose v(0)=0 (dof index n = 401 in v-block start)
    n = idx['n']
    keep2 = [i for i in range(2*n) if i != n]          # remove v_0; alpha excluded by range
    Q2 = Q[np.ix_(keep2, keep2)]; M2 = Mm[np.ix_(keep2, keep2)]
    ev2 = eigvalsh(Q2, M2); n_neg_red = int((ev2 < 0).sum())
    print(f"[{tag} M=400] n_neg(ext)={n_neg_ext}  1+n_neg(red)={1+n_neg_red}  "
          f"identity_ok={n_neg_ext == 1+n_neg_red}")

# (b) N=5 at M=1600
tag, a = RUNGS[1]
bg = get_bg(a, 1600)
for col in ('FREE', 'FIXED'):
    res = analyze(bg, col, 1600)
    print(f"[{tag} {col} M=1600] ndof={res['ndof']} n_neg={res['n_neg']} "
          f"(V:{res['n_negV']}-,{res['n_posV']}+ lamMaxV={res['lam_maxV']:.3e}) "
          f"n_neg(S_u)={res['n_negS']} schur_ok={res['schur_ok']}")
    print(f"    near0: {['%.3e'%x for x in res['near0']]}")
    if 'translation_RQ' in res:
        print(f"    translation RQ={res['translation_RQ']:.3e}")
    print(f"    lam_min(S_u)={res['lam_minS']:.3e}")

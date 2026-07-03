"""T1 (Richardson, FREE deflated+undeflated soft eig at M0, 2M0, 4M0[, 8M0])
 + T4 (same in ANCHORED). Checkpointed per (rung, grid, column).
usage: python3 s3_t1_t4.py <tag> <mult> <col>   e.g. s3_t1_t4.py B00 2 FREE
"""
import numpy as np, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from s3_lib import SCR, TAGS, load_bg, build, mass_vec, near0_eigs, deflated_near0, \
    anchored_indices, wdot, wnorm
from scipy import sparse

M0 = dict(B00=6348, SM2=5963, SZ1=6835)

tag, mult, col = sys.argv[1], int(sys.argv[2]), sys.argv[3]
Mg = M0[tag]*mult
ck = os.path.join(SCR, f's3_t1_{tag}_{col}_M{Mg}.json')
if os.path.exists(ck):
    print('checkpoint exists:', ck); sys.exit(0)

t0 = time.time()
bg = load_bg(tag)
Q, ix, t = build(bg, Mg)
mass = mass_vec(ix)

if col == 'ANCHORED':
    ai = anchored_indices(ix)
    Qc = Q[np.ix_(ai, ai)].tocsc()
    mc = mass[ai]; tc = t[ai]
    # translation satisfies u(0) = -phi'(0) = 0 exactly -> it lives in the anchored space
    u0_val = float(t[ix['iu'][0]])
else:
    Qc, mc, tc = Q, mass, t
    u0_val = None

wU, VU = near0_eigs(Qc, mc, k=10)
# identify translation in the undeflated cluster by overlap
ovl = np.array([abs(wdot(VU[:, j], tc, mc))/(wnorm(VU[:, j], mc)*wnorm(tc, mc))
                for j in range(VU.shape[1])])
jt = int(np.argmax(ovl))
rest = [j for j in range(len(wU)) if j != jt]
wD, VD, diag = deflated_near0(Qc, mc, tc, k=8)

out = dict(tag=tag, col=col, M=Mg, h=float(ix['h']),
           undeflated_near0=[float(x) for x in wU],
           undeflated_t_overlap=[float(x) for x in ovl],
           transl_eig=float(wU[jt]), transl_overlap=float(ovl[jt]),
           smallest_nontransl_undeflated=float(wU[rest[0]]),
           deflated_near0=[float(x) for x in wD],
           deflated_t_content_max=float(max(diag['t_content'])),
           soft_eig_deflated=float(wD[0]),
           wall_s=round(time.time()-t0, 1))
if u0_val is not None:
    out['translation_u0'] = u0_val
# save deflated soft eigenvector at 2M0 for T2/T3/T5
if mult == 2:
    np.savez_compressed(os.path.join(SCR, f's3_softvec_{tag}_{col}_M{Mg}.npz'),
                        vec=VD[:, 0], eig=wD[0],
                        vecs=VD[:, :4], eigs=wD[:4])
json.dump(out, open(ck, 'w'), indent=1)
print(json.dumps({k: out[k] for k in ('tag', 'col', 'M', 'soft_eig_deflated',
                                      'smallest_nontransl_undeflated', 'transl_eig', 'wall_s')}))

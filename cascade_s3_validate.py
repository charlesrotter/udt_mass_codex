"""s3 V-phase: harness validation before any T-measurement.
V1: cached s2 pickle seal scalars vs bv14_bg_*.json (independent shot) — rel agreement.
V2: my regenerated-array assembly reproduces banked bv14 near0 eigs at M (per rung).
V3: bordered/Sherman-Morrison deflation vs dense exact-projection deflation at M=800.
"""
import numpy as np, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from s3_lib import SCR, TAGS, load_bg, build, mass_vec, near0_eigs, deflated_near0
from scipy.linalg import eigh

out = {}
for tag, row in TAGS.items():
    bg = load_bg(tag)
    ref = json.load(open(os.path.join(SCR, f'bv14_bg_{row}.json')))
    v1 = {k: dict(pkl=float(bg[k]), bv14=float(ref[k]),
                  rel=float(abs(bg[k]-ref[k])/max(abs(ref[k]), 1e-30)))
          for k in ('r_s', 'rho_s', 'q', 'phip_s', 'Lrho_s')}
    out[tag] = dict(V1=v1, M0=ref['M'])
    print(f'[{tag}] V1 rel: ' + ' '.join(f"{k}={v['rel']:.2e}" for k, v in v1.items()), flush=True)

for tag in TAGS:
    bg = load_bg(tag)
    M0 = out[tag]['M0']
    Q, ix, t = build(bg, M0)
    mass = mass_vec(ix)
    w, V = near0_eigs(Q, mass, k=8)
    banked = json.load(open(os.path.join(SCR, f'bv14_counts_{TAGS[tag]}.json')))
    bk = banked['grids'][str(M0)]['near0_eigs'][:8]
    out[tag]['V2'] = dict(mine=[float(x) for x in w], banked_sorted=sorted(bk, key=abs)[:8])
    print(f'[{tag}] V2 near0 mine  : ' + ' '.join(f'{x:+.4e}' for x in w))
    print(f'[{tag}] V2 near0 banked: ' + ' '.join(f'{x:+.4e}' for x in sorted(bk, key=abs)[:8]), flush=True)

# V3: dense exact projection vs Sherman-Morrison bordered, M=800, all rungs
for tag in TAGS:
    bg = load_bg(tag)
    Q, ix, t = build(bg, 800)
    mass = mass_vec(ix)
    wd, Vd, diag = deflated_near0(Q, mass, t, k=6)
    # dense reference: project onto W-orthogonal complement of t
    Qd = Q.toarray()
    n = Q.shape[0]
    Wt = mass*t
    # Householder basis of {x: (Wt)^T x = 0}... constraint is t^T W x = 0 -> normal vector Wt
    c = Wt/np.linalg.norm(Wt)
    wv = c.copy(); wv[0] += np.sign(c[0] if c[0] != 0 else 1.0)
    wv /= np.linalg.norm(wv)
    H = np.eye(n) - 2.0*np.outer(wv, wv)
    P = H[:, 1:]
    Qp = P.T @ Qd @ P
    Wp = P.T @ (mass[:, None]*P)
    wall = eigh(Qp, Wp, eigvals_only=True)
    near = sorted([float(x) for x in wall], key=abs)[:6]
    out[tag]['V3'] = dict(sherman=[float(x) for x in wd], dense=near,
                          t_content=diag['t_content'])
    print(f'[{tag}] V3 SM    : ' + ' '.join(f'{x:+.4e}' for x in wd))
    print(f'[{tag}] V3 dense : ' + ' '.join(f'{x:+.4e}' for x in near))
    print(f"[{tag}] V3 t-content of deflated vecs: max={max(diag['t_content']):.2e}", flush=True)

json.dump(out, open(os.path.join(SCR, 's3_validate.json'), 'w'), indent=1)
print('saved s3_validate.json')

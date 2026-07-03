"""T2 (mode anatomy) + T3 (overlaps with candidate directions) + direction RQs (feeds T6).
Deflated negative-branch eigenvector recomputed at the requested grid; candidates built from
Jacobi integrations (linear ODEs off the cached dense background — ledgered, not shots).
usage: python3 s3_t2_t3.py <tag> <mult>
"""
import numpy as np, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from s3_lib import SCR, TAGS, load_bg, build, mass_vec, deflated_near0, dir_homothety, \
    integrate_jacobi, dir_from_fields, wdot, wnorm, overlap

M0 = dict(B00=6348, SM2=5963, SZ1=6835)
tag, mult = sys.argv[1], int(sys.argv[2])
Mg = M0[tag]*mult
ck = os.path.join(SCR, f's3_t23_{tag}_M{Mg}.json')

bg = load_bg(tag)
Q, ix, t = build(bg, Mg)
mass = mass_vec(ix)
h = ix['h']
rn = np.arange(Mg+1)*h

# ---- deflated negative branch eigenpair
wD, VD, diag = deflated_near0(Q, mass, t, k=8)
neg = [j for j in range(len(wD)) if wD[j] < 0]
assert len(neg) == 1, f'negative-branch ambiguity: {wD[neg]}'
jn = neg[0]
lam = float(wD[jn]); x = VD[:, jn]
x = x/wnorm(x, mass)

# ---- Jacobi integrations (ledgered)
ledger = []
Yc = integrate_jacobi(bg, 'phic', ledger=ledger)
Ya = integrate_jacobi(bg, 'a', ledger=ledger)
r_s = bg['r_s']
Yc_n = Yc.sol(rn); Ya_n = Ya.sol(rn)   # rows: u, u', v, v'
Yc_s = Yc.sol(r_s); Ya_s = Ya.sol(r_s)
phip_s = bg['phip_s']
rhopp_s = -bg['Lrho_s']/4.0            # Lrho_s = -4 rho''(r_s), EOM-exact

# ---- candidate directions on the grid
# C5 shooting: Y_phic with beta from the essential fold constraint
beta_sh = -float(Yc_s[0])/phip_s
d_shoot = dir_from_fields(ix, Yc_n[0], Yc_n[2], alpha=0.0, beta=beta_sh)
# v(r_s)-NBC residual of the shooting direction (banked-hazard cross-check):
# deltaH(r_s) = q u'(r_s) + (Z rho_s phip_s^2 + U'(rho_s)) v(r_s) [auto-satisfied];
# the NBC it fails is the v(r_s) natural BC of the operator — report Q-residual instead below.

# C3 manifold tangent: null space of the 2x3 linearized seal-pair system
#   u(r_s) + phip_s*beta = 0  (phi(seal)=0 held)
#   v'(r_s) + rhopp_s*beta = 0 (rho'(seal)=0 held)
A23 = np.array([[float(Ya_s[0]), float(Yc_s[0]), phip_s],
                [float(Ya_s[3]), float(Yc_s[3]), rhopp_s]])
_, sv, Vt = np.linalg.svd(A23)
null = Vt[-1]                     # (da, dphic, beta)
da, dphic, beta_tan = [float(v) for v in null]
u_tan = da*Ya_n[0] + dphic*Yc_n[0]
v_tan = da*Ya_n[2] + dphic*Yc_n[2]
d_tan = dir_from_fields(ix, u_tan, v_tan, alpha=0.0, beta=beta_tan)
# residual of the 2x3 solve (conditioning)
res23 = np.linalg.norm(A23 @ null)/np.linalg.norm(A23)

# C4 homothety
d_hom = dir_homothety(bg, ix)

def pack(d):
    nrm = wnorm(d, mass)
    rq = wdot(d, Q @ d, mass*0 + 1)/ (nrm*nrm)  # d^T Q d / d^T W d  (Q apply plain)
    return nrm, float(d @ (Q @ d))/(nrm*nrm)

out = dict(tag=tag, M=Mg, lam_neg_branch=lam,
           deflated_cluster=[float(v) for v in wD],
           t_content_max=float(max(diag['t_content'])),
           jacobi_ledger=ledger,
           jacobi_growth=dict(Yc_seal=[float(v) for v in Yc_s], Ya_seal=[float(v) for v in Ya_s]),
           tangent=dict(da=da, dphic=dphic, beta=beta_tan, sv=[float(v) for v in sv],
                        res23=float(res23)),
           shooting=dict(beta=beta_sh, u_rs=float(Yc_s[0]), v_rs=float(Yc_s[2])))

# ---- T2 anatomy of x
iu, ib, iv, ia = ix['iu'], ix['ib'], ix['iv'], ix['ia']
mu = mass[iu]; mv = mass[iv]
u_part = x[iu]; v_part = x[iv]
alpha = float(x[ia]); beta = float(x[ib])
nu2 = float(np.sum(mu*u_part**2)); nv2 = float(np.sum(mv*v_part**2))
tot = nu2 + nv2 + alpha**2 + beta**2
thirds_u = [float(np.sum((mu*u_part**2)[(rn[:Mg] >= a*r_s/3) & (rn[:Mg] < (a+1)*r_s/3)]))/tot
            for a in range(3)]
thirds_v = [float(np.sum((mv*v_part**2)[(rn >= a*r_s/3) & (rn < (a+1)*r_s/3 + (1e-9 if a == 2 else 0))]))/tot
            for a in range(3)]
out['anatomy'] = dict(lam=lam, alpha=alpha, beta=beta,
                      frac_u=nu2/tot, frac_v=nv2/tot,
                      frac_alpha=alpha**2/tot, frac_beta=beta**2/tot,
                      u_thirds=thirds_u, v_thirds=thirds_v,
                      u0=float(u_part[0]), v0=float(v_part[0]),
                      u_rs_over_beta=float(-phip_s*beta) if beta else None)

# ---- T3 overlaps + RQs
dirs = dict(tangent=d_tan, homothety=d_hom, shooting=d_shoot, translation=t)
ovl = {}; rqs = {}
for k, d in dirs.items():
    ovl[k] = float(abs(overlap(x, d, mass)))
    nrm2 = wdot(d, d, mass)
    rqs[k] = float(d @ (Q @ d))/nrm2
# pairwise direction overlaps (context)
keys = list(dirs)
pair = {f'{a}|{b}': float(abs(overlap(dirs[a], dirs[b], mass)))
        for i, a in enumerate(keys) for b in keys[i+1:]}
out['overlaps_softmode'] = ovl
out['dir_RQ'] = rqs
out['dir_pairwise_overlap'] = pair
# tangent fixed-U-shadow bookkeeping: da relative to the W-norm of the fixed-U part
nrm_tan = wnorm(d_tan, mass)
out['tangent']['da_over_shadow_norm'] = float(abs(da)/nrm_tan)
out['tangent']['dphic_over_shadow_norm'] = float(abs(dphic)/nrm_tan)
out['tangent']['u0_over_norm'] = float(abs(d_tan[iu[0]])/nrm_tan)

json.dump(out, open(ck, 'w'), indent=1)
print(json.dumps(dict(tag=tag, M=Mg, lam=lam, overlaps=ovl, RQ=rqs,
                      anatomy={k: out['anatomy'][k] for k in
                               ('frac_u', 'frac_v', 'frac_alpha', 'frac_beta')},
                      tangent=out['tangent']), indent=1))

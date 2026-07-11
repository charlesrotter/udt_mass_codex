"""Branch-following stability test at 256^3 (per Charles 2026-07-11).

Takes the M-normalized lowest negative eigenvector v (stability_lowmode_256.npz) and the best-relaxed
carrier n0 (controlled_best_field.npz). Builds branches n_pm = normalize(n0 +- eps v) at several
controlled relative-L2 displacements delta and BOTH signs, plus a delta=0 control. Relaxes each branch
with a STRONG constraint-respecting optimizer -- Riemannian L-BFGS (memory m=6, vector transport by
projection) + backtracking Armijo line search, FIXED asymptotic boundary (pin n_inf, 2 layers), and
NO Derrick rescaling anywhere (criticality stage is rescale-off). Follows the COMPLETE trajectory,
logging E, E2, E4, Q_H, ||grad E||, max energy density, a core-size proxy in grid points, max pointwise
gradient, and displacement from n0. Classifies each branch:
  (a) RETURNS to the original carrier   (Q~1, small disp, E~E0, small grad)
  (b) LOWER-energy Q=1 stationary carrier (Q~1, small grad, E<E0 by a resolved margin, disp not tiny)
  (c) lattice TOPOLOGY SLIP             (Q collapses toward 0, core pinches sub-grid, E -> vacuum)
Per-branch wall budget; resumable checkpoints. DATA-BLIND. Comparison to external FS-hopfion stability
is NOT used to grade the result (Charles) -- only recorded as context. One clean GPU process."""
import sys, os, gc, time, json, numpy as np, torch
from collections import deque
sys.path.insert(0, 'hopfion_arc_scripts_2026-07-05')
import fs_hopfion as m
import hopfion_static_mass_common as C
torch.set_default_dtype(torch.float64); dev = m.dev

N0 = np.load('controlled_best_field.npz'); n0 = torch.tensor(N0['n'], device=dev)
N = int(N0['N']); L = float(N0['L']); h = float(N0['h']); xi = float(N0['xi']); kap = float(N0['kappa'])
n0 = n0 / n0.norm(dim=0, keepdim=True)
VD = np.load('stability_lowmode_256.npz'); v = torch.tensor(VD['v'], device=dev)   # M-normalized: v^T M v=1
lam_v = float(VD['lam_phys']); rel_v = float(VD['rel_res'])
n_inf = torch.tensor([0., 0., -1.], device=dev).view(3, 1, 1, 1)

def E_of(nn): return m.energy(nn, h, xi, kap)[0]
def gE(nn):                                       # manual autograd (proven leak-free vs functorch)
    nn2 = nn.detach().clone().requires_grad_(True)
    g, = torch.autograd.grad(m.energy(nn2, h, xi, kap)[0], nn2); return g.detach()
def tang(nn, a): return a - (a * nn).sum(0, keepdim=True) * nn
def pin(nn):
    with torch.no_grad(): m.pin_boundary(nn, n_inf, 2)
    return nn / nn.norm(dim=0, keepdim=True)
def rgrad(nn): return tang(nn, gE(nn))
def Qof(nn):
    try: return float(abs(m.hopf_charge(nn, h, N, L)[0]))
    except Exception: return float('nan')
def ip(a, b): return float((a * b).sum())
def diag(nn):
    mf = C.matter_fields(nn, h, xi, kap)
    E2 = float(mf['rho2'].sum() * h**3); E4 = float(mf['rho4'].sum() * h**3)
    edens = mf['rho2'] + mf['rho4']; maxe4 = float(mf['rho4'].max())
    wgp = float((E4 / (maxe4 + 1e-30))**(1.0 / 3.0) / h)          # core-size proxy in grid points
    g = rgrad(nn); gn = float(g.norm()); maxg = float(g.abs().max())
    disp = float((nn - n0).norm() / n0.norm())
    return dict(E=E2 + E4, E2=E2, E4=E4, Q=Qof(nn), gn=gn, maxe4=maxe4, wgp=wgp, maxg=maxg, disp=disp)

LOG = 'scratchpad/stability_branch_follow_256.log'
def logline(s):
    with open(LOG, 'a') as f: f.write(s + '\n')
    print(s, flush=True)

# --- Riemannian L-BFGS with backtracking Armijo; fixed boundary; NO rescaling ---
def lbfgs_branch(n_start, tag, budget_s, maxit=6000):
    n = pin(n_start.clone()); hist = deque(maxlen=6); g = rgrad(n); E = float(E_of(n))
    d0 = diag(n); E0c = d_ref['E']
    logline(f"[{tag}] start E={d0['E']:.5f}(dE0={d0['E']-E0c:+.5f}) Q={d0['Q']:.4f} gn={d0['gn']:.4e} "
            f"maxe4={d0['maxe4']:.3f} wgp={d0['wgp']:.2f} disp={d0['disp']:.4e}")
    traj = [dict(it=0, t=0.0, **d0)]; t0 = time.time(); g_prev = g; n_prev = n.clone()
    best = dict(gn=d0['gn'], n=n.clone(), d=d0); outcome = 'budget'
    for it in range(1, maxit + 1):
        # two-loop recursion (transport history to current tangent by projection)
        q = g.clone(); alphas = []
        H = [(tang(n, s), tang(n, y)) for (s, y) in hist]
        rhos = [1.0 / ip(y, s) for (s, y) in H if ip(y, s) > 1e-12]
        Huse = [(s, y) for (s, y) in H if ip(y, s) > 1e-12]
        for (s, y), rho in zip(reversed(Huse), reversed(rhos)):
            a = rho * ip(s, q); alphas.append(a); q = q - a * y
        gamma = (ip(Huse[-1][0], Huse[-1][1]) / ip(Huse[-1][1], Huse[-1][1])) if Huse else None
        r = (gamma * q) if gamma else q
        for (s, y), rho, a in zip(Huse, rhos, reversed(alphas)):
            b = rho * ip(y, r); r = r + (a - b) * s
        dvec = tang(n, -r)
        if ip(g, dvec) >= -1e-14 * (g.norm() * dvec.norm() + 1e-30):    # not a descent dir -> steepest
            dvec = -g; hist.clear()
        # backtracking Armijo line search (retraction = pin(normalize(n + a d))), NO rescaling
        slope = ip(g, dvec); a = 1.0 if hist else min(1.0, 1.0 / (g.norm() + 1e-30))
        E_new = None
        for _ in range(30):
            n_try = pin(n + a * dvec); E_try = float(E_of(n_try))
            if E_try <= E + 1e-4 * a * slope:
                E_new = E_try; break
            a *= 0.5
        if E_new is None:                                              # line search failed
            if hist: hist.clear(); continue                           # reset memory, retry steepest
            outcome = 'stuck'; break
        n_new = n_try; g_new = rgrad(n_new)
        s = tang(n_new, a * dvec); y = g_new - tang(n_new, g)
        if ip(s, y) > 1e-12: hist.append((s.clone(), y.clone()))
        n_prev = n; g_prev = g; n = n_new; g = g_new; E = E_new
        if it % 10 == 0:
            gc.collect()
            if dev == 'cuda': torch.cuda.empty_cache()
        if it % 25 == 0 or it == 1:
            dd = diag(n); dd['E'] = E
            traj.append(dict(it=it, t=time.time() - t0, **dd))
            logline(f"[{tag}] it={it} t={time.time()-t0:.0f}s E={E:.5f}(dE0={E-E0c:+.5f}) Q={dd['Q']:.4f} "
                    f"gn={dd['gn']:.4e} maxe4={dd['maxe4']:.3f} wgp={dd['wgp']:.2f} disp={dd['disp']:.4e}")
            if dd['gn'] < best['gn'] and dd['Q'] > 0.9: best = dict(gn=dd['gn'], n=n.clone(), d=dd)
            if dd['gn'] < 1e-3: outcome = 'converged'; break
            if dd['Q'] < 0.2: outcome = 'topology_slip'; break
            if time.time() - t0 > budget_s: outcome = 'budget'; break
    df = diag(n); df['E'] = float(E_of(n))
    # classification
    slip_seen = any(t['Q'] < 0.5 for t in traj) or df['Q'] < 0.5
    min_wgp = min(t['wgp'] for t in traj + [df]); max_maxe4 = max(t['maxe4'] for t in traj + [df])
    if slip_seen or df['Q'] < 0.5:
        cls = 'topology_slip'
    elif df['Q'] > 0.9 and df['gn'] < 5e-3 and df['E'] < d_ref['E'] - 5e-3 and df['disp'] > 5e-3:
        cls = 'lower_energy_Q1_carrier'
    elif df['Q'] > 0.9 and df['gn'] < 5e-2 and abs(df['E'] - d_ref['E']) < 5e-3:
        cls = 'returns_to_original'
    else:
        cls = f'unsettled({outcome})'
    logline(f"[{tag}] END outcome={outcome} class={cls} E={df['E']:.5f}(dE0={df['E']-E0c:+.5f}) "
            f"Q={df['Q']:.4f} gn={df['gn']:.4e} disp={df['disp']:.4e} min_wgp={min_wgp:.2f} "
            f"max_maxe4={max_maxe4:.3f} iters={it}")
    with torch.no_grad():
        np.savez(f'stability_branch_{tag}.npz', n=(n / n.norm(dim=0, keepdim=True)).cpu().numpy(),
                 N=N, L=L, h=h, xi=xi, kappa=kap)
    return dict(tag=tag, outcome=outcome, cls=cls, final=df, min_wgp=min_wgp, max_maxe4=max_maxe4,
                iters=it, traj=traj, E0=E0c)

open(LOG, 'w').close()
d_ref = diag(n0); E0c = d_ref['E']
logline(f"# n0={('controlled_best_field.npz')} N={N} L={L} h={h:.5f} E0={E0c:.5f} E2={d_ref['E2']:.3f} "
        f"E4={d_ref['E4']:.3f} Q0={d_ref['Q']:.4f} gn0={d_ref['gn']:.4e} maxe4_0={d_ref['maxe4']:.3f} "
        f"wgp0={d_ref['wgp']:.2f}")
logline(f"# eigenvector v: lam_phys={lam_v:.3e} rel_res={rel_v:.2e} (M-normalized v^T M v=1)")

# relative-L2 displacement delta -> eps: ||eps v|| = delta ||n0||  =>  eps = delta ||n0|| / ||v||
n0norm = float(n0.norm()); vnorm = float(v.norm())
BUDGET_S = float(os.environ.get('BRANCH_BUDGET_S', '1500'))       # per-branch wall budget (default 25 min)
branches = [('control', 0.0, +1)]
for delta in (0.05, 0.10, 0.20):
    branches += [(f'p{int(delta*100):02d}', delta, +1), (f'm{int(delta*100):02d}', delta, -1)]

results = []
for tag, delta, sgn in branches:
    ckpt = f'stability_branch_{tag}.npz'
    if os.path.exists(ckpt) and os.environ.get('RESUME', '0') == '1':
        logline(f"[{tag}] SKIP (checkpoint exists, RESUME=1)"); continue
    eps = delta * n0norm / (vnorm + 1e-30)
    n_start = pin(n0 + sgn * eps * v) if delta > 0 else n0.clone()
    res = lbfgs_branch(n_start, tag, BUDGET_S)
    results.append({k: res[k] for k in ('tag', 'outcome', 'cls', 'min_wgp', 'max_maxe4', 'iters', 'E0')} |
                   {'final': res['final'], 'delta': delta, 'sign': sgn})
    json.dump(results, open('stability_branch_follow_256_out.json', 'w'), indent=1)   # incremental
    if dev == 'cuda': torch.cuda.empty_cache()

logline("# ALL BRANCHES DONE")
for r in results:
    f = r['final']
    logline(f"  {r['tag']:8s} delta={r['delta']:.2f} sign={r['sign']:+d}  class={r['cls']:24s} "
            f"dE0={f['E']-r['E0']:+.5f} Q={f['Q']:.3f} gn={f['gn']:.3e} disp={f['disp']:.3e} "
            f"min_wgp={r['min_wgp']:.2f} max_maxe4={r['max_maxe4']:.2f}")
json.dump(results, open('stability_branch_follow_256_out.json', 'w'), indent=1)

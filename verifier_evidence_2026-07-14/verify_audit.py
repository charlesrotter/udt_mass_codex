# BLIND VERIFIER — independent criticality + eigenpair audit.
# Own implementation; uses ONLY energy_noNull/grad_noNull from noNull_energy.py as the black-box functional.
import os, sys, time, math
import numpy as np, torch
sys.path.insert(0, '/home/udt-admin/udt_mass_codex')
from noNull_energy import energy_noNull, grad_noNull

torch.set_default_dtype(torch.float64)
dev = 'cuda'
GRID = os.environ.get('GRID', '128')   # '128','192','256'
SEED_FILE = os.environ.get('SEEDF', '0')

root = '/home/udt-admin/udt_mass_codex/'
field_file = {'128': 'noNull_critical_field_128.npz',
              '192': 'noNull_critical_field_192.npz',
              '256': 'noNull_critical_field.npz'}[GRID]
ref_file = {'128': f'noNull_hess_refine_s128_{SEED_FILE}.npz',
            '192': f'noNull_hess_refine_s192_{SEED_FILE}.npz',
            '256': f'noNull_hess_refine_s{SEED_FILE}.npz'}[GRID]

d = np.load(root + field_file)
N = int(d['N']); L = float(d['L']); h = float(d['h']); xi = float(d['xi']); kap = float(d['kappa'])
print(f"=== GRID {GRID}: N={N} L={L} h={h:.10f} xi={xi} kap={kap}  refine={ref_file}", flush=True)
print(f"h check: 2L/(N-1)={2*L/(N-1):.10f}  (match={abs(h-2*L/(N-1))<1e-12})")
n = torch.tensor(d['n'], device=dev)
print(f"field unit-norm check: max | |n|-1 | = {float((n.norm(dim=0)-1).abs().max()):.3e}")
# boundary constancy check (outer 2 layers should be pinned)
b = n[:, :2, :, :].reshape(3, -1)
print(f"outer-layer values (x-slab 0:2): mean={b.mean(1).cpu().numpy()}, std={b.std(1).max():.3e}")

# --- my own projections ---
W = 2
msk = torch.zeros(N, N, N, device=dev); msk[W:-W, W:-W, W:-W] = 1.0
def P(v):  # tangent + free
    return (v - (v * n).sum(0, keepdim=True) * n) * msk
def ipf(a, b): return float((a * b).sum())
def gE(x): return grad_noNull(x, h, xi, kap)

t0 = time.time()
E = float(energy_noNull(n, h, xi, kap)[0])
g = gE(n)
g_f = P(g)
ng_f = float(g_f.norm()); ng = float(g.norm())
nfree = 3 * (N - 2 * W) ** 3
print(f"E = {E:.6f}")
print(f"||grad|| (raw euclid) = {ng:.6e}   ||P_free P_tan grad|| = {ng_f:.6e}   RMS/freeDOF = {ng_f/math.sqrt(nfree):.3e}")

# relative scale: force response to a unit-norm random tangent perturbation
torch.manual_seed(12345)
t = P(torch.randn(3, N, N, N, device=dev)); t = t / t.norm()
eps = 1e-4
def hvp(v, ee=eps):
    vp = P(v)
    return P((gE(n + ee * vp) - gE(n - ee * vp)) / (2 * ee))
Ht = hvp(t)
print(f"||H t_rand_unit|| = {float(Ht.norm()):.6e}  (typical unit-displacement force);  ratio ||g_f||/||H t|| = {ng_f/float(Ht.norm()):.4e}")
lam_t = ipf(t, Ht) / h**3
print(f"RQ of random tangent (lam_phys units) = {lam_t:.4f}")
# perturbed-field gradient (finite kick, unit norm)
npert = n + 1.0 * t
npert = npert / npert.norm(dim=0, keepdim=True)
gp = P(gE(npert))
print(f"||g_f(perturbed by unit-norm kick)|| = {float(gp.norm()):.6e}   ratio ||g_f(n)||/that = {ng_f/float(gp.norm()):.4e}")
del t, Ht, npert, gp, g

# --- symmetry directions (my own build from stated definitions) ---
xg = torch.linspace(-L, L, N, device=dev)
Xg, Yg, Zg = torch.meshgrid(xg, xg, xg, indexing='ij')
dnc = [(torch.roll(n, -1, a + 1) - torch.roll(n, 1, a + 1)) / (2 * h) for a in range(3)]
u1raw = torch.stack([-n[1], n[0], torch.zeros_like(n[0])], 0)
u1 = P(u1raw); u1 = u1 / u1.norm()
trs = [dnc[0], dnc[1], dnc[2],
       Yg * dnc[2] - Zg * dnc[1], Zg * dnc[0] - Xg * dnc[2], Xg * dnc[1] - Yg * dnc[0]]
# orthonormal TR basis, u1 removed first
Q = [u1]
for v in trs:
    c = P(v); c = c - ipf(c, u1) * u1
    for q in Q[1:]: c = c - ipf(c, q) * q
    nc = float(c.norm())
    if nc > 1e-9: Q.append(c / nc)
Q_TR = Q[1:]
print(f"# symmetry basis: u1 + {len(Q_TR)} T/R orthonormal directions")
del dnc, trs, Xg, Yg, Zg, u1raw

# gradient overlap with claimed modes comes below; also with symmetry dirs:
print(f"|<g_f,u1>| = {abs(ipf(g_f,u1)):.3e}   max|<g_f,q_TR>| = {max(abs(ipf(g_f,q)) for q in Q_TR):.3e}")

# --- eigenpair audit ---
r = np.load(root + ref_file)
lam_d_file = np.array(r['lam_doublet']); lam_i_file = float(r['lam_isolated'])
print(f"file: lam_doublet={lam_d_file}, lam_isolated={lam_i_file:.10f}, eta_c={float(r['eta_c_doublet']):.3e}, r_j_iso={float(r['r_j_isolated']):.3e}")
V = r['V']  # (3 vecs, 3, N,N,N)
Hlist = []
lam_mine = []
for j in range(3):
    v = torch.tensor(V[j], device=dev)
    nv = float(v.norm())
    tangerr = float(((v * n).sum(0)).abs().max())
    outer = float((v * (1 - msk)).abs().max())
    Hv = hvp(v)
    lam_raw = ipf(v, Hv) / nv**2
    lam_phys = lam_raw / h**3
    res_raw = Hv - lam_raw * v
    r_raw = float(res_raw.norm()) / (float(Hv.norm()) + abs(lam_raw))
    # deflated residuals
    res_u1 = res_raw - ipf(res_raw, u1) * u1
    r_u1 = float(res_u1.norm()) / (float(Hv.norm()) + abs(lam_raw))
    res_tr = res_u1.clone()
    for q in Q_TR: res_tr = res_tr - ipf(res_tr, q) * q
    r_tr = float(res_tr.norm()) / (float(Hv.norm()) + abs(lam_raw))
    ov_u1 = abs(ipf(v, u1))
    ov_tr = max(abs(ipf(v, q)) for q in Q_TR)
    a_j = ipf(g_f, v)
    print(f" vec{j}: ||v||={nv:.12f} max|v.n|={tangerr:.2e} max|outer|={outer:.2e}")
    print(f"        lam_phys(mine)={lam_phys:.10f}  r_raw={r_raw:.3e} r_u1defl={r_u1:.3e} r_TRdefl={r_tr:.3e}")
    print(f"        |<v,u1>|={ov_u1:.2e} max|<v,qTR>|={ov_tr:.2e}  <g_f,v>={a_j:+.3e}", flush=True)
    lam_mine.append(lam_phys)
    if j < 2: Hlist.append(Hv.clone())
    del v, Hv, res_raw, res_u1, res_tr

# doublet mutual orthogonality + 2x2 invariant-subspace residual
v0 = torch.tensor(V[0], device=dev); v1 = torch.tensor(V[1], device=dev)
print(f"doublet <v0,v1> = {ipf(v0,v1):+.3e}")
Hm = torch.zeros(2, 2, dtype=torch.float64)
vv = [v0, v1]
for a in range(2):
    for b in range(2):
        Hm[a, b] = ipf(vv[a], Hlist[b])
HV_norm = math.sqrt(sum(float(Hv.norm())**2 for Hv in Hlist))
# residual R = HV2 - V2 (V2^T H V2)
Rn2 = 0.0; VS_n2 = 0.0
for b in range(2):
    Rb = Hlist[b] - Hm[0, b].item() * v0 - Hm[1, b].item() * v1
    Rn2 += float(Rb.norm())**2
    VS_n2 += Hm[0, b].item()**2 + Hm[1, b].item()**2
    del Rb
r2x2 = math.sqrt(Rn2) / (HV_norm + math.sqrt(VS_n2))
ew = np.linalg.eigvalsh(((Hm + Hm.T) / 2).numpy()) / h**3
print(f"2x2 subspace: eigs(sym)={ew}, asym |H01-H10|={abs(Hm[0,1]-Hm[1,0]):.2e}, invariant-residual eta = {r2x2:.3e}")
print(f"SUMMARY {GRID}: lam_mine={['%.8f'%x for x in lam_mine]} vs file d={lam_d_file} i={lam_i_file:.8f}")
print(f"time {time.time()-t0:.1f}s")

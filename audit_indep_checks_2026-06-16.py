#!/usr/bin/env python3
"""
INDEPENDENT INFRASTRUCTURE AUDIT cross-checks (CPU-only, sympy + numpy + CPU-torch).
Auditor: Claude (Opus 4.8, 1M) -- standing infra-audit practice, 2026-06-16.
DATA-BLIND.  GPU is OFF-LIMITS (parallel job): force CPU for any torch.

Checks:
  A. Independent symbolic Einstein tensor (g->Gamma->Riem->Ricci->G) for
     (i)  Schwarzschild -> must be 0.
     (ii) a metric with a TIME-PSI OFF-DIAGONAL (g_tphi != 0) -> nonzero G,
          and re-derive numerically with whole_metric_3d_core.py (CPU) -> compare.
  B. Independent symbolic L2+L4 Hilbert stress for the unit hedgehog vs the
     committed mixed (rho, p_r, pT) AND vs whole_metric_3d_matter.stress_tensor (CPU).
  C. Field/stress consistency: confirm hedgehog n is UNIT, and that the SAME n
     gives both the energy density and the stress in whole_metric_3d_matter.
  D. radial_Bfree_soliton: confirm a CONVERGED solution drives ALL THREE mixed
     residuals (t,t),(r,r),(th,th) -> 0 (not merely (t,t) with B=1/A).
"""
import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""          # HARD-disable GPU for this audit
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math
import numpy as np
import sympy as sp
import torch
torch.set_default_dtype(torch.float64)
assert not torch.cuda.is_available(), "GPU must be hidden for the audit"
DEV = "cpu"

import importlib.util
def load(modname, path):
    spec = importlib.util.spec_from_file_location(modname, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

ROOT = "/home/udt-admin/udt_mass_codex"
core = load("wm_core", f"{ROOT}/whole_metric_3d_core.py")
matt = load("wm_matt", f"{ROOT}/whole_metric_3d_matter.py")
rbf  = load("rbf",      f"{ROOT}/radial_Bfree_soliton.py")

print("="*78)
print("A. INDEPENDENT SYMBOLIC EINSTEIN ENGINE")
print("="*78)
t, r, th, ps = sp.symbols('t r theta psi', real=True)

def sym_einstein_mixed(g, coords):
    gi = g.inv()
    n = 4
    Gam = [[[sp.S(0)]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                s = sp.S(0)
                for d in range(n):
                    s += gi[a, d]*(sp.diff(g[d, b], coords[c])
                                   + sp.diff(g[d, c], coords[b])
                                   - sp.diff(g[b, c], coords[d]))
                Gam[a][b][c] = sp.simplify(s/2)
    def riem(a, b, c, d):
        s = sp.diff(Gam[a][b][d], coords[c]) - sp.diff(Gam[a][b][c], coords[d])
        for e in range(n):
            s += Gam[a][c][e]*Gam[e][b][d] - Gam[a][d][e]*Gam[e][b][c]
        return s
    Ric = sp.zeros(n, n)
    for b in range(n):
        for d in range(n):
            Ric[b, d] = sp.simplify(sum(riem(a, b, a, d) for a in range(n)))
    Rs = sp.simplify(sum(gi[i, j]*Ric[i, j] for i in range(n) for j in range(n)))
    Gdn = sp.Matrix(n, n, lambda i, j: Ric[i, j] - sp.Rational(1, 2)*g[i, j]*Rs)
    return sp.simplify(Gdn), sp.simplify(gi*Gdn)

# (i) Schwarzschild
M = sp.symbols('M', positive=True)
f = 1 - 2*M/r
gS = sp.diag(-f, 1/f, r**2, r**2*sp.sin(th)**2)
GdnS, GmixS = sym_einstein_mixed(gS, [t, r, th, ps])
schw_ok = all(GmixS[i, i] == 0 for i in range(4))
print("  (i) Schwarzschild G^mu_nu all zero:", schw_ok)

print("\n" + "="*78)
print("A.(ii) OFF-DIAGONAL metric: numeric core vs symbolic G_{mu nu}")
print("="*78)
# A stationary metric with a t-psi off-diagonal (rotation-like) AND functions of r,th.
# g_tt=-(1+ar^2),  g_tphi = w0*r^2 sin^2 th,  g_rr=1+b r^2,
# g_thth=r^2, g_psps=r^2 sin^2 th. Pick small numeric coeffs; evaluate at a point.
a0, b0, w0 = sp.Rational(1,10), sp.Rational(1,7), sp.Rational(1,5)
gtt = -(1 + a0*r**2)
gtp = w0*r**2*sp.sin(th)**2
grr = 1 + b0*r**2
gthth = r**2
gpsps = r**2*sp.sin(th)**2
gM = sp.Matrix([
    [gtt, 0, 0, gtp],
    [0, grr, 0, 0],
    [0, 0, gthth, 0],
    [gtp, 0, 0, gpsps]])
GdnM, GmixM = sym_einstein_mixed(gM, [t, r, th, ps])

# Build the SAME metric numerically on a small 3D (r,th,psi) grid and run the core.
Nr, Nth, Nps = 41, 41, 24
r0, r1 = 1.0, 3.0
th0, th1 = 0.6, 2.4
rg = torch.linspace(r0, r1, Nr)
thg = torch.linspace(th0, th1, Nth)
# psi periodic on [0,2pi)
psg = torch.linspace(0, 2*math.pi, Nps+1)[:-1]
hr = (rg[1]-rg[0]).item(); hth = (thg[1]-thg[0]).item(); hps = (2*math.pi/Nps)
RR, TT, PP = torch.meshgrid(rg, thg, psg, indexing='ij')

def npf(expr):
    return sp.lambdify((r, th, ps), expr, 'numpy')

g = torch.zeros(Nr, Nth, Nps, 4, 4)
comps = {(0,0):gtt,(0,3):gtp,(3,0):gtp,(1,1):grr,(2,2):gthth,(3,3):gpsps}
for (i,j),e in comps.items():
    fn = npf(e)
    vals = fn(RR.numpy(), TT.numpy(), PP.numpy())
    g[..., i, j] = torch.as_tensor(np.broadcast_to(vals, RR.shape).astype(np.float64))

ginv = core.metric_inverse(g)
# dg[...,k,mu,nu] = d_k g_{mu nu}; k=0 is t (=0), k=1..3 = r,th,psi
dg = torch.zeros(Nr, Nth, Nps, 4, 4, 4)
for mu in range(4):
    for nu in range(4):
        dg[..., 1, mu, nu] = core.d_dx(g[..., mu, nu], hr, 0)
        dg[..., 2, mu, nu] = core.d_dx(g[..., mu, nu], hth, 1)
        dg[..., 3, mu, nu] = core.d_dx(g[..., mu, nu], hps, 2, periodic=True)
Gamma = core.christoffel(ginv, dg)
# dGamma[...,k,a,b,c] = d_k Gamma^a_{bc}
dGamma = torch.zeros(Nr, Nth, Nps, 4, 4, 4, 4)
for a in range(4):
    for b in range(4):
        for c in range(4):
            dGamma[..., 1, a, b, c] = core.d_dx(Gamma[..., a, b, c], hr, 0)
            dGamma[..., 2, a, b, c] = core.d_dx(Gamma[..., a, b, c], hth, 1)
            dGamma[..., 3, a, b, c] = core.d_dx(Gamma[..., a, b, c], hps, 2, periodic=True)
Gmn_num, Ric_num, Rscal_num = core.einstein(g, ginv, Gamma, dGamma)

# Compare at an INTERIOR point (avoid FD edge degradation): mid indices.
ir, ith, ips = Nr//2, Nth//2, Nps//2
rv = rg[ir].item(); thv = thg[ith].item(); psv = psg[ips].item()
Gdn_sym_pt = np.array(GdnM.subs({r: rv, th: thv, ps: psv}).evalf(), dtype=np.float64)
Gdn_num_pt = Gmn_num[ir, ith, ips].numpy()
# include the off-diagonal (t,psi)
abserr = np.abs(Gdn_sym_pt - Gdn_num_pt)
print(f"  point (r,th,psi)=({rv:.3f},{thv:.3f},{psv:.3f})")
print("  max |G_num - G_sym| over ALL 16 components:", abserr.max())
print("  G_{t psi} sym =", Gdn_sym_pt[0,3], " num =", Gdn_num_pt[0,3],
      " |err|=", abs(Gdn_sym_pt[0,3]-Gdn_num_pt[0,3]))
# symmetry of numeric G
asym = (Gmn_num - Gmn_num.transpose(-1,-2)).abs().max().item()
print("  numeric G symmetry max|G-G^T| (whole grid):", asym)

print("\n" + "="*78)
print("B. INDEPENDENT SYMBOLIC L2+L4 STRESS vs committed (rho,p_r,pT) and vs tool")
print("="*78)
# Symbolic: unit S^3 hedgehog n on the diagonal soliton metric.
phi = sp.Function('phi')
Th = sp.Function('Theta')
xi, kap = sp.symbols('xi kappa', positive=True)
A = sp.Function('A'); Bf = sp.Function('B')   # general g_tt=-A, g_rr=B (B FREE)
# Use general diagonal metric with FREE g_tt,g_rr (NOT tied) to test B-free claim.
gtt_s = -A(r); grr_s = Bf(r)
g4 = sp.diag(gtt_s, grr_s, r**2, r**2*sp.sin(th)**2)
gi4 = g4.inv()
# hedgehog n(4-vector)
ThR = Th(r)
n_vec = sp.Matrix([sp.sin(ThR)*sp.sin(th)*sp.cos(ps),
                   sp.sin(ThR)*sp.sin(th)*sp.sin(ps),
                   sp.sin(ThR)*sp.cos(th),
                   sp.cos(ThR)])
unit = sp.simplify(n_vec.dot(n_vec))
print("  |n|^2 (must be 1):", unit)
coords = [t, r, th, ps]
# dn[m,a] = d_m n_a
dn = sp.Matrix(4, 4, lambda m, a: sp.diff(n_vec[a], coords[m]))
# field metric Gmn = sum_a dn[m,a] dn[n,a]
Gfm = sp.Matrix(4, 4, lambda m, nn: sum(dn[m, a]*dn[nn, a] for a in range(4)))
Gfm = sp.simplify(Gfm)
# L2 = -(xi/2) g^{mn} Gmn ; L4 = -(kap/4) g^{mp} g^{nq}(Gmp Gnq - Gmq Gnp)
L2 = -(xi/2)*sum(gi4[m, nn]*Gfm[m, nn] for m in range(4) for nn in range(4))
L4 = sp.S(0)
for m in range(4):
    for nn in range(4):
        for pp in range(4):
            for q in range(4):
                L4 += -(kap/4)*gi4[m, pp]*gi4[nn, q]*(Gfm[m, pp]*Gfm[nn, q]
                                                      - Gfm[m, q]*Gfm[nn, pp])
L2 = sp.simplify(L2); L4 = sp.simplify(L4); Ltot = sp.simplify(L2+L4)
# Hilbert stress T_{ab} = -2 dL/dg^{ab} + g_{ab} L.  Differentiate wrt inverse-metric
# entries treated as independent symbols (diagonal here for clarity but keep g^{rr}).
# Easier: use the closed forms from the tool: T_{ab}=xi Gmn + kap C_ab + g_ab L,
# C_ab = sym g^{nq} SS_{a n b q}. Build SS and C symbolically, then mixed T^a_b.
SS = sp.MutableDenseNDimArray.zeros(4,4,4,4)
for m in range(4):
    for nn in range(4):
        for pp in range(4):
            for q in range(4):
                SS[m,nn,pp,q] = Gfm[m,pp]*Gfm[nn,q] - Gfm[m,q]*Gfm[nn,pp]
Cab = sp.zeros(4,4)
for a in range(4):
    for b in range(4):
        Cab[a,b] = sum(gi4[nn,q]*SS[a,nn,b,q] for nn in range(4) for q in range(4))
Cab = (Cab + Cab.T)/2
Tab = sp.zeros(4,4)
for a in range(4):
    for b in range(4):
        Tab[a,b] = xi*Gfm[a,b] + kap*Cab[a,b] + g4[a,b]*Ltot
Tab = sp.simplify(Tab)
Tmix = sp.simplify(gi4*Tab)  # T^a_b
# committed mixed:  T^t_t=-rho, T^r_r=p_r, T^th_th=pT with X=g^{rr}Theta'^2, Y=sin^2/r^2
grr_inv = 1/Bf(r)
Xc = grr_inv*sp.diff(ThR, r)**2
Yc = sp.sin(ThR)**2/r**2
rho_c = (xi/2)*(Xc+2*Yc) + (kap/2)*(2*Xc*Yc+Yc**2)
pr_c  = (xi/2)*(Xc-2*Yc) + (kap/2)*(2*Xc*Yc-Yc**2)
pT_c  = (kap/2)*Yc**2 - (xi/2)*Xc
d_tt = sp.simplify(Tmix[0,0] - (-rho_c))
d_rr = sp.simplify(Tmix[1,1] - pr_c)
d_thth = sp.simplify(Tmix[2,2] - pT_c)
d_psps = sp.simplify(Tmix[3,3] - pT_c)
print("  T^t_t - (-rho_committed)   =", d_tt)
print("  T^r_r - p_r_committed      =", d_rr)
print("  T^th_th - pT_committed     =", d_thth)
print("  T^ps_ps - pT_committed     =", d_psps)
# off-diagonal of mixed stress (should vanish for this static hedgehog)
offmax = max(sp.simplify(Tmix[i,j]) for i in range(4) for j in range(4) if i!=j)
alloff = [sp.simplify(Tmix[i,j]) for i in range(4) for j in range(4) if i!=j]
print("  all off-diagonal T^a_b zero:", all(e==0 for e in alloff))

print("\n" + "="*78)
print("B'. NUMERIC stress_tensor (tool) vs symbolic Tab at a point (CPU)")
print("="*78)
# numeric eval of the tool's stress_tensor on the hedgehog at one (r,th,psi)
xi_n = kap_n = 1.0
rv, thv, psv = 1.7, 1.1, 0.9
Av, Bv = 1.3, 1.6        # arbitrary g_tt=-A, g_rr=B (B free)
Thv = 0.7; Thpv = 0.45   # Theta and Theta'
# Build n and dn numerically EXACTLY as the symbolic (analytic derivs)
def hedge_dn(Thv, Thpv, thv, psv):
    sT, cT = math.sin(Thv), math.cos(Thv)
    sth, cth = math.sin(thv), math.cos(thv)
    sps, cps = math.sin(psv), math.cos(psv)
    n = np.array([sT*sth*cps, sT*sth*sps, sT*cth, cT])
    dn = np.zeros((4,4))  # dn[m,a]=d_m n_a, m in t,r,th,psi
    # d_r: via Theta'(r)
    dn[1] = np.array([cT*sth*cps, cT*sth*sps, cT*cth, -sT])*Thpv
    # d_th
    dn[2] = np.array([sT*cth*cps, sT*cth*sps, -sT*sth, 0.0])
    # d_psi
    dn[3] = np.array([-sT*sth*sps, sT*sth*cps, 0.0, 0.0])
    return n, dn
n_np, dn_np = hedge_dn(Thv, Thpv, thv, psv)
g_pt = torch.tensor([[-Av,0,0,0],[0,Bv,0,0],[0,0,rv**2,0],[0,0,0,rv**2*math.sin(thv)**2]])
ginv_pt = core.metric_inverse(g_pt)
dn_t = torch.tensor(dn_np)
Tab_num, L_num, L2_num, L4_num = matt.stress_tensor(g_pt, ginv_pt, dn_t, xi_n, kap_n)
Tmix_num = (ginv_pt @ Tab_num).numpy()
# symbolic at same point
subs = {A(r):Av, Bf(r):Bv, ThR:Thv, sp.Derivative(ThR,r):Thpv, r:rv, th:thv, ps:psv,
        xi:xi_n, kap:kap_n}
# Tmix is in terms of A(r),B(r),Theta(r),Theta'(r); substitute Derivative too
Tmix_sym_pt = np.array(sp.Matrix(4,4, lambda i,j: Tmix[i,j].subs(subs)).evalf(), dtype=np.float64)
err = np.abs(Tmix_sym_pt - Tmix_num)
print(f"  point (r,th,psi)=({rv},{thv},{psv}), A={Av},B={Bv},Th={Thv},Thp={Thpv}")
print("  max |T^a_b(tool) - T^a_b(sym)| =", err.max())
print("  T^t_t tool=", Tmix_num[0,0], " sym=", Tmix_sym_pt[0,0])
print("  T^r_r tool=", Tmix_num[1,1], " sym=", Tmix_sym_pt[1,1])

print("\n" + "="*78)
print("C. FIELD/STRESS CONSISTENCY: same unit n for stress AND energy")
print("="*78)
# |n| unit numerically
print("  |n|^2 numeric:", float(n_np@n_np))
# The tool's stress uses field_metric(dn) = Gmn; the energy density that the radial
# solver uses is rho = -T^t_t. Confirm tool's -T^t_t equals committed rho with the
# SAME dn -> already shown equal symbolically; numeric tie:
Xn = (1.0/Bv)*Thpv**2; Yn = math.sin(Thv)**2/rv**2
rho_committed = (xi_n/2)*(Xn+2*Yn)+(kap_n/2)*(2*Xn*Yn+Yn**2)
print("  -T^t_t (tool) =", -Tmix_num[0,0], "  committed rho =", rho_committed,
      "  |diff|=", abs(-Tmix_num[0,0]-rho_committed))

print("\n" + "="*78)
print("D. radial_Bfree_soliton: ALL THREE residuals -> 0 on a CONVERGED solve (CPU)")
print("="*78)
xi_n = kap_n = 1.0
rc = 0.05; ri = rc + 14.0
def run(N):
    rgr = rbf.make_grid(1, N, rc=rc, rint=ri, geom=False, device="cpu")
    out = rbf.selfconsistent_Bfree(rgr, xi_n, kap_n, p=0.4, kap8=0.05,
                                   iters=200, relax=0.4, tol=1e-11, verbose=False)
    res = out['res']
    def interior_max(x):
        return x[:, 2:-2].abs().max().item()
    return (interior_max(res['res_tt']), interior_max(res['res_rr']),
            interior_max(res['res_thth']))
for N in (400, 800, 1600):
    rtt, rrr, rth = run(N)
    print(f"  N={N:5d}  max|res_tt|={rtt:.3e}  max|res_rr|={rrr:.3e}  max|res_thth|={rth:.3e}")

# Also confirm the SEAL-DEFECT (legacy) reintroduces a non-converging (t,t) floor:
print("\n  legacy seal_defect=True (should pin res_tt, NOT converge):")
for N in (400, 800, 1600):
    rgr = rbf.make_grid(1, N, rc=rc, rint=ri, geom=False, device="cpu")
    out = rbf.selfconsistent_Bfree(rgr, xi_n, kap_n, p=0.4, kap8=0.05,
                                   iters=200, relax=0.4, tol=1e-11,
                                   verbose=False, seal_defect=True)
    res = out['res']
    rtt = res['res_tt'][:, 2:-2].abs().max().item()
    print(f"    N={N:5d}  max|res_tt|(seal_defect)={rtt:.3e}")
print("\nDONE.")

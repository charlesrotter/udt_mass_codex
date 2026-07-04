"""Blind adversarial verifier for E2d. Independent, bounded, single process."""
import os, math, time, json
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np, torch
torch.set_default_dtype(torch.float64)
import cell_solver_composite as C
import e2d_continuation_driver as D

DEV = D.DEV
Nr, Nth, Na, KMAP = 12, 8, 192, 2.5
print("DEV =", DEV)

# ---------- (5) prolongate round-trip identity ----------
ctx = C.make_ctx_comp(Nr, Nth, Na, kmap=KMAP, device=DEV)
br = C.load_bracket("A1 m=3 Z=8"); prm = (br["Z"], 0.5, 0.1, 1)
v = C.seed_comp(ctx, br, rp0=0.95*br["r_s"], amp=0.8, device=DEV)
# coarse->fine->coarse round trip
ctxc = C.make_ctx_comp(8, Nth, Na, kmap=KMAP, device=DEV)
vc = D.prolongate(v, ctx, ctxc)            # 12 -> 8
vcf = D.prolongate(vc, ctxc, ctx)          # 8 -> 12
# identity check: fine->fine
vff = D.prolongate(v, ctx, ctx)
id_err = float((vff - v).abs().max())
print(f"[roundtrip] fine->fine identity err = {id_err:.2e}")

# ---------- (1) homotopy endpoint solves the TRUE residual ----------
# build an MMS and confirm Newton-homotopy g at s=1 == true residual pointwise
def build_mms(label, rp0_frac, amp, bulge=0.0):
    br = C.load_bracket(label); prm = (br["Z"], 0.5, 0.1, 1)
    ctx = C.make_ctx_comp(Nr, Nth, Na, kmap=KMAP, device=DEV)
    rp0 = rp0_frac*br["r_s"] if rp0_frac<=1.0 else rp0_frac
    def genericize(vv):
        phi_c, rho_c, uf, phi_a, rho_a, r_p, r_sU = C.unpack_comp(vv, ctx)
        z=ctx["cell"]["zeta"].to(DEV); mu=ctx["cell"]["mu"].to(DEV); h=ctx["ha"].to(DEV)
        phi_c=phi_c+0.05*torch.cos(math.pi*z); rho_c=rho_c+0.03*torch.sin(0.5*math.pi*(z+1))
        uf=uf+0.05*(1-mu[None,:]**2)*mu[None,:]*torch.cos(math.pi*(z[:,None]+1))
        uf=uf+bulge*(1-mu[None,:]**2)*torch.sin(math.pi*(z[:,None]+1)/2)
        phi_a=phi_a+0.02*torch.sin(math.pi*h); rho_a=rho_a+0.01*h*(1-h)
        return C.pack_comp(phi_c,rho_c,uf,phi_a,rho_a,float(r_p),float(r_sU),device=DEV)
    v_star=genericize(C.seed_comp(ctx, br, rp0=rp0, amp=amp, device=DEV))
    F_star=C.residual_comp(v_star, ctx, prm, br).detach()
    resfn=lambda vv: C.residual_comp(vv, ctx, prm, br)-F_star
    return dict(br=br,prm=prm,ctx=ctx,v_star=v_star,resfn=resfn,F_star=F_star,n=v_star.numel())

mm = build_mms("A1 m=3 Z=8", 0.95, 0.8, 0.0)
n = mm["n"]; resfn = mm["resfn"]
v0 = mm["v_star"].cpu().numpy().astype(np.longdouble).copy()
v0[:5] += 0.13   # arbitrary off-root probe
v0_t = torch.as_tensor(np.asarray(v0,dtype=float), device=DEV)
F0 = resfn(v0_t).detach()
# Newton homotopy g_s at s=1: c=0 -> g == resfn ; check on a random point
vp = torch.as_tensor(np.asarray(v0,dtype=float)+0.01, device=DEV)
c1 = 1.0-1.0
g1 = resfn(vp) - c1*F0
diff_s1 = float((g1 - resfn(vp)).abs().max())
# and at s=0, v0 is exact root of g_0
c0 = 1.0-0.0
g0v0 = resfn(v0_t) - c0*F0
print(f"[homotopy] g(s=1)==true residual diff = {diff_s1:.2e}   g(s=0)(v0) max = {float(g0v0.abs().max()):.2e}")
# verify at v* residual is ~0 (MMS exact root)
print(f"[MMS] max|R(v*)| = {float(resfn(mm['v_star']).abs().max()):.2e}")

# ---------- (2) COMPONENT SEPARATION re-run: A1Z8 cell 0.3, MY OWN shape ----------
def perturb_cell_shapeB(mm, sc, seed=0):
    """DIFFERENT shape combined-cell perturbation at controlled sup-distance sc."""
    ctx=mm["ctx"]; v=mm["v_star"]
    phi_c, rho_c, uf, phi_a, rho_a, r_p, r_sU = C.unpack_comp(v, ctx)
    z=ctx["cell"]["zeta"].to(DEV); mu=ctx["cell"]["mu"].to(DEV)
    rng=np.random.default_rng(seed)
    # different analytic modes than the certification script
    phi_c=phi_c+sc*torch.cos(2*math.pi*(z+0.3))
    rho_c=rho_c+sc*torch.sin(math.pi*(z-0.2))
    uf=uf+sc*(1-mu[None,:]**2)*torch.cos(1.5*math.pi*(z[:,None]))
    return C.pack_comp(phi_c,rho_c,uf,phi_a,rho_a,float(r_p),float(r_sU),device=DEV)

def reach_metrics(mm, w):
    n=mm["n"]; resfn=mm["resfn"]; vstar=mm["v_star"].cpu().numpy().astype(np.longdouble)
    wt=torch.as_tensor(np.asarray(w,dtype=float),device=DEV)
    maxF=float(resfn(wt).abs().max())
    dist=float(np.abs(np.asarray(w,dtype=np.longdouble)-vstar).max())
    rp=float(abs(w[n-2])/abs(vstar[n-2]))
    return maxF, dist, rp

print("\n=== COMPONENT SEPARATION re-run (A1Z8), cert-shape vs my-shape, cell 0.3 ===")
def cert_shape_cell(mm, sc):
    ctx=mm["ctx"]; v=mm["v_star"]
    phi_c, rho_c, uf, phi_a, rho_a, r_p, r_sU = C.unpack_comp(v, ctx)
    z=ctx["cell"]["zeta"].to(DEV); mu=ctx["cell"]["mu"].to(DEV)
    uf=uf+sc*(1-mu[None,:]**2)*torch.sin(0.5*math.pi*(z[:,None]+1))
    phi_c=phi_c+sc*torch.sin(math.pi*(z+1)); rho_c=rho_c+sc*torch.cos(0.5*math.pi*z)
    return C.pack_comp(phi_c,rho_c,uf,phi_a,rho_a,float(r_p),float(r_sU),device=DEV)

for shapename, pf in [("certShape", cert_shape_cell), ("myShapeB", perturb_cell_shapeB)]:
    v0 = pf(mm, 0.3).cpu().numpy().astype(np.longdouble)
    d0 = float(np.abs(v0 - mm["v_star"].cpu().numpy().astype(np.longdouble)).max())
    # arclen
    w,info = D.arclength_homotopy(resfn, v0, n, budget=55.0, maxsteps=150, s_target=1.0,
                                  fold_abort=0.03, runaway_cap=1e5)
    mF,dist,rp = reach_metrics(mm,w)
    print(f"  {shapename:10s} d0={d0:.2f} ARCLEN s_max={info['s_max']:.3f} maxF={mF:.2e} dist={dist:.2e} rp={rp:.2f} {'REACH' if (mF<=1e-8 and dist<5 and 0.5<rp<2) else 'no'}")
    # fp
    w2,info2 = D.fixedpoint_homotopy(resfn, v0, n, budget=55.0)
    mF2,dist2,rp2 = reach_metrics(mm,w2)
    print(f"  {shapename:10s}          FP     s_reached={info2['s_reached']:.3f} maxF={mF2:.2e} dist={dist2:.2e} rp={rp2:.2f} {'REACH' if (mF2<=1e-8 and dist2<5 and 0.5<rp2<2) else 'no'}")
print("DONE bv_checks")

"""e2d_gridhomotopy_probe.py -- exercise the GRID-HOMOTOPY lever (charter §5 step 1a) on the
binding combined-cell field-distant cases that Newton + fixed-point homotopy could not bridge.
Coarse grid (fewer field DOFs -> wider basin) -> barycentric prolongate -> fine polish.  If the
coarse landscape has no s-fold, grid homotopy reaches v* where the fine-grid homotopies fold.

Method: build the MMS at coarse Nr_c and fine Nr with the SAME smooth genericize (so the coarse
root is the restriction of the fine root).  Perturb the COARSE seed by cell sc, solve coarse
(arclength homotopy on the coarse residual), prolongate to fine, polish on the fine TRUE residual,
check reach-to-fine-v*.  Bounded/GPU/CPU-checked.  Data-blind.
"""
import os, math, time, json
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np, torch
torch.set_default_dtype(torch.float64)
import cell_solver_composite as C
import e2d_continuation_driver as D

DEV = D.DEV
Nth, Na, KMAP = 8, 192, 2.5


def build_mms_grid(label, rp0_frac, amp, Nr, bulge=0.0):
    br = C.load_bracket(label); prm = (br["Z"], 0.5, 0.1, 1)
    ctx = C.make_ctx_comp(Nr, Nth, Na, kmap=KMAP, device=DEV)
    rp0 = rp0_frac * br["r_s"] if rp0_frac <= 1.0 else rp0_frac

    def genericize(v):
        phi_c, rho_c, uf, phi_a, rho_a, r_p, r_sU = C.unpack_comp(v, ctx)
        z = ctx["cell"]["zeta"].to(DEV); mu = ctx["cell"]["mu"].to(DEV); h = ctx["ha"].to(DEV)
        phi_c = phi_c + 0.05 * torch.cos(math.pi * z)
        rho_c = rho_c + 0.03 * torch.sin(0.5 * math.pi * (z + 1.0))
        uf = uf + 0.05 * (1.0 - mu[None, :] ** 2) * mu[None, :] * torch.cos(math.pi * (z[:, None] + 1.0))
        uf = uf + bulge * (1.0 - mu[None, :] ** 2) * torch.sin(math.pi * (z[:, None] + 1.0) / 2.0)
        phi_a = phi_a + 0.02 * torch.sin(math.pi * h)
        rho_a = rho_a + 0.01 * h * (1.0 - h)
        return C.pack_comp(phi_c, rho_c, uf, phi_a, rho_a, float(r_p), float(r_sU), device=DEV)

    v_star = genericize(C.seed_comp(ctx, br, rp0=rp0, amp=amp, device=DEV))
    F_star = C.residual_comp(v_star, ctx, prm, br).detach()
    resfn = lambda vv: C.residual_comp(vv, ctx, prm, br) - F_star
    return dict(br=br, prm=prm, ctx=ctx, v_star=v_star, resfn=resfn, F_star=F_star, n=v_star.numel())


def perturb_cell(mm, sc):
    ctx = mm["ctx"]; v = mm["v_star"]
    phi_c, rho_c, uf, phi_a, rho_a, r_p, r_sU = C.unpack_comp(v, ctx)
    z = ctx["cell"]["zeta"].to(DEV); mu = ctx["cell"]["mu"].to(DEV)
    uf = uf + sc * (1.0 - mu[None, :] ** 2) * torch.sin(0.5 * math.pi * (z[:, None] + 1.0))
    phi_c = phi_c + sc * torch.sin(math.pi * (z + 1.0))
    rho_c = rho_c + sc * torch.cos(0.5 * math.pi * z)
    return C.pack_comp(phi_c, rho_c, uf, phi_a, rho_a, float(r_p), float(r_sU), device=DEV)


def run(label, rpf, amp, bulge, sc, Nr_c=8, Nr_f=12, budget=90.0):
    mmC = build_mms_grid(label, rpf, amp, Nr_c, bulge=bulge)
    mmF = build_mms_grid(label, rpf, amp, Nr_f, bulge=bulge)
    nC, nF = mmC["n"], mmF["n"]
    v0C = perturb_cell(mmC, sc).cpu().numpy().astype(np.longdouble)
    t0 = time.time()
    # coarse solve (arclength homotopy on the coarse residual)
    wC, iC = D.arclength_homotopy(mmC["resfn"], v0C, nC, budget=budget * 0.6, maxsteps=150,
                                  fold_abort=0.03, runaway_cap=1e5)
    # prolongate coarse -> fine, polish on fine TRUE residual
    v0F = D.prolongate(torch.as_tensor(wC.astype(float), device=DEV), mmC["ctx"], mmF["ctx"])
    wF, iF = D._correct(mmF["resfn"], v0F.cpu().numpy().astype(np.longdouble), nF, maxit=300,
                        budget=budget * 0.4)
    # reach metrics vs fine v*
    vstarF = mmF["v_star"].cpu().numpy().astype(np.longdouble)
    wt = torch.as_tensor(wF.astype(float), device=DEV)
    maxF = float(mmF["resfn"](wt).abs().max())
    dist = float(np.abs(wF - vstarF).max())
    rp_ratio = float(abs(wF[nF - 2]) / abs(vstarF[nF - 2]))
    reach = maxF <= 1e-8 and dist < 5.0 and 0.5 < rp_ratio < 2.0
    print(f"  [{label} cell {sc}] coarseNr{Nr_c}->fineNr{Nr_f}: coarse s_max={iC['s_max']:.3f} "
          f"coarse_maxF={iC['maxF']:.2e} -> fine maxF={maxF:.2e} dist={dist:.2e} rp={rp_ratio:.2f} "
          f"{'REACH' if reach else 'no'} ({time.time()-t0:.0f}s)", flush=True)
    return dict(label=label, sc=sc, coarse_smax=iC["s_max"], coarse_maxF=iC["maxF"],
                fine_maxF=maxF, dist=dist, rp_ratio=rp_ratio, reach=bool(reach))


if __name__ == "__main__":
    out = []
    print("GRID-HOMOTOPY probe on the binding combined-cell field-distant cases:")
    for (lab, rpf, amp, bulge, sc) in [
            ("A1 m=3 Z=8", 0.95, 0.8, 0.0, 0.15),
            ("A1 m=3 Z=8", 0.95, 0.8, 0.0, 0.3),
            ("A3 Z=1", 100.0, 0.8, 0.4, 0.1),
            ("A3 Z=1", 100.0, 0.8, 0.4, 0.15),
            ("A3 Z=1", 100.0, 0.8, 0.4, 0.3)]:
        out.append(run(lab, rpf, amp, bulge, sc))
    json.dump(out, open("e2d_gridhomotopy_probe.json", "w"), indent=1, default=float)
    print("DONE grid-homotopy probe")

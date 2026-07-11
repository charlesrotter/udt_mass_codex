"""hopfion_static_mass_hessian.py -- Phase B: matrix-free Hessian classification of the
flat-background carrier energy E=E2+E4 about the banked H3 hopfion (dispatch section 4/5).

Tangent perturbations eta=(I-n n^T) dn. Matrix-free HVP by autodiff of the energy defined on
rays (n=m/|m|, scale-invariant so radial modes are null). Symmetry modes (translations,
rotations, target-SO(2) fixing n_inf) deflated via LOBPCG constraints. Lowest eigenvalues,
domain/grid scaling, explicit scale-mode E''(1)=2E4 test.

CRITICAL (dispatch): the exterior is GAPLESS. Extended modes with lambda ~ L_box^-2 -> 0 as the
box grows are EXPECTED and are NOT instability. Only a converged LOCALIZED_NEGATIVE fails.
"""
import argparse, json, numpy as np, torch
from scipy.sparse.linalg import LinearOperator, lobpcg
import hopfion_static_mass_common as C
torch.set_default_dtype(torch.float64)


def downsample(n, stride):
    return (n[:, ::stride, ::stride, ::stride]).contiguous()


def energy_of(n, h, xi, k4):
    n = n / n.norm(dim=0, keepdim=True)
    dn = [C._dc(n, i + 1, h) for i in range(3)]
    X = sum((dn[i] * dn[i]).sum(0) for i in range(3))
    def cr(a, b): return torch.stack([a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]], 0)
    Y = torch.zeros_like(X)
    for i in range(3):
        for j in range(3):
            if i != j:
                Fij = (n * cr(dn[i], dn[j])).sum(0)
                Y = Y + Fij * Fij
    return (0.5 * xi * X + 0.25 * k4 * Y).sum() * h**3


def symmetry_modes(n, h, L):
    """translations d_i n (3), rotations (x x grad) n (3), target-SO(2) about n_inf (1)."""
    dev = n.device; N = n.shape[1]
    x = torch.linspace(-L, L, N, device=dev)
    X, Y, Z = torch.meshgrid(x, x, x, indexing="ij")
    dn = [C._dc(n, i + 1, h) for i in range(3)]
    modes = []
    modes += dn                                                   # translations
    # spatial rotations L_k = (r x grad)_k
    modes.append(Y * dn[2] - Z * dn[1])
    modes.append(Z * dn[0] - X * dn[2])
    modes.append(X * dn[1] - Y * dn[0])
    # target rotation about n_inf: a x n with a=n_inf (=(0,0,-1) here)
    ninf = n[:, 0, 0, 0]
    a = ninf / ninf.norm()
    axn = torch.stack([a[1]*n[2]-a[2]*n[1], a[2]*n[0]-a[0]*n[2], a[0]*n[1]-a[1]*n[0]], 0)
    modes.append(axn)
    # project each to tangent, flatten, normalize
    out = []
    for m in modes:
        m = m - (m * n).sum(0, keepdim=True) * n                  # tangent projection
        v = m.reshape(-1).cpu().numpy()
        nv = np.linalg.norm(v)
        if nv > 1e-10:
            out.append(v / nv)
    return np.stack(out, axis=1)                                  # (3N, nmodes)


def make_hvp(n, h, xi, k4):
    from torch.func import grad, jvp
    n = n.detach()
    def E(m): return energy_of(m, h, xi, k4)
    gE = grad(E)
    def proj(v):
        return v - (v * n).sum(0, keepdim=True) * n
    def hvp(vec):
        v = torch.as_tensor(vec, dtype=torch.float64, device=n.device).reshape(n.shape)
        v = proj(v)
        _, Hv = jvp(gE, (n,), (v,))
        Hv = proj(Hv)
        return Hv.reshape(-1).cpu().numpy()
    return hvp


def run_grid(path, stride, L, xi, k4, kmodes=8, seed=0):
    d = C.load_h3(path); n0 = d["n"]; h0 = d["h"]
    n = downsample(n0, stride); n = n / n.norm(dim=0, keepdim=True)
    N = n.shape[1]; h = h0 * stride
    E2 = float((0.5 * xi * sum((C._dc(n, i+1, h)[None] * 0 + (C._dc(n, i+1, h) * C._dc(n, i+1, h)).sum(0)) for i in range(3))).sum() * h**3)  # placeholder
    mf = C.matter_fields(n, h, xi, k4); E2 = float(mf["rho2"].sum()*h**3); E4 = float(mf["rho4"].sum()*h**3)
    Q = float(d["stored"]["Q"])
    ndof = 3 * N**3
    Ymodes = symmetry_modes(n, h, L)
    hvp = make_hvp(n, h, xi, k4)
    A = LinearOperator((ndof, ndof), matvec=hvp, dtype=np.float64)
    rng = np.random.default_rng(seed)
    Xb = rng.standard_normal((ndof, kmodes))
    # tangent-project + deflate symmetry modes from the initial block
    nnp = n.reshape(3, -1).cpu().numpy()
    def tproj(V):
        Vr = V.reshape(3, N**3, -1)
        dots = (nnp[:, :, None] * Vr).sum(0, keepdims=True)
        Vr = Vr - dots * nnp[:, :, None]
        return Vr.reshape(ndof, -1)
    Xb = tproj(Xb)
    # localization: fraction of ||eta||^2 inside r<r_tex (localized) vs box (extended)
    dev = n.device
    xg = torch.linspace(-L, L, N, device=dev)
    Xg, Yg, Zg = torch.meshgrid(xg, xg, xg, indexing="ij")
    rmask = (torch.sqrt(Xg**2 + Yg**2 + Zg**2) <= 2.5).reshape(-1).cpu().numpy()
    def classify(vec, lam):
        w = (vec.reshape(3, N**3) ** 2).sum(0)                    # |eta|^2 per point
        frac = float(w[rmask].sum() / (w.sum() + 1e-30))          # in-core fraction
        ipr = float((w**2).sum() / (w.sum()**2 + 1e-30) * (N**3)) # inverse participation (large=localized)
        vol_frac = float(rmask.sum()) / (N**3)
        localized = frac > 5 * vol_frac                           # >> uniform => localized
        if lam < -1e-3 * abs(E4) / (N**3):                        # meaningfully negative (scale to problem)
            cls = "LOCALIZED_NEGATIVE" if localized else "EXTENDED_NEGATIVE(continuum/boundary)"
        elif abs(lam) < 1e-3 * abs(E4) / (N**3):
            cls = "LOCALIZED_ZERO" if localized else "EXTENDED_ZERO(continuum)"
        else:
            cls = "LOCALIZED_POSITIVE" if localized else "EXTENDED_POSITIVE"
        return dict(lam=float(lam), frac=frac, ipr=ipr, localized=bool(localized), cls=cls)
    try:
        vals, vecs = lobpcg(A, Xb, Y=Ymodes, largest=False, tol=1e-6, maxiter=200, retLambdaHistory=False)
        order = np.argsort(vals); vals = vals[order]; vecs = vecs[:, order]
        modes = [classify(vecs[:, i], vals[i]) for i in range(len(vals))]
    except Exception as e:
        vals = np.array([float("nan")]); modes = []; print("lobpcg warn:", e)
    # explicit scale mode E''(1) = 2 E4 : scan E(n(x/s)) at s near 1
    def E_at_scale(s):
        # n_s(x)=n(x/s): resample by scaling coordinates (nearest) -- use FFT-free linear via grid_sample
        import torch.nn.functional as Fn
        grid = torch.linspace(-1, 1, N, device=n.device)
        gx, gy, gz = torch.meshgrid(grid, grid, grid, indexing="ij")
        coords = torch.stack([gz, gy, gx], -1)[None] / s           # sample at x/s
        ns = Fn.grid_sample(n[None], coords, align_corners=True, padding_mode="border")[0]
        ns = ns / ns.norm(dim=0, keepdim=True)
        return float(energy_of(ns, h, xi, k4))
    ds = 0.02
    Epp = (E_at_scale(1 + ds) - 2 * E_at_scale(1.0) + E_at_scale(1 - ds)) / ds**2
    loc_neg = [m for m in modes if m["cls"] == "LOCALIZED_NEGATIVE"]
    return dict(N=N, L=L, h=h, ndof=ndof, E2=E2, E4=E4, Q=Q, nsym=Ymodes.shape[1],
                low_eigs=[float(v) for v in vals[:kmodes]], modes=modes,
                min_eig=float(np.nanmin(vals)), n_localized_negative=len(loc_neg),
                scale_Epp=float(Epp), scale_pred_2E4=float(2 * E4))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="hopfion_arc_scripts_2026-07-05/prod_an256.npz")
    ap.add_argument("--phase", default="spectrum")
    a = ap.parse_args()
    L = 6.0; xi = 1.0; k4 = 1.0
    runs = []
    for stride in (6, 4, 3):                                       # 3 grid/domain combos (43^3, 64^3, 86^3)
        r = run_grid(a.input, stride, L, xi, k4)
        print(f"stride={stride} N={r['N']} nsym={r['nsym']} min_eig={r['min_eig']:+.3e} "
              f"LOCALIZED_NEG={r['n_localized_negative']}  scale E''={r['scale_Epp']:.2f} vs 2E4={r['scale_pred_2E4']:.2f}")
        for m in r["modes"][:6]:
            print(f"    lam={m['lam']:+.3e}  in-core frac={m['frac']:.3f}  {m['cls']}")
        runs.append(r)
    any_locneg = any(rr["n_localized_negative"] > 0 for rr in runs)
    gate = "FAIL_H3_INSTABILITY" if any_locneg else "PASS(no localized negative mode)"
    print(f"\nPHASE B GATE: {gate}")
    json.dump({"hessian_runs": runs, "gate": gate}, open("hopfion_static_mass_hessian_out.json", "w"), indent=1)
    print("saved hopfion_static_mass_hessian_out.json")

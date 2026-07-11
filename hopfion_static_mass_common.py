"""hopfion_static_mass_common.py -- shared, unit-tested operations for the H3 static
mass-backreaction dispatch (UDT_H3_STATIC_MASS_BACKREACTION_DISPATCH.md).

Frozen action (metric-native, EH geometric term CONDITIONAL-DERIVED via metric-only/local/
2-derivative minimality; NO g-bar, NO reciprocal-interior constraint, NO G/P, NO private wall):
    S = (1/2 kg) int sqrt(-g) R  +  int sqrt(-g)[ -(xi/2) dn.dn - (k4/4) Omega_uv Omega^uv ]
Static-slice matter identities (Section 2 of the dispatch), spatial metric gamma_ij (flat for Phase A/C):
    X = D_i n . D^i n ;  F_ij = n.(D_i n x D_j n) ;  Y = F_ij F^ij
    rho   = (xi/2) X + (k4/4) Y
    S_ij  = xi (D_i n.D_j n - 1/2 g_ij X) + k4 (F_i^k F_jk - 1/4 g_ij Y)
    S     = -(xi/2) X + (k4/4) Y
    rho+S = (k4/2) Y = 2 rho4 >= 0        [load-bearing positivity]
    D^2 N = kg N rho4                      [positive compact lapse source]
    M_N[dV] = (2/kg) oint D_i N dS^i = 2 int N rho4 dV   ;  weak field: M_N -> 2 E4 ~ E2+E4
DATA-BLIND. No particle labels, no fitted couplings.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np, torch
torch.set_default_dtype(torch.float64)


def load_h3(path, device=None):
    dev = device or ("cuda" if torch.cuda.is_available() else "cpu")
    d = np.load(path)
    n = torch.tensor(d["n"], device=dev)
    n = n / n.norm(dim=0, keepdim=True)                    # unit projection
    return dict(n=n, N=int(d["N"]), L=float(d["L"]), h=float(d["h"]),
                xi=float(d["xi"]), k4=float(d["kappa"]), stored=d, dev=dev)


def _dc(f, ax, h):
    return (torch.roll(f, -1, ax) - torch.roll(f, 1, ax)) / (2 * h)   # banked central-diff convention


def matter_fields(n, h, xi, k4):
    """Return dict with X, Y, rho2=(xi/2)X, rho4=(k4/4)Y, rho, S, Sij (3x3,N,N,N), e2,e4 densities."""
    dn = [_dc(n, i + 1, h) for i in range(3)]              # D_i n on flat slice
    X = sum((dn[i] * dn[i]).sum(0) for i in range(3))      # D_i n . D^i n
    def cross(a, b):
        return torch.stack([a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]], 0)
    F = {}
    for i in range(3):
        for j in range(3):
            F[(i, j)] = (n * cross(dn[i], dn[j])).sum(0) if i != j else torch.zeros_like(X)
    Y = sum(F[(i, j)] * F[(i, j)] for i in range(3) for j in range(3))   # F_ij F^ij (flat)
    rho2 = 0.5 * xi * X
    rho4 = 0.25 * k4 * Y
    rho = rho2 + rho4
    # S_ij (flat gamma=delta)
    Sij = torch.zeros(3, 3, *X.shape, device=X.device)
    for i in range(3):
        for j in range(3):
            dd = (dn[i] * dn[j]).sum(0)
            FikFjk = sum(F[(i, k)] * F[(j, k)] for k in range(3))
            Sij[i, j] = xi * (dd - 0.5 * (X if i == j else 0.0)) \
                + k4 * (FikFjk - 0.25 * (Y if i == j else 0.0))
    S = sum(Sij[i, i] for i in range(3))                   # trace
    return dict(X=X, Y=Y, rho2=rho2, rho4=rho4, rho=rho, S=S, Sij=Sij,
                e2=rho2, e4=rho4)                          # E2=int rho2, E4=int rho4


def energies(mf, h):
    E2 = float(mf["rho2"].sum() * h**3)
    E4 = float(mf["rho4"].sum() * h**3)
    return E2, E4


def axisymmetry_residual(field, L, nbin=64):
    """||field - <field>_phi|| / ||field|| about the z-axis (m!=0 azimuthal content). field: (N,N,N)."""
    dev = field.device
    N = field.shape[0]
    x = torch.linspace(-L, L, N, device=dev)
    Xc, Yc, Zc = torch.meshgrid(x, x, x, indexing="ij")
    phi = torch.atan2(Yc, Xc)                              # azimuth
    rho_cyl = torch.sqrt(Xc**2 + Yc**2)
    # bin by (rho_cyl, z); subtract azimuthal mean within each (rho_cyl,z) bin
    rb = torch.clamp((rho_cyl / L * nbin).long(), 0, nbin - 1)
    zb = torch.clamp(((Zc + L) / (2 * L) * nbin).long(), 0, nbin - 1)
    key = (rb * nbin + zb).flatten()
    fv = field.flatten()
    nb = nbin * nbin
    s = torch.zeros(nb, device=dev).scatter_add_(0, key, fv)
    c = torch.zeros(nb, device=dev).scatter_add_(0, key, torch.ones_like(fv))
    mean = (s / c.clamp(min=1))[key].reshape(field.shape)
    return float((field - mean).norm() / field.norm().clamp(min=1e-30))


def cumulative_mass_flux(rho4, L, nR=80):
    """Gauss-law mass: M_N(R) = 2 * int_{r<R} rho4 dV  (= 2 oint_{S_R} grad u . dS for D^2u=rho4).
    Compact rho4 => plateaus at 2 E4, cutoff-independent. Returns (Rs, MN_R, E4)."""
    dev = rho4.device
    N = rho4.shape[0]; h = 2 * L / (N - 1)
    x = torch.linspace(-L, L, N, device=dev)
    Xc, Yc, Zc = torch.meshgrid(x, x, x, indexing="ij")
    r = torch.sqrt(Xc**2 + Yc**2 + Zc**2)
    E4 = float(rho4.sum() * h**3)
    Rs = np.linspace(0.5, L * 0.98, nR)
    MN = []
    for R in Rs:
        MN.append(2.0 * float((rho4 * (r <= R)).sum() * h**3))
    return Rs, np.array(MN), E4


def poisson_solve_isolated(rho4, L):
    """TRUE isolated (free-space) Poisson: Laplacian u = rho4, u->0 at infinity, via the Hockney
    method -- zero-pad to 2N and convolve with the FREE-SPACE Green's function G(r)=-1/(4 pi r)
    (signed-index kernel + zero-pad => NO periodic images). Returns u (N,N,N)."""
    dev = rho4.device
    N = rho4.shape[0]; h = 2 * L / (N - 1)
    M = 2 * N
    src = torch.zeros(M, M, M, device=dev); src[:N, :N, :N] = rho4
    idx = torch.arange(M, device=dev); idx = torch.where(idx < N, idx, idx - M).to(torch.float64)
    IX, IY, IZ = torch.meshgrid(idx, idx, idx, indexing="ij")
    r = torch.sqrt(IX**2 + IY**2 + IZ**2) * h
    r[0, 0, 0] = 0.5 * h                                   # regularize the self-cell
    G = -1.0 / (4 * np.pi * r)
    u = torch.fft.ifftn(torch.fft.fftn(src) * torch.fft.fftn(G)).real * h**3   # discrete convolution
    return u[:N, :N, :N].contiguous()


def discrete_face_flux(u, half, h):
    """EXACT discrete Gauss-law flux over the cubic box of cells [c-half, c+half]^3, using the ONE-SIDED
    differences across the 6 box faces that the 7-point Laplacian's telescoping sum produces:
        sum_{cells in box} lap_FD(u) * h^3  ==  h * sum_{boundary bonds} (u_outside - u_inside).
    (Central differences do NOT give the discrete divergence theorem; one-sided bonds do.) If u solves
    lap_FD(u)=rho4, this equals the enclosed charge sum rho4*h^3 EXACTLY, for any BC (Gauss is local)."""
    N = u.shape[0]; c = N // 2
    lo, hi = c - half, c + half
    sl = slice(lo, hi + 1)
    s = 0.0
    s += float((u[hi + 1, sl, sl] - u[hi, sl, sl]).sum())     # +x boundary bonds (inside hi -> outside hi+1)
    s += float((u[lo - 1, sl, sl] - u[lo, sl, sl]).sum())     # -x
    s += float((u[sl, hi + 1, sl] - u[sl, hi, sl]).sum())     # +y
    s += float((u[sl, lo - 1, sl] - u[sl, lo, sl]).sum())     # -y
    s += float((u[sl, sl, hi + 1] - u[sl, sl, hi]).sum())     # +z
    s += float((u[sl, sl, lo - 1] - u[sl, sl, lo]).sum())     # -z
    return s * h


def poisson_solve_open(rho4, L):
    """Solve Laplacian u = rho4 with u->0 (open BC) via zero-padded FFT. The source is CENTERED in
    the padded domain (else it sits by the pad boundary and periodic images leak -> large residual).
    Uses the FD (7-point) Laplacian symbol so the solution is FD-consistent (small FD residual).
    Returns u (N,N,N)."""
    dev = rho4.device
    N = rho4.shape[0]; h = 2 * L / (N - 1)
    M = 2 * N                                              # zero-pad to suppress periodic images
    off = (M - N) // 2                                     # CENTER the source in the padded box
    src = torch.zeros(M, M, M, device=dev)
    src[off:off + N, off:off + N, off:off + N] = rho4
    kk = 2 * np.pi * torch.fft.fftfreq(M, d=h).to(dev)
    KX, KY, KZ = torch.meshgrid(kk, kk, kk, indexing="ij")
    # FD 7-point Laplacian symbol (so ifft solution is consistent with the FD Laplacian used for residual)
    sym = (2 * torch.cos(KX * h) + 2 * torch.cos(KY * h) + 2 * torch.cos(KZ * h) - 6) / h**2
    sym[0, 0, 0] = 1.0
    u = torch.fft.ifftn(torch.fft.fftn(src) / sym).real    # FD_Laplacian u = rho4
    u = u - u.mean()
    return u[off:off + N, off:off + N, off:off + N].contiguous()

"""Preconditioning + gradient verification for the no-null re-solve (Charles steer 2026-07-11).

(A) Verify grad_noNull (per-orientation accumulation) against the FULL-autograd gradient of energy_noNull
    on small grids (where the full 8-orientation graph fits) -- must match to ~machine precision.
(B) SPD spectral preconditioner from the no-null lattice symbol
        L_h(k) = (4/h^2) sum_a sin^2(k_a h / 2)   (= symbol of the forward/link Laplacian; SPD, 0 only at k=0)
    applied to the RESIDUAL / SEARCH DIRECTION ONLY (never to the energy or Hessian being tested):
        precond(r) = IFFT( FFT(r) / (xi*L_h(k) + shift) ) ,  shift regularizes the k=0 / low-k band.
    This damps the +3e4 Nyquist stiffness in the search direction, leaving E and HVP untouched.

Also provides mnorm(g,h) = ||g||_{M^-1} = ||g||_2 / h^{3/2}  (resolution-aware residual; M=h^3 I) for grading
criticality consistently with lam_phys = lam_euclid/h^3."""
import numpy as np, torch


def Lh_symbol(N, h, dev):
    k = 2 * np.pi * torch.fft.fftfreq(N, d=h).to(dev)
    KX, KY, KZ = torch.meshgrid(k, k, k, indexing='ij')
    return (4.0 / h**2) * (torch.sin(KX * h / 2)**2 + torch.sin(KY * h / 2)**2 + torch.sin(KZ * h / 2)**2)


def make_precond(N, h, xi, dev, shift=None):
    Lh = Lh_symbol(N, h, dev)
    if shift is None:
        nz = Lh[Lh > 0]
        shift = float(nz.min()) * 4.0                       # light low-k regularization (~ few lowest-k modes)
    denom = xi * Lh + shift

    def precond(r):                                          # r: (3,N,N,N) -> preconditioned (SPD)
        R = torch.fft.fftn(r, dim=(1, 2, 3))
        return torch.fft.ifftn(R / denom, dim=(1, 2, 3)).real
    return precond, float(shift)


def mnorm(g, h):                                            # ||g||_{M^-1}, M=h^3 I  (resolution-aware)
    return float(g.norm()) / h**1.5


if __name__ == '__main__':
    import sys
    sys.path.insert(0, 'hopfion_arc_scripts_2026-07-05')
    from noNull_energy import energy_noNull, grad_noNull
    torch.set_default_dtype(torch.float64); dev = 'cuda' if torch.cuda.is_available() else 'cpu'
    xi, kap = 1.0, 1.0

    def smooth_field(N, Lbox=2 * np.pi):
        x = torch.arange(N, device=dev) * Lbox / N
        X, Y, Z = torch.meshgrid(x, x, x, indexing='ij')
        n = torch.stack([torch.sin(X) * torch.cos(Z), torch.sin(Y), 2.0 + torch.cos(Z) * torch.cos(X)], 0)
        return n / n.norm(dim=0, keepdim=True)

    print("=== (A) grad_noNull vs FULL-autograd gradient (small grids) ===", flush=True)
    for N in (16, 24, 32):
        h = 2 * np.pi / N
        n = smooth_field(N)
        g_acc = grad_noNull(n, h, xi, kap)                  # per-orientation accumulation
        n2 = n.clone().requires_grad_(True)                 # full autograd (whole 8-orientation graph)
        g_full, = torch.autograd.grad(energy_noNull(n2, h, xi, kap)[0], n2)
        rel = float((g_acc - g_full.detach()).norm() / g_full.norm())
        print(f"  N={N:3d}  ||g_acc - g_full||/||g_full|| = {rel:.3e}", flush=True)

    print("\n=== (B) preconditioner: effective conditioning of the search direction ===", flush=True)
    N = 48; h = 2 * np.pi / N
    Lh = Lh_symbol(N, h, dev)
    print(f"  L_h(k) range: min-nonzero={float(Lh[Lh>0].min()):.3f}  max(Nyquist)={float(Lh.max()):.3f}  "
          f"ratio={float(Lh.max()/Lh[Lh>0].min()):.1f}", flush=True)
    precond, shift = make_precond(N, h, xi, dev)
    print(f"  shift={shift:.4f}", flush=True)
    # a stiff residual = smooth part + Nyquist part; show precond equalizes their magnitudes
    n = smooth_field(N)
    ii = torch.arange(N, device=dev); IX, IY, IZ = torch.meshgrid(ii, ii, ii, indexing='ij')
    sgn = (((IX + IY + IZ) % 2 == 0).double() * 2 - 1)
    env = torch.exp(-(((IX - N / 2)**2 + (IY - N / 2)**2 + (IZ - N / 2)**2) / (2 * (N / 6)**2)))
    smooth = torch.stack([env * torch.cos(2 * np.pi * IX / (N / 4)) for _ in range(3)], 0)
    nyq = torch.stack([env * sgn for _ in range(3)], 0)
    for nm, r in (('smooth', smooth), ('Nyquist', nyq)):
        rp = precond(r)
        print(f"  {nm:8s}: ||r||={float(r.norm()):.3e} -> ||P r||={float(rp.norm()):.3e}  "
              f"(precond gain {float(rp.norm()/r.norm()):.4f})", flush=True)
    print("  -> Nyquist gets a MUCH smaller gain than smooth => stiff band damped in the search direction")

"""STEP 2 of the corrected-operator plan (Charles + collaborating AI, 2026-07-11): a Faddeev-Skyrme
energy with NO Nyquist null, to replace the centered-difference energy (fs_hopfion.py:54) whose
D^c=(f_{i+1}-f_{i-1})/2h annihilates the checkerboard mode (-1)^i exactly and produced spurious
negative Hessian modes (see stability_checkerboard_audit_out.json: all 3 negative modes had R_cb~0.01).

REPRESENTATION CHANGE, NOT A NEW PHYSICAL OPERATOR: same continuum functional
    E = int [ (xi/2) d_i n . d_i n  +  (kappa/4) F_ij F_ij ] ,  F_ij = n.(d_i n x d_j n),
discretized as the average over the 8 one-sided orientations s in {+,-}^3 of the density built with
the one-sided difference D^{s_a}_a n (forward if s_a=+, backward if s_a=-). Each one-sided difference
has symbol (e^{i k h}-1)/h (backward: (1-e^{-i k h})/h), NONZERO at k=pi/h -> no null. The 8-fold
average is cubic-symmetric and O(h^2)-consistent for smooth fields (the O(h) forward/backward biases
cancel). Fully autograd-differentiable (drop-in for the Hessian re-solve).

Matches fs_hopfion.energy's normalization exactly per orientation; returns (E, E2, E4)."""
import torch


_ORIENTS = [(s0, s1, s2) for s0 in (1, -1) for s1 in (1, -1) for s2 in (1, -1)]


def _dop(f, ax, s, h):                              # one-sided first difference, no Nyquist null
    return (torch.roll(f, -1, ax) - f) / h if s > 0 else (f - torch.roll(f, 1, ax)) / h


def _cross(a, b):
    return torch.stack([a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]], 0)


def _orient_E2E4(n, h, xi, kappa, s):               # single-orientation (E2, E4), n already unit
    dn = [_dop(n, 1, s[0], h), _dop(n, 2, s[1], h), _dop(n, 3, s[2], h)]
    e2 = 0.5 * xi * sum((dn[i] * dn[i]).sum(0) for i in range(3))
    e4 = torch.zeros_like(e2)
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            Fij = (n * _cross(dn[i], dn[j])).sum(0)
            e4 = e4 + 0.25 * kappa * Fij * Fij
    dV = h**3
    return e2.sum() * dV, e4.sum() * dV


def energy_noNull(n_raw, h, xi, kappa):             # VALUE = 8-orientation average (fine w/o grad)
    n = n_raw / n_raw.norm(dim=0, keepdim=True)
    E2 = n.new_zeros(()); E4 = n.new_zeros(())
    for s in _ORIENTS:
        e2, e4 = _orient_E2E4(n, h, xi, kappa, s); E2 = E2 + e2; E4 = E4 + e4
    return (E2 + E4) / 8, E2 / 8, E4 / 8


def grad_noNull(n_raw, h, xi, kappa):               # MEMORY-SAFE gradient: sum per-orientation grads
    """grad of (1/8) sum_s E_s w.r.t. n_raw, accumulated one orientation at a time so the autograd graph
    of only ONE orientation is ever live (the full 8-orientation graph OOMs at 256^3)."""
    g = torch.zeros_like(n_raw)
    for s in _ORIENTS:
        n2 = n_raw.detach().clone().requires_grad_(True)
        nn = n2 / n2.norm(dim=0, keepdim=True)
        e2, e4 = _orient_E2E4(nn, h, xi, kappa, s)
        gg, = torch.autograd.grad((e2 + e4) / 8, n2)
        g = g + gg.detach(); del n2, nn, gg
    return g


def energy_centered(n_raw, h, xi, kappa):           # reference: the OLD centered-difference energy
    n = n_raw / n_raw.norm(dim=0, keepdim=True)

    def dc(f, ax):
        return (torch.roll(f, -1, ax) - torch.roll(f, 1, ax)) / (2 * h)

    def cross(a, b):
        return torch.stack([a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]], 0)
    dn = [dc(n, i + 1) for i in range(3)]
    dV = h**3
    e2 = 0.5 * xi * sum((dn[i] * dn[i]).sum(0) for i in range(3))
    e4 = torch.zeros_like(e2)
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            Fij = (n * cross(dn[i], dn[j])).sum(0)
            e4 = e4 + 0.25 * kappa * Fij * Fij
    E2 = e2.sum() * dV; E4 = e4.sum() * dV
    return E2 + E4, E2, E4


if __name__ == '__main__':
    import numpy as np
    torch.set_default_dtype(torch.float64)
    dev = 'cuda' if torch.cuda.is_available() else 'cpu'
    xi, kappa = 1.0, 1.0

    def smooth_field(N, Lbox=2 * np.pi):             # smooth periodic manufactured field, |n|=1
        x = torch.arange(N, device=dev) * Lbox / N
        X, Y, Z = torch.meshgrid(x, x, x, indexing='ij')
        n = torch.stack([torch.sin(X) * torch.cos(Z), torch.sin(Y), 2.0 + torch.cos(Z) * torch.cos(X)], 0)
        return n / n.norm(dim=0, keepdim=True)

    print("=== (A) CONVERGENCE on a smooth manufactured field (Lbox=2pi) ===", flush=True)
    print("    expect O(h^2): successive-difference ratio ~4 as N doubles; noNull and centered -> same limit")
    Es = {}
    for N in (32, 64, 128, 256):
        h = 2 * np.pi / N
        n = smooth_field(N)
        En = float(energy_noNull(n, h, xi, kappa)[0]); Ec = float(energy_centered(n, h, xi, kappa)[0])
        Es[N] = (En, Ec)
        print(f"  N={N:4d} h={h:.5f}  E_noNull={En:.6f}  E_centered={Ec:.6f}  diff={En-Ec:+.3e}", flush=True)
    for op, idx in (('noNull', 0), ('centered', 1)):
        d1 = Es[64][idx] - Es[32][idx]; d2 = Es[128][idx] - Es[64][idx]; d3 = Es[256][idx] - Es[128][idx]
        print(f"  {op:9s} Richardson ratios (want ~4 for O(h^2)): {d1/d2:.2f}, {d2/d3:.2f}")

    print("\n=== (B) NO-NULL TEST: a PURE Nyquist mode (smooth envelope x checkerboard) ===", flush=True)
    N = 64; h = 2 * np.pi / N
    n = smooth_field(N)
    ii = torch.arange(N, device=dev); IX, IY, IZ = torch.meshgrid(ii, ii, ii, indexing='ij')
    sgn = (((IX + IY + IZ) % 2 == 0).double() * 2 - 1)
    env = torch.exp(-(((IX - N / 2)**2 + (IY - N / 2)**2 + (IZ - N / 2)**2) / (2 * (N / 6)**2)))  # smooth
    e = torch.tensor([1.0, 0.3, -0.7], device=dev).view(3, 1, 1, 1)
    u = (e * env * sgn); u = u - (u * n).sum(0, keepdim=True) * n            # smooth-envelope Nyquist, tangent
    cb = u / u.norm()
    E0n = float(energy_noNull(n, h, xi, kappa)[0]); E0c = float(energy_centered(n, h, xi, kappa)[0])
    for delta in (0.02, 0.01, 0.005):
        npert = n + delta * cb * n.norm()
        dEn = float(energy_noNull(npert, h, xi, kappa)[0]) - E0n
        dEc = float(energy_centered(npert, h, xi, kappa)[0]) - E0c
        print(f"  delta={delta:.3f}  dE_noNull={dEn:+.4e} (/delta^2={dEn/delta**2:.1f})  "
              f"dE_centered={dEc:+.4e} (/delta^2={dEc/delta**2:.2f})  centered/noNull={dEc/dEn:.4f}", flush=True)
    print("  -> pure Nyquist mode: noNull COSTS large O(delta^2) energy; centered cost is a tiny fraction (the null)")

    print("\n=== (C) autograd differentiability check ===", flush=True)
    N = 32; h = 2 * np.pi / N; n = smooth_field(N).clone().requires_grad_(True)
    g, = torch.autograd.grad(energy_noNull(n, h, xi, kappa)[0], n)
    print(f"  grad ok: ||grad E_noNull||={float(g.norm()):.4e}  finite={bool(torch.isfinite(g).all())}")

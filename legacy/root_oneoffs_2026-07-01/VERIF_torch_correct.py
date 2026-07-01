#!/usr/bin/env python3
"""
Patch the committed torch solver to use the CORRECT matter EL (verified consistent
with the Hilbert stress) and re-run the gate + l=2 relax-back with the SAME robust
torch dense LM the committed solver used.  Everything else (Einstein, Hilbert
stress, weighting, BCs, LM) is the committed machinery -- ONLY the EL is replaced.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math
import numpy as np
import torch
torch.set_default_dtype(torch.float64)

import spectral_catalog_solver as S
from spectral_catalog_solver import (TGrid, metric_stack, einstein_mixed_t,
    matter_stress_t, unpack, pack, diagnostics, round_seed, DEV, PI)

# --- build a torch-callable CORRECT EL by exec'ing the numpy source with torch ---
def _load_correct_el():
    src = open('axisym_matter_el_CORRECT.py').read()
    src = '\n'.join(l for l in src.split('\n')
                    if not l.strip().startswith('import numpy')
                    and not l.strip().startswith('from numpy'))
    ns = {'np': torch, 'numpy': torch, 'exp': torch.exp, 'sin': torch.sin,
          'cos': torch.cos, 'tan': torch.tan, 'sqrt': torch.sqrt}
    exec(src, ns)
    return ns['matter_el_resid_CORRECT']

_ELc = _load_correct_el()


def matter_el_correct_t(G, Th, a, b, c, d, xi=1.0, kap=1.0):
    def D(f):
        fr = G.d_r(f); ft = G.d_th(f)
        return f, fr, ft, G.d_r(fr), G.d_th(ft), G.d_th(fr)
    A = D(a); B = D(b); C = D(c); Dd = D(d); Tt = D(Th)
    return _ELc(G.R, G.THm, A[0], A[1], A[2], A[3], A[4], A[5],
               B[0], B[1], B[2], B[3], B[4], B[5],
               C[0], C[1], C[2], C[3], C[4], C[5],
               Dd[0], Dd[1], Dd[2], Dd[3], Dd[4], Dd[5],
               Tt[0], Tt[1], Tt[2], Tt[3], Tt[4], Tt[5], xi, kap)


# monkeypatch the EL used inside residual_fields
S.matter_el_t = matter_el_correct_t


def legP(l, x):
    from numpy.polynomial.legendre import Legendre
    cc = np.zeros(l+1); cc[l] = 1.0
    return Legendre(cc)(x)


if __name__ == "__main__":
    import sys
    Nr, Nth = 40, 6
    G = TGrid(Nr, Nth, rc=0.05, cell=14.0)
    u0, rad = round_seed(G, p=0.4, kap8=0.05)

    print(f"=== GATE (round seed), CORRECT EL, Nr={Nr} Nth={Nth} ===")
    # verify EL machine-zero on round seed
    a, b, c, d, Th = unpack(u0, G)
    el0 = matter_el_correct_t(G, Th, a, b, c, d)
    body = (G.R > 0.8) & (G.R < G.ri-0.8)
    print(f"  CORRECT EL on round seed, body max = {float(el0[body].abs().max()):.3e}")
    u, rf, hist = S.lm_solve(u0, G, 0.4, 0.05, maxit=30, verbose=False)
    dg = diagnostics(G, rf, 0.05)
    F = S.residual_vector(u, G, 0.4, 0.05)[0]
    print(f"  GATE solved: Phi={float((F**2).sum()):.3e} M_MS={dg['M_MS']:.5f} "
          f"tvar={dg['tvar']:.4e} res_thth={dg['res_thth']:.2e} res_EL={dg['res_EL']:.2e} cdshape={dg['cdshape']:.2e}")

    for kind in (sys.argv[1:] or ['l2']):
        a, b, c, d, Th = unpack(u0, G)
        a = a.clone(); b = b.clone(); c = c.clone(); d = d.clone(); Th = Th.clone()
        rprof = torch.exp(-((G.R-2.0)/1.5)**2)
        if kind.startswith('l'):
            Pl = torch.tensor(legP(int(kind[1:]), G.CTH.cpu().numpy()), device=DEV)
            Th = Th + 0.30*rprof*Pl
        elif kind == 'ring':
            Th = Th + 0.40*rprof*torch.sin(G.THm)**2
        Th[0, :] = PI; Th[-1, :] = 0.0
        us = pack(a, b, c, d, Th)
        F0, rf0 = S.residual_vector(us, G, 0.4, 0.05)
        d0 = diagnostics(G, rf0, 0.05)
        print(f"\n=== seed {kind} CORRECT EL: seed_tvar={d0['tvar']:.4f} Phi0={float((F0**2).sum()):.2e} ===")
        u = us
        for blk in range(6):
            u, rf, h = S.lm_solve(u, G, 0.4, 0.05, maxit=12)
            dg = diagnostics(G, rf, 0.05)
            F = S.residual_vector(u, G, 0.4, 0.05)[0]
            print(f"  block {blk+1}: Phi={float((F**2).sum()):.3e} tvar={dg['tvar']:.4e} "
                  f"M_MS={dg['M_MS']:.5f} res_thth={dg['res_thth']:.2e} res_EL={dg['res_EL']:.2e} cdshape={dg['cdshape']:.2e}")

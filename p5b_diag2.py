#!/usr/bin/env python3
"""p5b_diag2.py -- inspect the single near-null right-singular vector (smin=6.3e-5)
of the reposed J, and test whether a TINY Tikhonov/damping (LSMR's own damp) already
floors it -- i.e. whether the deep-floor plateau is (a) this isolated mode or (b) the
bulk kappa.  Also probe the Nr-dependence of smin (does the near-null mode persist?).
Driver: Claude Opus 4.8.  2026-06-20.  DATA-BLIND.  Branch p5b-pc-floor."""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")
import numpy as np, torch
torch.set_default_dtype(torch.float64)
from full3d_spectral import Grid3D, attach_coord_weight
from full3d_solver import round_seed
import p5a_prime_repose as RP

fields = ['a', 'b', 'c', 'd', 'Th']

def probe(NR, NTH=6, NPS=8, P=0.4, KAP8=0.05):
    G = Grid3D(NR, NTH, NPS, rc=0.05, cell=14.0); G = attach_coord_weight(G)
    u0, sol = round_seed(G, p=P, kap8=KAP8)
    rp = RP.Repose(G, p=P, m=1, edge_mode='hold', fit_deg=4); rp.set_edge_hold(u0)
    ub0 = rp.extract(u0)
    J, F = RP.reposed_jacobian_jacrev(ub0, rp, KAP8)
    U, S, Vh = torch.linalg.svd(J, full_matrices=False)
    kappa = float(S[0]/S[-1])
    # count SVs below 1e-3*smax = "isolated tail"
    nsmall = int((S < 1e-3*S[0]).sum())
    # the smallest right-singular vector
    v = Vh[-1].reshape(5, rp.nbr, NTH, NPS)
    energy = (v*v).sum(dim=(1, 2, 3))
    dom_field = fields[int(energy.argmax())]
    # radial localization
    rad = (v*v).sum(dim=(0, 2, 3))
    return dict(NR=NR, kappa=kappa, smax=float(S[0]), smin=float(S[-1]),
                s2=float(S[-2]), nsmall=nsmall,
                field_energy={fields[i]: float(energy[i]) for i in range(5)},
                dom_field=dom_field, rad=rad.cpu().numpy(),
                body_r=rp.body_r.cpu().numpy(), r=G.r.cpu().numpy())

for NR in [12, 16, 24]:
    d = probe(NR)
    print(f"\nNr={NR}: kappa={d['kappa']:.3e} smax={d['smax']:.3e} smin={d['smin']:.3e} "
          f"2nd-smallest={d['s2']:.3e}  (#SV<1e-3*smax={d['nsmall']})")
    print(f"  smallest-SV field energy: " +
          " ".join(f"{k}={v:.2f}" for k, v in d['field_energy'].items()) +
          f"  -> dominant: {d['dom_field']}")
    rprof = d['rad']/d['rad'].max()
    print("  radial energy profile (body rows): " +
          " ".join(f"r{int(br)}={rprof[i]:.2f}" for i, br in enumerate(d['body_r'])))
print("\n[done diag2]")

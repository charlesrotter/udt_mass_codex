#!/usr/bin/env python3
"""
gapcloser_seeds.py -- seed constructors for the gap-closer search.

Driver: Claude (Opus 4.8, 1M).  2026-06-15.  OBSERVE mode.  DATA-BLIND.

Provides:
  * the CORRECTED #56 round soliton mapped onto the (r,theta,psi) grid (the gate /
    relax-back target), solved DIRECTLY at the grid Nr (no interpolation degradation);
  * a library of qualitatively-DIFFERENT seeds for the disconnected-type search:
    multipole (l=1..4) angular shaping, prolate/oblate deformation, two-center on
    axis, ring/toroidal, large-amplitude -- each a DEFORMATION of the round metric
    and/or the matter profile, NOT a new mechanism (we deform initial data and let the
    gauge-fixed solver relax; whatever it settles into is the OBSERVATION).

All metrics carry ALL 10 components allocated; deformations turn on shape and (where
named) off-diagonal pieces, all of which are FREE in the solve.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math
import numpy as np
import torch

torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
T, R, TH, PS = 0, 1, 2, 3

import whole_metric_3d_solver as S
import radial_Bfree_soliton as rb

XI = KAP = 1.0


def solve_radial56(Nr, rc, ri, p=0.4, kap8=0.05):
    """Solve the corrected #56 radial soliton at resolution Nr (matched, no interp)."""
    rN = rb.make_grid(1, Nr, rc=rc, rint=ri, geom=False)
    o = rb.selfconsistent_Bfree(rN, XI, KAP, p=p, kap8=kap8, iters=300, relax=0.4,
                                tol=1e-11, verbose=False)
    return (o['a'][0], o['b'][0], o['Th'][0], o['r'][0], o['M_MS'].item())


def round_metric(G, a_r, b_r):
    """Diagonal round soliton on the grid (a,b independent -- the #56 correction)."""
    Nr, Nth, Nps = G['Nr'], G['Nth'], G['Nps']
    a_f = a_r[:, None, None].expand(Nr, Nth, Nps)
    b_f = b_r[:, None, None].expand(Nr, Nth, Nps)
    g = torch.zeros(Nr, Nth, Nps, 4, 4, device=DEV)
    g[..., T, T] = -torch.exp(2*a_f)
    g[..., R, R] = torch.exp(2*b_f)
    g[..., TH, TH] = G['Rr']**2
    g[..., PS, PS] = (G['Rr']*torch.sin(G['Tht']))**2
    return g


def round_seed(G, rc, ri, p=0.4, kap8=0.05):
    """The gate / relax-back target: round #56 soliton + hedgehog profile field."""
    a_r, b_r, Th_r, rr, M = solve_radial56(G['Nr'], rc, ri, p=p, kap8=kap8)
    g = round_metric(G, a_r, b_r)
    Th_field = Th_r[:, None, None].expand(G['Nr'], G['Nth'], G['Nps']).contiguous()
    return g, Th_field, dict(a_r=a_r, b_r=b_r, Th_r=Th_r, M_MS=M)


# ---------------------------------------------------------------------------
# A smooth radial envelope of the body (1 inside the soliton, ->0 outside), used to
# localize deformations to the body so BCs at core/seal are untouched.
# ---------------------------------------------------------------------------
def body_envelope(G, rc, width=None):
    L = 1.0
    r = G['Rr']
    rcen = rc + 2.0*L
    w = width if width is not None else 1.5*L
    return torch.exp(-((r - rcen)/w)**2)


# ===========================================================================
# DEFORMED SEEDS.  Each returns (g_seed, Th_field, label).  amp = deformation size.
# We deform the round seed; the solver then relaxes under the FULL gauge-fixed
# Einstein system and we CLASSIFY the endpoint.
# ===========================================================================
def seed_multipole(G, base_g, base_Th, rc, l=2, amp=0.3):
    """l-th Legendre angular shaping of the spatial conformal factor: g_thth, g_psps
    and g_tt acquire a P_l(cos theta) modulation localized in the body.  l=1 dipole
    (up-down asymmetric), l=2 prolate/oblate, l=3,4 higher multipoles."""
    g = base_g.clone()
    env = body_envelope(G, rc)
    ct = torch.cos(G['Tht'])
    Pl = {1: ct,
          2: 0.5*(3*ct**2 - 1),
          3: 0.5*(5*ct**3 - 3*ct),
          4: 0.125*(35*ct**4 - 30*ct**2 + 3)}[l]
    mod = 1.0 + amp*env*Pl
    g[..., TH, TH] = base_g[..., TH, TH]*mod
    g[..., PS, PS] = base_g[..., PS, PS]*mod
    g[..., T, T]   = base_g[..., T, T]*(1.0 - 0.5*amp*env*Pl)
    return g, base_Th.clone(), f"multipole_l{l}_amp{amp}"


def seed_prolate_oblate(G, base_g, base_Th, rc, amp=0.4):
    """Strong prolate/oblate: stretch g_thth vs g_psps oppositely (a genuine spatial
    quadrupole shape, distinct from the conformal l=2)."""
    g = base_g.clone()
    env = body_envelope(G, rc)
    ct2 = torch.cos(G['Tht'])**2
    g[..., TH, TH] = base_g[..., TH, TH]*(1.0 + amp*env*(ct2 - 1.0/3))
    g[..., PS, PS] = base_g[..., PS, PS]*(1.0 - amp*env*(ct2 - 1.0/3))
    return g, base_Th.clone(), f"prolate_oblate_amp{amp}"


def seed_two_center(G, base_g, base_Th, rc, sep=2.0, amp=0.5):
    """Two-center on axis: the matter profile gets a second winding lump displaced
    along theta=0 and theta=pi (two cores), and g_tt deepens at both -- the canonical
    disconnected (multi-soliton) candidate."""
    g = base_g.clone()
    # deepen g_tt near both poles in the body (two potential wells)
    env = body_envelope(G, rc)
    ct = torch.cos(G['Tht'])
    twolobe = (torch.exp(-((ct-1.0)/0.5)**2) + torch.exp(-((ct+1.0)/0.5)**2))
    g[..., T, T] = base_g[..., T, T]*(1.0 - amp*env*twolobe)
    g[..., R, R] = base_g[..., R, R]*(1.0 + 0.3*amp*env*twolobe)
    # matter: add winding concentration at both poles
    Th = base_Th.clone()
    Th = Th*(1.0 + 0.2*amp*env*twolobe)
    return g, Th, f"two_center_amp{amp}"


def seed_ring(G, base_g, base_Th, rc, amp=0.5):
    """Ring / toroidal: deform so the matter and g_tt well concentrate on the EQUATOR
    (theta=pi/2) -- a toroidal lump, topologically/shape-distinct from the round core."""
    g = base_g.clone()
    env = body_envelope(G, rc)
    st = torch.sin(G['Tht'])
    ring = st**4                              # peaked at equator
    g[..., T, T] = base_g[..., T, T]*(1.0 - amp*env*ring)
    g[..., R, R] = base_g[..., R, R]*(1.0 + 0.3*amp*env*ring)
    Th = base_Th.clone()*(1.0 + 0.2*amp*env*ring)
    return g, Th, f"ring_amp{amp}"


def seed_large_amplitude(G, base_g, base_Th, rc, amp=0.6):
    """Large-amplitude breather-like: uniformly deepen the core well far beyond the
    round equilibrium (test for a second, more-bound branch)."""
    g = base_g.clone()
    env = body_envelope(G, rc, width=2.5)
    g[..., T, T] = base_g[..., T, T]*(1.0 - amp*env)
    g[..., R, R] = base_g[..., R, R]*(1.0 + amp*env)
    Th = base_Th.clone()
    return g, Th, f"large_amplitude_amp{amp}"


def seed_twist(G, base_g, base_Th, rc, amp=0.2):
    """Off-diagonal TWIST: turn on g_{r psi} (a spatial shear / rotation-like off-diag)
    localized in the body -- the non-axisymmetric / rotating candidate.  This directly
    populates a previously-zero off-diagonal so the solver must either relax it away
    (=> gauge/round) or settle to a genuinely twisted type."""
    g = base_g.clone()
    env = body_envelope(G, rc)
    st = torch.sin(G['Tht'])
    g[..., R, PS] = amp*env*st*G['Rr']
    g[..., PS, R] = g[..., R, PS]
    return g, base_Th.clone(), f"twist_rpsi_amp{amp}"


def all_seeds(G, base_g, base_Th, rc):
    """The full disconnected-type seed library."""
    seeds = []
    for l in (1, 2, 3, 4):
        seeds.append(seed_multipole(G, base_g, base_Th, rc, l=l, amp=0.3))
    seeds.append(seed_prolate_oblate(G, base_g, base_Th, rc, amp=0.4))
    seeds.append(seed_two_center(G, base_g, base_Th, rc, amp=0.5))
    seeds.append(seed_ring(G, base_g, base_Th, rc, amp=0.5))
    seeds.append(seed_large_amplitude(G, base_g, base_Th, rc, amp=0.6))
    seeds.append(seed_twist(G, base_g, base_Th, rc, amp=0.2))
    return seeds

#!/usr/bin/env python3
"""
solver_pack.py -- the 5-field <-> flat-vector pack/unpack reshape helpers.

NUMERIC-METHOD ONLY (no physics).  Extracted from full3d_solver.py (2026-06-25, the
solution-space-gate import-traceability cleanup) so the LIVE solver graph can borrow
pack/unpack WITHOUT transitively importing full3d_solver's physics surface (its legacy
residual_vector + round_seed, which pulls the 1-D spectral_radial_soliton solver).  These
are pure torch tensor reshapes -- they carry no boundary condition, ansatz, coupling, or
mechanism; every number stays traceable to the action + numeric methods.

full3d_solver.py re-exports `pack, unpack` from here, so its ~30 existing callers are
unaffected; new live-graph code imports them straight from this numeric-only module.
"""
import torch


def pack(a, b, c, d, Th):
    return torch.cat([a.reshape(-1), b.reshape(-1), c.reshape(-1),
                      d.reshape(-1), Th.reshape(-1)])


def unpack(u, G):
    n = G.Nr*G.Nth*G.Nps
    sh = (G.Nr, G.Nth, G.Nps)
    a = u[0:n].reshape(sh); b = u[n:2*n].reshape(sh); c = u[2*n:3*n].reshape(sh)
    d = u[3*n:4*n].reshape(sh); Th = u[4*n:5*n].reshape(sh)
    return a, b, c, d, Th

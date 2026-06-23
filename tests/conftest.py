"""Shared fixtures/helpers for the P1 purity harness.

Anti-hang: all tests are FORWARD residual/Einstein evals only (no Newton, no jacrev) on small
bounded grids (Nr<=24, single process); whole suite < 1s.
"""
import os, sys, math
# repo root on path (this file lives in <repo>/tests/)
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)
# match the operator module's CUDA/NVML workarounds BEFORE torch is touched downstream
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")

import torch
torch.set_default_dtype(torch.float64)
import pytest

from full3d_spectral import Grid3D, attach_coord_weight, PI


def make_grid(Nr=12, Nth=8, Nps=8, rc=0.05, cell=14.0):
    G = Grid3D(Nr=Nr, Nth=Nth, Nps=Nps, rc=rc, cell=cell)
    return attach_coord_weight(G)


@pytest.fixture(scope="session")
def grid():
    return make_grid()


@pytest.fixture(scope="session")
def offround_fields(grid):
    """A GENERIC OFF-ROUND background: every one of the 8 P1 fields nonzero, with
    theta- AND psi-dependence so NO DOF is decoupled by symmetry.  This is NOT a
    solution -- liveness only needs the residual to RESPOND to each DOF.  (MAP premise:
    a ROUND background would let symmetry false-flag the off-diagonals as 'dead'.)"""
    G = grid
    R, TH, PS = G.Rg, G.THg, G.PSg
    rmid = 0.5 * (G.rc + G.ri)
    bump = torch.exp(-((R - rmid) / 2.0) ** 2)
    sTH = torch.sin(TH)
    a = 0.05 * bump * torch.cos(TH)
    b = 0.04 * bump * (1.0 + 0.3 * torch.cos(PS))
    c = 0.03 * bump * sTH ** 2 * torch.cos(PS)
    d = 0.02 * bump * torch.cos(2 * PS)
    Th = 0.6 * PI * torch.exp(-((R - G.rc) / 3.0)) * (1.0 + 0.1 * sTH * torch.cos(PS))
    e_rt = 0.012 * bump * sTH
    e_rp = 0.009 * bump * sTH * torch.cos(PS)
    e_tp = 0.007 * bump * sTH ** 2 * torch.sin(PS)
    return [a, b, c, d, Th, e_rt, e_rp, e_tp]

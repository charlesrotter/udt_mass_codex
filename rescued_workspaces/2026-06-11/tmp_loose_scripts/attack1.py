# Independent attack: recompute curvature, check field signs, examine the kinetic-vs-field balance
# Reuse the script's machinery by importing the relevant pieces.
import numpy as np
from numpy import pi as PI

# --- ANALYTIC curvature of E_total at beta=0 ---
# kinetic(beta)=3*(cos^2 b * E_m1 + sin^2 b * E_p2) = 3*(E_m1 + sin^2 b *(E_p2-E_m1))
# d/db = 3*(E_p2-E_m1)*sin(2b); d2/db2 at 0 = 3*(E_p2-E_m1)*2 = 6*gap
gap = 3.8876-0.9428
print("kinetic curvature d2/db2 at 0 = 6*gap =", 6*gap)
# This is huge and POSITIVE -> kinetic strongly opposes deformation. Confirmed structurally.

# Field-energy terms scale: n2 ~ 2 cb sb (linear in beta near 0) -> Coulomb cross term ~ beta.
# But energy is quadratic form: E_coul has a term linear in n2*A2... A2 sourced by n2 (~beta), so E2 ~ beta^2.
# The off-diagonal density n2 ~ beta gives a CROSS Coulomb energy with the l=0 potential? NO - different multipoles orthogonal.
# So field energy correction is O(beta^2), same order as kinetic. Magnitude is what matters.
print("\nCoulomb total ~0.364 but the beta-dependent PART from 0.0->0.05:", 0.36393-0.36389)
print("kinetic part 0.0->0.05:", 2.85054-2.82847)
print("ratio field/kinetic change:", (0.36393-0.36389)/(2.85054-2.82847))

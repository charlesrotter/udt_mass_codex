"""Hostile monotonicity scan around c* (C3) + collar steepness fit on a
forming flow (C6)."""
import numpy as np
from el_core import classify, run_flow, threshold, SQ3

gamma = 1/3
cstar = 0.035057
# fine scan around threshold: any reentrant classification?
print("hostile scan around c* (gamma=1/3): 240 points in [0.9 c*, 1.1 c*]")
cs = np.linspace(0.9*cstar, 1.1*cstar, 240)
labs = []
for c in cs:
    lab, _ = classify(gamma, c, Tmax=80.0)
    labs.append(lab == 'TERM')
labs = np.array(labs)
switches = np.where(labs[1:] != labs[:-1])[0]
print(f"  transitions: {len(switches)} at c={[f'{cs[i+1]:.6f}' for i in switches]}")
print(f"  monotone single switch: {len(switches)==1}")

# coarse scan over decades (both sides far from threshold)
print("coarse scan, gamma=1/3:")
for c in [1e-5, 1e-4, 1e-3, 5e-3, 0.02, 0.03, 0.04, 0.1, 0.5, 2.0]:
    lab, _ = classify(gamma, c, Tmax=80.0)
    print(f"  c={c:<8g}: {lab}")

# also gamma=0.1 fine scan (independent monotonicity check)
cstar2 = 0.004075
cs2 = np.linspace(0.95*cstar2, 1.05*cstar2, 120)
labs2 = np.array([classify(0.1, c, Tmax=80.0)[0] == 'TERM' for c in cs2])
sw2 = np.where(labs2[1:] != labs2[:-1])[0]
print(f"gamma=0.1 scan: transitions={len(sw2)} (monotone: {len(sw2)==1})")

# ---- C6: steepness of a formed cavity: local exponent p(y) = F_t/F ----
# forming flow, gamma=1/3, c just above threshold; collar stretch
sol, sealed = run_flow(gamma, 0.036057, Tmax=80.0, dense=True)
tend = sol.t[-1]
ts = np.linspace(0.02*tend, 0.98*tend, 400)
u = sol.sol(ts)
p_loc = u[1]/u[0]   # d ln F / dt = -d ln F / d ln y  => F ~ y^-p
print(f"\nC6 fit: forming flow g=1/3 c=c*+1e-3 (t_seal={tend:.3f})")
print(f"  local exponent p = F_t/F: min={p_loc.min():.4f} max={p_loc.max():.4f}")
for fr in [0.1, 0.25, 0.5, 0.75, 0.9]:
    i = int(fr*len(ts))
    print(f"    t={ts[i]:6.3f} (y={np.exp(-ts[i]):.4g}): p={p_loc[i]:.4f}")
print(f"  q=1/3 collar would be p=0.3333; X1 fit range 0.42..0.76")
# global power-law fit over middle half
i0, i1 = len(ts)//4, 3*len(ts)//4
A = np.polyfit(-ts[i0:i1], np.log(u[0][i0:i1]), 1)
print(f"  global fit exponent over middle half: {-A[0]:.4f}")

"""Trimmed gamma sweep for the exponent fit (decade 0.01..0.1)."""
import numpy as np
from el_core import threshold

gammas = [0.1, 0.0562, 0.0316, 0.0178, 0.01]
cs = []
for g in gammas:
    guess = 0.5*g**2
    cst = threshold(g, 0.4*guess, 2.2*guess, tol_rel=5e-6, Tmax=80.0)
    cs.append(cst)
    print(f"gamma={g:.4f}  c*={cst:.8f}  c*/g^2={cst/g**2:.5f}", flush=True)
cs = np.array(cs); gammas = np.array(gammas)
p = np.polyfit(np.log(gammas), np.log(cs), 1)
print(f"log-log slope over decade: {p[0]:.4f}")
loc = (np.log(cs[-1]) - np.log(cs[-2]))/(np.log(gammas[-1]) - np.log(gammas[-2]))
print(f"local slope at small end: {loc:.4f}")
print(f"chat estimate (c*/g^2 at g=0.01): {cs[-1]/gammas[-1]**2:.5f}")

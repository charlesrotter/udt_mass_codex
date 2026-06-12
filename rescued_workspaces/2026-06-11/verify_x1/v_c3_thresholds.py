"""C3: reproduce threshold table entries + sanity of SAT/TERM phenomenology."""
import numpy as np
from el_core import classify, threshold, run_flow, SQ3

# --- sanity: what do flows look like far from threshold ---
for gamma, c in [(1/3, 0.001), (1/3, 0.2)]:
    lab, sol = classify(gamma, c)
    F, A = sol.y[0], sol.y[2]
    k = SQ3*A/F
    print(f"gamma={gamma:.4f} c={c}: {lab}; t_end={sol.t[-1]:.3f} "
          f"kappa_end={k[-1]:.6f} F_end={F[-1]:.4g} F_t/F_end={sol.y[1][-1]/F[-1]:.4f}")

# --- table reproduction ---
table = {0.1: 0.004075, 1/3: 0.035057, 0.5: 0.06916, 1.0: 0.20699}
print("\nthreshold table:")
for gamma, claimed in table.items():
    cst = threshold(gamma, claimed*0.5, claimed*2.0, tol_rel=5e-6)
    print(f"  gamma={gamma:<8.5f} c*_mine={cst:.6f}  c*_X1={claimed:.6f} "
          f" rel.diff={(cst-claimed)/claimed:+.2e}  c*/g^2={cst/gamma**2:.5f}")

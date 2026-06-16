import numpy as np
from spectral_radial_soliton import solve as rsolve
# (1) Stage A gate: recover #56 with exponential convergence + EL machine-zero
print("=== Stage A radial gate (independent re-run) ===")
prev=None
for N in [32,48,64,96]:
    out=rsolve(N,p=0.4,kap8=0.05,maxit=100)
    r=out['r'];body=(r>0.5)&(r<r[-1]-0.5)
    el=np.max(np.abs(out['res_thetaEL'][body]))
    print(f"  N={N}: M_MS={out['M_MS']:.6f} max|res_tt|body={np.max(np.abs(out['res_tt'][body])):.1e} max|EL|body={el:.1e} a0={out['a'][0]:.4f} b0={out['b'][0]:.4f}")

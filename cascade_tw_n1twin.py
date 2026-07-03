"""tw_n1twin.py -- FINAL bounded batch: refine the two crossings around the would-be N=1 twin
and classify each root's node count. 8-step bisections + 2 classification shots. Then STOP."""
import sys
import numpy as np
from scipy.integrate import solve_ivp
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from cell_solver_universe_T3 import rhs, PHI_C, make_risefall_slice, miss
from cascade_stageB_common import graded_count

M, Z = 3.0, 8.0
SHOTS = 0

def f_of(dp):
    global SHOTS
    a_param = 1.5*(1.0 + dp)
    U, Up, _ = make_risefall_slice(a_param, m=M)
    SHOTS += 1
    f, o = miss(Z, U, Up, 1.0)
    return f, o

def bisect(dlo, dhi, flo, fhi, steps=8):
    a_, b_, fa = dlo, dhi, flo
    for _ in range(steps):
        mid = 0.5*(a_ + b_)
        fm, om = f_of(mid)
        if not np.isfinite(fm): break
        if fa*fm <= 0: b_ = mid
        else: a_, fa = mid, fm
    return 0.5*(a_ + b_)

def classify(dp):
    global SHOTS
    a_param = 1.5*(1.0 + dp)
    U, Up, _ = make_risefall_slice(a_param, m=M)
    seal = lambda r, y, *aa: y[0]
    seal.terminal, seal.direction = True, +1
    SHOTS += 1
    sol = solve_ivp(rhs, (0.0, 5.0e7), [PHI_C, 0.0, 1.0, 0.0], args=(Z, Up),
                    method="LSODA", rtol=1e-10, atol=1e-12, events=[seal], dense_output=True)
    r_s = sol.t_events[0][0]
    rr = np.linspace(0.0, r_s, 200001)
    phi, phip, rho, rhop = sol.sol(rr)
    Nd, Nd_rng, _ = graded_count(rr[1:-1], (rho - 1.0)[1:-1])
    Np, Np_rng, _ = graded_count(rr[1:-1], rhop[1:-1])
    L = float(np.trapezoid(np.exp(phi), rr))
    print(f"  ROOT d'={dp:.7f} a={a_param:.9f}: N_delta={Nd} N_rhop={Np} rho_s={rho[-1]:.6f} "
          f"q={Z*rho[-1]**2*phip[-1]:.5f} L={L:.4f} r_s={r_s:.2f} rhop_s={rhop[-1]:+.2e}")

# crossing 1: (0.00655, 0.00660): miss -0.268 -> +0.232
d1 = bisect(0.00655, 0.00660, -0.268, +0.232)
classify(d1)
# crossing 2: (0.00660, 0.0068): miss +0.232 -> -2.03
d2 = bisect(0.00660, 0.0068, +0.232, -2.03)
classify(d2)
print(f"shots this script = {SHOTS}")

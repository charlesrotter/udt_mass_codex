"""tw_confirm.py -- classify the two new above-side roots (node counts, graduated floors)
+ map the near-miss arch where the N=1 twin should sit. 5 shots."""
import sys
import numpy as np
from scipy.integrate import solve_ivp
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from cell_solver_universe_T3 import rhs, PHI_C, make_risefall_slice, miss
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from cascade_stageB_common import graded_count

M, Z = 3.0, 8.0

def shoot_count(dp):
    a_param = 1.5*(1.0 + dp)
    U, Up, _ = make_risefall_slice(a_param, m=M)
    seal = lambda r, y, *aa: y[0]
    seal.terminal, seal.direction = True, +1
    sol = solve_ivp(rhs, (0.0, 5.0e7), [PHI_C, 0.0, 1.0, 0.0], args=(Z, Up),
                    method="LSODA", rtol=1e-10, atol=1e-12, events=[seal], dense_output=True)
    r_s = sol.t_events[0][0]
    rr = np.linspace(0.0, r_s, 200001)
    phi, phip, rho, rhop = sol.sol(rr)
    Nd, Nd_rng, _ = graded_count(rr[1:-1], (rho - 1.0)[1:-1])
    Np, Np_rng, _ = graded_count(rr[1:-1], rhop[1:-1])
    print(f"d'={dp:.7f} a={a_param:.8f}: N_delta={Nd} (floors {Nd_rng}), N_rhop={Np} (floors {Np_rng})")
    print(f"   rho_s={rho[-1]:.6f} q={Z*rho[-1]**2*phip[-1]:.5f} r_s={r_s:.2f} rhop_s={rhop[-1]:+.3e}")

print("== node classification of the two new above-side roots ==")
shoot_count(0.0055630)   # R1: outer-sealing
shoot_count(0.0058920)   # R2: inner-sealing

print("\n== near-miss arch mapping (would-be N=1 twin; below N=1 at d=0.0064619) ==")
for dp in (0.00645, 0.00650, 0.00660):
    a_param = 1.5*(1.0 + dp)
    U, Up, _ = make_risefall_slice(a_param, m=M)
    f, o = miss(Z, U, Up, 1.0)
    print(f"d'={dp:.5f}  miss={f:+.5e} [{o['status']}]"
          + (f" rho_s={o['rho_s']:.5f} q={o['q']:.4f}" if o["status"] == "seal" else ""))

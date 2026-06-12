"""Seal-shell thinness: test convention sensitivity (seal cutoff, log base,
c* value) to adjudicate my 0.747% vs X1's ~0.4%."""
import numpy as np
from scipy.integrate import solve_ivp
from el_core import rhs, ev_Fzero, SQ3

gamma = 1/3
c = 0.035057 + 1e-3

def shell_frac(kcut):
    def ev(t, u): return SQ3*u[2]/u[0] - kcut
    ev.terminal = True; ev.direction = 1
    sol = solve_ivp(rhs, (0, 80.0), [1.0, gamma, 0.0, c], method='LSODA',
                    events=[ev, ev_Fzero], rtol=1e-11, atol=1e-13,
                    dense_output=True, max_step=1.0)
    tend = sol.t[-1]
    ts = np.linspace(0, tend, 400001)
    u = sol.sol(ts)
    fmin = u[0]*(1 - SQ3*u[2]/u[0])
    # last downward crossing of 1 (robust to t=0 artifacts)
    below = fmin < 1.0
    # find last index where it transitions False->True and stays
    idx = np.where(~below[:-1] & below[1:])[0]
    tc = ts[idx[-1]+1]
    return tend, tc, (tend-tc)/tend

for kcut in [1-1e-3, 1-1e-6, 1-1e-9, 1-1e-12]:
    tend, tc, fr = shell_frac(kcut)
    print(f"seal cutoff kappa=1-{1-kcut:.0e}: t_seal={tend:.5f} t_cross={tc:.5f} "
          f"shell frac={fr*100:.3f}%")

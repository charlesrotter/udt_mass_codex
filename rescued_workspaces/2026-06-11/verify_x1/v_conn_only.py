"""Connection problem only (gamma-free), with chat bisection + kappa_inf probe."""
import numpy as np
from el_core import rhs, ev_seal, ev_Fzero, SQ3
from scipy.integrate import solve_ivp

def connection_classify(chat, xi_big=1e5, xi_min=1e-12, rtol=1e-10, atol=1e-15):
    F0 = 1 + 1/xi_big
    Ft0 = 1/xi_big
    a0 = (chat/3)/xi_big**2
    at0 = (2*chat/3)/xi_big**2
    Tmax = np.log(xi_big/xi_min)
    sol = solve_ivp(rhs, (0.0, Tmax), [F0, Ft0, a0, at0], method='LSODA',
                    events=[ev_seal, ev_Fzero], rtol=rtol, atol=atol, max_step=1.0)
    sealed = len(sol.t_events[0]) > 0
    kend = SQ3*sol.y[2][-1]/sol.y[0][-1]
    return ('TERM' if sealed else 'SAT'), kend

for xi_big, xi_min in [(1e4, 1e-10), (1e5, 1e-12), (1e6, 1e-12)]:
    lo, hi = 0.3, 0.8
    assert connection_classify(lo, xi_big, xi_min)[0] == 'SAT'
    assert connection_classify(hi, xi_big, xi_min)[0] == 'TERM'
    while hi - lo > 5e-7:
        mid = 0.5*(lo+hi)
        lab, _ = connection_classify(mid, xi_big, xi_min)
        if lab == 'TERM': hi = mid
        else: lo = mid
    print(f"xi_big={xi_big:g} xi_min={xi_min:g}: chat = {0.5*(lo+hi):.6f}", flush=True)

print("\nkappa_inf approach (xi_big=1e5):", flush=True)
for ch in [0.40, 0.45, 0.48, 0.495, 0.4988]:
    lab, kend = connection_classify(ch)
    print(f"  chat={ch:.5f}: {lab}, kappa_end={kend:.6f}", flush=True)

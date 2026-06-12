"""C3 part 2: gamma^2 collapse — fit exponent over a gamma decade, and solve
the gamma-free connection problem directly to get chat independently.

My re-derivation of the connection problem (done blind):
 - System in t = ln(1/y) is autonomous => scale invariant under y -> lam y.
 - Outer (y~1, kappa small): F ~ 1 + gamma(1/y - 1); a-eq linearizes:
   (y^2 a')' = 2a  =>  a = (c/3)(y^-2 - y) for jet a(1)=0, a'(1)=-c.
 - Inner scale y = gamma xi: equations identical in xi; gamma->0 limit:
   F -> (1+xi)/xi, incoming a -> (chat/3) xi^-2 (from c = chat gamma^2;
   the growing y-branch is O(gamma^3), drops out). gamma-free problem.
 - Deep (xi->0): F ~ 1/xi, a ~ k/xi; ride kappa_inf = sqrt(3) k.
   SAT iff kappa stays < 1.  Threshold = critical chat.
So I solve: integrate from xi_big with F=(1+xi)/xi, F'=-1/xi^2,
a=(chat/3)xi^-2, a'=-(2chat/3)xi^-3, inward; bisect chat on seal vs ride.
"""
import numpy as np
from el_core import threshold, run_flow, rhs, ev_seal, ev_Fzero, SQ3
from scipy.integrate import solve_ivp

# ---------- exponent fit over a decade ----------
gammas = np.array([0.1, 0.0707, 0.05, 0.0354, 0.025, 0.0177, 0.0125, 0.01])
cs = []
print("gamma sweep:")
for g in gammas:
    guess = 0.5*g**2
    cst = threshold(g, 0.4*guess, 2.2*guess, tol_rel=2e-6, Tmax=80.0)
    cs.append(cst)
    print(f"  gamma={g:.4f}  c*={cst:.8f}  c*/g^2={cst/g**2:.5f}")
cs = np.array(cs)
# log-log fit
p = np.polyfit(np.log(gammas), np.log(cs), 1)
print(f"\nglobal log-log slope over decade [0.01,0.1]: {p[0]:.4f}")
# local slope at small end
loc = (np.log(cs[-1]) - np.log(cs[-3]))/(np.log(gammas[-1]) - np.log(gammas[-3]))
print(f"local slope at small-gamma end: {loc:.4f}")
print(f"c*/g^2 at gamma=0.01: {cs[-1]/gammas[-1]**2:.5f}  (chat claim 0.4989)")

# ---------- direct gamma-free connection problem ----------
def connection_classify(chat, xi_big=1e5, xi_min=1e-12, rtol=1e-11, atol=1e-16):
    # integrate in tau = ln(xi_big/xi): same autonomous form as el_core
    # at xi_big: F=1+1/xi, F_t = -y dF/dy -> in xi var: F_t = xi*(1/xi^2)=1/xi
    F0 = 1 + 1/xi_big
    Ft0 = 1/xi_big          # F_t = -xi dF/dxi = -xi*(-1/xi^2)
    a0 = (chat/3)/xi_big**2
    at0 = (2*chat/3)/xi_big**2   # a_t = -xi da/dxi = -xi*(-2chat/3 xi^-3)
    Tmax = np.log(xi_big/xi_min)
    sol = solve_ivp(rhs, (0.0, Tmax), [F0, Ft0, a0, at0], method='LSODA',
                    events=[ev_seal, ev_Fzero], rtol=rtol, atol=atol, max_step=1.0)
    sealed = len(sol.t_events[0]) > 0
    kend = SQ3*sol.y[2][-1]/sol.y[0][-1]
    return ('TERM' if sealed else 'SAT'), sol, kend

lo, hi = 0.3, 0.8
assert connection_classify(lo)[0] == 'SAT'
assert connection_classify(hi)[0] == 'TERM'
while hi - lo > 1e-7:
    mid = 0.5*(lo+hi)
    lab, _, _ = connection_classify(mid)
    if lab == 'TERM': hi = mid
    else: lo = mid
chat_conn = 0.5*(lo+hi)
print(f"\nconnection-problem chat = {chat_conn:.6f}  (X1: 0.4989(2); test 1/2 exactly)")
# convergence check with bigger xi_big
lo, hi = chat_conn - 0.05, chat_conn + 0.05
def conn2(ch): return connection_classify(ch, xi_big=1e6, xi_min=1e-14)[0]
while hi - lo > 1e-7:
    mid = 0.5*(lo+hi)
    if conn2(mid) == 'TERM': hi = mid
    else: lo = mid
print(f"chat (xi_big=1e6) = {0.5*(lo+hi):.6f}")
# subcritical ride: kappa_inf vs chat (check kappa_inf -> 1 at threshold)
for ch in [0.40, 0.45, 0.48, chat_conn*0.999]:
    lab, sol, kend = connection_classify(ch)
    print(f"  chat={ch:.5f}: {lab}, kappa_end={kend:.6f}")

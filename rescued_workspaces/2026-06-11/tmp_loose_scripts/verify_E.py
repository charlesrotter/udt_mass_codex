import math
try:
    from scipy.integrate import solve_ivp
    HAVE = True
except ImportError:
    HAVE = False

def rhs(sign):
    def f(t, y):
        q, fv = y
        sloc = (1/3)*(1 - fv*(1-q))
        return [sign*(q*q - q + 2*sloc), sign*(-q*fv)]
    return f

if HAVE:
    for sign, lbl in [(+1, "outward t=+ln r"), (-1, "inward t=-ln r")]:
        ev = lambda t, y: abs(y[0]) - 1e6
        ev.terminal = True
        sol = solve_ivp(rhs(sign), [0, 6], [1/3, 1.0], rtol=1e-10, atol=1e-12,
                        dense_output=True, events=ev, max_step=0.01)
        print(f"-- {lbl} (scipy RK45, rtol=1e-10) --")
        for tm in [0.5, 1, 2, 3, 4]:
            if tm <= sol.t[-1]:
                q, fv = sol.sol(tm)
                sl = (1/3)*(1 - fv*(1-q))
                print(f"  t={tm}: q={q:.8f} f={fv:.6g} s_loc={sl:.8f} (s_loc-1/9={sl-1/9:+.4e})")
        if sol.t_events[0].size:
            print(f"  blow-up |q|>1e6 at t = {sol.t_events[0][0]:.4f}")
        else:
            print(f"  reached t={sol.t[-1]:.3f}, q_end={sol.y[0][-1]:.6f}, f_end={sol.y[1][-1]:.6g}")
# analytic sanity: at start (q=1/3, f=1): s_loc=1/9, dq/dt=0, df/dt=-1/3 != 0
print("start derivs:", rhs(+1)(0,[1/3,1.0]))
# inward asymptote check: q->1, f->inf, s_loc -> (1/3)(1 - f*0) = 1/3?? compute:
# as q->1, (1-q)->0 but f grows like e^{t}; product f(1-q)->? from run above

import numpy as np
from scipy.integrate import solve_ivp

print("="*70)
print("NUMERIC: integrate true ambient  Z(r^2 phi')' = 4 e^{-2phi} outward")
print("  autonomous in t=ln r:  u_tt = -u_t + (4/Z) e^{-2u}")
print("="*70)

def run(Z, u0, up0, tmax=40):
    # state y=[u, u_t]
    def f(t,y):
        u,ut = y
        return [ut, -ut + (4.0/Z)*np.exp(-2*u)]
    sol = solve_ivp(f,[0,tmax],[u0,up0],dense_output=True,rtol=1e-10,atol=1e-12,max_step=0.05)
    return sol

for Z in [1.0, 8.0]:
    print(f"\n--- Z_phi = {Z} ---")
    # start moderately deep (u small -> W large -> complex-root band) and integrate out
    sol = run(Z, u0=0.2, up0=0.1, tmax=60)
    ts = np.array([2,5,10,20,40,60])
    Wc = Z/32.0
    print(f"  critical W_crit=Z/32={Wc:.4f}, phi_crit={-0.5*np.log(Wc):.4f}")
    print("   t=lnr     phi_amb     W=e^-2phi    disc=1-32W/Z   root-type")
    for t in ts:
        u,ut = sol.sol(t)
        W = np.exp(-2*u)
        disc = 1 - 32*W/Z
        typ = "COMPLEX(osc)" if disc<0 else "REAL(power)"
        print(f"   {t:5.0f}   {u:9.4f}   {W:9.4e}   {disc:9.4f}   {typ}")
    # asymptotic check vs (1/2)ln((8/Z)t)
    u_far,_ = sol.sol(59)
    pred = 0.5*np.log((8.0/Z)*59)
    print(f"   asymptotic check @t=59: phi={u_far:.4f}  vs (1/2)ln((8/Z)t)={pred:.4f}  (log-log growth)")
    # crossover radius where W=W_crit
    from scipy.optimize import brentq
    g = lambda t: np.exp(-2*sol.sol(t)[0]) - Wc
    try:
        tstar = brentq(g, 0.1, 59)
        print(f"   crossover t*=ln r* = {tstar:.3f}  (r* = {np.exp(tstar):.3e}); for t>t* roots REAL -> clean tail")
    except Exception as e:
        # if already shallow everywhere or deep everywhere
        print("   crossover: W stays", "below" if g(1)<0 else "above", "W_crit in range")

print("\n" + "="*70)
print("EXACT-EULER (genuine DSI) TEST")
print("="*70)
print("  Operator Z(r^2 dphi')' + 8 W(r) dphi = 0 is EXACTLY scale-invariant (Euler)")
print("  iff W(r)=const. True W(r)=e^{-2phi_amb(r)} runs (shown: ~Z/(8 ln r) -> 0).")
print("  => NOT exactly Euler => NO genuine DSI. Frozen-W0 Euler is a LOCAL/WKB snapshot only.")
print("  Moreover W=const would require phi_amb=const = the P-forbidden asymptotic vacuum")
print("  (the very P discriminator). So the DSI-producing freeze assumes what P forbids.")

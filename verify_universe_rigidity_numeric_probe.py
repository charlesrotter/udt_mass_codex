"""T1 numeric probes (bounded, CPU). PROBE not proof.
(a) two-mirror attack: shoot from phi'(in)=0 with nonzero smooth S(r); can phi' return to 0
    at any r_out with anything nonconstant in between?  Track Phi = Z rho^2 phi' monotonicity.
(b) seal-fork counterexample: rho'=0-only seals (phi' free) -- exhibit a NONCONSTANT solution
    with rho'(in)=rho'(out)=0 and Delta-phi != 0.
"""
import numpy as np
from scipy.integrate import solve_ivp

Z = 8.0

def rhs(r, y, Sfun):
    phi, rho, phip, rhop = y
    e2m = np.exp(-2*phi)
    phipp = 4*e2m*rhop**2/(Z*rho**2) - 2*phip*rhop/rho
    rhopp = 2*phip*rhop - (Z/4)*rho*np.exp(2*phi)*phip**2 + Sfun(r, y)
    return [phip, rhop, phipp, rhopp]

print("== (a) two-mirror attack: phi'(in)=0, S = bump(s), scan ICs ==")
def bump(a, c, w):
    return lambda r, y: a*np.exp(-((r-c)/w)**2)
cases = []
for a in (+0.5, -0.5, +2.0, -2.0):
    for rhop0 in (0.0, 0.5, 1.0, -0.5):
        for phi0 in (0.0, 1.0, -1.0):
            cases.append((a, rhop0, phi0))
worst = None
for a, rhop0, phi0 in cases:
    Sf = bump(a, 3.0, 1.0)
    y0 = [phi0, 1.0, 0.0, rhop0]
    sol = solve_ivp(rhs, (1.0, 30.0), y0, args=(Sf,), rtol=1e-10, atol=1e-12,
                    max_step=0.01, dense_output=False, t_eval=np.linspace(1.0, 30.0, 6000))
    if not sol.success:
        # find where it died (rho->0 collapse typically)
        pass
    phi_, rho_, phip_, rhop_ = sol.y
    ok = rho_ > 0
    phi_, rho_, phip_, rhop_, tt = phi_[ok], rho_[ok], phip_[ok], rhop_[ok], sol.t[ok]
    Phi = Z*rho_**2*phip_
    dPhi = np.diff(Phi)
    monotone = dPhi.min() if dPhi.size else np.nan
    # after the solution first becomes nonconstant (Phi > tol), does phi' ever return to <= 0?
    tol = 1e-10
    idx = np.where(Phi > tol)[0]
    ret = np.nan
    if idx.size:
        later = phip_[idx[0]:]
        ret = later.min()   # min of phi' after activation; a return to 0 would show <= 0
    tag = f"S_amp={a:+.1f} rho'0={rhop0:+.1f} phi0={phi0:+.1f}"
    print(f"  {tag}: r_end={tt[-1]:6.2f} minDeltaPhi_step={monotone:+.2e} "
          f"min phi' after activation={ret:+.3e}")
    if worst is None or (not np.isnan(ret) and ret < worst):
        worst = ret
print(f"  -> WORST min phi' after activation over all cases: {worst:+.3e} (must be >0 for the claim)")

print()
print("== (b) rho'-only seal counterexample: phi'(in)=0.3, rho'(in)=0, S bump to fold rho' back to 0 ==")
# rho''(in) = -(Z/4) rho e^{2phi} phi'^2 < 0 -> rho' goes negative; a positive S bump can bring it back.
from scipy.optimize import brentq
def make(amp):
    Sf = bump(amp, 2.0, 0.6)
    y0 = [0.0, 1.0, 0.3, 0.0]
    sol = solve_ivp(rhs, (1.0, 6.0), y0, args=(Sf,), rtol=1e-11, atol=1e-13,
                    max_step=0.005, dense_output=True)
    return sol
def rhop_at_end_crossing(amp):
    """return max of rho' after the bump: if it crosses 0 again we have the seal."""
    sol = make(amp)
    t = np.linspace(2.5, 6.0, 2000)
    vals = sol.sol(t)
    return vals[3].max()   # rho' max after bump region
# find amp where rho' just re-crosses zero
lo, hi = 0.0, 5.0
sol_hi = make(hi)
amp = None
try:
    amp = brentq(rhop_at_end_crossing, 0.05, 5.0, xtol=1e-10)
    print(f"  marginal amp={amp:.6f} (rho' max returns exactly to 0)")
except ValueError:
    pass
# easier: pick an amp where rho' definitely re-crosses 0, find crossing point
amp_use = 2.0
sol = make(amp_use)
t = np.linspace(1.0, 6.0, 40000)
Y = sol.sol(t)
phi_, rho_, phip_, rhop_ = Y
# find first crossing of rho' from - to + after r=2.5 (post-bump)... we need rho'(r_out)=0
mask = t > 2.2
cross = np.where((rhop_[mask][:-1] < 0) & (rhop_[mask][1:] >= 0))[0]
if cross.size:
    i = np.where(mask)[0][cross[0]]
    r_out = t[i]
    print(f"  amp={amp_use}: rho'(1.0)=0 and rho'({r_out:.4f})={rhop_[i]:+.2e}  <- second rho'=0 seal")
    print(f"  at r_out: phi'={phip_[i]:+.5f} (NONZERO), Delta-phi = phi(out)-phi(in) = {phi_[i]-phi_[0]:+.5f}")
    print(f"  rho(in)=1.0 rho(out)={rho_[i]:.5f}  -> NONCONSTANT geometry with two rho'=0 ends")
else:
    print(f"  amp={amp_use}: no rho' zero-recrossing in window; rho' range post-bump:",
          rhop_[mask].min(), rhop_[mask].max())

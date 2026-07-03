"""bv15 X3 precision c2: even-part extraction at small eps, N=2^21 Simpson + N/2 error check.
c2 from fit of e(eps)/eps^2 = c2 + c4 eps^2 + c6 eps^4, e = (dS(+eps)+dS(-eps))/2 (exact
constraint handling). Compare against lambda(51200), lambda* (Richardson), lambda*/2.
"""
import numpy as np, json, os
import bv15_asm as asm
import bv15_x3_ray as ray
from scipy.optimize import brentq

SCR = os.path.dirname(os.path.abspath(__file__))

info, sol = asm.load_bg("B00")
U, _, _ = asm.makeU(info["a"], info["m"])
lam, al, be, us, vs, r_s = ray.get_mode(info, sol, 51200)
eps_set = [0.02, 0.03, 0.045, 0.06, 0.09, 0.12]
out = {"lam_grid": lam}
for NQ in (2**20, 2**21):
    ray.NQ = NQ
    S0 = ray.action(info, sol, us, vs, r_s, 0.0, 0.0, r_s, U)
    rows = []
    for e in eps_set:
        vals = {}
        for eps in (e, -e):
            a = eps * al
            f = lambda bb: ray.phi_eps_at(sol, r_s, us, vs, eps, bb)
            b1 = r_s + eps * be
            bex = brentq(f, b1 - 0.3, b1 + 0.3, xtol=1e-14, rtol=8.9e-16)
            vals[np.sign(eps)] = ray.action(info, sol, us, vs, r_s, eps, a, bex, U) - S0
        even = 0.5 * (vals[1.0] + vals[-1.0])
        rows.append((e, vals[1.0], vals[-1.0], even, even / e**2))
        print(f"NQ=2^{int(np.log2(NQ))} eps={e:.3f} dS+={vals[1.0]:+.6e} dS-={vals[-1.0]:+.6e}"
              f" even/e2={even/e**2:+.6e}")
    x = np.array([r[0] for r in rows]); y = np.array([r[4] for r in rows])
    A = np.vstack([np.ones_like(x), x**2, x**4]).T
    c, *_ = np.linalg.lstsq(A, y, rcond=None)
    print(f"  NQ=2^{int(np.log2(NQ))}: c2={c[0]:+.5e} c4={c[1]:+.5e} c6={c[2]:+.5e}")
    out[f"rows_{NQ}"] = rows
    out[f"fit_{NQ}"] = c.tolist()
lam_star = -6.33e-7
c2 = out[f"fit_{2**21}"][0]
print(f"c2/lam(51200) = {c2/lam:+.4f}   c2/lam* = {c2/lam_star:+.4f}   2c2/lam* = {2*c2/lam_star:+.4f}")
json.dump(out, open(os.path.join(SCR, "bv15_x3_c2.json"), "w"), indent=1)

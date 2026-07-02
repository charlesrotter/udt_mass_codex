import sys, json, time
sys.path.insert(0, "/tmp/claude-1000/-home-udt-admin-udt-mass-codex/749e82df-e440-4596-af14-d52dfbde5fed/scratchpad")
import numpy as np
import bv6_lib
from bv6_lib import shoot, diagnose, SHOTS, eval_piecewise
from scipy.integrate import solve_ivp

ROOTS = [("N1_below", 1.49030710407), ("N7_below", 1.49376717398),
         ("N20_below", 1.49657345446), ("N9_above", 1.50556166549)]


def shoot_method(a, method, rtol, atol):
    """Same chunked shooter but with a chosen method/tolerance (monkey-patch style)."""
    import bv6_lib as L
    orig = solve_ivp
    # simplest: temporarily wrap solve_ivp via module attribute
    def wrapped(fun, span, y0, **kw):
        kw["method"] = method
        kw["rtol"] = rtol
        kw["atol"] = atol
        return orig(fun, span, y0, **kw)
    L.solve_ivp = wrapped
    try:
        o = L.shoot(a, keep_sols=True)   # rtol/atol overridden by wrapper
    finally:
        L.solve_ivp = orig
    return o


t0 = time.time()
res = {}
for name, a in ROOTS:
    entry = {}
    for tag, method, rtol, atol in (("dop853_tight", "DOP853", 1e-12, 1e-14),
                                    ("radau", "Radau", 1e-10, 1e-12)):
        tt = time.time()
        o = shoot_method(a, method, rtol, atol)
        dt = time.time() - tt
        if o["status"] != "seal":
            entry[tag] = {"status": o["status"]}
            print(f"{name} {tag}: {o['status']} ({dt:.1f}s)")
            continue
        d = diagnose(o, nsamp=40001)
        entry[tag] = {"r_s": d["r_s"], "rho_s": d["rho_s"], "q": d["q"],
                      "rhop_s": d["rhop_s"],
                      "N_delta": d["counts"]["1x"]["N_delta"],
                      "N_rhop": d["counts"]["1x"]["N_rhop"],
                      "t": dt}
        print(f"{name} {tag}: r_s={d['r_s']:.8f} rho_s={d['rho_s']:.10f} "
              f"q={d['q']:.10f} rhop_s={d['rhop_s']:+.3e} "
              f"N={d['counts']['1x']['N_delta']}/{d['counts']['1x']['N_rhop']} ({dt:.1f}s)")
    res[name] = entry

# interleaving structure on the load-bearing N7 root (zeros of rho' precede zeros of delta?)
o = shoot(1.49376717398, keep_sols=True)  # baseline tolerances
rr = np.linspace(0.0, o["r_s"], 80001)[1:-1]
v = eval_piecewise(o["sols"], rr)
delta, rp = v[2] - 1.0, v[3]


def zero_locs(s, floor=1e-8):
    m = np.abs(s) > floor
    idx = np.where(m)[0]
    sg = np.sign(s[idx])
    ch = np.where(sg[1:] != sg[:-1])[0]
    return [0.5 * (rr[idx[c]] + rr[idx[c + 1]]) for c in ch]


zd, zp = zero_locs(delta), zero_locs(rp)
print(f"\nN7 interleaving: {len(zd)} delta-zeros at {['%.1f' % z for z in zd]}")
print(f"                 {len(zp)} rho'-zeros at {['%.1f' % z for z in zp]}")
merged = sorted([(z, "d") for z in zd] + [(z, "p") for z in zp])
pattern = "".join(t for _, t in merged)
print(f"merged pattern (p=rho', d=delta): {pattern}")

print(f"\ntime {time.time()-t0:.1f}s shots(this proc)={SHOTS['n']}")
json.dump(res | {"interleave_pattern_N7": pattern, "shots_this_proc": SHOTS["n"]},
          open("bv6_xcheck.json", "w"), indent=1, default=str)

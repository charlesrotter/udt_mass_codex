"""C4 floor audit: is N_rhop=118 (vs N_delta=126) a genuine inequality or my floor gating
out small genuine rho' lobes? Recount with graduated floors; inspect each Rolle-violating
dd-gap for a sub-floor rho' crossing and measure its amplitude vs integration noise."""
import numpy as np
from bv5_common import make_A3, shoot_bv5, eval_dense, count_zeros, SHOTS

Z = 8.0
b_star = 0.999148274122
U, Up = make_A3(b_star)
o = shoot_bv5(Z, Up, keep_segments=True)
assert o["status"] == "seal"
r_s, segs = o["r_s"], o["segments"]
print(f"b*={b_star}  r_s={r_s:.6f}  resid rho'_s={o['rhop_s']:+.3e}")

N = 300_000
rr = np.linspace(0.0, r_s, N)
y = eval_dense(segs, rr)
delta, rhop = y[2] - 1.0, y[3]
fl_d = max(1e-12, 1e-8*np.max(np.abs(delta)))
nd, pos_d, _ = count_zeros(rr, delta, fl_d)
print(f"N_delta = {nd} (floor {fl_d:.2e})")

print("\ngraduated rho' floors:")
for fl_p in (3.4e-6, 1e-6, 3e-7, 1e-7, 3e-8, 1e-8, 3e-9, 1e-9, 1e-10):
    np_, pos_p, lobe = count_zeros(rr, rhop, fl_p)
    merged = sorted([(x, "d") for x in pos_d] + [(x, "p") for x in pos_p])
    pat = "".join(t for _, t in merged)
    dd = sum(1 for a, b in zip(pat, pat[1:]) if a == b == "d")
    pp = sum(1 for a, b in zip(pat, pat[1:]) if a == b == "p")
    print(f"  floor={fl_p:.1e}: N_rhop={np_:4d}  min_lobe={lobe:.3e}  adj-dd={dd} adj-pp={pp}")

# inspect the dd-gaps at the reporting floor 3.4e-6
np_, pos_p, _ = count_zeros(rr, rhop, 3.4e-6)
merged = sorted([(x, "d") for x in pos_d] + [(x, "p") for x in pos_p])
print("\ndd-gap inspection (rho' behavior between adjacent delta-zeros with no counted"
      " rho' zero):")
for (x1, t1), (x2, t2) in zip(merged, merged[1:]):
    if t1 == t2 == "d":
        rz = np.linspace(x1, x2, 20000)
        rp = eval_dense(segs, rz)[3]
        print(f"  gap [{x1:.3f},{x2:.3f}] (len {x2-x1:.3f}): rho' range"
              f" [{rp.min():+.3e}, {rp.max():+.3e}]  sign changes(raw)="
              f"{int(np.sum(rp[1:]*rp[:-1] < 0))}")
# what happens right at the tail (last 5 merged zeros to the seal)?
tail0 = merged[-5][0]
rz = np.linspace(tail0, r_s, 40000)
rp = eval_dense(segs, rz)[3]
dl = eval_dense(segs, rz)[2] - 1.0
print(f"\ntail [{tail0:.2f}, r_s]: rho' range [{rp.min():+.3e},{rp.max():+.3e}],"
      f" raw sign changes rho'={int(np.sum(rp[1:]*rp[:-1] < 0))},"
      f" delta range [{dl.min():+.3e},{dl.max():+.3e}]")
print(f"SHOTS used this run: {SHOTS['n']}")

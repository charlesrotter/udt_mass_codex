"""bv11 V5: rho_s product law. 4 shots (above rungs N=8..11 at banked a*).
Below rho_s from banked cascade_stageB_rungs.json. A(N) = Lemma-D sqrt(Z)/Theta class:
A = sqrt(Z(1-x_c))/((N+1)pi + theta0), theta0 = 0.3209*pi (banked, Z=8 N=8);
also report the naive theta0=0 version."""
import json
import numpy as np
import bv11_lib as L

ABOVE = {8: 1.50587703866, 9: 1.50556166549, 10: 1.50526832529, 11: 1.50501146174}
banked = json.load(open("/home/udt-admin/udt_mass_codex/cascade_stageB_rungs.json"))
below = {r["N_delta"]: r for r in banked["rungs"]}

x_c = 1.0 / 1101.0
th0 = 0.3209 * np.pi
print(f"{'N':>2} {'rho_s_above':>12} {'rho_s_below':>12} {'prod-1':>12} "
      f"{'-3A^2':>12} {'ratio':>7} {'-3A0^2':>12} {'ratio0':>7}")
for N, a in ABOVE.items():
    o = L.shoot(a)
    assert o["status"] == "seal", o["status"]
    rsA = float(o["y_s"][2])
    rsB = below[N]["rho_s"]
    prod = rsA * rsB - 1.0
    A = np.sqrt(L.Z * (1 - x_c)) / ((N + 1) * np.pi + th0)
    A0 = np.sqrt(L.Z * (1 - x_c)) / ((N + 1) * np.pi)
    print(f"{N:>2} {rsA:12.6f} {rsB:12.6f} {prod:+12.6f} "
          f"{-3*A*A:+12.6f} {prod/(-3*A*A):7.3f} {-3*A0*A0:+12.6f} {prod/(-3*A0*A0):7.3f}")
    print(f"    |rho_s-1|: above {abs(rsA-1):.4f}  below {abs(rsB-1):.4f}  A={A:.4f} A0={A0:.4f}"
          f"  rhop_seal_resid={float(o['y_s'][3]):+.2e}")
print("shots:", L.SHOTS["n"])

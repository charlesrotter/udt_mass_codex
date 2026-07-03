"""bv11 V2: desert check, 4 shots at d' in {0.0078, 0.0160, 0.0230, 0.0300}.
(My scan already covers (0.0060,0.00718] -- monotone negative dive after the N=0 root;
banked blind probe covers (8.2e-3, 1.4e-2] with no sign change.)"""
import numpy as np
import bv11_lib as L

prev = None
for dp in (0.0078, 0.0160, 0.0230, 0.0300):
    f, o = L.miss_dp(dp)
    extra = ""
    if o["status"] == "seal":
        extra = f" rho_s={o['y_s'][2]:.4f} q={L.Z*o['y_s'][2]**2*o['y_s'][1]:.4f} r_s={o['r_s']:.1f}"
    print(f"d'={dp:.4f}  status={o['status']}  miss={f:+.4e}{extra}")
    if prev is not None and np.isfinite(prev) and np.isfinite(f) and prev * f < 0:
        print("  *** SIGN CHANGE -- desert REFUTED ***")
    prev = f
print("shots:", L.SHOTS["n"])

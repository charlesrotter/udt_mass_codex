"""C5: U'(1)=0 exactly at stuck points (numeric + FD cross-check) + stuck-point shots."""
import numpy as np
from bv5_common import make_A1, make_A3, make_A2, shoot_bv5, SHOTS

# --- U'(1) at the stuck parameters, via slice Up AND central finite difference of U ---
cases = [("A1 m=1 a=0.5",  make_A1(1.0, 0.5)),
         ("A1 m=3 a=1.5",  make_A1(3.0, 1.5)),
         ("A1 m=4 a=2.0",  make_A1(4.0, 2.0)),
         ("A3 b=1",        make_A3(1.0)),
         ("A2 k=3 a=2/3",  make_A2(3.0, 2.0/3.0)),
         ("A2 k=1 a=2",    make_A2(1.0, 2.0))]
h = 1e-6
for lab, (U, Up) in cases:
    fd = (U(1.0+h) - U(1.0-h)) / (2*h)
    print(f"{lab:16s}  Up(1) = {Up(1.0):+.3e}   FD dU/drho|_1 = {fd:+.3e}   U(1) = {U(1.0):.15f}")

# off-stuck sanity: Up(1) != 0 slightly off stuck
for lab, (U, Up) in [("A1 m=3 a=1.49", make_A1(3.0, 1.49)), ("A3 b=0.99", make_A3(0.99))]:
    print(f"{lab:16s}  Up(1) = {Up(1.0):+.6e}  (expect nonzero)")

# --- stuck-point shots, r_max=1e5, report what happens ---
shots = [("A1 m=3 a=1.5 Z=8", 8.0, make_A1(3.0, 1.5)),
         ("A1 m=3 a=1.5 Z=1", 1.0, make_A1(3.0, 1.5)),
         ("A3 b=1     Z=8",   8.0, make_A3(1.0)),
         ("A2 k=3 a=2/3 Z=8", 8.0, make_A2(3.0, 2.0/3.0))]
for lab, Z, (U, Up) in shots:
    o = shoot_bv5(Z, Up, r_max=1e5)
    extra = ""
    if o["status"] == "seal":
        extra = f" r_s={o['r_s']:.6g} rhop_s={o['rhop_s']:+.3e}"
    print(f"[stuck shot] {lab}: status={o['status']}{extra}")
print(f"SHOTS used: {SHOTS['n']}")

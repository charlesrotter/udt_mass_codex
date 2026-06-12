import numpy as np
# n=4 (and remaining) modes predicted in 1.35-1.9 GeV
hi_modes = sorted([1873.4, 1548.9, 1664.1, 1833.6, 1530.7, 1588.6, 1331.4])
hi_modes = [m for m in hi_modes if m>1350]
# Established/known light unflavored mesons 1.35-1.9 GeV (PDG)
mesons_hi = [1409.8,1426.4,1430,1453,1474,1505,1517,1525,1561,1623,1647,1670,1680,1720,1812,1816,1855,1870,1880]
print("UDT modes 1350-1900:", hi_modes)
A=np.array(mesons_hi)
for m in hi_modes:
    i=np.argmin(abs(m-A)); print(f"  {m:7.1f} -> nearest meson {A[i]:7.1f}  err {100*abs(m-A[i])/m:5.2f}%")
print(f"\nmesons in 1350-1900: {len(mesons_hi)} states = 1 per {(1900-1350)/len(mesons_hi):.0f} MeV (EVEN denser)")

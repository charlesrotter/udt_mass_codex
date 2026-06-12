import numpy as np

# UDT predicted modes (from the run)
P = np.array(sorted([132.9, 784.3, 1331.4, 973.6, 752.3, 1156.1, 548.0, 1270.6, 1184.1, 1022.8]))
print("P =", P)
C = 140.962

# === The script's meson list ===
O_script = dict(pi=134.98, eta=547.9, rho=775.3, omega=782.7, etap=957.8, a0_980=980.0, f0_980=990.0,
       phi=1019.5, h1_1170=1166.0, b1_1235=1229.5, a1_1260=1230.0, f2_1270=1275.5,
       f1_1285=1281.9, eta_1295=1294.0, pi_1300=1300.0, a2_1320=1318.2)
Ovals = np.array(sorted(O_script.values()))

def nn_rms(pred, obs):  # script metric: each obs -> nearest pred
    return np.sqrt(np.mean([min(abs(o-pred)/o)**2 for o in obs]))*100

print("\n=== Script metric (obs->nearest pred) on script list:", round(nn_rms(P,Ovals),3),"% over",len(Ovals),"obs")

# What does each observed map to?
for o in Ovals:
    i=np.argmin(abs(o-P)); print(f"  obs {o:7.1f} -> pred {P[i]:7.1f}  err {100*abs(o-P[i])/o:5.2f}%")

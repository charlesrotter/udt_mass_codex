import numpy as np
rng=np.random.default_rng(7)
# base eigenvalues E (in units before C)
E_units = np.array(sorted([132.9, 784.3, 1331.4, 973.6, 752.3, 1156.1, 548.0, 1270.6, 1184.1, 1022.8]))/140.962
A = np.array(sorted([134.98,547.9,775.3,782.7,957.8,980.0,990.0,1019.5,1166.0,1229.5,1230.0,1275.5,1281.9,1294.0,1300.0,1318.2]))
def nn_rms_pred(pred,obs): return np.sqrt(np.mean([min(abs(p-obs)/p)**2 for p in pred]))*100
def nn_rms_obs(pred,obs): return np.sqrt(np.mean([min(abs(o-pred)/o)**2 for o in obs]))*100

print("=== AXIS 2: is C tuned? scan C, find best ===")
print(f"{'C':>8} {'obs->pred':>10} {'pred->obs':>10}")
best=(1e9,0)
for C in np.arange(120,162,1.0):
    P=E_units*C
    a=nn_rms_obs(P,A); b=nn_rms_pred(P,A)
    if a<best[0]: best=(a,C)
    flag=" <== claimed C=140.96" if abs(C-141)<0.5 else ""
    if C%4<1 or flag: print(f"{C:8.1f} {a:10.2f} {b:10.2f}{flag}")
print(f"\nBest obs->pred RMS over C-scan: {best[0]:.2f}% at C={best[1]:.1f} (claimed 140.96)")

# fine scan around 141
print("\nfine scan:")
best=(1e9,0)
for C in np.arange(135,148,0.5):
    P=E_units*C; a=nn_rms_obs(P,A)
    if a<best[0]: best=(a,C)
print(f"Best in [135,148]: {best[0]:.2f}% at C={best[1]:.1f}")
# +-10%
for f in [0.9,0.95,1.0,1.05,1.1]:
    P=E_units*140.962*f
    print(f"C x{f:.2f} = {140.962*f:6.1f}: obs->pred={nn_rms_obs(P,A):5.2f}%  pred->obs={nn_rms_pred(P,A):5.2f}%")

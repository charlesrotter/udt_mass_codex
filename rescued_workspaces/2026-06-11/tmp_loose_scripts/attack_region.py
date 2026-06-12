import numpy as np
rng=np.random.default_rng(7)
P = np.array(sorted([132.9, 784.3, 1331.4, 973.6, 752.3, 1156.1, 548.0, 1270.6, 1184.1, 1022.8]))
# full meson list 130-1900 for honest density
A_all = np.array(sorted([134.98,547.9,775.3,782.7,957.8,980.0,990.0,1019.5,1166.0,1229.5,1230.0,
   1275.5,1281.9,1294.0,1300.0,1318.2,1409.8,1426.4,1474,1505,1517,1525,1561,1623,1647,1670,1680,1720]))
def nn_rms_pred(pred,obs): return np.sqrt(np.mean([min(abs(p-obs)/p)**2 for p in pred]))*100

print("=== Region decomposition (pred->obs err) against FULL meson density ===")
low=[p for p in P if p<1100]; high=[p for p in P if p>=1100]
print(f"LOW modes (<1100, SPARSE region): {[round(p) for p in low]}")
for p in low:
    i=np.argmin(abs(p-A_all)); print(f"   {p:7.1f} -> {A_all[i]:7.1f} ({100*abs(p-A_all[i])/p:.2f}%)")
print(f"   LOW pred->obs RMS = {nn_rms_pred(np.array(low),A_all):.2f}%")
print(f"HIGH modes (>=1100, DENSE region): {[round(p) for p in high]}")
print(f"   HIGH pred->obs RMS = {nn_rms_pred(np.array(high),A_all):.2f}%")

# NULL restricted to LOW region only (133-1100): is the sparse region match still significant?
A_low=A_all[A_all<1100]
print(f"\n=== Null in SPARSE region 133-1100 only ({len(A_low)} mesons, 1 per {(1100-133)/len(A_low):.0f} MeV) ===")
lo,hi=133,1100; n=len(low); udt=nn_rms_pred(np.array(low),A_low)
null=np.array([nn_rms_pred(np.sort(rng.uniform(lo,hi,n)),A_low) for _ in range(40000)])
print(f"UDT low-region={udt:.2f}%  null median={np.median(null):.2f}%  p={np.mean(null<=udt):.4f}")

# NULL in DENSE region 1100-1350
A_d=A_all[(A_all>=1100)&(A_all<1350)]
print(f"\n=== Null in DENSE region 1100-1350 ({len(A_d)} mesons, 1 per {(1350-1100)/len(A_d):.0f} MeV) ===")
udt=nn_rms_pred(np.array(high),A_d)
null=np.array([nn_rms_pred(np.sort(rng.uniform(1100,1350,len(high))),A_d) for _ in range(40000)])
print(f"UDT high-region={udt:.2f}%  null median={np.median(null):.2f}%  p={np.mean(null<=udt):.4f}")

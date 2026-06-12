import numpy as np
rng=np.random.default_rng(7)
P=np.array(sorted([132.9,784.3,1331.4,973.6,752.3,1156.1,548.0,1270.6,1184.1,1022.8]))
def rms_pred(p,o): return np.sqrt(np.mean([min(abs(x-o)/x)**2 for x in p]))*100
def rms_obs(p,o): return np.sqrt(np.mean([min(abs(x-p)/x)**2 for x in o]))*100

# f0(500)/sigma is a PDG-established (****) state at ~400-550, pole ~475. UDT has NOTHING between 133 and 548.
# In the SPARSE low region this is the biggest test - does UDT predict sigma?
print("UDT gap 133->548 = 415 MeV with NO predicted mode. f0(500) sigma (PDG ****) lives here.")
print("Nearest UDT mode to sigma(475):", P[np.argmin(abs(P-475))], "-> err", round(100*min(abs(475-P)/475),1),"%")

# Low-region null INCLUDING sigma
A_low_sig=np.array([134.98,475,547.9,775.3,782.7,957.8,980,990,1019.5])
low=np.array([p for p in P if p<1100])
udt=rms_obs(low,A_low_sig)  # obs->pred: does every low meson have a UDT mode?
print(f"\nLow mesons WITH sigma, obs->pred RMS={udt:.2f}% (sigma is the orphan)")
for o in A_low_sig:
    i=np.argmin(abs(o-low)); print(f"  meson {o:7.1f} -> UDT {low[i]:7.1f} ({100*abs(o-low[i])/o:.1f}%)")

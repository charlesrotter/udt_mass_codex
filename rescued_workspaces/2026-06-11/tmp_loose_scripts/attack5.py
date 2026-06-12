import numpy as np
rng=np.random.default_rng(7)
P = np.array(sorted([132.9, 784.3, 1331.4, 973.6, 752.3, 1156.1, 548.0, 1270.6, 1184.1, 1022.8]))
A = np.array(sorted([134.98,547.9,775.3,782.7,957.8,980.0,990.0,1019.5,1166.0,1229.5,1230.0,1275.5,1281.9,1294.0,1300.0,1318.2]))
def nn_rms_obs(pred,obs): return np.sqrt(np.mean([min(abs(o-pred)/o)**2 for o in obs]))*100
def nn_rms_pred(pred,obs): return np.sqrt(np.mean([min(abs(p-obs)/p)**2 for p in pred]))*100

print("=== AXIS 5: J^PC. The 10 modes are 1-fermion Dirac eigenvalues. The mesons:")
# J^PC of the named matches
jpc = {"pi":"0-+","eta":"0-+","rho":"1--","omega":"1--","a0/f0_980":"0++","phi":"1--",
       "h1":"1+-","b1":"1+-","f2":"1++/2++","a2":"2++"}
print("   matched mesons span 0-+,0++,1--,1+-,1++,2++ — 6 different J^PC.")
print("   A single Dirac eigenvalue E_n(kappa) carries no 2-body J^PC; mass-only match.")

# How many DISTINCT meson J^PC multiplets exist <1.35 GeV? The nonet structure means
# at EACH mass region there are SEVERAL states (the pile-up at 1.2-1.3 is 6+ states).
# So 'a prediction near 1270' is guaranteed to hit SOME meson regardless of physics.
print("\n   States in [1150,1330]:", sorted([x for x in A if 1150<=x<=1330]), f"= {sum(1 for x in A if 1150<=x<=1330)} mesons in 180 MeV")
print("   => any pred in 1150-1330 is within", round(100*40/1230,1),"% of a meson by density alone (1 per ~25 MeV)")

# === DENSITY-MATCHED null (Axis 3 fairer): sample random preds, but the obs are SO dense
# that we should test: how good is a random 10-set under pred->obs given the real meson density?
print("\n=== Density-aware null: random 10-set, scored pred->obs, in the same [133,1331] ===")
lo,hi=P.min(),P.max()
udt=nn_rms_pred(P,A)
null=np.array([nn_rms_pred(np.sort(rng.uniform(lo,hi,10)),A) for _ in range(40000)])
print(f"UDT pred->obs={udt:.2f}%  null median={np.median(null):.2f}%  p={np.mean(null<=udt):.4f}")
print(f"null 5th pct={np.percentile(null,5):.2f}%  1st pct={np.percentile(null,1):.2f}%")

# What fraction of random preds get every mode within 3%? (the 'every prediction within 3%' claim)
def all_within(pred,obs,tol): return all(min(abs(p-obs)/p)<=tol for p in pred)
frac3=np.mean([all_within(np.sort(rng.uniform(lo,hi,10)),A,0.03) for _ in range(40000)])
print(f"\nFraction of RANDOM 10-sets with ALL modes within 3% of a meson: {frac3:.4f}")
print(f"UDT all within 3%? {all_within(P,A,0.03)}")

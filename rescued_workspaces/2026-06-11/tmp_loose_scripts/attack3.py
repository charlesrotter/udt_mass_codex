import numpy as np
rng=np.random.default_rng(7)
P = np.array(sorted([132.9, 784.3, 1331.4, 973.6, 752.3, 1156.1, 548.0, 1270.6, 1184.1, 1022.8]))
A = np.array(sorted([134.98,547.9,775.3,782.7,957.8,980.0,990.0,1019.5,1166.0,1229.5,1230.0,1275.5,1281.9,1294.0,1300.0,1318.2]))

def nn_rms_obs(pred, obs):
    return np.sqrt(np.mean([min(abs(o-pred)/o)**2 for o in obs]))*100
def nn_rms_pred(pred, obs):  # HONEST: every prediction must hit a real meson
    return np.sqrt(np.mean([min(abs(p-obs)/p)**2 for p in pred]))*100

print("=== AXIS 3: metric direction + density ===")
print(f"UDT obs->pred RMS : {nn_rms_obs(P,A):.2f}%")
print(f"UDT pred->obs RMS : {nn_rms_pred(P,A):.2f}%  (this is what 'every prediction within 3%' should use)")
# pred->obs detail
for p in P:
    i=np.argmin(abs(p-A)); print(f"  pred {p:7.1f} -> obs {A[i]:7.1f}  err {100*abs(p-A[i])/p:5.2f}%")

# Mesons per 100 MeV in [130,1330]: density
print(f"\nMeson density: {len(A)} states over {A.max()-A.min():.0f} MeV = 1 per {(A.max()-A.min())/len(A):.0f} MeV")

# FAIR NULL: random predicted sets, scored with pred->obs (every random pred must also hit a real meson)
def null_pred(trials=20000):
    lo,hi=P.min(),P.max(); N=len(P); udt=nn_rms_pred(P,A)
    null=np.array([nn_rms_pred(np.sort(rng.uniform(lo,hi,N)),A) for _ in range(trials)])
    return udt, np.median(null),(null<=udt).mean()
u,m,p=null_pred()
print(f"\nFAIR NULL (pred->obs, every prediction scored): UDT={u:.2f}% null_med={m:.2f}% p={p:.4f}")

# SYMMETRIC metric (both directions averaged)
def sym(pred,obs): return 0.5*(nn_rms_obs(pred,obs)+nn_rms_pred(pred,obs))
def null_sym(trials=20000):
    lo,hi=P.min(),P.max(); N=len(P); udt=sym(P,A)
    null=np.array([sym(np.sort(rng.uniform(lo,hi,N)),A) for _ in range(trials)])
    return udt,np.median(null),(null<=udt).mean()
u,m,p=null_sym()
print(f"SYMMETRIC NULL: UDT={u:.2f}% null_med={m:.2f}% p={p:.4f}")

# How good is a TRIVIAL prediction: 10 evenly-spaced points in range?
even=np.linspace(P.min(),P.max(),10)
print(f"\nTrivial 10 evenly-spaced points: obs->pred={nn_rms_obs(even,A):.2f}%  pred->obs={nn_rms_pred(even,A):.2f}%")

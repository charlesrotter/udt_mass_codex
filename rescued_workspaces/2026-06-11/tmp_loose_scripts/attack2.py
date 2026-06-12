import numpy as np
rng=np.random.default_rng(7)
P = np.array(sorted([132.9, 784.3, 1331.4, 973.6, 752.3, 1156.1, 548.0, 1270.6, 1184.1, 1022.8]))
C=140.962

def nn_rms_obs(pred, obs):  # obs->nearest pred (script)
    return np.sqrt(np.mean([min(abs(o-pred)/o)**2 for o in obs]))*100
def nn_rms_pred(pred, obs):  # pred->nearest obs (the HONEST direction for "every prediction is real")
    return np.sqrt(np.mean([min(abs(p-obs)/p)**2 for p in pred]))*100

# ============ AXIS 1: meson list selection bias ============
# Honest full PDG light unflavored list in [130,1330]. Build several variants.
# Variant A: script list
A = [134.98,547.9,775.3,782.7,957.8,980.0,990.0,1019.5,1166.0,1229.5,1230.0,1275.5,1281.9,1294.0,1300.0,1318.2]
# Variant B: add f0(500)/sigma ~475 and rho/omega only-established core, drop the dense 1200-1320 pileup that isn't all "established"
B = [134.98, 475.0, 547.9, 775.3, 782.7, 957.8, 980.0, 1019.5, 1170.0, 1230.0, 1275.5, 1318.2]
# Variant C: ALL PDG entries incl f0(500),pi(1300)... and also include the kaon-like? no, unflavored only. Add eta(1405)? out of range.
C_list = [134.98, 475.0, 547.9, 775.3, 782.7, 957.8, 980.0, 990.0, 1019.5, 1166.0,
          1229.5, 1230.0, 1235.0, 1275.5, 1281.9, 1294.0, 1300.0, 1318.2]
# Variant D: drop the f0/a0 controversial scalars and h1/b1/a1 axials (keep only "clean" 0-+,1--,2++): pi,eta,eta',rho,omega,phi,f2,a2
D = [134.98, 547.9, 957.8, 775.3, 782.7, 1019.5, 1275.5, 1318.2]

def fullnull(obs, P, trials=20000, metric=nn_rms_obs):
    obs=np.array(sorted(obs)); lo,hi=P.min(),P.max(); N=len(P)
    udt=metric(P,obs)
    null=np.array([metric(rng.uniform(lo,hi,N),obs) for _ in range(trials)])
    return udt, np.median(null), (null<=udt).mean()

for name,L in [("A script",A),("B core+sigma",B),("C all+extra",C_list),("D clean JPC only",D)]:
    u,m,p = fullnull(L,P)
    print(f"{name:18s} n_obs={len(L):2d}  UDT_rms={u:5.2f}%  null_med={m:5.2f}%  p={p:.4f}")

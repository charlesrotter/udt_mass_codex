import numpy as np
# Claim 2 analytic: for 0<E<m and PHI<=0 (e^{2PHI}<=1):
# A+A- = E^2 e^{4PHI} - m^2 e^{2PHI} = e^{2PHI}(E^2 e^{2PHI} - m^2)
# Since e^{2PHI}<=1: E^2 e^{2PHI} <= E^2 < m^2  => (E^2 e^{2PHI} - m^2) < 0
# and e^{2PHI} > 0 => A+A- < 0 strictly. Then k^2 = A+A- - kappa^2/r^2 < 0. QED.
# Let's just sanity-check across a grid.
rng = np.random.default_rng(0)
N=200000
PHI = -np.abs(rng.normal(0,2,N))   # PHI<=0
E = rng.uniform(0,1,N)             # 0<E<m with m=1
m=1.0
kappa = rng.integers(1,5,N)
r = rng.uniform(0.01,100,N)
ApAm = E**2*np.exp(4*PHI) - m**2*np.exp(2*PHI)
k2 = ApAm - kappa**2/r**2
print("Among", N, "random points with PHI<=0, 0<E<m:")
print("  max A+A- =", ApAm.max(), "(should be < 0)")
print("  max k^2  =", k2.max(), "(should be < 0)")
print("  all A+A- <0 :", np.all(ApAm<0))
print("  all k^2  <0 :", np.all(k2<0))

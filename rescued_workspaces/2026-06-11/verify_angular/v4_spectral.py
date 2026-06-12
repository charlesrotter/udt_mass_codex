"""
V4 -- SPECTRAL CONSEQUENCE TEST (decisive, cheap): diagonal class vs
corrected class on the spherical collar f0 = y^{-qc}.

Derivation (verifier's own, from the V1/V1b-certified densities):
  diagonal (in-scheme):  L = (c/2)s[ r^2 dpT^2 - f0^2 r^2 Q_r - f0 ang ]
  corrected (flipped):   L = (c/2)s[ -r^2 dpT^2 - f0^2 r^2 Q_r + f0 ang ]
  Q_r = dpr^2 - 8 p0r dp dpr + 8 p0r^2 dp^2; ang -> lambda = l(l+1) dp^2.
  Symmetrized radial potential on the collar:
     V(y) = 4 (p0r f0^2 r^2)' + 8 p0r^2 f0^2 r^2 = 2 qc (1-qc) y^{-2qc}
  Define A_pm psi = -(y^{2-2qc} psi')' + V psi pm lambda y^{-qc} psi,
  weight W = y^2 (both classes). Mode dp = psi(y) Y_lm e^{-i w T}:
     DIAGONAL :  w^2 = +spec(A_+, W)   (centrifugal +lambda f0, repulsive)
     CORRECTED:  w^2 = -spec(A_-, W)   (time weight flipped AND
                                        centrifugal -lambda f0, attractive)
  => in the corrected class, REAL-frequency (oscillation) modes exist
     iff A_- has NEGATIVE directions, i.e. iff the attractive angular
     term beats kinetic+V; everything else is exponential (relaxation).
Dirichlet on [y0, 1]; FD self-adjoint discretization; float64.
Also: gauge-profile residual test (psi = p0r ~ 1/y) and an l-sweep.
"""
import numpy as np
from scipy.linalg import eigh

def spec_Apm(qc, lam, sign, y0=0.118303, N=3000, nev=6):
    yy = np.linspace(y0, 1.0, N + 2)
    h = yy[1] - yy[0]
    yi = yy[1:-1]
    p = lambda Y: Y**(2 - 2*qc)
    Vd = 2*qc*(1 - qc)*yi**(-2*qc) + sign*lam*yi**(-qc)
    main = (p(yi + h/2) + p(yi - h/2))/h**2 + Vd
    off = -p(yi[:-1] + h/2)/h**2
    A = np.diag(main) + np.diag(off, 1) + np.diag(off, -1)
    Wm = yi**2
    # symmetric reduction: B = W^{-1/2} A W^{-1/2}
    s = 1/np.sqrt(Wm)
    B = A*s[:, None]*s[None, :]
    ev = eigh(B, eigvals_only=True, subset_by_index=[0, nev - 1])
    return ev, (yi, s)

print("collar f0 = y^{-qc}; Dirichlet [y0, 1]; weight y^2")
for qc in (0.4, 1.0):
    for y0 in (0.118303, 0.01):
        print(f"\n===== qc = {qc}, y0 = {y0} =====")
        print(" l  lam | diag w^2 (lowest 3, = +eig A_+) "
              "| corr w^2 (highest 3, = -eig A_-) | corr osc modes?")
        for l in range(0, 7):
            lam = l*(l + 1)
            evp, _ = spec_Apm(qc, lam, +1, y0=y0)
            evm, _ = spec_Apm(qc, lam, -1, y0=y0)
            w2_diag = evp[:3]
            w2_corr = -evm[:3]          # most positive corrected w^2
            nosc = int(np.sum(evm < 0)) # negative directions of A_- among nev
            print(f" {l}  {lam:3d} | {w2_diag[0]:9.3f} {w2_diag[1]:9.3f} "
                  f"{w2_diag[2]:9.3f} | {w2_corr[0]:9.3f} {w2_corr[1]:9.3f} "
                  f"{w2_corr[2]:9.3f} | "
                  f"{'YES x%d' % nosc if nosc > 0 else 'no (all relaxational)'}")

# l-threshold scan at qc=0.4, both domains: smallest l with a negative
# direction of A_- (= real-frequency oscillation candidate in corrected)
print("\nthreshold scan: smallest l with corrected oscillation candidate")
for qc in (0.4, 1.0):
    for y0 in (0.118303, 0.05, 0.01):
        lc = None
        for l in range(1, 40):
            evm, _ = spec_Apm(qc, l*(l + 1), -1, y0=y0, nev=2)
            if evm[0] < 0:
                lc = l
                break
        print(f"  qc={qc}, y0={y0}: l_crit = {lc}")

# gauge-profile residual: is psi = 1/y (prop. to p0r) an interior zero
# mode of the corrected static operator A_- at l(l+1)=2?  (G3 says the
# chart-preserving direction is NOT null; verify on the collar.)
qc = 0.4
y0 = 0.118303
N = 4000
yy = np.linspace(y0, 1.0, N)
psi = 1/yy
def apply_Am(qc, lam, yy, psi):
    h = yy[1] - yy[0]
    p = yy**(2 - 2*qc)
    dpsi = np.gradient(psi, h)
    flux = p*dpsi
    out = -np.gradient(flux, h)
    out += (2*qc*(1 - qc)*yy**(-2*qc) - lam*yy**(-qc))*psi
    return out
res = apply_Am(qc, 2.0, yy, psi)[10:-10]
scale = np.max(np.abs((2*qc*(1 - qc)*yy**(-2*qc) + 2*yy**(-qc))*psi))
print(f"\ngauge-profile test psi = 1/y, l=1: max|A_- psi|/scale = "
      f"{np.max(np.abs(res))/scale:.3e}  (0 would mean the d_z direction "
      "is a corrected zero mode; nonzero = consistent with G3 breaking)")

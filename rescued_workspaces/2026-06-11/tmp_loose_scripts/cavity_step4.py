"""EXTERIOR-SOURCED CAVITY, step 4 (scratch): independent FD eigensolve
of the FULL two-sided problem (matter cell + mirrored medium exterior,
smooth background, gamma_eff = 0):
  (r^2 f^2 u')' - [lam f + (4-2n) s f^2] u = w2 r^2 u,  f = (R/r)^q all r
(uses E0 = s/r^2 both sides => (4-2n) r^2 f^2 E0 = (4-2n) s f^2).
Verdict check: top eigenvalue < 0 (relaxation only), domain-stable.
Plus: null-test record on the 2.998229-vs-3 proximity.
"""
import numpy as np
import scipy.sparse as sps
from scipy.sparse.linalg import eigsh

PASS = 0; FAIL = 0
def check(label, ok):
    global PASS, FAIL
    print(f"[{'PASS' if ok else 'FAIL'}] {label}")
    if ok: PASS += 1
    else: FAIL += 1

q = 1/3; s = q*(1-q)/2

def fd_top(m, lam, rmin=1e-5, rmax=40.0, n=24000, k=3):
    rg = np.exp(np.linspace(np.log(rmin), np.log(rmax), n))
    h = np.diff(rg); rm = 0.5*(rg[:-1]+rg[1:])
    fm = rm**(-q)             # R=1; f = (R/r)^q globally (smooth mirror)
    Pm = rm**2*fm**2
    Qm = lam*fm + m*fm**2     # m = (4-2n)s
    Wm = rm**2
    N = len(rg)
    Qn = np.zeros(N); Wn = np.zeros(N)
    Qn[:-1] += Qm*h/2; Qn[1:] += Qm*h/2
    Wn[:-1] += Wm*h/2; Wn[1:] += Wm*h/2
    cp = Pm/h
    dg = np.zeros(N); dg[:-1] += cp; dg[1:] += cp
    idx = np.arange(1, N-1)   # Dirichlet truncation both ends
    Kd = dg[idx] + Qn[idx]; Ko = -cp[1:len(idx)]
    A = -sps.diags([Ko, Kd, Ko], [-1, 0, 1], format='csc')
    W = sps.diags(Wn[idx], 0, format='csc')
    return np.sort(eigsh(A, k=k, M=W, sigma=10.0, which='LM',
                         return_eigenvectors=False))[::-1]

for lam, m, tag in ((2.0, 2*s, "screened n=1"), (2.0, 4*s, "n=0 control"),
                    (6.0, 2*s, "screened n=1")):
    t40 = fd_top(m, lam, rmax=40.0)
    t80 = fd_top(m, lam, rmax=80.0, n=30000)
    print(f"   lam={lam:g} [{tag}]: top w2 = {t40[0]:+.6f} (rmax=40), "
          f"{t80[0]:+.6f} (rmax=80); ratio {t40[0]/t80[0]:.3f}")
    check(f"FULL two-sided FD lam={lam:g} [{tag}]: top eigenvalue "
          "NEGATIVE at rmax=40 and 80 — no real-omega mode; "
          "negative top is a box artifact scaling away (>=1.5x under "
          "doubling): RELAXATION ONLY, independent of shooting",
          t40[0] < 0 and t80[0] < 0 and t40[0]/t80[0] > 1.5)

# null-test record
sf = 2.998229
check(f"null-test record: static shortfall {sf} is NOT 3 "
      f"(off {abs(sf-3)/3:.3%}) — recorded as a NON-match "
      "(small-rational coverage caveat; the 2.0075 history)",
      abs(sf-3) > 1e-3)

print(f"\nSTEP4: {PASS} PASS / {FAIL} FAIL")
import sys; sys.exit(1 if FAIL else 0)
